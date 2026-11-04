#!/usr/bin/env python3
"""Self-test of the implement-spec ticket-branch case: builds the fixture, checks the rendered input says what the
case means, scores a reference answer (it must pass) and planted wrong answers (each must fail). It is not a model run.

Run: python3 evals/implement-spec/ticket-branch/test_cases.py
"""
import pathlib
import subprocess
import sys
import tempfile

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import make_fixture  # noqa: E402
import score  # noqa: E402

REFERENCE = """Observed: local ticket-31 holds one unpushed commit ahead of the Spec branch; ticket 31 has not landed.
Command: git worktree add /tmp/wt-31 ticket-31
Cleanup: none
Branch: reuse
Spec tip: the Implementer merges spec-30's tip into ticket-31 first (a merge, never a rebase), then reruns the tests.
Brief: Handoff: the bye command is committed as a first pass; open: tests and evidence. Continue; your evidence and the ticket check are still required, nothing here is trusted unchecked.
"""
WRONG = {
    "recreate with -b": REFERENCE.replace("git worktree add /tmp/wt-31 ticket-31", "git worktree add /tmp/wt-31 -b ticket-31 spec-30"),
    "discard the branch": REFERENCE.replace("Branch: reuse", "Branch: discard").replace("git worktree add /tmp/wt-31 ticket-31", "git branch -D ticket-31 && git worktree add /tmp/wt-31 -b ticket-31 spec-30"),
    "rebase": REFERENCE.replace("a merge, never a rebase", "rebased onto it").replace("merges", "rebases"),
    "no handoff": REFERENCE.split("Brief:")[0] + "Brief: go.\n",
    "brief without evidence or check wording": REFERENCE.split("Brief:")[0] + "Brief: Handoff: the bye command is committed as a first pass; open: tests. Continue from there.\n",
    "reuse with a branch delete in Cleanup": REFERENCE.replace("Cleanup: none", "Cleanup: git branch -D ticket-31"),
    "no answer": "",
}
LANDED_REFERENCE = """Observed: spec-30 already holds Ticket 31's squash commit; the local ticket-31 is a stale leftover.
Command: none
Cleanup: git branch -D ticket-31
Branch: discard
Spec tip: none
Brief: none; no Implementer is started for a landed ticket.
"""
LANDED_WRONG = {
    "reuse the landed ticket's branch": REFERENCE,
    "-b on the existing branch, no delete": LANDED_REFERENCE.replace("Command: none", "Command: git worktree add /tmp/wt-31 -b ticket-31 spec-30").replace("Cleanup: git branch -D ticket-31", "Cleanup: none").replace("Branch: discard", "Branch: fresh"),
    "rebuilds the landed ticket after deleting": LANDED_REFERENCE.replace("Command: none", "Command: git worktree add /tmp/wt-31 -b ticket-31 spec-30"),
    "rebuild brief": LANDED_REFERENCE.replace("Brief: none; no Implementer is started for a landed ticket.", "Brief: Rebuild Ticket 31 on spec-30."),
    "discard said but nothing deleted": LANDED_REFERENCE.replace("Cleanup: git branch -D ticket-31", "Cleanup: none"),
    "no answer": "",
}
PASSING_VARIANTS = {
    "a merge rather than a rebase": REFERENCE.replace("(a merge, never a rebase)", "(a merge rather than a rebase)"),
    "don't rebase": REFERENCE.replace("(a merge, never a rebase)", "(a merge; don't rebase)"),
    "merge instead of rebasing": REFERENCE.replace("(a merge, never a rebase)", "(merge instead of rebasing)"),
}


def run(out, answer, tamper=False):
    (out / "repo/.scratch").mkdir(exist_ok=True)
    (out / "repo/.scratch/answer.md").write_text(answer)
    if tamper:
        subprocess.run(["git", "-C", str(out / "repo"), "branch", "-D", "ticket-31"], check=True, capture_output=True)
    return subprocess.run([sys.executable, str(here / "score.py"), str(out)], capture_output=True, text=True)


