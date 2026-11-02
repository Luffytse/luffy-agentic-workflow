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
        (self.repo / "docs/agents/boundaries.md").unlink()
        self.check(1)

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
        for name in ["implement", "implement-spec", "agentic-review", "to-tickets",
                     "release", "retro-planning", "setup-project"]:
            self.assertIn("model-tiers", (skills / name / "SKILL.md").read_text(), name)

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

    def test_cited_tracker_operation_missing_from_tracker_doc_fails(self):
        for cite in ('the tracker doc\'s **Comment** operation', 'the tracker doc\'s "Comment" operation'):
            result = self.cite("Intro line.\n" + cite)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("fixture-contract/SKILL.md:8", result.stdout)
            self.assertIn("Comment", result.stdout)


if __name__ == "__main__":
    unittest.main()
