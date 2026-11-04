#!/usr/bin/env python3
"""Build the main-check case of the implement-spec eval, outside this repo.

Usage: make_fixture.py <out-dir> [fixed|valid|worker]
Makes <out-dir>/origin.git (a bare origin), <out-dir>/repo (a clone whose local `main` is one commit behind origin's,
so only a fetch shows what merged since the Spec was written), <out-dir>/PROMPT.md and <out-dir>/fixture.json (what
score.py compares against). Spec 50 "Greeter commands" (written 2026-10-02) has two unblocked tickets: 51 adds
`src/bye.sh`, 52 adds `src/shout.sh`. The tracker is local Markdown files under `.scratch/`, not in git.
Scenario `fixed` (default): a later commit on origin's main, pull request 9 (someone else's, closing no issue), added
both commands with their tests in `test.sh`, so the Spec is already fixed on main; there is no Spec branch yet. Scenario `valid`: the later commit
only edits the README; there is no Spec branch yet. Scenario `worker`: the Spec is owned by another thread
(`spec-thread-50`, its owner record on the Spec), the Spec branch `spec-50` is pushed, and the run is a Worker the
coordinator handed Ticket 51; pull request 9 added only `src/bye.sh` and its test, so Ticket 51 is already fixed on main.
See README.md.
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys

TRACKER = """# Issue tracker

Issues and pull requests are local Markdown files; there is no forge and no CI.

