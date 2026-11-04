#!/usr/bin/env python3
"""Self-test of the release ranked-pick cases: fixture builder and scorer agree.

Run: python3 evals/release/ranked-pick/test_cases.py
For each case it builds the fixture, writes a reference run by hand from the case's expected pick (the release issue,
its label writes and, in the cut case, the cut's blocks), and scores it: the reference must pass, and planted wrong
runs (two entries swapped, a non-severe issue taken past the size, an unplanned feature ranked, a Versions line in a
repo with no version, the mark left on a taken issue, a severe issue left out, an old-shape release issue planned
again instead of cut) must fail. It is not a model run of the
skill: see evals/release/README.md and RESULTS.md for the model runs.
"""
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cases import CASES, EXPECT  # noqa: E402
import make_fixture  # noqa: E402


def block(k, op, issue, fields):
    return f"### {k}. {op}\nIssue: {issue}\n{fields}\n"


EMPTY_REPORT = ("Nothing qualified for Release 3, so I opened no release issue and labelled nothing.\n"
                "- #20 Quiet flag (planned) is left out: its blocker #40 is at ready-for-human, which no agent can take.\n"
                "- #50 Colour output: an unplanned feature, proposed to you; the Milestone issue does not list it.\n"
                "- #34 is at needs-triage and is not a candidate.\n")


def carry_reference(variant=None):
    """Reference run of carry-over-cut; `variant` plants one wrong run: label_first, no_line, heading, twice."""
    body = ("**Goal:** Say goodbye and keep quiet.\n\n**Size:** 5. Used: 3.\n\n## Order\n\n1. #10 Farewell command: next.\n"
            "2. #20 Quiet flag: next.\n3. #31 Empty name prints `Hello, !`: next.\n\n## Left out\n\nNone.\n\n")
    line = "- #31 Empty name prints `Hello, !`: the user chose to carry it over; the fix is not done.\n"
    head = "## Carried over" if variant != "heading" else "## Carry-over"
    if variant == "twice":
        line += line
    if variant != "no_line":
        body += f"{head}\n\n{line}\n"
    body += "## Notes\n\nPosted as a comment when the Release is cut.\n"
    edit = block(1, "Edit an issue body", "02-release-2.md", f"Body:\n~~~\n{body}~~~")
    label = block(2, "Apply / remove labels", "31-empty-name.md", "Add: none\nRemove: release-2")
    if variant == "label_first":
        return label.replace("### 2.", "### 1.") + edit.replace("### 1.", "### 2.")
    return edit + label


