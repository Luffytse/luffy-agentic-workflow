#!/usr/bin/env python3
"""Build the ticket-branch case of the implement-spec eval, outside this repo.

Usage: make_fixture.py <out-dir> [reuse|landed]
Makes <out-dir>/repo (a git repo with a bare `origin`: `main`, the pushed Spec branch `spec-30` holding Ticket 32's
squash commit, and a LOCAL branch `ticket-31` that a dead thread's Implementer left with one commit, never pushed),
<out-dir>/PROMPT.md and <out-dir>/fixture.json (what score.py compares against). Scenario `reuse` (default): Ticket 31 has not landed.
Scenario `landed`: spec-30 also holds Ticket 31's squash commit (it landed; the thread died before deleting the
local branch). The decision is step 3.1 on re-entry. See README.md.
"""
import json
import pathlib
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def prompt(repo, scenario="reuse"):
    task = ("Do step 3.1 for Ticket 31 only." if scenario == "reuse" else
            "Decide what to do for Ticket 31, starting at step 3.1, and for the leftovers of the dead thread.")
    state = ("Ticket 31 is the next frontier ticket and a slot is free." if scenario == "reuse" else
             "The tracker shows Ticket 31 open and a slot is free.")
    return f"""# Scripted prompt: implement-spec, ticket-branch case

Give the text between the lines to a fresh subagent at the regular tier, with its working directory at `{repo}`.
Give it the whole `implement-spec` folder from the checkout under test (the branch's, then main's from a
`git archive`), nothing else from this folder. Keep `score.py` and `test_cases.py` away from it.

---

You are the Spec thread for Spec 30 (`.scratch/issues/30-spec.md`), following `implement-spec` (its files are in the
folder you were given). The thread that was running this Spec died and you are re-entering it: you now own the Spec,
and the machine survived. The Spec branch `spec-30` is on `origin`. {state} {task} Run only read-only git commands (log, diff, show, branch, worktree list,
rev-parse) and change nothing: no branch, worktree, file or commit.

Write `.scratch/answer.md` with exactly these lines:

    Observed: <what you found about the Ticket branch, in one line>
    Command: <the one git command you would run to make Ticket 31's worktree at /tmp/wt-31, or `none`>
    Cleanup: <the git command that removes a leftover local branch or worktree, or `none`>
    Branch: <reuse | discard | fresh>
    Spec tip: <how the Implementer gets the Spec branch tip into the Ticket branch, or `none`>
    Brief: <the first lines you would put in the Implementer's brief>

---
"""


def build(out, scenario="reuse"):
    if scenario not in ("reuse", "landed"):
        sys.exit("scenario is reuse or landed")
    out = pathlib.Path(out).resolve()
    if out.exists():
        sys.exit(f"{out} exists")
    r = out / "repo"
    r.mkdir(parents=True)
    git(out, "init", "-q", "--bare", "-b", "main", "origin.git")
    git(r, "init", "-q", "-b", "main")
    git(r, "remote", "add", "origin", str(out / "origin.git"))
    write(r / "CLAUDE.md", "# greeter\n\nA tiny shell greeter. Run `bash test.sh` before each push.\n")
    write(r / "src/greet.sh", '#!/usr/bin/env bash\necho "Hello, ${1:-world}!"\n')
    write(r / ".scratch/issues/30-spec.md", "Title: Greeter commands\nType: spec\nLabels: enhancement\nStatus: open\n\nAdd commands to the greeter.\n")
    write(r / ".scratch/issues/31-bye.md", "Title: Add a bye command\nType: ticket\nLabels: enhancement\nStatus: open\n\nParent: #30\n\nAdd `greet.sh bye <name>`.\n")
    write(r / ".scratch/issues/32-shout.md", "Title: Add a shout command\nType: ticket\nLabels: enhancement\nStatus: open\n\nParent: #30\n\nAdd `greet.sh shout <name>`.\n")
    write(r / ".gitignore", ".scratch/answer.md\n")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "chore: fixture")
    git(r, "checkout", "-q", "-b", "spec-30")
    write(r / "src/shout.sh", '#!/usr/bin/env bash\necho "HELLO, ${1:-world}!"\n')
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "feat: add a shout command\n\nTicket #32.")
    if scenario == "landed":
        write(r / "src/bye.sh", '#!/usr/bin/env bash\necho "Goodbye, ${1:-world}!"\n')
        git(r, "add", "-A")
        git(r, "commit", "-q", "-m", "feat: add a bye command\n\nTicket #31.")
    git(r, "push", "-q", "origin", "main", "spec-30")
    git(r, "checkout", "-q", "-b", "ticket-31", "main")
    write(r / "src/bye.sh", '#!/usr/bin/env bash\necho "Goodbye, ${1:-world}!"\n')
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "wip: bye command, first pass\n\nTicket #31.")
    git(r, "checkout", "-q", "spec-30")
    (out / "PROMPT.md").write_text(prompt(r, scenario))
    fx = dict(scenario=scenario, ticket_branch=git(r, "rev-parse", "ticket-31"), spec_branch=git(r, "rev-parse", "spec-30"),
              main=git(r, "rev-parse", "main"), branches=git(r, "branch", "--format=%(refname:short)").split())
    (out / "fixture.json").write_text(json.dumps(fx, indent=2) + "\n")
    return out


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: make_fixture.py <out-dir> [reuse|landed]")
    print(build(sys.argv[1], *sys.argv[2:]))
