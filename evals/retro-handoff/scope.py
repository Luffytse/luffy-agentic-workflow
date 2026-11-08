#!/usr/bin/env python3
"""Build and score the scope case of the Retro handoff eval. See evals/retro-handoff/README.md.

  scope.py build <out-dir> [<checkout>]   make the fixture and PROMPT.md in <out-dir>
  scope.py score <out-dir>                 score the fixture a run left in <out-dir>

One fixture, a Release-end Retro planning with nobody to ask, in the repo where the plugin's Retros go:
  #51  no Scope line; really an `environment` limit (a thread may push only its designated branch; lost commits).
  #52  `Scope: environment`, another thread, the same limit. #51 and #52 are severe and seen in 2 threads.
  #53  `Scope: skill`, seen in 2 threads (a Seen again comment), not severe.
  #54  `Scope: this repo`, filed here by mistake: it is another project's own lesson. That project's tracker is the
       local directory other-project/.
A right run gives each a Scope in the record (#51 gets one there), never groups two Scopes together, aims the
environment Ticket at the Harness reference (`worker-control`) and Startup verification instead of a sentence in
each skill, and refiles #54 in other-project/ and closes it here with a link. On main's skill (root cause only,
no Scope) it is red. The scorer reads the tracker files the run leaves, never the skill's text. Keep this file away
from the session under test: the checks are the answer.
"""
import hashlib
import pathlib
import re
import sys
import tempfile


TRACKER = """# Fixture issue tracker
This repository is where the dev-skills plugin's Retro issues go. It uses only Markdown files under issues/ as its tracker. Read full files including comments. Each issue has State, Labels and Created lines. New issue: next unused number filename, with its issue body and metadata. Append comments under Comments. Edit state to close. Read files to verify writes. Native dependencies and parents are unavailable: use Blocked by and Part of body lines when needed. Source briefs link as issues/<number>.md. Another project's tracker, other-project/issues/, follows the same form (see other-project/docs/agents/issue-tracker.md). No remote tools or real tracker actions. No build is authorized; this is planning only.
"""

OTHER_TRACKER = """# Fixture issue tracker of the project acme-app
This project uses only Markdown files under issues/ as its tracker, in the same form as the plugin repository's: State, Labels and Created lines, a body, and a Comments section. New issue: next unused number filename. No remote tools or real tracker actions.
"""

LABELS = """State roles: ready-for-agent, needs-triage, needs-info, ready-for-human, wontfix. Category: bug, enhancement. Next-release role: `next-release` (an issue that must join the next Release). No agent-only mapping.
"""

INDEX = """# Docs
- agents/issue-tracker.md: local fixture tracker operations.
- agents/triage-labels.md: fixture labels.
"""

RELEASE = """# Release 3
State: closed
Labels: release
Created: 2026-10-25
Milestone issue: issues/31.md
## Scope
- #32 Summary report export
## Comments
All scoped issues closed. Release 3 cut on 2026-10-31.
"""

MILESTONE = """# Milestone 1: reliable reports
State: open
Labels: milestone
Created: 2026-10-20
## Goal
Reports never fail on real data.
## Features (in order)
1. #33 Summary report handles every import (planned, not yet built)
## Exclusions
None
"""

DONE = """# Summary report export
State: closed
Labels: enhancement
Created: 2026-10-21
Closed as completed in Release 3.
"""

FEATURE = """# Summary report handles every import
State: open
Labels: enhancement
Created: 2026-10-22
Part of #31. Planned, not yet built.
"""

