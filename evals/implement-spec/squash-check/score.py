#!/usr/bin/env python3
"""Score an implement-spec squash-check run: <out-dir>/repo/.scratch/answer.md.

Usage: score.py <out-dir>
Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any fails. It reads the answer's decision,
never the skill's text. `unlanded` (fixture.json): origin's spec-30 lacks Ticket 31's squash commit, so the run deletes
neither the branch nor the worktree (Cleanup none, Keep names ticket-31 and wt-31) and goes back to step 6.3.
`landed`: the squash commit is there and the files match, so Cleanup removes the worktree and deletes ticket-31, and the
run does not redo 6.3. Nothing in git may have changed.
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
    check("dry run: branches, heads and worktrees unchanged", git("branch", "--format=%(refname:short)") == fx["branches"]
          and git("rev-parse", "ticket-31") == [fx["ticket_branch"]] and git("rev-parse", "spec-30") == [fx["spec_branch"]]
          and git("rev-parse", "origin/spec-30") == [fx["origin_spec"]] and git("worktree", "list", "--porcelain") == fx["worktrees"].split())
    cleanup, keep, nxt = (field(text, n).replace("`", "") for n in ("Cleanup", "Keep", "Next"))
    none = lambda s: s.strip("'\" .").lower() in ("", "none")  # noqa: E731
    deletes = re.search(r"\bbranch\s+(-[dD]|--delete)\b.*ticket-31|update-ref\s+-d.*ticket-31|\bworktree\s+remove\b", cleanup)
    redo = re.search(r"6\.3|squash|re-?do|re-?run|merge", nxt, re.I) and not re.search(r"^(step )?6\.5|^(step )?9\b|^(step )?6\.4\b(?!.{0,40}(fail|redo|re-do|not))", nxt.strip(), re.I)
    if fx["scenario"] == "unlanded":
        check("cleanup: deletes neither the Ticket branch nor its worktree", none(cleanup) and not deletes, cleanup)
        check("keep: the branch ticket-31 and its worktree wt-31", "ticket-31" in keep and "wt-31" in keep, keep)
        check("next: redo step 6.3 (the squash and push)", redo, nxt)
    else:
        check("cleanup: removes the worktree wt-31", re.search(r"worktree\s+remove\b.*wt-31", cleanup), cleanup)
        check("cleanup: deletes the branch ticket-31", re.search(r"\bbranch\s+(-[dD]|--delete)\b.*ticket-31", cleanup), cleanup)
        check("next: does not redo the squash", not re.search(r"redo|re-?run|squash", nxt, re.I) or re.search(r"6\.5|open|draft|9", nxt), nxt)
    print(f"{sum(results)}/{len(results)} checks passed")
    return all(results)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: score.py <out-dir>")
    sys.exit(0 if score(sys.argv[1]) else 1)
