#!/usr/bin/env bash
# Builds every merge-authority fixture into a scratch directory and checks each holds what its case needs.
# Run: bash evals/implement/merge-authority/test-fixture.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
out="$(mktemp -d)"
fail=0
bad() { echo "FAIL: $*"; fail=1; }
for flow in ticket spec; do
  for case in no-milestone inside-deep-adr inside-boundary retro-inside retro-outside unrelated-no-issue; do
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
      no-milestone|retro-outside) grep -q '^Labels:.*milestone-' "$issue" && bad "$flow/$case: work issue has a Milestone label" ;;
      *) grep -q '^Labels:.*milestone-1' "$issue" || bad "$flow/$case: work issue lacks milestone-1"
         grep -q '^Labels:.*milestone-1' "$d/repo/.scratch/issues/00-milestone.md" 2>/dev/null || bad "$flow/$case: Milestone issue lacks milestone-1" ;;
    esac
    case "$case" in
      retro-inside|retro-outside|unrelated-no-issue)
        [ -f "$d/DECISION.md" ] || bad "$flow/$case: no decision prompt"
        [ -f "$d/repo/REVIEW.md" ] || bad "$flow/$case: no review rule change"
        git -C "$d/repo" diff --name-only origin/main...HEAD | grep -q '^REVIEW.md$' || bad "$flow/$case: review change is not on branch"
        if [ "$case" = unrelated-no-issue ]; then
          grep -q '^Retro origin:' "$d/repo/.scratch/pulls/1.md" && bad "$flow/$case: unrelated PR has origin"
        else
          grep -q '^Retro origin: .scratch/issues/10-work.md$' "$d/repo/.scratch/pulls/1.md" || bad "$flow/$case: missing origin input"
        fi
        ;;
    esac
    if [ "$case" = inside-deep-adr ]; then
      grep -q 'pull requests bump' "$d/repo/docs/agents/release.md" 2>/dev/null || bad "$flow/$case: release doc does not say pull requests bump"
      if [ "$flow" = spec ]; then grep -q 'score it on main' "$d/PROMPT.md" || bad "$flow/$case: Expected does not score the bump on main"
      else grep -q 'last commit before the squash' "$d/PROMPT.md" || bad "$flow/$case: Expected does not score the bump before the squash"; fi
    else
      [ -f "$d/repo/docs/agents/release.md" ] && bad "$flow/$case: unexpected release doc"
    fi
    [ "$flow" = spec ] && { grep -q '^Type: spec' "$issue" || bad "$flow/$case: work issue is not a Spec"; }
  done
done
rm -rf "$out"
[ "$fail" = 0 ] && echo "OK: merge-authority fixtures" || exit 1