ISSUES = {
    51: """# Retro: a thread cannot push outside its designated branch
State: open
Labels: retro
Created: 2026-10-26
Source thread: fixture-A
What went wrong: the thread was started on one designated branch and every push to any other branch, main included, was refused by the environment it ran in. The thread kept retrying, finished its work on a second branch and ended with the commits unpushed; that work was lost when the container was discarded.
Suggested fix: add a sentence to implement, implement-spec and release telling the thread to push only to its designated branch.
## Comments
None
""",
    52: """# Retro: push to a new branch refused, work lost
State: open
Labels: retro
Created: 2026-10-27
Scope: environment, the coding agent's sandbox refuses any push but the designated branch, in any repo run there.
Source thread: fixture-B
What went wrong: the thread created a feature branch, the push was refused, and the commits were lost when the session ended.
Suggested fix: warn threads in the skills that start work that only the designated branch can be pushed.
## Comments
None
""",
    53: """# Retro: Ticket template omits the Blocked by line
State: open
Labels: retro
Created: 2026-10-24
Scope: skill, the Ticket template the plugin ships has no Blocked by line, so any repo using it hits this.
Source thread: fixture-C
What went wrong: a Ticket written from the template named no blocker, and a build thread started it before its blocker had merged. The thread rebased twice; nothing was lost.
Suggested fix: add a Blocked by line to the Ticket template.
## Comments
Seen again in fixture-D: same template, same missing line; a short delay only.
""",
    54: """# Retro: reports in acme-app use the old date format
State: open
Labels: retro
Created: 2026-10-28
Scope: this repo, only acme-app's report generator formats dates this way; a fresh repo using the skills would not.
Source thread: fixture-E (project acme-app, whose tracker is other-project/issues/)
What went wrong: acme-app's own report code prints dates as dd/mm/yy, and a review missed it because acme-app's docs/acme-style.md does not name a date format.
Suggested fix: add the date format to acme-app's docs/acme-style.md.
## Comments
None
""",
}

PROMPT = """Release 3 has just ended. Run the Release-end retro-planning for this fixture repository; the release issue is issues/30.md. All issue state is in issues/, configured by docs/agents/issue-tracker.md, and the label strings are in docs/agents/triage-labels.md. The only other place you may write is another project's tracker, other-project/issues/, when a Retro belongs there. Use the skills in <checkout>/plugins/dev-skills/skills/ (load retro-planning from there; any other skill it names is in the same folder). Use only these local trackers; remote reads or writes are forbidden. Nobody is available to answer questions. Do not start `to-tickets`: file any Ticket yourself as the next unused issue file, labelled `ready-for-agent` (and `next-release` when it joins the next Release), naming the Retro issues it absorbs and its done condition, and comment `Absorbed by #<n>` on each issue it absorbs. Do not implement code.
"""

STATIC = {
    "docs/agents/issue-tracker.md": TRACKER,
    "docs/agents/triage-labels.md": LABELS,
    "docs/index.md": INDEX,
    "other-project/docs/agents/issue-tracker.md": OTHER_TRACKER,
    "issues/30.md": RELEASE,
    "issues/31.md": MILESTONE,
    "issues/32.md": DONE,
    "issues/33.md": FEATURE,
}
GUARDED = ("docs", "other-project/docs")
SEED_MAX = 54
SCOPES = {51: "environment", 52: "environment", 53: "skill", 54: "this repo"}


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
    (out / "other-project/issues").mkdir(parents=True, exist_ok=True)
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
    _, _, comments = text.partition("## Comments")
    return dict(
        text=text,
        state=state.group(1).lower() if state else "",
        labels={x.strip() for x in (labels.group(1) if labels else "").split(",") if x.strip()},
        comments=comments.strip(),
    )


def load(d):
    return {int(p.stem): parse(p) for p in pathlib.Path(d).glob("*.md") if p.stem.isdigit()}


def table_rows(text, n):
    """Table rows of the record that name issue #n."""
    return [l for l in text.splitlines() if l.startswith("|") and re.search(rf"#{n}\b", l)]


