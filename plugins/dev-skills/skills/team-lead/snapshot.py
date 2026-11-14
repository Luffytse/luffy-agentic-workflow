#!/usr/bin/env python3
"""Print one row per running worker for a team lead's check-in: last commit, last comment, pull request, verdict.

Usage:
  snapshot.py --worker 'id=<worker>;issue=<n>;branch=<branch>[;pr=<n>][;started=<UTC>][;reported=<UTC>][;resumed=<UTC>][;waiting=<UTC>][;state=<text>]' ...
              [--repo <dir>] [--tracker-doc <file>] [--now <UTC>] [--silent-after <minutes>] [--no-fetch]

A worker's fields: its id, the issue it works on, the branch it pushes, its pull request if any (left out, it is looked
up by the branch: GitHub's pulls?head= route, or a pull request file's Branch: line), when it started,
when it last reported to the team lead, when the team lead last resumed it after a pause (activity, so a nudge
before it is void and the worker gets a full window), when the team lead recorded it as waiting on the user's action (its
`wait` record), and its state as the harness reports it (printed as given). Times are UTC,
as 2026-11-03T14:40:00Z.

The tracker is read the way the tracker doc (default <repo>/docs/dev-skills/issue-tracker.md) says it is kept:
  - GitHub, when the doc uses `gh`: issue and pull request comments, the pull request and its ready event, through
    the `gh api` REST routes (they work where GraphQL does not);
  - a tracker kept as files, when the doc says "Issues are files under `<dir>`" (and "Pull requests are files
    under `<dir>`"): comments under "## Comments" as "### <UTC time> <author>" headings; a pull request file's
    State:, Opened:, Ready:, Merged: and Closed: lines.
Any other tracker, or a read that fails, prints "read by hand" in that row's tracker cells and verdict, and the
command exits 3: read those rows with the tracker doc's own operations. Git is read either way.

Verdicts: "pull request ready but not reported" (ready or merged after the later of the worker's last report and
its start, so a replacement is not flagged for its predecessor's pull request; a ready pull request still open
counts only while the worker has made no comment or push (or been resumed) since marking it ready, because a Spec thread marks its pull request
ready before its review and the review's comments and pushes are the worker at work); "active" (activity within the
silent-after window); "waiting on the user since <T>" (a wait given, with no push, comment or pull request change after
it: such a worker is neither silent nor due a nudge until it comments or pushes again); "nudged at <T>, waiting"; "still silent after its nudge at <T>" (a window, less a 10-minute grace
for a nudge recorded minutes after its check-in, has passed since the nudge with no activity); "silent since <T>". Activity is a pushed commit, a comment
on the issue or the pull request, a pull request change, the worker's start, its last report or its resume. Comments
whose first line starts "<!-- team-lead" or, from the earlier milestone loop, "<!-- milestone " are the team lead's own
records, never activity; "<!-- team-lead nudge -->" and "<!-- milestone nudge -->" are nudges. In a tracker kept as files
only a "### <UTC time> <author>" heading starts a comment; other ### headings belong to the comment above them.

Exit 0 when every row was read, 3 when a row must be read by hand, 2 on a usage error. Writes nothing.
"""
import argparse
import datetime as dt
import pathlib
import re
import shutil
import subprocess
import sys

OWN = ("<!-- team-lead", "<!-- milestone ")
NUDGE = ("<!-- team-lead nudge -->", "<!-- milestone nudge -->")
# A nudge record is written minutes after the check-in that found the worker silent; the next check-in, one interval
# after that one, still counts as a whole interval since the nudge.
GRACE = dt.timedelta(minutes=10)


class Unreadable(Exception):
    pass


def parse_time(text):
    text = text.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    t = dt.datetime.fromisoformat(text)
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.timezone.utc)
    return t.astimezone(dt.timezone.utc)


