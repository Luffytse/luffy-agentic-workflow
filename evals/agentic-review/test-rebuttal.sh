#!/usr/bin/env bash
# Builds the fixture and the rebuttal check's briefs, and checks each brief holds what the check needs: the rebuttal
# Verifier brief from VERIFY.md word for word, one Finding from VERIFY-ONLY.md with its id, and the rebuttal of it from
# REBUTTALS.md, with every file:line a rebuttal cites holding the text it quotes, and no scoring file named.
# Run: bash evals/agentic-review/test-rebuttal.sh
set -u
here="$(cd "$(dirname "$0")" && pwd)"
verify="$here/../../plugins/dev-skills/skills/agentic-review/VERIFY.md"
out="$(mktemp -d)"
fail=0
bad() { echo "FAIL: $*"; fail=1; }

r="$out/repo"
bash "$here/setup.sh" "$r" >/dev/null || { echo "FAIL: setup.sh failed"; exit 1; }
berr="$(bash "$here/briefs.sh" --rebuttal "$r" 2>&1 >/dev/null)" || { echo "FAIL: briefs.sh --rebuttal failed: $berr"; exit 1; }
b="$r.briefs/rebuttal"

# The rebuttal brief's first sentence, as VERIFY.md has it.
first="$(awk '/^#+ Rebuttal Verifier brief/ { on = 1; next } on && /^"/ { sub(/^"/, ""); print; exit }' "$verify" | sed 's/\. .*/./')"
[ -n "$first" ] || bad "VERIFY.md has no Rebuttal Verifier brief section with a quoted brief"

n=0
for f in "$b"/rebuttal-*.md; do
  [ -s "$f" ] || continue
  n=$((n + 1))
  name="$(basename "$f")"
  [ -n "$first" ] && { grep -qF -- "$first" "$f" || bad "$name: lacks the rebuttal Verifier brief from VERIFY.md"; }
  [ "$(grep -c '^### ' "$f")" = 1 ] || bad "$name: should hold exactly one Finding"
  grep -q '^- Id: R1-[0-9]' "$f" || bad "$name: the Finding has no id"
  grep -q '^## The rebuttal' "$f" || bad "$name: has no rebuttal section"
  grep -q '^## Inputs for this Review' "$f" || bad "$name: lacks the Review's inputs"
  grep -qi 'EXPECTED\|VERIFY-ONLY\|REBUTTALS\|false alarm\|planted Finding' "$f" && bad "$name: names a scoring file or gives the answer away"
  # each cited `file:line` `text` pair in the rebuttal holds at the planted head
  awk '/^## The rebuttal/ { on = 1; next } on' "$f" | grep -o '`[a-z_/]*\.py:[0-9]*` `[^`]*`' | while read -r cite; do
    loc="$(printf '%s' "$cite" | sed 's/^`\([^`]*\)`.*/\1/')"; text="$(printf '%s' "$cite" | sed 's/^`[^`]*` `\(.*\)`$/\1/')"
    git -C "$r" show "planted:${loc%%:*}" | sed -n "${loc##*:}p" | grep -qF -- "$text" || echo "FAIL: $name: $loc does not hold \`$text\`"
  done | grep . && fail=1
done
[ "$n" = 4 ] || bad "expected 4 rebuttal briefs, found $n"
# the briefs sit outside the scratch repo
[ -z "$(find "$r" -path "$r/.git" -prune -o -name 'rebuttal-*' -print)" ] || bad "a rebuttal brief is inside the scratch repo"

rm -rf "$out"
[ "$fail" = 0 ] && echo "rebuttal fixture: all checks pass"
exit "$fail"
