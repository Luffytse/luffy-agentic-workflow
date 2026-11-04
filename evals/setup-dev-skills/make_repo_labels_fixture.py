#!/usr/bin/env python3
"""Build the scratch fixture for one Repo labels case of the setup-dev-skills eval.
Usage: python3 make_repo_labels_fixture.py <out-dir> <fresh|rerun-drop|none>
<out-dir> gets: repo/ (a git repo with a made-up GitHub remote), bin/gh (a logging stub), gh-state.json (the made-up
tracker's labels and issues), gh.log (empty) and PROMPT.md (the only thing the agent under test is given besides the
skill folder)."""
import json, os, shutil, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from repo_labels_cases import *  # noqa: F401,F403


def triage_labels_doc(rows):
    """A triage-labels doc as an earlier setup run would have left it: the role tables and a Repo labels section."""
    t = "# Triage Labels\n\n| Role in `dev-skills` | Label in our tracker | Meaning |\n| --- | --- | --- |\n"
    for r in ROLE_LABELS:
        t += f"| `{r}` | `{r}` | {r} |\n"
    t += ("\nWhen a skill mentions a role, use the corresponding label string from this table.\n\n## Repo labels\n\n"
          "Labels this repo records for its own kinds of work. They are not triage roles. An empty table means the repo has none.\n\n"
          "| Label in our tracker | When it applies |\n| --- | --- |\n")
    for label, line in rows.items():
        t += f"| `{label}` | {line} |\n"
    t += "\n## Other labels\n\n`retro` and `retro-planning` are not triage roles.\n"
    return t


def prompt(out, name):
    case = CASES[name]
    if name == "fresh":
        own = (f"Does this repo have labels of its own: **yes**. Pick `frontend` and `backend`; do not pick `docs-only`. Accept the "
               f"lines you draft for the two picked labels as they are. Then add one new label, `{NEW_LABEL}`, with the line "
               f"\"{NEW_LINE}\". Add no other label.")
    elif name == "rerun-drop":
        own = ("This is a re-run. Does this repo have labels of its own: **yes**. We no longer use `backend`: drop it. Keep `frontend` "
               "as it is. Edit nothing and add no label.")
    else:
        own = "Does this repo have labels of its own: **no**."
    return f"""Run the `setup-dev-skills` skill from the skill folder you were given, on the repo in `{out}/repo`
(your working directory). The user's answers are below, so log each question you would ask instead of waiting for a reply.

`gh` on your PATH is a local stand-in for the tracker: put `{out}/bin` first on PATH (`export PATH={out}/bin:$PATH`)
and use `gh` for every tracker operation. The remote is made up; do not try to reach it any other way.

Answers, in the order the skill asks:

- Section A: accept GitHub.
- Section B: keep the default labels: yes. Agent-only labels: no. {own}
- Section C: single-context.
- Section D: no rules of its own.
- Section E: this repo does not cut Releases.
- Section F: irreversible actions agents may take, none; actions needing approval, none; budget, none; check-in interval, 1 hour; Milestone label form, `milestone-<n>`.
- Approve every draft. If neither `CLAUDE.md` nor `AGENTS.md` exists, create `CLAUDE.md`.

Two notes for the log. When you offer the user a list of labels to pick from, write exactly those label names, one per line,
to `{out}/CANDIDATES.txt` before you go on; write no such file if you offer no list. And end your final reply with every
question you asked, one per line, in the form `Q: <the question> | recommended: <your recommended answer>`.
"""


def build(out, name):
    case = CASES[name]
    out = os.path.abspath(out)
    if os.path.exists(out):
        shutil.rmtree(out)
    repo = os.path.join(out, "repo")
    os.makedirs(os.path.join(out, "bin")), os.makedirs(repo)
    def git(*a):
        subprocess.run(["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.org", *a], cwd=repo, check=True,
                       capture_output=True)
    git("init", "-q", "-b", "main")
    git("remote", "add", "origin", f"https://github.com/{REPO}.git")
    open(os.path.join(repo, "README.md"), "w").write("# scratch-app\n")
    open(os.path.join(repo, "package.json"), "w").write('{"name": "scratch-app"}\n')
    if case["existing_rows"]:
        os.makedirs(os.path.join(repo, "docs/dev-skills"))
        open(os.path.join(repo, "docs/dev-skills/triage-labels.md"), "w").write(triage_labels_doc(case["existing_rows"]))
        open(os.path.join(repo, "CLAUDE.md"), "w").write(
            "## Agent skills\n\nStart at `docs/dev-skills/index.md`; it says which doc to read for what.\n\n"
            "### Triage labels\n\n5 state roles + 2 category roles. See `docs/dev-skills/triage-labels.md`.\n")
    git("add", "."), git("commit", "-q", "-m", "init")
    shutil.copy(os.path.join(here, "repo_labels_gh_stub.py"), os.path.join(out, "bin", "gh"))
    os.chmod(os.path.join(out, "bin", "gh"), 0o755)
    descs = dict(UNMAPPED)
    json.dump({"labels": [{"name": n, "description": descs.get(n, "")} for n in ALL_LABELS], "issues": ISSUES},
              open(os.path.join(out, "gh-state.json"), "w"), indent=1)
    open(os.path.join(out, "gh.log"), "w").close()
    open(os.path.join(out, "PROMPT.md"), "w").write(prompt(out, name))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
