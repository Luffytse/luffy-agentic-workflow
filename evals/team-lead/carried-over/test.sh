#!/usr/bin/env bash
# Checks the carried-over case files exist and the prompt and state name no rule the case scores (no cut, no
# "Find where you are", no "Rerun first", no "accounted for", no current Release). It never greps skill text:
# rewording must not fail it.
set -u
root=$(cd "$(dirname "$0")/../../.." && pwd)
d="$root/evals/team-lead/carried-over"
fail=0
for f in STATE.md PROMPT.md EXPECTED.md; do [ -s "$d/$f" ] || { echo "FAIL: missing $f"; fail=1; }; done
if grep -Eiq '\bcut|find where you are|rerun first|accounted for|current release|holds no issue' "$d/PROMPT.md" "$d/STATE.md"; then
  echo "FAIL: PROMPT.md or STATE.md names a rule the case scores"; fail=1
fi
[ $fail = 0 ] && echo "ok"
exit $fail
