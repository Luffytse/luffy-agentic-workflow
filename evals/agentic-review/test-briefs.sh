#!/usr/bin/env bash
# Checks the brief builder (briefs.sh) against the review-rounds skill files: it builds the planted fixture with setup.sh,
# builds the briefs at every level and for the Verify-only check, and checks each Finder and Verifier gets what the
# skill says it gets, and nothing it says to leave out. It runs no agent. It tests the routing (which part goes into
# which brief), never a skill's wording: each part is found by a line brief-lib.sh cuts from the skill files (the first
# line of a quoted brief, or the first body line under a section's heading, so a brief that keeps a heading but loses
# its body fails), so rewording the body of a part does not fail it. Renaming a heading or label brief-lib.sh cuts by
# does, and brief-lib.sh names it.
# Usage: bash evals/agentic-review/test-briefs.sh
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
skill="$here/../../plugins/dev-skills/skills/review-rounds"
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

# What the skill files say, cut out by brief-lib.sh (it stops with a message if a part is missing); each marker is the
# first line of a part.
. "$here/brief-lib.sh"
load_rules "$skill"
first() { printf '%s\n' "$1" | sed -n '/./{p;q;}'; }
# body <section>: the section's first body line, skipping its heading, blank lines, code fences and sub-headings
body() { printf '%s\n' "$1" | awk 'NR > 1 && !/^[[:space:]]*$/ && !/^```/ && !/^#/ {print; exit}'; }
shared="$(first "$shared")"; copy="$(first "$copy_rule")"
format_m="$(body "$format")"; important_m="$(first "$important")"; smell_m="$(body "$smell")"; drift_m="$(body "$drift")"
for m in "$format_m" "$smell_m" "$drift_m"; do [ -n "$m" ] || { echo "FAIL: a section brief-lib.sh cuts has no body line"; exit 1; }; done
verifier_m="$(first "$verifier_brief")"; security_m="$(first "$security")"
angle="Bugs and edge cases"   # briefs.sh's default angle
always_py="public function without a docstring"   # the fixture's Always check line for the Python files the diff touches
always_sh="unquoted variable"                      # the fixture's Always check line for shell scripts, which the diff does not touch

expect_files() {
  level="$1"; shift
  for f in "$@"; do [ -f "$b/$level/$f" ] && ok "$level writes $f" || no "$level writes $f"; done
  n="$(ls "$b/$level" | wc -l | tr -d ' ')"
  [ "$n" = "$#" ] && ok "$level writes only those $# files" || no "$level writes $n files, expected $#: $(ls "$b/$level" | tr '\n' ' ')"
}
expect_files quick finder-standards.md finder-spec.md verifier.md
expect_files standard finder-standards.md finder-spec.md finder-adversarial.md verifier.md
expect_files deep finder-standards.md finder-spec.md finder-adversarial.md finder-security.md verifier.md
expect_files standard-verify-only verifier.md

for level in quick standard deep; do
  for f in "$b/$level"/finder-*.md; do
    n="$level/$(basename "$f")"
    has "$n has the shared brief" "$f" "$shared"
    has "$n has the copy rule" "$f" "$copy"
    has "$n has the Finding format" "$f" "$format_m"
    has "$n has the meaning of Important" "$f" "$important_m"
    has "$n has the Boundary record line" "$f" "The Boundary record: none"
    hasnt "$n has no Always check line for shell scripts" "$f" "$always_sh"
  done
  has "$level standards Finder has the Python Always check line" "$b/$level/finder-standards.md" "$always_py"
  has "$level standards Finder has the smell baseline (the diff changes code)" "$b/$level/finder-standards.md" "$smell_m"
  has "$level standards Finder has the docs index drift check" "$b/$level/finder-standards.md" "$drift_m"
  has "$level spec Finder has the spec" "$b/$level/finder-spec.md" "spare cents"
  hasnt "$level spec Finder has no Always check line" "$b/$level/finder-spec.md" "$always_py"
  has "$level Verifier has the Verifier brief" "$b/$level/verifier.md" "$verifier_m"
  has "$level Verifier has the copy rule" "$b/$level/verifier.md" "$copy"
  hasnt "$level Verifier has no Always check line before any candidate is raised from one" "$b/$level/verifier.md" "$always_py"
done
for level in standard deep; do
  f="$b/$level/finder-adversarial.md"
  has "$level adversarial Finder names its angle" "$f" "$angle"
  hasnt "$level adversarial Finder has no Always check line" "$f" "$always_py"
  hasnt "$level adversarial Finder has no smell baseline" "$f" "$smell_m"
  hasnt "$level adversarial Finder has no spec" "$f" "spare cents"
done
has "deep security Finder has the security brief" "$b/deep/finder-security.md" "$security_m"
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
