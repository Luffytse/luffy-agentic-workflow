#!/usr/bin/env python3
"""Score one case: python3 score.py <out-dir> <case>. Reads the published ticket files back: how many, and which blocks which."""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import CASES, ITEMS


def readback(out):
    """{ticket number: {"blocked_by": set of numbers, "text": lower-cased file text}} from .scratch/greeter/issues/*.md."""
    found = {}
    for p in sorted(glob.glob(os.path.join(out, ".scratch/greeter/issues/*.md"))):
        m = re.match(r"(\d+)-", os.path.basename(p))
        txt = open(p).read()
        b = re.search(r"^\*\*Blocked by:\*\*(.*)$", txt, re.M | re.I)
        found[m.group(1).zfill(2)] = {"blocked_by": {n.zfill(2) for n in re.findall(r"\d+", b.group(1))} if b else set(), "text": txt.lower()}
    return found


def has(t, key):
    """True when a checkbox (acceptance criterion) line of the ticket text carries the item's key."""
    return any(l.lstrip().startswith("- [") and key in l for l in t["text"].splitlines())


def reach(got, a, b):
    """True when ticket a is blocked by ticket b, directly or through other Tickets."""
    seen, todo = set(), [a]
    while todo:
        n = todo.pop()
        for m in got[n]["blocked_by"]:
            if m == b:
                return True
            if m in got and m not in seen:
                seen.add(m); todo.append(m)
    return False


def score(out, name):
    case, fails = CASES[name], []
    got = readback(out)
    shape = case["shape"]
    nums = sorted(got)
    keys = {c: dict(ITEMS[c], **case["overrides"].get(c, {}))["key"] for c in case["items"]}
    if shape == "grouped":
        if len(got) == 1:
            if not all(has(got[nums[0]], k) for k in keys.values()):
                fails.append("one Ticket published but it does not carry both work items")
        elif len(got) == 2:
            a, b = nums
            ab, ba = a in got[b]["blocked_by"], b in got[a]["blocked_by"]
            if ab == ba:
                fails.append("two Tickets edit the same glossary entry and " + ("block each other" if ab else "neither blocks the other"))
        else:
            fails.append(f"{len(got)} Tickets published, expected one or two")
    elif shape == "pairs":
        home = {c: [n for n in nums if has(got[n], k)] for c, k in keys.items()}
        for c, h in home.items():
            if not h:
                fails.append(f"no Ticket carries work item {c}")
        if not fails:
            x, y = case["pair"]
            hx, hy = home[x], home[y]
            if not (set(hx) & set(hy)) and not any(reach(got, p, q) or reach(got, q, p) for p in hx for q in hy):
                fails.append(f"work items {x} and {y} edit the same glossary entry but share no Ticket and no blocker path")
            if any(reach(got, n, n) for n in nums):
                fails.append("blocking cycle")
            need = [c for c in case["items"] if dict(ITEMS[c], **case["overrides"].get(c, {})).get("needs")]
            for c in need:
                src = dict(ITEMS[c], **case["overrides"].get(c, {}))["needs"]
                if not (set(home[c]) & set(home[src])) and not any(reach(got, p, q) for p in home[c] for q in home[src]):
                    fails.append(f"work item {c} needs {src} in code but is not in its Ticket or blocked by it")
    elif shape == "unblocked":
        if len(got) != 2:
            fails.append(f"{len(got)} Tickets published, expected two")
        for n in nums:
            if got[n]["blocked_by"]:
                fails.append(f"ticket {n} is blocked by {sorted(got[n]['blocked_by'])} though it shares no doc lines")
    elif shape == "chain_to_filed":
        if nums != ["01", "02"]:
            fails.append(f"tickets {nums}, expected 01 (filed) and 02 (new)")
        elif got["02"]["blocked_by"] != {"01"}:
            fails.append(f"ticket 02 blocked by {sorted(got['02']['blocked_by'])}, expected ['01']")
        elif got["01"]["blocked_by"]:
            fails.append("filed ticket 01 gained a blocker")
        elif not has(got["02"], keys["02"]):
            fails.append("ticket 02 does not carry the history item")
    return fails


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit("usage: score.py <out-dir> <case>")
    f = score(*sys.argv[1:])
    print("\n".join(f) if f else "PASS")
    sys.exit(1 if f else 0)
