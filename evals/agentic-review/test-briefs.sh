#!/usr/bin/env bash
# Checks the eval's brief builder (briefs.sh), which calls the plugin's review_briefs.py, on the planted fixture: it
# builds the fixture with setup.sh, builds the briefs at every level and for the Verify-only check, and checks the
# right files come out and that the fixture's own inputs reach the right brief (the spec, the Always check line for the
# touched files and not the other one, the candidates). What each brief holds from the skill files is tested by
# evals/review-briefs/test_review_briefs.py, so this checks no skill wording. It runs no agent.
# Usage: bash evals/agentic-review/test-briefs.sh
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
fails=0
ok() { echo "ok: $1"; }
no() { echo "FAIL: $1"; fails=$((fails + 1)); }
has() { if grep -qF -- "$3" "$2"; then ok "$1"; else no "$1"; fi; }
hasnt() { if grep -qF -- "$3" "$2"; then no "$1"; else ok "$1"; fi; }

bash "$here/setup.sh" "$tmp/repo" >/dev/null
for level in quick standard deep; do bash "$here/briefs.sh" "$tmp/repo" "$level" >/dev/null; done
bash "$here/briefs.sh" --verify-only "$tmp/repo" standard >/dev/null
b="$tmp/repo.briefs"
always_py="public function without a docstring"   # the fixture's Always check line for the Python files the diff touches
always_sh="unquoted variable"                      # the fixture's Always check line for shell scripts, which the diff does not touch

expect_files() {
  level="$1"; shift
  for f in "$@"; do [ -f "$b/$level/$f" ] && ok "$level writes $f" || no "$level writes $f"; done
  n="$(ls "$b/$level" | wc -l | tr -d ' ')"
  [ "$n" = "$#" ] && ok "$level writes only those $# files" || no "$level writes $n files, expected $#: $(ls "$b/$level" | tr '\n' ' ')"
}
expect_files quick finder-standards.md finder-spec.md
expect_files standard finder-standards.md finder-spec.md finder-adversarial.md
expect_files deep finder-standards.md finder-spec.md finder-adversarial.md finder-security.md
expect_files standard-verify-only verifier.md
[ -d "$tmp/repo/.scratch" ] && [ -z "$(git -C "$tmp/repo" status --porcelain)" ] && ok "briefs are outside the scratch repo" || no "briefs are outside the scratch repo"

for level in quick standard deep; do
  for f in "$b/$level"/finder-*.md; do hasnt "$level/$(basename "$f") has no Always check line for shell scripts" "$f" "$always_sh"; done
  has "$level standards Finder has the Python Always check line" "$b/$level/finder-standards.md" "$always_py"
  has "$level spec Finder has the spec" "$b/$level/finder-spec.md" "spare cents"
  hasnt "$level spec Finder has no Always check line" "$b/$level/finder-spec.md" "$always_py"
done
for level in standard deep; do
  f="$b/$level/finder-adversarial.md"
  hasnt "$level adversarial Finder has no Always check line" "$f" "$always_py"
  hasnt "$level adversarial Finder has no spec" "$f" "spare cents"
done
has "deep security Finder has the spec" "$b/deep/finder-security.md" "spare cents"

v="$b/standard-verify-only/verifier.md"
for title in "Amounts go into the shared page without escaping" "settle skips the debtor after one who is paid off" \
             "settle never pays the last creditor" "Names typed by trip members reach the summary page unescaped"; do
  has "Verify-only brief holds the candidate \"$title\"" "$v" "### $title"
done
hasnt "Verify-only brief names no candidate file" "$v" "VERIFY-ONLY"
hasnt "Verify-only brief has no Always check line (no candidate is raised from one)" "$v" "$always_py"
hasnt "Verify-only brief has no placeholder left" "$v" "<<"

if [ "$fails" -gt 0 ]; then echo "$fails check(s) failed"; exit 1; fi
echo "all brief checks passed"
