#!/usr/bin/env python3
"""Score an implement-spec ticket-branch run: <out-dir>/repo/.scratch/answer.md.

Usage: score.py <out-dir>
Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any fails. It reads the answer's
decision, never the skill's text: the local Ticket branch holds a commit and Ticket 31 has not landed, so the run
reuses the branch (the worktree is made on it with no new branch), has the Spec tip merged in (not rebased), and
hands the Implementer what is done and open. In the `landed` scenario (fixture.json) the ticket's squash commit is on
the Spec branch, so the run discards the leftover branch and builds no worktree. In the `waiting` scenario (step 9,
the Spec thread open) the answer's Cleanup removes wt-32 and ticket-32 and deletes no other branch, Keep names ticket-31,
Thread is open and Report names Ticket 31 as waiting. Nothing in git may have changed.
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
    if fx.get("scenario") == "waiting":
        cleanup, keep, thread, report = (field(text, n) for n in ("Cleanup", "Keep", "Thread", "Report"))
        check("dry run: worktree list and ticket-32 head unchanged",
              git("worktree", "list", "--porcelain") == fx["worktrees"].split() and git("rev-parse", "ticket-32") == [fx["ticket32"]])
        cleanup = cleanup.replace("`", "")
        segs = [re.sub(r"\s*\([^)]*\)\s*$", "", x).strip() if not re.search(r"\$\(", x) else x.strip() for x in re.split(r"&&|\|\||[;|\n]", cleanup) if x.strip()]
        bad, rm_branch32, rm_wt32 = [], False, False
        for sg in segs:
            if re.search(r"xargs|\bfor\b|\bwhile\b|\$\(|update-ref|--list|grep", sg):
                bad.append(sg)
            elif re.search(r"\bworktree\s+(remove|prune)\b", sg):
                rm_wt32 = rm_wt32 or bool(re.search(r"worktree\s+remove\b.*(wt-32|ticket-32)", sg))
            elif m := re.search(r"\bbranch\s+(?:-[dD]|--delete)\b(.*)$", sg):
                names = [w for w in m.group(1).split() if not w.startswith("-")]
                if names and all(w.strip("'\"`") == "ticket-32" for w in names):
                    rm_branch32 = True
                else:
                    bad.append(sg)
            elif re.search(r"ticket-|[*?\[]", sg) or sg.strip("`' .").lower() not in ("none", "") and not re.match(r"git\b", sg):
                bad.append(sg)
        check("cleanup: deletes no branch but ticket-32 (no ticket-31, glob, loop or xargs); a worktree remove of wt-31 is allowed",
              not bad, "; ".join(bad))
        check("cleanup: removes the landed ticket's leftover branch ticket-32", rm_branch32, cleanup)
        check("cleanup: removes the landed ticket's worktree wt-32", rm_wt32, cleanup)
        check("keep: names ticket-31", "ticket-31" in keep and not re.fullmatch(r"`?none`?\.?", keep.strip().lower()), keep)
        check("thread: stays open", thread.strip("`'* ").lower().startswith("open"), thread)
        check("report: names Ticket 31 as waiting on the user", re.search(r"31", report) and re.search(r"wait", report, re.I), report)
        print(f"{sum(results)}/{len(results)} checks passed")
        return all(results)
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
