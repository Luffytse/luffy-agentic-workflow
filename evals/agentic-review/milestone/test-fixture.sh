#!/usr/bin/env bash
# Builds the Milestone-agreement fixture in both cases, builds its briefs, and checks each holds what the eval needs.
# Run: bash evals/agentic-review/milestone/test-fixture.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
skills="$here/../../../plugins/dev-skills/skills"
out="$(mktemp -d)"
fail=0
bad() { echo "FAIL: $*"; fail=1; }

# unchanged <repo> <from> <to> <file>: the file is the same at both commits.
unchanged() { git -C "$1" diff --quiet "$2" "$3" -- "$4"; }
# line_has <repo> <rev> <file> <line> <fixed-text>: that line of the file at rev holds the text.
line_has() { git -C "$1" show "$2:$3" | sed -n "$4p" | grep -qF -- "$5"; }

for case in inside outside; do
  d="$out/$case"
  err="$(bash "$here/make-fixture.sh" "$d" "$case" 2>&1 >/dev/null)" || { bad "$case: make-fixture failed: $err"; continue; }
  [ -z "$err" ] || bad "$case: make-fixture wrote to stderr: $err"
  r="$d/repo"
  for b in main design; do git -C "$r" rev-parse -q --verify "$b" >/dev/null || bad "$case: no branch $b"; done
  git -C "$r" show main:docs/agents/boundaries.md 2>/dev/null | grep -q 'Milestone label form.*milestone-<n>' || bad "$case: Boundary record has no label form"
  grep -q 'docs/agents/boundaries.md' "$r/CLAUDE.md" 2>/dev/null || bad "$case: CLAUDE.md does not point to the Boundary record"
  grep -q '^- \*\*Comment on an issue\*\*' "$r/docs/agents/issue-tracker.md" 2>/dev/null || bad "$case: tracker doc has no Comment on an issue operation"
  m="$r/.scratch/issues/00-milestone.md"; s="$r/.scratch/issues/10-export.md"
  grep -q '^Labels:.*milestone-1' "$m" 2>/dev/null || bad "$case: Milestone issue lacks milestone-1"
  for h in '## Goal' '## Acceptance criteria' '## Excluded'; do grep -q "^$h" "$m" 2>/dev/null || bad "$case: Milestone issue has no $h"; done
  grep -q '^## Decisions' "$s" 2>/dev/null || bad "$case: spec records no decisions"
  grep -q '^- \*\*AC1\*\*.*item,qty,added_by' "$s" 2>/dev/null || bad "$case: spec AC1 does not name the added_by header"
  grep -q 'names of household members' "$m" 2>/dev/null || bad "$case: Milestone exclusion of personal data is missing"
  if [ "$case" = inside ]; then
    grep -q '^Labels:.*milestone-1' "$s" || bad "$case: spec lacks milestone-1"
    grep -q '^### Comment 1' "$s" && grep -q '^### Comment 2' "$s" || bad "$case: spec issue lacks the earlier agent answers"
    grep -q 'R1-2.*(agent)' "$s" || bad "$case: spec comment 1 does not record the agent answer to R1-2"
  else
    grep -q '^Labels:.*milestone-' "$s" && bad "$case: spec carries a Milestone label"
    grep -q '^### Comment' "$s" && bad "$case: spec issue has design-answer comments outside a Milestone"
  fi
  # the change is design-changing: it adds or edits an ADR
  git -C "$r" diff --name-only main...design | grep -q '^docs/adr/' || bad "$case: the diff edits no ADR"
  git -C "$r" diff --name-only main...design | grep -q '^src/export.sh$' || bad "$case: the diff does not add src/export.sh"
  [ "$(git -C "$r" rev-list --count main..design)" = 2 ] || bad "$case: design should hold two commits (the change, then the Round 1 fix)"
  # the earlier Round comment and its kept-design rows
  c="$r/.scratch/pulls/1/01-round-1.md"
  [ -f "$c" ] || { bad "$case: no Round 1 comment"; continue; }
  head -1 "$c" | grep -q '^<!-- code-review kind=round round=1 depth=Standard head=[0-9a-f]\{40\} base=[0-9a-f]\{40\} -->$' || bad "$case: Round 1 marker malformed"
  r1="$(head -1 "$c" | sed 's/.*head=\([0-9a-f]*\).*/\1/')"
  git -C "$r" merge-base --is-ancestor "$r1" design 2>/dev/null || bad "$case: Round 1 head is not on design"
  [ "$r1" != "$(git -C "$r" rev-parse design)" ] || bad "$case: Round 1 head equals design (no Round 1 fix commit)"
  who=user; [ "$case" = inside ] && who=agent
  for row in 'R1-2 .*src/export.sh:6 .*dismissed' 'R1-3 .*src/export.sh:7 .*dismissed'; do
    grep -q "^| $row .*$who keeps the design" "$c" || bad "$case: Round 1 lacks kept row /$row/ by $who"
  done
  [ "$case" = inside ] && { grep -q '#comment-1' "$c" || bad "$case: R1-2 Note has no record link"; }
  unchanged "$r" "$r1" design src/export.sh || bad "$case: src/export.sh changed since Round 1 (kept rows would not bind)"
  line_has "$r" design src/export.sh 6 'while IFS=' || bad "$case: export.sh:6 is not the read loop"
  line_has "$r" design src/export.sh 7 'case "$qty"' || bad "$case: export.sh:7 is not the whole-number check"
  line_has "$r" design src/export.sh 5 'item,qty,added_by' || bad "$case: export.sh:5 is not the header"
  line_has "$r" design src/export.sh 8 "printf '%s,%s,%s" || bad "$case: export.sh:8 is not the raw printf"
  line_has "$r" design docs/adr/0002-export-format.md 3 'separated by commas' || bad "$case: ADR 0002:3 is not the format line"
  git -C "$r" show design:docs/index.md | grep -q '0002' && bad "$case: docs/index.md already lists ADR 0002 (the text Finding needs it missing)"
  # the scoring files stay out of the repo
  [ -z "$(find "$r" -name 'EXPECTED*' -o -name 'DESIGN-FINDINGS*')" ] || bad "$case: a scoring file is inside the repo"
  grep -q '^Expected:' "$d/PROMPT.md" 2>/dev/null || bad "$case: PROMPT.md has no Expected line"
  grep -q 'R2-1' "$d/PROMPT.md" && grep -q 'R2-2' "$d/PROMPT.md" && grep -q 'R2-3' "$d/PROMPT.md" || bad "$case: PROMPT.md lacks the kept Findings"
  grep -q 'DESIGN-FINDINGS\|Keep this file away' "$d/PROMPT.md" && bad "$case: PROMPT.md names or quotes the scoring files' notes"
  # the briefs
  berr="$(bash "$here/briefs.sh" "$d" 2>&1 >/dev/null)" || { bad "$case: briefs.sh failed: $berr"; continue; }
  b="$d/briefs"
  for f in shared.md finder-standards.md finder-spec.md finder-adversarial-1.md finder-adversarial-2.md verifier.md; do
    [ -s "$b/$f" ] || bad "$case: no brief $f"
  done
  grep -q 'Do not propose an alternative a settled decision rejected' "$b/shared.md" || bad "$case: shared brief lacks the settled-designs rule"
  grep -q 'R1-2' "$b/shared.md" && grep -q 'src/export.sh:6' "$b/shared.md" || bad "$case: shared brief lacks the kept row R1-2"
  grep -q 'Do not propose an alternative a settled decision rejected' "$b/verifier.md" || bad "$case: verifier brief lacks the settled-designs rule"
  grep -q 'R1-3' "$b/verifier.md" || bad "$case: verifier brief lacks the kept row R1-3"
  if [ "$case" = inside ]; then
    for n in 1 2; do
      f="$b/design-answer-D$n.md"
      [ -s "$f" ] || { bad "$case: no design-answer brief D$n"; continue; }
      grep -q 'When unsure whether your answer changes the agreement' "$f" && grep -q 'Sort only this Finding' "$f" || bad "$case: D$n brief is not the skill's brief"
      grep -q 'Never run `git checkout`' "$f" || bad "$case: D$n brief lacks the copy rule"
      grep -q 'names of household members' "$f" || bad "$case: D$n brief lacks the Milestone issue"
      grep -q 'item,qty,added_by' "$f" || bad "$case: D$n brief lacks the spec"
    done
    d1t='### Item names with a comma split into extra columns'; d2t="### The export carries household members' names"
    grep -qF "$d1t" "$b/design-answer-D1.md" && ! grep -qF "$d2t" "$b/design-answer-D1.md" || bad "$case: D1 brief does not hold only D1"
    grep -qF "$d2t" "$b/design-answer-D2.md" && ! grep -qF "$d1t" "$b/design-answer-D2.md" || bad "$case: D2 brief does not hold only D2"
    grep -q 'Comment 1' "$b/shared.md" || bad "$case: shared brief lacks the agent answers on the spec issue"
  else
    ls "$b"/design-answer-* >/dev/null 2>&1 && bad "$case: design-answer briefs outside a Milestone"
  fi
  # the control briefs leave the settled designs out
  bash "$here/briefs.sh" "$d" --control >/dev/null 2>&1 || bad "$case: briefs.sh --control failed"
  grep -q 'settled' "$d/briefs-control/shared.md" 2>/dev/null && bad "$case: control brief mentions settled designs"
  [ -s "$d/briefs-control/finder-spec.md" ] || bad "$case: no control spec Finder brief"
  rc="$d/repo-control"
  grep -q "$rc" "$d/briefs-control/shared.md" 2>/dev/null || bad "$case: control briefs do not point at the blind copy"
  [ -f "$rc/.scratch/pulls/1/01-round-1.md" ] && bad "$case: blind copy still holds the Round 1 comment"
  grep -q '^## Decisions\|^## Comments\|sorting' "$rc/.scratch/issues/10-export.md" 2>/dev/null && bad "$case: blind copy's spec still records the settled designs"
  grep -q '^- \*\*AC1\*\*' "$rc/.scratch/issues/10-export.md" 2>/dev/null || bad "$case: blind copy lost the spec"
  [ "$(git -C "$rc" rev-parse design 2>/dev/null)" = "$(git -C "$r" rev-parse design)" ] || bad "$case: blind copy's design branch differs"
  bash "$here/briefs.sh" "$d" --control >/dev/null 2>&1 || bad "$case: briefs.sh --control does not rerun"
done
rm -rf "$out"
[ "$fail" = 0 ] && echo "OK: Milestone-agreement fixtures" || exit 1
