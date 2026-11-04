#!/usr/bin/env bash
# Checks the main-check-report case files exist and the prompt names no rule of the check (no closing state, no
# "as completed", no Milestone agreement). It never greps skill text: rewording must not fail it.
set -u
root=$(cd "$(dirname "$0")/../../.." && pwd)
d="$root/evals/team-lead/main-check-report"
fail=0
for f in STATE.md PROMPT.md EXPECTED.md; do [ -s "$d/$f" ] || { echo "FAIL: missing $f"; fail=1; }; done
if grep -Eiq 'as completed|not planned|agreement|one question|open (its|the) evidence' "$d/PROMPT.md" "$d/STATE.md"; then
  echo "FAIL: PROMPT.md or STATE.md names a rule the case scores"; fail=1
fi
[ $fail = 0 ] && echo "ok"
exit $fail
