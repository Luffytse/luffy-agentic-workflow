#!/usr/bin/env bash
# Builds the Finder and Verifier briefs for a Round 1 of the agentic-review eval's planted fixture, from the current
# review-rounds FINDERS.md, VERIFY.md and DEEP.md (cut out by brief-lib.sh).
# Usage: briefs.sh [--verify-only] <scratch-repo> <quick|standard|deep> [angle-name]
# <scratch-repo> is the directory setup.sh built. The briefs go to <scratch-repo>.briefs/<level>/ (or
# <level>-verify-only/), a sibling of the scratch repo, so no agent working in the scratch repo can find them.
# quick writes finder-standards.md, finder-spec.md and verifier.md; standard adds finder-adversarial.md; deep adds
# finder-security.md too. Each file is complete: paste it whole into one fresh subagent. verifier.md ends with
# placeholder lines where the candidates go, because they exist only after the Finders have run.
# --verify-only writes just verifier.md, with VERIFY-ONLY.md pasted in as the candidates (the Finders never get this).
# The adversarial angle defaults to "Bugs and edge cases", the skill's default; pass another angle name from FINDERS.md.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
verify_only=0
if [ "${1:-}" = "--verify-only" ]; then verify_only=1; shift; fi
usage="usage: briefs.sh [--verify-only] <scratch-repo> <quick|standard|deep> [angle]"
scratch="${1:?$usage}"; level="${2:?$usage}"; angle="${3:-Bugs and edge cases}"
case "$level" in quick|standard|deep) ;; *) echo "level must be quick, standard or deep" >&2; exit 1 ;; esac

skill="$here/../../plugins/dev-skills/skills/review-rounds"
[ -f "$skill/FINDERS.md" ] || { echo "review-rounds skill not found under plugins/dev-skills" >&2; exit 1; }

git -C "$scratch" rev-parse -q --verify main >/dev/null && git -C "$scratch" rev-parse -q --verify planted >/dev/null ||
  { echo "$scratch is not a fixture built by setup.sh (needs branches main and planted)" >&2; exit 1; }
scratch="$(cd "$scratch" && pwd -P)" # absolute, no trailing slash, so the sibling output dir is outside the repo
spec_file="$scratch/.scratch/SPEC.md"
[ -f "$spec_file" ] || { echo "no .scratch/SPEC.md in $scratch" >&2; exit 1; }
review_file="$(mktemp)"; trap 'rm -f "$review_file"' EXIT
git -C "$scratch" show planted:REVIEW.md >"$review_file"
changed="$(git -C "$scratch" diff --name-only main...planted)"
has_index=0
git -C "$scratch" cat-file -e planted:docs/dev-skills/index.md 2>/dev/null && has_index=1

suffix=""; [ "$verify_only" = 1 ] && suffix="-verify-only"
out="$scratch.briefs/$level$suffix"
mkdir -p "$out"; rm -f "$out"/*.md

. "$here/brief-lib.sh"
load_rules "$skill"

skip="$(awk '/^## Skip/{on=1;next} /^## /{on=0} on' "$review_file" | sed -e '/./,$!d')"
inputs="## Inputs for this Round

- The diff command, run in the scratch repo ($scratch): \`git diff main...planted\` (the change is on branch \`planted\`, which is the head). No untracked new files are part of the change.
- The commit list: \`git log --oneline main..planted\`. The base for \`git show main:<file>\` is \`main\`.
- The meaning of Important (\`REVIEW.md\` keeps the default): $important
- The Skip list (\`REVIEW.md\`): $skip
- The Boundary record: none (the fixture has no \`docs/dev-skills/boundaries.md\`)."

candidates=""
[ "$verify_only" = 1 ] && candidates="$(tail -n +2 "$here/VERIFY-ONLY.md")" # without its own "# Candidate Findings" title line
build_briefs "$out" "$level" "$angle" "$inputs" ".scratch/SPEC.md" "$review_file" "$changed" "$has_index" "$candidates"
echo "Briefs for $level${suffix:+ ($suffix)} written to $out:"
ls "$out"
