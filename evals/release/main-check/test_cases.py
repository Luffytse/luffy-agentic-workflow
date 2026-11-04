#!/usr/bin/env python3
"""Self-test of the release main-check case: the rendered fixture says what the case means, and builder and scorer agree.

Run: python3 evals/release/main-check/test_cases.py
It builds the fixture and checks the rendered input a Release thread reads (main's script and history, the merged
pull requests, the Milestone issue, the issue bodies) makes each expected verdict decidable from main. Then it writes
a reference run by hand from the expected outcome and scores it: the reference must pass, and planted wrong runs (the
planned feature closed, the later-Milestone issue edited or given a row, the section missing, a wrong verdict, an
unchecked issue ranked, a close with no evidence, an already-fixed issue closed as not planned, the feature it blocks
left out, the closes made after the release issue) must fail. It is not a
model run of the skill: see evals/release/README.md and RESULTS.md for the model runs.
"""
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from main_case import EXPECT  # noqa: E402
import make_fixture  # noqa: E402

TITLES = {20: "Quiet flag", 21: "Shout flag", 22: "Help flag", 30: "Typo in usage text", 31: "Names with spaces are cut at the first space",
          32: "--version always prints 0.0.0", 33: "test.sh does not test bye", 34: "greet sometimes fails",
          45: "Colour output"}
ROWS = {20: "still valid", 21: "already fixed: main's src/greet.sh takes `-s` since #8", 22: "still valid",
        30: "already fixed: main's usage line in src/greet.sh says `hello` since #7",
        31: "changed scope: #9 fixed `hello`; `bye` still cuts the name in src/greet.sh",
        32: "obsolete: #10 dropped `--version` from src/greet.sh",
        33: "still valid", 34: "cannot tell: no command, output or steps to reproduce the failure"}
CLOSE_REASON = {30: "Fixed on main by #7: src/greet.sh's usage line says hello.",
                32: "Obsolete: #10 removed --version from src/greet.sh."}
NEW_31 = ("`greet.sh bye` drops everything after the first space of the name:\n\n"
          "- `greet.sh bye \"Ada Lovelace\"` prints `Goodbye, Ada!`\n\n"
          "Each should print the whole name.\n\n"
          "Scope changed after a check against main: `hello` keeps the whole name since #9; only `bye` is left.")


def block(k, op, issue, fields):
    return f"### {k}. {op}\nIssue: {issue}\n{fields}\n"


def reference(rows=None, closes=None, edits=None, order=None, section=True, plan_first=False, report="#21",
              question=True, left="None.", path="", outcome="completed"):
    rows = dict(ROWS) if rows is None else rows
    closes = dict(CLOSE_REASON) if closes is None else closes
    edits = {31: NEW_31} if edits is None else edits
    order = EXPECT["order"] if order is None else order
    checks = []
    if question:
        checks.append(("Comment on an issue", "21-x.md",
                       "Body:\n~~~\nChecked against main: main already does this since #8 (src/greet.sh `-s`). "
                       "Close this planned feature?\n~~~"))
    for n, reason in sorted(closes.items()):
        checks.append(("Close", f"{n:02d}-x.md", f"Outcome: {outcome}\nReason: {reason}"))
    for n, text in sorted(edits.items()):
        checks.append(("Edit an issue body", f"{n:02d}-x.md", f"Body:\n~~~\n{text}\n~~~"))
    lines = "\n".join(f"{j}. #{n} {TITLES[n]}: taken for its group and place in the ranked list." for j, n in enumerate(order, 1))
    checked = "\n".join(f"- #{n} {TITLES[n]}: {v}" for n, v in sorted(rows.items()))
    sec = f"## Checked against main\n\nMain: `abc1234`.\n\n{checked}\n\n" if section else ""
    body = (f"**Goal:** Quiet output.\n\n**Label:** `release-3`. Every issue in this Release carries it.\n\n"
            f"**Milestone:** #1\n\n**Size:** 5. Used: {len(order)}.\n\n## Order\n\n{lines}\n\n## Left out\n\n{left}\n\n"
            f"{sec}## Proposed to the user\n\nNone.\n\n## Notes\n\nPosted when cut.\n")
    plan = [("Create an issue", "new (60-release-3.md)", f"Title: Release 3\nLabels: none\nParent: none\nBody:\n~~~\n{body}~~~"),
            ("Create a label", "none", "Label: release-3")]
    plan += [("Apply / remove labels", f"{n:02d}-x.md", "Add: release-3\nRemove: none") for n in order]
    seq = plan + checks if plan_first else checks + plan
    seq = [(op, path + issue if issue[0].isdigit() else issue, f) for op, issue, f in seq]
    return "\n".join(block(k, *b) for k, b in enumerate(seq, 1)), report


