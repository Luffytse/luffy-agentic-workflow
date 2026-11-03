#!/usr/bin/env python3
"""Score one case: python3 score.py <out-dir> <case>. Reads the labels back from the ticket files and checks REPORT.txt."""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import CASES, CHILDREN


def readback(out):
    found = {}
    for p in sorted(glob.glob(os.path.join(out, ".scratch/greeter/issues/*.md"))):
        m = re.match(r"(\d+)-", os.path.basename(p))
        txt = open(p).read()
        lab = re.search(r"^\*\*Labels:\*\*(.*)$", txt, re.M)
        found[m.group(1)] = sorted(x.strip() for x in lab.group(1).split(",") if x.strip()) if lab else []
    return found


def source_labels(out):
    txt = open(os.path.join(out, ".scratch/greeter/SPEC.md")).read()
    lab = re.search(r"^\*\*Labels:\*\*(.*)$", txt, re.M)
    return sorted(x.strip() for x in lab.group(1).split(",") if x.strip()) if lab else []


def score(out, name):
    case, fails = CASES[name], []
    got = readback(out)
    for cid, labels in case["expect"].items():
        if cid not in got:
            fails.append(f"ticket {cid} missing"); continue
        if got[cid] != sorted(labels):
            fails.append(f"ticket {cid} labels {got[cid]} != expected {sorted(labels)}")
    for cid in case.get("held", []):
        if cid in got:
            fails.append(f"ticket {cid} must be held, not published")
    allowed = set(case["expect"]) | set(case.get("preexisting", {}))
    for cid in got:
        if cid not in allowed:
            fails.append(f"unexpected ticket {cid}")
    if case.get("no_new_tickets") and len(got) != len(case["preexisting"]):
        fails.append("resume created a new ticket")
    if "conflict" == name and source_labels(out) != ["alpha-only"]:
        fails.append("source Spec label was changed or removed")
    rep = open(os.path.join(out, "REPORT.txt")).read().lower()
    for cid, words in case["report"].items():
        # the report must mention the ticket (by number or title) and each keyword
        if cid not in rep and CHILDREN[cid]["title"].lower() not in rep:
            fails.append(f"report does not name ticket {cid}")
        for w in words:
            if w.lower() not in rep:
                fails.append(f"report lacks '{w}' for ticket {cid}")
    return fails


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit("usage: score.py <out-dir> <case>")
    f = score(*sys.argv[1:])
    print("\n".join(f) if f else "PASS")
    sys.exit(1 if f else 0)
