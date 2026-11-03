#!/usr/bin/env bash
# Builds the Round 0 fixture and checks each case's branch holds what the case needs: version-only changes only a
# version field and a changelog entry, typo fixes one word in a skill without changing what it says, and rule-change
# changes what a skill rule does. It also checks the fixture leaves the defaults in force (no "Review levels"
# section) and that each prompt names its branch and keeps the expected level out. It runs no agent.
# Usage: bash evals/agentic-review/round0/test-fixture.sh
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
fails=0
ok() { echo "ok: $1"; }
no() { echo "FAIL: $1"; fails=$((fails + 1)); }
check() { if eval "$2"; then ok "$1"; else no "$1"; fi; }

bash "$here/make-fixture.sh" "$tmp/out" >/dev/null
r="$tmp/out/repo"
g() { git -C "$r" "$@"; }

check "branch main exists" 'g rev-parse -q --verify main >/dev/null'
for b in version-only typo rule-change; do
  check "branch $b exists" 'g rev-parse -q --verify "$b" >/dev/null'
  check "branch $b is one commit on main" '[ "$(g rev-list --count main.."$b")" = 1 ] && [ "$(g merge-base main "$b")" = "$(g rev-parse main)" ]'
  check "PROMPT-$b.md names the branch" 'grep -qF "branch \`$b\`" "$tmp/out/PROMPT-$b.md"'
  check "PROMPT-$b.md holds no expected level" '! grep -qiE "expected|level (none|quick|standard|deep)" "$tmp/out/PROMPT-$b.md"'
done
check "REVIEW.md has no Review levels section, so the defaults apply" '! g show main:REVIEW.md | grep -qi "review levels"'
check "the repo has a Boundary record" 'g cat-file -e main:docs/dev-skills/boundaries.md'
check "the repo runs its checks with one command" 'g cat-file -e main:check.sh && (cd "$r" && bash check.sh >/dev/null)'

# version-only: every changed line is the manifest's version field or a changelog line
files="$(g diff --name-only main...version-only | sort | tr '\n' ' ')"
check "version-only touches only the manifest and the changelog" '[ "$files" = "CHANGELOG.md plugin/plugin.json " ]'
check "version-only changes only the version field in the manifest" \
  '[ -z "$(g diff -U0 main...version-only -- plugin/plugin.json | grep -E "^[-+][^-+]" | grep -vE "^[-+][[:space:]]*\"version\": \"[0-9.]+\",?$")" ]'
check "version-only only adds changelog lines" '[ -z "$(g diff -U0 main...version-only -- CHANGELOG.md | grep -E "^-[^-]")" ]'
check "the version-only branch still passes the checks" '(d="$tmp/v"; mkdir "$d"; g archive version-only | tar -x -C "$d"; cd "$d" && bash check.sh >/dev/null)'

# typo: one word in one skill file, a misspelling fixed, every other word the same
check "typo touches only the skill file" '[ "$(g diff --name-only main...typo)" = "skills/greet/SKILL.md" ]'
words="$(g diff --word-diff=porcelain -U0 main...typo | grep -E "^[-+][^-+]" | tr '\n' ' ')"
check "typo changes exactly one word, recieve to receive" '[ "$words" = "-recieve +receive " ]'

# rule-change: the same skill file, and the rule now says something else
check "rule-change touches only the skill file" '[ "$(g diff --name-only main...rule-change)" = "skills/greet/SKILL.md" ]'
check "rule-change removes the first-name rule" 'g diff main...rule-change | grep -qE "^-.*by their first name"'
check "rule-change adds a rule with a different meaning" 'g diff main...rule-change | grep -qE "^\+.*full name"'
check "rule-change is not a one-word spelling fix" '[ "$(g diff --word-diff=porcelain -U0 main...rule-change | grep -cE "^[-+][^-+]")" -gt 2 ]'

if [ "$fails" -gt 0 ]; then echo "$fails check(s) failed"; exit 1; fi
echo "all Round 0 fixture checks passed"
