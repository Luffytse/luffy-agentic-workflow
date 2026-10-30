#!/usr/bin/env bash
# Checks the dev-skills plugin layout and the Patches that ADR 0001 requires.
# Run from anywhere: plugins/dev-skills/scripts/check-plugin.sh
set -u
root="$(cd "$(dirname "$0")/.." && pwd)"
forked="$root/upstream-skills"
fail=0
bad() { echo "FAIL: $*"; fail=1; }

kept="ask-matt wayfinder grill-with-docs grilling domain-modeling research prototype handoff to-spec to-tickets implement implement-spec tdd agentic-review pr retro diagnosing-bugs triage improve-codebase-architecture codebase-design wizard writing-for-agents"
dropped="teach to-questionnaire grill-me wait-what"

# 1. exactly the 22 kept skills, each with a SKILL.md
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

# 2. every skill is model-invoked
if [ -d "$forked" ] && grep -rn --include=SKILL.md -E '^[[:space:]]*["'"'"']?(disable-model-invocation|user-invocable)["'"'"']?[[:space:]]*:' "$forked"; then
  bad "a skill still sets disable-model-invocation or user-invocable in frontmatter"
fi

# 2b. our own skills: each has a SKILL.md and is model-invoked
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

# 3. ask-matt no longer names the dropped skills
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

# 4. licence, manifest, docs
[ -f "$root/LICENSE-mattpocock-skills" ] || bad "missing LICENSE-mattpocock-skills"
[ -f "$root/.claude-plugin/plugin.json" ] || bad "missing .claude-plugin/plugin.json"
[ -f "$root/PATCHES.md" ] || bad "missing PATCHES.md"
[ -f "$root/README.md" ] || bad "missing README.md"
if [ -f "$root/PATCHES.md" ]; then
  grep -q "Upstream commit" "$root/PATCHES.md" || bad "PATCHES.md does not record the Upstream commit"
  grep -q "disable-model-invocation" "$root/PATCHES.md" || bad "PATCHES.md does not record the model-invocation change"
fi

# 5. every skill is implicitly invocable in the Codex/OpenAI metadata too
if [ -d "$forked" ] && grep -rn --include=openai.yaml 'allow_implicit_invocation: false' "$forked"; then
  bad "a skill's agents/openai.yaml still sets allow_implicit_invocation: false"
fi

# 6. no vendor model names in forked or own text (ADR 0002): skills name cheap,
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

# 7. docs index (ADR 0006): the rule file exists, writing skills link it, reading skills start at the index
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

# 8. agentic-review's reference files exist and SKILL.md links each one
for f in FINDERS.md VERIFY.md ROUNDS.md; do
  if [ ! -f "$forked/agentic-review/$f" ]; then bad "missing agentic-review/$f"
  elif ! grep -q "($f" "$forked/agentic-review/SKILL.md"; then bad "agentic-review/SKILL.md does not link $f"; fi
done

# 9. retro turns repeated Bug classes into checks (ADR 0003): the procedure exists, SKILL.md links it,
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

# 10. to-tickets' ticket templates carry a Model tier line, and to-tickets and wayfinder both name
# setup-project (ADR 0004). A presence check only: it does not test the offer's wording.
tt="$forked/to-tickets/SKILL.md"
for t in local-ticket-template issue-template; do
  sed -n "/^<$t>/,/^<\/$t>/p" "$tt" | grep -qF '**Model tier:**' || bad "to-tickets $t has no **Model tier:** line"
done
for s in to-tickets wayfinder; do
  grep -qF '`setup-project`' "$forked/$s/SKILL.md" || bad "$s does not offer \`setup-project\`"
done

# 11. implement is a Ticket thread's coordinator (ADR 0004): it hands the code to an Implementer,
# builds through tdd, opens the pull request with pr, reviews with agentic-review, and squash-merges
impl="$forked/implement/SKILL.md"
if [ -f "$impl" ]; then
  for s in tdd pr agentic-review; do
    grep -qF "\`$s\`" "$impl" || bad "implement/SKILL.md does not name the \`$s\` skill"
  done
  grep -qF 'Implementer' "$impl" || bad "implement/SKILL.md does not hand the work to an Implementer"
  grep -qiF 'squash' "$impl" || bad "implement/SKILL.md does not say lone tickets squash-merge"
fi

# 12. agentic-review applies REVIEW.md's Always check lines (issue #23): the standards Finder checks
# each line against the diff, and SKILL.md and VERIFY.md say how those Findings are handled
for f in FINDERS.md VERIFY.md SKILL.md; do
  grep -qF 'Always check' "$forked/agentic-review/$f" || bad "agentic-review/$f does not mention REVIEW.md's Always check lines"
done
grep -qF '### `REVIEW.md` Always check' "$forked/agentic-review/FINDERS.md" || bad "agentic-review/FINDERS.md has no REVIEW.md Always check section for the standards Finder"

# 13. ask-matt describes implement as the lone-ticket coordinator, agentic-review as Rounds, and sends a
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

