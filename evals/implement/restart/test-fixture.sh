#!/usr/bin/env bash
# Builds both restart-check fixtures into a scratch directory and checks each holds what its case needs.
# Run: bash evals/implement/restart/test-fixture.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
out="$(mktemp -d)"
fail=0
bad() { echo "FAIL: $*"; fail=1; }
for m in inside outside; do
  d="$out/$m"
  err="$(bash "$here/make-fixture.sh" "$d" "$m" 2>&1 >/dev/null)" || { bad "$m: make-fixture failed"; continue; }
  [ -z "$err" ] || bad "$m: make-fixture wrote to stderr: $err"
  r="$d/repo"; i="$r/.scratch/issues/10-work.md"; p="$r/.scratch/pulls/1.md"
  for op in Park 'Comment on an issue' 'Close a pull request'; do
    grep -q "^- \*\*$op\*\*" "$r/docs/dev-skills/issue-tracker.md" || bad "$m: tracker doc has no $op operation"
  done
  grep -q 'Review depth: Deep' "$i" && bad "$m: work issue still asks for Deep"
  grep -q '^State: open' "$p" 2>/dev/null || bad "$m: pull request 1 is not open"
  git -C "$r" rev-parse --verify -q origin/ticket-10 >/dev/null || { bad "$m: no origin/ticket-10"; continue; }
  head="$(git -C "$r" rev-parse origin/ticket-10)"
  files="$(git -C "$r" diff --name-only origin/main...origin/ticket-10 | sort | tr '\n' ' ')"
  [ "$files" = "docs/dev-skills/adr/0001-greetings-go-to-stdout.md docs/usage.md src/greet.sh tests/bye.sh " ] || bad "$m: unexpected diff files: $files"
  [ "$(git -C "$r" rev-list --count origin/main..origin/ticket-10)" = 3 ] || bad "$m: ticket-10 does not hold the build and two fixes"
  if [ "$m" = inside ]; then
    grep -q '^Labels:.*milestone-1' "$i" || bad "$m: work issue lacks milestone-1"
  else
    grep -q '^Labels:.*milestone-' "$i" && bad "$m: work issue has a Milestone label"
  fi
  grep -q "<!-- code-review kind=attempt attempt=1 pr=1 head=$head -->" "$i" || bad "$m: no attempt record at the branch head"
  grep -q '^Outcome: restart' "$i" || bad "$m: attempt record outcome is not restart"
  grep -q '^Untouched: docs/dev-skills/adr/0001-greetings-go-to-stdout.md, docs/usage.md' "$i" || bad "$m: Untouched line wrong"
  grep -q 'attempt ended: restart (a Finding returned)' "$p" || bad "$m: Round 3 Result is not the restart"
  grep -q 'Result: 5-Round cap reached' "$p" && bad "$m: pull request still shows the retired 5-Round cap Result"
  for sha in $(git -C "$r" rev-list origin/main..origin/ticket-10 --skip=0 --max-count=2); do
    grep -q "${sha:0:7}" "$i" || bad "$m: Tried does not name fix commit $sha"
  done
  grep -q 'restart' "$d/PROMPT.md" || bad "$m: prompt does not plant the restart outcome"
  git -C "$r" rev-parse --verify -q origin/main >/dev/null || bad "$m: no origin/main"
done
rm -rf "$out"
[ "$fail" = 0 ] && echo "OK: restart fixtures" || exit 1
