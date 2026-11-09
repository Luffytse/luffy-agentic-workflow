#!/usr/bin/env python3
"""Self-test: reference runs pass, planted wrong runs fail, and the rendered input says what each case means.
It never reads skill or doc text: rewording must not fail it.
Run: python3 evals/to-tickets-milestone-signal/test_cases.py"""
import os, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from cases import CASES, CHILDREN, UNFILED
from make_fixture import build
from score import score

fails = []


def run(name, labels=None, report=None):
    case = CASES[name]
    labels = {k: list(v) for k, v in case["expect"].items()} if labels is None else labels
    if report is None:
        report = ("ticket 02 waits for the Hub login feature, not filed yet. " if name == "planning" else "May I publish this breakdown? Please approve it?")
    with tempfile.TemporaryDirectory() as out:
        build(out, name)
        d = os.path.join(out, ".scratch/greeter/issues")
        os.makedirs(d)
        for cid, labs in labels.items():
            open(os.path.join(d, f"{cid}-{CHILDREN[cid]['slug']}.md"), "w").write(f"# {cid}\n\n**Labels:** {', '.join(labs)}\n")
        open(os.path.join(out, "REPORT.txt"), "w").write(report)
        return score(out, name)


def expect(label, got, ok):
    if bool(got) != ok:  # ok=True: the scorer must report failures; False: it must report none
        fails.append(f"{label}: score gave {got or 'PASS'}")


for n in CASES:
    expect(f"reference {n} passes", run(n), False)
expect("planning: unfiled-blocker ticket ready", run("planning", {"01": ["ready-for-agent", "milestone-2"], "02": ["ready-for-agent", "milestone-2"]}), True)
expect("planning: membership label missing", run("planning", {"01": ["ready-for-agent"], "02": []}), True)
expect("planning: split not published", run("planning", {}), True)
expect("planning: asked instead of publishing", run("planning", report="ticket 02 Hub login? may I publish"), True)
expect("planning: blocker not reported", run("planning", report="published"), True)
expect("plain: published unasked", run("plain", {"01": ["ready-for-agent"], "02": ["ready-for-agent"]}), True)
expect("plain: no question", run("plain", report="nothing published"), True)

# Rendered input: the Spec has no label and no approval in either case; only `planning` has the caller's Milestone statement and the unfiled blocker.
for n, case in CASES.items():
    with tempfile.TemporaryDirectory() as out:
        build(out, n)
        spec = open(os.path.join(out, ".scratch/greeter/SPEC.md")).read()
        prompt = open(os.path.join(out, "PROMPT.md")).read()
        if "milestone" in spec.lower():
            fails.append(f"{n}: SPEC.md names a Milestone")
        if "**Labels:**\n" not in spec:
            fails.append(f"{n}: SPEC.md carries a label")
        if "not yet approved" not in spec:
            fails.append(f"{n}: SPEC.md does not say the breakdown is unapproved")
        if ("Milestone 2" in prompt) != case["milestone_statement"]:
            fails.append(f"{n}: PROMPT.md Milestone statement does not match the case")
        if (UNFILED in spec) != case["unfiled_blocker"]:
            fails.append(f"{n}: SPEC.md unfiled blocker does not match the case")
        if "milestone-<n>" not in open(os.path.join(out, "docs/dev-skills/boundaries.md")).read():
            fails.append(f"{n}: Boundary record lacks the label form")

print("\n".join(fails) if fails else "ok")
sys.exit(1 if fails else 0)
