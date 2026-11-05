#!/usr/bin/env python3
"""Exercise scripts/check-public-history.py on disposable repositories.

Each test plants one private trace (a dai-portal plugin path, a personal email as author and in a file, a
session link in a commit message, a home-folder path, a database name, a Mac hostname) and checks that the
check fails naming the commit; a clean history passes. The planted strings are built from pieces, because
this file is published with the history the check guards and must not trip the check itself.
"""
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parent
CHECK = SCRIPTS / "check-public-history.py"

OWNER = "Luffytse <12742482+Luffytse@users.noreply.github.com>"
CLAUDE = "Claude <noreply@anthropic.com>"
PERSONAL_EMAIL = "pat.person" + "@mail.example"
SESSION_LINK = "https://" + "claude.ai/code/" + "session_01" + "AbCdEfGhIjKlMnOpQrStUv"
HOME_PATH = "/" + "Users/patmac" + "/work/notes.md"
PLUGIN_DIR = "plugins/" + "dai-portal-data"
DB_NAME = "dai" + "_widgets_dev"
CSE_ID = "cse_01" + "AbCdEfGhIjKlMnOpQrStUv"
TRIG_ID = "trig_01" + "AbCdEfGhIjKlMnOpQrStUv"


def git(repo, *args, env=None, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True,
                          env=env, check=check).stdout.strip()


def ident_env(author, committer=None):
    committer = committer or author
    name, email = author[:-1].split(" <")
    cname, cemail = committer[:-1].split(" <")
    env = dict(os.environ)
    env.update(GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email, GIT_COMMITTER_NAME=cname,
               GIT_COMMITTER_EMAIL=cemail, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    return env


class Repo:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.path.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.path)], check=True)

    def commit(self, message, files=None, remove=(), author=OWNER, committer=None):
        for name, text in (files or {}).items():
            target = self.path / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
            git(self.path, "add", name)
        for name in remove:
            git(self.path, "rm", "-rq", name)
        env = ident_env(author, committer)
        git(self.path, "commit", "-q", "--allow-empty", "-m", message, env=env)
        return git(self.path, "rev-parse", "HEAD")


def run_check(repo, *args):
    return subprocess.run([sys.executable, str(CHECK), "--repo", str(repo), *args],
                          text=True, capture_output=True)