- An issue is `.scratch/issues/<n>-<slug>.md` with `Title:`, `Type:` (ticket or spec), `Labels:`, `Status:` (open or
  closed), `Created:`, `Parent:` (a ticket's Spec) and `Blocked by:` lines, then its body. Comments go under a
  `## Comments` heading at its end.
- A pull request is `.scratch/pulls/<n>-<slug>.md` with `Title:`, `Status:` (open or merged), `Merged:`, `Commit:` and
  `Closes:` lines.
- **Count open blockers**: the issues on the `Blocked by:` line whose `Status:` is open. `none` is zero.
- **Park**: an issue is parked when its `Labels:` line holds `parked`.
- There are no agent-only labels.
- The coordinator (a team lead) runs this project's threads; you reach it, and any other thread, only by message.
"""
BYE = '#!/usr/bin/env bash\necho "Goodbye, ${1:-world}!"\n'
SHOUT = '#!/usr/bin/env bash\necho "HELLO, ${1:-world}!"\n'
TESTS = dict(base='[ "$(bash src/greet.sh Ann)" = "Hello, Ann!" ]\n',
             bye='[ "$(bash src/bye.sh Ann)" = "Goodbye, Ann!" ]\n',
             shout='[ "$(bash src/shout.sh Ann)" = "HELLO, Ann!" ]\n')


def test_sh(*names):
    return '#!/usr/bin/env bash\nset -e\n' + ''.join(TESTS[n] for n in ('base', *names))


def git(cwd, *args, date=None):
    env = dict(os.environ)
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    return subprocess.run(["git", "-C", str(cwd), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                          check=True, capture_output=True, text=True, env=env).stdout.strip()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def prompt(repo, scenario):
    if scenario == "worker":
        who = ("The coordinator started you as a Worker on Ticket 51 (`.scratch/issues/51-bye.md`) under Spec 50: you "
               "build that one ticket for the Spec's owner, the thread named in the owner record on the Spec. Work up "
               "to the point where you would start that ticket's Implementer")
    else:
        who = ("You are the Spec thread for Spec 50 (`.scratch/issues/50-spec.md`). This is your first entry. Work from "
               "step 1 up to the point where you would start the first Implementer")
    return f"""# Scripted prompt: implement-spec, main-check case, scenario {scenario}

Give the text between the lines to a fresh subagent at the regular tier, with its working directory at `{repo}`.
Give it the whole `implement-spec` folder from the checkout under test (the branch's, then main's from a
`git archive`), nothing else from this folder. Keep `score.py`, `test_cases.py` and `fixture.json` away from it.

---

{who}, following `implement-spec` (its files are in the folder you were given), and stop there: start no subagent.
The tracker doc is `docs/dev-skills/issue-tracker.md`. A coordinator runs this project; you reach it, and any other
thread, only by the messages you write below. Run only read-only commands (reading files; git fetch, log, diff, show,
branch, worktree list, rev-parse) and change nothing: no branch, worktree, push, file, comment or commit. Write each
command you would run instead.

Write `.scratch/answer.md` with exactly these lines:

    Title: <the title of the Spec, or of the ticket you were handed>
    Spec branch: <the git commands that make and push the Spec branch, one line joined with `&&`, or `none`>
    Worktrees: <the git commands that make Ticket worktrees, one line joined with `&&`, or `none`>
    Implementers: <the ticket numbers you start Implementers on, or `none`>
    Message: <what you tell the coordinator now, in one line, or `none`>
    Others: <what you tell any other thread now, naming it, in one line, or `none`>
    Thread: <building | waiting | stopped>

---
"""


def build(out, scenario="fixed"):
    if scenario not in ("fixed", "valid", "worker"):
        sys.exit("scenario is fixed, valid or worker")
    out = pathlib.Path(out).resolve()
    if out.exists():
        sys.exit(f"{out} exists")
    out.mkdir(parents=True)
    git(out, "init", "-q", "--bare", "-b", "main", "origin.git")
    seed = out / "seed"
    git(out, "init", "-q", "-b", "main", "seed")
    git(seed, "remote", "add", "origin", str(out / "origin.git"))
    write(seed / "CLAUDE.md", "# greeter\n\nA tiny shell greeter. Run `bash test.sh` before each push.\n")
    write(seed / "README.md", "# greeter\n\n`src/greet.sh <name>` greets someone.\n")
    write(seed / "src/greet.sh", '#!/usr/bin/env bash\necho "Hello, ${1:-world}!"\n')
    write(seed / "test.sh", '#!/usr/bin/env bash\n[ "$(bash src/greet.sh Ann)" = "Hello, Ann!" ]\n')
    write(seed / "docs/dev-skills/issue-tracker.md", TRACKER)
    write(seed / ".gitignore", ".scratch/\n")
    git(seed, "add", "-A")
    git(seed, "commit", "-q", "-m", "chore: greeter", date="2026-10-01T10:00:00Z")
    git(seed, "push", "-q", "origin", "main")
    if scenario == "worker":
        git(seed, "checkout", "-q", "-b", "spec-50")
        git(seed, "commit", "-q", "--allow-empty", "-m", "chore: start the Spec branch for #50", date="2026-10-03T10:00:00Z")
        git(seed, "push", "-q", "origin", "spec-50")
        git(seed, "checkout", "-q", "main")
    r = out / "repo"
    git(out, "clone", "-q", str(out / "origin.git"), "repo")
    if scenario == "fixed":
        write(seed / "src/bye.sh", BYE)
        write(seed / "src/shout.sh", SHOUT)
        write(seed / "test.sh", test_sh("bye", "shout"))
        title = "feat: bye and shout commands"
    elif scenario == "worker":
        write(seed / "src/bye.sh", BYE)
        write(seed / "test.sh", test_sh("bye"))
        title = "feat: a bye command"
    else:
        write(seed / "README.md", "# greeter\n\n`src/greet.sh <name>` greets someone. See `test.sh`.\n")
        title = "docs: point the README at test.sh"
    git(seed, "add", "-A")
    git(seed, "commit", "-q", "-m", f"{title} (#9)\n\nPull request 9.", date="2026-10-10T10:00:00Z")
    git(seed, "push", "-q", "origin", "main")
    later = git(seed, "rev-parse", "HEAD")
    shutil.rmtree(seed)
    owner = ("\n## Comments\n\nOwner record: this Spec is owned by thread `spec-thread-50`, reached by message. "
             "Replaces: none.\n") if scenario == "worker" else ""
    write(r / ".scratch/issues/50-spec.md", f"""Title: Greeter commands
Type: spec
Labels: enhancement
Status: open
Created: 2026-10-02
Blocked by: none

Add two commands to the greeter, each with a test: `bye` (ticket 51) and `shout` (ticket 52).
{owner}""")
    write(r / ".scratch/issues/51-bye.md", """Title: Add a bye command
Type: ticket
Labels: enhancement, ready-for-agent
Status: open
Created: 2026-10-02
Parent: #50
Blocked by: none

Add `src/bye.sh <name>`, printing `Goodbye, <name>!`, with a test.
""")
    write(r / ".scratch/issues/52-shout.md", """Title: Add a shout command
Type: ticket
Labels: enhancement, ready-for-agent
Status: open
Created: 2026-10-02
Parent: #50
Blocked by: none

Add `src/shout.sh <name>`, printing `HELLO, <name>!`, with a test.
""")
    write(r / ".scratch/pulls/9-pr.md", f"Title: {title}\nStatus: merged\nMerged: 2026-10-10\nCommit: {later}\nCloses: none\n")
    (out / "PROMPT.md").write_text(prompt(r, scenario))
    fx = dict(scenario=scenario, later=later, main=git(r, "rev-parse", "main"),
              branches=git(r, "branch", "--format=%(refname:short)").split(),
              origin_branches=git(out / "origin.git", "branch", "--format=%(refname:short)").split(),
              worktrees=git(r, "worktree", "list", "--porcelain"))
    (out / "fixture.json").write_text(json.dumps(fx, indent=2) + "\n")
    return out


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: make_fixture.py <out-dir> [fixed|valid|worker]")
    print(build(sys.argv[1], *sys.argv[2:]))
