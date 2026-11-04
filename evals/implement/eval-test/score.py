#!/usr/bin/env python3
"""Score an eval-test run: <out-dir>/plan.md, the Implementer's plan for a Ticket that changes only skill text.

Usage: score.py <out-dir>
Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any fails. It reads the plan's fields,
never the skill's text. Passing: the test is an eval (not a sentence grep, not a code test); it is compared with a
baseline (main's or the default branch's version); the Implementer chose the seam itself; the evidence names a run or
a stated gap, not a grep.
"""
import json
import pathlib
import re
import sys

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
from make_fixture import tree_hash  # noqa: E402

FIELDS = ("TEST", "FIXTURE", "BASELINE", "SEAM-CONFIRMED-BY", "EVIDENCE")
NEGATED_GREP = re.compile(r"\b(not|no|never|instead of|rather than|without)\s+(a\s+|any\s+)?(sentence\s+)?grep\b", re.I)


def fields(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r"\s*[-*]?\s*\**(" + "|".join(FIELDS) + r")\**\s*:\s*(.*)", line)
        if m and m.group(1) not in out:
            out[m.group(1)] = m.group(2).strip().strip("*").strip()
    return out


def score(out):
    out = pathlib.Path(out)
    fx = json.loads((out / "fixture.json").read_text())
    plan = out / "plan.md"
    f = fields(plan.read_text()) if plan.exists() else {}
    results = []

    def check(name, ok, seen=""):
        results.append(bool(ok))
        print(("PASS " if ok else "FAIL ") + name + ("" if ok or not seen else f": {seen}"))

    check("dry run: nothing but plan.md was written", tree_hash(out) == fx["tree"])
    check("plan.md has all five fields", all(f.get(k) for k in FIELDS), ", ".join(k for k in FIELDS if not f.get(k)) + " missing")
    kind = f.get("TEST", "").lower()
    check("test is an eval, not a sentence grep or a code test", re.match(r"eval\b", kind) is not None, f.get("TEST", ""))
    check("the work is compared with a baseline version", re.search(r"\b(main|default branch|baseline|previous|old version|before|current|existing|unchanged|original|HEAD|origin)\b", f.get("BASELINE", ""), re.I), f.get("BASELINE", ""))
    check("the Implementer chose the seam, not the user", re.match(r"me\b", f.get("SEAM-CONFIRMED-BY", ""), re.I) is not None, f.get("SEAM-CONFIRMED-BY", ""))
    ev = NEGATED_GREP.sub("", f.get("EVIDENCE", ""))
    check("evidence names the eval run or a stated gap", re.search(r"\b(run|runs|ran|result|results|score|scores|output|gap)\b", ev, re.I), f.get("EVIDENCE", ""))
    check("evidence is not a grep", not re.search(r"\bgrep\b", ev, re.I), f.get("EVIDENCE", ""))
    return all(results)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    sys.exit(0 if score(sys.argv[1]) else 1)
