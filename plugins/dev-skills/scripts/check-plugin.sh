#!/usr/bin/env bash
# Checks the dev-skills plugin layout and the Patches that ADR 0001 requires.
# Run from anywhere: plugins/dev-skills/scripts/check-plugin.sh
set -u
root="$(cd "$(dirname "$0")/.." && pwd)"
forked="$root/upstream-skills"
fail=0
bad() { echo "FAIL: $*"; fail=1; }

kept="ask-matt wayfinder grill-with-docs grilling domain-modeling research prototype handoff to-spec to-tickets implement implement-spec tdd code-review pr retro diagnosing-bugs triage improve-codebase-architecture codebase-design setup-matt-pocock-skills wizard writing-for-agents"
dropped="teach to-questionnaire grill-me wait-what"

# 1. exactly the 23 kept skills, each with a SKILL.md
count=0
for s in $kept; do
  [ -f "$forked/$s/SKILL.md" ] && count=$((count + 1)) || bad "missing $forked/$s/SKILL.md"
done
[ "$count" -eq 23 ] || bad "expected 23 skills, found $count"
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

# 6. no vendor model names in our own text. Upstream text, the README tier table,
# PATCHES.md (which describes this grep), this script and ADR 0002 (which defines the
# tiers by naming the models) are exempt.
plugin_rel="plugins/dev-skills"
repo="$(cd "$root/../.." && pwd)"
own="$(cd "$repo" && find . -type f -not -path './.git/*' -not -path "./$plugin_rel/upstream-skills/*" \
  -not -path "./$plugin_rel/README.md" -not -path "./$plugin_rel/PATCHES.md" \
  -not -path "./$plugin_rel/scripts/check-plugin.sh" -not -name 'LICENSE*' \
  -not -path './docs/adr/0002-*')"
if [ -n "$own" ] && (cd "$repo" && echo "$own" | xargs grep -nIiE '\b(haiku|sonnet|opus)\b|(^|[^./a-z-])claude-(opus|sonnet|haiku|[0-9])|\bgpt-' ); then
  bad "own text names a vendor model"
fi

[ "$fail" -eq 0 ] && echo "OK: dev-skills plugin checks passed ($count skills)"
exit "$fail"
