#!/usr/bin/env python3
"""Build the main-check case of the implement eval, outside this repo.

Usage: make_fixture.py <out-dir> [fixed|valid]
Makes <out-dir>/origin.git (a bare origin), <out-dir>/repo (a clone whose local `main` is one commit behind origin's,
so only a fetch shows what merged since the Ticket was written), <out-dir>/PROMPT.md and <out-dir>/fixture.json (what
score.py compares against). Ticket 40, written on 2026-10-02, says the usage line prints `helo`.
Scenario `fixed` (default): a later commit on origin's main, pull request 7 (written by someone else, closing no issue),
fixed the usage line and added its test to `test.sh`, so the Ticket (the fix "with a test") is already fixed on main. Scenario `valid`: the later commit on origin's main only
edits the README, so the bug is still on main. The tracker is local Markdown files under `.scratch/`, not in git.
See README.md.
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys

BUGGY = '#!/usr/bin/env bash\n[ $# -gt 0 ] || { echo "usage: greet.sh helo <name>"; exit 1; }\necho "Hello, $1!"\n'
FIXED = BUGGY.replace("helo", "hello")
USAGE_TEST = ('#!/usr/bin/env bash\nset -e\n[ "$(bash src/greet.sh Ann)" = "Hello, Ann!" ]\n'
              '[ "$(bash src/greet.sh)" = "usage: greet.sh hello <name>" ]\n')
TRACKER = """# Issue tracker

Issues and pull requests are local Markdown files; there is no forge and no CI.

- An issue is `.scratch/issues/<n>-<slug>.md` with `Title:`, `Type:` (ticket or spec), `Labels:`, `Status:` (open or
  closed), `Created:` and `Blocked by:` lines, then its body. Comments go under a `## Comments` heading at its end.
- A pull request is `.scratch/pulls/<n>-<slug>.md` with `Title:`, `Status:` (open or merged), `Merged:`, `Commit:` and
  `Closes:` lines.
- **Count open blockers**: the issues on the `Blocked by:` line whose `Status:` is open. `none` is zero.
- **Park**: an issue is parked when its `Labels:` line holds `parked`.
- The coordinator (a team lead) runs this project's threads; you reach it only by message.
"""


def git(cwd, *args, date=None):
    env = dict(os.environ)
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    return subprocess.run(["git", "-C", str(cwd), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                          check=True, capture_output=True, text=True, env=env).stdout.strip()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def prompt(repo):
    return f"""# Scripted prompt: implement, main-check case

Give the text between the lines to a fresh subagent at the regular tier, with its working directory at `{repo}`.
Give it the whole `implement` folder from the checkout under test (the branch's, then main's from a `git archive`),
nothing else from this folder. Keep `score.py`, `test_cases.py` and `fixture.json` away from it.

---

You are the Ticket thread for Ticket 40 (`.scratch/issues/40-usage-typo.md`), following `implement` (its files are in
the folder you were given). The tracker doc is `docs/dev-skills/issue-tracker.md`. A coordinator runs this project; you
reach it only by the message you write below. Work from step 1 up to the point where you would start the Implementer,
and stop there: start no subagent. Run only read-only commands (reading files; git fetch, log, diff, show, branch,
worktree list, rev-parse) and change nothing: no branch, worktree, push, file or commit. Write each command you would
run instead.

Write `.scratch/answer.md` with exactly these lines:

    Title: <the ticket's title>
    Branch: <the git commands that make the Ticket branch and its worktree and push it, one line joined with `&&`, or `none`>
    Brief: <the first lines of the Implementer's brief, or `none` if you start no Implementer>
    Message: <what you tell the coordinator now, in one line, or `none`>
    Thread: <building | waiting | stopped>

---
"""


def build(out, scenario="fixed"):
    if scenario not in ("fixed", "valid"):
        sys.exit("scenario is fixed or valid")
    out = pathlib.Path(out).resolve()
    if out.exists():
        sys.exit(f"{out} exists")
    out.mkdir(parents=True)
    git(out, "init", "-q", "--bare", "-b", "main", "origin.git")
    seed = out / "seed"
    git(out, "init", "-q", "-b", "main", "seed")
    git(seed, "remote", "add", "origin", str(out / "origin.git"))
    write(seed / "CLAUDE.md", "# greeter\n\nA tiny shell greeter. Run `bash test.sh` before each push.\n")
    write(seed / "README.md", "# greeter\n\n`greet.sh <name>` greets someone.\n")
    write(seed / "src/greet.sh", BUGGY)
    write(seed / "test.sh", '#!/usr/bin/env bash\n[ "$(bash src/greet.sh Ann)" = "Hello, Ann!" ]\n')
    write(seed / "docs/dev-skills/issue-tracker.md", TRACKER)
    write(seed / ".gitignore", ".scratch/\n")
    git(seed, "add", "-A")
    git(seed, "commit", "-q", "-m", "chore: greeter", date="2026-10-01T10:00:00Z")
    git(seed, "push", "-q", "origin", "main")
    r = out / "repo"
    git(out, "clone", "-q", str(out / "origin.git"), "repo")
    if scenario == "fixed":
        write(seed / "src/greet.sh", FIXED)
        write(seed / "test.sh", USAGE_TEST)
        msg = "fix: the usage line says hello (#7)\n\nPull request 7."
    else:
        write(seed / "README.md", "# greeter\n\n`greet.sh <name>` greets someone. See `test.sh`.\n")
        msg = "docs: point the README at test.sh (#7)\n\nPull request 7."
    git(seed, "commit", "-q", "-am", msg, date="2026-10-10T10:00:00Z")
    git(seed, "push", "-q", "origin", "main")
    later = git(seed, "rev-parse", "HEAD")
    shutil.rmtree(seed)
    write(r / ".scratch/issues/40-usage-typo.md", """Title: The usage line says "helo"
Type: ticket
Labels: bug, ready-for-agent
Status: open
Created: 2026-10-02
Blocked by: none

`bash src/greet.sh` with no name prints `usage: greet.sh helo <name>`. It should say `hello`.

Acceptance: the usage line reads `usage: greet.sh hello <name>`, with a test.
""")
    title = "fix: the usage line says hello" if scenario == "fixed" else "docs: point the README at test.sh"
    write(r / ".scratch/pulls/7-pr.md", f"Title: {title}\nStatus: merged\nMerged: 2026-10-10\nCommit: {later}\nCloses: none\n")
    (out / "PROMPT.md").write_text(prompt(r))
    fx = dict(scenario=scenario, later=later, main=git(r, "rev-parse", "main"),
              branches=git(r, "branch", "--format=%(refname:short)").split(),
              origin_branches=git(out / "origin.git", "branch", "--format=%(refname:short)").split(),
              worktrees=git(r, "worktree", "list", "--porcelain"))
    (out / "fixture.json").write_text(json.dumps(fx, indent=2) + "\n")
    return out


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("usage: make_fixture.py <out-dir> [fixed|valid]")
    print(build(sys.argv[1], *sys.argv[2:]))
