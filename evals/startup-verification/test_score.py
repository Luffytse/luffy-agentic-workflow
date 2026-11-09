#!/usr/bin/env python3
"""Self-test of score.py: builds each reuse case with make-fixture.sh, scores a hand-written reference result (which must
pass) and planted wrong results (each must fail). Exits 1 when any expectation fails.

Usage: python3 evals/startup-verification/test_score.py
See evals/startup-verification/README.md.
"""
import contextlib
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score  # noqa: E402

ROWS = score.ROWS


def result(rerun, link=score.LINK, run_now=None, verdict="Verdict: ready"):
    """A result comment: rows in `rerun` read `ran now (simulated)`, the others `reused from <link>`."""
    names = ", ".join(sorted(run_now if run_now is not None else rerun))
    lines = ["## Startup verification", "",
             f"Harness: claude.ai project threads · Run: 2026-11-09T09:00Z-10:30Z UTC; rows run now: {names}",
             "Runtime: claude.ai project; permission mode: default; sandbox: on; tools held: start_thread", "",
             "| Capability | Essential | Method and source | Result | Evidence | Limits |", "|---|---|---|---|---|---|"]
    for n in ROWS:
        ev = "ran now (simulated)" if n in rerun else f"reused from {link}"
        lines.append(f"| {n} | yes | m | pass | {ev} | none |")
    return "\n".join(lines + ["", verdict])


def run(case, text):
    with contextlib.redirect_stdout(io.StringIO()):
        return score.score(text, case)[0]


failures = []


def expect(name, got, want):
    if got != want:
        failures.append(f"{name}: scored {'pass' if got else 'fail'}, expected {'pass' if want else 'fail'}")


for case, rerun in score.RERUN.items():
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, case)
        subprocess.run(["bash", os.path.join(HERE, "make-fixture.sh"), out, case], check=True, stdout=subprocess.DEVNULL)
        for f in ("PROMPT.md", "records/earlier-result.md", "records/harness-now.md", "records/reference-history.md",
                  "records/recorded-failures.md"):
            expect(f"{case} fixture has {f}", os.path.exists(os.path.join(out, f)), True)
        earlier = open(os.path.join(out, "records/earlier-result.md")).read()
        expect(f"{case} fixture link matches the scorer", score.LINK in earlier, True)
    expect(f"{case} reference run", run(case, result(rerun)), True)
    # Planted wrong runs.
    expect(f"{case}: reuses nothing (re-runs every row)", run(case, result(set(ROWS))), rerun == set(ROWS))
    expect(f"{case}: reuses Loaded skill version", run(case, result(rerun - {score.LOADED})), False)
    expect(f"{case}: reused rows without the earlier link", run(case, result(rerun, link="the earlier result")),
           rerun == set(ROWS))
    expect(f"{case}: Run line does not name the rows run now", run(case, result(rerun, run_now=set())), False)
    expect(f"{case}: no Verdict", run(case, result(rerun, verdict="")), False)
    if rerun - {score.LOADED}:
        expect(f"{case}: reuses a row whose conditions fail", run(case, result({score.LOADED})), False)
    if rerun != set(ROWS):
        expect(f"{case}: re-runs one row too many", run(case, result(rerun | {"Start a worker"})), False)

if failures:
    print("\n".join(failures))
    sys.exit(1)
print("ok")
