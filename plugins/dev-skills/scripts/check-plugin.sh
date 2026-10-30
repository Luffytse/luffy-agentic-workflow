#!/usr/bin/env bash
# Checks the dev-skills plugin layout and the Patches that ADR 0001 requires.
# Run from anywhere: plugins/dev-skills/scripts/check-plugin.sh (or a symlink to it)
# Same result however it runs: under `bash -e` or SHELLOPTS=errexit (this script reports every failure itself
# with bad(), and a no-match grep or find in a command substitution is a normal answer, not an error), and
# through a symlink (the plugin tree is found from the script's real path).
set -u
set +e
src="${BASH_SOURCE[0]:-$0}"
# follow symlinks one hop at a time with plain readlink: `readlink -f` is GNU-only and macOS lacks it
while [ -L "$src" ]; do
  link_dir="$(CDPATH= cd "$(dirname "$src")" && pwd)"
  src="$(readlink "$src")"
  case "$src" in /*) ;; *) src="$link_dir/$src" ;; esac
done
root="$(CDPATH= cd "$(dirname "$src")/.." && pwd)"
forked="$root/upstream-skills"
fail=0
bad() { echo "FAIL: $*"; fail=1; }

kept="ask-matt wayfinder grill-with-docs grilling domain-modeling research prototype handoff to-spec to-tickets implement implement-spec tdd agentic-review pr retro diagnosing-bugs triage improve-codebase-architecture codebase-design wizard writing-for-agents"
dropped="teach to-questionnaire grill-me wait-what"

# 1. kept-skills: exactly the 22 kept skills, each with a SKILL.md
count=0
for s in $kept; do
  [ -f "$forked/$s/SKILL.md" ] && count=$((count + 1)) || bad "missing $forked/$s/SKILL.md"
done
[ "$count" -eq 22 ] || bad "expected 22 skills, found $count"
for s in $dropped; do
  [ -e "$forked/$s" ] && bad "dropped skill present: $s"
done
if [ -d "$forked" ]; then
  for f in "$forked"/* "$forked"/.[!.]*; do
    [ -e "$f" ] && [ ! -d "$f" ] && bad "stray file in upstream-skills: $(basename "$f")"
  done
  for d in "$forked"/*/; do
    n="$(basename "$d")"
    case " $kept " in *" $n "*) ;; *) bad "unexpected skill folder: $n" ;; esac
  done
fi

# 2. model-invoked: every skill is model-invoked
if [ -d "$forked" ] && grep -rn --include=SKILL.md -E '^[[:space:]]*["'"'"']?(disable-model-invocation|user-invocable)["'"'"']?[[:space:]]*:' "$forked"; then
  bad "a skill still sets disable-model-invocation or user-invocable in frontmatter"
fi

