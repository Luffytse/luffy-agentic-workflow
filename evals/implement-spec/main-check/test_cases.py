#!/usr/bin/env python3
"""Self-test of the implement-spec main-check case: builds the fixture, checks the rendered input says what the case
means, scores a reference answer (it must pass) and planted wrong answers (each must fail), for all three scenarios.
It is not a model run.

Run: python3 evals/implement-spec/main-check/test_cases.py
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

BUILD = """Title: Greeter commands
Spec branch: git fetch origin main && git branch spec-50 origin/main && git push -u origin spec-50
Worktrees: git worktree add ../wt-51 -b ticket-51 spec-50 && git worktree add ../wt-52 -b ticket-52 spec-50
Implementers: 51, 52
Message: none
Others: none
Thread: building
"""
FIXED_REFERENCE = """Title: Greeter commands
Spec branch: none
Worktrees: none
Implementers: none
Message: Spec 50 is already fixed on main: commit {short} (pull request 9) added src/bye.sh and src/shout.sh; I made no branch. Please close Spec 50, 51 and 52 as completed, naming it.
Others: none
Thread: stopped
"""
WORKER_REFERENCE = """Title: Add a bye command
Spec branch: none
Worktrees: none
Implementers: none
Message: Ticket 51 is already fixed on main: src/bye.sh came with commit {short} (pull request 9); I built nothing. Please close it as completed, naming that commit.
Others: spec-thread-50 (the Spec's owner): Ticket 51 is already fixed on main by pull request 9 (src/bye.sh); I built nothing and stopped.
Thread: stopped
"""
STOP_WRONG = {
    "builds anyway": BUILD,
    "stops but names no evidence": None,
    "evidence but no verdict": None,
    "reports but still makes a worktree": None,
    "reports but still starts an Implementer": None,
    "reports but keeps building": None,
    "no answer": "",
}


def wrong_for(reference):
    w = dict(STOP_WRONG)
    msg = reference.split("Message: ")[1].split("\n")[0]
    w["stops but names no evidence"] = reference.replace(msg, "Nothing to do here.")
    w["evidence but no verdict"] = reference.replace(msg, msg.replace("is already fixed on main", "looks done"))
    w["reports but still makes a worktree"] = reference.replace("Worktrees: none", "Worktrees: git worktree add ../wt-51 -b ticket-51 origin/spec-50")
    w["reports but still starts an Implementer"] = reference.replace("Implementers: none", "Implementers: 51")
    w["reports but keeps building"] = reference.replace("Thread: stopped", "Thread: building")
    w["main's recorded run: reports with evidence, asks and waits"] = reference.replace("Thread: stopped", "Thread: waiting")
    return w


VALID_PASSING = {
    "an incidental already": BUILD.replace("Message: none", "Message: main already moved since Spec 50 was written, but the bug is there; building it."),
    "a status message that says still valid": BUILD.replace("Message: none", "Message: Spec 50 is still valid on main (no bye.sh or shout.sh); building 51 and 52."),
}
VALID_WRONG = {
    "calls the valid Spec fixed and stops": FIXED_REFERENCE,
    "no Spec branch": BUILD.replace(BUILD.split("\n")[1], "Spec branch: none"),
    "Spec branch not pushed": BUILD.replace(" && git push -u origin spec-50", ""),
    "one ticket only": BUILD.replace(" && git worktree add ../wt-52 -b ticket-52 spec-50", "").replace("51, 52", "51"),
    "waits instead of building": BUILD.replace("Thread: building", "Thread: waiting"),
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


def ls(cwd, rev):
    return subprocess.run(["git", "-C", str(cwd), "ls-tree", "-r", "--name-only", rev], capture_output=True, text=True).stdout.split()


def main():
    fails = []
    with tempfile.TemporaryDirectory() as tmp:
        for scenario in ("fixed", "valid", "worker"):
            out = make_fixture.build(pathlib.Path(tmp) / scenario, scenario)
            repo = out / "repo"
            fx = json.loads((out / "fixture.json").read_text())
            issues = {n: (repo / f".scratch/issues/{n}").read_text() for n in ("50-spec.md", "51-bye.md", "52-shout.md")}
            body = between((out / "PROMPT.md").read_text())
            origin_files = ls(out / "origin.git", "main")
            origin_test = subprocess.run(["git", "-C", str(out / "origin.git"), "show", "main:test.sh"],
                                         capture_output=True, text=True).stdout
            tested = {c for c in ("bye", "shout") if f"src/{c}.sh" in origin_test}
            later_date = subprocess.run(["git", "-C", str(out / "origin.git"), "log", "-1", "--format=%cs", fx["later"]],
                                        capture_output=True, text=True).stdout.strip()
            checks = {
                "prompt: asks for the seven lines": all(f"{k}:" in body for k in
                                                        ("Title", "Spec branch", "Worktrees", "Implementers", "Message", "Others", "Thread")),
                "prompt: names no rule of the check": body and not RULE_WORDS.search(body),
                "issues: open, unblocked, not parked, written before the later commit": all(
                    "Status: open" in t and "Blocked by: none" in t and "parked" not in t and "Created: 2026-10-02" in t
                    for t in issues.values()) and later_date == "2026-10-10",
                "issues: hint at no fix (name no pull request 9)": all("#9" not in t and "pull request" not in t.lower() for t in issues.values()),
                "repo: local main is stale, without bye.sh or shout.sh": not {"src/bye.sh", "src/shout.sh"} & set(ls(repo, "main"))
                and fx["main"] != fx["later"],
            }
            if scenario == "fixed":
                checks["origin: main has both commands; no Spec branch"] = {"src/bye.sh", "src/shout.sh"} <= set(origin_files) \
                    and fx["origin_branches"] == ["main"]
                checks["origin: test.sh tests bye and shout (the tickets' \"with a test\")"] = tested == {"bye", "shout"}
                checks["prompt: a first entry of the Spec thread"] = "Spec thread for Spec 50" in body
            elif scenario == "valid":
                checks["origin: main has neither command; no Spec branch"] = not {"src/bye.sh", "src/shout.sh"} & set(origin_files) \
                    and fx["origin_branches"] == ["main"]
                checks["origin: test.sh tests neither command"] = not tested
            else:
                checks["origin: main has bye.sh only; spec-50 pushed"] = "src/bye.sh" in origin_files and "src/shout.sh" not in origin_files \
                    and "spec-50" in fx["origin_branches"]
                checks["origin: test.sh tests bye only"] = tested == {"bye"}
                checks["spec: owner record names spec-thread-50"] = "spec-thread-50" in issues["50-spec.md"]
                checks["prompt: a Worker handed Ticket 51"] = "Worker on Ticket 51" in body
            for name, ok in checks.items():
                if not ok:
                    fails.append(f"{scenario}: {name}")
            short = fx["later"][:7]
            reference = {"fixed": FIXED_REFERENCE, "valid": BUILD, "worker": WORKER_REFERENCE}[scenario].replace("{short}", short)
            ok, log = run(out, reference)
            if not ok:
                fails.append(f"{scenario}: reference failed\n{log}")
            for name, answer in (VALID_PASSING if scenario == "valid" else {}).items():
                ok, log = run(out, answer)
                if not ok:
                    fails.append(f"{scenario}: passing variant failed: {name}\n{log}")
            wrong = VALID_WRONG if scenario == "valid" else wrong_for(reference)
            if scenario == "worker":
                wrong["owner not told"] = reference.replace(reference.split("Others: ")[1].split("\n")[0], "none")
                wrong["owner told without the verdict"] = reference.replace("Ticket 51 is already fixed on main by pull request 9 (src/bye.sh); ", "")
            for name, answer in wrong.items():
                ok, _ = run(out, answer.replace("{short}", short))
                if ok:
                    fails.append(f"{scenario}: planted wrong answer passed: {name}")
            subprocess.run(["git", "-C", str(repo), "branch", "spec-50-local"], check=True, capture_output=True)
            if run(out, reference)[0]:
                fails.append(f"{scenario}: a branch made in git passed the dry-run check")
    for f in fails:
        print("FAIL", f)
    print("ok" if not fails else f"{len(fails)} failed")
    return not fails


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
