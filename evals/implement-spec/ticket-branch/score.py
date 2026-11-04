#!/usr/bin/env python3
"""Score an implement-spec ticket-branch run: <out-dir>/repo/.scratch/answer.md.

Usage: score.py <out-dir>
Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any fails. It reads the answer's
decision, never the skill's text: the local Ticket branch holds a commit and Ticket 31 has not landed, so the run
reuses the branch (the worktree is made on it with no new branch), has the Spec tip merged in (not rebased), and
hands the Implementer what is done and open. In the `landed` scenario (fixture.json) the ticket's squash commit is on
the Spec branch, so the run discards the leftover branch and builds no worktree. Nothing in git may have changed.
"""
import json
import pathlib
import re
import subprocess
import sys


def field(text, name):
    m = re.search(rf"^{name}:[ \t]*(.*)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


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

    git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True).stdout.split()  # noqa: E731
    check("answer written", bool(text.strip()))
    check("dry run: branches and heads unchanged", git("branch", "--format=%(refname:short)") == fx["branches"]
          and git("rev-parse", "ticket-31") == [fx["ticket_branch"]] and git("rev-parse", "spec-30") == [fx["spec_branch"]])
    cmd, branch, tip, brief, cleanup = (field(text, n) for n in ("Command", "Branch", "Spec tip", "Brief", "Cleanup"))
    if fx.get("scenario") == "landed":
        check("decision: discard the leftover Ticket branch, never reuse it", branch.lower().startswith("discard"), branch)
        check("cleanup: deletes local ticket-31", re.search(r"git\b.*\bbranch\s+-D\b.*ticket-31", cleanup), cleanup)
        check("brief: none, or no Implementer is started", re.search(r"^none|no Implementer", brief, re.I), brief)
        check("command: no worktree built for the landed ticket", not re.search(r"worktree add", cmd), cmd)
        check("no push, reset or rebuild of the landed ticket", not re.search(r"push|reset|checkout|switch|-b\s", cmd + " " + cleanup + " "), cmd + " " + cleanup)
        print(f"{sum(results)}/{len(results)} checks passed")
        return all(results)
    cmd, branch, tip, brief = (field(text, n) for n in ("Command", "Branch", "Spec tip", "Brief"))
    check("cleanup: reuse deletes, resets and removes nothing", cleanup.strip("`' .").lower() in ("", "none")
          and not re.search(r"branch\s+-[dD]|worktree remove|reset", cleanup), cleanup)
    check("decision: reuse the existing Ticket branch", branch.lower().startswith("reuse"), branch)
    check("command: a worktree add naming ticket-31", re.search(r"git\b.*\bworktree add\b", cmd) and "ticket-31" in cmd, cmd)
    check("command: no new branch (-b or -B)", not re.search(r"\s-[bB]\s", cmd + " "), cmd)
    check("command: no delete, reset or push", not re.search(r"branch\s+-[dD]|reset|push|checkout|switch", cmd), cmd)
    check("Spec tip: merged in, never rebased", re.search(r"merg", tip, re.I) and not re.search(
        r"(?<!never a )(?<!never )(?<!not a )(?<!not )(?<!no )(?<!n't )(?<!rather than a )(?<!rather than )(?<!instead of )(?<!instead of a )rebas", tip, re.I), tip)
    check("brief: a handoff of what is done and open", re.search(r"done|committed|already|first pass|open|left|remain", brief, re.I) and len(brief) > 20, brief)
    check("brief: evidence and the ticket check still required, nothing trusted unchecked",
          re.search(r"evidence|ticket check|not trusted|unchecked|re-?check", brief, re.I), brief)
    print(f"{sum(results)}/{len(results)} checks passed")
    return all(results)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: score.py <out-dir>")
    sys.exit(0 if score(sys.argv[1]) else 1)
