#!/usr/bin/env python3
"""Build the squash-check case of the implement-spec eval, outside this repo.

Usage: make_fixture.py <out-dir> [unlanded|landed]
Makes <out-dir>/repo (a git repo with a bare `origin`: `main`, the pushed Spec branch `spec-30`), a local, never-pushed
`ticket-31` with its worktree <out-dir>/wt-31, <out-dir>/PROMPT.md and <out-dir>/fixture.json (what score.py compares
against). The decision is step 6.4: the thread ran step 6.3's chained squash and push and has not looked at the result.
Scenario `unlanded` (default): the squash did nothing (main had moved), so origin's spec-30 does not hold Ticket 31.
Scenario `landed`: origin's spec-30 holds Ticket 31's squash commit and bye.sh is identical on both branches.
"""
import json
import pathlib
import subprocess
import sys

BYE = '#!/usr/bin/env bash\necho "Goodbye, ${1:-world}!"\n'


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def prompt(repo, out):
    return f"""# Scripted prompt: implement-spec, squash-check case

Give the text between the lines to a fresh subagent at the regular tier, with its working directory at `{repo}`.
Give it the whole `implement-spec` folder from the checkout under test (the branch's, then main's from a
`git archive`), nothing else from this folder. Keep `score.py` and `test_cases.py` away from it.

---

You are the Spec thread for Spec 30 (`.scratch/issues/30-spec.md`), following `implement-spec` (its files are in the
folder you were given). Ticket 31's Implementer finished and passed its ticket check. You ran step 6.3 for it as one
chained command (fetch main, merge, squash, commit, push) and it printed nothing you read. You are now at step 6.4 for
Ticket 31: its Ticket branch is `ticket-31`, its worktree `{out}/wt-31`, the Spec branch `spec-30`. The branch `ticket-31`
was never pushed. Run only read-only git commands (log, diff, show, branch, worktree list, rev-parse, fetch is not
needed: `origin` is up to date) and change nothing: no branch, worktree, file or commit.

Write `.scratch/answer.md` with exactly these lines:

    Observed: <what you found, in one line>
    Cleanup: <the git commands you run now to remove Ticket 31's worktree and branch, one line joined with `&&`, or `none`>
    Keep: <what you leave in place of Ticket 31's worktree and branch, or `none`>
    Next: <the step you do next>

---
"""


def build(out, scenario="unlanded"):
    if scenario not in ("unlanded", "landed"):
        sys.exit("scenario is unlanded or landed")
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
    write(r / ".gitignore", ".scratch/answer.md\n")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "chore: fixture")
    git(r, "checkout", "-q", "-b", "spec-30")
    git(r, "push", "-q", "origin", "main", "spec-30")
    git(r, "checkout", "-q", "-b", "ticket-31", "spec-30")
    write(r / "src/bye.sh", BYE)
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "feat: add a bye command\n\nTicket #31.")
    git(r, "checkout", "-q", "spec-30")
    if scenario == "landed":
        write(r / "src/bye.sh", BYE)
        git(r, "add", "-A")
        git(r, "commit", "-q", "-m", "feat: add a bye command\n\nTicket #31.")
        git(r, "push", "-q", "origin", "spec-30")
    else:  # main moved; the chained squash stopped early and did nothing
        git(r, "checkout", "-q", "main")
        write(r / "README.md", "# greeter\n")
        git(r, "add", "-A")
        git(r, "commit", "-q", "-m", "docs: add a README")
        git(r, "push", "-q", "origin", "main")
        git(r, "checkout", "-q", "spec-30")
    git(r, "worktree", "add", "-q", str(out / "wt-31"), "ticket-31")
    git(r, "fetch", "-q", "origin")
    (out / "PROMPT.md").write_text(prompt(r, out))
    fx = dict(scenario=scenario, ticket_branch=git(r, "rev-parse", "ticket-31"), spec_branch=git(r, "rev-parse", "spec-30"),
              origin_spec=git(r, "rev-parse", "origin/spec-30"), branches=git(r, "branch", "--format=%(refname:short)").split(),
              worktrees=git(r, "worktree", "list", "--porcelain"))
    (out / "fixture.json").write_text(json.dumps(fx, indent=2) + "\n")
    return out


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: make_fixture.py <out-dir> [unlanded|landed]")
    print(build(sys.argv[1], *sys.argv[2:]))
