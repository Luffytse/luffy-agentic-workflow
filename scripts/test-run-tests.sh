#!/usr/bin/env bash
# Tests scripts/run-tests.sh through its exit code over disposable trees: a clean tree passes,
# a planted failing .sh or .py test* file, or one in a path with spaces, exits non-zero and is named, a test* file
# it cannot run and a tree with no tests also fail, and a file not named test* is ignored, and a test* file in a __pycache__ folder (a compiled .pyc) is skipped.
set -u
here=$(cd "$(dirname "$0")" && pwd)
runner="$here/run-tests.sh"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
fail=0
mkdir -p "$tmp/evals/a" "$tmp/evals/fx/tests" "$tmp/scripts"
printf '#!/usr/bin/env bash\nexit 0\n' > "$tmp/evals/a/test-ok.sh"
printf 'import sys\nsys.exit(0)\n' > "$tmp/scripts/test_ok.py"
printf 'exit 1\n' > "$tmp/evals/a/notatest.sh"      # not named test*: ignored
printf 'exit 1\n' > "$tmp/evals/fx/tests/test_fixture.sh"   # fixture code under a tests/ folder: ignored

out=$("$runner" "$tmp" 2>&1); rc=$?
[ $rc = 0 ] || { echo "FAIL: clean tree exited $rc: $out"; fail=1; }

printf '#!/usr/bin/env bash\nexit 3\n' > "$tmp/evals/a/test-planted.sh"
out=$("$runner" "$tmp" 2>&1); rc=$?
[ $rc != 0 ] || { echo "FAIL: planted failing test exited 0"; fail=1; }
case "$out" in *evals/a/test-planted.sh*) ;; *) echo "FAIL: output does not name the planted test: $out"; fail=1;; esac

printf 'import sys\nsys.exit(1)\n' > "$tmp/scripts/test_planted.py"
out=$("$runner" "$tmp" 2>&1); rc=$?
[ $rc != 0 ] || { echo "FAIL: planted failing .py test exited 0"; fail=1; }
case "$out" in *scripts/test_planted.py*) ;; *) echo "FAIL: output does not name the planted .py test: $out"; fail=1;; esac
rm "$tmp/scripts/test_planted.py" "$tmp/evals/a/test-planted.sh"

mkdir -p "$tmp/evals/my dir"
printf 'exit 5\n' > "$tmp/evals/my dir/test one.sh"
out=$("$runner" "$tmp" 2>&1); rc=$?
[ $rc != 0 ] || { echo "FAIL: failing test in a path with spaces exited 0"; fail=1; }
case "$out" in *"evals/my dir/test one.sh"*) ;; *) echo "FAIL: output does not name the spaced path: $out"; fail=1;; esac
rm -r "$tmp/evals/my dir"

printf 'x\n' > "$tmp/evals/a/test-notes.txt"
out=$("$runner" "$tmp" 2>&1); rc=$?
[ $rc != 0 ] || { echo "FAIL: a test* file with another extension exited 0"; fail=1; }
case "$out" in *evals/a/test-notes.txt*) ;; *) echo "FAIL: output does not name the unrunnable file: $out"; fail=1;; esac
rm "$tmp/evals/a/test-notes.txt"

mkdir -p "$tmp/evals/a/__pycache__"
printf 'x\n' > "$tmp/evals/a/__pycache__/test_x.cpython-311.pyc"   # a compiled test: skipped, not an unrunnable test*
out=$("$runner" "$tmp" 2>&1); rc=$?
[ $rc = 0 ] || { echo "FAIL: a __pycache__ test*.pyc made a passing tree exit $rc: $out"; fail=1; }
rm -r "$tmp/evals/a/__pycache__"

empty=$(mktemp -d); mkdir -p "$empty/evals" "$empty/scripts"
out=$("$runner" "$empty" 2>&1); rc=$?
rm -r "$empty"
[ $rc != 0 ] || { echo "FAIL: a tree with no tests exited 0"; fail=1; }

[ $fail = 0 ] && echo "ok"
exit $fail
