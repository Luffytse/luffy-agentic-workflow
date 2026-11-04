#!/usr/bin/env python3
"""Self-test of the first-sighting case: no model session.

1. The rendered input says what the case's meaning says (a fixture builder's self-test must not pass while the case
   is wrong): #41 proposes a deterministic check seen in one thread; the check really would have failed on the past
   mistake and really is run by nothing; #42 proposes a prose reminder seen in one thread; neither is severe; there is
   no earlier record, no Boundary record, cap default.
2. The scorer passes a reference run written from the expectation and fails each planted wrong run, among them
   main's behaviour (both close as wontfix).

Run: python3 evals/retro-handoff/test_first_sighting.py
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import first_sighting as fs  # noqa: E402


def passes(out):
    res = fs.score(out)
    return all(ok for _, ok, _ in res), [n for n, ok, _ in res if not ok]


def reference(out):
    """What a right run leaves: Ticket #43 for #41, #42 closed wontfix, record #44 closed."""
    out = pathlib.Path(out)
    (out / "issues/41.md").write_text(fs.ISSUES[41].replace("## Comments\nNone", "## Comments\nAbsorbed by #43; closes when it is completed."))
    (out / "issues/42.md").write_text(
        fs.ISSUES[42].replace("State: open", "State: closed").replace("Labels: retro", "Labels: retro, wontfix")
        .replace("## Comments\nNone", "## Comments\nSeen in one thread, not severe, and a prose reminder is no check. Closed as wontfix."))
    (out / "issues/43.md").write_text(
        "# Run the scorer's test in CI\nState: open\nLabels: enhancement, ready-for-agent\nCreated: 2026-11-01\n"
        "Absorbs #41. Add a CI step running `python3 tests/test_score.py`.\n## Done when\nCI fails on history/broken/score.py.\n## Comments\nNone\n")
    (out / "issues/44.md").write_text(
        "# Retro planning 2026-11-01\nState: closed\nLabels: retro-planning\nCreated: 2026-11-01\n"
        "## Cap\n3 (default)\n## Verdicts\n| Group | Retro issues | Distinct threads | Verdict | Reason or Ticket |\n|---|---|---|---|---|\n"
        "| CI skips the scorer test | #41 | 1 | Ticket | #43; necessity check: confirmed (the test fails on history/broken; no CI step runs it) |\n"
        "| Summaries run long | #42 | 1 | wontfix | a prose reminder, one thread |\n"
        "## Tickets filed\n- #43 (CI skips the scorer test), absorbs #41\n## Comments\nNone\n")