def show(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ") if t else ""


def parse_worker(spec):
    fields = {}
    for part in spec.split(";"):
        if not part.strip():
            continue
        if "=" not in part:
            raise ValueError(f"worker field without '=': {part!r}")
        k, v = part.split("=", 1)
        fields[k.strip()] = v.strip()
    for need in ("id", "issue", "branch"):
        if not fields.get(need):
            raise ValueError(f"worker needs id=, issue= and branch= (missing {need}=): {spec!r}")
    for k in ("started", "reported", "resumed", "waiting"):
        fields[k] = parse_time(fields[k]) if fields.get(k) else None
    return fields


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)


def last_commit(repo, branch):
    for ref in (f"origin/{branch}", branch):
        r = git(repo, "log", "-1", "--format=%cI%x09%s", ref, "--")
        if r.returncode == 0 and r.stdout.strip():
            when, _, subject = r.stdout.strip().partition("\t")
            return parse_time(when), subject
    return None, None


# --- trackers -----------------------------------------------------------------------------------------------


class MarkdownTracker:
    name = "files"

    def __init__(self, repo, issues, pulls):
        self.issues = repo / issues
        self.pulls = repo / pulls if pulls else None

    @staticmethod
    def comments(text):
        out = []
        _, _, rest = text.partition("\n## Comments")
        for m in re.finditer(r"^### (\d{4}-\d\d-\d\dT\S+) (\S+)[^\n]*\n(.*?)(?=^### \d{4}-\d\d-\d\dT\S+ |\Z)", rest, re.S | re.M):
            body = m.group(3).strip()
            out.append((parse_time(m.group(1)), m.group(2), body.splitlines()[0] if body else ""))
        return out

    def issue_comments(self, issue):
        if not self.issues.is_dir():
            raise Unreadable(f"no folder {self.issues}")
        files = [p for p in self.issues.iterdir() if p.name in (issue, f"{issue}.md") or p.name.startswith(f"{issue}-")]
        if len(files) != 1:
            raise Unreadable(f"issue {issue}: {len(files)} files")
        return self.comments(files[0].read_text())

    def find_pr(self, branch):
        """The newest pull request whose Branch: line names this branch, closed-unmerged ones last; or None."""
        if not self.pulls or not self.pulls.is_dir():
            return None
        found = []
        for p in self.pulls.glob("*.md"):
            text = p.read_text()
            if re.search(rf"^Branch:[ \t]*{re.escape(branch)}[ \t]*$", text, re.M) and p.stem.isdigit():
                closed = bool(re.search(r"^State:[ \t]*closed", text, re.M | re.I))
                found.append((not closed, int(p.stem)))
        return str(max(found)[1]) if found else None

    def pull(self, n):
        if not self.pulls:
            raise Unreadable("the tracker doc names no pull request folder")
        p = self.pulls / f"{n}.md"
        if not p.is_file():
            raise Unreadable(f"no pull request file {p.name}")
        text = p.read_text()
        head = dict(re.findall(r"^(State|Opened|Ready|Merged|Closed):[ \t]*(.*)$", text, re.M))
        state = head.get("State", "").strip().lower()
        if state not in ("draft", "open", "merged", "closed"):
            raise Unreadable(f"pull request {n}: State: {state!r}")
        return {"state": state, "opened": parse_time(head.get("Opened", "")), "ready": parse_time(head.get("Ready", "")),
                "merged": parse_time(head.get("Merged", "")), "closed": parse_time(head.get("Closed", "")),
                "comments": self.comments(text)}


