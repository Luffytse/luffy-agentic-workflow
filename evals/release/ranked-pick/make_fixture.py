#!/usr/bin/env python3
"""Build one ranked-pick case of the release eval, outside this repo.

Usage: make_fixture.py <out-dir> <case>
Makes <out-dir>/repo (a git repo on main with a dry-run local tracker under .scratch/) and <out-dir>/PROMPT.md (the
prompt for a fresh Release thread). Cases are in cases.py; see evals/release/README.md.
"""
import os
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cases import CASES, GOAL  # noqa: E402

TRACKER = """# Issue tracker: local Markdown, dry run

Issues are files under `.scratch/issues/`, one per issue, named `NN-slug.md`; issue `#NN` is the file whose name
starts `NN-`. Each starts with header lines: `Title:`, `Type:` (milestone, release, spec or ticket), `Labels:`
(comma-separated), `Status:` (open or closed), `Closed as:` (closed issues only: completed or not planned),
`Created:` (date), `Parent:` (an issue file, or none) and `Blocked by:` (issue files, or none). The body follows a
blank line; comments follow a `## Comments` heading, each with its time. The labels that exist are listed in
`.scratch/labels.md`, one per line. Pull requests are files under `.scratch/pulls/`, `<n>.md`.

**Dry run.** Read operations read the files. **No write operation changes any file under `.scratch/issues/`,
`.scratch/pulls/` or `.scratch/labels.md`, and no commit or branch is made in git.** Instead, each write is appended
to `.scratch/proposed-actions.md` as one block, numbered in the order you would take it:

    ### <k>. <Operation name>
    Issue: <issue file, or "new">
    <the operation's fields, as listed below>

A message to the user goes to `.scratch/report.md` (if you cannot write that file, return the same text as your final message) instead.

- **Read an issue**: read its file.
- **List issues**: read every file under `.scratch/issues/`.
- **Create an issue**: fields `Title:`, `Labels:`, `Parent:`, then `Body:` followed by the whole body between `~~~` lines. The new issue's file name is the next free `NN-slug.md`; give it in the `Issue:` line as `new (NN-slug.md)`.
- **Edit an issue body**: fields `Body:` followed by the WHOLE new body between `~~~` lines.
- **Create a label**: field `Label:`.
- **Apply / remove labels**: fields `Add:` and `Remove:` (comma-separated, or none).
- **Check a sub-issue link**: an issue is a sub-issue of a parent when its `Parent:` header names the parent's file, or its body has a `Part of #<parent>` line.
- **Comment on an issue**: field `Body:` followed by the comment between `~~~` lines.
- **Close**: field `Outcome:` (completed or not planned) and a one-line `Reason:`.
- **Count open blockers**: read the issue's `Blocked by:` header and the `Status:` of each issue it names. A blocker whose status is `closed` is cleared, unless it has a `Closed as: not planned` line. The issue is startable when no named blocker is open or uncleared.
- **Park**: an issue is parked when its `Labels:` include `parked`.
- **Read a PR**: read `.scratch/pulls/<n>.md`: its title, state, base branch, merge commit and body.
- **List PRs**: read every file under `.scratch/pulls/`.
- **Open a pull request**: fields `Branch:`, `Title:`, `Body:` (between `~~~` lines), then, for each file it changes, `File: <path>` followed by the file's WHOLE new content between `~~~` lines. Give it the next free number in the `Issue:` line as `new (PR <n>)`.
- **Update a pull request**: as **Open a pull request**, with `Issue:` naming the pull request.
- **Merge a pull request**: field `Pull:` (its number). It merges into main.
- **Run a command**: field `Command:`. Use it for a check you would run on a pull request's branch; in this dry run every such check passes.
- **Run a skill**: fields `Skill:` and `Brief:` (between `~~~` lines). In this dry run the skill runs and changes nothing.
"""

BOUNDARIES = """# Boundary record

- **Irreversible actions agents may take**: none beyond the defaults.
- **Actions that need the user's approval**: none.
- **Merges**: agents merge every pull request whose checks pass, including docs-only changelog pull requests.
- **Budget**: none.
- **Check-in interval**: 1 hour.
- **Milestone label form**: `milestone-<n>`. An issue belongs to a Milestone when it carries that Milestone's label, and the Milestone issue carries it too.
"""

