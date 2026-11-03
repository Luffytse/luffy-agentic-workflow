#!/usr/bin/env bash
# Checks the mixed-agent case files exist and that the skills carry the continuation mechanism it scores.
set -u
root=$(cd "$(dirname "$0")/../../.." && pwd)
fail=0
chk() { grep -qF -- "$2" "$root/$1" || { echo "FAIL: $1 lacks: $2"; fail=1; }; }
for f in SPEC.md PROMPT.md EXPECTED.md; do [ -s "$root/evals/implement-spec/mixed-agent/$f" ] || { echo "FAIL: missing $f"; fail=1; }; done
s=plugins/dev-skills/skills/implement-spec/SKILL.md
chk $s '**foreign ticket**'
chk $s '**landed**'
chk $s 'Continuation handoff'
chk $s 'for that one ticket only'
chk $s 'continuation Spec pull request'
chk $s 'incomplete handoff'
chk $s 'never rebuilt'
chk $s 'is out'
chk $s 'or the handoff is an incomplete one'
chk $s 'the owner (your thread or session, and how to reach it)'
chk $s "on another agent's worker, go to step 9"
chk $s 'the one the tracker shows closing the ticket'
chk $s 'the owner the handoff names'
chk $s 'one-way-door call on the ticket'
chk $s '**Rejected push.**'
chk $s 'since the branch was recreated'
chk $s 'the body of a merged pull request'
chk $s 'stay open and re-enter at step 1'
chk plugins/dev-skills/skills/team-lead/SKILL.md 'tell the owning Spec worker'
chk plugins/dev-skills/skills/implement/SKILL.md 'and any handoff it was given'
chk plugins/dev-skills/skills/team-lead/SKILL.md 'continuation handoff'
chk docs/dev-skills/adr/0005-a-spec-is-one-long-lived-branch.md 'Amended 2026-11-03 (#513)'
[ $fail = 0 ] && echo "ok"
exit $fail
