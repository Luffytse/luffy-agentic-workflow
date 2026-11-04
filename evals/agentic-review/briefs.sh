#!/usr/bin/env bash
# Builds the Finder briefs for a Round 1 of the agentic-review eval's planted fixture by calling the plugin's brief
# script (plugins/dev-skills/skills/review-rounds/review_briefs.py), the one builder; this file holds no brief text.
# Usage: briefs.sh [--verify-only] <scratch-repo> <quick|standard|deep> [angle-name]
# <scratch-repo> is the directory setup.sh built. The briefs go to <scratch-repo>.briefs/<level>/ (or
# <level>-verify-only/), a sibling of the scratch repo, so no agent working in the scratch repo can find them.
# quick writes finder-standards.md and finder-spec.md; standard adds finder-adversarial.md; deep adds
# finder-security.md too. Each file is complete: paste it whole into one fresh subagent. The Verifier brief does not
# exist yet: after the Finders have run, save each one's final message to <finder>.md in a directory and run
# `review_briefs.py verify` (see README.md).
# --verify-only writes just verifier.md: VERIFY-ONLY.md split into one report file per Finder (a Finder with no
# candidate there reports "nothing found"), checked and pasted whole by `review_briefs.py verify`. The Finders never
# get this. Its reports are kept in <level>-verify-only.reports/ for inspection.
# The adversarial angle defaults to the script's default; pass another angle name from FINDERS.md.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
verify_only=0
if [ "${1:-}" = "--verify-only" ]; then verify_only=1; shift; fi
usage="usage: briefs.sh [--verify-only] <scratch-repo> <quick|standard|deep> [angle]"
scratch="${1:?$usage}"; level="${2:?$usage}"; angle="${3:-}"
case "$level" in quick|standard|deep) ;; *) echo "level must be quick, standard or deep" >&2; exit 1 ;; esac

script="$here/../../plugins/dev-skills/skills/review-rounds/review_briefs.py"
[ -f "$script" ] || { echo "review_briefs.py not found under plugins/dev-skills" >&2; exit 1; }
git -C "$scratch" rev-parse -q --verify main >/dev/null && git -C "$scratch" rev-parse -q --verify planted >/dev/null ||
  { echo "$scratch is not a fixture built by setup.sh (needs branches main and planted)" >&2; exit 1; }
scratch="$(cd "$scratch" && pwd -P)" # absolute, no trailing slash, so the sibling output dir is outside the repo
[ -f "$scratch/.scratch/SPEC.md" ] || { echo "no .scratch/SPEC.md in $scratch" >&2; exit 1; }

common=(--base main --head planted --repo "$scratch" --spec "$scratch/.scratch/SPEC.md")
if [ "$verify_only" = 0 ]; then
  out="$scratch.briefs/$level"
  mkdir -p "$out"; rm -f "$out"/*.md
  python3 "$script" round1 --level "$level" "${common[@]}" ${angle:+--angle "$angle"} --out "$out"
else
  out="$scratch.briefs/$level-verify-only"; reports="$out.reports"
  rm -rf "$reports"; mkdir -p "$out" "$reports"; rm -f "$out"/*.md
  # Split VERIFY-ONLY.md into one report per Finder. The reports cover Deep's four Finders, so the one file serves
  # every level; the Verifier brief is the same text at any level, but the script prints premium (Deep's tier): run
  # it on the tier of the level you test.
  python3 -I - "$here/VERIFY-ONLY.md" "$reports" <<'PY'
import pathlib, re, sys
src, dest = pathlib.Path(sys.argv[1]).read_text(), pathlib.Path(sys.argv[2])
names = {"bugs and edge cases": "adversarial", "spec": "spec", "security and privacy": "security", "standards": "standards"}
parts = {k: [] for k in names.values()}
for who, body in re.findall(r"Raised by the (.*?) Finder:\n\n```\n(.*?)\n```", src, re.S):
    parts[names[who]].append(body)
for finder, bodies in parts.items():
    (dest / f"{finder}.md").write_text("\n\n".join(bodies) + "\n" if bodies else "nothing found\n")
PY
  python3 "$script" verify --level deep "${common[@]}" --reports "$reports" --out "$out"
fi
echo "Briefs for $level$([ "$verify_only" = 1 ] && echo " (verify-only)") written to $out"