LABEL_DOC = """# Triage Labels

| Role in `dev-skills` | Label in our tracker |
| --- | --- |
| `needs-triage` | `needs-triage` |
| `needs-info` | `needs-info` |
| `ready-for-agent` | `ready-for-agent` |
| `ready-for-human` | `ready-for-human` |
| `wontfix` | `wontfix` |
| `bug` | `bug` |
| `enhancement` | `enhancement` |
| `next-release` | `next-release` |

`next-release` marks an issue that must join the next Release. `parked` marks an issue that waits on the user.
`release-<n>` labels mark the issues of one Release.
"""

RELEASE_DOC = """# Releases

- **Versioning policy**: none.
- **Release name**: the name `Release <n>`, the label `release-<n>` and the release issue title `Release <n>`; `<n>` counts up.
- **Release size**: {size}. A Release takes at most {size} items, counted of any kind: a Spec with its Tickets is 1, a lone Ticket is 1, a bug is 1. A severe issue joins past it.
- **Changelog**: `CHANGELOG.md`, newest entry first. One entry per Release, covering everything merged since the last Release, with its start and end commits.
- **Label prefix**: `release-`.
- **Cut steps**: none.
- **Whole-Release check**: `bash test.sh` on the changelog pull request's branch.

## Policy: none

This repo keeps no version. A Release's changelog entry lists no versions, and no cut step changes a version.
"""

INDEX = """# Docs index

- [docs/dev-skills/issue-tracker.md](issue-tracker.md): the local Markdown tracker, in dry-run mode, and its operations. Read before any tracker or pull request operation.
- [docs/dev-skills/triage-labels.md](triage-labels.md): the label for each triage role and `next-release`.
- [docs/dev-skills/boundaries.md](boundaries.md): the Boundary record, including who merges.
- [docs/dev-skills/release.md](release.md): the release doc: name, size, changelog, cut steps, whole-Release check. Read when cutting or planning a Release.
"""

CLAUDE = """# greeter

A tiny shell greeter. Run `bash test.sh` before each push.

## Agent skills

Start at `docs/dev-skills/index.md`. Issues live in the local dry-run tracker (`docs/dev-skills/issue-tracker.md`).
"""

GREET = """#!/usr/bin/env bash
# usage: greet.sh hello <name>
case "${1:-}" in
  hello) echo "Hello, ${2:-world}!" ;;
  *) echo "usage: greet.sh hello <name>" >&2; exit 2 ;;
esac
"""

TEST_SH = '#!/usr/bin/env bash\nset -e\n[ "$(bash src/greet.sh hello Ada)" = "Hello, Ada!" ]\necho OK\n'


def main_files(case):
    """main's src/greet.sh and test.sh for a case: the base greeter, plus each defect an open issue of the case reports,
    so every issue is true on the fixture's main. Keyed by issue slug; test_cases.py checks each claim."""
    slugs = {i["slug"] for i in case["issues"] if i.get("status", "open") == "open"}
    greet, test = GREET, TEST_SH
    if "usage-typo" in slugs:  # #30: the usage line says helo
        greet = greet.replace('echo "usage: greet.sh hello <name>"', 'echo "usage: greet.sh helo <name>"')
    if "empty-name" in slugs:  # an empty name is kept, so the greeting reads "Hello, !"
        greet = greet.replace("${2:-world}", "${2-world}")
    if "exit-code" in slugs:  # an unknown command exits 0 when stdout is not a terminal, so a pipe hides it
        greet = greet.replace('>&2; exit 2 ;;', '>&2; if [ -t 1 ]; then exit 2; fi; exit 0 ;;')
    if "trailing-space" in slugs:  # every greeting ends in a space; test.sh trims it, so it does not catch it
        greet = greet.replace('world}!"', 'world}! "')
        test = test.replace("$(bash src/greet.sh hello Ada)", "$(bash src/greet.sh hello Ada | sed 's/ *$//')")
    if "name-log" in slugs:  # every name goes to a world-readable log
        greet = greet.replace('case "${1:-}" in',
                              "printf '%s\\n' \"${2:-}\" >> /tmp/greet.log; chmod 0666 /tmp/greet.log\ncase \"${1:-}\" in")
    if "profile" in slugs:  # --save writes the greeting over ~/.profile
        greet = greet.replace('  hello) echo "Hello, ${2:-world}!" ;;',
                              '  hello) echo "Hello, ${2:-world}!"\n'
                              '    if [ "${3:-}" = "--save" ]; then echo "Hello, ${2:-world}!" > "$HOME/.profile"; fi ;;')
    if "token-log" in slugs:  # test.sh prints the registry token
        test = test.replace("set -e\n", 'set -e\necho "registry token: ${REGISTRY_TOKEN:-}"\n')
    if "slow-test" in slugs:  # test.sh sleeps 10 s for nothing
        test = test.replace("set -e\n", "set -e\nsleep 10\n")
    return greet, test


