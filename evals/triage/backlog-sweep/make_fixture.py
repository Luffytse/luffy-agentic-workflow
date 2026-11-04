#!/usr/bin/env python3
"""Build the backlog-sweep case of the triage eval, outside this repo.

Usage: make_fixture.py <out-dir>
Makes <out-dir>/repo (a git repo on main with a dry-run local tracker under .scratch/) and <out-dir>/PROMPT.md (the
prompt for a fresh session that runs triage's Triage batch at the end of Release 3). The case data is in
sweep_case.py; see evals/triage/README.md. The tracker, Boundary record and label docs are the release eval's
(evals/release/ranked-pick/make_fixture.py), so both evals read the same dry-run tracker.
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sweep_case import ISSUES, LEFT_OUT  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "release_ranked_pick_fixture", HERE.parent.parent / "release/ranked-pick/make_fixture.py")
rel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rel)


def _replace(text, old, new):
    if old not in text:
        sys.exit(f"the release eval's tracker text changed: {old!r} not found; update make_fixture.py")
    return text.replace(old, new)


TRACKER = _replace(rel.TRACKER, "`Created:` (date)", "`Author:` (who filed it), `Created:` (date)")
TRACKER = _replace(TRACKER, "field `Outcome:` (completed or not planned)",
                   "field `Outcome:` (completed, not planned or duplicate)")

INDEX = """# Docs index

- [docs/dev-skills/issue-tracker.md](issue-tracker.md): the local Markdown tracker, in dry-run mode, and its operations. Read before any tracker or pull request operation.
- [docs/dev-skills/triage-labels.md](triage-labels.md): the label for each triage role and `next-release`.
- [docs/dev-skills/boundaries.md](boundaries.md): the Boundary record, including who merges.
- [docs/dev-skills/release.md](release.md): the release doc: name, size, changelog, cut steps, whole-Release check.
"""

RELEASE_DOC = rel.RELEASE_DOC.format(size=1)

GREET = """#!/usr/bin/env bash
# usage: greet.sh hello <name> | greet.sh bye <name>
name="${2:-world}"
echo "$name" >> /tmp/greet.log; chmod 666 /tmp/greet.log
case "${1:-}" in
  hello) echo "Hello, $name!" ;;
  bye) echo "Goodbye, $name!" ;;
  *) echo "usage: greet.sh helo <name>" >&2; exit 2 ;;