# 2b. own-skills: our own skills: each has a SKILL.md and is model-invoked
own="$root/skills"
if [ -d "$own" ]; then
  for d in "$own"/*/; do
    [ -d "$d" ] || continue
    [ -f "$d/SKILL.md" ] || bad "own skill $(basename "$d") has no SKILL.md"
  done
  if grep -rn --include=SKILL.md -E '^[[:space:]]*["'"'"']?(disable-model-invocation|user-invocable)["'"'"']?[[:space:]]*:' "$own"; then
    bad "an own skill sets disable-model-invocation or user-invocable in frontmatter"
  fi
fi

# 3. ask-matt-dropped: ask-matt no longer names the dropped skills
if [ -f "$forked/ask-matt/SKILL.md" ]; then
  for s in $dropped; do
    grep -rnE "(^|[^a-z-])$s([^a-z-]|$)" "$forked/ask-matt" && bad "ask-matt still mentions $s"
  done
fi
# no kept skill points at a dropped one
if [ -d "$forked" ]; then
  for s in $dropped; do
    if [ "$s" = teach ]; then pat="/$s([^a-z-]|\$)|\`$s\`"; else pat="(^|[^a-z-])$s([^a-z-]|\$)"; fi
    grep -rnE "$pat" "$forked" && bad "a kept skill still points at dropped skill $s"
  done
fi

# 4. licence-manifest-docs: licence, manifest, docs
[ -f "$root/LICENSE-mattpocock-skills" ] || bad "missing LICENSE-mattpocock-skills"
[ -f "$root/.claude-plugin/plugin.json" ] || bad "missing .claude-plugin/plugin.json"
[ -f "$root/PATCHES.md" ] || bad "missing PATCHES.md"
[ -f "$root/README.md" ] || bad "missing README.md"
if [ -f "$root/PATCHES.md" ]; then
  grep -q "Upstream commit" "$root/PATCHES.md" || bad "PATCHES.md does not record the Upstream commit"
  grep -q "disable-model-invocation" "$root/PATCHES.md" || bad "PATCHES.md does not record the model-invocation change"
fi

# 5. codex-implicit-invocation: every skill is implicitly invocable in the Codex/OpenAI metadata too
if [ -d "$forked" ] && grep -rn --include=openai.yaml 'allow_implicit_invocation: false' "$forked"; then
  bad "a skill's agents/openai.yaml still sets allow_implicit_invocation: false"
fi

# 6. vendor-model-names: no vendor model names in forked or own text (ADR 0002): skills name cheap,
# regular or premium tiers. The README tier table, PATCHES.md (which describes this
# grep), this script and ADR 0002 (which define the tiers by naming the models) are exempt.
plugin_rel="plugins/dev-skills"
repo="$(cd "$root/../.." && pwd)"
# NUL-separated file list and a check on grep's output (not xargs' exit code), so file
# names with spaces and multi-batch xargs runs cannot hide a match.
hits="$(cd "$repo" && find . -type f -not -path './.git/*' \
  -not -path "./$plugin_rel/README.md" -not -path "./$plugin_rel/PATCHES.md" \
  -not -path "./$plugin_rel/scripts/check-plugin.sh" -not -path './LICENSE*' \
  -not -path "./$plugin_rel/LICENSE-mattpocock-skills" -not -path './docs/adr/0002-*' -print0 |
  xargs -0 grep -nIiE '\b(haiku|sonnet|opus)\b|claude[-_]?(opus|sonnet|haiku|[0-9])|\bgpt-?[0-9]|\bgemini\b')"
if [ -n "$hits" ]; then
  echo "$hits"
  bad "forked or own text names a vendor model"
fi

# 7. docs-index: docs index (ADR 0006): the rule file exists, writing skills link it, reading skills start at the index
writers="domain-modeling/SKILL.md improve-codebase-architecture/SKILL.md triage/SKILL.md triage/OUT-OF-SCOPE.md retro/SKILL.md retro/BUG-CLASSES.md research/SKILL.md grill-with-docs/SKILL.md"
readers="tdd diagnosing-bugs improve-codebase-architecture pr to-spec to-tickets triage grill-with-docs wayfinder implement implement-spec agentic-review"
[ -f "$forked/domain-modeling/DOCS-INDEX.md" ] || bad "missing domain-modeling/DOCS-INDEX.md"
for f in $writers; do
  grep -qF "DOCS-INDEX.md" "$forked/$f" || bad "writing skill file $f does not mention DOCS-INDEX.md"
done
for s in $readers; do
  grep -qiF 'start at `docs/index.md`' "$forked/$s/SKILL.md" || bad "reading skill $s does not say to start at \`docs/index.md\`"
  grep -qF 'GLOSSARY-MAP.md' "$forked/$s/SKILL.md" || bad "reading skill $s does not name GLOSSARY-MAP.md in its fallback"
done
grep -qF 'docs/index.md' "$own/setup-dev-skills/domain.md" || bad "domain.md template does not start at docs/index.md"
grep -qF "DOCS-INDEX.md" "$own/setup-dev-skills/SKILL.md" || bad "writing skill file setup-dev-skills/SKILL.md does not mention DOCS-INDEX.md"

# 8. agentic-review-files: agentic-review's reference files exist and SKILL.md links each one
for f in FINDERS.md VERIFY.md ROUNDS.md; do
  if [ ! -f "$forked/agentic-review/$f" ]; then bad "missing agentic-review/$f"
  elif ! grep -q "($f" "$forked/agentic-review/SKILL.md"; then bad "agentic-review/SKILL.md does not link $f"; fi
done

# 9. retro-bug-classes: retro turns repeated Bug classes into checks (ADR 0003): the procedure exists, SKILL.md links it,
# and it reads the same Round and Ticket-check markers that agentic-review/ROUNDS.md writes
bc="$forked/retro/BUG-CLASSES.md"
rounds="$forked/agentic-review/ROUNDS.md"
if [ ! -f "$bc" ]; then bad "missing retro/BUG-CLASSES.md"
else
  grep -q "(BUG-CLASSES.md" "$forked/retro/SKILL.md" || bad "retro/SKILL.md does not link BUG-CLASSES.md"
  for m in '<!-- code-review kind=round' '<!-- code-review kind=ticket-check'; do
    grep -qF "$m" "$bc" || bad "BUG-CLASSES.md does not mention the marker $m"
    grep -qF "$m" "$rounds" || bad "agentic-review/ROUNDS.md no longer has the marker $m that retro reads"
  done
  grep -qF 'REVIEW.md' "$bc" || bad "BUG-CLASSES.md does not mention REVIEW.md"
fi

# 10. ticket-templates: to-tickets' ticket templates carry a Model tier line, and to-tickets and wayfinder both name
# setup-project (ADR 0004). A presence check only: it does not test the offer's wording.
tt="$forked/to-tickets/SKILL.md"
for t in local-ticket-template issue-template; do
  sed -n "/^<$t>/,/^<\/$t>/p" "$tt" | grep -qF '**Model tier:**' || bad "to-tickets $t has no **Model tier:** line"
done
for s in to-tickets wayfinder; do
  grep -qF '`setup-project`' "$forked/$s/SKILL.md" || bad "$s does not offer \`setup-project\`"
done

# 11. implement-coordinator: implement is a Ticket thread's coordinator (ADR 0004): it hands the code to an Implementer,
# builds through tdd, opens the pull request with pr, reviews with agentic-review, and squash-merges
impl="$forked/implement/SKILL.md"
if [ -f "$impl" ]; then
  for s in tdd pr agentic-review; do
    grep -qF "\`$s\`" "$impl" || bad "implement/SKILL.md does not name the \`$s\` skill"
  done
  grep -qF 'Implementer' "$impl" || bad "implement/SKILL.md does not hand the work to an Implementer"
  grep -qiF 'squash' "$impl" || bad "implement/SKILL.md does not say lone tickets squash-merge"
fi

# 12. always-check: agentic-review applies REVIEW.md's Always check lines (issue #23): the standards Finder checks
# each line against the diff, and SKILL.md and VERIFY.md say how those Findings are handled
for f in FINDERS.md VERIFY.md SKILL.md; do
  grep -qF 'Always check' "$forked/agentic-review/$f" || bad "agentic-review/$f does not mention REVIEW.md's Always check lines"
done
grep -qF '### `REVIEW.md` Always check' "$forked/agentic-review/FINDERS.md" || bad "agentic-review/FINDERS.md has no REVIEW.md Always check section for the standards Finder"

# 13. ask-matt-routing: ask-matt describes implement as the lone-ticket coordinator, agentic-review as Rounds, and sends a
# Spec's tickets to implement-spec (issue #28), not as Upstream wrote them
am="$forked/ask-matt/SKILL.md"
if [ -f "$am" ]; then
  for w in 'same context window' 'two-axis'; do
    grep -qiF "$w" "$am" && bad "ask-matt/SKILL.md still says \"$w\""
  done
  grep -qF 'Rounds' "$am" || bad "ask-matt/SKILL.md does not describe agentic-review's Rounds"
  # a Spec's tickets go to implement-spec, never one by one to implement (implement step 1)
  grep -qF '`/implement`** per ticket' "$am" && bad "ask-matt/SKILL.md still offers /implement per ticket for a Spec's tickets"
fi

# 14. implement-spec-coordinator: implement-spec is a Spec thread's coordinator (ADR 0004, ADR 0005): Implementers build in
# ticket worktrees made with git worktree add, through tdd; the Spec pull request is written with pr,
# reviewed with agentic-review, and merged with a merge commit; no "integration branch" is left, here or in ask-matt
spec="$forked/implement-spec/SKILL.md"
if [ -f "$spec" ]; then
  for s in tdd pr agentic-review; do
    grep -qF "\`$s\`" "$spec" || bad "implement-spec/SKILL.md does not name the \`$s\` skill"
  done
  grep -qF 'Implementer' "$spec" || bad "implement-spec/SKILL.md does not hand the work to Implementers"
  grep -qF 'git worktree add' "$spec" || bad "implement-spec/SKILL.md does not make ticket worktrees with git worktree add"
  grep -qiF 'merge commit' "$spec" || bad "implement-spec/SKILL.md does not say the Spec pull request merges with a merge commit"
  grep -qiF 'integration branch' "$spec" && bad "implement-spec/SKILL.md still says integration branch"
fi
grep -qiF 'integration branch' "$forked/ask-matt/SKILL.md" && bad "ask-matt/SKILL.md still says integration branch"

# 15. no-code-review-skill: no skill tells an agent to run the built-in `code-review` (issue #50): our review skill is
# `agentic-review`. Scoped to skill text (upstream-skills/ and skills/, *.md and *.yaml). The
# `<!-- code-review kind=...` Round-comment markers are a data format, not a skill name, and
# PATCHES.md, ADRs, evals and this script are outside the scope.
if [ -d "$forked" ]; then
  scan="$forked"; [ -d "$own" ] && scan="$scan $own"
  # shellcheck disable=SC2086
  if grep -rnE --include=*.md --include=*.yaml '`(dev-skills:)?code-review`|(^|[^a-z-])/code-review([^a-z-]|$)|dev-skills:code-review|^name:[[:space:]]*code-review|[Tt]he code-review skill' $scan; then
    bad "a skill still tells an agent to run code-review; use agentic-review"
  fi
  [ -e "$forked/code-review" ] && bad "skill folder code-review still exists; it is agentic-review"
fi

# 16. no-person-names: no person's name in skill or doc text (issues #49, retro of PR #54): text says "the user", never
# the maintainer's name. The marketplace and repo names (luffy-dev, luffy-dev-skills), the GitHub
# owner Luffytse and the project name luffydev are not people. Checks upstream-skills/, skills/ and
# the plugin README, and the repo's CLAUDE.md, GLOSSARY.md and docs/ (all of it). Not the manifests
# (author fields) or dai-portal-data.
# Paths are relative to each root (in a subshell, so cwd is unchanged), so a checkout under a path
# such as ~/ cannot trip the check. awk keeps the script portable (no GNU-only flags).
name_awk='{l=tolower($0); gsub(/luffy-dev-skills|luffy-dev|luffytse|luffydev/,"",l); if (l ~ /lufei|luffy/) print FILENAME ":" FNR ": " $0}'
name_hits="$(
  (cd "$root" && find upstream-skills skills README.md -type f -print0 2>/dev/null | xargs -0 awk "$name_awk" 2>/dev/null)
  (cd "$repo" && find CLAUDE.md GLOSSARY.md docs -type f -print0 2>/dev/null | xargs -0 awk "$name_awk" 2>/dev/null)
)"
if [ -n "$name_hits" ]; then
  echo "$name_hits"
  bad "skill or doc text names a person (Lufei or Luffy); say \"the user\""
fi

# 17. retro-filing: retro files its suggestions as Retro issues (ADR 0007, "Filing"): the manifest names the dev-skills
# repo, retro/SKILL.md links the filing reference file, which names the label, title, vote and record,
# triage skips Retro issues, and no skill text names a particular project, repo or person
grep -qE '"repository"[[:space:]]*:[[:space:]]*"https://github.com/[^"/]+/[^"/]+"' "$root/.claude-plugin/plugin.json" || bad "plugin.json has no repository field with a GitHub URL"
fil="$forked/retro/FILING.md"
if [ ! -f "$fil" ]; then bad "missing retro/FILING.md"
else
  grep -q "(FILING.md" "$forked/retro/SKILL.md" || bad "retro/SKILL.md does not link FILING.md"
  for w in '`retro`' 'Retro:' 'seen again' '`retro-planning`'; do
    grep -qiF "$w" "$fil" || bad "FILING.md does not mention $w"
  done
fi
grep -qiE 'skip.*`retro`|`retro`.*skip' "$forked/triage/SKILL.md" || bad "triage/SKILL.md does not skip issues labelled retro"
if grep -rniE --include='*.md' --include='*.yaml' 'luffydev|luffytse|luffy-dev|lufei' "$forked" "$root/skills"; then
  bad "skill text names a particular project, repo or person"
fi

# 18. retro-last-step: implement and implement-spec end with a retro step (issue #42): their last step, after the report,
# runs `retro` on the thread, so each build feeds the Retro backlog
for s in implement implement-spec; do
  [ -f "$forked/$s/SKILL.md" ] || continue
  last="$(awk '/^## /{buf=""} {buf=buf"\n"$0} END{print buf}' "$forked/$s/SKILL.md")"
  printf '%s' "$last" | grep -qF '`retro`' || bad "$s/SKILL.md: the last step does not run \`retro\`"
  printf '%s' "$last" | grep -qF 'REVIEW.md' || bad "$s/SKILL.md: the last step does not say a retro check that changes REVIEW.md goes to the user"
done

# 19. ci-workflow: CI (issue #39, spec #38): a GitHub Actions workflow runs on pull requests and pushes to main,
# installs Claude Code's CLI from npm, and runs this script and `claude plugin validate .`
wf="$repo/.github/workflows/plugin-checks.yml"
if [ ! -f "$wf" ]; then bad "missing .github/workflows/plugin-checks.yml"
else
  grep -qE '^[[:space:]]*pull_request:' "$wf" || bad "plugin-checks.yml does not run on pull_request"
  { grep -qE '^[[:space:]]*push:' "$wf" && grep -qE 'main' "$wf"; } || bad "plugin-checks.yml does not run on pushes to main"
  grep -qF '@anthropic-ai/claude-code' "$wf" || bad "plugin-checks.yml does not install @anthropic-ai/claude-code from npm"
  grep -qF 'plugins/dev-skills/scripts/check-plugin.sh' "$wf" || bad "plugin-checks.yml does not run check-plugin.sh"
  grep -qF 'claude plugin validate .' "$wf" || bad "plugin-checks.yml does not run claude plugin validate ."
fi

# 20. retro-planning: retro-planning works through one repo's Retro backlog (ADR 0007, "Retro planning"): our own skill
# exists, names the `retro-planning` record label, the cap of 3 and the labels its verdicts use, and
# ask-matt routes a due Retro backlog to it. A presence check only: it does not test the rules' wording.
rp="$root/skills/retro-planning/SKILL.md"
if [ ! -f "$rp" ]; then bad "missing skills/retro-planning/SKILL.md"
else
  for w in '`retro-planning`' 'Retro planning <yyyy-mm-dd>' 'at most 3' '`wontfix`' '`ready-for-agent`'; do
    grep -qiF "$w" "$rp" || bad "retro-planning/SKILL.md does not mention $w"
  done
fi
grep -qF '`/retro-planning`' "$forked/ask-matt/SKILL.md" || bad "ask-matt/SKILL.md does not route to \`/retro-planning\`"

# 21. patches-agree: PATCHES.md and this script agree on check numbers and names (retro of PR #56, #78): every
# check header here reads "# N. <name>: ..." and every "new check N (<name>..." line in PATCHES.md must match
# one header as a pair, so a line pointing at another check's number fails even when that number is named
# elsewhere; no pair is claimed as new twice; and every check from 9 up is named as "check N" somewhere in
# PATCHES.md. Two further rules work on numbers alone: a number claimed as new under two different names
# fails, and so do two headers sharing a number (2 and 2b are different header numbers; for the pairs, 2b
# is written as 2). A placeholder number (TBD- and a capital N) is exempt from those two number rules, since
# several new checks in one pull request share it, but a placeholder pair (same name) claimed twice still fails.
self="$root/scripts/check-plugin.sh"
patches="$root/PATCHES.md"
if [ ! -f "$patches" ]; then bad "missing PATCHES.md"
else
  num='([0-9]+|TBD-[N])'
  nameless=$(grep -E "^# ${num}b?\\." "$self" | grep -vE "^# ${num}b?\\. [a-z0-9-]+:" | sed -E "s/^# ${num}.*/\\1/")
  for n in $nameless; do bad "check-plugin.sh check $n has no name in its header (# $n. <name>: ...)"; done
  headers=$(grep -E "^# ${num}b?\\. [a-z0-9-]+:" "$self" | sed -E "s/^# ${num}b?\\. ([a-z0-9-]+):.*/\\1 \\2/" | sort -u)
  claimed=$(grep -oiE "new check ${num} \\([a-z0-9-]+[:)]" "$patches" | sed -E 's/^[^ ]+ [^ ]+ ([^ ]+) \(([a-z0-9-]+).$/\1 \2/')
  # a "new check N" with no (<name>...) after it cannot be paired
  unnamed=$(grep -oiE "new check ${num}( \\([a-z0-9-]+[:)])?" "$patches" | grep -v '(' | sed -E 's/^[^ ]+ [^ ]+ //')
  for n in $unnamed; do bad "PATCHES.md says \"new check $n\" without the check's name; write new check $n (<name>)"; done
  while IFS= read -r pair; do
    [ -n "$pair" ] || continue
    printf '%s\n' "$headers" | grep -qxF "$pair" || bad "PATCHES.md says \"new check ${pair% *} (${pair#* }\" but check-plugin.sh has no \"# ${pair% *}. ${pair#* }:\" check"
  done <<< "$claimed"
  for pair in $(printf '%s\n' "$claimed" | sort | uniq -d | tr ' ' '~'); do
    bad "PATCHES.md claims \"new check ${pair//\~/ }\" more than once"
  done
  # a number is claimed as new once, whatever the name, and is the number of one header only (2 and 2b are
  # different headers); placeholders are skipped, since several new checks in one pull request share one
  for n in $(printf '%s\n' "$claimed" | awk '$1 ~ /^[0-9]+$/ {print $1}' | sort | uniq -d); do
    bad "PATCHES.md claims \"new check $n\" more than once (under different names)"
  done
  for n in $(grep -oE '^# [0-9]+b?\.' "$self" | sed -E 's/^# (.*)\.$/\1/' | sort | uniq -d); do
    bad "check-plugin.sh has more than one \"# $n.\" header"
  done
  mentioned=$(grep -oiE 'check [0-9]+' "$patches" | sed -E 's/.* //' | sort -u)
  for n in $(printf '%s\n' "$headers" | awk '$1 ~ /^[0-9]+$/ {print $1}' | sort -u); do
    [ "$n" -ge 9 ] || continue
    printf '%s\n' "$mentioned" | grep -qx "$n" || bad "PATCHES.md never names check $n"
  done