class CheckPublicHistory(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.repo = Repo(self.root / "repo")
        self.repo.commit("feat: start\n", {"README.md": "Hello, see ~/notes and https://claude.ai/code\n"})

    def assert_fails_naming(self, sha, kind, *args):
        result = run_check(self.repo.path, *args)
        out = result.stdout + result.stderr
        self.assertEqual(result.returncode, 1, out)
        lines = [line for line in out.splitlines() if line.startswith("FAIL " + sha)]
        self.assertTrue(lines, f"no FAIL line names {sha}:\n{out}")
        self.assertTrue(any(kind in line for line in lines), f"no '{kind}' finding for {sha}:\n{out}")
        return out

    def test_clean_history_passes(self):
        self.repo.commit(
            "feat: more\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n",
            {"docs/a.md": "Run it from ~/src. Mail fixture@example.invalid.\n"},
            author=CLAUDE, committer="GitHub <noreply@github.com>")
        result = run_check(self.repo.path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_plugin_folder_in_an_earlier_commit_fails(self):
        sha = self.repo.commit("add plugin\n", {PLUGIN_DIR + "/README.md": "plugin\n"})
        self.repo.commit("drop plugin\n", remove=[PLUGIN_DIR])
        self.assert_fails_naming(sha, "dai-portal path")

    def test_personal_author_email_fails(self):
        sha = self.repo.commit("fix: typo\n", {"b.md": "b\n"}, author="Pat <" + PERSONAL_EMAIL + ">")
        self.assert_fails_naming(sha, "personal email")

    def test_personal_committer_email_fails(self):
        sha = self.repo.commit("fix: typo\n", {"b.md": "b\n"}, committer="Pat <" + PERSONAL_EMAIL + ">")
        self.assert_fails_naming(sha, "personal email")

    def test_personal_email_in_a_file_fails(self):
        # The email is known from the source history (its author field), as in the rewrite's own check.
        source = Repo(self.root / "source")
        source.commit("init\n", {"x": "x\n"}, author="Pat <" + PERSONAL_EMAIL + ">")
        sha = self.repo.commit("docs: log\n", {"evals/log.txt": "Author: Pat <" + PERSONAL_EMAIL + ">\n"})
        self.assert_fails_naming(sha, "personal email", "--source", str(source.path))

    def test_personal_email_in_a_file_fails_from_a_terms_file(self):
        terms = self.root / "terms.txt"
        terms.write_text("# private terms\n" + PERSONAL_EMAIL + "\n")
        sha = self.repo.commit("docs: log\n", {"evals/log.txt": "mail " + PERSONAL_EMAIL.upper() + "\n"})
        self.assert_fails_naming(sha, "private term", "--terms", str(terms))

    def test_session_link_in_a_commit_message_fails(self):
        sha = self.repo.commit("feat: x\n\n" + SESSION_LINK + "\n", {"c.md": "c\n"})
        self.assert_fails_naming(sha, "session link")

    def test_session_trailer_in_a_commit_message_fails(self):
        sha = self.repo.commit("feat: x\n\n" + "Claude-" + "Session: elsewhere\n", {"c.md": "c\n"})
        self.assert_fails_naming(sha, "session link")

    def test_session_link_and_bare_session_id_in_a_file_fail(self):
        sha = self.repo.commit("docs: r\n", {"r.md": "see " + SESSION_LINK + "\n"})
        self.assert_fails_naming(sha, "session link")
        sha2 = self.repo.commit("docs: r2\n", {"r2.md": "session `" + SESSION_LINK.rsplit("/", 1)[1] + "`\n"})
        self.assert_fails_naming(sha2, "session link")

    def test_code_session_and_trigger_ids_fail(self):
        sha = self.repo.commit("docs: r\n", {"r.md": "session `" + CSE_ID + "` done\n"})
        self.assert_fails_naming(sha, "session link")
        sha2 = self.repo.commit("chore: t\n\nFired by trigger " + TRIG_ID + ".\n", {"t.md": "t\n"})
        self.assert_fails_naming(sha2, "session link")

    def test_root_commit_is_scanned_whatever_the_user_config(self):
        repo = Repo(self.root / "rooted")
        sha = repo.commit("add plugin\n", {PLUGIN_DIR + "/README.md": "plugin\n"})
        repo.commit("drop plugin\n", remove=[PLUGIN_DIR])
        env = dict(os.environ, GIT_CONFIG_COUNT="2", GIT_CONFIG_KEY_0="log.showRoot", GIT_CONFIG_VALUE_0="false",
                   GIT_CONFIG_KEY_1="log.diffMerges", GIT_CONFIG_VALUE_1="first-parent")
        result = subprocess.run([sys.executable, str(CHECK), "--repo", str(repo.path)], text=True,
                                capture_output=True, env=env)
        out = result.stdout + result.stderr
        self.assertEqual(result.returncode, 1, out)
        self.assertTrue(any(line.startswith("FAIL " + sha) and "dai-portal path" in line
                            for line in out.splitlines()), out)

    def test_counts_of_derived_values_are_printed_and_zero_emails_warn(self):
        result = run_check(self.repo.path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("derived 0 personal emails, 0 hostnames, 0 database names, 0 terms", result.stdout)
        self.assertIn("WARNING", result.stdout)
        self.assertIn("--source", result.stdout)
        source = Repo(self.root / "source")
        source.commit("init\n", {"x": "x\n"}, author="Pat <" + PERSONAL_EMAIL + ">")
        result = run_check(self.repo.path, "--source", str(source.path))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("derived 1 personal emails,", result.stdout)
        self.assertNotIn("WARNING", result.stdout)
        self.assertNotIn(PERSONAL_EMAIL, result.stdout)

    def test_project_link_in_a_commit_message_fails(self):
        link = "https://" + "claude.ai/code/" + "project/chan_01AbCdEfGhIjKlMnOp"
        sha = self.repo.commit("plan\n\nPlanned in " + link + "\n", {"d.md": "d\n"})
        self.assert_fails_naming(sha, "session link")

    def test_home_path_in_a_file_fails(self):
        sha = self.repo.commit("docs: e\n", {"e.md": "open " + HOME_PATH + "\n"})
        self.assert_fails_naming(sha, "home path")

    def test_home_path_in_a_commit_message_fails(self):
        sha = self.repo.commit("fix: path " + HOME_PATH + "\n", {"e.md": "e\n"})
        self.assert_fails_naming(sha, "home path")

    def test_database_name_outside_the_plugin_fails(self):
        source = Repo(self.root / "source")
        source.commit("plugin\n", {PLUGIN_DIR + "/s.sh": "psql -d " + DB_NAME + "\n"})
        sha = self.repo.commit("docs: db\n", {"notes.md": "the " + DB_NAME + " database\n"})
        self.assert_fails_naming(sha, "private term", "--source", str(source.path))

    def test_mac_hostname_email_fails_in_a_file(self):
        sha = self.repo.commit("docs: h\n", {"h.md": "From: pat@" + "Pats-Mac" + ".local\n"})
        self.assert_fails_naming(sha, "hostname")

    def test_ref_option_limits_the_walk(self):
        git(self.repo.path, "checkout", "-q", "-b", "side")
        self.repo.commit("feat: x\n\n" + SESSION_LINK + "\n")
        git(self.repo.path, "checkout", "-q", "main")
        self.assertEqual(run_check(self.repo.path, "--ref", "main").returncode, 0)
        self.assertEqual(run_check(self.repo.path).returncode, 1)

    def test_these_scripts_do_not_trip_the_check(self):
        files = {p.name: p.read_text() for p in SCRIPTS.glob("*public-history*.py")}
        self.assertGreaterEqual(len(files), 2, files.keys())
        self.repo.commit("add scripts\n", {"scripts/" + n: t for n, t in files.items()})
        result = run_check(self.repo.path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