def git(repo, *args, date=None):
    env = dict(os.environ, GIT_AUTHOR_NAME="dev", GIT_AUTHOR_EMAIL="dev@example.com",
               GIT_COMMITTER_NAME="dev", GIT_COMMITTER_EMAIL="dev@example.com")
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True, env=env).stdout.strip()


def commit(repo, msg, date):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg, date=date)
    return git(repo, "rev-parse", "--short=7", "HEAD")


def issue_file(i):
    name = f"{i['n']:02d}-{i['slug']}.md"
    status = i.get("status", "open")
    blocked = ", ".join(f"{b:02d}-" + slug_of[b] + ".md" for b in i.get("blocked_by", [])) or "none"
    parent = f"{i['parent']:02d}-{slug_of[i['parent']]}.md" if i.get("parent") else "none"
    head = [f"Title: {i['title']}", f"Type: {i['type']}", f"Labels: {', '.join(i['labels']) or 'none'}",
            f"Status: {status}"]
    if status == "closed":
        head.append(f"Closed as: {i.get('closed_as', 'completed')}")
    head += [f"Created: {i['created']}", f"Parent: {parent}", f"Blocked by: {blocked}"]
    text = "\n".join(head) + "\n\n" + i["body"].rstrip() + "\n\n## Comments\n"
    for c in i.get("comments", []):
        text += f"\n### {c[0]}\n\n{c[1].rstrip()}\n"
    return name, text


slug_of = {}


def notes_extra(case):
    return f"\n{case['notes_text']}\n" if case.get("notes_text") else ""


def carried_order(case):
    """Order lines for the issues Release 2 carried over (they were taken into it, so they sit in its Order)."""
    return "".join(f"{k}. #{n} {t}: taken for its place in the Milestone's order.\n"
                   for k, (n, t, _) in enumerate(case.get("carried", []), 2))


def carried_section(case):
    """The `## Carried over` section of Release 2's release issue, for a case whose Release 2 carried issues over."""
    if not case.get("carried"):
        return ""
    lines = "\n".join(f"- #{n} {t}: {why}." for n, t, why in case["carried"])
    return f"## Carried over\n\n{lines}\n\n"


