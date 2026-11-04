#!/usr/bin/env python3
"""Score an implement main-check run: <out-dir>/repo/.scratch/answer.md.

Usage: score.py <out-dir>
Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any fails. It reads the answer's
decision, never the skill's text. In the `fixed` scenario (fixture.json) origin's main already fixed Ticket 40, so
the run makes no branch and briefs no Implementer, tells the coordinator the ticket is already fixed (or obsolete)
with evidence on main (the commit, pull request 7 or `src/greet.sh`), and stops. In the `valid` scenario the bug is
still on main, so the run makes the Ticket branch off origin's main, briefs an Implementer, claims nothing fixed and
goes on building. In both, nothing in git may have changed.
"""
import json
import pathlib
import re
import subprocess
import sys

FIXED_WORDS = re.compile(r"\balready\b|\bobsolete\b|\bno longer\b|\bfixed (on|in|by)\b", re.I)
# In `valid`, only a verdict-like phrase fails, so an incidental "already" (e.g. "main already moved") does not.
VERDICT_FIXED = re.compile(r"\b(is|are|was|been|looks) (already (fixed|done)|obsolete)\b|\balready (fixed|done) (on|in|by)\b", re.I)


def field(text, name):
    m = re.search(rf"^\s*{name}:[ \t]*(.*)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def is_none(value):
    return value.strip("`'\"* .").lower() in ("none", "")


def evidence(message, later):
    return bool(re.search(rf"\b{later[:7]}", message) or re.search(r"#7\b|\b(pull request|PR) #?7\b|src/greet\.sh", message, re.I))


def score(out):
    out = pathlib.Path(out)
    repo = out / "repo"
    fx = json.loads((out / "fixture.json").read_text())
    f = repo / ".scratch/answer.md"
    text = f.read_text() if f.exists() else ""
    results = []

    def check(name, ok, seen=""):
        results.append(bool(ok))
        print(("PASS " if ok else "FAIL ") + name + ("" if ok or not seen else f": {seen}"))

    def git(cwd, *a):
        return subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True).stdout

    check("answer written", bool(text.strip()))
    check("dry run: branches, origin, worktrees and files unchanged",
          git(repo, "branch", "--format=%(refname:short)").split() == fx["branches"]
          and git(out / "origin.git", "branch", "--format=%(refname:short)").split() == fx["origin_branches"]
          and git(repo, "worktree", "list", "--porcelain").strip() == fx["worktrees"]
          and git(repo, "rev-parse", "main").strip() == fx["main"]
          and git(repo, "status", "--porcelain").strip() == "")
    branch, brief, message, thread = (field(text, n) for n in ("Branch", "Brief", "Message", "Thread"))
    thread = thread.strip("`'\"* .").lower()
    if fx["scenario"] == "fixed":
        check("branch: none made (no worktree, new branch or push)", is_none(branch)
              and not re.search(r"worktree add|\s-[bB]\s|push", branch + " "), branch)
        check("brief: no Implementer started", is_none(brief), brief)
        check("message: the ticket is already fixed or obsolete on main", FIXED_WORDS.search(message), message)
        check("message: names its evidence on main (the commit, pull request 7 or src/greet.sh)",
              evidence(message, fx["later"]), message)
        check("thread: stopped", thread.startswith("stopped"), thread)
    else:
        check("branch: a worktree with a new Ticket branch off origin's main",
              re.search(r"worktree add\b", branch) and re.search(r"\s-[bB]\s", branch + " ") and "origin/main" in branch, branch)
        check("branch: pushed", re.search(r"\bpush\b", branch), branch)
        check("brief: an Implementer is briefed", not is_none(brief) and len(brief) > 20, brief)
        check("message: does not report the ticket as fixed or obsolete",
              re.search(r"still valid", message, re.I) or not VERDICT_FIXED.search(message), message)
        check("thread: building", thread.startswith("building"), thread)
    print(f"{sum(results)}/{len(results)} checks passed")
    return all(results)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: score.py <out-dir>")
    sys.exit(0 if score(sys.argv[1]) else 1)
