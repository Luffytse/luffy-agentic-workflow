#!/usr/bin/env bash
# Builds both loop fixtures (merge, after-round3) and checks each holds what its case needs, then checks the scorer:
# a hand-written right outcome passes and planted wrong ones fail. It runs no agent.
# Usage: bash evals/agentic-review/loop/test-fixture.sh
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
fails=0
ok() { echo "ok: $1"; }
no() { echo "FAIL: $1"; fails=$((fails + 1)); }
check() { if eval "$2"; then ok "$1"; else no "$1"; fi; }
py() { (cd "$1" && python3 -I -c "import sys; sys.path.insert(0, '.'); from app.quota import *; $2"); }

# ---- merge: Round 2 after a merge of main
bash "$here/make-fixture.sh" "$tmp/m" merge >/dev/null
r="$tmp/m/repo"; g() { git -C "$r" "$@"; }
r1="$(sed -n 's/^<!-- code-review kind=round round=1 .*head=\([0-9a-f]*\) .*/\1/p' "$r/.scratch/pulls/1/01-round-1.md")"
merge="$(g rev-parse quota)"
fix="$(g rev-parse quota^1)"
check "Round 1's comment names a head on the pull request branch" '[ -n "$r1" ] && g merge-base --is-ancestor "$r1" quota'
check "the head is a merge whose first parent is the fix commit and second is main" \
  '[ "$(g rev-list --parents -n1 quota | wc -w)" = 3 ] && [ "$(g rev-parse quota^2)" = "$(g rev-parse main)" ] && [ "$(g rev-parse "$fix^")" = "$r1" ]'
check "merging main into the fix commit conflicts (merge-tree exits 1, not with an error)" '(set +e; g merge-tree --write-tree "$fix" main >/dev/null 2>&1; [ $? = 1 ])'
new="$(g log -p --first-parent --remerge-diff "$r1"..quota)"
check "the new-commits diff shows the fix commit" 'printf "%s" "$new" | grep -qE "^\+    return used < limit"'
check "the new-commits diff shows the merge's resolution" 'printf "%s" "$new" | grep -qE "^\+    return max\(0, used - limit\)"'
check "the new-commits diff hides what main brought in" '! printf "%s" "$new" | grep -q "usage_percent"'
check "a plain diff since Round 1 does show main's change, so the case can tell the two apart" 'g diff "$r1"..quota | grep -q "usage_percent"'
d="$tmp/m-head"; mkdir "$d"; g archive quota | tar -x -C "$d"
check "R1-1 is fixed at the head: the limit itself is refused" '[ "$(py "$d" "print(allowed(10, 10))")" = False ]'
check "the resolution's bug is real at the head: 3 of 10 used leaves 0" '[ "$(py "$d" "print(remaining(3, 10))")" = 0 ]'
dm="$tmp/m-main"; mkdir "$dm"; g archive main | tar -x -C "$dm"
check "main itself is right: 3 of 10 used leaves 7" '[ "$(py "$dm" "print(remaining(3, 10))")" = 7 ]'
check "the project's checks pass at the head, so only review finds it" '(cd "$d" && bash check.sh >/dev/null 2>&1)'
check "the prompt gives no answer away" '! grep -qiE "used - limit|usage_percent|resolution|expected" "$tmp/m/PROMPT.md"'

# ---- after-round3: the sort after a Round 3 that is not clean
bash "$here/make-fixture.sh" "$tmp/a" after-round3 >/dev/null
r="$tmp/a/repo"
head="$(g rev-parse fix)"
for n in 1 2 3; do check "Round $n's comment exists" '[ -f "$r/.scratch/pulls/1/0$n-round-$n.md" ]'; done
c3="$r/.scratch/pulls/1/03-round-3.md"
check "Round 3's comment is at the branch head" 'grep -q "round=3 .*head=$head " "$c3"'
check "Round 3 is not clean, one Important open" 'grep -qx "Result: not clean, 1 Important open" "$c3"'
check "R3-1 is an open Important" 'grep -qE "^\| R3-1 \| Important \|.*\| open \|" "$c3"'
check "R3-2 is an open fix Nit" 'grep -qE "^\| R3-2 \| Nit \(fix\) \|.*\| open \|" "$c3"'
d="$tmp/a-head"; mkdir "$d"; g archive fix | tar -x -C "$d"
check "R3-1 is real at the head: 12 of 10 used leaves -2" '[ "$(py "$d" "print(remaining(12, 10))")" = -2 ]'
check "the tracker doc has a Create an issue operation" 'grep -q "\*\*Create an issue\*\*" "$r/docs/dev-skills/issue-tracker.md"'
check "the triage-labels doc maps bug and ready-for-agent" 'grep -q "| \`bug\` " "$r/docs/dev-skills/triage-labels.md" && grep -q "| \`ready-for-agent\` " "$r/docs/dev-skills/triage-labels.md"'
check "no issue carries the bug label yet" '! grep -l "^Labels:.*bug" "$r"/.scratch/issues/*.md >/dev/null 2>&1'
check "the prompt gives no answer away" '! grep -qiE "ticket|dismiss|expected" "$tmp/a/PROMPT.md"'

# ---- the scorer: a right outcome passes, planted wrong ones fail
score() { python3 -I "$here/score.py" "$@" >/dev/null 2>&1; }
check "merge: the untouched fixture fails (no Round 2 comment yet)" '! score merge "$tmp/m"'
cp -R "$tmp/m" "$tmp/m0"
bash "$here/reference.sh" merge "$tmp/m" good
check "merge: a right Round 2 comment passes" 'score merge "$tmp/m"'
for bad in reports-main misses-resolution whole-pr r1-open; do
  rm -rf "$tmp/m2"; cp -R "$tmp/m0" "$tmp/m2"; bash "$here/reference.sh" merge "$tmp/m2" "$bad"
  check "merge: planted wrong outcome '$bad' fails" '! score merge "$tmp/m2"'
done
check "after-round3: the untouched fixture fails (nothing sorted yet)" '! score after-round3 "$tmp/a"'
cp -R "$tmp/a" "$tmp/a0"
bash "$here/reference.sh" after-round3 "$tmp/a" good
check "after-round3: a right sort passes" 'score after-round3 "$tmp/a"'
for bad in nit-filed no-labels round-4 not-noted; do
  rm -rf "$tmp/a2"; cp -R "$tmp/a0" "$tmp/a2"; bash "$here/reference.sh" after-round3 "$tmp/a2" "$bad"
  check "after-round3: planted wrong outcome '$bad' fails" '! score after-round3 "$tmp/a2"'
done

if [ "$fails" -gt 0 ]; then echo "$fails check(s) failed"; exit 1; fi
echo "all loop fixture checks passed"
