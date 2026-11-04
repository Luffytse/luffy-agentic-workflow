#!/usr/bin/env python3
"""Build the eval-test case of the implement eval, outside this repo.

Usage: make_fixture.py <out-dir> <skills-dir> [ticket|spec]
<skills-dir> is the skills tree under test (a checkout's plugins/dev-skills/skills, or the same folder of a
`git archive` of main). Makes in <out-dir>: TICKET.md (a Ticket whose whole change is skill text), BRIEF.md (the
bullets of the Implementer brief, copied from the `implement` or `implement-spec` skill's step "Start ... Implementer",
verbatim), skills/tdd/ (a copy of the `tdd` skill, which the brief tells the Implementer to build with), PROMPT.md and
fixture.json (what score.py compares against). The case's meaning: given a Ticket that changes only skill text, does
the Implementer plan an eval, choose its own seam and report the eval run as evidence? The case separates main's brief from the new one on the seam and evidence lines, not on grep versus eval. See README.md.
"""
import hashlib
import json
import pathlib
import re
import shutil
import sys

TICKET = """# 52: Standup asks for blockers first

**What to build:** the `standup` skill (`plugins/demo/skills/standup/SKILL.md`) asks the user for blockers before it asks
for yesterday's work, so a blocker is never skipped when the user is short of time.

**Model tier:** regular

## Acceptance criteria

- [ ] An agent that runs `standup` asks for blockers first, then yesterday's work, then today's plan.
- [ ] When the user names a blocker, the agent keeps it as the first line of the summary it writes.
- [ ] The skill's description and its other steps are unchanged.
"""

PROMPT = """# Scripted prompt: implement, eval-test case

Give the text between the lines to a fresh regular-tier subagent, working in <out-dir>, which holds {files}.
Keep the case README, `score.py` and `test_cases.py` away from it.

---

You are the Implementer for the Ticket in `TICKET.md`. The Ticket thread's brief is in `BRIEF.md`; the skill it tells
you to build with is in `skills/tdd/SKILL.md` (read it, and anything it links in that folder). Do not run anything
and do not edit the Ticket.

Before writing any test or code, write your plan to `plan.md`, one line per field, each field on one line:

TEST: eval | sentence-grep | code-test   (the kind of test you will write for the Ticket's acceptance criteria)
FIXTURE: <what the test is given to work on>
BASELINE: <what the test compares the changed work with, or none>
SEAM-CONFIRMED-BY: user | me   (who confirms the seam before your first test)
EVIDENCE: <what you will report as evidence for the criteria>

Then stop.

---
"""


def bullets(text):
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.rstrip().endswith("not copies:")]
    if not starts:
        raise SystemExit("no Implementer brief found in the skill")
    out = []
    for line in lines[starts[0] + 1:]:
        if re.match(r"\s*- ", line):
            out.append(re.sub(r"^\s+", "", line))
        elif out and line.strip() == "":
            break
    if not out:
        raise SystemExit("the Implementer brief has no bullets")
    return out


def tree_hash(root):
    h = hashlib.sha256()
    for p in sorted(pathlib.Path(root).rglob("*")):
        if p.is_file() and p.name not in ("plan.md", "fixture.json"):
            h.update(str(p.relative_to(root)).encode() + b"\0" + p.read_bytes())
    return h.hexdigest()


def build(out, skills, flow="ticket"):
    out, skills = pathlib.Path(out), pathlib.Path(skills)
    skill = "implement" if flow == "ticket" else "implement-spec"
    out.mkdir(parents=True, exist_ok=True)
    (out / "TICKET.md").write_text(TICKET)
    brief = bullets((skills / skill / "SKILL.md").read_text())
    (out / "BRIEF.md").write_text("# Brief from the Ticket thread\n\n" + "\n".join(brief) + "\n")
    shutil.copytree(skills / "tdd", out / "skills/tdd", dirs_exist_ok=True)
    (out / "PROMPT.md").write_text(PROMPT.format(files="TICKET.md, BRIEF.md, skills/tdd/"))
    (out / "fixture.json").write_text(json.dumps({"tree": tree_hash(out), "flow": flow}))


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        raise SystemExit(__doc__)
    build(*sys.argv[1:])
