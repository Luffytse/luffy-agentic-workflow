#!/usr/bin/env python3
"""Self-test of the scope case: no model session.

1. The rendered input says what the case's meaning says: #51 has no Scope line and really is an environment limit
   (its text names the agent's sandbox refusing a push, nothing about a skill or this repo); #52 repeats the limit with
   a Scope line; #53 is a skill Retro seen in two threads; #54 is another project's own lesson, filed here, whose
   tracker is the local other-project/; #51 and #52 are severe (lost work); #53 is not; the Milestone, release issue and
   next-release mapping a Release-end run needs are present; no Boundary record; the prompt names the checkout and
   asks no user.
2. The scorer passes a reference run written from the expectation and fails each planted wrong run, among them
   main's behaviour (grouped by root cause only, no Scope, #54 decided here).

Run: python3 evals/retro-handoff/test_scope.py
"""
import pathlib
import re
import sys
import tempfile
import unittest

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import scope as sc  # noqa: E402


def passes(out):
    res = sc.score(out)
    return all(ok for _, ok, _ in res), [n for n, ok, _ in res if not ok]


RECORD = """# Retro planning 2026-11-08
State: closed
Labels: retro-planning
Created: 2026-11-08
Snapshot time: 2026-11-08T00:00

## Cap

none (Release end)

## Snapshot

| Retro issue | Scope | Distinct threads | New vote | Status |
|---|---|---|---|---|
| #51 | environment (given here: the sandbox refuses a push to any other branch) | 1 | yes | in the backlog |
| #52 | environment | 1 | yes | in the backlog |
| #53 | skill | 2 | yes | in the backlog |
| #54 | this repo | 1 | yes | refiled in other-project/issues/1.md |

## Verdicts

| Group | Scope | Retro issues | Distinct threads | Verdict | Reason or Ticket |
|---|---|---|---|---|---|
| push limited to the designated branch | environment | #51, #52 | 2 | joins the next Release | #55 |
| Ticket template lacks Blocked by | skill | #53 | 2 | stays open | does not block a feature, not severe |
| acme-app date format | this repo | #54 | 1 | closed | refiled in other-project/issues/1.md |

## Tickets filed

- #55 (push limited to the designated branch), absorbs #51, #52
"""

TICKET = """# Record the designated-branch push limit in the Harness reference and Startup verification
State: open
Labels: enhancement, ready-for-agent, next-release
Created: 2026-11-08
Absorbs #51, #52.
Fix: the limit is the environment's, so it goes in worker-control's Harness reference and in Startup verification, one place, not a sentence in each skill that starts work.
## Done when
worker-control names the one-designated-branch limit and Startup verification checks it.
## Comments
None
"""


def reference(out):
    out = pathlib.Path(out)
    i = out / "issues"
    for n in (51, 52):
        (i / f"{n}.md").write_text(sc.ISSUES[n].replace("## Comments\nNone", "## Comments\nAbsorbed by #55; closes when it is completed."))
    (i / "54.md").write_text(sc.ISSUES[54].replace("State: open", "State: closed").replace("## Comments\nNone", "## Comments\nRefiled in other-project/issues/1.md; closed here."))
    (i / "55.md").write_text(TICKET)
    (i / "56.md").write_text(RECORD)
    (out / "other-project/issues/1.md").write_text(
        "# Retro: reports in acme-app use the old date format\nState: open\nLabels: retro\nCreated: 2026-11-08\nScope: this repo\n"
        "Suggested fix: add the date format to acme-app's docs/acme-style.md.\n## Comments\nNone\n")


