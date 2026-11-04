#!/usr/bin/env bash
# Builds the script-briefs case in a new directory: the planted fixture as <out-dir>/repo, the Finders' canned final
# messages in <out-dir>/messages/, and the prompt for the fresh subagent as <out-dir>/PROMPT.md (<plugins> replaced
# by the path you pass: a copy of the plugins/ folder under test, the branch's or main's).
# Usage: make-case.sh <new-out-dir> <plugins-dir>
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
out="${1:?usage: make-case.sh <new-out-dir> <plugins-dir>}"; plugins="${2:?usage: make-case.sh <new-out-dir> <plugins-dir>}"
mkdir -p "$out"; out="$(cd "$out" && pwd -P)"; plugins="$(cd "$plugins" && pwd -P)"
[ -z "$(ls -A "$out")" ] || { echo "not empty: $out" >&2; exit 1; }
bash "$here/../setup.sh" "$out/repo" >/dev/null
mkdir "$out/messages"; cp "$here"/messages/*.txt "$out/messages/"
sed -e "s|<plugins>|$plugins|g" -e "s|<repo>|$out/repo|g" -e "s|<messages>|$out/messages|g" -e "s|<briefs>|$out/repo.briefs/round|g" \
  "$here/PROMPT.md" >"$out/PROMPT.md"
echo "Case ready in $out: give the subagent PROMPT.md; score with: python3 $here/score.py $out"
