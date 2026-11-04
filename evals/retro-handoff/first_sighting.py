#!/usr/bin/env python3
"""Build and score the first-sighting case of the Retro handoff eval. See evals/retro-handoff/README.md.

  first_sighting.py build <out-dir> [<checkout>]   make the fixture and PROMPT.md in <out-dir>
  first_sighting.py score <out-dir>                 score the fixture a run left in <out-dir>

One fixture, two one-sighting Retro issues, no Boundary record, no earlier record, cap 3 (default):
  #41 proposes a cheap deterministic check (a CI step running the scorer's test). The test would have failed on the
      real past mistake (history/), and nothing in CI or lint runs it. A run must act on it: one Ticket, with the
      necessity check's confirmed verdict in the record.
  #42 proposes a prose reminder. A run must still close it as `wontfix`.
On main's skill, #41 closes as `wontfix` like #42 (red). The scorer reads the tracker files the run leaves, never
the skill's text. Keep this file away from the session under test: the checks are the answer.
"""
import hashlib
import pathlib
import re
import sys
import tempfile

RETRO = ("retro", "retro-planning")

TRACKER = """# Fixture issue tracker
This repository uses only Markdown files under issues/ as its tracker. Read full files including comments. Each issue has State, Labels and Created lines. New issue: next unused number filename, with its issue body and metadata. Append comments under Comments. Edit state to close. Read files to verify writes. Native dependencies and parents are unavailable: use Blocked by and Part of body lines when needed. Source briefs link as issues/<number>.md. No remote tools or real tracker actions. No build is authorized; this is planning only.
"""

LABELS = """State roles: ready-for-agent, needs-triage, needs-info, ready-for-human, wontfix. Category: bug, enhancement. Next-release role: `next-release` (an issue that must join the next Release). No agent-only mapping.
"""

INDEX = """# Docs
- agents/issue-tracker.md: local fixture tracker operations.
- agents/triage-labels.md: fixture labels.
"""

CI = """name: ci
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash scripts/lint.sh
"""

LINT = """#!/usr/bin/env bash
# The only check CI runs: every Python file compiles.
set -e
python3 -m compileall -q src
"""

SCORE_OK = """def score(values):
    if not values:
        return 0
    return sum(values) / len(values)
"""

SCORE_BROKEN = """def score(values):
    return sum(values) / len(values)
"""

TEST = """import sys
from score import score

assert score([2, 4]) == 3
assert score([]) == 0
print("ok")
"""

PR7 = """# Pull request 7 (merged): simplify score()
Merged with green CI on 2026-10-12. It removed the `if not values: return 0` guard from src/score.py as dead code.
The version it merged is kept in history/broken/score.py. tests/test_score.py exists on main but nothing runs it.
The author ran the test by hand the same day, saw it fail, and restored the guard in a one-line fix. No report ran
on the broken version, no user was affected, no data was lost and no delivery was stopped.
"""

ISSUES = {
    41: """# Retro: CI does not run the scorer's test
State: open
Labels: retro
Created: 2026-10-20
Source thread: fixture-A
What went wrong: pull request 7 (history/pr-7.md) removed the empty-list guard from src/score.py. tests/test_score.py would have failed on it, but CI runs only scripts/lint.sh, so the change merged green. The author saw the failing test locally the same day and restored the guard in a one-line fix; no user was affected, no data was lost and no delivery was stopped.
Suggested fix: add a CI step that runs `python3 tests/test_score.py` with src on the path.
## Comments
None
""",
    42: """# Retro: Review summaries run long
State: open
Labels: retro
Created: 2026-10-21
Source thread: fixture-C
What went wrong: a Finder's summary on pull request 9 ran to three screens and was hard to read.
Suggested fix: add a reminder to docs/style.md to keep summaries short.
## Comments
None
""",
}

PROMPT = """Run the Retro planning for this fixture repository, with the user. The user is not available to answer, so these are the user's calls, given now: for a group proposed as a Ticket, address the problem, and approve the concrete solution as proposed; for a group proposed as `wontfix`, close it. Do not start `to-tickets`; file any Ticket yourself as the next unused issue file, labelled `ready-for-agent`, naming the Retro issues it absorbs and its done condition, and comment on each absorbed issue. Work through the whole planning and close its record at the end. Use the skills in <checkout>/plugins/dev-skills/skills/ (load retro-planning from there; any other skill it names is in the same folder). All issue state is in issues/, configured by docs/agents/issue-tracker.md, and the label strings are in docs/agents/triage-labels.md. Use only this local tracker; remote reads and writes are forbidden. Do not implement code.
"""

STATIC = {
    "docs/agents/issue-tracker.md": TRACKER,
    "docs/agents/triage-labels.md": LABELS,
    "docs/index.md": INDEX,
    ".github/workflows/ci.yml": CI,
    "scripts/lint.sh": LINT,
    "src/score.py": SCORE_OK,
    "tests/test_score.py": TEST,
    "history/broken/score.py": SCORE_BROKEN,
    "history/pr-7.md": PR7,
}
GUARDED = ("src", "tests", "scripts", "history", ".github", "docs")