fi

# 22. agentic-review-strengths: agentic-review takes the built-in review's strengths (issue #51): a fixed-point Review includes
# uncommitted work, every Finding states a failure scenario, Finders pass on unsure candidates, the
# new adversarial angles exist, the Verifier keeps realistic rare paths, and Deep runs a gap sweep
ar="$forked/agentic-review"
grep -qF 'untracked' "$ar/SKILL.md" || bad "agentic-review/SKILL.md does not include uncommitted and untracked work in a fixed-point Review"
grep -qF -- '- Failure scenario:' "$ar/FINDERS.md" || bad "agentic-review/FINDERS.md Finding format has no Failure scenario line"
grep -qF '(unsure)' "$ar/FINDERS.md" || bad "agentic-review/FINDERS.md does not have Finders pass on unsure candidates"
for a in 'Removed behaviour' 'Cross-file callers' 'Language pitfalls' 'Wrappers and proxies' 'Altitude'; do
  grep -qF "**$a**" "$ar/FINDERS.md" || bad "agentic-review/FINDERS.md has no adversarial angle $a"
done
grep -qF '## Gap sweep' "$ar/FINDERS.md" || bad "agentic-review/FINDERS.md has no Gap sweep section"
grep -qiF 'gap sweep' "$ar/SKILL.md" || bad "agentic-review/SKILL.md depth table does not name the gap sweep"
grep -qiF 'gap sweep' "$ar/VERIFY.md" || bad "agentic-review/VERIFY.md does not verify the gap sweep's Findings"
grep -qF 'failure scenario' "$ar/VERIFY.md" || bad "agentic-review/VERIFY.md does not use the failure scenario"
grep -qF 'rare' "$ar/VERIFY.md" || bad "agentic-review/VERIFY.md does not keep realistic rare paths"
for f in "$repo/GLOSSARY.md" "$repo/docs/adr/0003-code-review-runs-find-verify-rank-in-rounds.md"; do
  for w in 'Gap sweep' 'Failure scenario'; do
    grep -qiF "$w" "$f" || bad "$(basename "$f") does not describe the $w"
  done
