# Helpers shared by the agentic-review eval's brief builders (briefs.sh and milestone/briefs.sh), which source this
# file. Each cuts a brief out of the current skill files word for word, so no one cuts them out by hand.

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

# bullet_quote <file> <pattern> <after>: the quoted text after <after> on the bullet of <file> matching <pattern>.
bullet_quote() { grep -m1 -e "$2" "$1" | sed -e "s/^.*$3 \"//" -e 's/"$//'; }

must() { [ -n "$2" ] || { echo "could not find $1 in the current skill files; the script needs updating" >&2; exit 1; }; }

# load_rules <skill-dir>: reads the current FINDERS.md, VERIFY.md and SKILL.md of agentic-review into the variables
# the builders use: skill, finders, verify, format, report_rule, copy_rule and important.
load_rules() {
  skill="$1"
  finders="$skill/FINDERS.md"
  verify="$skill/VERIFY.md"
  format="$(section "$finders" '## Finding format')"; must "the Finding format" "$format"
  report_rule="$(bullet_quote "$finders" '^- The \*\*Finding format\*\*' 'with:')"; must "the Finding format bullet" "$report_rule"
  copy_rule="$(bullet_quote "$finders" '^- The \*\*copy rule\*\*' 'pasted in full:')"; must "the copy rule" "$copy_rule"
  important="$(grep -m1 -o 'Without it, \*\*Important\*\* means.*' "$skill/SKILL.md" | sed 's/^Without it, //')"; must "the default meaning of Important" "$important"
}

# build_briefs <out> <depth> <angle1> <angle2> <verify-only 0|1> <inputs> [candidates]: writes the Finder and Verifier
# briefs for one depth into <out>, each file complete, with <inputs> (the "## Inputs for this Review" section) as the
# part every Finder and Verifier gets. Without candidates, verifier*.md ends with a placeholder line for them.
build_briefs() {
  out="$1"; depth="$2"; angle1="$3"; angle2="$4"; verify_only="$5"; inputs="$6"; candidates="${7:-}"
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

  if [ "$verify_only" = 0 ]; then
    standards="$(section "$finders" '## Standards Finder')"; must "the standards Finder section" "$standards"
    # the brief line, then the three sections it says to paste in full
    brief="$(quoted "$standards")"; must "the standards Finder brief" "$brief"
    smell="$(section "$finders" '### Smell baseline')"
    drift="$(section "$finders" '### Docs index drift')"
    always="$(section "$finders" '### `REVIEW.md` Always check')"
    must "the Smell baseline section" "$smell"; must "the Docs index drift section" "$drift"; must "the REVIEW.md Always check section" "$always"
    record="$(section "$skill/../review-record/SKILL.md" '## Terminology')"
    must "the review-record terminology" "$record"
    index_contract="$(cat "$skill/../docs-index/SKILL.md")"
    must "the docs-index contract" "$index_contract"
    drift="$drift

$index_contract"
    always="$always

$record"
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
}
