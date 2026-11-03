#!/usr/bin/env bash
# Builds the Round 0 fixture of the agentic-review eval: a small repo that writes skills, with three one-commit branches
# off main, each a pull request Round 0 must size.
# Usage: make-fixture.sh <out-dir>
# Makes <out-dir>/repo and one <out-dir>/PROMPT-<branch>.md per branch:
#   version-only  the manifest's version field and a changelog entry (the bump at merge time)
#   typo          one misspelled word fixed in a skill file; what the skill says is unchanged
#   rule-change   a skill rule now says something else
# REVIEW.md has no "Review levels" section, so the defaults apply. The expected levels are in EXPECTED.md, next to
# this script, never in the repo or the prompts. See evals/agentic-review/README.md, "Round 0".
set -eu
out="${1:?usage: make-fixture.sh <out-dir>}"
[ -e "$out" ] && { echo "$out exists" >&2; exit 2; }
mkdir -p "$out"; out="$(cd "$out" && pwd -P)"
r="$out/repo"
mkdir -p "$r/plugin" "$r/skills/greet" "$r/docs/dev-skills"
git -C "$r" init -q -b main
git -C "$r" config user.name fixture
git -C "$r" config user.email fixture@example.invalid

cat >"$r/CLAUDE.md" <<'MD'
# greeter

A plugin of skills that tell a coding agent how to greet the people it works with. Run `bash check.sh` before each push.

## Agent skills

Start at `docs/dev-skills/index.md`. The Boundary record is `docs/dev-skills/boundaries.md`.
MD

cat >"$r/REVIEW.md" <<'MD'
# Review rules

## Important

The default meaning of Important applies.

## Skip

Nothing yet.

## Always check

- **rule without a reason** (files: `skills/**/SKILL.md`): a rule that tells the agent to do something says why, in the same paragraph.
MD

cat >"$r/docs/dev-skills/index.md" <<'MD'
# Docs index

- [docs/dev-skills/boundaries.md](boundaries.md): the Boundary record. Read when deciding whether an action needs the user.
MD

cat >"$r/docs/dev-skills/boundaries.md" <<'MD'
# Boundary record

- **Irreversible actions agents may take**: any, except deleting a user's saved greetings.
- **Actions that need the user's approval**: deleting a user's saved greetings.
- **Budget**: none.
- **Check-in interval**: 1 hour.
MD

cat >"$r/plugin/plugin.json" <<'JSON'
{
  "name": "greeter",
  "version": "0.3.0",
  "description": "Skills for greeting the people an agent works with"
}
JSON

cat >"$r/CHANGELOG.md" <<'MD'
# Changelog

## 0.3.0

- `greet`: greet a user who returns after a week with "welcome back".
MD

cat >"$r/skills/greet/SKILL.md" <<'MD'
---
name: greet
description: Greet the person you work with at the start of a session. Use when a session starts.
---

Greet the user by their first name, because people who work together use first names.

When you recieve a message that starts with a question, answer the question first and greet after, so the greeting never delays the answer.

A user who returns after a week gets "welcome back", so they know the session remembers them.
MD

cat >"$r/check.sh" <<'SH'
#!/usr/bin/env bash
# The project's checks: the manifest is JSON with a version, and each skill has a SKILL.md naming its folder.
set -eu
cd "$(dirname "$0")"
python3 -c 'import json; v = json.load(open("plugin/plugin.json"))["version"]; assert v.count(".") == 2, v'
for d in skills/*/; do
  n="$(basename "$d")"
  grep -qx "name: $n" "$d/SKILL.md" || { echo "skill $n: SKILL.md does not name its folder" >&2; exit 1; }
done
echo "checks passed"
SH

git -C "$r" add -A
git -C "$r" commit -q -m "greet: welcome back after a week (0.3.0)"

branch() { git -C "$r" switch -q -c "$1" main; }
commit() { git -C "$r" add -A; git -C "$r" commit -q -m "$1"; git -C "$r" switch -q main; }

branch version-only
sed -i.bak 's/"version": "0.3.0"/"version": "0.4.0"/' "$r/plugin/plugin.json" && rm "$r/plugin/plugin.json.bak"
python3 - "$r/CHANGELOG.md" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("# Changelog\n\n", "# Changelog\n\n## 0.4.0\n\n- `greet`: answer a question before greeting.\n\n", 1)
open(p, "w").write(s)
PY
commit "chore: bump greeter to 0.4.0"

branch typo
sed -i.bak 's/When you recieve a message/When you receive a message/' "$r/skills/greet/SKILL.md" && rm "$r/skills/greet/SKILL.md.bak"
commit "fix: spelling in greet"

branch rule-change
python3 - "$r/skills/greet/SKILL.md" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("Greet the user by their first name, because people who work together use first names.",
              "Greet the user by their full name, and switch to their first name only once they sign with it, because a new colleague is greeted formally.")
open(p, "w").write(s)
PY
commit "feat: greet by full name until the user signs with a first name"

for b in version-only typo rule-change; do
  cat >"$out/PROMPT-$b.md" <<MD
Give the text between the lines to a fresh top-level session whose working directory is $r, with <checkout> replaced
by the path of a copy of this checkout's plugins/ folder.

---
You are the build thread of pull request 1 in this repo: branch \`$b\` into \`main\`. There is no forge: wherever a skill
says to post a comment on the pull request, write its body to $out/comments-$b.md instead.

Load the agentic-review skill from <checkout>/dev-skills/skills/agentic-review/SKILL.md and review the pull request.
If Round 0 hands over to a Round, stop there: do not load the next skill and start no subagent.

Answer with: the level Round 0 picked and its one-line reason, every file you read, every skill you loaded, and what
you wrote to $out/comments-$b.md, if anything.
---
MD
done
echo "Round 0 fixture ready in $out: repo, PROMPT-version-only.md, PROMPT-typo.md, PROMPT-rule-change.md"