done

# 23. ask-matt-tracker: ask-matt's tracker and routing text matches the skills it routes to (issue #32): blocking edges are
# native links or a "Blocked by" line, the local path names the spec file and the ticket files, the
# wayfinder shortcut writes a lone ticket first, and the triage on-ramp sends an issue under a Spec to implement-spec
if [ -f "$am" ]; then
  grep -qF 'become native blocking links' "$am" && bad "ask-matt/SKILL.md still says the edges become native blocking links"
  grep -qF '"Blocked by" line' "$am" || bad "ask-matt/SKILL.md does not give the \"Blocked by\" line fallback for blocking edges"
  grep -qF '.scratch/<feature-slug>/spec.md' "$am" || bad "ask-matt/SKILL.md does not name the local spec file"
  grep -qF 'write one lone ticket' "$am" || bad "ask-matt/SKILL.md wayfinder shortcut does not say to write a lone ticket first"
  grep -F 'Bugs and requests piling up' "$am" | grep -qF '`/implement-spec`' || bad "ask-matt/SKILL.md triage on-ramp does not send an issue under a Spec to /implement-spec"
fi

# 24. setup-dev-skills: setup-dev-skills is our own skill (issue #77), not a fork of Upstream's setup skill: the forked
# folder is gone, the own skill exists with its seeds and no openai.yaml, credits Upstream and its
# licence file, is GitHub only, creates the wayfinder labels, and reports (never changes) GitHub settings
sd="$own/setup-dev-skills"
# the old name is built from two halves so that grep for it finds only PATCHES.md history
old="setup-matt-""pocock-skills"
[ -e "$forked/$old" ] && bad "upstream-skills/$old is back; the skill is skills/setup-dev-skills"
if [ ! -f "$sd/SKILL.md" ]; then bad "missing skills/setup-dev-skills/SKILL.md"
else
  for f in issue-tracker-github.md triage-labels.md domain.md; do
    [ -f "$sd/$f" ] || bad "missing skills/setup-dev-skills/$f"
  done
  [ -e "$sd/agents/openai.yaml" ] && bad "setup-dev-skills/agents/openai.yaml exists; our own skills have none"
  grep -qF 'LICENSE-mattpocock-skills' "$sd/SKILL.md" || bad "setup-dev-skills/SKILL.md does not credit Upstream and LICENSE-mattpocock-skills"
  grep -qF 'wayfinder:map' "$sd/SKILL.md" || bad "setup-dev-skills/SKILL.md does not create the wayfinder labels"
  grep -qiF 'never change' "$sd/SKILL.md" || bad "setup-dev-skills/SKILL.md does not say the settings check never changes settings"
  [ -e "$sd/issue-tracker-gitlab.md" ] || [ -e "$sd/issue-tracker-local.md" ] && bad "setup-dev-skills still carries a GitLab or local tracker seed"