class GithubTracker:
    name = "GitHub (gh REST)"

    def __init__(self, repo):
        self.repo = repo
        if not shutil.which("gh"):
            raise Unreadable("no gh on PATH")

    def api(self, route, jq, paginate=False):
        cmd = ["gh", "api", route] + (["--paginate"] if paginate else []) + ["--jq", jq]
        r = subprocess.run(cmd, cwd=self.repo, text=True, capture_output=True)
        if r.returncode != 0:
            raise Unreadable(f"gh api {route}: {(r.stderr or r.stdout).strip()[:120]}")
        return r.stdout

    def comment_list(self, n):
        out = self.api(f"repos/{{owner}}/{{repo}}/issues/{n}/comments",
                       '.[] | [.created_at, .user.login, (.body | split("\\n")[0])] | @tsv', paginate=True)
        rows = []
        for line in out.splitlines():
            if line.strip():
                when, author, first = (line.split("\t") + ["", ""])[:3]
                rows.append((parse_time(when), author, first))
        return rows

    def issue_comments(self, issue):
        if not str(issue).isdigit():
            raise Unreadable(f"issue {issue!r} is not a GitHub issue number")
        return self.comment_list(issue)

    def find_pr(self, branch):
        """The newest pull request whose head is this branch, or None."""
        out = self.api(f"repos/{{owner}}/{{repo}}/pulls?head={{owner}}:{branch}&state=all", ".[] | .number")
        numbers = [l.strip() for l in out.splitlines() if l.strip()]
        return numbers[0] if numbers else None

    def pull(self, n):
        line = self.api(f"repos/{{owner}}/{{repo}}/pulls/{n}",
                        '[.state, .draft, .created_at, (.merged_at // ""), (.closed_at // "")] | @tsv').strip()
        state, draft, created, merged, closed = (line.split("\t") + [""] * 5)[:5]
        ready = [l for l in self.api(f"repos/{{owner}}/{{repo}}/issues/{n}/events",
                                     '.[] | select(.event == "ready_for_review") | .created_at', paginate=True).splitlines()
                 if l.strip()]
        if merged:
            state = "merged"
        elif state == "open" and draft == "true":
            state = "draft"
        elif state not in ("open", "closed"):
            raise Unreadable(f"pull request {n}: state {state!r}")
        return {"state": state, "opened": parse_time(created), "ready": parse_time(ready[-1]) if ready else None,
                "merged": parse_time(merged), "closed": parse_time(closed), "comments": self.comment_list(n)}


def open_tracker(repo, doc):
    """The tracker the doc describes, or (None, why)."""
    if not doc.is_file():
        return None, f"no tracker doc at {doc}"
    text = doc.read_text()
    m = re.search(r"Issues are files under `([^`]+)`", text)
    if m:
        p = re.search(r"Pull requests are files under `([^`]+)`", text)
        return MarkdownTracker(repo, m.group(1), p.group(1) if p else None), ""
    if re.search(r"\bgh (issue|api|pr)\b|`gh` CLI", text):
        try:
            return GithubTracker(repo), ""
        except Unreadable as e:
            return None, str(e)
    return None, "a tracker this command does not know"


# --- verdict ------------------------------------------------------------------------------------------------


