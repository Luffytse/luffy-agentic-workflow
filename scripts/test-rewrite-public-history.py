#!/usr/bin/env python3
"""Exercise scripts/rewrite-public-history.py on disposable repositories and a local bare remote.

A seeded source repo holds each private trace the pre-publish check looks for. The rewrite's result must
pass the check, keep every commit message otherwise (the Anthropic co-author line included), leave the
source untouched, push only main and nothing else, and refuse to push when the check fails. Planted
strings are built from pieces, because this file is published with the history the check guards.
"""
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True  # a test*.pyc in scripts/__pycache__ would be run (and failed) by run-tests.sh
SCRIPTS = pathlib.Path(__file__).resolve().parent
REWRITE = SCRIPTS / "rewrite-public-history.py"
CHECK = SCRIPTS / "check-public-history.py"

spec = importlib.util.spec_from_file_location("check_test_helpers", SCRIPTS / "test-check-public-history.py")
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
Repo, git, run_check = helpers.Repo, helpers.git, helpers.run_check

OWNER_EMAIL = "12742482+Luffytse@users.noreply.github.com"
PERSONAL = "Pat <" + helpers.PERSONAL_EMAIL + ">"
MAC = "Pat <pat@" + "Pats-Mac" + ".local>"
CO_AUTHOR = "Co-Authored-By: Claude <noreply@anthropic.com>"
TRAILER = "Claude-" + "Session: " + helpers.SESSION_LINK
PROJECT_LINK = "https://" + "claude.ai/code/" + "project/chan_01AbCdEfGhIjKlMnOp?thread=cmsg_01Xy"
SESSION_ID = helpers.SESSION_LINK.rsplit("/", 1)[1]
PLUGIN = helpers.PLUGIN_DIR
DB = helpers.DB_NAME
HAS_FILTER_REPO = subprocess.run(["git", "filter-repo", "--version"], capture_output=True).returncode == 0


def seed(root):
    src = Repo(root / "source")
    src.commit("feat: add plugin\n", {PLUGIN + "/s.sh": "psql -d " + DB + "\n", "README.md": "Hi\n"},
               author=PERSONAL)
    src.commit("docs: readme\n\nUses the " + DB + " schema.\n\n" + CO_AUTHOR + "\n" + TRAILER + "\n",
               {"README.md": "Hi, the `" + DB + "` schema. Mail " + helpers.PERSONAL_EMAIL + "\n"},
               author=helpers.CLAUDE, committer=MAC)
    src.commit("chore: drop plugin\n", remove=[PLUGIN], author=MAC, committer="GitHub <noreply@github.com>")
    src.commit("docs: evidence\n\nPlanned in [the thread](" + PROJECT_LINK + ").\nTrigger " + helpers.TRIG_ID
               + ".\n\n" + CO_AUTHOR + "\n",
               {"evals/r.md": "Run in " + helpers.HOME_PATH + "\n" + helpers.SESSION_LINK + "\n"
                + "_Made by [Claude Code](" + helpers.SESSION_LINK + ")_ in session `" + SESSION_ID + "`.\n"
                + "Code session `" + helpers.CSE_ID + "`, trigger " + helpers.TRIG_ID + ".\n"},
               author=helpers.OWNER, committer="GitHub <noreply@github.com>")
    git(src.path, "tag", "v1")
    git(src.path, "branch", "side")
    return src


def rewrite(*args):
    return subprocess.run([sys.executable, str(REWRITE), *map(str, args)], text=True, capture_output=True)


def messages(repo, ref="main"):
    return git(repo, "log", "--reverse", "--format=%B%x00", ref).split("\x00")


