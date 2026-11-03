#!/usr/bin/env bash
# Builds both park-check fixtures into a scratch directory and checks each holds what its case needs.
# Run: bash evals/implement-spec/park/test-fixture.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
out="$(mktemp -d)"
fail=0
bad() { echo "FAIL: $*"; fail=1; }
for m in inside outside; do
  d="$out/$m"
  err="$(bash "$here/make-fixture.sh" "$d" "$m" 2>&1 >/dev/null)" || { bad "$m: make-fixture failed"; continue; }
  [ -z "$err" ] || bad "$m: make-fixture wrote to stderr: $err"
  r="$d/repo"; i="$r/.scratch/issues"
  grep -q '^- \*\*Park\*\*' "$r/docs/dev-skills/issue-tracker.md" || bad "$m: tracker doc has no Park operation"
  grep -q '^- \*\*Comment on an issue\*\*' "$r/docs/dev-skills/issue-tracker.md" || bad "$m: tracker doc has no Comment on an issue operation"
  grep -q 'contradict\|nothing to standard output' "$i/11-code.md" || bad "$m: Ticket 11 is not planted"
  grep -q '^Blocked by: .scratch/issues/11-code.md' "$i/12-adr.md" || bad "$m: Ticket 12 is not blocked by 11"
  grep -q '^Blocked by: none' "$i/13-usage.md" || bad "$m: Ticket 13 is not free"
  grep -q 'Review depth: Deep' "$i/10-work.md" && bad "$m: Spec still asks for Deep"
  if [ "$m" = inside ]; then
    grep -q '^Labels:.*milestone-1' "$i/10-work.md" || bad "$m: Spec lacks milestone-1"
    grep -q 'Outcome: park' "$d/PROMPT.md" || bad "$m: Expected does not name the park outcome"
  else
    grep -q '^Labels:.*milestone-' "$i/10-work.md" && bad "$m: Spec has a Milestone label"
    grep -q 'no attempt record' "$d/PROMPT.md" || bad "$m: Expected does not rule out the attempt record"
  fi
  git -C "$r" rev-parse --verify -q origin/main >/dev/null || bad "$m: no origin/main"
done
rm -rf "$out"
[ "$fail" = 0 ] && echo "OK: park fixtures" || exit 1
