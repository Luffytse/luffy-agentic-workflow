#!/usr/bin/env bash
# Checks the evidence-owner case files exist and that the three skills carry the mechanism it scores.
set -u
root=$(cd "$(dirname "$0")/../../.." && pwd)
fail=0
chk() { grep -q -- "$2" "$root/$1" || { echo "FAIL: $1 lacks: $2"; fail=1; }; }
for f in TICKET.md PROMPT.md EXPECTED.md; do [ -s "$root/evals/implement/evidence-owner/$f" ] || { echo "FAIL: missing $f"; fail=1; }; done
for s in implement implement-spec; do
  chk plugins/dev-skills/skills/$s/SKILL.md 'PENDING: <the run>'
  chk plugins/dev-skills/skills/$s/SKILL.md 'no added line holds a `PENDING:` marker'
  chk plugins/dev-skills/skills/$s/SKILL.md 'return to step 4 and make the run again'
done
chk plugins/dev-skills/skills/to-tickets/SKILL.md '(evidence from the build thread)'
[ $fail = 0 ] && echo "ok"
exit $fail
