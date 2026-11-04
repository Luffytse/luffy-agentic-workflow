#!/usr/bin/env bash
# Checks the evidence-owner case files exist. It never greps skill text: rewording must not fail it.
set -u
root=$(cd "$(dirname "$0")/../../.." && pwd)
fail=0
for f in TICKET.md PROMPT.md EXPECTED.md; do [ -s "$root/evals/implement/evidence-owner/$f" ] || { echo "FAIL: missing $f"; fail=1; }; done
[ $fail = 0 ] && echo "ok"
exit $fail
