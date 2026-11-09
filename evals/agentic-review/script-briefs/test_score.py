#!/usr/bin/env python3
"""Self-test of the script-briefs case: make-case.sh renders the prompt, and score.py passes a run whose briefs come
from the plugin script and fails hand-made, missing, altered or misplaced ones. Runs no agent.
Usage: python3 evals/agentic-review/script-briefs/test_score.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRIPT = ROOT / "plugins/dev-skills/skills/review-rounds/review_briefs.py"
sys.path.insert(0, str(HERE))
import score  # noqa: E402


def run_script(case, *argv):
    repo = case / "repo"
    common = ["--base", "main", "--head", "planted", "--repo", str(repo), "--spec", str(repo / ".scratch/SPEC.md")]
    return subprocess.run([sys.executable, str(SCRIPT), argv[0], *common, *argv[1:]], capture_output=True, text=True, check=True)


class CaseTest(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.case = pathlib.Path(self._t.name) / "case"
        subprocess.run(["bash", str(HERE / "make-case.sh"), str(self.case), str(ROOT / "plugins")], check=True, capture_output=True)
        self.briefs = self.case / "repo.briefs" / "round"

    def tearDown(self):
        self._t.cleanup()

    def scripted_run(self):
        reports = self.case / "reports"
        reports.mkdir()
        for finder, name in score.REPORTS.items():
            shutil.copy(self.case / "messages" / name, reports / f"{finder}.md")
        run_script(self.case, "round1", "--level", "standard", "--out", str(self.briefs))
        run_script(self.case, "verify", "--level", "standard", "--reports", str(reports), "--out", str(self.briefs))
        self.handoff(f"Read {(self.briefs / 'finder-standards.md').resolve()} whole; it is your only instruction.")

    def handoff(self, text):
        (self.case / "handoff-standards.txt").write_text(text)

    def result(self):
        return {cid: ok for cid, ok, _ in score.score(self.case, SCRIPT)}

    def test_prompt_is_rendered_for_this_case(self):
        text = (self.case / "PROMPT.md").read_text()
        for placeholder in ("<plugins>", "<repo>", "<messages>", "<briefs>", "<handoff>"):
            self.assertNotIn(placeholder, text)
        self.assertIn(str(ROOT / "plugins"), text)
        self.assertIn(f"{self.case}/handoff-standards.txt", text)
        self.assertIn(f"{self.case}/repo.briefs/round", text)
        self.assertTrue((self.case / "repo/.scratch/SPEC.md").is_file())
        for name in score.REPORTS.values():
            self.assertIn(name, text)
            self.assertTrue((self.case / "messages" / name).is_file())
        self.assertNotIn("EXPECTED", text)

    def test_script_briefs_pass_and_are_independent_of_the_out_dir(self):
        self.scripted_run()
        self.assertTrue(all(self.result().values()), self.result())

    def test_scorer_ignores_edits_to_the_case_messages(self):
        self.scripted_run()
        for f in (self.case / "messages").iterdir():
            f.write_text("moved or edited by the run")
        self.assertTrue(all(self.result().values()), self.result())
        shutil.rmtree(self.case / "messages")
        self.assertTrue(all(self.result().values()), self.result())

    def test_no_run_fails(self):
        self.assertFalse(any(v for k, v in self.result().items() if k.startswith("B")))

    def test_hand_altered_brief_fails_only_itself(self):
        self.scripted_run()
        p = self.briefs / "finder-spec.md"
        p.write_text(p.read_text().replace("Finding", "finding", 1))
        r = self.result()
        self.assertFalse(r["B2"])
        self.assertTrue(r["B1"] and r["B3"] and r["B4"])

    def test_reports_directory_is_ignored_by_f1(self):
        self.scripted_run()
        (self.briefs / "reports").mkdir()
        (self.briefs / "reports" / "standards.md").write_text("x")
        self.assertTrue(self.result()["F1"])

    def test_missing_and_extra_files_fail(self):
        self.scripted_run()
        (self.briefs / "finder-adversarial.md").unlink()
        (self.briefs / "notes.md").write_text("x")
        r = self.result()
        self.assertFalse(r["F1"])
        self.assertFalse(r["B3"])

    def test_verifier_with_a_changed_report_fails(self):
        self.scripted_run()
        p = self.briefs / "verifier.md"
        p.write_text(p.read_text().replace("settle never pays the last creditor", "settle pays nobody"))
        self.assertFalse(self.result()["B4"])

    def test_pasted_or_missing_handoff_fails_only_h2(self):
        self.scripted_run()
        self.handoff((self.briefs / "finder-standards.md").read_text())
        r = self.result()
        self.assertFalse(r["H2"])
        self.assertTrue(r["B1"] and r["F1"] and r["L1"])
        self.handoff("Please review the branch.")
        self.assertFalse(self.result()["H2"])
        (self.case / "handoff-standards.txt").unlink()
        self.assertFalse(self.result()["H2"])

    def test_file_written_in_the_repository_fails(self):
        self.scripted_run()
        (self.case / "repo" / "finder-notes.md").write_text("x")
        self.assertFalse(self.result()["L1"])


if __name__ == "__main__":
    unittest.main()