class Scope(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.out = pathlib.Path(self._t.name)
        sc.build(self.out)

    def tearDown(self):
        self._t.cleanup()

    def read(self, rel):
        return (self.out / rel).read_text()

    # 1. The rendered input says what the case's meaning says.

    def test_51_has_no_scope_line_and_is_an_environment_limit(self):
        t = self.read("issues/51.md")
        self.assertNotRegex(t, r"(?im)^Scope:")
        self.assertRegex(t, r"(?i)refused by the environment")
        self.assertNotRegex(t, r"(?i)\bthis repo\b|template|skill text")
        self.assertEqual(len(re.findall(r"^Source thread:", t, re.M)), 1)

    def test_52_repeats_the_limit_with_a_scope_line_from_another_thread(self):
        t, t51 = self.read("issues/52.md"), self.read("issues/51.md")
        self.assertRegex(t, r"(?m)^Scope: environment,")
        self.assertNotEqual(re.search(r"^Source thread:.*$", t, re.M).group(0), re.search(r"^Source thread:.*$", t51, re.M).group(0))
        self.assertRegex(t, r"(?i)refused")

    def test_51_and_52_are_severe(self):
        for n in (51, 52):
            self.assertRegex(self.read(f"issues/{n}.md"), r"(?i)work was lost|commits were lost")

    def test_53_is_a_skill_retro_in_two_threads_and_not_severe(self):
        t = self.read("issues/53.md")
        self.assertRegex(t, r"(?m)^Scope: skill,")
        self.assertRegex(t, r"Seen again in fixture-D")
        self.assertIn("nothing was lost", t)
        self.assertNotRegex(t, r"(?i)work was lost|security|data loss|large waste")

    def test_54_is_another_projects_own_lesson_with_a_local_tracker(self):
        t = self.read("issues/54.md")
        self.assertRegex(t, r"(?m)^Scope: this repo,")
        self.assertIn("acme-app", t)
        self.assertIn("other-project/issues/", t)
        self.assertTrue((self.out / "other-project/issues").is_dir())
        self.assertEqual(list((self.out / "other-project/issues").iterdir()), [])
        self.assertIn("acme-app", self.read("other-project/docs/agents/issue-tracker.md"))

    def test_release_end_inputs_are_present(self):
        self.assertIn("next-release", self.read("docs/agents/triage-labels.md"))
        self.assertIn("issues/31.md", self.read("issues/30.md"))
        self.assertIn("#33", self.read("issues/31.md"))
        self.assertIn("State: closed", self.read("issues/30.md"))
        self.assertFalse(any("boundar" in p.name.lower() for p in self.out.rglob("*") if p.is_file()))
        self.assertFalse(any("retro-planning" in p.read_text() for p in (self.out / "issues").glob("*.md")))

    def test_prompt_names_checkout_and_asks_no_user(self):
        p = self.read("PROMPT.md")
        self.assertIn("Nobody is available", p)
        self.assertIn("issues/30.md", p)
        self.assertNotRegex(p, r"(?i)scope|environment|worker-control|startup verification|refile")
        self.assertIn("You may also write to other-project/issues/ (another project's tracker).", p)
        sc.build(self.out, "/x/checkout")
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

    def edit(self, rel, old, new):
        p = self.out / rel
        s = p.read_text()
        self.assertIn(old, s)
        p.write_text(s.replace(old, new))

    def test_main_behaviour_fails(self):
        """Root cause only: no Scope, a Ticket per skill sentence, #54 decided here and nothing refiled."""
        def m(out):
            (out / "other-project/issues/1.md").unlink()
            (out / "issues/54.md").write_text(sc.ISSUES[54].replace("State: open", "State: closed").replace("Labels: retro", "Labels: retro, wontfix")
                                              .replace("## Comments\nNone", "## Comments\nOne thread. Closed as wontfix."))
            (out / "issues/55.md").write_text(
                "# Tell threads to push only to their designated branch\nState: open\nLabels: enhancement, ready-for-agent\nCreated: 2026-11-08\n"
                "Absorbs #51, #52.\nAdd a sentence to implement, implement-spec and release.\n## Done when\nEach skill says it.\n## Comments\nNone\n")
            (out / "issues/56.md").write_text(
                "# Retro planning 2026-11-08\nState: closed\nLabels: retro-planning\nCreated: 2026-11-08\n## Verdicts\n"
                "| push limit | #51, #52 | 2 | Ticket | #55 |\n| template | #53 | 2 | Ticket | none |\n| date | #54 | 1 | wontfix | one thread |\n")
        reference(self.out)
        m(self.out)
        ok, bad = passes(self.out)
        self.assertFalse(ok)
        for part in ("gives #51 the Scope", "refiled in other-project", "Harness reference", "next-release"):
            self.assertTrue(any(part in b for b in bad), (part, bad))

    def test_51_left_without_a_scope_in_the_record_fails(self):
        self.planted(lambda out: self.edit("issues/56.md", "| #51 | environment (given here: the sandbox refuses a push to any other branch) |", "| #51 | |"), "gives #51 the Scope")

    def test_51_given_the_wrong_scope_fails(self):
        self.planted(lambda out: self.edit("issues/56.md", "| #51 | environment (given here: the sandbox refuses a push to any other branch) |", "| #51 | skill |"), "gives #51 the Scope")

    def test_mixed_scope_group_fails(self):
        self.planted(lambda out: self.edit("issues/56.md", "| #51, #52 |", "| #51, #52, #53 |"), "two Scopes")

    def test_sentence_in_each_skill_fails(self):
        self.planted(lambda out: self.edit("issues/55.md", "Fix: the limit", "Add a warning line to each skill that starts work. Fix: the limit"), "sentence in each skill")

    def test_add_a_sentence_to_named_skills_fails(self):
        self.planted(lambda out: self.edit("issues/55.md", "Fix: the limit", "Add a sentence to implement, implement-spec and release. Fix: the limit"), "sentence in each skill")

    def test_negated_sentence_in_each_skill_passes(self):
        reference(self.out)
        self.edit("issues/55.md", "Fix: the limit", "Do not add a sentence to implement, implement-spec and release; add it instead of a line in each skill. Fix: the limit")
        ok, bad = passes(self.out)
        self.assertTrue(ok, bad)

    def test_harness_reference_wording_passes(self):
        reference(self.out)
        self.edit("issues/55.md", "worker-control", "the Harness reference")
        ok, bad = passes(self.out)
        self.assertTrue(ok, bad)

    def test_two_ticket_run_passes(self):
        reference(self.out)
        (self.out / "issues/55.md").write_text(TICKET.replace("Absorbs #51, #52.", "Absorbs #51."))
        (self.out / "issues/57.md").write_text(TICKET.replace("Absorbs #51, #52.", "Absorbs #52.").replace("Record the", "Also record the"))
        self.edit("issues/52.md", "Absorbed by #55", "Absorbed by #57")
        ok, bad = passes(self.out)
        self.assertTrue(ok, bad)

    def test_ticket_mentioning_53_without_absorbing_it_passes(self):
        reference(self.out)
        self.edit("issues/55.md", "Absorbs #51, #52.", "Absorbs #51, #52. Not absorbing #53 or #54.")
        ok, bad = passes(self.out)
        self.assertTrue(ok, bad)

    def test_ticket_without_next_release_fails_among_two(self):
        def m(out):
            (out / "issues/57.md").write_text(TICKET.replace("Absorbs #51, #52.", "Absorbs #52.").replace("next-release", "bug"))
        self.planted(m, "joins the next Release")

    def test_scope_word_outside_snapshot_and_verdicts_is_ignored(self):
        def m(out):
            self.edit("issues/56.md", "| #51 | environment (given here: the sandbox refuses a push to any other branch) |", "| #51 | |")
            self.edit("issues/56.md", "## Tickets filed", "## Notes\n| #51 | environment |\n\n## Tickets filed")
        self.planted(m, "gives #51 the Scope")

    def test_ticket_without_the_harness_reference_fails(self):
        def m(out):
            p = out / "issues/55.md"
            p.write_text(re.sub(r"worker-control|Harness reference", "the docs", p.read_text()))
        self.planted(m, "Harness reference")

    def test_ticket_absorbing_the_skill_retro_fails(self):
        self.planted(lambda out: self.edit("issues/55.md", "Absorbs #51, #52.", "Absorbs #51, #52, #53."), "absorbs only #51 and #52")

    def test_misfiled_retro_left_in_place_fails(self):
        def m(out):
            (out / "other-project/issues/1.md").unlink()
        self.planted(m, "refiled in other-project")

    def test_misfiled_retro_not_closed_with_a_link_fails(self):
        self.planted(lambda out: self.edit("issues/54.md", "Refiled in other-project/issues/1.md; closed here.", "Closed here."), "closed here with a comment linking")

    def test_record_left_open_fails(self):
        self.planted(lambda out: self.edit("issues/56.md", "State: closed", "State: open"), "one planning record")

    def test_changed_docs_fail(self):
        self.planted(lambda out: (out / "docs/index.md").write_text("changed"), "unchanged")


if __name__ == "__main__":
    unittest.main()
