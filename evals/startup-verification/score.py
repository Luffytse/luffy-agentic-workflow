#!/usr/bin/env python3
"""Score a dry run of the reuse rule in the milestone skill's Startup verification.

Usage: score.py <out-dir> <case>   (same, runtime, reference, old, failure or failedrow)
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


def parse(text):
    """Return (run_line, {row name: (result, evidence)}, has_heading, verdict_line)."""
    rows, run_line, verdict = {}, "", ""
    for line in text.splitlines():
        if re.search(r"\bRun:", line):
            run_line = line
        if line.startswith("Verdict:"):
            verdict = line
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 5 and cells[0] in ROWS:
            rows[cells[0]] = (cells[3], cells[4])
    return run_line, rows, bool(re.search(r"^## Startup verification\s*$", text, re.M)), verdict


def score(text, case):
    results = []

    def check(name, ok, seen=""):
        results.append(ok)
        print(("PASS " if ok else "FAIL ") + name + ("" if ok or not seen else f": {seen}"))

    run_line, rows, heading, verdict = parse(text)
    rerun = RERUN[case]
    check("headed ## Startup verification", heading)
    check("all seven rows present", set(rows) == set(ROWS), f"saw {sorted(rows)}")
    check("a Verdict line", bool(verdict), "none")
    for name in ROWS:
        if name not in rows:
            continue
        evidence = rows[name][1]
        reused = "reused from" in evidence.lower()
        if name in rerun:
            check(f"{name} is re-run", not reused and bool(evidence), f"Evidence reads {evidence!r}")
        else:
            check(f"{name} is reused from the earlier result", reused and LINK in evidence, f"Evidence reads {evidence!r}")
    ran_named = {n for n in ROWS if n.lower() in run_line.lower()}
    says_all = rerun == set(ROWS) and "all rows" in run_line.lower()
    check("Run line names exactly the rows run now", ran_named == rerun or says_all,
          f"Run line {run_line!r} names {sorted(ran_named)}")
    return all(results), results


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in RERUN:
        sys.exit(__doc__)
    ok, _ = score(open(f"{sys.argv[1]}/.scratch/result.md").read(), sys.argv[2])
    sys.exit(0 if ok else 1)