def reference(case, exp, repo, order=None, labelled=None, cleared=None, left=None, versions=False, used=None, cut=True,
              empty_issue=False, variant=None):
    if exp.get("carry"):
        return carry_reference(variant)
    order = order if order is not None else exp["order"]
    labelled = labelled if labelled is not None else exp["labelled"]
    cleared = cleared if cleared is not None else exp["cleared"]
    left = left if left is not None else exp["left_out"]
    out, k = [], 1
    if "cut" in exp and cut:
        git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True).stdout.strip()  # noqa: E731
        start = git("log", "-1", "--format=%h", "--abbrev=7", "--grep", "(#5)", "--fixed-strings")
        end = git("rev-parse", "--short=7", "HEAD")
        old = (repo / "CHANGELOG.md").read_text().split("\n", 2)[2]
        vline = "Versions: 0.1.0. " if versions else ""
        entry = (f"## Release 2 (2026-11-04)\n\nSay goodbye and keep quiet.\n\n{vline}Commits: {start}..{end}.\n\n"
                 "- Farewell command (#10)\n- Quiet flag (#20)\n\nAlso merged: README usage (#9).\n")
        out.append(block(k, "Open a pull request", "new (PR 10)",
                         f"Branch: release-2\nTitle: docs(release): Release 2\nBody:\n~~~\nCuts #2.\n~~~\n"
                         f"File: CHANGELOG.md\n~~~\n# Changelog\n\n{entry}\n{old}~~~")); k += 1
        out.append(block(k, "Run a command", "PR 10", "Command: bash test.sh")); k += 1
        out.append(block(k, "Merge a pull request", "PR 10", "Pull: 10")); k += 1
        out.append(block(k, "Comment on an issue", "02-release-2.md", f"Body:\n~~~\n{entry}~~~")); k += 1
        out.append(block(k, "Close", "02-release-2.md", "Outcome: completed\nReason: cut")); k += 1
        for s in ("triage", "retro-planning"):
            out.append(block(k, "Run a skill", "02-release-2.md", f"Skill: {s}\nBrief:\n~~~\nRelease 2 ended.\n~~~")); k += 1
            out.append(block(k, "Comment on an issue", "02-release-2.md",
                             f"Body:\n~~~\n<!-- release end-of-Release pass -->\n{s} ran for this Release.\n~~~")); k += 1
    titles = {i["n"]: i["title"] for i in CASES[case]["issues"]}
    lines = "\n".join(f"{j}. #{n} {titles.get(n, '')}: taken here for the reason its group and place give." for j, n in enumerate(order, 1))
    lo = "\n".join(f"- #{n} {titles.get(n, '')}: size reached or blocked." for n in sorted(left)) or "None."
    prop = "\n".join(f"- #{n} {titles[n]}: not listed by the Milestone issue." for n in sorted(exp.get("proposed", set()))) or "None."
    past = f", plus {exp['past']} severe past the size" if exp.get("past") else ""
    size = CASES[case]["size"]
    body = (f"**Goal:** the next step.\n\n**Label:** `release-3`. Every issue in this Release carries it.\n\n"
            f"**Milestone:** #1\n\n**Size:** {size}. Used: {used if used is not None else exp['used']}{past}.\n\n"
            f"## Order\n\n{lines}\n\n## Left out\n\n{lo}\n\n## Proposed to the user\n\n{prop}\n\n## Notes\n\nPosted when cut.\n")
    if exp.get("empty") and not empty_issue:
        body = None
    if body is not None:
        out.append(block(k, "Create an issue", "new (60-release-3.md)", f"Title: Release 3\nLabels: none\nParent: none\nBody:\n~~~\n{body}~~~")); k += 1
        out.append(block(k, "Create a label", "none", "Label: release-3")); k += 1
    for n in sorted(labelled):
        rem = "next-release" if n in cleared else "none"
        out.append(block(k, "Apply / remove labels", f"{n:02d}-x.md", f"Add: release-3\nRemove: {rem}")); k += 1
    return "\n".join(out)


def _run(repo, *args, env=None):
    return subprocess.run(["bash", "src/greet.sh", *args], cwd=repo, capture_output=True, text=True,
                          env=dict(os.environ, **(env or {})))


def _text(repo, f):
    return (repo / f).read_text()


# What each open issue claims about main, checked on the rendered fixture: every open issue of every case must be
# true on its main (evals.md "Fixture self-tests"), since release checks every open issue against main before
# ranking. A feature's claim is that main does not do it yet.
CLAIMS = {
    "farewell": lambda r: "Goodbye" not in _run(r, "bye", "Ada").stdout,
    "bye-code": lambda r: "Goodbye" not in _run(r, "bye", "Ada").stdout,
    "bye-usage": lambda r: "bye" not in _run(r).stderr,
    "quiet": lambda r: _run(r, "-q", "hello", "Ada").stdout != "Hello, Ada!",
    "shout": lambda r: "HELLO, ADA!" not in _run(r, "-s", "hello", "Ada").stdout,
    "name-file": lambda r: _names_file_not_read(r),
    "count": lambda r: _run(r, "-n", "2", "hello", "Ada").stdout.count("Hello") != 2,
    "colour": lambda r: not re.search(r"\\033|\\e\[|tput|colou?r", _text(r, "src/greet.sh")),
    "json": lambda r: '"greeting"' not in _run(r, "--json", "hello", "Ada").stdout,
    "config": lambda r: ".greetrc" not in _text(r, "src/greet.sh"),
    "lint": lambda r: "shellcheck" not in _text(r, "test.sh"),
    "accents": lambda r: True,  # closed: it claims nothing about main
    "usage-typo": lambda r: "usage: greet.sh helo " in _run(r).stderr,
    "empty-name": lambda r: _run(r, "hello", "").stdout.rstrip(" \n") == "Hello, !",  # #33's trailing space aside
    # the issue's own step: greet.sh's exit status in a pipe (PIPESTATUS[0]), not the pipeline's, which is cat's
    "exit-code": lambda r: subprocess.run(["bash", "-c", "bash src/greet.sh nope | cat; exit ${PIPESTATUS[0]}"], cwd=r,
                                          capture_output=True).returncode == 0,
    "trailing-space": lambda r: _run(r, "hello", "Ada").stdout == "Hello, Ada! \n",
    "unicode": lambda r: True,  # at needs-triage, "Reported, not yet triaged": it claims nothing about main
    "flag-parse": lambda r: _run(r, "hello", "Ada", "-x").stdout == _run(r, "hello", "Ada").stdout == "Hello, Ada!\n",
    # read, not run: running it would write the shared /tmp/greet.log
    "name-log": lambda r: re.search(r'printf .*"\$\{2:-\}" >> /tmp/greet\.log; chmod 0666 /tmp/greet\.log\ncase', _text(r, "src/greet.sh")),
    "profile": lambda r: _profile_overwritten(r),
    "ci-red": lambda r: _test_sh(r).returncode != 0
                        and "(#9)" in subprocess.run(["git", "-C", str(r), "log", "--format=%s"], capture_output=True, text=True).stdout,
    "token-log": lambda r: "s3cret-token" in _test_sh(r, {"REGISTRY_TOKEN": "s3cret-token"}).stdout,
    "slow-test": lambda r: re.search(r"^sleep 10$", _text(r, "test.sh"), re.M),
}


