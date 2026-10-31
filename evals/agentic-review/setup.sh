#!/usr/bin/env bash
# Builds the agentic-review eval fixture as a scratch git repo.
# Usage: setup.sh <new-empty-dir>
# Result: branch `main` holds base/, branch `planted` adds one commit with the change in after/.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
dest="${1:?usage: setup.sh <new-empty-dir>}"
mkdir -p "$dest"
[ -z "$(ls -A "$dest")" ] || { echo "not empty: $dest" >&2; exit 1; }
cd "$dest"
git init -q -b main
git config user.name "eval"
git config user.email "eval@example.invalid"
# Build artifacts in base/ or after/ (a stray __pycache__ from running the fixture tests) are not fixture source.
printf '%s\n' "__pycache__/" "*.pyc" >> .git/info/exclude
cp -R "$here/base/." .
git add -A
git commit -q -m "splitter: money helpers and expenses"
git switch -q -c planted
git rm -q docs/currency.md
cp -R "$here/after/." .
git add -A
git commit -q -m "Add even splitting, settle-up and the summary page (#1)"
# The spec sits untracked in .scratch/, outside the diff, away from EXPECTED.md.
mkdir -p .scratch
cp "$here/SPEC.md" .scratch/SPEC.md
echo ".scratch/" >> .git/info/exclude
echo "Fixture ready in $dest: review branch 'planted' against 'main', spec at .scratch/SPEC.md"
