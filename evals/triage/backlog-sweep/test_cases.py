#!/usr/bin/env python3
"""Self-test of the triage backlog-sweep case: fixture builder and scorer agree.

Run: python3 evals/triage/backlog-sweep/test_cases.py
It builds the fixture, writes a reference run by hand from the expected outcome, and scores it: the reference must
pass, and planted wrong runs (a duplicate closed with no link, an obsolete issue closed with no reason or as not
planned, the issue left out twice expired, the expired issue closed without "reopen to bring it back", an agent-found enhancement
expired or put at ready-for-agent, the planned feature expired, the feature-blocker left unmarked, a release label
applied, no summary, a comment without the disclaimer) must fail. It is not a model run of the skill: see
evals/triage/README.md and RESULTS.md for the model runs.
"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sweep_case import DISCLAIMER  # noqa: E402
import make_fixture  # noqa: E402

FILES = {4: "04-release-3.md", 20: "20-quiet.md", 30: "30-usage-typo.md", 31: "31-usage-misspelt.md",
         32: "32-empty-name.md", 33: "33-upper-case.md", 34: "34-two-names.md", 40: "40-flag-parse.md",
         41: "41-name-log.md", 50: "50-json-output.md", 51: "51-colour.md"}


def reference(drop=(), extra=(), replace=None):
    """The expected run as (op, issue, fields) blocks; drop removes blocks by key, extra and replace plant faults."""
    d = DISCLAIMER
    blocks = {
        "dup-comment": ("Comment on an issue", 31, f"Body:\n~~~\n{d}\n\nDuplicate of #30, which is kept.\n~~~"),
        "dup-close": ("Close", 31, "Outcome: duplicate\nReason: duplicate of #30."),
        "obs-comment": ("Comment on an issue", 32,
                        f"Body:\n~~~\n{d}\n\nObsolete: since #8 `src/greet.sh` defaults the name to `world`, so "
                        "`greet.sh hello` prints `Hello, world!`.\n~~~"),
        "obs-close": ("Close", 32, "Outcome: completed\nReason: obsolete, main's greet.sh greets the world when no name is given."),
        "exp-comment": ("Comment on an issue", 33,
                        f"Body:\n~~~\n{d}\n\nLeft out of Releases 1, 2 and 3 in a row, so it expires. Reopen to bring it back.\n~~~"),
        "exp-close": ("Close", 33, "Outcome: not planned\nReason: left out of 3 Releases in a row; reopen to bring it back."),
        "blk-comment": ("Comment on an issue", 40, f"Body:\n~~~\n{d}\n\nBlocks the planned feature #20: next-release.\n~~~"),
        "blk-mark": ("Apply / remove labels", 40, "Add: next-release\nRemove: none"),
        "sev-comment": ("Comment on an issue", 41, f"Body:\n~~~\n{d}\n\nbug, ready-for-agent: a security hole, next-release.\n~~~"),
        "sev-labels": ("Apply / remove labels", 41, "Add: bug, ready-for-agent, next-release\nRemove: needs-triage"),
        "enh-comment": ("Comment on an issue", 50, f"Body:\n~~~\n{d}\n\nAn agent-found enhancement: waits for the user.\n~~~"),
        "enh-labels": ("Apply / remove labels", 50, "Add: ready-for-human\nRemove: needs-triage"),
        "col-comment": ("Comment on an issue", 51, f"Body:\n~~~\n{d}\n\nAn agent-found enhancement: waits for the user.\n~~~"),
        "col-labels": ("Apply / remove labels", 51, "Add: ready-for-human\nRemove: ready-for-agent"),
        "summary": ("Comment on an issue", 4,
                    f"Body:\n~~~\n{d}\n\n## Triage batch\n\n| Issue | Outcome |\n| --- | --- |\n| #31 | closed, duplicate of #30 |\n"
                    "| #32 | closed, obsolete |\n| #33 | expired |\n| #40 | next-release |\n| #41 | next-release |\n"
                    "| #50 | ready-for-human |\n| #51 | ready-for-human |\n~~~"),
    }
    if replace:
        blocks.update(replace)
    out = [v for key, v in blocks.items() if key not in drop] + list(extra)
    return "\n".join(f"### {k}. {op}\nIssue: {FILES.get(n, f'{n:02d}-x.md')}\n{fields}\n"
                     for k, (op, n, fields) in enumerate(out, 1))


class Sweep(unittest.TestCase):
    def score(self, run):
        with tempfile.TemporaryDirectory() as t:
            repo = make_fixture.build(pathlib.Path(t) / "out")
            (repo / ".scratch/proposed-actions.md").write_text(run)
            return subprocess.run([sys.executable, str(HERE / "score.py"), str(repo.parent)], capture_output=True, text=True)

    def fails(self, run):
        r = self.score(run)
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_reference_run_passes(self):
        r = self.score(reference())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_duplicate_closed_without_a_link_fails(self):
        self.fails(reference(drop={"dup-comment"}, replace={"dup-close": ("Close", 31, "Outcome: duplicate\nReason: a duplicate.")}))

    def test_obsolete_closed_without_a_reason_fails(self):
        self.fails(reference(drop={"obs-comment"}, replace={"obs-close": ("Close", 32, "Outcome: completed\nReason: obsolete.")}))

    def test_obsolete_closed_as_not_planned_fails(self):
        self.fails(reference(replace={"obs-close": ("Close", 32, "Outcome: not planned\nReason: obsolete, main's greet.sh "
                                                               "greets the world when no name is given.")}))

    def test_issue_left_out_twice_expired_fails(self):
        self.fails(reference(extra=[("Close", 34, "Outcome: not planned\nReason: expired; reopen to bring it back.")]))

    def test_expired_without_reopen_line_fails(self):
        self.fails(reference(drop={"exp-comment"}, replace={"exp-close": ("Close", 33, "Outcome: not planned\nReason: stale.")}))

    def test_agent_found_enhancement_expired_fails(self):
        self.fails(reference(extra=[("Close", 51, "Outcome: not planned\nReason: expired; reopen to bring it back.")]))

    def test_agent_found_enhancement_made_ready_for_agent_fails(self):
        self.fails(reference(replace={"enh-labels": ("Apply / remove labels", 50, "Add: ready-for-agent\nRemove: needs-triage")}))

    def test_agent_found_enhancement_left_at_ready_for_agent_fails(self):
        self.fails(reference(replace={"col-labels": ("Apply / remove labels", 51, "Add: ready-for-human\nRemove: none")}))

    def test_planned_feature_expired_fails(self):
        self.fails(reference(extra=[("Close", 20, "Outcome: not planned\nReason: expired; reopen to bring it back.")]))

    def test_feature_blocker_left_unmarked_fails(self):
        self.fails(reference(drop={"blk-mark"}))

    def test_severe_issue_left_unmarked_fails(self):
        self.fails(reference(replace={"sev-labels": ("Apply / remove labels", 41, "Add: bug, ready-for-agent\nRemove: needs-triage")}))

    def test_extra_next_release_mark_fails(self):
        self.fails(reference(extra=[("Apply / remove labels", 34, "Add: next-release\nRemove: none")]))

    def test_release_label_applied_fails(self):
        self.fails(reference(extra=[("Apply / remove labels", 41, "Add: release-4\nRemove: none")]))

    def test_no_summary_fails(self):
        self.fails(reference(drop={"summary"}))

    def test_comment_without_disclaimer_fails(self):
        self.fails(reference(replace={"blk-comment": ("Comment on an issue", 40, "Body:\n~~~\nBlocks #20.\n~~~")}))


if __name__ == "__main__":
    unittest.main()
