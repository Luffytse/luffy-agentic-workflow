#!/usr/bin/env python3
"""Exercise plugin packaging through the checker CLI using disposable repositories."""
import pathlib
import shutil
import subprocess
import tempfile
import unittest


class SkillLoadingPackaging(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = pathlib.Path(self.temp.name) / "repo"
        source = pathlib.Path(__file__).resolve().parents[1]
        shutil.copytree(source, self.repo, symlinks=True, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.skill = self.repo / "plugins/dev-skills/skills/fixture-contract"
        (self.skill / "agents").mkdir(parents=True)
        self.write_skill("user-invocable: false\n")
        self.write_policy("  allow_implicit_invocation: true\n")

    def write_skill(self, controls):
        (self.skill / "SKILL.md").write_text(
            "---\nname: fixture-contract\ndescription: Use when a caller needs the fixture contract.\n"
            + controls + "---\n\nReturn the fixture record.\n"
        )

    def write_policy(self, policy):
        (self.skill / "agents/openai.yaml").write_text(
            'interface:\n  display_name: "Fixture Contract"\n'
            '  short_description: "Interpret fixture records"\npolicy:\n' + policy
        )

    def check(self, expected):
        result = subprocess.run(
            ["bash", str(self.repo / "scripts/check-plugin.sh")],
            cwd=self.repo, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_hidden_reference_remains_model_loadable(self):
        self.check(0)

    def test_visible_skill_remains_supported(self):
        self.write_skill("")
        self.check(0)

    def test_hidden_skill_cannot_disable_model_invocation(self):
        self.write_skill("user-invocable: false\ndisable-model-invocation: true\n")
        self.check(1)

    def test_hidden_skill_cannot_disable_implicit_invocation(self):
        self.write_policy("  allow_implicit_invocation: false\n")
        self.check(1)

    def test_hidden_skill_still_requires_agent_metadata(self):
        (self.skill / "agents/openai.yaml").unlink()
        self.check(1)

    def test_missing_boundary_seed_fails(self):
        (self.repo / "plugins/dev-skills/skills/setup-dev-skills/boundaries.md").unlink()
        self.check(1)

    def test_missing_boundary_record_fails(self):
        (self.repo / "docs/dev-skills/boundaries.md").unlink()
        self.check(1)

    def test_missing_release_doc_fails(self):
        (self.repo / "docs/dev-skills/release.md").unlink()
        self.check(1)

    def test_person_name_in_glossary_fails(self):
        self.plant("docs/dev-skills/glossary.md", "Ask Lu" + "fei.\n")
        self.check(1)

    def test_skill_file_over_5000_words_fails_and_under_passes(self):
        self.plant("plugins/dev-skills/skills/implement/SKILL.md", "word " * 5000)
        self.check(1)
        shutil.copy(pathlib.Path(__file__).resolve().parents[1] / "plugins/dev-skills/skills/implement/SKILL.md",
                    self.repo / "plugins/dev-skills/skills/implement/SKILL.md")
        self.plant("plugins/dev-skills/skills/implement/SKILL.md", "word " * 100)
        self.check(0)

    def test_new_reference_file_over_5000_words_fails(self):
        (self.skill / "big.md").write_text("word " * 5001)
        self.check(1)
        (self.skill / "big.md").write_text("word " * 4999)
        self.check(0)

    def test_known_over_file_may_not_grow(self):
        self.plant("plugins/dev-skills/skills/release/SKILL.md", "word " * 5)
        self.check(1)

    def test_known_over_file_under_the_limit_must_leave_the_list(self):
        path = self.repo / "plugins/dev-skills/skills/release/SKILL.md"
        path.write_text("word " * 4000)
        self.check(1)

    def test_known_over_file_that_is_gone_must_leave_the_list(self):
        (self.repo / "plugins/dev-skills/skills/release/SKILL.md").rename(
            self.repo / "plugins/dev-skills/skills/release/NOTES.md")
        self.check(1)

    def test_known_over_file_that_shrinks_passes(self):
        path = self.repo / "plugins/dev-skills/skills/release/SKILL.md"
        words = path.read_text().split(" ")
        path.write_text(" ".join(words[:-20]))
        self.check(0)

    def plant(self, rel, text="Run it on Son" + "net.\n"):
        with open(self.repo / rel, "a") as f:
            f.write("\n" + text)

    def test_model_name_in_readme_fails(self):
        self.plant("plugins/dev-skills/README.md")
        self.check(1)

    def test_model_name_in_other_skill_fails(self):
        self.plant("plugins/dev-skills/skills/implement/SKILL.md")
        self.check(1)

    def test_model_tiers_reference_is_exempt(self):
        self.plant("plugins/dev-skills/skills/model-tiers/SKILL.md")
        self.check(0)

    def test_every_tier_naming_skill_points_at_the_map(self):
        skills = self.repo / "plugins/dev-skills/skills"
        for name in ["implement", "implement-spec", "review-rounds", "to-tickets",
                     "release", "retro-planning", "setup-project"]:
            self.assertIn("model-tiers", (skills / name / "SKILL.md").read_text(), name)

    def test_repo_only_merge_rules_in_skill_text_fail(self):
        for text in ("The coordinator hands out the next version number.\n",
                     "Hand out version numbers one at a time.\n",
                     "Re-read open Tickets after a skill merge.\n",
                     "Re-read open issues after a merge.\n"):
            self.plant("plugins/dev-skills/skills/implement/SKILL.md", text)
            self.check(1)
            shutil.copy(pathlib.Path(__file__).resolve().parents[1] / "plugins/dev-skills/skills/implement/SKILL.md",
                        self.repo / "plugins/dev-skills/skills/implement/SKILL.md")

    def test_no_shipped_skill_states_the_repo_only_merge_rules(self):
        self.check(0)

    def cite(self, text):
        (self.skill / "SKILL.md").write_text(
            "---\nname: fixture-contract\ndescription: Use when a caller needs the fixture contract.\n"
            "user-invocable: false\n---\n\n" + text + "\n"
        )
        return subprocess.run(
            ["bash", str(self.repo / "scripts/check-plugin.sh")],
            cwd=self.repo, text=True, capture_output=True,
        )

    def test_cited_tracker_operation_that_exists_passes(self):
        for cite in ('the tracker doc\'s **Close** operation', 'the tracker doc\'s "Comment on an issue" operation'):
            result = self.cite(cite)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_cited_park_operation_exists_in_the_seed(self):
        for cite in ('the tracker doc\'s **Park** operation', 'the tracker doc\'s "Park" operation'):
            result = self.cite(cite)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_build_skills_cite_park_and_the_seed_defines_it(self):
        skills = self.repo / "plugins/dev-skills/skills"
        seed = (skills / "setup-dev-skills/issue-tracker-github.md").read_text()
        self.assertIn("- **Park**", seed)
        for name in ["implement", "implement-spec"]:
            self.assertIn("tracker doc's **Park** operation", (skills / name / "SKILL.md").read_text(), name)

    def worker_reference(self):
        return self.repo / "plugins/dev-skills/skills/worker-control/claude-code-project-threads.md"

    def run_checker(self):
        return subprocess.run(["bash", str(self.repo / "scripts/check-plugin.sh")],
                              cwd=self.repo, text=True, capture_output=True)

    def test_worker_reference_method_without_source_fails(self):
        self.plant("plugins/dev-skills/skills/worker-control/claude-code-project-threads.md",
                   "### Wake a worker\n\nSend it a message; it wakes.\n")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Wake a worker", result.stdout)

    def test_team_lead_naming_a_harness_tool_fails(self):
        for text in ("Read the state with `list_threads`.\n", "Start it with mcp__hearthbot__start_thread.\n"):
            self.plant("plugins/dev-skills/skills/team-lead/SKILL.md", text)
            result = self.run_checker()
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("team-lead-no-harness-detail", result.stdout)
            shutil.copy(pathlib.Path(__file__).resolve().parents[1] / "plugins/dev-skills/skills/team-lead/SKILL.md",
                        self.repo / "plugins/dev-skills/skills/team-lead/SKILL.md")

    def test_shipped_team_lead_names_no_harness_detail(self):
        self.check(0)

    def test_milestone_naming_a_harness_tool_fails(self):
        for text in ("Read the state with `list_threads`.\n", "Start it with mcp__hearthbot__start_thread.\n"):
            self.plant("plugins/dev-skills/skills/milestone/SKILL.md", "team-lead\n" + text)
            result = self.run_checker()
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("milestone-no-delivery-detail", result.stdout)
            self.assertNotIn("does not name team-lead", result.stdout)
            self.assertRegex(result.stdout, r"milestone/SKILL\.md:\d+: names (list_threads|mcp__hearthbot)")
            shutil.copy(pathlib.Path(__file__).resolve().parents[1] / "plugins/dev-skills/skills/milestone/SKILL.md",
                        self.repo / "plugins/dev-skills/skills/milestone/SKILL.md")

    def test_milestone_check_fails_when_worker_control_references_yield_no_names(self):
        for ref in (self.repo / "plugins/dev-skills/skills/worker-control").glob("*.md"):
            if ref.name != "SKILL.md":
                ref.write_text(ref.read_text().replace("`", ""))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("worker-control references yield no backticked names", result.stdout)

    def test_milestone_holding_a_delivery_record_kind_fails(self):
        self.plant("plugins/dev-skills/skills/milestone/reporting.md", "Post `<!-- milestone nudge -->` on the issue.\n")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("milestone-no-delivery-detail", result.stdout)

    def test_milestone_not_naming_team_lead_fails(self):
        path = self.repo / "plugins/dev-skills/skills/milestone/SKILL.md"
        path.write_text(path.read_text().replace("team-lead", "delivery"))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("milestone-no-delivery-detail", result.stdout)

    def test_shipped_milestone_holds_no_delivery_detail(self):
        self.check(0)

    def test_worker_reference_method_with_source_passes(self):
        self.plant("plugins/dev-skills/skills/worker-control/claude-code-project-threads.md",
                   "### Wake a worker\n\nSend it a message.\nSource: [page](https://example.com/docs/wake)\n")
        self.check(0)

    def test_worker_reference_fact_without_doc_link_fails(self):
        path = self.worker_reference()
        text = path.read_text().replace(
            "## What the harness does by itself\n",
            "## What the harness does by itself\n\n- **Guessed.** Threads never die.\n", 1)
        path.write_text(text)
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Guessed", result.stdout)

    def test_worker_reference_reference_without_methods_fails(self):
        (self.repo / "plugins/dev-skills/skills/worker-control/new-harness.md").write_text(
            "# New harness\n\n## Detect\n\n- It says so. Source: [docs](https://example.com)\n")
        self.check(1)

    def test_cited_tracker_operation_missing_from_tracker_doc_fails(self):
        for cite in ('the tracker doc\'s **Comment** operation', 'the tracker doc\'s "Comment" operation'):
            result = self.cite("Intro line.\n" + cite)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("fixture-contract/SKILL.md:8", result.stdout)
            self.assertIn("Comment", result.stdout)


if __name__ == "__main__":
    unittest.main()
