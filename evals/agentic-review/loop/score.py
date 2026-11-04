#!/usr/bin/env python3
"""Score a run of a loop fixture from what it left in the repo: the pull request's comments, the issues and the branch.

Usage: score.py <merge|after-round3|after-round3-labels|empty-round> <out-dir>   (the directory make-fixture.sh built, after the run)
Prints one line per check and exits 1 if any fails. It reads files only; it judges outcomes, never wording.
"""
import re
import subprocess
import sys
from pathlib import Path

case, out = sys.argv[1], Path(sys.argv[2])
repo = out / "repo"
pulls = repo / ".scratch" / "pulls" / "1"
issues = repo / ".scratch" / "issues"
fails = 0


def check(name, ok):
    global fails
    print(("ok: " if ok else "FAIL: ") + name)
    fails += 0 if ok else 1


def git(*args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


def comments(kind_round):
    """The pull request comments whose marker is `kind=round round=<n>`."""
    found = []
    for f in sorted(pulls.glob("*.md")):
        first = f.read_text().splitlines()[0] if f.read_text() else ""
        if re.match(rf"<!-- code-review kind=round round={kind_round} ", first):
            found.append(f)
    return found


def marker(text, field):
    m = re.search(rf"\b{field}=(\S+)", text.splitlines()[0])
    return m.group(1) if m else None


def rows(text):
    """Table rows as dicts keyed by the header cells."""
    lines = [l for l in text.splitlines() if l.startswith("|")]
    if len(lines) < 2:
        return []
    head = [c.strip() for c in lines[0].strip("|").split("|")]
    return [dict(zip(head, [c.strip() for c in l.strip("|").split("|")])) for l in lines[2:]]


def line_of(rev, path, needle):
    for n, l in enumerate(git("show", f"{rev}:{path}").splitlines(), 1):
        if needle in l:
            return n
    raise SystemExit(f"{needle!r} not in {rev}:{path}")


def covers(locations, path, line):
    for loc in re.split(r",\s*", locations):
        m = re.fullmatch(r"`?([^:`]+):(\d+)(?:-(\d+))?`?", loc.strip())
        if m and m.group(1) == path and int(m.group(2)) <= line <= int(m.group(3) or m.group(2)):
            return True
    return False


if case == "merge":
    head = git("rev-parse", "quota")
    r1 = marker((pulls / "01-round-1.md").read_text(), "head")
    found = comments(2)
    check("exactly one Round 2 comment was posted", len(found) == 1)
    check("no Round 3 comment was posted", not comments(3))
    if len(found) == 1:
        text = found[0].read_text()
        check("Round 2's head is the merge at the branch head", marker(text, "head") == head)
        check("Round 2 reviewed from Round 1's head", marker(text, "base") == r1)
        reviewed = next((l for l in text.splitlines() if l.startswith("Reviewed:")), "")
        check("Round 2 says it reviewed the new commits, not the whole pull request",
              "new commits" in reviewed and "whole pull request" not in reviewed)
        finders = next((l for l in text.splitlines() if l.startswith("Finders:")), "")
        check("Round 2 ran one Finder, no adversarial one", finders != "" and "adversarial" not in finders
              and "," not in finders)
        rs = rows(text)
        by_id = {r.get("id"): r for r in rs}
        check("R1-1 is fixed", by_id.get("R1-1", {}).get("Status") == "fixed")
        bad = line_of(head, "app/quota.py", "max(0, used - limit)")
        check("an open Important sits on the merge's resolution line",
              any(r.get("Severity") == "Important" and r.get("Status") == "open"
                  and covers(r.get("Locations", ""), "app/quota.py", bad) for r in rs))
        check("nothing main brought in is reported",
              not any("report.py" in r.get("Locations", "") or "usage_percent" in r.get("Claim", "") for r in rs))
        check("Result counts the open Important", re.search(r"^Result: not clean, [1-9]\d* Important open$", text, re.M)
              is not None)
elif case == "empty-round":
    head = git("rev-parse", "quota")
    r1 = marker((pulls / "01-round-1.md").read_text(), "head")
    found = comments(2)
    check("exactly one Round 2 comment was posted", len(found) == 1)
    check("no Round 3 comment was posted", not comments(3))
    if len(found) == 1:
        text = found[0].read_text()
        check("Round 2's head is the merge at the branch head", marker(text, "head") == head)
        check("Round 2 reviewed from Round 1's head", marker(text, "base") == r1)
        reviewed = next((l for l in text.splitlines() if l.startswith("Reviewed:")), "")
        check("Round 2 says it reviewed the new commits, not the whole pull request",
              "new commits" in reviewed and "whole pull request" not in reviewed)
        finders = next((l for l in text.splitlines() if l.startswith("Finders:")), "")
        check("Round 2 ran one Finder, no adversarial one", finders != "" and "adversarial" not in finders
              and "," not in finders)
        verifier = next((l for l in text.splitlines() if l.startswith("Verifier:")), "")
        check("the Round comment says no candidates went to a Verifier", re.match(r"Verifier: none\b", verifier) is not None)
        check("the table has no rows", rows(text) == [])
        check("Result is clean", re.search(r"^Result: clean$", text, re.M) is not None)
elif case in ("after-round3", "after-round3-labels"):
    head = git("rev-parse", "fix")
    c3 = (pulls / "03-round-3.md").read_text()
    check("Round 3's head is still the branch head (nothing new committed or reviewed)", marker(c3, "head") == head)
    check("no Round 4 comment was posted", not comments(4))
    new = [f for f in sorted(issues.glob("*.md")) if not f.name.startswith("01-")]
    check("exactly one issue was created", len(new) == 1)
    bad = line_of(head, "app/quota.py", "return limit + burst - used")
    if len(new) == 1:
        body = new[0].read_text()
        labels = next((l for l in body.splitlines() if l.startswith("Labels:")), "")
        check("the issue carries the bug and ready-for-agent labels", "bug" in labels and "ready-for-agent" in labels)
        have = {x.strip() for x in labels.partition(":")[2].split(",") if x.strip()}
        # With a Repo labels table the bug is server code, so it carries backend and not frontend; with no table, no repo label.
        want = {"bug", "ready-for-agent", "backend"} if case == "after-round3-labels" else {"bug", "ready-for-agent"}
        check("the issue carries the repo labels that fit and no other label" if case == "after-round3-labels"
              else "the issue carries no label beyond bug and ready-for-agent (no Repo labels table)", have == want)
        check("the issue names R3-1's location", re.search(rf"app/quota\.py:{bad}\b", body) is not None)
        check("the issue links the pull request", ".scratch/pulls/1" in body or "pull request 1" in body.lower())
        check("the issue is not about the Nit", "mysterious name" not in body and "`n`" not in body)
        r31 = {r.get("id"): r for r in rows(c3)}.get("R3-1", {})
        check("Round 3's R3-1 row notes the bug Ticket by its link",
              "bug Ticket" in r31.get("Note", "") and new[0].name in r31.get("Note", ""))
    check("Round 3's Result says it was sorted",
          re.search(r"^Result: sorted after Round 3: 1 bug Tickets?, 0 dismissed$", c3, re.M) is not None)
else:
    raise SystemExit("usage: score.py <merge|after-round3|after-round3-labels|empty-round> <out-dir>")

print("PASS" if fails == 0 else f"{fails} check(s) failed")
sys.exit(1 if fails else 0)