class Fixture(unittest.TestCase):
    """The rendered input says what each case means."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.repo = make_fixture.build(pathlib.Path(cls.tmp.name) / "out")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def sh(self, *args):
        return subprocess.run(["bash", "src/greet.sh", *args], cwd=self.repo, capture_output=True, text=True)

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, text=True).stdout

    def issue(self, n):
        return next((self.repo / ".scratch/issues").glob(f"{n:02d}-*.md")).read_text()

    def test_fixed_bug_30_is_fixed_on_main_by_7(self):
        usage = self.sh().stderr
        self.assertIn("hello|bye", usage)
        self.assertNotIn("helo|", usage)
        self.assertIn("helo|bye", self.git("show", "HEAD~4:src/greet.sh"))  # before #7
        self.assertIn("helo", self.issue(30))
        self.assertIn("#30", (self.repo / ".scratch/pulls/7.md").read_text())

    def test_changed_scope_bug_31_half_fixed_by_9(self):
        self.assertEqual(self.sh("hello", "Ada Lovelace").stdout.strip(), "Hello, Ada Lovelace!")
        self.assertEqual(self.sh("bye", "Ada Lovelace").stdout.strip(), "Goodbye, Ada!")
        body = self.issue(31)
        self.assertIn("`greet.sh hello \"Ada Lovelace\"` prints `Hello, Ada!`", body)
        self.assertIn("`greet.sh bye \"Ada Lovelace\"` prints `Goodbye, Ada!`", body)
        self.assertIn("`bye` is unchanged", (self.repo / ".scratch/pulls/9.md").read_text())

    def test_obsolete_bug_32_its_option_is_gone(self):
        r = self.sh("--version")
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("0.0.0", r.stdout)
        self.assertIn("--version", self.issue(32))
        self.assertIn("--version", (self.repo / ".scratch/pulls/10.md").read_text())

    def test_planned_feature_21_already_done_on_main(self):
        self.assertEqual(self.sh("-s", "hello", "Ada").stdout.strip(), "HELLO, ADA!")
        self.assertIn("`greet.sh -s hello Ada` prints `HELLO, ADA!`", self.issue(21))
        ms = self.issue(1)
        self.assertRegex(ms, r"\| #21 Shout flag \|")
        self.assertIn("Status: open", self.issue(21))

    def test_planned_feature_22_blocked_by_30_and_not_on_main(self):
        body = self.issue(22)
        self.assertIn("Blocked by: 30-usage-typo.md", body)
        self.assertIn("Status: open", body)
        self.assertIn("Status: open", self.issue(30))
        self.assertRegex(self.issue(1), r"\| #22 Help flag \|")
        self.assertNotIn("-h", (self.repo / "src/greet.sh").read_text())
        self.assertEqual(self.sh("-h").returncode, 2)  # no -h yet: it prints the usage line as an error
        # the dry-run tracker reads a blocker closed as not planned as uncleared, as the tracker doc does
        self.assertIn("unless it has a `Closed as: not planned` line",
                      (self.repo / "docs/dev-skills/issue-tracker.md").read_text())

    def test_valid_issues_20_and_33_still_true_on_main(self):
        self.assertNotIn("-q", (self.repo / "src/greet.sh").read_text())
        self.assertRegex(self.issue(1), r"\| #20 Quiet flag \|")
        self.assertNotIn("bye", (self.repo / "test.sh").read_text())

    def test_unreadable_34_names_no_command_or_output(self):
        body = self.issue(34).split("\n\n", 1)[1].split("## Comments")[0]
        self.assertNotIn("`", body)
        self.assertNotIn("greet.sh", body)

    def test_later_milestone_45_left_to_next_milestone(self):
        self.assertRegex(self.issue(1), r"## Excluded[\s\S]*- #45 Colour output: left to the next Milestone\.")
        self.assertNotIn("milestone-1", self.issue(45).split("\n")[2])
        self.assertIn("--version", self.issue(45))  # a check would find it changed: the case tests it is not checked

    def test_merges_close_no_issue_and_main_is_ahead_of_release_2(self):
        for n in (7, 8, 9, 10):
            text = (self.repo / f".scratch/pulls/{n}.md").read_text()
            self.assertNotRegex(text, r"(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?) #\d+")
            sha = re.search(r"Merge commit: (\w+)", text).group(1)
            self.assertEqual(subprocess.run(["git", "-C", str(self.repo), "merge-base", "--is-ancestor", sha, "main"]).returncode, 0)
        for n in (20, 21, 22, 30, 31, 32, 33, 34, 45):
            self.assertIn("Status: open", self.issue(n))
        self.assertIn("Status: closed", self.issue(2))
        self.assertIn("retro-planning ran for this Release.", self.issue(2))
        self.assertEqual(self.git("log", "--format=%s", "-4").split("\n")[:4],
                         ["chore: drop --version (#10)", "fix: hello keeps the whole name (#9)",
                          "feat: -s shouts the greeting (#8)", "fix: usage line says hello (#7)"])

    def test_test_sh_passes(self):
        self.assertEqual(subprocess.run(["bash", "test.sh"], cwd=self.repo, capture_output=True).returncode, 0)


class Scorer(unittest.TestCase):
    def score(self, **wrong):
        with tempfile.TemporaryDirectory() as t:
            repo = make_fixture.build(pathlib.Path(t) / "out")
            actions, report = reference(**wrong)
            (repo / ".scratch/proposed-actions.md").write_text(actions)
            (repo / ".scratch/report.md").write_text(f"Asked the user: {report} Shout flag is done on main (#8); close it?\n")
            return subprocess.run([sys.executable, str(HERE / "score.py"), str(repo.parent)], capture_output=True, text=True)

    def test_reference_passes(self):
        r = self.score()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_planned_feature_closed_fails(self):
        self.assertEqual(self.score(closes={**CLOSE_REASON, 21: "Done on main by #8."}).returncode, 1)

    def test_planned_feature_not_asked_fails(self):
        self.assertEqual(self.score(report="nothing").returncode, 1)

    def test_planned_feature_question_not_on_the_issue_fails(self):
        self.assertEqual(self.score(question=False).returncode, 1)

    def test_left_out_line_for_waiting_and_unchecked_issues_passes(self):
        left = "- #21 Shout flag: waits on the user.\n- #34 greet sometimes fails: unchecked."
        r = self.score(left=left)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_issue_lines_given_as_paths_pass(self):
        r = self.score(path=".scratch/issues/")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_planned_feature_closed_through_a_path_fails(self):
        self.assertEqual(self.score(path=".scratch/issues/", closes={**CLOSE_REASON, 21: "Done on main by #8."}).returncode, 1)

    def test_later_milestone_issue_edited_fails(self):
        self.assertEqual(self.score(edits={31: NEW_31, 45: "Colour output, without the --version part."}).returncode, 1)

    def test_later_milestone_issue_given_a_row_fails(self):
        self.assertEqual(self.score(rows={**ROWS, 45: "changed scope: #10 dropped --version"}).returncode, 1)

    def test_missing_section_fails(self):
        self.assertEqual(self.score(section=False).returncode, 1)

    def test_wrong_verdict_fails(self):
        r = self.score(rows={**ROWS, 31: "still valid"}, edits={})
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.score(rows={**ROWS, 30: "still valid"}, closes={32: CLOSE_REASON[32]}).returncode, 1)

    def test_unchecked_issue_ranked_fails(self):
        self.assertEqual(self.score(order=EXPECT["order"] + [34]).returncode, 1)

    def test_close_without_evidence_fails(self):
        self.assertEqual(self.score(closes={**CLOSE_REASON, 30: "No longer happens."}).returncode, 1)
        self.assertEqual(self.score(rows={**ROWS, 32: "obsolete"}).returncode, 1)

    def test_fixed_issue_closed_as_not_planned_fails(self):
        self.assertEqual(self.score(outcome="not planned").returncode, 1)

    def test_feature_blocked_by_the_fixed_issue_left_out_fails(self):
        left = "- #22 Help flag: blocked by #30, closed as not planned, which never clears."
        self.assertEqual(self.score(order=[20, 31, 33], left=left).returncode, 1)
        self.assertEqual(self.score(left=left).returncode, 1)

    def test_features_either_way_round_pass(self):
        r = self.score(order=[22, 20, 31, 33])
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_check_after_ranking_fails(self):
        self.assertEqual(self.score(plan_first=True).returncode, 1)


if __name__ == "__main__":
    unittest.main()