fi

# 25. retro-planning-record: retro-planning's record carries its state from one planning to the next (issue #70): the next
# planning reads only closed records, so a section dropped from the template silently breaks the chain.
# The template must keep the snapshot, cap, spin-off and arrival sections, and the skill must file the
# record open at the start, walk one group at a time, and give spun-off groups their own planning.
if [ -f "$rp" ]; then
  for h in '## Snapshot' '## Cap' '## Spun off' '## Spun off, waiting' '## Arrived during this planning' \
           '## Held back by the cap' '## Open issues: plannings without a new vote' '## Waiting on open Tickets' \
           '## Running a spun-off planning'; do
    grep -qxF "$h" "$rp" || bad "retro-planning/SKILL.md has no heading line $h"
  done
  for w in '**open** issue' 'one at a time' 'Spun off to <thread link>'; do
    grep -qF "$w" "$rp" || bad "retro-planning/SKILL.md does not have $w"
  done
fi

# 26. grilling-round-cap: grilling asks at most 3 questions per round (issue #34): the cap and what happens to the rest of the
# frontier are in grilling itself, and setup-project relies on it instead of overriding it
gr="$forked/grilling/SKILL.md"
sp="$root/skills/setup-project/SKILL.md"
if [ -f "$gr" ]; then
  grep -qF 'at most **3**' "$gr" || bad "grilling/SKILL.md does not cap a round at 3 questions"
  grep -qF 'keep the rest for later rounds' "$gr" || bad "grilling/SKILL.md does not say what happens to the rest of the frontier"
  grep -qF 'whole frontier' "$gr" && bad "grilling/SKILL.md still says to ask the whole frontier"
