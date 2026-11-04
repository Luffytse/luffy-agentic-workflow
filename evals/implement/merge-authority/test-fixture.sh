#!/usr/bin/env bash
# Builds every merge-authority fixture into a scratch directory and checks each holds what its case needs.
# Run: bash evals/implement/merge-authority/test-fixture.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
out="$(mktemp -d)"
fail=0
bad() { echo "FAIL: $*"; fail=1; }
for flow in ticket spec; do
  for case in no-milestone inside-deep-adr inside-boundary outside-boundary no-record-twoway no-record-oneway retro-inside retro-outside unrelated-no-issue; do
    d="$out/$flow-$case"
    err="$(bash "$here/make-fixture.sh" "$d" "$case" "$flow" 2>&1 >/dev/null)" || { bad "$flow/$case: make-fixture failed"; continue; }
    [ -z "$err" ] || bad "$flow/$case: make-fixture wrote to stderr: $err"
    grep -q 'loaded from the same `skills/` folder' "$d/PROMPT.md" 2>/dev/null || bad "$flow/$case: PROMPT.md lost its skills-folder line"
    case "$case" in
      no-record-*)
        [ -e "$d/repo/docs/dev-skills/boundaries.md" ] && bad "$flow/$case: a no-record case has a Boundary record"
        grep -rqi 'boundar' "$d/repo/CLAUDE.md" "$d/repo/docs/dev-skills/index.md" 2>/dev/null && bad "$flow/$case: a no-record case still points at a Boundary record"
        [ -e "$d/repo/.scratch/issues/00-milestone.md" ] && bad "$flow/$case: a no-record case has a Milestone issue" ;;
      *)
        [ -f "$d/repo/docs/dev-skills/boundaries.md" ] || bad "$flow/$case: no Boundary record"
        grep -q 'Milestone label form' "$d/repo/docs/dev-skills/boundaries.md" 2>/dev/null || bad "$flow/$case: record has no label form"
        grep -q 'wins over this record' "$d/repo/docs/dev-skills/boundaries.md" && bad "$flow/$case: record lets a Milestone issue win over it"
        grep -q '^## Boundaries' "$d/repo/.scratch/issues/00-milestone.md" 2>/dev/null && bad "$flow/$case: Milestone issue holds boundaries of its own" ;;
    esac
    # One merge rule, one listing line: no fixture text uses the old line name or the old membership split.
    grep -rlE 'Milestone review:|outside-a-Milestone|inside list|outside list' "$d/PROMPT.md" "$d/DECISION.md" "$d/repo" --exclude-dir=.git 2>/dev/null | grep -q . && bad "$flow/$case: fixture text keeps the old line name or the old inside/outside split"
    exp="$(grep '^Expected:' "$d/PROMPT.md" 2>/dev/null)"
    case "$case" in
      no-milestone|inside-deep-adr|no-record-twoway)
        case "$exp" in *'Merged by the thread'*'Agent-merged rules:'*) ;; *) bad "$flow/$case: Expected is not an agent merge with the Agent-merged rules: line" ;; esac ;;
      inside-boundary|outside-boundary|no-record-oneway)
        case "$exp" in 'Expected: Brought to the user, not merged'*) ;; *) bad "$flow/$case: Expected is not a hand-over" ;; esac
        case "$exp" in *'Agent-merged rules:'*) bad "$flow/$case: a hand-over Expected asks for the listing line" ;; esac ;;
    esac
    case "$case" in
      outside-boundary|no-record-oneway) grep -q 'migrations/002_purge' "$d/repo/.scratch/issues/10-work.md" 2>/dev/null || bad "$flow/$case: work issue has no one-way migration" ;;
    esac
    git -C "$d/repo" rev-parse --verify -q origin/main >/dev/null || bad "$flow/$case: no origin/main"
    [ -f "$d/PROMPT.md" ] || bad "$flow/$case: no PROMPT.md"
    # The review has no depth, attempts, restart, park outcome or rebuttals any more: no fixture text may ask for them.
    grep -rlEi 'depth|attempt|convergence|rebuttal|restart' "$d/PROMPT.md" "$d/DECISION.md" "$d/repo/.scratch" "$d/repo/docs" 2>/dev/null | grep -q . && bad "$flow/$case: fixture names a removed review rule"
    issue="$d/repo/.scratch/issues/10-work.md"
    [ -f "$issue" ] || { bad "$flow/$case: no work issue"; continue; }
    grep -q '^Review level: Deep' "$issue" || bad "$flow/$case: work issue does not ask for a Deep review level"
    case "$case" in
      no-milestone|retro-outside|outside-boundary|no-record-*) grep -q '^Labels:.*milestone-' "$issue" && bad "$flow/$case: work issue has a Milestone label" ;;
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
      grep -q 'pull requests bump' "$d/repo/docs/dev-skills/release.md" 2>/dev/null || bad "$flow/$case: release doc does not say pull requests bump"
      if [ "$flow" = spec ]; then grep -q 'score it on main' "$d/PROMPT.md" || bad "$flow/$case: Expected does not score the bump on main"
      else grep -q 'last commit before the squash' "$d/PROMPT.md" || bad "$flow/$case: Expected does not score the bump before the squash"; fi
    else
      [ -f "$d/repo/docs/dev-skills/release.md" ] && bad "$flow/$case: unexpected release doc"
    fi
    [ "$flow" = spec ] && { grep -q '^Type: spec' "$issue" || bad "$flow/$case: work issue is not a Spec"; }
  done
done
# The skills under test hold one merge rule: both name the listing line, and implement-spec keeps no inside/outside merge list.
skills="$here/../../../plugins/dev-skills/skills"
for s in implement implement-spec; do
  grep -q 'Agent-merged rules:' "$skills/$s/SKILL.md" || bad "$s: SKILL.md does not name the Agent-merged rules: line"
  grep -qiE 'Milestone review:|(inside|outside) a Milestone\*{0,2}, bring' "$skills/$s/SKILL.md" && bad "$s: SKILL.md keeps the old line name or an inside/outside merge list"
  grep -qiE "Milestone issue's own boundaries|Milestone-issue test" "$skills/$s/SKILL.md" && bad "$s: SKILL.md still reads a Milestone issue's own boundaries at merge"
done
# The merge rule lives in the merging Base skill (Spec #641): implement loads it and keeps no copy of the rule and no merge command.
[ -f "$skills/merging/SKILL.md" ] || bad "merging: no SKILL.md"
grep -q '`merging`' "$skills/implement/SKILL.md" || bad "implement: SKILL.md does not load merging"
grep -qE 'Read the Boundary record|gh (pr|api)[^`]*merge|Bump the version' "$skills/implement/SKILL.md" && bad "implement: SKILL.md keeps its own Boundary reading, bump step or merge command"
rm -rf "$out"
[ "$fail" = 0 ] && echo "OK: merge-authority fixtures" || exit 1