# 14. implement-spec is a Spec thread's coordinator (ADR 0004, ADR 0005): Implementers build in
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

# 15. no skill tells an agent to run the built-in `code-review` (issue #50): our review skill is
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

# 16. no person's name in skill or doc text (issues #49, retro of PR #54): text says "the user", never
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

# 17. retro files its suggestions as Retro issues (ADR 0007, "Filing"): the manifest names the dev-skills
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

# 18. implement and implement-spec end with a retro step (issue #42): their last step, after the report,
# runs `retro` on the thread, so each build feeds the Retro backlog
for s in implement implement-spec; do
  [ -f "$forked/$s/SKILL.md" ] || continue
  last="$(awk '/^## /{buf=""} {buf=buf"\n"$0} END{print buf}' "$forked/$s/SKILL.md")"
  printf '%s' "$last" | grep -qF '`retro`' || bad "$s/SKILL.md: the last step does not run \`retro\`"
  printf '%s' "$last" | grep -qF 'REVIEW.md' || bad "$s/SKILL.md: the last step does not say a retro check that changes REVIEW.md goes to the user"
done

# 19. CI (issue #39, spec #38): a GitHub Actions workflow runs on pull requests and pushes to main,
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

# 20. retro-planning works through one repo's Retro backlog (ADR 0007, "Retro planning"): our own skill
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

# 21. PATCHES.md and this script agree on check numbers (retro of PR #56): every "new check N" in
# PATCHES.md names a check whose "# N." header is in this script, no N is claimed as new twice, and
# every check from 9 up is named as "check N" somewhere in PATCHES.md.
self="$root/scripts/check-plugin.sh"
patches="$root/PATCHES.md"
if [ ! -f "$patches" ]; then bad "missing PATCHES.md"
else
  headers=$(grep -E '^# [0-9]+b?\.' "$self" | sed -E 's/^# ([0-9]+).*/\1/' | sort -u)
  claimed=$(grep -oiE 'new check [0-9]+' "$patches" | sed -E 's/.* //')
  for n in $claimed; do
    printf '%s\n' "$headers" | grep -qx "$n" || bad "PATCHES.md says \"new check $n\" but check-plugin.sh has no check $n"
  done
  for n in $(printf '%s\n' "$claimed" | sort | uniq -d); do
    bad "PATCHES.md claims \"new check $n\" more than once"
  done
  mentioned=$(grep -oiE 'check [0-9]+' "$patches" | sed -E 's/.* //' | sort -u)
  for n in $headers; do
    [ "$n" -ge 9 ] || continue
    printf '%s\n' "$mentioned" | grep -qx "$n" || bad "PATCHES.md never names check $n"
  done
fi

# 22. agentic-review takes the built-in review's strengths (issue #51): a fixed-point Review includes
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

# 23. ask-matt's tracker and routing text matches the skills it routes to (issue #32): blocking edges are
# native links or a "Blocked by" line, the local path names the spec file and the ticket files, the
# wayfinder shortcut writes a lone ticket first, and the triage on-ramp sends an issue under a Spec to implement-spec
if [ -f "$am" ]; then
  grep -qF 'become native blocking links' "$am" && bad "ask-matt/SKILL.md still says the edges become native blocking links"
  grep -qF '"Blocked by" line' "$am" || bad "ask-matt/SKILL.md does not give the \"Blocked by\" line fallback for blocking edges"
  grep -qF '.scratch/<feature-slug>/spec.md' "$am" || bad "ask-matt/SKILL.md does not name the local spec file"
  grep -qF 'write one lone ticket' "$am" || bad "ask-matt/SKILL.md wayfinder shortcut does not say to write a lone ticket first"
  grep -F 'Bugs and requests piling up' "$am" | grep -qF '`/implement-spec`' || bad "ask-matt/SKILL.md triage on-ramp does not send an issue under a Spec to /implement-spec"
fi

# 24. setup-dev-skills is our own skill (issue #77), not a fork of Upstream's setup skill: the forked
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

# 25. retro-planning's record carries its state from one planning to the next (issue #70): the next
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

# 26. grilling asks at most 3 questions per round (issue #34): the cap and what happens to the rest of the
# frontier are in grilling itself, and setup-project relies on it instead of overriding it
gr="$forked/grilling/SKILL.md"
sp="$root/skills/setup-project/SKILL.md"
if [ -f "$gr" ]; then
  grep -qF 'at most **3**' "$gr" || bad "grilling/SKILL.md does not cap a round at 3 questions"
  grep -qF 'keep the rest for later rounds' "$gr" || bad "grilling/SKILL.md does not say what happens to the rest of the frontier"
  grep -qF 'whole frontier' "$gr" && bad "grilling/SKILL.md still says to ask the whole frontier"
fi
[ -f "$sp" ] && grep -qF 'This overrides' "$sp" && bad "setup-project/SKILL.md still overrides grilling's round size"

[ "$fail" -eq 0 ] && echo "OK: dev-skills plugin checks passed ($count skills)"
exit "$fail"