def _test_sh(repo, env=None):
    """test.sh as CI runs it, minus its 10 s sleep (slow-test checks that line on its own)."""
    return subprocess.run(["bash", "-c", "sed '/^sleep 10$/d' test.sh | bash"], cwd=repo, capture_output=True, text=True,
                          env=dict(os.environ, **(env or {})))


def _names_file_not_read(repo):
    with tempfile.TemporaryDirectory() as d:
        f = pathlib.Path(d, "names")
        f.write_text("Ada\nBob\n")
        return "Hello, Bob" not in _run(repo, "-f", str(f), "hello").stdout


def _profile_overwritten(repo):
    with tempfile.TemporaryDirectory() as home:
        pathlib.Path(home, ".profile").write_text("export PATH=/usr/bin\n")
        _run(repo, "hello", "Ada", "--save", env={"HOME": home})
        return pathlib.Path(home, ".profile").read_text() == "Hello, Ada!\n"


class Fixture(unittest.TestCase):
    """Each case's rendered main makes every open issue's claim true; test.sh passes except where an issue says not."""

    def test_every_open_issue_is_true_on_main(self):
        for case, data in CASES.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as t:
                repo = make_fixture.build(pathlib.Path(t) / "out", case)
                for i in data["issues"]:
                    if i.get("status", "open") != "open":
                        continue
                    self.assertIn(i["slug"], CLAIMS, f"#{i['n']} has no claim check")
                    self.assertTrue(CLAIMS[i["slug"]](repo), f"{case}: #{i['n']} {i['title']} is not true on main")
                red = any(i["slug"] == "ci-red" for i in data["issues"])
                ok = _test_sh(repo).returncode == 0
                self.assertEqual(ok, not red, f"{case}: test.sh {'passes' if ok else 'fails'} on main")
                self.assertEqual(_run(repo, "hello", "Ada").stdout.rstrip(" \n"), "Hello, Ada!")


