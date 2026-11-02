#!/usr/bin/env bash
# Builds the Finder and Verifier briefs for a run of the agentic-review eval, from the current FINDERS.md and VERIFY.md
# (cut out by brief-lib.sh, which milestone/briefs.sh shares).
# Usage: briefs.sh [--verify-only] <scratch-repo> <standard|deep> [angle-name angle-name]
# <scratch-repo> is the directory setup.sh built. The briefs go to <scratch-repo>.briefs/<depth>/ (or
# <depth>-verify-only/), a sibling of the scratch repo, so no agent working in the scratch repo can find them.
# A full run writes: shared.md, finder-standards.md, finder-spec.md, finder-adversarial-1.md and finder-adversarial-2.md;
# Deep adds finder-security.md and finder-gap-sweep.md. Standard writes verifier.md; Deep writes verifier-tracer.md,
# verifier-skeptic.md and verifier-spec-checker.md instead.
# Each brief file is complete: paste it whole into one fresh subagent. verifier*.md ends with a placeholder line where
# the candidate Findings go, because they exist only after the Finders have run.
# --verify-only writes just the Verifier briefs for the Verify-only check, with VERIFY-ONLY.md pasted in as the
# candidates (the Finders never get this; build it after, or away from, a full run's agents).
# Angles default to the ones every run so far used (Standard: bugs and edge cases + security and privacy; Deep: bugs and
# edge cases + money, numbers and time), so runs stay comparable; pass two angle names from FINDERS.md to change them.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
verify_only=0
if [ "${1:-}" = "--verify-only" ]; then verify_only=1; shift; fi
scratch="${1:?usage: briefs.sh [--verify-only] <scratch-repo> <standard|deep> [angle angle]}"
depth="${2:?usage: briefs.sh [--verify-only] <scratch-repo> <standard|deep> [angle angle]}"
case "$depth" in standard|deep) ;; *) echo "depth must be standard or deep" >&2; exit 1 ;; esac
case "$depth" in
  standard) angle1="${3:-Bugs and edge cases}"; angle2="${4:-Security and privacy}" ;;
  deep) angle1="${3:-Bugs and edge cases}"; angle2="${4:-Money, numbers and time}" ;;
esac

skill=""
d="$here/../../plugins/dev-skills/skills/agentic-review"
[ -f "$d/FINDERS.md" ] && skill="$d"
[ -n "$skill" ] || { echo "agentic-review skill not found under plugins/dev-skills" >&2; exit 1; }

git -C "$scratch" rev-parse -q --verify main >/dev/null && git -C "$scratch" rev-parse -q --verify planted >/dev/null ||
  { echo "$scratch is not a fixture built by setup.sh (needs branches main and planted)" >&2; exit 1; }
scratch="$(cd "$scratch" && pwd -P)" # absolute, no trailing slash, so the sibling output dir is outside the repo
[ -f "$scratch/.scratch/SPEC.md" ] || { echo "no .scratch/SPEC.md in $scratch" >&2; exit 1; }
review="$(git -C "$scratch" show planted:REVIEW.md)"
git -C "$scratch" cat-file -e planted:docs/index.md ||
  { echo "the fixture has no docs/index.md; the Standards Finder brief assumes it has one" >&2; exit 1; }
printf '%s\n' "$review" | grep -q '^- \*\*' ||
  { echo "the fixture's REVIEW.md has no Always check line; the Standards Finder brief assumes it has one" >&2; exit 1; }

suffix=""
[ "$verify_only" = 1 ] && suffix="-verify-only"
out="$scratch.briefs/$depth$suffix"
mkdir -p "$out"

. "$here/brief-lib.sh"
load_rules "$skill"

inputs="## Inputs for this Review

- The diff command, run in the scratch repo ($scratch): \`git diff --merge-base main\` (the change is on branch \`planted\`, which is the head). No untracked new files are part of the change.
- The commit list: \`git log --oneline main..planted\`. The base for \`git show main:<file>\` is \`main\`.
- The spec: \`.scratch/SPEC.md\` in the scratch repo.
- The settled designs: none (there is no earlier Round, and the spec records no decisions).
- The standards-source files: the fixture has no \`CLAUDE.md\`, \`AGENTS.md\` or \`CODING_STANDARDS.md\`; its \`REVIEW.md\` is the whole list.
- \`REVIEW.md\`, as follows. It has an Always check line.

\`\`\`
$review
\`\`\`

- The meaning of Important (\`REVIEW.md\` keeps the default): $important"

candidates=""
[ "$verify_only" = 1 ] && candidates="$(tail -n +2 "$here/VERIFY-ONLY.md")" # without its own "# Candidate Findings" title line
build_briefs "$out" "$depth" "$angle1" "$angle2" "$verify_only" "$inputs" "$candidates"
echo "Briefs for $depth${suffix:+ ($suffix)} written to $out:"
ls "$out"
