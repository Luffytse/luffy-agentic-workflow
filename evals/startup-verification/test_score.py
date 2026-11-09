#!/usr/bin/env python3
"""Self-test of score.py: builds each reuse case with make-fixture.sh, scores a hand-written reference result (which must
pass) and planted wrong results (each must fail). Exits 1 when any expectation fails.

Usage: python3 evals/startup-verification/test_score.py
See evals/startup-verification/README.md.
"""
import contextlib
import datetime
import io
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score  # noqa: E402

ROWS = score.ROWS


def result(rerun, link=score.LINK, run_now=None, verdict="Verdict: ready", style="harness", reused_result="pass"):
    """A result comment: rows in `rerun` read `ran now (simulated)`, the others `reused from <link>`. `style` puts the
    run-now clause on the Harness line, on a line of its own after a `Reused:` list, or as `all rows`."""
    names = ", ".join(sorted(run_now if run_now is not None else rerun))
    reused = ", ".join(n for n in ROWS if n not in rerun)
    harness = "Harness: claude.ai project threads · Run: 2026-11-09T09:00Z-10:30Z UTC"
    if style == "harness":
        harness += f"; rows run now: {names}"
    lines = ["## Startup verification", "", harness,
             "Runtime: claude.ai project; permission mode: default; sandbox: on; tools held: start_thread"]
    if style == "own-line":
        lines.append(f"Reused: {reused or 'none'}. Rows run now: {names}")
    elif style == "all":
        lines.append("Rows run now: all rows")
    lines += ["", "| Capability | Essential | Method and source | Result | Evidence | Limits |", "|---|---|---|---|---|---|"]
    for n in ROWS:
        ev = "ran now (simulated)" if n in rerun else f"reused from {link}"
        lines.append(f"| {n} | yes | m | {'pass' if n in rerun else reused_result} | {ev} | none |")
    return "\n".join(lines + ["", verdict])


def run(case, text):
    with contextlib.redirect_stdout(io.StringIO()):
        return score.score(text, case)[0]


def read(out, name):
    return open(os.path.join(out, "records", name)).read()


def conditions(out):
    """Which of the five reuse conditions hold in a built fixture, read from its rendered records: the row passed, the
    Runtime line matches, the reference has no commit after the result was posted, the result is under 30 days old, no
    failure of the row's capability is recorded since. Returns the set of conditions that FAIL."""
    earlier, now = read(out, "earlier-result.md"), read(out, "harness-now.md")
    posted = re.search(r"posted (\d{4}-\d\d-\d\d)", earlier).group(1)
    then = re.search(r"^Runtime: (.*)$", earlier, re.M).group(1)
    nowrt = re.search(r"^Runtime line read now: (.*)$", now, re.M).group(1)
    newest_ref = re.search(r"^- (\d{4}-\d\d-\d\d)", read(out, "reference-history.md"), re.M).group(1)
    age = (datetime.date(2026, 11, 9) - datetime.date.fromisoformat(posted)).days
    failed = set()
    if "| pass |" not in re.search(r"\| Scheduled check-in .*", earlier).group(0):
        failed.add("row result")
    if then != nowrt:
        failed.add("runtime")
    if newest_ref > posted:
        failed.add("reference")
    if age >= 30:
        failed.add("age")
    if "Confirmed stop" in read(out, "recorded-failures.md"):
        failed.add("failure")
    return failed


CONDITIONS = {"same": set(), "runtime": {"runtime"}, "reference": {"reference"}, "old": {"age"},
              "failure": {"failure"}, "failedrow": {"row result"}}


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
        expect(f"{case} fixture input", conditions(out), CONDITIONS[case])
        expect(f"{case} fixture has no Essential value 'no'", "| no |" in earlier, False)
    expect(f"{case} reference run", run(case, result(rerun)), True)
    expect(f"{case} reference run, run-now clause on its own line after Reused:", run(case, result(rerun, style="own-line")), True)
    expect(f"{case}: reused row's Result is not pass", run(case, result(rerun, reused_result="fail")), rerun == set(ROWS))
    if rerun == set(ROWS):
        expect(f"{case} reference run, 'all rows'", run(case, result(rerun, style="all")), True)
    else:
        expect(f"{case}: 'all rows' when only some rows are run", run(case, result(rerun, style="all")), False)
    for extra in score.OPTIONAL.get(case, ()):
        expect(f"{case}: {extra} re-run too is accepted", run(case, result(rerun | {extra})), True)
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
        expect(f"{case}: re-runs one row too many", run(case, result(rerun | {"Pause and resume"})), False)

if failures:
    print("\n".join(failures))
    sys.exit(1)
print("ok")
