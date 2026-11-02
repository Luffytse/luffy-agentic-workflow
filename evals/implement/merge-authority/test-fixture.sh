#!/usr/bin/env bash
# Builds every merge-authority fixture into a scratch directory and checks each holds what its case needs.
# Run: bash evals/implement/merge-authority/test-fixture.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
out="$(mktemp -d)"
fail=0
bad() { echo "FAIL: $*"; fail=1; }
for flow in ticket spec; do
  for case in no-milestone inside-deep-adr inside-boundary; do
    d="$out/$flow-$case"
    err="$(bash "$here/make-fixture.sh" "$d" "$case" "$flow" 2>&1 >/dev/null)" || { bad "$flow/$case: make-fixture failed"; continue; }
    [ -z "$err" ] || bad "$flow/$case: make-fixture wrote to stderr: $err"
    grep -q 'loaded from the same `skills/` folder' "$d/PROMPT.md" 2>/dev/null || bad "$flow/$case: PROMPT.md lost its skills-folder line"
    [ -f "$d/repo/docs/agents/boundaries.md" ] || bad "$flow/$case: no Boundary record"
    grep -q 'Milestone label form' "$d/repo/docs/agents/boundaries.md" 2>/dev/null || bad "$flow/$case: record has no label form"
    git -C "$d/repo" rev-parse --verify -q origin/main >/dev/null || bad "$flow/$case: no origin/main"
    [ -f "$d/PROMPT.md" ] || bad "$flow/$case: no PROMPT.md"
    issue="$d/repo/.scratch/issues/10-work.md"
    [ -f "$issue" ] || { bad "$flow/$case: no work issue"; continue; }
    case "$case" in
      no-milestone) grep -q '^Labels:.*milestone-' "$issue" && bad "$flow/$case: work issue has a Milestone label" ;;
      *) grep -q '^Labels:.*milestone-1' "$issue" || bad "$flow/$case: work issue lacks milestone-1"
         grep -q '^Labels:.*milestone-1' "$d/repo/.scratch/issues/00-milestone.md" 2>/dev/null || bad "$flow/$case: Milestone issue lacks milestone-1" ;;
    esac
    if [ "$case" = inside-deep-adr ]; then
      grep -q 'pull requests bump' "$d/repo/docs/agents/release.md" 2>/dev/null || bad "$flow/$case: release doc does not say pull requests bump"
    else
      [ -f "$d/repo/docs/agents/release.md" ] && bad "$flow/$case: unexpected release doc"
    fi
    [ "$flow" = spec ] && { grep -q '^Type: spec' "$issue" || bad "$flow/$case: work issue is not a Spec"; }
  done
done
rm -rf "$out"
[ "$fail" = 0 ] && echo "OK: merge-authority fixtures" || exit 1