fi
[ -f "$sp" ] && grep -qF 'This overrides' "$sp" && bad "setup-project/SKILL.md still overrides grilling's round size"

# 27. version-bumps: Version bumps in PATCHES.md agree with plugin.json (retro of PR #91: stale or duplicated version
# numbers after renumbering came up 4 times): no "version X to Y" bump has the same target Y twice, and
# the highest Y is plugin.json's version. A gap-free chain is not required (history has gaps).
bumps="$(grep -oE 'version [0-9]+\.[0-9]+\.[0-9]+ to [0-9]+\.[0-9]+\.[0-9]+' "$root/PATCHES.md" | awk '{print $4}')"
dup="$(printf '%s\n' "$bumps" | sort | uniq -d | tr '\n' ' ')"
[ -z "$dup" ] || bad "PATCHES.md has more than one version bump to: $dup"
top="$(printf '%s\n' "$bumps" | sort -V | tail -1)"
cur="$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$root/.claude-plugin/plugin.json" | head -1)"
[ -n "$top" ] && [ "$top" = "$cur" ] || bad "plugin.json is version $cur but the highest version bump in PATCHES.md is to ${top:-none}"

# 28. report-counts: agentic-review counts reports (issue #102, absorbs #44): cheap-tier Finders ended without returning
# their report in five threads and the Review went on without them. No script can see a subagent end
# early, so the thread counts reports itself (SKILL.md: Find, Verify and the gap sweep), and every Finder
# and Verifier brief ends with the last-action line. This check guards against either being reverted.
last='Your last action is to return your full report.'
n=$(grep -c '^Brief: "' "$ar/FINDERS.md")
[ "$n" -ge 5 ] || bad "agentic-review/FINDERS.md has $n Finder briefs; expected at least 5"
while IFS= read -r l; do
  case "$l" in *"$last\"") ;; *) bad "agentic-review/FINDERS.md brief does not end with the last-action line: ${l:0:50}" ;; esac
done < <(grep '^Brief: "' "$ar/FINDERS.md")
grep -F 'Answer per Finding:' "$ar/VERIFY.md" | grep -qF "$last\"" || bad "agentic-review/VERIFY.md Verifier brief does not end with \"$last\""
for g in 'you need one report from each Finder you started' \
         'you need one report from each Verifier you started' \
         'you need one report from the gap sweep Finder before the second Verify starts' \
         'one report from each second Verifier before Rank'; do
  grep -qF "$g" "$ar/SKILL.md" || bad "agentic-review/SKILL.md has lost the report-count gate: $g"
done

