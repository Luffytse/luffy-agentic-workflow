#!/usr/bin/env python3
"""Unit tests of the team-lead skill's snapshot command on fixture tracker and git data.

Run: python3 evals/team-lead/test_snapshot.py
Each test builds a disposable git repo with dated commits and a tracker (a local Markdown tracker, or a stub `gh`
that answers like GitHub's REST API), runs plugins/dev-skills/skills/team-lead/snapshot.py as a command and reads
its printed rows. See evals/team-lead/README.md.
"""
import os
import pathlib
import subprocess
import tempfile
import textwrap
import unittest

SNAPSHOT = pathlib.Path(__file__).resolve().parents[2] / "plugins/dev-skills/skills/team-lead/snapshot.py"
NOW = "2026-11-03T15:00:00Z"

MARKDOWN_TRACKER_DOC = """\
# Issue tracker: local Markdown

Issues are files under `.scratch/issues/`, one per issue, named `NN-slug.md`.
Pull requests are files under `.scratch/pulls/`, one per pull request, named `<n>.md`.

- **Read an issue**: read its file.
- **Read a PR**: read its file.
"""

GITHUB_TRACKER_DOC = """\
# Issue tracker: GitHub

Use the `gh` CLI for all operations.

- **Read an issue**: `gh issue view <number> --json number,title,body,labels,comments`.
"""

OTHER_TRACKER_DOC = """\
# Issue tracker: Linear

Issues live in the team's Linear workspace. Use the Linear tools the session has.

- **Read an issue**: open it in Linear.
"""


def run(cmd, cwd, env=None, check=True):
    return subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True, check=check)


class Fixture:
    """A disposable repo: git history plus a tracker doc and tracker files."""

    def __init__(self, root, tracker_doc=MARKDOWN_TRACKER_DOC):
        self.repo = pathlib.Path(root) / "repo"
        (self.repo / "docs/dev-skills").mkdir(parents=True)
        (self.repo / ".scratch/issues").mkdir(parents=True)
        (self.repo / ".scratch/pulls").mkdir(parents=True)
        (self.repo / "docs/dev-skills/issue-tracker.md").write_text(tracker_doc)
        run(["git", "init", "-q", "-b", "main"], self.repo)
        self.commit("main", "2026-11-03T09:00:00Z", "start")

    def commit(self, branch, when, subject):
        env = dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when, GIT_AUTHOR_NAME="w",
                   GIT_AUTHOR_EMAIL="w@example.com", GIT_COMMITTER_NAME="w", GIT_COMMITTER_EMAIL="w@example.com")
        heads = run(["git", "branch", "--list", branch], self.repo).stdout.strip()
        if branch != "main":
            run(["git", "checkout", "-q"] + ([] if heads else ["-b"]) + [branch], self.repo)
        (self.repo / "work.txt").write_text(subject + "\n")
        run(["git", "add", "-A"], self.repo, env)
        run(["git", "commit", "-q", "-m", subject], self.repo, env)
        run(["git", "checkout", "-q", "main"], self.repo)

    def issue(self, name, comments=()):
        lines = ["Title: " + name, "Status: open", "", "Body.", "", "## Comments", ""]
        for when, author, text in comments:
            lines += [f"### {when} {author}", "", text, ""]
        (self.repo / ".scratch/issues" / name).write_text("\n".join(lines))

    def pull(self, n, builds, state, opened, ready="", merged="", closed="", comments=(), branch=""):
        lines = [f"Builds: {builds}"] + ([f"Branch: {branch}"] if branch else []) + [f"State: {state}", f"Opened: {opened}"]
        lines += [f"Ready: {ready}"] if ready else []
        lines += [f"Merged: {merged}"] if merged else []
        lines += [f"Closed: {closed}"] if closed else []
        lines += ["", "## Comments", ""]
        for when, author, text in comments:
            lines += [f"### {when} {author}", "", text, ""]
        (self.repo / ".scratch/pulls" / f"{n}.md").write_text("\n".join(lines))

    def snapshot(self, *workers, now=NOW, env=None, extra=()):
        cmd = ["python3", str(SNAPSHOT), "--repo", str(self.repo), "--now", now, "--silent-after", "60"]
        for w in workers:
            cmd += ["--worker", w]
        return run(cmd + list(extra), self.repo, env=env, check=False)