@unittest.skipUnless(HAS_FILTER_REPO, "git filter-repo is not installed")
class RewritePublicHistory(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.src = seed(self.root)
        self.work = self.root / "work"
        self.remote = self.root / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", str(self.remote)], check=True)

    def test_no_arguments_prints_the_steps_and_does_nothing(self):
        result = rewrite()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("luffy-agentic-workflow", result.stdout)
        self.assertIn("no initial commit", result.stdout)
        self.assertFalse(self.work.exists())

    def test_dry_run_result_passes_the_check_and_keeps_messages(self):
        before = git(self.src.path, "for-each-ref")
        result = rewrite("--source", self.src.path, "--workdir", self.work, "--dry-run")
        out = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, out)
        self.assertLess(out.index("Steps"), out.index("filter-repo"), "the steps come first")
        self.assertIn("PASS", out)
        self.assertIn("commits on main: 4 before, 3 after", out)
        self.assertIn("DRY RUN", out)
        self.assertIn("files at the tip that the rewrite changed: 2\n  README.md\n  evals/r.md\n", out)
        self.assertEqual(git(self.src.path, "for-each-ref"), before, "the source is untouched")
        self.assertEqual(git(self.remote, "for-each-ref"), "", "nothing was pushed")
        self.assertEqual(git(self.work, "for-each-ref", "--format=%(refname)"), "refs/heads/main")
        # the check passes on its own too, knowing the source's private values
        check = run_check(self.work, "--source", str(self.src.path))
        self.assertEqual(check.returncode, 0, check.stdout)
        msgs = messages(self.work)
        self.assertEqual(msgs[0].strip(), "feat: add plugin")
        self.assertEqual(msgs[1].strip(), "docs: readme\n\nUses the example_db schema.\n\n" + CO_AUTHOR)
        self.assertEqual(msgs[2].strip(), "docs: evidence\n\nPlanned in [the thread](https://claude.ai/code).\nTrigger trig_REMOVED."
                         "\n\n"
                         + CO_AUTHOR)
        idents = set(git(self.work, "log", "--format=%an <%ae>%n%cn <%ce>", "main").splitlines())
        self.assertEqual(idents, {"Claude <noreply@anthropic.com>", "GitHub <noreply@github.com>",
                                  "Luffytse <" + OWNER_EMAIL + ">"})
        self.assertEqual(git(self.work, "show", "main:README.md"),
                         "Hi, the `example_db` schema. Mail " + OWNER_EMAIL)
        self.assertEqual(git(self.work, "show", "main:evals/r.md"),
                         "Run in ~/work/notes.md\n_Made by [Claude Code](https://claude.ai/code)_ in session "
                         "`session_REMOVED`.\nCode session `cse_REMOVED`, trigger trig_REMOVED.")
        self.assertNotIn(PLUGIN, git(self.work, "log", "--name-only", "--format=", "main"))

    def test_push_sends_only_main(self):
        result = rewrite("--source", self.src.path, "--workdir", self.work, "--push-url", self.remote)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(git(self.remote, "for-each-ref", "--format=%(refname)"), "refs/heads/main")
        self.assertEqual(git(self.remote, "rev-parse", "main"), git(self.work, "rev-parse", "main"))

    def test_named_branch_is_pushed_as_main(self):
        git(self.src.path, "checkout", "-q", "side")
        self.src.commit("feat: side work\n", {"side.md": "s\n"})
        result = rewrite("--source", self.src.path, "--branch", "side", "--workdir", self.work,
                         "--push-url", self.remote)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(git(self.remote, "for-each-ref", "--format=%(refname)"), "refs/heads/main")
        self.assertEqual(git(self.remote, "log", "-1", "--format=%s", "main"), "feat: side work")

    def test_refuses_to_push_when_the_check_fails(self):
        # filter-repo leaves binary files alone, so a session link inside one survives the rewrite.
        (self.src.path / "blob.bin").write_bytes(b"\0\x01" + helpers.SESSION_LINK.encode() + b"\n")
        git(self.src.path, "add", "blob.bin")
        bad = self.src.commit("chore: binary\n")
        result = rewrite("--source", self.src.path, "--workdir", self.work, "--push-url", self.remote)
        out = result.stdout + result.stderr
        self.assertEqual(result.returncode, 1, out)
        self.assertIn("FAIL", out)
        self.assertIn("session link", out)
        self.assertIn("not pushed", out)
        self.assertEqual(git(self.remote, "for-each-ref"), "", "nothing was pushed")
        self.assertTrue(bad)

    def test_refuses_a_used_workdir(self):
        self.work.mkdir()
        (self.work / "x").write_text("x")
        result = rewrite("--source", self.src.path, "--workdir", self.work, "--dry-run")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(os.listdir(self.work), ["x"])

    def test_refuses_a_shallow_source(self):
        shallow = self.root / "shallow"
        subprocess.run(["git", "clone", "-q", "--depth", "1", "file://" + str(self.src.path), str(shallow)],
                       check=True)
        result = rewrite("--source", shallow, "--workdir", self.work, "--dry-run")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("shallow", result.stdout + result.stderr)
        self.assertFalse(self.work.exists())


if __name__ == "__main__":
    unittest.main()