# 29. placeholders-and-bumps: numbers are taken at merge time, and every plugin change bumps its version (issue #106). (a) No
# placeholder is left: a Patch, check or version written as the placeholder (bare, in backticks or in
# parentheses), a placeholder check header in
# this script, or a placeholder version in a manifest. The patterns write the N in brackets so they do not
# match this script's own text. (b) Every plugin under plugins/ whose files differ from origin/main
# (committed since the merge-base, staged, unstaged or untracked) has a plugin.json version strictly higher
# than origin/main's. No origin/main (a shallow clone, no remote): (b) is skipped with a note. On main
# itself HEAD is origin/main, so nothing differs and (b) passes.
ph_hits="$(
  (cd "$repo" && find plugins/*/PATCHES.md plugins/*/README.md README.md CLAUDE.md GLOSSARY.md docs -type f -print0 2>/dev/null |
    xargs -0 grep -nE '(Patch|[Cc]heck|version|to) [`(]?TBD-[N]' 2>/dev/null)
  grep -nE '^# TBD-[N]' "$self" | sed "s|^|$self:|"
  (cd "$repo" && grep -nE '"version"[[:space:]]*:[[:space:]]*"TBD' .claude-plugin/marketplace.json plugins/*/.claude-plugin/plugin.json 2>/dev/null)
)"
if [ -n "$ph_hits" ]; then
  echo "$ph_hits"
  bad "a placeholder number is left; take the real numbers before merging"
fi
ver_of() { sed -nE 's/^[[:space:]]*"version"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/p' | head -n 1; }
# prints 1 when version $1 is strictly higher than $2, comparing dot-separated fields as numbers
ver_gt() { awk -v a="$1" -v b="$2" 'BEGIN{n=split(a,x,".");m=split(b,y,".");k=n>m?n:m;
  for(i=1;i<=k;i++){if(x[i]+0>y[i]+0){print 1;exit} if(x[i]+0<y[i]+0){print 0;exit}} print 0}'; }
if ! (cd "$repo" && git rev-parse --verify -q 'origin/main^{commit}' >/dev/null 2>&1); then
  echo "NOTE: origin/main not found; skipped the version bump check (check 29b)"
else
  for pj in "$repo"/plugins/*/.claude-plugin/plugin.json; do
    [ -f "$pj" ] || continue
    pd="plugins/$(basename "$(dirname "$(dirname "$pj")")")"
    changed="$(cd "$repo" && { git diff --name-only origin/main...HEAD -- "$pd"; git diff --name-only HEAD -- "$pd"
      git ls-files --others --exclude-standard -- "$pd"; })"
    [ -n "$changed" ] || continue
    old_v="$(cd "$repo" && git show "origin/main:$pd/.claude-plugin/plugin.json" 2>/dev/null | ver_of)"
    [ -n "$old_v" ] || continue # a new plugin: nothing to bump from
    new_v="$(ver_of < "$pj")"
    [ "$(ver_gt "$new_v" "$old_v")" = 1 ] || bad "$pd changed since origin/main but its version $new_v is not higher than origin/main's $old_v"
  done
fi

# 30. review-own-copy: Review subagents experiment only in their own copy (issues #60, #63): a Finder or Verifier that runs
# `git checkout <sha>` in the shared tree leaves it on a detached HEAD under the Implementer. Both briefs
# must say to work in a copy (`git archive` or a throwaway `git worktree`) and forbid checkout, switch,
# stash and reset in the shared tree. The Implementer's push check is a step it carries out; no script sees it.
for f in FINDERS.md VERIFY.md; do
  rb="$root/upstream-skills/agentic-review/$f"
  [ -f "$rb" ] || continue
  for w in 'own copy' 'git archive' 'git worktree' '`git checkout`' '`switch`' '`stash`' '`reset`' 'shared tree' 'on its branch'; do
    grep -qF -- "$w" "$rb" || bad "agentic-review/$f does not carry the copy rule ($w)"
  done
done

# 31. handoff-location: handoff saves where the next agent can read it (issue #109, absorbs #35): the temp directory is a
# session's own container in a cloud or remote session, which no other thread can open. No script can see
# where a thread saved a file, so this guards the wording against a revert: the tracker is the default, a
# shared folder only when the user names one, the temp directory only when the next agent runs on the same
# machine, and the skill ends by telling the user where the handoff is.
ho="$forked/handoff/SKILL.md"
for g in 'By default, save the handoff as an issue on the tracker' \
         'Use a shared folder only when the user names one' \
         'Use the temporary directory only when the next agent runs on the same machine' \
         'End by telling the user where the handoff is' \
         'ask the user where to save it'; do
  grep -qF "$g" "$ho" || bad "handoff/SKILL.md has lost the save-location rule: $g"
done
grep -qF 'Save to the temporary directory of the user' "$ho" && bad "handoff/SKILL.md still makes the temporary directory the default"

# 32. grilling-facts: grilling states a rule's purpose, checks a recommendation's facts, and counts its fact-finding
# sub-agent as asked for (issue #108); grill-with-docs gathers what other skills expect of a reworked skill
# first. Prose rules that no other check can see, so each sentence is pinned by a distinctive phrase.
gwd="$forked/grill-with-docs/SKILL.md"
if [ -f "$gr" ]; then
  grep -qF 'what the rule does today and why it exists' "$gr" || bad "grilling/SKILL.md does not have the rule-purpose line"
  grep -qF 'citing the ADR or doc' "$gr" || bad "grilling/SKILL.md does not tell the question to cite the ADR or doc"
  grep -qF 'waits for that fact, or is marked as a guess' "$gr" || bad "grilling/SKILL.md does not have the checked-fact-or-marked-guess rule"
  grep -qF 'counts as this skill asking for a sub-agent' "$gr" || bad "grilling/SKILL.md does not say its fact-finding sub-agent counts as asked for"
  grep -qF 'a few greps do not replace it' "$gr" || bad "grilling/SKILL.md does not say a few greps do not replace the sub-agent"
fi
[ -f "$gwd" ] && { grep -qF 'what every other skill expects of that skill' "$gwd" || bad "grill-with-docs/SKILL.md does not have the first fact for a skill rename or rework"; }

# 33. design-findings: agentic-review returns design Findings to the user as grilling (issue #112, absorbs #43): on a pull
# request that changes design, the thread fixed Findings about the design itself and wrote rules the user
# never agreed into ADRs. Only judgment tells a design Finding from a wording one, so this guards the rule's
# text: ROUNDS.md has the section and its key phrases, the Round loop points to it, and implement and
# implement-spec send design Findings to the user, not straight to the Implementer.
rd="$ar/ROUNDS.md"
grep -qxF '## Design Findings go to the user' "$rd" || bad "agentic-review/ROUNDS.md has no section \"## Design Findings go to the user\""
for w in 'a Finding that questions the design' 'grilling question' 'at most 3 at a time' 'recommended answer' \
         'until the user says nothing more is worth settling' 'only the agreed answer' 'wording, citations and index lines' \
         'saying plainly that the change is unreviewed' 'the Round counts as clean' "edit that Round's own comment"; do
  grep -qF "$w" "$rd" || bad "agentic-review/ROUNDS.md design-Findings rule has lost: $w"
