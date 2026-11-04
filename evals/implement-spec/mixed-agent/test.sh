#!/usr/bin/env bash
# Checks the mixed-agent case files exist. It never greps skill, ADR or doc text: rewording must not fail it.
set -u
root=$(cd "$(dirname "$0")/../../.." && pwd)
fail=0
for f in SPEC.md PROMPT.md EXPECTED.md; do [ -s "$root/evals/implement-spec/mixed-agent/$f" ] || { echo "FAIL: missing $f"; fail=1; }; done
[ $fail = 0 ] && echo "ok"
exit $fail
