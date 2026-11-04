#!/usr/bin/env python3
"""Self-test of the triage repo-labels case: fixture builder and scorer agree, and the rendered input says what the case means.

Run: python3 evals/triage/repo-labels/test_cases.py
It builds each case, checks the files a session would read (the issue files, the triage-labels doc, the tracker's label
list, the prompt), then writes a reference run by hand from the expected outcome and scores it: the reference must
pass, and planted wrong runs (a UI bug given both labels, an unmatched issue given a label, an unlisted label applied
or created, a stale label left on or removed with no comment, a user-named label removed, and for the empty table any
repo label applied or removed) must fail. It is not a model run of the skill: see evals/triage/README.md and RESULTS.md.
"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from label_case import DISCLAIMER, ISSUES, TABLE, TRACKER_LABELS  # noqa: E402
import make_fixture  # noqa: E402

FILES = {i["n"]: f"{i['n']:02d}-{i['slug']}.md" for i in ISSUES}
D = DISCLAIMER


def block(op, n, fields):
    return (op, n, fields)


def labels(n, add="none", remove="none"):
    return block("Apply / remove labels", n, f"Add: {add}\nRemove: {remove}")


def comment(n, text="Triaged."):
    return block("Comment on an issue", n, f"Body:\n~~~\n{D}\n\n{text}\n~~~")


def reference_table(replace=None, drop=(), extra=()):
    base = {
        "ui": labels(10, "bug, ready-for-agent, frontend", "needs-triage"),
        "doc": labels(11, "bug, ready-for-agent", "needs-triage"),
        "slow": labels(12, "bug, ready-for-agent, backend", "needs-triage"),
        "stale": labels(13, "bug, ready-for-agent, backend", "needs-triage, frontend"),
        "stale-why": comment(13, "Removed `frontend`: the work is all in api/export.py."),
        "named": labels(14, "bug, ready-for-agent, frontend", "needs-triage"),
    }
    base.update(replace or {})
    return render([v for k, v in base.items() if k not in drop] + list(extra))


def reference_empty(replace=None, extra=()):
    base = {n: labels(n, "bug, ready-for-agent", "needs-triage") for n in FILES}
    base.update(replace or {})
    return render(list(base.values()) + list(extra))


def render(blocks):
    return "\n".join(f"### {k}. {op}\nIssue: {FILES.get(n, 'new')}\n{fields}\n" for k, (op, n, fields) in enumerate(blocks, 1))


class RepoLabels(unittest.TestCase):
    def score(self, name, run):
        with tempfile.TemporaryDirectory() as t:
            repo = make_fixture.build(pathlib.Path(t) / "out", name)
            (repo / ".scratch/proposed-actions.md").write_text(run)
            return subprocess.run([sys.executable, str(HERE / "score.py"), str(repo.parent), name], capture_output=True, text=True)

    def passes(self, name, run):
        r = self.score(name, run)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def fails(self, name, run):
        r = self.score(name, run)
        self.assertEqual(r.returncode, 1, r.stdout)

    # The rendered input says what each case means.
    def test_rendered_input(self):
        for name in ("table", "empty"):
            with tempfile.TemporaryDirectory() as t:
                repo = make_fixture.build(pathlib.Path(t) / "out", name)
                doc = (repo / "docs/dev-skills/triage-labels.md").read_text()
                self.assertIn("## Repo labels", doc)
                rows = [l for l in doc.splitlines() if l.startswith("| `frontend`") or l.startswith("| `backend`")]
                self.assertEqual(len(rows), 2 if name == "table" else 0, doc)
                issues = {n: (repo / ".scratch/issues" / f).read_text() for n, f in FILES.items()}
                self.assertIn("Labels: needs-triage, frontend", issues[13])      # the stale label is on the issue
                self.assertIn("api/export.py", issues[13])                        # and the work is in the API
                self.assertNotIn("ui/", issues[13].split("## Comments")[0].split("Nothing under")[0])
                self.assertIn("Labels: needs-triage, backend", issues[14])        # the user-named label is on the issue
                self.assertIn("ui/footer.html", issues[14])                       # and the work is in the UI
                self.assertRegex(issues[14].split("## Comments")[1], r"`backend`.*leave it on")
                for n in (10, 11, 12, 13, 14):
                    self.assertIn("Status: open", issues[n])
                self.assertIn("ui/cart.html", issues[10])
                self.assertIn("api/orders.py", issues[12])
                self.assertNotIn("ui/", issues[11] + issues[12])                  # #11 and #12 name no UI file
                self.assertNotIn("api/", issues[11])                              # #11 matches neither label
                self.assertTrue(set(TABLE) | {"performance", "security", "docs"} <= set((repo / ".scratch/labels.md").read_text().split()))
                self.assertTrue(set(TRACKER_LABELS) >= set(TABLE))
                for n, text in issues.items():                                    # no body gives the answer away
                    body = text.split("## Comments")[0].split("Blocked by: none")[1]
                    self.assertNotIn("frontend", body)
                    self.assertNotIn("backend", body)
                prompt = (repo.parent / "PROMPT.md").read_text()
                self.assertNotIn("frontend", prompt)
                named = [l for l in prompt.splitlines() if "backend" in l]  # only the user's request names a label
                self.assertEqual(len(named), 1 if name == "table" else 0, prompt)
                if name == "table":
                    self.assertIn("#14", named[0])

    def test_reference_table_passes(self):
        self.passes("table", reference_table())

    def test_reference_empty_passes(self):
        self.passes("empty", reference_empty())

    def test_ui_bug_given_both_labels_fails(self):
        self.fails("table", reference_table({"ui": labels(10, "bug, ready-for-agent, frontend, backend", "needs-triage")}))

    def test_ui_bug_given_no_label_fails(self):
        self.fails("table", reference_table({"ui": labels(10, "bug, ready-for-agent", "needs-triage")}))

    def test_unmatched_issue_given_a_label_fails(self):
        self.fails("table", reference_table({"doc": labels(11, "bug, ready-for-agent, backend", "needs-triage")}))

    def test_unlisted_label_applied_fails(self):
        self.fails("table", reference_table({"slow": labels(12, "bug, ready-for-agent, backend, performance", "needs-triage")}))

    def test_unlisted_label_created_fails(self):
        self.fails("table", reference_table(extra=[block("Create a label", 0, "Label: perf")]))

    def test_stale_label_left_on_fails(self):
        self.fails("table", reference_table({"stale": labels(13, "bug, ready-for-agent, backend", "needs-triage")}))

    def test_stale_label_removed_with_no_comment_fails(self):
        self.fails("table", reference_table(drop={"stale-why"}))

    def test_stale_comment_not_naming_the_label_fails(self):
        self.fails("table", reference_table({"stale-why": comment(13, "Triaged as a bug.")}))

    def test_user_named_label_removed_fails(self):
        self.fails("table", reference_table({"named": labels(14, "bug, ready-for-agent, frontend", "needs-triage, backend")}))

    def test_comment_without_disclaimer_fails(self):
        self.fails("table", reference_table({"stale-why": block("Comment on an issue", 13, "Body:\n~~~\nRemoved frontend.\n~~~")}))

    def test_empty_table_repo_label_applied_fails(self):
        self.fails("empty", reference_empty({10: labels(10, "bug, ready-for-agent, frontend", "needs-triage")}))

    def test_empty_table_repo_label_removed_fails(self):
        self.fails("empty", reference_empty({13: labels(13, "bug, ready-for-agent", "needs-triage, frontend")}))

    def test_empty_run_fails(self):
        self.fails("table", "")
        self.fails("empty", "")


if __name__ == "__main__":
    unittest.main()
