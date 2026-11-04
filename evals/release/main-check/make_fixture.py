#!/usr/bin/env python3
"""Build the main-check case of the release eval, outside this repo.

Usage: make_fixture.py <out-dir>
Makes <out-dir>/repo (a git repo on main with a dry-run local tracker under .scratch/) and <out-dir>/PROMPT.md (the
prompt for a fresh Release thread that plans Release 3). The case data is in main_case.py; see
evals/release/README.md. The tracker, Boundary record, label and release docs are the ranked-pick cases'
(evals/release/ranked-pick/make_fixture.py), so every release case reads the same dry-run tracker.
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from main_case import GOAL, ISSUES, LATER, MILESTONE_FEATURES, PULLS, TEST_SH, greet  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "release_ranked_pick_fixture", HERE.parent / "ranked-pick/make_fixture.py")
rel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rel)

SIZE = 5


def build(out):
    out = pathlib.Path(out)
    if out.exists():
        sys.exit(f"{out} exists")
    r = out / "repo"
    (r / "docs/dev-skills").mkdir(parents=True)
    (r / "src").mkdir()
    (r / ".scratch/issues").mkdir(parents=True)
    (r / ".scratch/pulls").mkdir()
    rel.git(r, "init", "-q", "-b", "main")
    (r / "CLAUDE.md").write_text(rel.CLAUDE)
    (r / "docs/dev-skills/index.md").write_text(rel.INDEX)
    (r / "docs/dev-skills/issue-tracker.md").write_text(rel.TRACKER)
    (r / "docs/dev-skills/boundaries.md").write_text(rel.BOUNDARIES)
    (r / "docs/dev-skills/triage-labels.md").write_text(rel.LABEL_DOC)
    (r / "docs/dev-skills/release.md").write_text(rel.RELEASE_DOC.format(size=SIZE))
    (r / "src/greet.sh").write_text(greet())
    (r / "test.sh").write_text(TEST_SH)
    (r / ".gitignore").write_text(".scratch/proposed-actions.md\n.scratch/report.md\n")
    (r / "CHANGELOG.md").write_text("# Changelog\n")
    c0 = rel.commit(r, "chore: initial greeter", "2026-10-01T10:00:00Z")
    (r / "README.md").write_text("# greeter\n\n`bash src/greet.sh hello <name>` greets by name.\n")
    c1 = rel.commit(r, "feat: hello greets by name (#5)", "2026-10-15T10:00:00Z")
    (r / "CHANGELOG.md").write_text(
        f"# Changelog\n\n## Release 2 (2026-10-16)\n\nHello greets by name.\n\nCommits: {c0}..{c1}.\n\n- Hello command (#3)\n")
    rel.commit(r, "docs(release): Release 2 (#6)", "2026-10-16T10:00:00Z")
    for p in PULLS:
        (r / "src/greet.sh").write_text(greet(**p["state"]))
        sha = rel.commit(r, f"{p['title']} (#{p['n']})", f"{p['date']}T10:00:00Z")
        (r / f".scratch/pulls/{p['n']}.md").write_text(
            f"Title: {p['title']}\nState: merged\nBase: main\nMerge commit: {sha}\nMerged at: {p['date']}T10:00:00Z\n"
            f"Body:\n~~~\n{p['body']}\n~~~\n")
    (r / ".scratch/pulls/5.md").write_text(
        f"Title: feat: hello greets by name\nState: merged\nBase: main\nMerge commit: {c1}\nMerged at: 2026-10-15T10:00:00Z\n"
        "Body:\n~~~\nCloses #3\n~~~\n")

    title = {i["n"]: i["title"] for i in ISSUES}
    rows = "\n".join(f"| {k} | #{n} {title[n]} | ticket | it works as its issue says |"
                     for k, n in enumerate(MILESTONE_FEATURES, 1))
    milestone = dict(n=1, slug="milestone-1", title=f"Milestone 1: {GOAL.rstrip('.')}", type="milestone",
                     labels=["milestone-1"], created="2026-10-01",
                     body=f"## Goal\n\n{GOAL}\n\n## Features, in build order\n\n| # | Feature | Kind | Accepted when |\n"
                          f"| --- | --- | --- | --- |\n{rows}\n\n## Excluded\n\n- Translations.\n"
                          f"- #{LATER} {title[LATER]}: left to the next Milestone.\n")
    release2 = dict(n=2, slug="release-2", title="Release 2", type="release", labels=[], created="2026-10-10",
                    status="closed",
                    body="**Goal:** Hello greets by name.\n\n**Label:** `release-2`. Every issue in this Release carries it.\n\n"
                         "**Milestone:** #1\n\n**Size:** 5. Used: 1.\n\n## Order\n\n1. #3 Hello command: first in the Milestone's order.\n\n"
                         "## Left out\n\nNone.\n\n## Notes\n\nPosted as a comment when the Release is cut.\n",
                    comments=[("2026-10-16T10:05:00Z", "## Release 2 (2026-10-16)\n\nHello greets by name.\n\n"
                               f"Commits: {c0}..{c1}.\n\n- Hello command (#3)"),
                              ("2026-10-16T11:00:00Z", "<!-- release end-of-Release pass -->\ntriage ran for this Release."),
                              ("2026-10-16T12:00:00Z", "<!-- release end-of-Release pass -->\nretro-planning ran for this Release.")])
    hello = dict(n=3, slug="hello", title="Hello command", type="ticket", status="closed", created="2026-10-02",
                 labels=["ready-for-agent", "enhancement", "milestone-1", "release-2"],
                 body="`greet.sh hello <name>` greets by name.",
                 comments=[("2026-10-15T10:00:00Z", "Closed by pull request #5.")])
    every = [milestone, release2, hello] + [dict(i) for i in ISSUES]
    rel.slug_of.clear()
    for i in every:
        rel.slug_of[i["n"]] = i["slug"]
    for i in every:
        fname, text = rel.issue_file(i)
        (r / ".scratch/issues" / fname).write_text(text)
    labels = ["release-1", "release-2", "milestone-1", "needs-triage", "needs-info", "ready-for-agent",
              "ready-for-human", "wontfix", "bug", "enhancement", "next-release", "parked"]
    (r / ".scratch/labels.md").write_text("\n".join(labels) + "\n")
    (out / "PROMPT.md").write_text("""# release main-check case

Give the fresh session only the text between the --- lines, with <checkout> replaced by the checkout under test.

---
You are a Release thread for the repo in your working directory. Load the `release` skill from
`<checkout>/plugins/dev-skills/skills/release/SKILL.md` and follow it; load any skill it names from
`<checkout>/plugins/dev-skills/skills/<name>/SKILL.md`. Today is 2026-11-04, 09:00 UTC.

This is not a dry run of the skill: run it as written, making every write it says. The tracker and pull requests
are in dry-run mode, so every write is recorded as a block in `.scratch/proposed-actions.md` instead of being made;
`docs/dev-skills/issue-tracker.md` says how. Main is the `main` branch of this repo, already fetched: read its code,
docs and git history freely, and run its scripts; make no commit or branch. If the skill tells you to start
subagents and you cannot, do their part yourself and say so in the report. The user is away: write anything you
would tell or ask the user to `.scratch/report.md`, and wait on no reply. Stop when the skill's run ends.
---
""")
    return r


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: make_fixture.py <out-dir>")
    build(sys.argv[1])
