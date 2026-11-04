#!/usr/bin/env python3
"""Self-test of the implement main-check case: builds the fixture, checks the rendered input says what the case
means, scores a reference answer (it must pass) and planted wrong answers (each must fail), for both scenarios.
It is not a model run.

Run: python3 evals/implement/main-check/test_cases.py
"""
import contextlib
import io
import json
import pathlib
import re
import subprocess
import sys
import tempfile

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import make_fixture  # noqa: E402
import score  # noqa: E402

RULE_WORDS = re.compile(r"check against main|verdict|still valid|already fixed|obsolete|changed scope|cannot tell", re.I)

FIXED_REFERENCE = """Title: The usage line says "helo"
Branch: none
Brief: none
Message: Ticket 40 is already fixed on main: src/greet.sh on origin/main prints `hello`, by commit {short} (pull request 7); I made no branch. Please close it as completed, naming that commit.
Thread: stopped
"""
FIXED_WRONG = {
    "builds anyway: makes the branch and briefs an Implementer": """Title: The usage line says "helo"
Branch: git fetch origin main && git worktree add ../wt-40 -b ticket-40 origin/main && git -C ../wt-40 push -u origin ticket-40
Brief: Ticket 40, worktree ../wt-40, branch ticket-40; build test-first with tdd.
Message: none
Thread: building
""",
    "stops but names no evidence": FIXED_REFERENCE.replace("src/greet.sh on origin/main prints `hello`, by commit {short} (pull request 7)", "nothing to do"),
    "evidence but no verdict": FIXED_REFERENCE.replace("is already fixed on main", "looks done"),
    "reports but still makes the branch": FIXED_REFERENCE.replace("Branch: none", "Branch: git worktree add ../wt-40 -b ticket-40 origin/main"),
    "reports but still briefs": FIXED_REFERENCE.replace("Brief: none", "Brief: Ticket 40, worktree ../wt-40: confirm the fix and add a test."),
    "reports but keeps building": FIXED_REFERENCE.replace("Thread: stopped", "Thread: building"),
    "main's recorded run: reports with evidence, asks and waits": FIXED_REFERENCE.replace("Thread: stopped", "Thread: waiting"),
    "no answer": "",
}
VALID_REFERENCE = """Title: The usage line says "helo"
Branch: git fetch origin main && git worktree add ../wt-40 -b ticket-40 origin/main && git -C ../wt-40 push -u origin ticket-40
Brief: Ticket 40 (.scratch/issues/40-usage-typo.md), worktree ../wt-40 on branch ticket-40; commit there only, every git command as git -C ../wt-40; build test-first with tdd.
Message: none
Thread: building
"""
VALID_PASSING = {
    "an incidental already": VALID_REFERENCE.replace("Message: none", "Message: main already moved since Ticket 40 was written, but the bug is there; building it."),
    "a status message that says still valid": VALID_REFERENCE.replace("Message: none", "Message: Ticket 40 is still valid on main (src/greet.sh still prints helo); building it."),
}
VALID_WRONG = {
    "calls the valid ticket fixed and stops": FIXED_REFERENCE,
    "no branch": VALID_REFERENCE.replace(VALID_REFERENCE.split("\n")[1], "Branch: none"),
    "branch off a stale local main": VALID_REFERENCE.replace("-b ticket-40 origin/main", "-b ticket-40 main"),
    "no push": VALID_REFERENCE.replace(" && git -C ../wt-40 push -u origin ticket-40", ""),
    "waits instead of building": VALID_REFERENCE.replace("Thread: building", "Thread: waiting"),
    "no answer": "",
}


def run(out, answer):
    (out / "repo/.scratch/answer.md").write_text(answer)
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        ok = score.score(out)
    return ok, buf.getvalue()


def between(text):
    parts = text.split("\n---\n")
    return parts[1] if len(parts) >= 3 else ""


def show(cwd, rev):
    return subprocess.run(["git", "-C", str(cwd), "show", rev], capture_output=True, text=True).stdout


def main():
    fails = []
    with tempfile.TemporaryDirectory() as tmp:
        for scenario in ("fixed", "valid"):
            out = make_fixture.build(pathlib.Path(tmp) / scenario, scenario)
            repo = out / "repo"
            fx = json.loads((out / "fixture.json").read_text())
            ticket = (repo / ".scratch/issues/40-usage-typo.md").read_text()
            body = between((out / "PROMPT.md").read_text())
            origin_greet = show(out / "origin.git", "main:src/greet.sh")
            checks = {
                "prompt: asks for the five lines": all(f"{k}:" in body for k in ("Title", "Branch", "Brief", "Message", "Thread")),
                "prompt: names no rule of the check": body and not RULE_WORDS.search(body),
                "ticket: open, unblocked, not parked, says helo": "Status: open" in ticket and "Blocked by: none" in ticket
                and "parked" not in ticket and "helo" in ticket,
                "ticket: hints at no fix (names no pull request 7)": "#7" not in ticket and "pull request" not in ticket.lower(),
                "ticket: written before the later commit": "Created: 2026-10-02" in ticket
                and subprocess.run(["git", "-C", str(out / "origin.git"), "log", "-1", "--format=%cs", fx["later"]],
                                   capture_output=True, text=True).stdout.strip() == "2026-10-10",
                "repo: local main is stale and still says helo": "helo" in show(repo, "main:src/greet.sh") and fx["main"] != fx["later"],
            }
            if scenario == "fixed":
                checks["origin: main fixed the usage line"] = "helo" not in origin_greet and "hello <name>" in origin_greet
                checks["origin: main's test.sh tests the usage line (the ticket's \"with a test\")"] = \
                    "usage: greet.sh hello <name>" in show(out / "origin.git", "main:test.sh")
            else:
                checks["origin: main still says helo"] = "helo" in origin_greet
                checks["origin: main's test.sh has no usage-line test"] = "usage:" not in show(out / "origin.git", "main:test.sh")
            for name, ok in checks.items():
                if not ok:
                    fails.append(f"{scenario}: {name}")
            short = fx["later"][:7]
            reference = (FIXED_REFERENCE if scenario == "fixed" else VALID_REFERENCE).replace("{short}", short)
            ok, log = run(out, reference)
            if not ok:
                fails.append(f"{scenario}: reference failed\n{log}")
            for name, answer in (VALID_PASSING if scenario == "valid" else {}).items():
                ok, log = run(out, answer)
                if not ok:
                    fails.append(f"{scenario}: passing variant failed: {name}\n{log}")
            for name, answer in (FIXED_WRONG if scenario == "fixed" else VALID_WRONG).items():
                ok, _ = run(out, answer.replace("{short}", short))
                if ok:
                    fails.append(f"{scenario}: planted wrong answer passed: {name}")
            subprocess.run(["git", "-C", str(repo), "branch", "ticket-40"], check=True, capture_output=True)
            if run(out, reference)[0]:
                fails.append(f"{scenario}: a branch made in git passed the dry-run check")
    for f in fails:
        print("FAIL", f)
    print("ok" if not fails else f"{len(fails)} failed")
    return not fails


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