def score(out):
    """Return a list of (name, ok, seen)."""
    out = pathlib.Path(out)
    res = []

    def check(name, ok, seen=""):
        res.append((name, bool(ok), seen))

    with tempfile.TemporaryDirectory() as tmp:
        build(tmp)
        check("the fixture's docs are unchanged", tree_hash(out) == tree_hash(tmp))
    issues = load(out / "issues")
    new = {n: i for n, i in issues.items() if n > SEED_MAX}
    records = {n: i for n, i in new.items() if "retro-planning" in i["labels"]}
    tickets = {n: i for n, i in new.items() if "ready-for-agent" in i["labels"] and "retro-planning" not in i["labels"]}
    check("exactly one planning record, closed", len(records) == 1 and all(r["state"] == "closed" for r in records.values()),
          f"{[(n, r['state']) for n, r in records.items()]}")
    rec = next(iter(records.values()), None)
    text = rec["text"] if rec else ""

    # Scope in the record: each Retro has its own, #51 (no Scope line) included.
    for n, sc in SCOPES.items():
        rows = [r for r in table_rows(text, n) if {int(m) for m in re.findall(r"#(\d+)", r)} & set(SCOPES) == {n}]
        ok = any(re.search(rf"(?<![\w`]){re.escape(sc)}(?![\w`])|`{re.escape(sc)}`", r) for r in rows)
        wrong = [s for s in set(SCOPES.values()) - {sc} if any(re.search(rf"\b{re.escape(s)}\b", r) and not re.search(rf"\b{re.escape(sc)}\b", r) for r in rows)]
        check(f"the record gives #{n} the Scope {sc}", ok and not wrong, rows[:2])

    # Groups never mix Scopes.
    sec = re.search(r"^## Verdicts\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    verdict_rows = [l for l in (sec.group(1) if sec else "").splitlines() if l.startswith("|") and re.search(r"#\d+", l)]
    mixed = [l for l in verdict_rows if len({SCOPES[int(m)] for m in re.findall(r"#(\d+)", l) if int(m) in SCOPES}) > 1]
    check("no Verdicts row groups Retros of two Scopes", verdict_rows and not mixed, mixed[:1])

    # The environment group: one Ticket aimed at the Harness reference.
    check("exactly one new Ticket is filed, labelled ready-for-agent", len(tickets) == 1, f"{sorted(tickets)}")
    tn, t = next(iter(tickets.items()), (None, None))
    tt = t["text"] if t else ""
    check("the Ticket absorbs #51 and #52 and not #53 or #54",
          t and "#51" in tt and "#52" in tt and not re.search(r"#5[34]\b", tt))
    check("the Ticket joins the next Release: labelled next-release", t and "next-release" in t["labels"], t and sorted(t["labels"]))
    check("the Ticket aims the fix at the Harness reference (worker-control) and Startup verification",
          t and re.search(r"worker-control", tt) and re.search(r"(?i)startup verification", tt))
    check("the Ticket does not ask for a sentence in each skill",
          t and not re.search(r"(?i)\b(?:add|append|put|write)\b[^.\n]*\b(?:sentence|line|warning|reminder)\b[^.\n]*\b(?:each|every|all)\b[^.\n]*\bskills?\b", tt))
    for n in (51, 52):
        i = issues.get(n)
        check(f"#{n} carries an Absorbed by comment naming the Ticket", i and tn and re.search(rf"Absorbed by #{tn}\b", i["comments"]))

    # The skill group is a skill group, apart from the environment Ticket.
    i53 = issues.get(53)
    check("#53 (skill) is not closed as wontfix and not absorbed by the environment Ticket",
          i53 and "wontfix" not in i53["labels"] and not (tn and re.search(rf"Absorbed by #{tn}\b", i53["comments"])))

    # The misfiled #54 goes to its own project's tracker.
    other = load(pathlib.Path(out) / "other-project/issues")
    refiled = {n: i for n, i in other.items() if "retro" in i["labels"]}
    check("#54 is refiled in other-project/issues as a Retro with its suggested fix",
          len(refiled) == 1 and all("acme-style.md" in i["text"] and "needs-triage" not in i["labels"] for i in refiled.values()), sorted(other))
    i54 = issues.get(54)
    rn = next(iter(refiled), None)
    check("#54 is closed here with a comment linking the refiled issue",
          i54 and rn and i54["state"] == "closed" and re.search(rf"other-project/issues/{rn}(?:\.md)?\b", i54["comments"]), i54 and i54["comments"][:120])
    check("the record says #54 was refiled", rec and rn and any(re.search(rf"other-project/issues/{rn}\b|refil|moved|belongs", l, re.I) for l in table_rows(text, 54) + [l for l in text.splitlines() if "#54" in l]))
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
