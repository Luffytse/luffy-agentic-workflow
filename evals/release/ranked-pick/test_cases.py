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
import pathlib
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


def reference(case, exp, repo, order=None, labelled=None, cleared=None, left=None, versions=False, used=None, cut=True):
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
    out.append(block(k, "Create an issue", "new (60-release-3.md)", f"Title: Release 3\nLabels: none\nParent: none\nBody:\n~~~\n{body}~~~")); k += 1
    out.append(block(k, "Create a label", "none", "Label: release-3")); k += 1
    for n in sorted(labelled):
        rem = "next-release" if n in cleared else "none"
        out.append(block(k, "Apply / remove labels", f"{n:02d}-x.md", f"Add: release-3\nRemove: {rem}")); k += 1
    return "\n".join(out)


class Cases(unittest.TestCase):
    def run_case(self, case, **wrong):
        with tempfile.TemporaryDirectory() as t:
            repo = make_fixture.build(pathlib.Path(t) / "out", case)
            make_fixture.slug_of.clear()
            (repo / ".scratch/proposed-actions.md").write_text(reference(case, EXPECT[case], repo, **wrong))
            return subprocess.run([sys.executable, str(HERE / "score.py"), str(repo.parent), case],
                                  capture_output=True, text=True)

    def test_reference_runs_pass(self):
        for case in CASES:
            with self.subTest(case=case):
                r = self.run_case(case)
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_swapped_order_fails(self):
        for case in CASES:
            o = EXPECT[case]["order"]
            if len(o) > 1:
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

    def test_severe_issue_left_out_fails(self):
        e = EXPECT["severe-first"]
        r = self.run_case("severe-first", order=e["order"][1:], labelled=e["labelled"] - {31}, left={31}, used=4)
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