def build(out, name):
    case = CASES[name]
    slug_of.clear()
    out = pathlib.Path(out)
    if out.exists():
        sys.exit(f"{out} exists")
    r = out / "repo"
    (r / "docs/dev-skills").mkdir(parents=True)
    (r / "src").mkdir()
    (r / ".scratch/issues").mkdir(parents=True)
    (r / ".scratch/pulls").mkdir()
    git(r, "init", "-q", "-b", "main")
    (r / "CLAUDE.md").write_text(CLAUDE)
    (r / "docs/dev-skills/index.md").write_text(INDEX)
    (r / "docs/dev-skills/issue-tracker.md").write_text(TRACKER)
    (r / "docs/dev-skills/boundaries.md").write_text(BOUNDARIES)
    (r / "docs/dev-skills/triage-labels.md").write_text(LABEL_DOC)
    (r / "docs/dev-skills/release.md").write_text(RELEASE_DOC.format(size=case["size"]))
    greet, test = main_files(case)
    (r / "src/greet.sh").write_text(greet)
    (r / "test.sh").write_text(test)
    (r / ".gitignore").write_text(".scratch/proposed-actions.md\n.scratch/report.md\n")
    (r / "CHANGELOG.md").write_text("# Changelog\n")
    c0 = commit(r, "chore: initial greeter", "2026-10-01T10:00:00Z")
    also = ""
    if any(i["slug"] == "ci-red" for i in case["issues"]):  # #9 made test.sh expect a full stop: red on main since
        (r / "test.sh").write_text(test.replace('"Hello, Ada!" ]', '"Hello, Ada." ]'))
        sha9 = commit(r, "test: hello ends with a full stop (#9)", "2026-10-04T10:00:00Z")
        (r / ".scratch/pulls/9.md").write_text(
            f"Title: test: hello ends with a full stop\nState: merged\nBase: main\nMerge commit: {sha9}\n"
            "Merged at: 2026-10-04T10:00:00Z\nBody:\n~~~\nThe greeting should end with a full stop.\n~~~\n")
        also = "\nAlso merged: test.sh expects a full stop (#9).\n"
    (r / "src/greet.sh").write_text(greet.replace("# usage", "# greeter\n# usage"))
    c1 = commit(r, "feat: hello greets by name (#5)", "2026-10-15T10:00:00Z")
    last = "Release 1" if case.get("cut") else "Release 2"
    (r / "CHANGELOG.md").write_text(
        f"# Changelog\n\n## {last} (2026-10-16)\n\nHello greets by name.\n\nCommits: {c0}..{c1}.\n\n- Hello command (#3)\n{also}")
    commit(r, f"docs(release): {last} (#6)", "2026-10-16T10:00:00Z")

    issues = list(case["issues"])
    for i in issues:
        slug_of[i["n"]] = i["slug"]
    goal = case.get("goal", GOAL)
    rows = "\n".join(f"| {k} | #{n} {next(i['title'] for i in issues if i['n'] == n)} | "
                     f"{next(i['type'] for i in issues if i['n'] == n)} | it works as its issue says |"
                     for k, n in enumerate(case["milestone"], 1))
    milestone = dict(n=1, slug="milestone-1", title=f"Milestone 1: {goal.rstrip('.')}", type="milestone",
                     labels=["milestone-1"], created="2026-10-01",
                     body=f"## Goal\n\n{goal}\n\n## Features, in build order\n\n| # | Feature | Kind | Accepted when |\n"
                          f"| --- | --- | --- | --- |\n{rows}\n\n## Excluded\n\n- Translations.\n")
    slug_of[1] = "milestone-1"
    if case.get("cut"):
        # The Order Release 2 was planned with: the case's own (carried-over issues lost the label but stay listed), or
        # else the issues carrying its label.
        members = case.get("order2") or [i["n"] for i in issues if "release-2" in i["labels"]]
        order = "\n".join(f"{k}. #{n} {next(i['title'] for i in issues if i['n'] == n)}: next in the Milestone's order."
                          for k, n in enumerate(members, 1))
        rel = dict(n=2, slug="release-2", title="Release 2", type="release", labels=[], created="2026-10-16",
                   body=f"**Goal:** Say goodbye and keep quiet.\n\n**Label:** `release-2`. Every issue in this Release carries it.\n\n"
                        f"**Milestone:** #1\n\n**Size:** {case['size']}. Used: {len(members)}.\n\n## Order\n\n{order}\n\n"
                        f"## Left out\n\nNone.\n\n{carried_section(case)}## Notes\n\nPosted as a comment when the Release is cut.\n")
        if case.get("old_shape"):
            title = lambda n: next(i["title"] for i in issues if i["n"] == n)  # noqa: E731
            scope = "\n".join(f"- **{title(n)}**: next in the Milestone's order.\n  - #{n} {title(n)}" for n in members)
            rel["body"] = ("**Goal:** Say goodbye and keep quiet.\n\n**Label:** `release-2`. Every issue in this Release carries it.\n\n"
                           f"**Milestone:** #1\n\n**Cap:** 5 features. Used: {len(members)}. Maintenance fixes: 0, outside the cap.\n\n"
                           f"## Scope\n\n{scope}\n\n## Notes\n\nPosted as a comment when the Release is cut.\n")
        shas = {}
        for k, p in enumerate(case["pulls"]):
            f = r / p["file"]
            f.write_text((f.read_text() if f.exists() else "") + p["line"])
            shas[p["n"]] = commit(r, f"{p['title']} (#{p['n']})", f"2026-10-{20 + k}T10:00:00Z")
            (r / f".scratch/pulls/{p['n']}.md").write_text(
                f"Title: {p['title']}\nState: merged\nBase: main\nMerge commit: {shas[p['n']]}\n"
                f"Merged at: 2026-10-{20 + k}T10:00:00Z\nBody:\n~~~\n{p['body']}\n~~~\n")
        for i in issues:
            if i.get("status") == "closed":
                pr = next(p["n"] for p in case["pulls"] if f"#{i['n']}" in p["body"])
                i.setdefault("comments", []).append(
                    (f"2026-10-{20 + [p['n'] for p in case['pulls']].index(pr)}T10:00:00Z",
                     f"Closed by pull request #{pr}."))
        labels = ["release-1", "release-2"]
    else:
        rel = dict(n=2, slug="release-2", title="Release 2", type="release", labels=[], created="2026-10-10",
                   status="closed",
                   body="**Goal:** Hello greets by name.\n\n**Label:** `release-2`. Every issue in this Release carries it.\n\n"
                        f"**Milestone:** #1\n\n**Size:** 5. Used: {1 + len(case.get('carried', []))}.\n\n## Order\n\n1. #3 Hello command: first in the Milestone's order.\n{carried_order(case)}\n"
                        f"## Left out\n\nNone.\n\n{carried_section(case)}## Notes\n\nPosted as a comment when the Release is cut.\n{notes_extra(case)}",
                   comments=[("2026-10-16T10:05:00Z", "## Release 2 (2026-10-16)\n\nHello greets by name.\n\n"
                              f"Commits: {c0}..{c1}.\n\n- Hello command (#3)"),
                             ("2026-10-16T11:00:00Z", "<!-- release end-of-Release pass -->\ntriage ran for this Release."),
                             ("2026-10-16T12:00:00Z", "<!-- release end-of-Release pass -->\nretro-planning ran for this Release.")])
        labels = ["release-1", "release-2"]
    hello = dict(n=3, slug="hello", title="Hello command", type="ticket", status="closed", created="2026-10-02",
                 labels=["ready-for-agent", "enhancement", "milestone-1", "release-1" if case.get("cut") else "release-2"],
                 body="`greet.sh hello <name>` greets by name.",
                 comments=[("2026-10-15T10:00:00Z", "Closed by pull request #5.")])
    (r / ".scratch/pulls/5.md").write_text(
        f"Title: feat: hello greets by name\nState: merged\nBase: main\nMerge commit: {c1}\nMerged at: 2026-10-15T10:00:00Z\n"
        "Body:\n~~~\nCloses #3\n~~~\n")
    for i in [milestone, rel, hello] + issues:
        slug_of[i["n"]] = i["slug"]
    for i in [milestone, rel, hello] + issues:
        fname, text = issue_file(i)
        (r / ".scratch/issues" / fname).write_text(text)
    labels += ["milestone-1", "needs-triage", "needs-info", "ready-for-agent", "ready-for-human", "wontfix", "bug",
               "enhancement", "next-release", "parked"]
    (r / ".scratch/labels.md").write_text("\n".join(labels) + "\n")
    (out / "PROMPT.md").write_text(f"""# release ranked-pick case: {name}

Give the fresh session only the text between the --- lines, with <checkout> replaced by the checkout under test.

---
You are a Release thread for the repo in your working directory. Load the `release` skill from
`<checkout>/plugins/dev-skills/skills/release/SKILL.md` and follow it; load any skill it names from
`<checkout>/plugins/dev-skills/skills/<name>/SKILL.md`. Today is 2026-11-04, 09:00 UTC.

The tracker and pull requests are in dry-run mode: `docs/dev-skills/issue-tracker.md` says how to record each write
as a block in `.scratch/proposed-actions.md`. Read git history freely; make no commit or branch. The user is away:
write anything you would tell the user to `.scratch/report.md` (if you cannot write that file, return the same text as your final message), and wait on no reply. Stop when the skill's run ends.
{case.get('prompt_extra', '')}
---
""")
    return r


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit(f"usage: make_fixture.py <out-dir> <{'|'.join(CASES)}>")
    build(sys.argv[1], sys.argv[2])
