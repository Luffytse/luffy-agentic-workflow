#!/usr/bin/env python3
"""Self-test of the implement eval-test case: builds the fixture from a stub skills tree and checks that the rendered
input says what the case means, then scores a reference plan (it must pass) and planted wrong plans (each must fail).
It proves the builder and the scorer agree; it is not a model run.

Run: python3 evals/implement/eval-test/test_cases.py
"""
import pathlib
import subprocess
import sys
import tempfile

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import make_fixture  # noqa: E402

STUB = """# Stub

Intro.

Brief it with pointers, not copies:
{b}- first stub bullet {tag};
{b}- second stub bullet {tag};
{n}- nested stub bullet {tag}.

Give trivial jobs to a cheap subagent.
"""
fail = 0


def check(name, ok):
    global fail
    print(("ok   " if ok else "FAIL ") + name)
    fail |= not ok


def stub_skills(root):
    for skill, b, n in (("implement", "", ""), ("implement-spec", "   ", "   ")):
        d = root / skill
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(STUB.format(b=b, n=n, tag=skill))
    (root / "tdd").mkdir()
    (root / "tdd/SKILL.md").write_text("# tdd stub\n")
    (root / "tdd/tests.md").write_text("# tests stub\n")


def plan(test="eval", fixture="a sample session the agent runs the skill on", baseline="main's skill, run the same way",
         seam="me", evidence="the eval run on both versions, scored by the scorer's output"):
    return (f"TEST: {test}\nFIXTURE: {fixture}\nBASELINE: {baseline}\nSEAM-CONFIRMED-BY: {seam}\nEVIDENCE: {evidence}\n")


def score(out, text):
    (out / "plan.md").write_text(text)
    r = subprocess.run([sys.executable, str(here / "score.py"), str(out)], capture_output=True, text=True)
    return r.returncode == 0


with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)
    skills = tmp / "skills"
    stub_skills(skills)
    for flow, skill in (("ticket", "implement"), ("spec", "implement-spec")):
        out = tmp / flow
        make_fixture.build(out, skills, flow)
        brief = (out / "BRIEF.md").read_text()
        want = "\n".join(f"- {w} stub bullet {skill}" + (";" if w != "nested" else ".") for w in ("first", "second", "nested"))
        check(f"{flow}: BRIEF.md holds the {skill} brief bullets verbatim, unindented, and nothing around them", brief.endswith(want + "\n") and "Intro" not in brief and "cheap subagent" not in brief)
        check(f"{flow}: the tdd skill folder is copied beside the brief", (out / "skills/tdd/SKILL.md").exists() and (out / "skills/tdd/tests.md").exists())
    out = tmp / "ticket"
    ticket = (out / "TICKET.md").read_text()
    check("TICKET.md changes only skill text: it names a SKILL.md and no source file", "SKILL.md" in ticket and not any(e in ticket for e in (".py", ".js", ".ts", ".sh")))
    check("TICKET.md does not hint at evals or greps", not any(w in ticket.lower() for w in ("eval", "grep", "fixture")))
    prompt = (out / "PROMPT.md").read_text()
    check("PROMPT.md asks for all five plan fields", all(f"{k}:" in prompt for k in ("TEST", "FIXTURE", "BASELINE", "SEAM-CONFIRMED-BY", "EVIDENCE")))
    check("PROMPT.md names no skill rule and does not say whether a user can be reached", "No user can be reached" not in prompt and "instructions for an agent" not in prompt)
    check("PROMPT.md offers all three kinds of test", all(k in prompt for k in ("eval", "sentence-grep", "code-test")))

    check("reference plan passes", score(out, plan()))
    check("reference with a stated gap as evidence passes", score(out, plan(evidence="the eval run, or its stated gap if it cannot be made")))
    for w in ("current", "existing", "unchanged", "original", "HEAD", "origin"):
        check(f"reference with baseline word '{w}' passes", score(out, plan(baseline=f"the {w} version of the skill")))
    for w in ("ran", "result", "results", "score", "scores", "output", "gap"):
        check(f"reference with evidence word '{w}' passes", score(out, plan(evidence=f"the {w} of the comparison on both versions")))
    check("evidence with the bare word 'eval' only fails", not score(out, plan(evidence="an eval")))
    check("'not a grep' in evidence passes", score(out, plan(evidence="the eval run on both versions, not a sentence grep")))
    planted = [
        ("sentence grep test", plan(test="sentence-grep", evidence="grep finds the sentence in SKILL.md")),
        ("code test", plan(test="code-test")),
        ("eval label but evidence is a grep", plan(evidence="grep for the new sentence in SKILL.md")),
        ("no baseline named", plan(baseline="")),
        ("seam confirmed by the user", plan(seam="user")),
        ("evidence names no run", plan(evidence="the diff and a description of the change")),
        ("missing field", "TEST: eval\nFIXTURE: x\nBASELINE: main\nEVIDENCE: the run\n"),
        ("no plan", None),
    ]
    for name, text in planted:
        if text is None:
            (out / "plan.md").unlink(missing_ok=True)
            ok = subprocess.run([sys.executable, str(here / "score.py"), str(out)], capture_output=True).returncode == 0
        else:
            ok = score(out, text)
        check(f"planted wrong plan fails: {name}", not ok)
    (out / "plan.md").write_text(plan())
    (out / "stray.txt").write_text("x")
    check("planted wrong run fails: a file written besides plan.md",
          subprocess.run([sys.executable, str(here / "score.py"), str(out)], capture_output=True).returncode != 0)

print("ok" if not fail else "FAILED")
sys.exit(fail)
