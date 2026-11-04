#!/usr/bin/env python3
"""Self-test: reference runs pass, planted wrong runs fail, and the inherited case's rendered Spec names only the source's
runtime. It never reads skill or doc text: rewording must not fail it.
Run: python3 evals/to-tickets-agent-label/test_cases.py"""
import os, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from cases import CASES, CHILDREN
from make_fixture import build, child_text
from score import score

fails = []


def reference(out, name, mutate=None, report=None):
    case = CASES[name]
    labels = {k: list(v) for k, v in case["expect"].items()}
    rep = report if report is not None else " ".join(
        f"ticket {cid} {' '.join(words)}; ticket {cid} needs the other agent's runtime, conflict with source" for cid, words in case["report"].items())
    if mutate:
        mutate(labels)
    d = os.path.join(out, ".scratch/greeter/issues")
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    for cid, labs in labels.items():
        open(os.path.join(d, f"{cid}-{CHILDREN[cid]['slug']}.md"), "w").write(child_text(cid, labs, case))
    open(os.path.join(out, "REPORT.txt"), "w").write(rep)


def run(name, mutate=None, report=None):
    with tempfile.TemporaryDirectory() as out:
        build(out, name)
        reference(out, name, mutate, report)
        return score(out, name)


def expect(label, got, ok):
    if bool(got) != ok:  # ok=True: the scorer must report failures; False: it must report none
        fails.append(f"{label}: score gave {got or 'PASS'}")


for n in CASES:
    expect(f"reference {n} passes", run(n), False)

expect("unrestricted: derived label dropped", run("unrestricted", lambda l: l.update({"02": ["ready-for-agent"]})), True)
expect("unrestricted: ordinary child labelled", run("unrestricted", lambda l: l.update({"01": ["ready-for-agent", "beta-only"]})), True)
expect("unrestricted: no reason reported", run("unrestricted", report="published both"), True)
expect("inherited: label removed from child", run("inherited", lambda l: l.update({"02": ["ready-for-agent"]})), True)
expect("inherited: switched to other agent", run("inherited", lambda l: l.update({"02": ["ready-for-agent", "beta-only"]})), True)
expect("conflict: relabelled and published", run("conflict", lambda l: l.update({"02": ["ready-for-agent", "beta-only"]})), True)
expect("conflict: published with source label", run("conflict", lambda l: l.update({"02": ["ready-for-agent", "alpha-only"]})), True)
expect("conflict: blocked child published", run("conflict", lambda l: l.update({"03": ["ready-for-agent", "alpha-only"]})), True)
expect("no-mapping: label guessed", run("no-mapping", lambda l: l.update({"02": ["ready-for-agent", "beta-only"]})), True)
expect("milestone: membership label lost", run("milestone", lambda l: l.update({"02": ["ready-for-agent", "beta-only"]})), True)
expect("resume: extra ticket", run("resume", lambda l: l.update({"03": ["ready-for-agent"]})), True)
expect("resume: 02 left unlabelled", run("resume", lambda l: l.update({"02": ["ready-for-agent"]})), True)

# The inherited case's Spec must name alpha's runtime for 02 and never beta's, or a correct run sees a conflict.
with tempfile.TemporaryDirectory() as out:
    build(out, "inherited")
    spec = open(os.path.join(out, ".scratch/greeter/SPEC.md")).read().lower()
    if "beta" in spec:
        fails.append("inherited SPEC.md mentions beta")
    if "alpha" not in spec:
        fails.append("inherited SPEC.md does not name alpha's runtime for 02")

print("\n".join(fails) if fails else "ok")
sys.exit(1 if fails else 0)