def rows(output):
    """The printed table as {worker: {column: cell}}."""
    table = [l for l in output.splitlines() if l.startswith("|")]
    if not table:
        return {}
    head = [c.strip() for c in table[0].strip("|").split("|")]
    out = {}
    for line in table[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        out[cells[0]] = dict(zip(head, cells))
    return out


class MarkdownTracker(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.f = Fixture(self.tmp.name)

    def test_recent_commit_is_active(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        row = rows(out.stdout)["w25"]
        self.assertIn("2026-11-03T14:40:00Z", row["Last commit"])
        self.assertIn("readme: hello", row["Last commit"])
        self.assertEqual(row["Verdict"], "active")

    def test_no_activity_within_the_interval_is_silent_since_the_last_activity(self):
        self.f.commit("t25", "2026-11-03T13:30:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [("2026-11-03T13:35:00Z", "worker", "Pushed the first draft.")])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T13:10:00Z").stdout)["w25"]
        self.assertEqual(row["Verdict"], "silent since 2026-11-03T13:35:00Z")
        self.assertIn("2026-11-03T13:35:00Z worker", row["Last comment"])

    def test_the_team_leads_own_records_are_not_activity(self):
        self.f.commit("t25", "2026-11-03T13:30:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [("2026-11-03T14:30:00Z", "coordinator", "<!-- team-lead start -->\nStarted w25.")])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T13:10:00Z").stdout)["w25"]
        self.assertEqual(row["Verdict"], "silent since 2026-11-03T13:30:00Z")

    def test_nothing_pushed_counts_from_the_start(self):
        self.f.issue("25-hello-doc.md")
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T13:10:00Z").stdout)["w25"]
        self.assertEqual(row["Last commit"], "none pushed")
        self.assertEqual(row["Verdict"], "silent since 2026-11-03T13:10:00Z")

    def test_a_nudge_with_nothing_after_it_for_an_interval_is_still_silent(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [("2026-11-03T14:00:00Z", "coordinator", "<!-- team-lead nudge -->\nNudged w25.")])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T12:10:00Z").stdout)["w25"]
        self.assertEqual(row["Verdict"], "still silent after its nudge at 2026-11-03T14:00:00Z")

    def test_a_nudge_written_minutes_after_the_last_check_in_counts_a_whole_interval(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [("2026-11-03T14:03:00Z", "coordinator", "<!-- team-lead nudge -->\nNudged w25.")])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T12:10:00Z").stdout)["w25"]
        self.assertEqual(row["Verdict"], "still silent after its nudge at 2026-11-03T14:03:00Z")

    def test_a_replacement_started_after_its_predecessors_merged_pull_request_is_active(self):
        self.f.commit("t25", "2026-11-03T13:00:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "merged", "2026-11-03T13:01:00Z", ready="2026-11-03T13:05:00Z",
                    merged="2026-11-03T14:20:00Z", branch="t25")
        row = rows(self.f.snapshot("id=w25b;issue=25;branch=t25;started=2026-11-03T14:30:00Z").stdout)["w25b"]
        self.assertEqual(row["Verdict"], "active")

    def test_a_nudge_younger_than_the_interval_is_waited_on(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [("2026-11-03T14:30:00Z", "coordinator", "<!-- team-lead nudge -->\nNudged w25.")])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T12:10:00Z").stdout)["w25"]
        self.assertEqual(row["Verdict"], "nudged at 2026-11-03T14:30:00Z, waiting")

    def test_an_answer_after_the_nudge_makes_it_active_again(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [
            ("2026-11-03T14:00:00Z", "coordinator", "<!-- team-lead nudge -->\nNudged w25."),
            ("2026-11-03T14:20:00Z", "worker", "Waiting on CI; pushing soon."),
        ])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T12:10:00Z").stdout)["w25"]
        self.assertEqual(row["Verdict"], "active")

    def test_a_heading_inside_a_comment_body_is_not_a_comment(self):
        self.f.commit("t25", "2026-11-03T13:30:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [("2026-11-03T14:30:00Z", "worker", "Round 1 done.\n\n### Round 2 summary\n\nAll clean.")])
        out = self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T13:10:00Z")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        row = rows(out.stdout)["w25"]
        self.assertEqual(row["Verdict"], "active")
        self.assertIn("2026-11-03T14:30:00Z worker", row["Last comment"])

    def test_a_resume_restarts_the_silence_clock_and_voids_an_earlier_nudge(self):
        self.f.commit("t25", "2026-11-03T11:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [("2026-11-03T12:00:00Z", "coordinator", "<!-- team-lead nudge -->\nNudged w25.")])
        spec = "id=w25;issue=25;branch=t25;started=2026-11-03T11:10:00Z;resumed=2026-11-03T14:30:00Z"
        self.assertEqual(rows(self.f.snapshot(spec).stdout)["w25"]["Verdict"], "active")
        later = self.f.snapshot(spec, now="2026-11-03T15:40:00Z")
        self.assertEqual(rows(later.stdout)["w25"]["Verdict"], "silent since 2026-11-03T14:30:00Z")

    def test_an_earlier_milestone_nudge_record_counts_and_is_not_activity(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [("2026-11-03T14:00:00Z", "coordinator", "<!-- milestone nudge -->\nNudged w25.")])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T12:10:00Z").stdout)["w25"]
        self.assertEqual(row["Verdict"], "still silent after its nudge at 2026-11-03T14:00:00Z")

    def test_an_earlier_milestone_record_is_not_activity(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md", [("2026-11-03T14:30:00Z", "coordinator", "<!-- milestone stand-up -->\nCheck-in.")])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T12:10:00Z").stdout)["w25"]
        self.assertEqual(row["Verdict"], "silent since 2026-11-03T12:40:00Z")

    def test_a_ready_pull_request_not_reported_is_flagged(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "open", "2026-11-03T14:41:00Z", ready="2026-11-03T14:50:00Z")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T14:10:00Z;reported=2026-11-03T14:20:00Z")
        row = rows(out.stdout)["w25"]
        self.assertEqual(row["Pull request"], "#11 ready since 2026-11-03T14:50:00Z")
        self.assertEqual(row["Verdict"], "pull request ready but not reported")

    def test_a_ready_spec_pull_request_still_in_review_is_active(self):
        # A Spec thread marks its pull request ready before the review (ADR 0005); its Round comment is the worker at work.
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "open", "2026-11-03T14:41:00Z", ready="2026-11-03T14:50:00Z",
                    comments=[("2026-11-03T14:55:00Z", "worker", "Round 1: no open Findings.")])
        out = self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T14:10:00Z;reported=2026-11-03T14:20:00Z")
        row = rows(out.stdout)["w25"]
        self.assertEqual(row["Pull request"], "#11 ready since 2026-11-03T14:50:00Z")
        self.assertEqual(row["Verdict"], "active")

    def test_an_open_pull_request_file_with_no_dates_does_not_crash_the_snapshot(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        (self.f.repo / ".scratch/pulls/11.md").write_text("Builds: 25-hello-doc.md\nBranch: t25\nState: open\n\n## Comments\n")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(rows(out.stdout)["w25"]["Verdict"], "active")

    def test_a_ready_pull_request_with_a_fix_pushed_after_ready_is_active(self):
        self.f.commit("t25", "2026-11-03T14:55:00Z", "fix: Round 1 finding")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "open", "2026-11-03T14:41:00Z", ready="2026-11-03T14:50:00Z")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T14:10:00Z;reported=2026-11-03T14:20:00Z")
        self.assertEqual(rows(out.stdout)["w25"]["Verdict"], "active")

    def test_a_ready_pull_request_gone_quiet_after_its_review_is_then_tested_for_silence(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "open", "2026-11-03T14:41:00Z", ready="2026-11-03T14:50:00Z",
                    comments=[("2026-11-03T14:55:00Z", "worker", "Round 1: no open Findings.")])
        out = self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T14:10:00Z", now="2026-11-03T16:00:00Z")
        self.assertEqual(rows(out.stdout)["w25"]["Verdict"], "silent since 2026-11-03T14:55:00Z")

    def test_a_merged_pull_request_is_flagged_even_with_comments_after_ready(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "merged", "2026-11-03T12:41:00Z", ready="2026-11-03T12:45:00Z",
                    merged="2026-11-03T13:05:00Z", comments=[("2026-11-03T12:55:00Z", "worker", "Round 1: clean.")])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T12:10:00Z").stdout)["w25"]
        self.assertEqual(row["Verdict"], "pull request ready but not reported")

    def test_a_ready_pull_request_already_reported_is_active(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "open", "2026-11-03T14:41:00Z", ready="2026-11-03T14:50:00Z")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T14:10:00Z;reported=2026-11-03T14:51:00Z")
        self.assertEqual(rows(out.stdout)["w25"]["Verdict"], "active")

    def test_a_lost_report_is_found_by_the_branch_when_no_pr_is_given(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(9, "25-hello-doc.md", "closed", "2026-11-03T13:00:00Z", closed="2026-11-03T13:10:00Z", branch="t25-old")
        self.f.pull(11, "25-hello-doc.md", "open", "2026-11-03T14:41:00Z", ready="2026-11-03T14:50:00Z", branch="t25")
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z").stdout)["w25"]
        self.assertEqual(row["Pull request"], "#11 ready since 2026-11-03T14:50:00Z")
        self.assertEqual(row["Verdict"], "pull request ready but not reported")

    def test_no_pull_request_on_the_branch_reads_none(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(9, "20-quiet.md", "open", "2026-11-03T13:00:00Z", ready="2026-11-03T13:10:00Z", branch="t20")
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z").stdout)["w25"]
        self.assertEqual(row["Pull request"], "none")
        self.assertEqual(row["Verdict"], "active")

    def test_a_ready_pull_request_acted_on_is_then_tested_for_silence(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "open", "2026-11-03T14:41:00Z", ready="2026-11-03T14:50:00Z", branch="t25")
        first = rows(self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T14:10:00Z").stdout)["w25"]
        self.assertEqual(first["Verdict"], "pull request ready but not reported")
        # The team lead acted on it at the 15:00 check-in; the worker then died with nothing more.
        later = self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T14:10:00Z;reported=2026-11-03T15:00:00Z",
                                now="2026-11-03T16:00:00Z")
        self.assertEqual(rows(later.stdout)["w25"]["Verdict"], "silent since 2026-11-03T15:00:00Z")

    def test_a_merged_pull_request_not_reported_is_flagged(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "merged", "2026-11-03T12:41:00Z", ready="2026-11-03T12:45:00Z",
                    merged="2026-11-03T13:05:00Z")
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T12:10:00Z").stdout)["w25"]
        self.assertEqual(row["Pull request"], "#11 merged 2026-11-03T13:05:00Z")
        self.assertEqual(row["Verdict"], "pull request ready but not reported")

    def test_a_draft_pull_request_comment_is_activity(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        self.f.pull(11, "25-hello-doc.md", "draft", "2026-11-03T12:41:00Z",
                    comments=[("2026-11-03T14:30:00Z", "worker", "Round 1 fixes pushed soon.")])
        row = rows(self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T12:10:00Z").stdout)["w25"]
        self.assertEqual(row["Pull request"], "#11 draft")
        self.assertEqual(row["Verdict"], "active")

    def test_the_harness_state_is_printed_as_given(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.f.issue("25-hello-doc.md")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z;state=idle since 14:41Z")
        self.assertEqual(rows(out.stdout)["w25"]["Harness state"], "idle since 14:41Z")

    def test_one_row_per_worker(self):
        self.f.commit("t10", "2026-11-03T14:50:00Z", "farewell: bye")
        self.f.commit("t25", "2026-11-03T12:00:00Z", "readme: hello")
        self.f.issue("10-farewell.md")
        self.f.issue("25-hello-doc.md")
        out = self.f.snapshot("id=w10;issue=10;branch=t10;started=2026-11-03T10:05:00Z",
                              "id=w25;issue=25;branch=t25;started=2026-11-03T11:00:00Z")
        r = rows(out.stdout)
        self.assertEqual(sorted(r), ["w10", "w25"])
        self.assertEqual(r["w10"]["Verdict"], "active")
        self.assertEqual(r["w25"]["Verdict"], "silent since 2026-11-03T12:00:00Z")

    def test_a_missing_issue_file_is_read_by_hand(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z")
        self.assertEqual(out.returncode, 3, out.stdout + out.stderr)
        row = rows(out.stdout)["w25"]
        self.assertEqual(row["Verdict"], "read by hand")
        self.assertIn("2026-11-03T14:40:00Z", row["Last commit"])

    def test_a_bad_worker_spec_is_a_usage_error(self):
        out = self.f.snapshot("issue=25;branch=t25")
        self.assertEqual(out.returncode, 2)
        self.assertIn("id=", out.stderr)


class GithubTracker(unittest.TestCase):
    """A stub `gh` on PATH answers the REST calls the command makes, from files named after their routes."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.f = Fixture(self.tmp.name, GITHUB_TRACKER_DOC)
        self.bin = pathlib.Path(self.tmp.name) / "bin"
        self.answers = pathlib.Path(self.tmp.name) / "answers"
        self.bin.mkdir()
        self.answers.mkdir()
        gh = self.bin / "gh"
        gh.write_text(textwrap.dedent(f"""\
            #!/usr/bin/env bash
            # Stub gh: `gh api <route> ...` prints answers/<route with / as _>, or fails like an unreachable API.
            [ "$1" = api ] || {{ echo "stub gh: only api" >&2; exit 1; }}
            f="{self.answers}/$(printf '%s' "$2" | tr '/' '_')"
            [ -f "$f" ] || {{ echo "HTTP 404: Not Found ($2)" >&2; exit 1; }}
            cat "$f"
            """))
        gh.chmod(0o755)
        self.env = dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}")

    def answer(self, route, text):
        (self.answers / route.replace("/", "_")).write_text(text)

    def test_comments_and_a_ready_pull_request_from_the_rest_api(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.answer("repos/{owner}/{repo}/issues/25/comments",
                    "2026-11-03T14:45:00Z\tworker\tOpened the pull request.\n"
                    "2026-11-03T14:46:00Z\tcoordinator\t<!-- team-lead start -->\n")
        self.answer("repos/{owner}/{repo}/pulls/11", "open\tfalse\t2026-11-03T14:41:00Z\t\t\n")
        self.answer("repos/{owner}/{repo}/issues/11/events", "2026-11-03T14:50:00Z\n")
        self.answer("repos/{owner}/{repo}/issues/11/comments", "")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T14:10:00Z;reported=2026-11-03T14:20:00Z",
                              env=self.env)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        row = rows(out.stdout)["w25"]
        self.assertIn("2026-11-03T14:45:00Z worker", row["Last comment"])
        self.assertEqual(row["Pull request"], "#11 ready since 2026-11-03T14:50:00Z")
        self.assertEqual(row["Verdict"], "pull request ready but not reported")

    def test_a_merged_pull_request_from_the_rest_api(self):
        self.f.commit("t25", "2026-11-03T12:40:00Z", "readme: hello")
        self.answer("repos/{owner}/{repo}/issues/25/comments", "")
        self.answer("repos/{owner}/{repo}/pulls/11",
                    "closed\tfalse\t2026-11-03T12:41:00Z\t2026-11-03T13:05:00Z\t2026-11-03T13:05:00Z\n")
        self.answer("repos/{owner}/{repo}/issues/11/events", "")
        self.answer("repos/{owner}/{repo}/issues/11/comments", "")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;pr=11;started=2026-11-03T12:10:00Z;reported=2026-11-03T14:30:00Z",
                              env=self.env)
        row = rows(out.stdout)["w25"]
        self.assertEqual(row["Pull request"], "#11 merged 2026-11-03T13:05:00Z")
        self.assertEqual(row["Verdict"], "active")

    def test_a_lost_report_is_found_by_the_branch_through_the_rest_api(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        self.answer("repos/{owner}/{repo}/issues/25/comments", "")
        self.answer("repos/{owner}/{repo}/pulls?head={owner}:t25&state=all", "11\n")
        self.answer("repos/{owner}/{repo}/pulls/11", "open\tfalse\t2026-11-03T14:41:00Z\t\t\n")
        self.answer("repos/{owner}/{repo}/issues/11/events", "2026-11-03T14:50:00Z\n")
        self.answer("repos/{owner}/{repo}/issues/11/comments", "")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z", env=self.env)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        row = rows(out.stdout)["w25"]
        self.assertEqual(row["Pull request"], "#11 ready since 2026-11-03T14:50:00Z")
        self.assertEqual(row["Verdict"], "pull request ready but not reported")

    def test_an_unreachable_api_falls_back_to_reading_by_hand(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z", env=self.env)
        self.assertEqual(out.returncode, 3, out.stdout + out.stderr)
        row = rows(out.stdout)["w25"]
        self.assertEqual(row["Verdict"], "read by hand")
        self.assertIn("2026-11-03T14:40:00Z", row["Last commit"])
        self.assertIn("read by hand", out.stdout.splitlines()[0] + out.stdout)

    def test_no_gh_on_path_falls_back_to_reading_by_hand(self):
        self.f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
        env = dict(os.environ, PATH="/usr/bin:/bin")
        if pathlib.Path("/usr/bin/gh").exists() or pathlib.Path("/bin/gh").exists():
            self.skipTest("a real gh is on the system path")
        out = self.f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z", env=env)
        self.assertEqual(out.returncode, 3, out.stdout + out.stderr)
        self.assertEqual(rows(out.stdout)["w25"]["Verdict"], "read by hand")


class UnknownTracker(unittest.TestCase):
    def test_a_tracker_the_command_cannot_read_falls_back_to_reading_by_hand(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(tmp, OTHER_TRACKER_DOC)
            f.commit("t25", "2026-11-03T14:40:00Z", "readme: hello")
            out = f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z")
            self.assertEqual(out.returncode, 3, out.stdout + out.stderr)
            row = rows(out.stdout)["w25"]
            self.assertEqual(row["Verdict"], "read by hand")
            self.assertEqual(row["Last comment"], "read by hand")
            self.assertIn("2026-11-03T14:40:00Z", row["Last commit"])
            self.assertIn("tracker: not readable by this command", out.stdout)

    def test_no_tracker_doc_falls_back_to_reading_by_hand(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Fixture(tmp)
            (f.repo / "docs/dev-skills/issue-tracker.md").unlink()
            out = f.snapshot("id=w25;issue=25;branch=t25;started=2026-11-03T14:10:00Z")
            self.assertEqual(out.returncode, 3, out.stdout + out.stderr)
            self.assertEqual(rows(out.stdout)["w25"]["Verdict"], "read by hand")


if __name__ == "__main__":
    unittest.main()
