#!/usr/bin/env python3
"""Self-test: reference runs pass, planted wrong runs fail, and each case's rendered Spec says what the case means
(shared: both items rewrite one glossary entry; separate: two different entries; hidden: the first and third share an entry, the second needs the first in code; different code files and functions; no blocking edge written for the shared entry).
It never reads skill or doc text: rewording must not fail it.
Run: python3 evals/to-tickets-shared-docs/test_cases.py"""
import os, re, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from cases import CASES, ITEMS
from make_fixture import build, ticket_text
from score import score

fails = []


def put(out, num, slug, title, body, blocked=()):
    d = os.path.join(out, ".scratch/greeter/issues")
    os.makedirs(d, exist_ok=True)
    lines = [f"# {num}: {title}", "", "**Labels:** ready-for-agent"]
    if blocked:
        lines += ["", "**Blocked by:** " + ", ".join(blocked)]
    open(os.path.join(d, f"{num}-{slug}.md"), "w").write("\n".join(lines + ["", body, ""]))


def run(name, published):
    """published: list of (num, blocked_by tuple, body). Replaces whatever the fixture put in the issues folder."""
    with tempfile.TemporaryDirectory() as out:
        build(out, name)
        d = os.path.join(out, ".scratch/greeter/issues")
        if os.path.isdir(d):
            for f in os.listdir(d):
                os.remove(os.path.join(d, f))
        for num, blocked, body in published:
            put(out, num, ITEMS[num]["slug"] if num in ITEMS else "merged", ITEMS.get(num, {}).get("title", "merged"), body, blocked)
        return score(out, name)


def expect(label, got, ok):
    if bool(got) != ok:  # ok=True: the scorer must report failures; False: it must report none
        fails.append(f"{label}: score gave {got or 'PASS'}")


B1, B2, B3 = "- [ ] format_greeting shout", "- [ ] record_greeting history", "- [ ] record_shout loud log"
BOTH = B1 + "\n" + B2
expect("shared: blocked chain passes", run("shared", [("01", (), B1), ("02", ("01",), B2)]), False)
expect("shared: reverse chain passes", run("shared", [("01", ("02",), B1), ("02", (), B2)]), False)
expect("shared: one merged Ticket passes", run("shared", [("01", (), BOTH)]), False)
expect("shared: two unblocked Tickets fail", run("shared", [("01", (), B1), ("02", (), B2)]), True)
expect("shared: cycle fails", run("shared", [("01", ("02",), B1), ("02", ("01",), B2)]), True)
expect("shared: one Ticket losing an item fails", run("shared", [("01", (), B1)]), True)
expect("shared: nothing published fails", run("shared", []), True)
expect("separate: two unblocked passes", run("separate", [("01", (), B1), ("02", (), B2)]), False)
expect("separate: needless edge fails", run("separate", [("01", (), B1), ("02", ("01",), B2)]), True)
expect("separate: merged Ticket fails", run("separate", [("01", (), BOTH)]), True)
expect("resume: 02 blocked by 01 passes", run("resume", [("01", (), B1), ("02", ("01",), B2)]), False)
expect("resume: 02 unblocked fails", run("resume", [("01", (), B1), ("02", (), B2)]), True)
expect("resume: 01 gained a blocker fails", run("resume", [("01", ("02",), B1), ("02", ("01",), B2)]), True)
expect("resume: only 01 fails", run("resume", [("01", (), B1)]), True)
expect("resume: 02 without the history item fails", run("resume", [("01", (), B1), ("02", ("01",), "- [ ] something else")]), True)
# hidden: items are 01 shout, 02 loud log (needs 01), 03 history (shares Greeting with 01)
expect("hidden: 02 and 03 each blocked by 01 passes", run("hidden", [("01", (), B1), ("02", ("01",), B3), ("03", ("01",), B2)]), False)
expect("hidden: 03 behind 02 behind 01 passes (path)", run("hidden", [("01", (), B1), ("02", ("01",), B3), ("03", ("02",), B2)]), False)
expect("hidden: 01 and 03 in one Ticket passes", run("hidden", [("01", (), B1 + "\n" + B2), ("02", ("01",), B3)]), False)
expect("hidden: 01 blocked by 03 passes", run("hidden", [("01", ("03",), B1), ("02", ("01",), B3), ("03", (), B2)]), False)
expect("hidden: all in one Ticket passes", run("hidden", [("01", (), B1 + "\n" + B2 + "\n" + B3)]), False)
expect("hidden: only the code edge fails", run("hidden", [("01", (), B1), ("02", ("01",), B3), ("03", (), B2)]), True)
expect("hidden: no edges fails", run("hidden", [("01", (), B1), ("02", (), B3), ("03", (), B2)]), True)
expect("hidden: 02 free of 01 fails", run("hidden", [("01", (), B1), ("02", (), B3), ("03", ("01",), B2)]), True)
expect("hidden: item dropped fails", run("hidden", [("01", (), B1), ("02", ("01",), B3)]), True)
expect("hidden: cycle fails", run("hidden", [("01", ("03",), B1), ("02", ("01",), B3), ("03", ("01",), B2)]), True)


# Rendered input: what the agent reads must say what each case means.
def spec_of(name):
    with tempfile.TemporaryDirectory() as out:
        build(out, name)
        files = {p: open(os.path.join(out, p)).read() for p in (".scratch/greeter/SPEC.md", "PROMPT.md")}
        files["issues"] = sorted(os.listdir(os.path.join(out, ".scratch/greeter/issues"))) if os.path.isdir(os.path.join(out, ".scratch/greeter/issues")) else []
        return files


for n, case in CASES.items():
    f = spec_of(n)
    spec = f[".scratch/greeter/SPEC.md"]
    k = len(case["items"])
    ents = re.findall(r"glossary entry `([^`]+)`", spec)
    codes = re.findall(r"Code: `([^`]+)`", spec)
    if len(ents) != k:
        fails.append(f"{n}: SPEC.md does not name a glossary entry for each of its {k} items")
    if len(codes) != k or len(set(codes)) != k or len({c.split(",")[0] for c in codes}) != k:
        fails.append(f"{n}: SPEC.md items do not name different code files and functions")
    if n == "hidden":
        if k != 3 or not (ents[0] == ents[2] and ents[1] != ents[0]):
            fails.append("hidden: items 01 and 03 must share a glossary entry that item 02 does not")
        if "cannot be built or checked without it" not in spec or len(re.findall(r"Calls item", spec)) != 1:
            fails.append("hidden: SPEC.md must state, for item 02 only, that it needs item 01's shout option")
    else:
        if re.search(r"blocked by|Calls item", spec, re.I):
            fails.append(f"{n}: SPEC.md states a dependency, which the agent must derive")
        same = len(set(ents)) == 1
        if n == "separate" and same:
            fails.append("separate: both items name the same glossary entry")
        if n != "separate" and not same:
            fails.append(f"{n}: items name different glossary entries")
    if (n == "resume") != bool(f["issues"]):
        fails.append(f"{n}: filed-ticket folder does not match the case")
    if (n == "resume") != ("resume" in f["PROMPT.md"]):
        fails.append(f"{n}: PROMPT.md and case disagree about a resumed publication")

print("\n".join(fails) if fails else "ok")
sys.exit(1 if fails else 0)
