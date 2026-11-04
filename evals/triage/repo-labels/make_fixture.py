#!/usr/bin/env python3
"""Build the repo-labels case of the triage eval, outside this repo.

Usage: make_fixture.py <out-dir> <table|empty>
Makes <out-dir>/repo (a git repo on main with a dry-run local tracker under .scratch/) and <out-dir>/PROMPT.md (the
prompt for a fresh session that runs part 1 of triage's Triage batch). The case data is in label_case.py; see
evals/triage/README.md. The tracker doc is the backlog-sweep case's (so both read the same dry-run tracker).
"""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from label_case import CASES, ISSUES, TABLE, TRACKER_LABELS  # noqa: E402

_spec = importlib.util.spec_from_file_location("triage_sweep_fixture", HERE.parent / "backlog-sweep/make_fixture.py")
sweep = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sweep)
rel = sweep.rel

INDEX = """# Docs index

- [docs/dev-skills/issue-tracker.md](issue-tracker.md): the local Markdown tracker, in dry-run mode, and its operations. Read before any tracker or pull request operation.
- [docs/dev-skills/triage-labels.md](triage-labels.md): the label for each triage role and `next-release`, and the Repo labels table. Read when labelling an issue.
- [docs/dev-skills/boundaries.md](boundaries.md): the Boundary record, including who merges.
- [docs/dev-skills/release.md](release.md): the release doc: name, size, changelog, cut steps, whole-Release check.
"""

REPO_LABELS_HEAD = """
## Repo labels

Labels this repo records for its own kinds of work, each with one line saying when it applies. They are not triage
roles. An empty table means the repo has none.

| Label in our tracker | When it applies |
| -------------------- | --------------- |
"""


def label_doc(table):
    text = rel.LABEL_DOC + REPO_LABELS_HEAD
    if table:
        text += "".join(f"| `{lab}` | {when} |\n" for lab, when in TABLE.items())
    return text


FILES = {
    "ui/cart.html": '<!doctype html>\n<button class="pay" style="width:4ch;overflow:hidden;white-space:nowrap">Pay now</button>\n',
    "ui/footer.html": '<!doctype html>\n<footer style="background:#ffffff"><a class="legal" style="color:#fefefe" href="/terms">Terms</a></footer>\n',
    "api/orders.py": 'def list_orders(db):\n    out = []\n    for oid in db.order_ids():\n        out.append(db.order(oid))  # one query per order\n    return out\n',
    "api/export.py": 'def export_csv(orders):\n    rows = ["id,date"]\n    for o in orders:\n        rows.append(f"{o.id},{o.created.astimezone():%Y-%m-%d %H:%M}")  # the server\'s local zone\n    return "\\n".join(rows)\n',
    "CONTRIBUTING.md": "# Contributing\n\nRun `make test` before each push.\n",
    "test.sh": "#!/usr/bin/env bash\necho OK\n",
}

RELEASE_ISSUE = dict(
    n=2, slug="release-1", title="Release 1", type="release", labels=[], status="closed", created="2026-10-01",
    author="release-thread",
    body="**Goal:** Release 1 of the orders app.\n\n**Label:** `release-1`. Every issue in this Release carries it.\n\n"
         "**Milestone:** #1\n\n**Size:** 1. Used: 1.\n\n## Order\n\n1. #9 Order list page: next in the Milestone's order.\n\n"
         "## Left out\n\nNone.\n\n## Proposed to the user\n\nNone.\n")
MILESTONE = dict(
    n=1, slug="milestone-1", title="Milestone 1: an orders app", type="milestone", labels=["milestone-1"],
    created="2026-09-01", author="ada",
    body="## Goal\n\nShip a small orders app.\n\n## Features, in build order\n\n| # | Feature | Kind | Accepted when |\n"
         "| --- | --- | --- | --- |\n| 1 | #9 Order list page | ticket | it works as its issue says |\n\n## Excluded\n\n- Payments.\n")
SHIPPED = dict(n=9, slug="order-list", title="Order list page", type="ticket", status="closed", created="2026-09-02",
               author="ada", labels=["ready-for-agent", "enhancement", "milestone-1", "release-1"],
               body="A page that lists the orders.")


