#!/usr/bin/env python3
"""Score a dry run of the reuse rule in the milestone skill's Startup verification.

Usage: score.py <out-dir> <case>   (same, runtime, reference, old, failure or failedrow)

The row names that say which rows run now may sit in the Run line or in a line of their own, and `all`, `every row` or
`all seven` stands for every row when every row is expected.
Reads <out-dir>/.scratch/result.md, the comment the coordinator would post. Prints one line per check (PASS or FAIL with
what it saw) and exits 1 when any fails. See evals/startup-verification/README.md.
"""
import re
import sys

LINK = "https://tracker.example/acme/greeter/issues/2#issuecomment-2001"
ROWS = ["Start a worker", "Worker state", "Pause and resume", "Confirmed stop", "End or failure notice",
        "Scheduled check-in", "Loaded skill version"]
LOADED = "Loaded skill version"
# The rows that must be re-run: Loaded skill version always, and per case the rows its conditions fail.
RERUN = {
    "same": {LOADED},
    "runtime": set(ROWS),
    "reference": set(ROWS),
    "old": set(ROWS),
    "failure": {"Confirmed stop", LOADED},
    "failedrow": {"Scheduled check-in", LOADED},
}


# Rows whose re-run is optional in a case: a Confirmed stop re-run needs a probe worker, so the rows that start and read
# one may be marked either way.
OPTIONAL = {"failure": {"Start a worker", "Worker state"}}
RUN_NOW = re.compile(r"\b(?:run|ran)\s+now\b|\brows?\s+(?:run|ran)\b|\bre-?run", re.I)


def parse(text):
    """Return (run_clauses, {row name: (result, evidence)}, has_heading, verdict_line).

    A run clause is a part of a non-table line (split at `;`, `.` and `·`, parentheticals removed and a trailing `reused` remark cut off) that says rows run
    now: it matches RUN_NOW and is not itself a `reused` list. It may be its own line or follow the Harness line."""
    rows, clauses, verdict = {}, [], ""
    for line in text.splitlines():
        if line.startswith("Verdict:"):
            verdict = line
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|"):
            if len(cells) >= 5 and cells[0] in ROWS:
                rows[cells[0]] = (cells[3], cells[4])
            continue
        line = re.sub(r"\([^)]*\)", " ", line)  # a parenthetical (for example "(the six rows are reused)") is not a clause
        for clause in re.split(r"[;.\u00b7]", line):
            # A trailing ", the others are reused" or " - the rest reused" is cut off; what is left must not itself be
            # a reused list.
            parts = re.split(r"(?:,|\s[\u2014\u2013-]\s)", clause)
            kept = []
            for part in parts:
                if "reused" in part.lower():
                    break
                kept.append(part)
            clause = ", ".join(kept)
            if RUN_NOW.search(clause):
                clauses.append(clause)
    return clauses, rows, bool(re.search(r"^## Startup verification\s*$", text, re.M)), verdict


def score(text, case):
    results = []

    def check(name, ok, seen=""):
        results.append(ok)
        print(("PASS " if ok else "FAIL ") + name + ("" if ok or not seen else f": {seen}"))

    clauses, rows, heading, verdict = parse(text)
    rerun, optional = RERUN[case], OPTIONAL.get(case, set())
    check("headed ## Startup verification", heading)
    check("all seven rows present", set(rows) == set(ROWS), f"saw {sorted(rows)}")
    check("a Verdict line", bool(verdict), "none")
    for name in ROWS:
        if name not in rows:
            continue
        result, evidence = rows[name]
        reused = "reused from" in evidence.lower()
        if name in optional:
            check(f"{name} is re-run or reused from the earlier result",
                  bool(evidence) and (not reused or LINK in evidence), f"Evidence reads {evidence!r}")
        elif name in rerun:
            check(f"{name} is re-run", not reused and bool(evidence), f"Evidence reads {evidence!r}")
        else:
            check(f"{name} is reused from the earlier result", reused and LINK in evidence, f"Evidence reads {evidence!r}")
        if reused:
            check(f"{name} reused row keeps Result pass", result.lower() == "pass", f"Result reads {result!r}")
    joined = " ".join(clauses)
    named = {n for n in ROWS if n.lower() in joined.lower()}
    says_all = bool(re.search(r"\ball\b|every row", joined, re.I))
    ok = (rerun <= named <= rerun | optional) or (rerun == set(ROWS) and says_all)
    check("a run-now clause names exactly the rows run now", ok, f"clauses {clauses!r} name {sorted(named)}")
    return all(results), results


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in RERUN:
        sys.exit(__doc__)
    ok, _ = score(open(f"{sys.argv[1]}/.scratch/result.md").read(), sys.argv[2])
    sys.exit(0 if ok else 1)