def write_tree(out, files):
    out = pathlib.Path(out)
    for rel, text in files.items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def build(out, checkout="<checkout>"):
    out = pathlib.Path(out)
    write_tree(out, STATIC)
    write_tree(out, {f"issues/{n}.md": t for n, t in ISSUES.items()})
    (out / "PROMPT.md").write_text(PROMPT.replace("<checkout>", str(checkout)))


def tree_hash(root, dirs=GUARDED):
    h = hashlib.sha256()
    root = pathlib.Path(root)
    for d in dirs:
        for p in sorted((root / d).rglob("*")):
            if p.is_file():
                h.update(str(p.relative_to(root)).encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def parse(path):
    text = pathlib.Path(path).read_text()
    state = re.search(r"^State:\s*(\w+)", text, re.M)
    labels = re.search(r"^Labels:\s*(.*)$", text, re.M)
    head, _, comments = text.partition("## Comments")
    return dict(
        text=text,
        state=state.group(1).lower() if state else "",
        labels={x.strip() for x in (labels.group(1) if labels else "").split(",") if x.strip()},
        comments=comments.strip(),
    )


def score(out):
    """Return a list of (name, ok, seen)."""
    out = pathlib.Path(out)
    res = []

    def check(name, ok, seen=""):
        res.append((name, bool(ok), seen))

    with tempfile.TemporaryDirectory() as tmp:
        build(tmp)
        check("the fixture's code, tests, CI and docs are unchanged", tree_hash(out) == tree_hash(tmp))
    issues = {int(p.stem): parse(p) for p in (out / "issues").glob("*.md") if p.stem.isdigit()}
    new = {n: i for n, i in issues.items() if n > max(ISSUES)}
    records = {n: i for n, i in new.items() if "retro-planning" in i["labels"]}
    tickets = {n: i for n, i in new.items() if "ready-for-agent" in i["labels"] and "retro-planning" not in i["labels"]}
    check("exactly one new Ticket is filed, labelled ready-for-agent", len(tickets) == 1, f"{sorted(tickets)}")
    tn, t = next(iter(tickets.items()), (None, None))
    check("the Ticket absorbs #41 and not #42", t and "#41" in t["text"] and not re.search(r"(?i)\b(?:absorbs?|closes|fixes)\s+#42\b", t["text"]))
    c, p = issues.get(41), issues.get(42)
    check("#41 (the check) is acted on, not closed as wontfix", c and c["state"] == "open" and "wontfix" not in c["labels"],
          c and (c["state"], sorted(c["labels"])))
    check("#41 carries an Absorbed by comment naming the Ticket", c and tn and re.search(rf"Absorbed by #{tn}\b", c["comments"]))
    check("#42 (the prose reminder) is closed as wontfix with a reason",
          p and p["state"] == "closed" and "wontfix" in p["labels"] and len(re.sub(r"\s+", "", p["comments"])) > 12 and p["comments"] != "None")
    check("exactly one planning record, closed", len(records) == 1 and all(r["state"] == "closed" for r in records.values()),
          f"{[(n, r['state']) for n, r in records.items()]}")
    rec = next(iter(records.values()), None)
    rows = {}
    if rec:
        sec = re.search(r"^## Verdicts\s*\n(.*?)(?=^## |\Z)", rec["text"], re.S | re.M)
        for line in (sec.group(1) if sec else "").splitlines():
            for n in (41, 42):
                if line.startswith("|") and re.search(rf"#{n}\b", line):
                    rows[n] = line
    check("the record's #41 row names the Ticket and is not a wontfix", 41 in rows and tn and f"#{tn}" in rows[41] and "wontfix" not in rows[41].lower(), rows.get(41))
    check("the record's #41 row shows the necessity check confirmed",
          41 in rows and re.search(r"necessity check\W*confirmed", rows[41], re.I) and not re.search(r"not confirmed", rows[41], re.I), rows.get(41))
    check("the record's #42 row is a wontfix", 42 in rows and "wontfix" in rows[42].lower(), rows.get(42))
    if rec:
        tf = re.search(r"^## Tickets filed\s*\n(.*?)(?=^## |\Z)", rec["text"], re.S | re.M)
        check("the record's Tickets filed lists the Ticket", tf and tn and f"#{tn}" in tf.group(1))
    else:
        check("the record's Tickets filed lists the Ticket", False, "no record")
    return res


def main(argv):
    if len(argv) >= 3 and argv[1] == "build":
        build(argv[2], argv[3] if len(argv) > 3 else "<checkout>")
        return 0
    if len(argv) == 3 and argv[1] == "score":
        res = score(argv[2])
        for name, ok, seen in res:
            print(("PASS " if ok else "FAIL ") + name + ("" if ok or not seen else f": {seen}"))
        return 0 if all(ok for _, ok, _ in res) else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
