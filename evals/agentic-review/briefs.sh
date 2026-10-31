#!/usr/bin/env bash
# Builds the Finder and Verifier briefs for a run of the agentic-review eval, from the current FINDERS.md and VERIFY.md.
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
finders="$skill/FINDERS.md"
verify="$skill/VERIFY.md"

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

# section <file> <heading-prefix>: the heading line and everything under it up to the next heading of the same or a
# higher level. A line inside a code fence is never a heading, so the `### <short title>` of the Finding format
# does not end its section.
section() {
  awk -v prefix="$2" '
    function level(s) { match(s, /^#+/); return RLENGTH }
    {
      isfence = ($0 ~ /^```/)
      if (!fence && !isfence && $0 ~ /^#+ /) {
        if (!on && index($0, prefix) == 1) { on = 1; lvl = level($0); print; next }
        if (on && level($0) <= lvl) exit
      }
      if (on) print
      if (isfence) fence = !fence
    }' "$1"
}

# quoted <text>: the first quoted brief ("Brief: "..." or a paragraph in quotes), which may run over several lines,
# without its quote marks.
quoted() {
  printf '%s\n' "$1" | awk '
    !on && /^(Brief: )?"/ { on = 1; sub(/^(Brief: )?"/, "") }
    on { if ($0 ~ /"$/) { sub(/"$/, ""); print; exit } print }'
}

# bullet_quote <pattern> <after>: the quoted text after <after> on the FINDERS.md bullet matching <pattern>.
bullet_quote() { grep -m1 -e "$1" "$finders" | sed -e "s/^.*$2 \"//" -e 's/"$//'; }

must() { [ -n "$2" ] || { echo "could not find $1 in the current FINDERS.md or VERIFY.md; the script needs updating" >&2; exit 1; }; }

format="$(section "$finders" '## Finding format')"; must "the Finding format" "$format"
report_rule="$(bullet_quote '^- The \*\*Finding format\*\*' 'with:')"; must "the Finding format bullet" "$report_rule"
copy_rule="$(bullet_quote '^- The \*\*copy rule\*\*' 'pasted in full:')"; must "the copy rule" "$copy_rule"
important="$(grep -m1 -o 'Without it, \*\*Important\*\* means.*' "$skill/SKILL.md" | sed 's/^Without it, //')"; must "the default meaning of Important" "$important"

inputs="## Inputs for this Review

- The diff command, run in the scratch repo ($scratch): \`git diff --merge-base main\` (the change is on branch \`planted\`, which is the head). No untracked new files are part of the change.
- The commit list: \`git log --oneline main..planted\`. The base for \`git show main:<file>\` is \`main\`.
- The spec: \`.scratch/SPEC.md\` in the scratch repo.
- The standards-source files: the fixture has no \`CLAUDE.md\`, \`AGENTS.md\` or \`CODING_STANDARDS.md\`; its \`REVIEW.md\` is the whole list.
- \`REVIEW.md\`, as follows. It has an Always check line.

\`\`\`
$review
\`\`\`

- The meaning of Important (\`REVIEW.md\` keeps the default): $important"

{
  printf '%s\n\n' "$inputs"
  printf '## Report rule\n\n%s\n\n' "$report_rule"
  printf '%s\n\n' "$format"
  printf '## Copy rule\n\n%s\n' "$copy_rule"
} >"$out/shared.md.tmp"

# finder <file-name> <brief-text> [extra-text]: a complete brief file, own brief first, shared part after.
finder() {
  { printf '%s\n\n' "$2"; [ -n "${3:-}" ] && printf '%s\n\n' "$3"; cat "$out/shared.md.tmp"; } >"$out/$1"
}

verifier() {
  # verifier <file-name> <brief-text> [stance-line] [candidates]
  {
    printf '%s\n\n' "$2"
    [ -n "${3:-}" ] && printf '## Your stance\n\n%s\n\n' "$3"
    printf '%s\n\n' "$inputs"
    printf '## Open Importants from earlier Rounds and Ticket checks\n\nNone.\n\n'
    printf '## Candidate Findings\n\n'
    if [ -n "${4:-}" ]; then printf '%s\n' "$4"; else printf '%s\n' '<<CANDIDATE FINDINGS: paste the merged candidates here, each tagged with its Finder>>'; fi
  } >"$out/$1"
}

verifier_brief="$(quoted "$(section "$verify" '## Verifier brief')")"; must "the Verifier brief" "$verifier_brief"
stance() { grep -m1 -e "^- \*\*$1:\*\*" "$verify" | sed -e 's/^[^"]*"//' -e 's/"$//'; }
tracer="$(stance Tracer)"; skeptic="$(stance Skeptic)"; checker="$(stance 'Spec checker')"
must "the three stances" "$tracer$skeptic$checker"
[ -n "$tracer" ] && [ -n "$skeptic" ] && [ -n "$checker" ] || { echo "a Deep stance is missing from VERIFY.md" >&2; exit 1; }

candidates=""
[ "$verify_only" = 1 ] && candidates="$(tail -n +2 "$here/VERIFY-ONLY.md")" # without its own "# Candidate Findings" title line

if [ "$verify_only" = 0 ]; then
  standards="$(section "$finders" '## Standards Finder')"; must "the standards Finder section" "$standards"
  # the brief line, then the three sections it says to paste in full
  brief="$(quoted "$standards")"; must "the standards Finder brief" "$brief"
  smell="$(section "$finders" '### Smell baseline')"
  drift="$(section "$finders" '### Docs index drift')"
  always="$(section "$finders" '### `REVIEW.md` Always check')"
  must "the Smell baseline section" "$smell"; must "the Docs index drift section" "$drift"; must "the REVIEW.md Always check section" "$always"
  finder finder-standards.md "$brief" "$(printf '%s\n\n%s\n\n%s' "$smell" "$drift" "$always")"

  spec="$(quoted "$(section "$finders" '## Spec Finder')")"; must "the spec Finder brief" "$spec"
  finder finder-spec.md "$spec"

  adv="$(section "$finders" '## Adversarial Finders')"
  adv_brief="$(quoted "$adv")"; must "the adversarial Finder brief" "$adv_brief"
  n=0
  for angle in "$angle1" "$angle2"; do
    n=$((n + 1))
    line="$(printf '%s\n' "$adv" | grep -m1 -i -e "^- \*\*$angle\*\*" || true)"
    [ -n "$line" ] || { echo "no angle called '$angle' in FINDERS.md" >&2; exit 1; }
    text="$(printf '%s' "${line#- }" | sed -e 's/\*\*//g' -e 's/\.$//')"
    finder "finder-adversarial-$n.md" "${adv_brief%%<angle>*}$text${adv_brief#*<angle>}"
  done

  if [ "$depth" = deep ]; then
    sec="$(quoted "$(section "$finders" '## Security Finder')")"; must "the security Finder brief" "$sec"
    finder finder-security.md "$sec"
    gap="$(quoted "$(section "$finders" '## Gap sweep')")"; must "the gap sweep brief" "$gap"
    finder finder-gap-sweep.md "$gap" "The Findings Verify kept (paste them here; report none of them again):

<<KEPT FINDINGS>>"
  fi
fi

if [ "$depth" = standard ]; then
  verifier verifier.md "$verifier_brief" "" "$candidates"
else
  verifier verifier-tracer.md "$verifier_brief" "$tracer" "$candidates"
  verifier verifier-skeptic.md "$verifier_brief" "$skeptic" "$candidates"
  verifier verifier-spec-checker.md "$verifier_brief" "$checker" "$candidates"
fi

if [ "$verify_only" = 0 ]; then mv "$out/shared.md.tmp" "$out/shared.md"; else rm "$out/shared.md.tmp"; fi
echo "Briefs for $depth${suffix:+ ($suffix)} written to $out:"
ls "$out"