done
# three in-file links: the Nit status bullet, the Round loop's fixes paragraph and its clean "Round 2 to Round 5" bullet
n=$(grep -oF '(#design-findings-go-to-the-user)' "$rd" | wc -l | tr -d ' ')
[ "$n" -ge 3 ] || bad "agentic-review/ROUNDS.md has $n links to the design-Findings section; expected at least 3 (Nit status, Round loop, clean Round bullet)"
# implement has one pointer (step 6); implement-spec has two (step 5's Ticket check and step 7's Rounds)
for fm in implement:1 implement-spec:2; do
  f="$forked/${fm%%:*}/SKILL.md"; want="${fm##*:}"
  n=$(grep -oF 'ROUNDS.md#design-findings-go-to-the-user' "$f" | wc -l | tr -d ' ')
  [ "$n" -ge "$want" ] || bad "${fm%%:*}/SKILL.md has $n pointers sending design Findings to the user; expected at least $want"
done
# 34. setup-project-state: setup-project writes how the project works, not the state of its work, and maps tiers to models
# (issue #142, absorbs #120 and #121): it no longer gathers open specs or the map as state, tells the
# coordinator to look them up on the tracker, asks for the tier-to-model map and writes it with the
# coordinator rule; skill text names no vendor model; no skill offers it to keep pointers current.
if [ -f "$sp" ]; then
  grep -qF 'open specs, plannings and tickets' "$sp" || bad "setup-project/SKILL.md does not tell the coordinator to find open specs, plannings and tickets on the tracker"
  grep -qF 'docs/agents/issue-tracker.md' "$sp" || bad "setup-project/SKILL.md does not point the coordinator at docs/agents/issue-tracker.md"
  grep -qF 'tier-to-model map' "$sp" || bad "setup-project/SKILL.md does not ask for the tier-to-model map"
  grep -qF "start each thread on the model mapped to its brief's Model tier" "$sp" || bad "setup-project/SKILL.md has no coordinator rule to start each thread on its tier's model"
  grep -qF 'pointers stay current' "$sp" && bad "setup-project/SKILL.md description still says pointers stay current"
  grep -qiE 'wayfinder map and the open specs|Link the wayfinder map|each open spec' "$sp" && bad "setup-project/SKILL.md still gathers or links open specs or the map as state"
  grep -qiE 'haiku|sonnet|opus|claude-|gpt-|gemini' "$sp" && bad "setup-project/SKILL.md names a vendor model"
fi
for s in to-tickets wayfinder; do
  grep -qiE 'a new (spec or map|spec|map) to point at' "$forked/$s/SKILL.md" && bad "$s still offers setup-project for a new spec or map to point at"
  grep -qF 'build threads to start' "$forked/$s/SKILL.md" && bad "$s still offers setup-project because build threads are ready to start"
done

# 35. patch-heading-numbers: no two "## Patch N" headings in PATCHES.md share a number (issue #123). A heading
# whose number is still a placeholder (TBD- and a capital N, CLAUDE.md) is skipped, since several can wait at once.
dup_patch="$(grep -oE '^## Patch [0-9]+' "$root/PATCHES.md" | awk '{print $3}' | sort | uniq -d)"
for n in $dup_patch; do
  bad "PATCHES.md has more than one \"## Patch $n\" heading"
done

# 36. skill-name-matches-folder: a skill's SKILL.md frontmatter name: equals its folder name (issue #61), for
# upstream-skills/ and skills/. The frontmatter is the block between the first two --- lines; quotes are ignored.
for d in "$forked"/*/ "$own"/*/; do
  [ -f "${d}SKILL.md" ] || continue
  folder="$(basename "$d")"
  fm_name="$(awk '/^---[[:space:]]*$/ {if (++b == 2) exit; next} b == 1 && /^name:/ {sub(/^name:[[:space:]]*/, ""); gsub(/["'"'"'[:space:]]/, ""); print; exit}' "${d}SKILL.md")"
  [ "$fm_name" = "$folder" ] || bad "skill $folder: SKILL.md frontmatter name \"$fm_name\" differs from its folder name"
done

# 37. openai-display-name: a skill's display_name in agents/openai.yaml names the skill (issue #62). The rule:
# the display_name, lowercased with each run of other characters turned into one hyphen, equals the skill's folder
# name ("Grill with Docs" is grill-with-docs, "PR" is pr). So a display_name that is another skill's or a built-in
# skill's name ("Code Review" for agentic-review) fails, and a rename of the folder needs a new display_name.
for y in "$forked"/*/agents/openai.yaml "$own"/*/agents/openai.yaml; do
  [ -f "$y" ] || continue
  folder="$(basename "$(dirname "$(dirname "$y")")")"
  dn="$(sed -n 's/^[[:space:]]*display_name:[[:space:]]*//p' "$y" | head -n 1 | sed -E 's/^["'"'"']//; s/["'"'"'][[:space:]]*$//')"
  norm="$(printf '%s' "$dn" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-//; s/-$//')"
  [ -n "$dn" ] || bad "skill $folder: agents/openai.yaml has no display_name"
  [ -z "$dn" ] || [ "$norm" = "$folder" ] || bad "skill $folder: display_name \"$dn\" does not match the skill name (it should read like \"$folder\")"
done

[ "$fail" -eq 0 ] && echo "OK: dev-skills plugin checks passed ($count skills)"
exit "$fail"