esac
"""

TEST = """#!/usr/bin/env bash
set -e
[ "$(bash src/greet.sh hello Ada)" = "Hello, Ada!" ]
[ "$(bash src/greet.sh bye Ada)" = "Goodbye, Ada!" ]
echo OK
"""

slug_of = {}


def issue_file(i):
    name = f"{i['n']:02d}-{i['slug']}.md"
    status = i.get("status", "open")
    blocked = ", ".join(f"{b:02d}-{slug_of[b]}.md" for b in i.get("blocked_by", [])) or "none"
    head = [f"Title: {i['title']}", f"Type: {i['type']}", f"Labels: {', '.join(i['labels']) or 'none'}",
            f"Status: {status}"]
    if status == "closed":
        head.append(f"Closed as: {i.get('closed_as', 'completed')}")
    head += [f"Author: {i.get('author', 'ada')}", f"Created: {i['created']}", "Parent: none", f"Blocked by: {blocked}"]
    text = "\n".join(head) + "\n\n" + i["body"].rstrip() + "\n\n## Comments\n"
    for c in i.get("comments", []):
        text += f"\n### {c[0]}\n\n{c[1].rstrip()}\n"
    return name, text


def release_issue(n, k, planned, cut, order, c_start, c_end):
    titles = {i["n"]: i["title"] for i in ISSUES}
    titles.update({12: "Hello command", 13: "Greeting lacks the exclamation mark"})
    left = "\n".join(f"- #{m} {titles[m]}: the size was reached by the entries above." for m in LEFT_OUT[n])
    lines = "\n".join(f"{j}. #{m} {titles[m]}: next in the Milestone's order." for j, m in enumerate(order, 1))
    notes = (f"## Release {k} ({cut})\n\nRelease {k} of the greeter.\n\nCommits: {c_start}..{c_end}.\n\n"
             + "\n".join(f"- {titles[m]} (#{m})" for m in order))
    comments = [(f"{cut}T10:05:00Z", notes)]
    if k < 3:
        comments += [(f"{cut}T11:00:00Z", "<!-- release end-of-Release pass -->\ntriage ran for this Release."),
                     (f"{cut}T12:00:00Z", "<!-- release end-of-Release pass -->\nretro-planning ran for this Release.")]
    return dict(n=n, slug=f"release-{k}", title=f"Release {k}", type="release", labels=[], status="closed",
                created=planned, author="release-thread",
                body=f"**Goal:** Release {k} of the greeter.\n\n**Label:** `release-{k}`. Every issue in this Release "
                     f"carries it.\n\n**Milestone:** #1\n\n**Size:** 1. Used: {len(order)}.\n\n## Order\n\n{lines}\n\n"
                     f"## Left out\n\n{left}\n\n## Proposed to the user\n\nNone.\n\n## Notes\n\n"
                     "Posted as a comment when the Release is cut.\n",
                comments=comments)


def build(out):
    out = pathlib.Path(out)
    if out.exists():
        sys.exit(f"{out} exists")
    slug_of.clear()
    r = out / "repo"
    (r / "docs/dev-skills").mkdir(parents=True)
    (r / "src").mkdir()
    (r / ".scratch/issues").mkdir(parents=True)
    (r / ".scratch/pulls").mkdir()
    rel.git(r, "init", "-q", "-b", "main")
    (r / "CLAUDE.md").write_text(rel.CLAUDE)
    (r / "docs/dev-skills/index.md").write_text(INDEX)
    (r / "docs/dev-skills/issue-tracker.md").write_text(TRACKER)
    (r / "docs/dev-skills/boundaries.md").write_text(rel.BOUNDARIES)
    (r / "docs/dev-skills/triage-labels.md").write_text(rel.LABEL_DOC)
    (r / "docs/dev-skills/release.md").write_text(RELEASE_DOC)
    (r / ".gitignore").write_text(".scratch/proposed-actions.md\n.scratch/report.md\n")
    (r / "test.sh").write_text(TEST)
    (r / "CHANGELOG.md").write_text("# Changelog\n")

    early = GREET.replace('name="${2:-world}"', 'name="${2:-}"').replace("  bye) echo \"Goodbye, $name!\" ;;\n", "")
    early = early.replace(" | greet.sh bye <name>", "")
    (r / "src/greet.sh").write_text(early)
    (r / "test.sh").write_text(TEST.replace('[ "$(bash src/greet.sh bye Ada)" = "Goodbye, Ada!" ]\n', ""))
    c0 = rel.commit(r, "chore: initial greeter with hello (#5)", "2026-09-10T10:00:00Z")
    (r / "CHANGELOG.md").write_text("# Changelog\n\n## Release 1 (2026-09-12)\n\nRelease 1 of the greeter.\n\n"
                                    f"Commits: {c0}..{c0}.\n\n- Hello command (#12)\n")
    c1 = rel.commit(r, "docs(release): Release 1 (#6)", "2026-09-12T10:00:00Z")
    (r / "src/greet.sh").write_text(early.replace('name="${2:-}"', 'name="${2:-world}"'))
    c2 = rel.commit(r, "fix: hello with no name greets the world (#8)", "2026-09-25T10:00:00Z")
    (r / "CHANGELOG.md").write_text((r / "CHANGELOG.md").read_text().replace(
        "# Changelog\n", "# Changelog\n\n## Release 2 (2026-10-01)\n\nRelease 2 of the greeter.\n\n"
        f"Commits: {c1}..{c2}.\n\n- Greeting lacks the exclamation mark (#13)\n", 1))
    c3 = rel.commit(r, "docs(release): Release 2 (#7)", "2026-10-01T10:00:00Z")
    (r / "src/greet.sh").write_text(GREET)
    (r / "test.sh").write_text(TEST)
    c4 = rel.commit(r, "feat: bye command (#9)", "2026-10-30T10:00:00Z")
    (r / "CHANGELOG.md").write_text((r / "CHANGELOG.md").read_text().replace(
        "# Changelog\n", f"# Changelog\n\n## Release 3 (2026-11-03)\n\nRelease 3 of the greeter.\n\n"
        f"Commits: {c3}..{c4}.\n\n- Farewell command (#10)\n", 1))
    rel.commit(r, "docs(release): Release 3 (#11)", "2026-11-03T10:00:00Z")

    pulls = {5: ("feat: hello command", c0, "Closes #12"), 8: ("fix: hello with no name greets the world", c2,
             "Closes #13. The name now defaults to `world` too."), 9: ("feat: bye command", c4, "Closes #10")}
    for n, (title, sha, body) in pulls.items():
        (r / f".scratch/pulls/{n}.md").write_text(
            f"Title: {title}\nState: merged\nBase: main\nMerge commit: {sha}\nBody:\n~~~\n{body}\n~~~\n")

    milestone = dict(n=1, slug="milestone-1", title="Milestone 1: Round out the greeter's commands", type="milestone",
                     labels=["milestone-1"], created="2026-09-01", author="ada",
                     body="## Goal\n\nRound out the greeter's commands.\n\n## Features, in build order\n\n"
                          "| # | Feature | Kind | Accepted when |\n| --- | --- | --- | --- |\n"
                          "| 1 | #10 Farewell command | ticket | it works as its issue says |\n"
                          "| 2 | #20 Quiet flag | ticket | it works as its issue says |\n\n## Excluded\n\n- Translations.\n")
    hello = dict(n=12, slug="hello", title="Hello command", type="ticket", status="closed", created="2026-09-01",
                 author="ada", labels=["ready-for-agent", "enhancement", "milestone-1", "release-1"],
                 body="`greet.sh hello <name>` greets by name.",
                 comments=[("2026-09-10T10:00:00Z", "Closed by pull request #5.")])
    bang = dict(n=13, slug="bang", title="Greeting lacks the exclamation mark", type="ticket", status="closed",
                created="2026-09-11", author="grace", labels=["ready-for-agent", "bug", "release-2"],
                body="`greet.sh hello Ada` should end with `!`.",
                comments=[("2026-09-25T10:00:00Z", "Closed by pull request #8.")])
    releases = [release_issue(2, 1, "2026-09-02", "2026-09-12", [12], c0, c0),
                release_issue(3, 2, "2026-09-12", "2026-10-01", [13], c1, c2),
                release_issue(4, 3, "2026-10-01", "2026-11-03", [10], c3, c4)]
    everything = [milestone, hello, bang] + releases + ISSUES
    for i in everything:
        slug_of[i["n"]] = i["slug"]
    for i in everything:
        fname, text = issue_file(i)
        (r / ".scratch/issues" / fname).write_text(text)
    labels = ["release-1", "release-2", "release-3", "milestone-1", "needs-triage", "needs-info", "ready-for-agent",
              "ready-for-human", "wontfix", "bug", "enhancement", "next-release", "parked"]
    (r / ".scratch/labels.md").write_text("\n".join(labels) + "\n")
    (out / "PROMPT.md").write_text("""# triage backlog-sweep case

Give the fresh session only the text between the --- lines, with <checkout> replaced by the checkout under test.

---
You are run by the Release thread of the repo in your working directory, at its end-of-Release pass: Release 3 was
just cut and its release issue, #4 (`.scratch/issues/04-release-3.md`), is closed. Load the `triage` skill from
`<checkout>/plugins/dev-skills/skills/triage/SKILL.md` and run its Triage batch for Release 3, naming release issue
#4; load any skill it names from `<checkout>/plugins/dev-skills/skills/<name>/SKILL.md`. Today is 2026-11-04,
09:00 UTC.

The tracker is in dry-run mode: `docs/dev-skills/issue-tracker.md` says how to record each write as a block in
`.scratch/proposed-actions.md`. Read git history and run the code freely; make no commit or branch. The user is
away: write anything you would tell the user to `.scratch/report.md` (if you cannot write that file, return the same text as your final message), and wait on no reply. Stop when the Triage
batch ends; plan no Release.
---
""")
    return r


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: make_fixture.py <out-dir>")
    build(sys.argv[1])
