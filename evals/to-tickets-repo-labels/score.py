#!/usr/bin/env python3
"""Score one case: python3 score.py <out-dir> <case>. Reads the labels back from the ticket files; never reads what the run said."""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import CASES


def labels_of(path):
    lab = re.search(r"^\*\*Labels:\*\*(.*)$", open(path).read(), re.M)
    return sorted(x.strip() for x in lab.group(1).split(",") if x.strip()) if lab else []


def readback(out):
    found = {}
    for p in sorted(glob.glob(os.path.join(out, ".scratch/orders/issues/*.md"))):
        found[re.match(r"(\d+)-", os.path.basename(p)).group(1)] = labels_of(p)
    return found


def score(out, name):
    case, fails = CASES[name], []
    got = readback(out)
    for cid, labels in case["expect"].items():
        if cid not in got:
            fails.append(f"ticket {cid} missing")
        elif got[cid] != sorted(labels):
            fails.append(f"ticket {cid} labels {got[cid]} != expected {sorted(labels)}")
    for cid in got:
        if cid not in case["expect"]:
            fails.append(f"unexpected ticket {cid}")
    if labels_of(os.path.join(out, ".scratch/orders/SPEC.md")) != sorted(case["source_labels"]):
        fails.append("source Spec labels were changed")
    return fails


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit("usage: score.py <out-dir> <case>")
    f = score(*sys.argv[1:])
    print("\n".join(f) if f else "PASS")
    sys.exit(1 if f else 0)
