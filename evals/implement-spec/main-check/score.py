#!/usr/bin/env python3
"""Score an implement-spec main-check run: <out-dir>/repo/.scratch/answer.md.

Usage: score.py <out-dir>
Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any fails. It reads the answer's
decision, never the skill's text. `fixed` (fixture.json): origin's main already has both tickets' work, so the Spec
thread makes no Spec branch or worktree, starts no Implementer, tells the coordinator the Spec is already fixed (or
obsolete) with evidence on main (the commit, pull request 9, `src/bye.sh` or `src/shout.sh`) and stops. `valid`: the
work is not on main, so it makes and pushes the Spec branch, makes worktrees for tickets 51 and 52, starts Implementers
on both, claims nothing fixed and builds. `worker`: a Worker handed Ticket 51, whose work is on main, makes nothing,
tells the coordinator with the same kind of evidence, also tells the Spec's owner (`spec-thread-50`), and stops.
Nothing in git may have changed.
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


def evidence(message, later, files):
    return bool(re.search(rf"\b{later[:7]}", message) or re.search(r"#9\b|\b(pull request|PR) #?9\b", message, re.I)
                or any(f in message for f in files))


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
    spec, wts, impl, message, others, thread = (field(text, n) for n in
                                                ("Spec branch", "Worktrees", "Implementers", "Message", "Others", "Thread"))
    thread = thread.strip("`'\"* .").lower()
    scenario = fx["scenario"]
    if scenario in ("fixed", "worker"):
        files = ["src/bye.sh", "src/shout.sh"] if scenario == "fixed" else ["src/bye.sh"]
        what = "Spec" if scenario == "fixed" else "ticket 51"
        check("spec branch: none made or pushed", is_none(spec) and not re.search(r"push|-b\s|checkout|switch", spec + " "), spec)
        check("worktrees: none made", is_none(wts) and "worktree add" not in wts, wts)
        check("implementers: none started", is_none(impl), impl)
        check(f"message: the {what} is already fixed or obsolete on main", FIXED_WORDS.search(message), message)
        check(f"message: names its evidence on main (the commit, pull request 9 or {' or '.join(files)})",
              evidence(message, fx["later"], files), message)
        if scenario == "worker":
            check("others: the Spec's owner spec-thread-50 is told", re.search(r"spec-thread-50|\bowner\b", others, re.I)
                  and not is_none(others), others)
            check("others: the owner hears the ticket is already fixed or obsolete", FIXED_WORDS.search(others), others)
        check("thread: stopped", thread.startswith("stopped"), thread)
    else:
        check("spec branch: made and pushed", re.search(r"\bpush\b", spec) and re.search(r"-b\s|-c\s|\bbranch\b", spec + " "), spec)
        check("worktrees: one per frontier ticket, 51 and 52", "worktree add" in wts and "51" in wts and "52" in wts, wts)
        check("implementers: started on 51 and 52", "51" in impl and "52" in impl, impl)
        check("message: does not report the Spec as fixed or obsolete",
              re.search(r"still valid", message, re.I) or not VERDICT_FIXED.search(message), message)
        check("thread: building", thread.startswith("building"), thread)
    print(f"{sum(results)}/{len(results)} checks passed")
    return all(results)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: score.py <out-dir>")
    sys.exit(0 if score(sys.argv[1]) else 1)