class Cases(unittest.TestCase):
    def run_case(self, case, path="", report=None, **wrong):
        with tempfile.TemporaryDirectory() as t:
            repo = make_fixture.build(pathlib.Path(t) / "out", case)
            make_fixture.slug_of.clear()
            text = reference(case, EXPECT[case], repo, **wrong)
            text = re.sub(r"^Issue: (\d)", lambda m: f"Issue: {path}{m.group(1)}", text, flags=re.M)
            (repo / ".scratch/proposed-actions.md").write_text(text)
            if EXPECT[case].get("empty"):
                (repo / ".scratch/report.md").write_text(EMPTY_REPORT if report is None else report)
            return subprocess.run([sys.executable, str(HERE / "score.py"), str(repo.parent), case],
                                  capture_output=True, text=True)

    def test_reference_runs_pass(self):
        for case in CASES:
            with self.subTest(case=case):
                r = self.run_case(case)
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_issue_lines_given_as_paths_pass(self):
        for case in ("severe-first", "no-version"):
            with self.subTest(case=case):
                r = self.run_case(case, path=".scratch/issues/")
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_swapped_order_fails(self):
        for case in CASES:
            o = EXPECT[case]["order"]
            if len(o) > 1 and not EXPECT[case].get("unordered"):
                with self.subTest(case=case):
                    self.assertEqual(self.run_case(case, order=[o[1], o[0]] + o[2:]).returncode, 1)

    def test_marked_issue_taken_past_the_size_fails(self):
        e = EXPECT["severe-past-size"]
        r = self.run_case("severe-past-size", order=e["order"] + [35], labelled=e["labelled"] | {35}, cleared={35})
        self.assertEqual(r.returncode, 1)

    def test_unplanned_feature_ranked_fails(self):
        e = EXPECT["unplanned-feature"]
        r = self.run_case("unplanned-feature", order=e["order"] + [50], labelled=e["labelled"] | {50}, used=4)
        self.assertEqual(r.returncode, 1)

    def test_versions_line_in_a_repo_with_no_version_fails(self):
        self.assertEqual(self.run_case("no-version", versions=True).returncode, 1)

    def test_mark_left_on_a_taken_issue_fails(self):
        self.assertEqual(self.run_case("severe-first", cleared=set()).returncode, 1)

    def test_old_shape_release_replanned_not_cut_fails(self):
        self.assertEqual(self.run_case("old-shape-cut", cut=False).returncode, 1)

    def test_empty_plan_opens_no_release_issue(self):
        r = self.run_case("empty")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("PASS no release issue opened", r.stdout)

    def test_empty_plan_with_an_empty_release_issue_fails(self):
        r = self.run_case("empty", empty_issue=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAIL no release issue opened", r.stdout)

    def test_empty_plan_with_a_label_applied_fails(self):
        r = self.run_case("empty", labelled={20})
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAIL no label created or applied", r.stdout)

    def test_empty_plan_report_silent_about_it_fails(self):
        r = self.run_case("empty", report="Done.\n")
        self.assertEqual(r.returncode, 1)

    def test_carried_over_issue_left_out_fails(self):
        r = self.run_case("carried-over", order=[20], labelled={20}, used=1)
        self.assertEqual(r.returncode, 1)

    def test_prose_mention_or_closed_carried_issue_ranked_fails(self):
        for extra in (32, 34):
            with self.subTest(extra=extra):
                r = self.run_case("carried-over", order=[20, 31, extra], labelled={20, 31, extra}, used=3)
                self.assertEqual(r.returncode, 1)

    def test_carried_over_fixture_renders_the_section(self):
        with tempfile.TemporaryDirectory() as t:
            repo = make_fixture.build(pathlib.Path(t) / "out", "carried-over")
            body = _text(repo, ".scratch/issues/02-release-2.md")
            sec = re.search(r"^## Carried over\n(.*?)(?=^## )", body, re.S | re.M).group(1)
            self.assertIn("#31", sec)
            self.assertIn("#34", sec)
            self.assertNotIn("#32", sec)
            self.assertIn("#32", body)  # in Notes, shaped like a carried-over line
            self.assertIn("carried to the next Release", body)
            order = re.search(r"^## Order\n(.*?)(?=^## )", body, re.S | re.M).group(1)
            self.assertIn("#31", order)
            self.assertIn("#34", order)
            self.assertIn("Used: 3", body)

    def test_carry_over_cut_reference_passes(self):
        r = self.run_case("carry-over-cut")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("PASS the line is written before the label is removed", r.stdout)

    def test_carry_over_cut_wrong_runs_fail(self):
        for variant, failing in (("label_first", "the line is written before the label is removed"),
                                 ("no_line", "the release issue (#2) is edited with a `## Carried over` section"),
                                 ("heading", "the release issue (#2) is edited with a `## Carried over` section"),
                                 ("twice", "the section has a `- #31 <title>: <why>` line")):
            with self.subTest(variant=variant):
                r = self.run_case("carry-over-cut", variant=variant)
                self.assertEqual(r.returncode, 1, r.stdout)
                self.assertIn("FAIL " + failing, r.stdout)

    def test_carry_over_cut_fixture_renders_the_blocker(self):
        with tempfile.TemporaryDirectory() as t:
            repo = make_fixture.build(pathlib.Path(t) / "out", "carry-over-cut")
            i31 = _text(repo, ".scratch/issues/31-empty-name.md")
            self.assertIn("Status: open", i31)
            self.assertIn("release-2", i31.splitlines()[2])
            self.assertIn("Status: open", _text(repo, ".scratch/issues/02-release-2.md"))
            self.assertNotIn("Carried over", _text(repo, ".scratch/issues/02-release-2.md"))
            self.assertIn("carry #31 over", (repo.parent / "PROMPT.md").read_text())

    def test_severe_issue_left_out_fails(self):
        e = EXPECT["severe-first"]
        r = self.run_case("severe-first", order=e["order"][1:], labelled=e["labelled"] - {31}, left={31}, used=4)
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
