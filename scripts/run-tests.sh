#!/usr/bin/env bash
# Runs every test under scripts/ and exits non-zero if any fails. It is what CI runs once the
# workflow step that calls it is in place (that line is committed by hand).
# A new test joins by its file name alone: no list to edit. A test is a regular file named test*
# anywhere under scripts/ (the tests of this repo's tooling and of the scripts the plugin ships), except in a
# __pycache__ folder (compiled files Python leaves, not tests); nothing outside scripts/ is run. A .sh test runs with
# bash and a .py test with python3, each from the repo root, and passes by exiting 0. Nothing is skipped silently: a test* file with any other extension
# (it cannot be run) fails and is named, and finding no test at all fails.
# Usage: scripts/run-tests.sh [root]   (root defaults to the repo root; the self-test passes a disposable tree)
set -u
root=${1:-$(cd "$(dirname "$0")/.." && pwd)}
cd "$root" || exit 2
list=$(mktemp); trap 'rm -f "$list"' EXIT
find scripts -type f -name 'test*' -not -path '*/__pycache__/*' -print0 > "$list" || { echo "FAIL: find could not read scripts/"; exit 2; }
failed=()
count=0
while IFS= read -r -d '' t; do
  count=$((count + 1))
  case "$t" in
    *.sh) cmd=(bash "$t");;
    *.py) cmd=(python3 "$t");;
    *) echo "FAIL $t"; echo "    named test* but not .sh or .py, so it cannot be run"; failed+=("$t"); continue;;
  esac
  if out=$("${cmd[@]}" 2>&1 </dev/null); then
    echo "PASS $t"
  else
    echo "FAIL $t"; printf '%s\n' "$out" | sed 's/^/    /'
    failed+=("$t")
  fi
done < <(LC_ALL=C sort -z "$list")
echo "ran $count tests, ${#failed[@]} failed"
[ "$count" -gt 0 ] || { echo "FAIL: no test* file found under scripts/"; exit 1; }
for t in "${failed[@]+"${failed[@]}"}"; do echo "FAILED: $t"; done
[ ${#failed[@]} = 0 ]
