#!/usr/bin/env python3
"""Exercise plugin packaging through the checker CLI using disposable repositories."""
import json
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

    def check(self, expected, message=None):
        result = subprocess.run(
            ["bash", str(self.repo / "scripts/check-plugin.sh")],
            cwd=self.repo, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        if message:
            self.assertIn(message, result.stdout + result.stderr)

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

    def test_unlisted_skill_file_over_4000_words_fails(self):
        (self.skill / "big.md").write_text("word " * 4001)
        self.check(1)

    def test_skill_file_of_exactly_4000_words_passes(self):
        (self.skill / "big.md").write_text("word " * 4000)
        self.check(0)

    def test_unlisted_existing_skill_over_4000_words_fails_and_under_passes(self):
        self.plant("plugins/dev-skills/skills/implement/SKILL.md", "word " * 4000)
        self.check(1)
        shutil.copy(pathlib.Path(__file__).resolve().parents[1] / "plugins/dev-skills/skills/implement/SKILL.md",
                    self.repo / "plugins/dev-skills/skills/implement/SKILL.md")
        self.plant("plugins/dev-skills/skills/implement/SKILL.md", "word " * 100)
        self.check(0)

    def test_listed_skill_file_that_grew_fails(self):
        # release/SKILL.md is on known_over: it may not grow past its recorded count.
        self.plant("plugins/dev-skills/skills/release/SKILL.md", "word")
        self.check(1, "grown past its recorded")

    def test_listed_skill_file_at_or_under_4000_words_must_leave_the_list(self):
        (self.repo / "plugins/dev-skills/skills/release/SKILL.md").write_text(
            "---\nname: release\ndescription: Use when cutting a Release.\n---\n\n" + "word " * 3900)
        self.check(1, "remove it from known_over")

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

    def test_spaced_gpt_name_fails(self):
        self.plant("plugins/dev-skills/skills/implement/SKILL.md", "Run it on GP" + "T 6.\n")
        self.check(1)

    def test_o_series_name_fails(self):
        self.plant("plugins/dev-skills/skills/implement/SKILL.md", "Use o" + "4-mini for this.\n")
        self.check(1)

    def test_underscore_joined_and_digit_prefixed_o_series_digits_pass(self):
        # Covers only underscore-joined (foo_o3_bar) and digit-prefixed (4o3) identifiers;
        # hyphen- or dot-joined ones are flagged by design.
        self.plant("plugins/dev-skills/skills/implement/SKILL.md", "Set foo_o" + "3_bar and version 4o3.\n")
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

    def fails_with(self, needle):
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(needle, result.stdout)

    def test_stray_file_in_skills_fails(self):
        (self.repo / "plugins/dev-skills/skills/notes.md").write_text("x\n")
        self.fails_with("stray file in skills: notes.md")

    def test_skill_folder_without_skill_md_fails(self):
        (self.skill / "SKILL.md").unlink()
        self.fails_with("skill folder fixture-contract has no SKILL.md")

    def test_frontmatter_name_differing_from_folder_fails(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text().replace("name: fixture-contract", "name: fixture-other"))
        self.fails_with('frontmatter name "fixture-other" differs from its folder name')

    def test_broken_relative_link_in_skill_md_fails(self):
        self.plant("plugins/dev-skills/skills/fixture-contract/SKILL.md", "See [the rules](RULES.md#top).\n")
        self.fails_with("fixture-contract/SKILL.md links RULES.md, which does not exist")
        (self.skill / "RULES.md").write_text("# Rules\n")
        self.check(0)

    def test_missing_changelog_fails(self):
        (self.repo / "plugins/dev-skills/CHANGELOG.md").unlink()
        self.fails_with("missing CHANGELOG.md")

    def test_manifest_without_repository_fails(self):
        path = self.repo / "plugins/dev-skills/.claude-plugin/plugin.json"
        path.write_text(path.read_text().replace('"repository"', '"homepage"'))
        self.fails_with("plugin.json has no repository field")

    def test_codex_version_drift_fails(self):
        path = self.repo / "plugins/dev-skills/.codex-plugin/plugin.json"
        data = json.loads(path.read_text())
        data["version"] = "9.9.9"
        path.write_text(json.dumps(data))
        self.fails_with("Codex manifest version differs from Claude manifest")

    def test_codex_marketplace_offering_a_second_plugin_fails(self):
        path = self.repo / ".agents/plugins/marketplace.json"
        data = json.loads(path.read_text())
        data["plugins"].append(dict(data["plugins"][0], name="other-plugin"))
        path.write_text(json.dumps(data))
        self.fails_with("Codex marketplace must offer only dev-skills")

    def test_missing_release_skill_fails(self):
        shutil.rmtree(self.repo / "plugins/dev-skills/skills/release")
        self.fails_with("missing plugins/dev-skills/skills/release/SKILL.md")

    def test_display_name_of_another_skill_fails(self):
        path = self.skill / "agents/openai.yaml"
        path.write_text(path.read_text().replace("Fixture Contract", "Implement"))
        self.fails_with('display_name "Implement" does not match the skill name')

    def test_repo_only_names_in_skill_text_fail(self):
        for text in ("Read ADR " + "0004 first.\n", "Ask Upstream.\n", "Run scripts/check-" + "plugin.sh.\n"):
            self.cite(text)
            self.fails_with("skill text names something only this repo has")
        self.cite("Return the fixture record.")
        # An example index line linking its own ADR file, and lowercase "upstream", are fine (in a reference file,
        # whose links skill-links does not follow).
        (self.skill / "example.md").write_text("- [ADR " + "0003](adr/0003-x.md): an example line; the upstream repo.\n")
        self.check(0)

    def test_agent_label_string_in_plugin_fails(self):
        self.cite("Label it claude" + "-only.")
        self.fails_with("plugin text names an agent-only label string")

    def test_skill_text_may_name_merge_steps_and_rereads(self):
        # The no-repo-merge-rules check is gone: the two rules it guarded skill text against no longer exist.
        self.cite("After a skill merge, re-read the open issues and hand out the next version number.")
        self.check(0)
        self.cite("Ask for the version hand" + "-out, then the Ticket re" + "-read.")
        self.check(0)


if __name__ == "__main__":
    unittest.main()
