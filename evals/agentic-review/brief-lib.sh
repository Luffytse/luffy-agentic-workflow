# Helpers for the agentic-review eval's brief builder (briefs.sh), which sources this file. They cut each brief out of
# the current review-rounds skill files word for word, so no one cuts them out by hand.

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

# quoted <label> <text>: the quoted text after `<label>: "`, which may run over several lines, without its quote marks.
quoted() {
  printf '%s\n' "$2" | awk -v label="$1: \"" '
    !on && index($0, label) == 1 { on = 1; $0 = substr($0, length(label) + 1) }
    on { if ($0 ~ /"$/) { sub(/"$/, ""); print; exit } print }'
}

must() { [ -n "$2" ] || { echo "could not find $1 in the current skill files; the script needs updating" >&2; exit 1; }; }

# load_rules <review-rounds-dir>: reads the current FINDERS.md, VERIFY.md, DEEP.md and SKILL.md into the variables
# build_briefs uses.
load_rules() {
  skill="$1"
  finders="$skill/FINDERS.md"; verify="$skill/VERIFY.md"; deep="$skill/DEEP.md"
  all="$(cat "$finders")"
  shared="$(quoted 'Shared brief' "$all")"; must "the shared brief" "$shared"
  copy_rule="$(quoted 'Copy rule' "$all")"; must "the copy rule" "$copy_rule"
  earlier="$(printf '%s\n' "$all" | sed -n 's/^The standards, spec and later-Round Finders also get .*, with: "\(.*\)"$/\1/p')"
  must "the earlier-Findings line" "$earlier"
  format="$(section "$finders" '## Finding format')"; must "the Finding format" "$format"
  standards="$(quoted Brief "$(section "$finders" '## Standards Finder')")"; must "the standards Finder brief" "$standards"
  smell="$(section "$finders" '### Smell baseline')"; must "the smell baseline" "$smell"
  drift="$(section "$finders" '### Docs index drift')"; must "the docs index drift check" "$drift"
  spec_brief="$(quoted Brief "$(section "$finders" '## Spec Finder')")"; must "the spec Finder brief" "$spec_brief"
  adv="$(section "$finders" '## Adversarial Finder')"
  adv_brief="$(quoted Brief "$adv")"; must "the adversarial Finder brief" "$adv_brief"
  verifier_brief="$(quoted Brief "$(cat "$verify")")"; must "the Verifier brief" "$verifier_brief"
  security="$(quoted Brief "$(section "$deep" '## Security Finder')")"; must "the security Finder brief" "$security"
  important="$(grep -m1 -o 'Without it, \*\*Important\*\* means.*' "$skill/SKILL.md" | sed 's/^Without it, //')"
  must "the default meaning of Important" "$important"
  record="$(section "$skill/../review-record/SKILL.md" '## Terminology')"; must "the review-record terminology" "$record"
  index_contract="$(cat "$skill/../docs-index/SKILL.md")"; must "the docs-index contract" "$index_contract"
}

# always_lines <review-md-file> <changed-files>: the REVIEW.md Always check lines whose `(files: <glob> ...)` matches a
# changed file, one per line.
always_lines() {
  python3 -I - "$1" "$2" <<'PY'
import fnmatch, re, sys
review = open(sys.argv[1]).read().splitlines()
changed = [p for p in sys.argv[2].split("\n") if p]
on = False
for line in review:
    if line.startswith("## "):
        on = line.strip() == "## Always check"
        continue
    if on and line.startswith("- **"):
        m = re.search(r"\(files: ([^)]*)\)", line)
        globs = re.findall(r"`([^`]+)`", m.group(1)) if m else []
        if any(fnmatch.fnmatch(p, g) for p in changed for g in globs):
            print(line)
PY
}

# build_briefs <out> <level> <angle> <inputs> <spec-path> <review-md-file> <changed-files> <has-index 0|1> [candidates]
# writes the Finder and Verifier briefs for one level into <out>, each file complete. <inputs> is the part every Finder
# and the Verifier get. With candidates (the Verify-only check), only verifier.md is written, holding them; without,
# verifier.md ends with placeholder lines for them.
build_briefs() {
  out="$1"; level="$2"; angle="$3"; inputs="$4"; spec_path="$5"; review_md="$6"; changed="$7"; has_index="$8"
  candidates="${9:-}"
  tail_part="$(printf '## Shared brief\n\n%s\n\n## Copy rule\n\n%s\n\n%s\n' "$shared" "$copy_rule" "$format")"
  spec_part="## The spec, the earlier Findings and the design answers

- The spec: \`$spec_path\` in the scratch repo, as follows.

\`\`\`
$(cat "$spec_file")
\`\`\`

- Earlier Findings: none (this is Round 1, and there was no Ticket check).
- Design answers: none.

$earlier"

  finder() { # finder <file> <brief> [extra]
    { printf '%s\n\n' "$2"; [ -n "${3:-}" ] && printf '%s\n\n' "$3"; printf '%s\n\n%s\n' "$inputs" "$tail_part"; } >"$out/$1"
  }

  if [ -z "$candidates" ]; then
    lines="$(always_lines "$review_md" "$changed")"
    extra="## Standards files

None besides \`REVIEW.md\`: the fixture has no \`CLAUDE.md\`, \`AGENTS.md\`, style guide or \`CONTRIBUTING.md\`.

## Always check lines for the files this diff touches

${lines:-None.}

$record"
    # the smell baseline only when the diff changes code (any file that is not text)
    if printf '%s\n' "$changed" | grep -qvE '\.(md|txt)$'; then extra="$extra

$smell"; fi
    [ "$has_index" = 1 ] && extra="$extra

$drift

$index_contract"
    finder finder-standards.md "$standards" "$extra

$spec_part"
    finder finder-spec.md "$spec_brief" "$spec_part"

    if [ "$level" != quick ]; then
      line="$(printf '%s\n' "$adv" | grep -m1 -i -e "^- \*\*$angle\*\*" || true)"
      [ -n "$line" ] || { echo "no angle called '$angle' in FINDERS.md" >&2; exit 1; }
      text="$(printf '%s' "${line#- }" | sed -e 's/\*\*//g' -e 's/\.$//')"
      finder finder-adversarial.md "${adv_brief%%<angle>*}$text${adv_brief#*<angle>}"
    fi
    if [ "$level" = deep ]; then
      finder finder-security.md "$security" "$spec_part"
    fi
  fi

  {
    printf '%s\n\n' "$verifier_brief"
    printf '## Copy rule\n\n%s\n\n' "$copy_rule"
    printf '%s\n\n' "$inputs"
    printf -- '- The spec: `%s` in the scratch repo. Design answers: none.\n\n' "$spec_path"
    printf '## Earlier open Findings and disputes\n\nNone.\n\n'
    printf '## Always check lines for candidates raised from one\n\n'
    if [ -n "$candidates" ]; then
      printf 'None: no candidate was raised from an Always check line.\n\n'
      printf '## Candidate Findings\n\n%s\n' "$candidates"
    else
      printf '%s\n\n' '<<ALWAYS CHECK LINES: paste the REVIEW.md line of each candidate the standards Finder raised from one, or write None>>'
      printf '## Candidate Findings\n\n%s\n' '<<CANDIDATE FINDINGS: paste the merged candidates here, each tagged with its Finder>>'
    fi
  } >"$out/verifier.md"
}