def row_for(w, repo, tracker, now, window):
    cell = {"Worker": w["id"], "Issue": w["issue"], "Harness state": w.get("state") or "not given"}
    when, subject = last_commit(repo, w["branch"])
    cell["Last commit"] = f"{show(when)} {subject}" if when else "none pushed"
    # The worker's own moves (pushes, comments, pull request changes); activity adds its start, report and resume.
    moves = [when] if when else []
    ready_at = None
    try:
        if tracker is None:
            raise Unreadable("tracker")
        comments = tracker.issue_comments(w["issue"])
        if not w.get("pr"):
            w = dict(w, pr=tracker.find_pr(w["branch"]))
        pr = tracker.pull(w["pr"]) if w.get("pr") else None
    except (Unreadable, ValueError):
        cell.update({"Last comment": "read by hand", "Pull request": "read by hand" if w.get("pr") else "none",
                     "Verdict": "read by hand"})
        return cell, False
    if pr:
        comments = comments + pr["comments"]
        moves += [t for t in (pr["opened"], pr["ready"], pr["merged"], pr["closed"]) if t]
        if pr["state"] == "merged":
            ready_at = pr["merged"] or pr["ready"] or pr["opened"]
            cell["Pull request"] = f"#{w['pr']} merged {show(ready_at)}"
        elif pr["state"] == "open":
            ready_at = pr["ready"] or pr["opened"]
            cell["Pull request"] = f"#{w['pr']} ready since {show(ready_at)}"
        elif pr["state"] == "draft":
            cell["Pull request"] = f"#{w['pr']} draft"
        else:
            cell["Pull request"] = f"#{w['pr']} closed {show(pr['closed'])}"
    else:
        cell["Pull request"] = "none"
    theirs = [c for c in comments if c[0] and not c[2].startswith(OWN)]
    nudges = [c[0] for c in comments if c[0] and c[2].startswith(NUDGE)]
    moves += [c[0] for c in theirs]
    activity = moves + [t for t in (w["started"], w["reported"], w["resumed"]) if t]
    latest = max(theirs, key=lambda c: c[0]) if theirs else None
    cell["Last comment"] = f"{show(latest[0])} {latest[1]}: {latest[2][:60]}" if latest else "none"
    last = max(activity) if activity else None
    nudge = max(nudges) if nudges else None
    seen = max([t for t in (w["reported"], w["started"]) if t], default=None)
    # An open pull request is finished only if the worker did nothing after marking it ready: a Spec thread marks its
    # pull request ready before its review, and the review's comments and fixes are the worker at work.
    working = ready_at and pr["state"] == "open" and any(t > ready_at for t in activity)
    if ready_at and (seen is None or seen < ready_at) and not working:
        verdict = "pull request ready but not reported"
    elif w["waiting"] and not any(t > w["waiting"] for t in moves):
        verdict = f"waiting on the user since {show(w['waiting'])}"
    elif last and now - last < window:
        verdict = "active"
    elif nudge and (last is None or nudge > last):
        verdict = (f"still silent after its nudge at {show(nudge)}" if now - nudge >= window - GRACE
                   else f"nudged at {show(nudge)}, waiting")
    else:
        verdict = f"silent since {show(last)}" if last else "silent since its start (start time not given)"
    cell["Verdict"] = verdict
    return cell, True


COLUMNS = ["Worker", "Issue", "Harness state", "Last commit", "Last comment", "Pull request", "Verdict"]


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--worker", action="append", default=[], required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--tracker-doc")
    ap.add_argument("--now")
    ap.add_argument("--silent-after", type=int, default=60, help="minutes; the check-in interval")
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args(argv)
    try:
        workers = [parse_worker(s) for s in a.worker]
        now = parse_time(a.now) if a.now else dt.datetime.now(dt.timezone.utc)
    except ValueError as e:
        print(f"snapshot: {e}", file=sys.stderr)
        return 2
    repo = pathlib.Path(a.repo).resolve()
    notes = []
    if not a.no_fetch and git(repo, "remote", "get-url", "origin").returncode == 0:
        try:
            if subprocess.run(["git", "-C", str(repo), "fetch", "--quiet", "origin"], capture_output=True,
                              timeout=120).returncode != 0:
                notes.append("git fetch failed: branches read as last fetched")
        except subprocess.TimeoutExpired:
            notes.append("git fetch timed out: branches read as last fetched")
    tracker, why = open_tracker(repo, pathlib.Path(a.tracker_doc) if a.tracker_doc else repo / "docs/dev-skills/issue-tracker.md")
    tname = tracker.name if tracker else f"not readable by this command ({why}): read by hand"
    window = dt.timedelta(minutes=a.silent_after)
    print(f"Snapshot at {show(now)} · silent after {a.silent_after} min · tracker: {tname}"
          + "".join(f" · {n}" for n in notes))
    print()
    print("| " + " | ".join(COLUMNS) + " |")
    print("|" + "---|" * len(COLUMNS))
    all_read = True
    for w in workers:
        cell, ok = row_for(w, repo, tracker, now, window)
        all_read = all_read and ok
        print("| " + " | ".join(cell[c].replace("|", "/") for c in COLUMNS) + " |")
    if not all_read:
        print()
        print("Rows marked read by hand: read the issue, its comments and the pull request with the tracker doc's "
              "operations, and decide from the same columns.")
    return 0 if all_read else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