def main():
    fails = 0
    with tempfile.TemporaryDirectory() as t:
        t = pathlib.Path(t)
        out = make_fixture.build(t / "ref")
        g = lambda *a: subprocess.run(["git", "-C", str(out / "repo"), *a], capture_output=True, text=True).stdout  # noqa: E731
        prompt = (out / "PROMPT.md").read_text()
        checks = [
            ("fixture: local ticket-31 holds a commit ahead of spec-30", "bye.sh" in g("diff", "--name-only", "spec-30...ticket-31")),
            ("fixture: ticket-31 was never pushed", "ticket-31" not in g("ls-remote", "--heads", "origin")),
            ("fixture: spec-30 is pushed and holds no work of Ticket 31", "spec-30" in g("ls-remote", "--heads", "origin") and "#31" not in g("log", "spec-30", "--format=%B")),
            ("fixture: Ticket 32's squash commit is on spec-30, Ticket 31's file is not", "#32" in g("log", "spec-30", "--format=%B") and not (out / "repo/src/bye.sh").exists()),
            ("rendered prompt: names Ticket 31, step 3.1 and re-entry", "Ticket 31" in prompt and "step 3.1" in prompt and "re-entering" in prompt),
            ("rendered prompt: asks for the six answer lines", all(k in prompt for k in ("Observed:", "Command:", "Branch:", "Spec tip:", "Brief:", "Cleanup:"))),
            ("rendered prompt: read-only, keeps the answer key away", "read-only" in prompt and "score.py" in prompt),
        ]
        for name, ok in checks:
            print(("PASS " if ok else "FAIL ") + name)
            fails += not ok
        r = run(out, REFERENCE)
        print(("PASS " if r.returncode == 0 else "FAIL ") + "reference answer scores clean")
        fails += r.returncode != 0
        for name, ans in WRONG.items():
            o = make_fixture.build(t / name.replace(" ", "-"))
            r = run(o, ans)
            print(("PASS " if r.returncode != 0 else "FAIL ") + f"planted wrong answer fails: {name}")
            fails += r.returncode == 0
        for name, ans in PASSING_VARIANTS.items():
            o = make_fixture.build(t / name.replace(" ", "-"))
            r = run(o, ans)
            print(("PASS " if r.returncode == 0 else "FAIL ") + f"passing variant scores clean: {name}")
            fails += r.returncode != 0
        lo = make_fixture.build(t / "landed", "landed")
        lg = lambda *a: subprocess.run(["git", "-C", str(lo / "repo"), *a], capture_output=True, text=True).stdout  # noqa: E731
        lp = (lo / "PROMPT.md").read_text()
        for name, ok in [
            ("landed fixture: spec-30 holds Ticket 31's squash commit", "#31" in lg("log", "spec-30", "--format=%B")),
            ("landed fixture: local ticket-31 still holds its commit, never pushed", "bye.sh" in lg("show", "--stat", "--format=", "ticket-31") and "ticket-31" not in lg("ls-remote", "--heads", "origin")),
            ("landed prompt: does not call Ticket 31 the next frontier ticket", "next frontier ticket" not in lp and "tracker shows Ticket 31 open" in lp),
            ("landed prompt: asks what to do for Ticket 31 and the leftovers, with a Cleanup line", "leftovers" in lp and "Cleanup:" in lp and "Ticket 31" in lp),
        ]:
            print(("PASS " if ok else "FAIL ") + name)
            fails += not ok
        r = run(lo, LANDED_REFERENCE)
        print(("PASS " if r.returncode == 0 else "FAIL ") + "landed reference answer scores clean")
        fails += r.returncode != 0
        for name, ans in LANDED_WRONG.items():
            o = make_fixture.build(t / ("landed-" + name.replace(" ", "-")), "landed")
            r = run(o, ans)
            print(("PASS " if r.returncode != 0 else "FAIL ") + f"landed planted wrong answer fails: {name}")
            fails += r.returncode == 0
        o = make_fixture.build(t / "tamper")
        r = run(o, REFERENCE, tamper=True)
        print(("PASS " if r.returncode != 0 else "FAIL ") + "planted wrong run fails: ticket branch deleted in git")
        fails += r.returncode == 0
    print("ok" if not fails else f"{fails} failed")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
