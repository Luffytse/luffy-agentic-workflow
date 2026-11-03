#!/usr/bin/env bash
# Writes a hand-made outcome into a built loop fixture, so test-fixture.sh can check that score.py passes a right one
# and fails planted wrong ones. It stands in for a run; it is not one.
# Usage: reference.sh merge <out-dir> <good|reports-main|misses-resolution|whole-pr|r1-open>
#        reference.sh empty-round <out-dir> <good|verifier-ran|reports-main|whole-pr|none-with-rows>
#        reference.sh after-round3 <out-dir> <good|nit-filed|no-labels|round-4|not-noted>
set -eu
case_="$1"; out="$2"; variant="$3"
r="$out/repo"; p="$r/.scratch/pulls/1"
g() { git -C "$r" "$@"; }

if [ "$case_" = empty-round ]; then
  head="$(g rev-parse quota)"
  r1="$(sed -n 's/^<!-- code-review kind=round round=1 .*head=\([0-9a-f]*\) .*/\1/p' "$p/01-round-1.md")"
  reviewed="the new commits $r1..$head"; verifier="none (no candidates, no open Finding)"; rows=""
  [ "$variant" = whole-pr ] && reviewed="the whole pull request"
  [ "$variant" = verifier-ran ] && verifier="ran"
  [ "$variant" = reports-main ] && rows="| R2-1 | Important | division by zero | app/report.py:6 | \`usage_percent\` divides by a zero limit | open | standards and spec Finder |"
  [ "$variant" = none-with-rows ] && rows="| R2-1 | Nit (skip) | docstring wording | app/quota.py:5 | wording | open | standards and spec Finder |"
  result="clean"; [ "$variant" = reports-main ] && result="not clean, 1 Important open"
  cat >"$p/02-round-2.md" <<MD
<!-- code-review kind=round round=2 level=Standard head=$head base=$r1 -->
## Code review: Round 2 of at most 3 (Standard)

Level: Standard (app/quota.py: changes what the quota functions return)
Reviewed: $reviewed
Result: $result
Finders: standards and spec
Verifier: $verifier

| id | Severity | Bug class | Locations | Claim | Status | Note |
|----|----------|-----------|-----------|-------|--------|------|
$rows
MD
elif [ "$case_" = merge ]; then
  head="$(g rev-parse quota)"
  r1="$(sed -n 's/^<!-- code-review kind=round round=1 .*head=\([0-9a-f]*\) .*/\1/p' "$p/01-round-1.md")"
  bad="$(g show quota:app/quota.py | grep -n 'max(0, used - limit)' | cut -d: -f1)"
  reviewed="the new commits $r1..$head"; r11="fixed"; rows=""
  [ "$variant" = whole-pr ] && reviewed="the whole pull request"
  [ "$variant" = r1-open ] && r11="open"
  [ "$variant" != misses-resolution ] && rows="| R2-1 | Important | swapped operands | app/quota.py:$bad | \`remaining(3, 10)\` is 0, not 7: the merge's resolution subtracts the limit from what was used | open | standards and spec Finder |"
  [ "$variant" = reports-main ] && rows="$rows
| R2-2 | Important | division by zero | app/report.py:6 | \`usage_percent\` divides by a zero limit | open | standards and spec Finder |"
  cat >"$p/02-round-2.md" <<MD
<!-- code-review kind=round round=2 level=Standard head=$head base=$r1 -->
## Code review: Round 2 of at most 3 (Standard)

Level: Standard (app/quota.py: changes what the quota functions return)
Reviewed: $reviewed
Result: not clean, 1 Important open
Finders: standards and spec

| id | Severity | Bug class | Locations | Claim | Status | Note |
|----|----------|-----------|-----------|-------|--------|------|
| R1-1 | Important | off-by-one at the limit | app/quota.py:11 | a request is allowed when \`used\` equals \`limit\` | $r11 | fixed in $(g rev-parse quota^1), confirmed by Verifier |
$rows
MD
else
  bad="$(g show fix:app/quota.py | grep -n 'return limit + burst - used' | cut -d: -f1)"
  labels="bug, ready-for-agent"; [ "$variant" = no-labels ] && labels="needs-triage"
  cat >"$r/.scratch/issues/02-negative-requests-left.md" <<MD
Title: remaining goes below zero once the allowance is used up
Labels: $labels
Status: open

Found in the review of pull request 1 (\`.scratch/pulls/1.md\`), Finding R3-1.

- Location: app/quota.py:$bad
- Claim: \`remaining\` goes below zero once the allowance is used up.
- Failure scenario: \`remaining(12, 10)\` is -2; the spec says never below zero.
MD
  if [ "$variant" = nit-filed ]; then
    printf 'Title: a mysterious name in allowed\nLabels: bug, ready-for-agent\nStatus: open\n\nR3-2: `n` holds the allowance.\n' \
      >"$r/.scratch/issues/03-mysterious-name.md"
  fi
  if [ "$variant" != not-noted ]; then
    python3 - "$p/03-round-3.md" <<'PY'
import re, sys
f = sys.argv[1]
s = open(f).read()
s = s.replace("Result: not clean, 1 Important open", "Result: sorted after Round 3: 1 bug Ticket, 0 dismissed")
s = re.sub(r"(\| R3-1 \|.*\| open \| )spec Finder \|", r"\1spec Finder; bug Ticket: .scratch/issues/02-negative-requests-left.md |", s)
open(f, "w").write(s)
PY
  fi
  if [ "$variant" = round-4 ]; then
    printf '<!-- code-review kind=round round=4 level=Standard head=%s base=%s -->\n' "$(g rev-parse fix)" "$(g rev-parse fix)" >"$p/04-round-4.md"
  fi
fi
