#!/usr/bin/env bash
# Builds the briefs for the Milestone-agreement check of the agentic-review eval, word for word from the current
# FINDERS.md, VERIFY.md and ROUNDS.md (cut out by ../brief-lib.sh, which ../briefs.sh shares).
# Usage: briefs.sh <out-dir> [--control]
# <out-dir> is the directory make-fixture.sh built (it holds repo/). The briefs go to <out-dir>/briefs/, outside the repo:
# - the Round 2 Finder and Verifier briefs at Standard depth (shared.md, finder-standards.md, finder-spec.md,
#   finder-adversarial-1.md, finder-adversarial-2.md, verifier.md), with the settled designs (the spec's decisions, the
#   kept-design rows of Round 1 and, inside a Milestone, the agent answers on the spec issue) and the rule FINDERS.md
#   gives with them;
# - inside a Milestone only, design-answer-D1.md and design-answer-D2.md: the design-answer brief from ROUNDS.md with
#   the inputs ROUNDS.md says each agent gets, one planted design Finding (R2-1, R2-2 of DESIGN-FINDINGS.md) each.
# --control writes <out-dir>/briefs-control/ instead: the Finder and Verifier briefs with no settled designs, run
# against <out-dir>/repo-control/, a blind copy of the repo (rebuilt each time) whose spec has no Decisions, no
# comments and no sorting exclusion and which has no Round 1 comment, to see what the Finders raise when nothing
# tells them the designs were settled.
# Each brief file is complete: paste it whole into one fresh subagent. verifier.md ends with a placeholder line where
# the candidate Findings go, because they exist only after the Finders have run.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
dir="${1:?usage: briefs.sh <out-dir> [--control]}"
control=0; [ "${2:-}" = --control ] && control=1
r="$dir/repo"
git -C "$r" rev-parse -q --verify design >/dev/null || { echo "$dir is not a fixture built by make-fixture.sh (no repo/ with branch design)" >&2; exit 1; }
r="$(cd "$r" && pwd -P)"; dir="$(cd "$dir" && pwd -P)"
spec_file="$r/.scratch/issues/10-export.md"; milestone_file="$r/.scratch/issues/00-milestone.md"; round1="$r/.scratch/pulls/1/01-round-1.md"
for f in "$spec_file" "$milestone_file" "$round1"; do [ -f "$f" ] || { echo "missing $f" >&2; exit 1; }; done
inside=0; grep -q '^Labels:.*milestone-1' "$spec_file" && inside=1

skill="$here/../../../plugins/dev-skills/skills/agentic-review"
[ -f "$skill/ROUNDS.md" ] || { echo "agentic-review skill not found under plugins/dev-skills" >&2; exit 1; }
skill="$(cd "$skill" && pwd -P)"
. "$here/../brief-lib.sh"
load_rules "$skill"

out="$dir/briefs"; [ "$control" = 1 ] && out="$dir/briefs-control"
mkdir -p "$out"

if [ "$control" = 1 ]; then
  rm -rf "$dir/repo-control"
  cp -R "$r" "$dir/repo-control"
  r="$dir/repo-control"; spec_file="$r/.scratch/issues/10-export.md"
  rm -f "$r/.scratch/pulls/1/01-round-1.md"
  # drop the Decisions and Comments sections, and sorting from the exclusions
  awk '/^## / { skip = ($0 == "## Decisions" || $0 == "## Comments") } !skip' "$spec_file" |
    sed 's/^- Import, and sorting\.$/- Import./' >"$spec_file.tmp"
  mv "$spec_file.tmp" "$spec_file"
fi

review="$(git -C "$r" show design:REVIEW.md)"
diffs="- The diff command, run in the repo ($r): \`git diff main...design\` (Round 2 reviews the whole pull request; its head is branch \`design\`).
- The commit list: \`git log --oneline main..design\`. The base for \`git show main:<file>\` is \`main\`."

settled=""
if [ "$control" = 0 ]; then
  rule="$(bullet_quote "$finders" '^- The \*\*settled designs\*\*' 'with:')"; must "the settled-designs bullet" "$rule"
  decisions="$(section "$spec_file" '## Decisions' | tail -n +2)"; must "the spec's decisions" "$decisions"
  kept="$(grep -e '^| R[0-9]*-[0-9]* .*| dismissed | .*keeps the design' "$round1")"; must "Round 1's kept-design rows" "$kept"
  answers=""
  if [ "$inside" = 1 ]; then
    answers="$(section "$spec_file" '## Comments' | tail -n +2)"; must "the agent answers on the spec issue" "$answers"
    answers="
Design answers recorded as comments on the spec issue (\`.scratch/issues/10-export.md\`):
$answers"
  fi
  settled="
- The settled designs. $rule

The decisions the spec records:
$decisions

Rows of earlier Round comments dismissed because the design was kept (their locations are unchanged at this head, \`src/export.sh\` being the same file since Round 1's head):

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
$kept
$answers"
fi

inputs="## Inputs for this Review

$diffs
- The spec: \`.scratch/issues/10-export.md\` in the repo (read it whole). It builds a feature of the Milestone in \`.scratch/issues/00-milestone.md\`.$settled
- The standards-source files: \`CLAUDE.md\` and \`REVIEW.md\` in the repo.
- \`REVIEW.md\`, as follows. It has an Always check line.

\`\`\`
$review
\`\`\`

- The meaning of Important (\`REVIEW.md\` keeps the default): $important"

build_briefs "$out" standard "Bugs and edge cases" "Contradictions" 0 "$inputs"

# finding <id>: one planted Finding from DESIGN-FINDINGS.md, its tag line included, up to the next tag line.
finding() { awk -v id="$1" '/^#### R/ { on = (index($0, "#### " id " ") == 1) } on' "$here/DESIGN-FINDINGS.md"; }

if [ "$inside" = 1 ] && [ "$control" = 0 ]; then
  brief="$(quoted "$(section "$skill/ROUNDS.md" '#### Design-answer brief')")"; must "the design-answer brief" "$brief"
  n=0
  for id in R2-1 R2-2; do
    n=$((n + 1))
    f="$(finding "$id")"; must "Finding $id in DESIGN-FINDINGS.md" "$f"
    {
      printf '%s\n\n' "$brief"
      printf '## The Finding\n\n%s\n\n' "$f"
      printf '## The Milestone issue (`.scratch/issues/00-milestone.md`)\n\n```\n%s\n```\n\n' "$(cat "$milestone_file")"
      printf '## The spec, with its comments (`.scratch/issues/10-export.md`)\n\n```\n%s\n```\n\n' "$(cat "$spec_file")"
      printf '## The ADR and glossary lines the Finding touches\n\n'
      for p in docs/dev-skills/adr/0001-the-list-is-a-text-file.md docs/dev-skills/adr/0002-export-format.md docs/dev-skills/glossary.md; do
        printf '`%s` at the head:\n\n```\n%s\n```\n\n' "$p" "$(git -C "$r" show "design:$p")"
      done
      printf '## The diff commands\n\n%s\n\n' "$diffs"
      printf '## Copy rule\n\n%s\n' "$copy_rule"
    } >"$out/design-answer-D$n.md"
  done
fi

echo "Briefs written to $out:"
ls "$out"