class FirstSighting(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.out = pathlib.Path(self._t.name)
        fs.build(self.out)

    def tearDown(self):
        self._t.cleanup()

    def read(self, rel):
        return (self.out / rel).read_text()

    # 1. The rendered input says what the case's meaning says.

    def test_41_proposes_a_deterministic_check_seen_in_one_thread(self):
        t = self.read("issues/41.md")
        self.assertRegex(t, r"Suggested fix: add a CI step that runs `python3 tests/test_score.py`")
        self.assertEqual(len(re.findall(r"^Source thread:", t, re.M)), 1)
        self.assertNotRegex(t, r"(?i)seen again")
        self.assertIn("## Comments\nNone", t)

    def test_42_proposes_a_prose_reminder_seen_in_one_thread(self):
        t = self.read("issues/42.md")
        self.assertRegex(t, r"Suggested fix: add a reminder to docs/style\.md")
        self.assertNotRegex(t, r"(?i)\bCI\b|\btest\b|checker|lint")
        self.assertEqual(len(re.findall(r"^Source thread:", t, re.M)), 1)
        self.assertNotRegex(t, r"(?i)seen again")
        self.assertNotEqual(re.search(r"^Source thread:.*$", t, re.M).group(0), re.search(r"^Source thread:.*$", self.read("issues/41.md"), re.M).group(0))

    def test_41_names_no_severe_wording(self):
        t = self.read("issues/41.md") + self.read("history/pr-7.md")
        self.assertNotRegex(t, r"(?i)crash|in use|outage|exploit|vulnerab|corrupt|hours? of|expensive")
        self.assertIn("no user was affected", t)
        self.assertIn("no data was lost", t)
        self.assertIn("no delivery was stopped", t)

    def test_neither_issue_is_severe(self):
        for n in (41, 42):
            self.assertNotRegex(self.read(f"issues/{n}.md"), r"(?i)lost data|security|data loss|large waste")

    def test_no_earlier_record_no_boundary_record_default_cap(self):
        for p in (self.out / "issues").glob("*.md"):
            self.assertNotIn("retro-planning", p.read_text().split("\n")[2])
        self.assertFalse((self.out / "docs/dev-skills/boundaries.md").exists())
        self.assertFalse(any("boundar" in p.name.lower() for p in self.out.rglob("*") if p.is_file()))
        self.assertNotIn("Milestone", self.read("PROMPT.md"))
        self.assertNotIn("cap", self.read("PROMPT.md").lower())

    def test_the_check_would_have_failed_on_the_past_mistake(self):
        def run(src):
            return subprocess.run([sys.executable, str(self.out / "tests/test_score.py")], cwd=self.out,
                                  env={"PYTHONPATH": str(self.out / src)}, capture_output=True)
        self.assertEqual(run("src").returncode, 0)
        self.assertNotEqual(run("history/broken").returncode, 0)
        self.assertIn("history/broken/score.py", self.read("history/pr-7.md"))

    def test_nothing_already_catches_it(self):
        self.assertNotIn("test", self.read("scripts/lint.sh").replace("tests", "").lower().split("\n", 2)[2])
        ci = self.read(".github/workflows/ci.yml")
        self.assertIn("scripts/lint.sh", ci)
        self.assertNotIn("test_score", ci)
        self.assertEqual(ci.count("- run:"), 1)

    def test_prompt_gives_the_users_calls_and_the_checkout(self):
        self.assertIn("address the problem", self.read("PROMPT.md"))
        self.assertNotIn("one Ticket", self.read("PROMPT.md"))
        self.assertIn("file any Ticket yourself", self.read("PROMPT.md"))
        fs.build(self.out, "/x/checkout")
        self.assertIn("/x/checkout/plugins/dev-skills/skills/", self.read("PROMPT.md"))

    # 2. The scorer.

    def test_untouched_fixture_fails(self):
        ok, bad = passes(self.out)
        self.assertFalse(ok)

    def test_reference_run_passes(self):
        reference(self.out)
        ok, bad = passes(self.out)
        self.assertTrue(ok, bad)

    def planted(self, mutate, expect_fail):
        reference(self.out)
        mutate(self.out)
        ok, bad = passes(self.out)
        self.assertFalse(ok)
        self.assertTrue(any(expect_fail in b for b in bad), bad)

    def test_main_behaviour_both_wontfix_fails(self):
        def m(out):
            (out / "issues/43.md").unlink()
            (out / "issues/41.md").write_text(
                fs.ISSUES[41].replace("State: open", "State: closed").replace("Labels: retro", "Labels: retro, wontfix")
                .replace("## Comments\nNone", "## Comments\nOne thread, not severe. Closed as wontfix."))
            (out / "issues/44.md").write_text(
                "# Retro planning 2026-11-01\nState: closed\nLabels: retro-planning\nCreated: 2026-11-01\n## Verdicts\n"
                "| a | #41 | 1 | wontfix | one thread |\n| b | #42 | 1 | wontfix | one thread |\n## Tickets filed\nNone\n")
        self.planted(m, "#41 (the check) is acted on")

    def test_acted_without_a_necessity_verdict_fails(self):
        def m(out):
            p = out / "issues/44.md"
            p.write_text(p.read_text().replace("; necessity check: confirmed (the test fails on history/broken; no CI step runs it)", ""))
        self.planted(m, "necessity check confirmed")

    def test_necessity_not_confirmed_but_acted_fails(self):
        def m(out):
            p = out / "issues/44.md"
            p.write_text(p.read_text().replace("necessity check: confirmed", "necessity check: not confirmed"))
        self.planted(m, "necessity check confirmed")

    def test_prose_proposal_also_ticketed_fails(self):
        def m(out):
            p = out / "issues/43.md"
            p.write_text(p.read_text() + "Absorbs #42 as well.\n")
        self.planted(m, "absorbs #41 and not #42")

    def test_prose_proposal_left_open_fails(self):
        self.planted(lambda out: (out / "issues/42.md").write_text(fs.ISSUES[42]), "#42")

    def test_second_ticket_fails(self):
        def m(out):
            (out / "issues/45.md").write_text("# x\nState: open\nLabels: ready-for-agent\nCreated: 2026-11-01\nAbsorbs #42.\n")
        self.planted(m, "exactly one new Ticket")

    def test_record_left_open_fails(self):
        def m(out):
            p = out / "issues/44.md"
            p.write_text(p.read_text().replace("State: closed", "State: open"))
        self.planted(m, "one planning record")

    def test_changed_code_fails(self):
        self.planted(lambda out: (out / ".github/workflows/ci.yml").write_text(fs.CI + "      - run: python3 tests/test_score.py\n"), "unchanged")


if __name__ == "__main__":
    unittest.main()
