#!/usr/bin/env python3
"""Build the closing case of the implement-spec eval, outside this repo.

Usage: make_fixture.py <out-dir>
Makes <out-dir>/repo (a git repo: `main` and branch `spec-20` holding Tickets 21 and 22, with the dry-run local
tracker of evals/merging under .scratch/), <out-dir>/PROMPT.md and <out-dir>/fixture.json (what score.py compares
against). Spec 20 has Tickets 21 and 22, which landed on the Spec branch, and Ticket 23, which the user dropped and
which never landed; the open Spec pull request 1 still carries Ticket 23's `Closes` line. See README.md.
"""
import json
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent.parent / "merging"))
from make_fixture import TRACKER, git, tree_hash, write  # noqa: E402

TITLE = "feat: greet and say goodbye"
LANDED, DROPPED, SPEC = (21, 22), 23, 20

BODY = """## Summary

Adds `greet.sh bye <name>` and `greet.sh shout <name>`.

Closes #20
Closes #21
Closes #22
Closes #23

## Evidence

`bash test.sh` passes.

**Door:** two-way. Reverting the merge removes both commands.
"""

GREET = """#!/usr/bin/env bash
case "${1:-}" in
  hello) echo "Hello, ${2:-world}!" ;;
  bye) echo "Goodbye, ${2:-world}!" ;;
  shout) echo "HELLO, ${2:-world}!" ;;
  *) echo "usage: greet.sh hello|bye|shout <name>" >&2; exit 2 ;;
esac
"""


def issue(n, title, kind, text):
    return f"Title: {title}\nType: {kind}\nLabels: enhancement\nStatus: open\n\n{text}\n"


def prompt(repo):
    return f"""# Scripted prompt: implement-spec, closing case

Give the text between the lines to a fresh session at the premium tier (load `model-tiers` for the model), with its
working directory at `{repo}`. Replace `<checkout>` with the checkout under test: the branch's, then main's.

---

You are the Spec thread for Spec 20 (`.scratch/issues/20-spec.md`). Load the `implement-spec` skill from
`<checkout>/plugins/dev-skills/skills/implement-spec/SKILL.md` (the checkout under test, not an installed copy), with
every skill it names loaded from the same `skills/` folder. Steps 1 to 7 are done: Tickets 21 and 22 landed on the
Spec branch `spec-20`, the user dropped Ticket 23 (it never landed and is not built), the Spec pull request 1
(`.scratch/pulls/1.md`) is open, and its review ended ready to merge with the checks passing. Follow `implement-spec`
from step 8 through step 9's report. The tracker is the dry-run one in `docs/dev-skills/issue-tracker.md`: write every
tracker, pull request and git write as a block in `.scratch/proposed-actions.md`, change no other file and make no
commit. An Implementer on the Spec branch is reachable by message: a commit it would make is a **Commit to a branch**
block with `By: Implementer`. The user answers no question: when you would bring the pull request to the user, write
what you would tell them to `.scratch/report.md` (if you cannot write that file, return the same text as your final message) and stop. Write your step 9 report to `.scratch/report.md` too.

---

Score it with `python3 evals/implement-spec/closing/score.py {repo.parent}`, and record the run in
`evals/implement-spec/RESULTS.md`.
"""


def build(out):
    out = pathlib.Path(out).resolve()
    if out.exists():
        sys.exit(f"{out} exists")
    r = out / "repo"
    r.mkdir(parents=True)
    git(r, "init", "-q", "-b", "main")
    write(r / "CLAUDE.md", "# greeter\n\nA tiny shell greeter. Run `bash test.sh` before each push.\n\n## Agent skills\n\nStart at `docs/dev-skills/index.md`. Issues and pull requests live in the local dry-run tracker (`docs/dev-skills/issue-tracker.md`).\n")
    write(r / "docs/dev-skills/index.md", "# Docs index\n\n- [docs/dev-skills/issue-tracker.md](issue-tracker.md): the local dry-run tracker and its operations. Read before any tracker, pull request or git write.\n")
    write(r / "docs/dev-skills/issue-tracker.md", TRACKER)
    write(r / "src/greet.sh", GREET.replace('  bye) echo "Goodbye, ${2:-world}!" ;;\n', "").replace('  shout) echo "HELLO, ${2:-world}!" ;;\n', ""))
    write(r / "test.sh", '#!/usr/bin/env bash\nset -e\n[ "$(bash src/greet.sh hello Ada)" = "Hello, Ada!" ]\necho OK\n')
    write(r / ".scratch/issues/20-spec.md", issue(20, "Greeter commands", "spec", "## Problem Statement\n\nThe greeter only says hello."))
    write(r / ".scratch/issues/21-bye.md", issue(21, "Add a bye command", "ticket", "Parent: #20\n\nAdd `greet.sh bye <name>`."))
    write(r / ".scratch/issues/22-shout.md", issue(22, "Add a shout command", "ticket", "Parent: #20\n\nAdd `greet.sh shout <name>`."))
    write(r / ".scratch/issues/23-wave.md", issue(23, "Add a wave command", "ticket", "Parent: #20\n\nAdd `greet.sh wave <name>`. The user dropped this Ticket."))
    write(r / ".scratch/pulls/1.md", f"Title: {TITLE}\nBase: main\nHead: spec-20\nState: open\n\n" + BODY)
    write(r / ".gitignore", ".scratch/proposed-actions.md\n.scratch/report.md\n")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "chore: fixture")
    git(r, "checkout", "-q", "-b", "spec-20")
    write(r / "src/greet.sh", GREET.replace('  shout) echo "HELLO, ${2:-world}!" ;;\n', ""))
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "feat: add a bye command\n\nTicket #21.")
    write(r / "src/greet.sh", GREET)
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "feat: add a shout command\n\nTicket #22.")
    git(r, "checkout", "-q", "main")
    (out / "PROMPT.md").write_text(prompt(r))
    fixture = dict(main=git(r, "rev-parse", "main"), branch=git(r, "rev-parse", "spec-20"), tree=tree_hash(r), title=TITLE)
    (out / "fixture.json").write_text(json.dumps(fixture, indent=2) + "\n")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: make_fixture.py <out-dir>")
    print(build(sys.argv[1]))