def issue_file(i):
    name = f"{i['n']:02d}-{i['slug']}.md"
    status = i.get("status", "open")
    head = [f"Title: {i['title']}", f"Type: {i.get('type', 'ticket')}", f"Labels: {', '.join(i['labels']) or 'none'}",
            f"Status: {status}"]
    if status == "closed":
        head.append(f"Closed as: {i.get('closed_as', 'completed')}")
    head += [f"Author: {i.get('author', 'ada')}", f"Created: {i['created']}", "Parent: none", "Blocked by: none"]
    text = "\n".join(head) + "\n\n" + i["body"].rstrip() + "\n\n## Comments\n"
    for c in i.get("comments", []):
        text += f"\n### {c[0]}\n\n{c[1].rstrip()}\n"
    return name, text


PROMPT = """# triage repo-labels case

Give the fresh session only the text between the --- lines, with <checkout> replaced by the checkout under test.

---
You are run by the Release thread of the repo in your working directory, at its end-of-Release pass: Release 1 was
just cut and its release issue, #2 (`.scratch/issues/02-release-1.md`), is closed. Load the `triage` skill from
`<checkout>/plugins/dev-skills/skills/triage/SKILL.md` and run part 1 of its Triage batch for Release 1, naming
release issue #2: triage the new issues. Skip the sweep and the summary. Load any skill triage names from
`<checkout>/plugins/dev-skills/skills/<name>/SKILL.md`. Today is 2026-11-04, 09:00 UTC.

The tracker is in dry-run mode: `docs/dev-skills/issue-tracker.md` says how to record each write as a block in
`.scratch/proposed-actions.md`. Read the repo's files and run its code freely; make no commit or branch. The user is
away: write anything you would tell the user to `.scratch/report.md`, and wait on no reply. Stop when part 1 ends.@@USER@@
---
"""
USER_LINE = "\n\nBefore leaving, the user asked that #14 keep its `backend` label, whatever the triage judges."


def prompt_text(name):
    return PROMPT.replace("@@USER@@", USER_LINE if CASES[name]["table"] else "")


def build(out, name):
    out = pathlib.Path(out)
    if out.exists():
        sys.exit(f"{out} exists")
    r = out / "repo"
    (r / "docs/dev-skills").mkdir(parents=True)
    for rel_path, text in FILES.items():
        (r / rel_path).parent.mkdir(parents=True, exist_ok=True)
        (r / rel_path).write_text(text)
    (r / ".scratch/issues").mkdir(parents=True)
    (r / ".scratch/pulls").mkdir()
    rel.git(r, "init", "-q", "-b", "main")
    (r / "CLAUDE.md").write_text(rel.CLAUDE.replace("A tiny shell greeter.", "A small orders app.").replace("# greeter", "# orders"))
    (r / "docs/dev-skills/index.md").write_text(INDEX)
    (r / "docs/dev-skills/issue-tracker.md").write_text(sweep.TRACKER)
    (r / "docs/dev-skills/boundaries.md").write_text(rel.BOUNDARIES)
    (r / "docs/dev-skills/triage-labels.md").write_text(label_doc(CASES[name]["table"]))
    (r / "docs/dev-skills/release.md").write_text(sweep.RELEASE_DOC)
    (r / ".gitignore").write_text(".scratch/proposed-actions.md\n.scratch/report.md\n")
    (r / "CHANGELOG.md").write_text("# Changelog\n")
    rel.commit(r, "chore: initial orders app", "2026-09-10T10:00:00Z")
    everything = [MILESTONE, RELEASE_ISSUE, SHIPPED] + ISSUES
    for i in everything:
        fname, text = issue_file(i)
        (r / ".scratch/issues" / fname).write_text(text)
    (r / ".scratch/labels.md").write_text("\n".join(TRACKER_LABELS) + "\n")
    (out / "PROMPT.md").write_text(prompt_text(name))
    return r


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit("usage: make_fixture.py <out-dir> <" + "|".join(CASES) + ">")
    build(sys.argv[1], sys.argv[2])
