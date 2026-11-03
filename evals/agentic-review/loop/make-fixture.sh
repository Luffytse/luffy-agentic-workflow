#!/usr/bin/env bash
# Builds a loop fixture of the agentic-review eval: a small Python repo with a local Markdown tracker and pull request 1,
# part way through its review.
# Usage: make-fixture.sh <out-dir> <merge|after-round3|empty-round>
# Makes <out-dir>/repo and <out-dir>/PROMPT.md.
# `merge`: branch quota has had Round 1 (R1-1 open). Since then the owner fixed R1-1, and merged main, which had changed
#   the same function, so the merge has a conflict resolution, and that resolution swaps two operands. main also added a
#   file with a bug of its own, which is not part of the pull request. Round 2 is next.
# `after-round3`: branch fix has had three Rounds; Round 3 is not clean, with one open Important (real at the head) and
#   one open "fix" Nit, and nothing has been committed since.
# `empty-round`: branch quota had a clean Round 1 (only a dismissed Nit). Since then the owner merged main, which had changed
#   the same function; the merge conflicted and its resolution is right. Round 2 is next, and it has nothing to verify:
#   a Finder has nothing to report and no earlier Finding is open. main also added a file with a bug of its own.
# The scoring (EXPECTED.md, score.py) stays next to this script, never in the repo or the prompt.
# See evals/agentic-review/README.md, "Loop cases".
set -eu
usage="usage: make-fixture.sh <out-dir> <merge|after-round3|empty-round>"
out="${1:?$usage}"; case_="${2:?$usage}"
case "$case_" in merge|after-round3|empty-round) ;; *) echo "unknown case: $case_" >&2; exit 2 ;; esac
[ -e "$out" ] && { echo "$out exists" >&2; exit 2; }
mkdir -p "$out"; out="$(cd "$out" && pwd -P)"
r="$out/repo"
mkdir -p "$r/app" "$r/tests" "$r/docs/dev-skills" "$r/.scratch/issues" "$r/.scratch/pulls/1"
git -C "$r" init -q -b main
git -C "$r" config user.name fixture
git -C "$r" config user.email fixture@example.invalid
echo ".scratch/" >>"$r/.git/info/exclude"
commit() { git -C "$r" add -A && git -C "$r" commit -q -m "$1" && git -C "$r" rev-parse HEAD; }

cat >"$r/CLAUDE.md" <<'MD'
# quota

Per-account request quotas for a small web service. Run `bash check.sh` before each push.

## Agent skills

Start at `docs/dev-skills/index.md`. Issues and pull requests are local Markdown files: see `docs/dev-skills/issue-tracker.md`. Triage labels: `docs/dev-skills/triage-labels.md`. The Boundary record is `docs/dev-skills/boundaries.md`.
MD

cat >"$r/REVIEW.md" <<'MD'
# Review rules

## Important

The default meaning of Important applies.

## Skip

Nothing yet.

## Always check

Nothing yet.
MD

cat >"$r/docs/dev-skills/index.md" <<'MD'
# Docs index

- [docs/dev-skills/issue-tracker.md](issue-tracker.md): the local Markdown tracker and its operations. Read before any tracker operation.
- [docs/dev-skills/triage-labels.md](triage-labels.md): the label string for each triage role. Read when labelling an issue.
- [docs/dev-skills/boundaries.md](boundaries.md): the Boundary record. Read when deciding whether an action needs the user.
MD

cat >"$r/docs/dev-skills/issue-tracker.md" <<'MD'
# Issue tracker: local Markdown

Issues are files under `.scratch/issues/`, one per issue, named `NN-slug.md`. Each starts with the header lines `Title:`, `Labels:` (comma-separated) and `Status:` (open or closed), then the body.

- **Read an issue**: read its file, its `## Comments` section included.
- **Create an issue**: write a new file `.scratch/issues/NN-slug.md`, `NN` one more than the highest in use, with the header lines and the body. Its link is its path.
- **Comment on an issue**: append to its `## Comments` section (add the heading at the end of the file if it is missing) a `### Comment <n>` heading and the text under it.
- **Pull requests**: there is no forge. A pull request is a file `.scratch/pulls/<n>.md` with `Title:`, `Base:`, `Head:`, `State:` and its body. Its comments are files `.scratch/pulls/<n>/NN-<slug>.md`, in order: posting a comment writes the next file, editing a comment edits its file. Merging is setting `State: merged`. There is no CI: the project's checks are `bash check.sh`.
MD

cat >"$r/docs/dev-skills/triage-labels.md" <<'MD'
# Triage labels

| Role | Label |
|------|-------|
| `needs-triage` | `needs-triage` |
| `needs-info` | `needs-info` |
| `ready-for-agent` | `ready-for-agent` |
| `ready-for-human` | `ready-for-human` |
| `wontfix` | `wontfix` |
| `bug` | `bug` |
| `enhancement` | `enhancement` |
MD

cat >"$r/docs/dev-skills/boundaries.md" <<'MD'
# Boundary record

- **Irreversible actions agents may take**: any.
- **Actions that need the user's approval**: none.
- **Budget**: none.
- **Check-in interval**: 1 hour.
MD

cat >"$r/check.sh" <<'SH'
#!/usr/bin/env bash
# The project's checks: the unit tests.
set -euo pipefail
cd "$(dirname "$0")"
python3 -m unittest -q 2>&1 | tail -n 1
SH

: >"$r/app/__init__.py"; : >"$r/tests/__init__.py"
cat >"$r/app/quota.py" <<'PY'
"""Request quotas for one account."""


def remaining(used, limit):
    """How many requests are left this hour."""
    return limit - used
PY
cat >"$r/tests/test_quota.py" <<'PY'
import unittest

from app.quota import remaining


class Remaining(unittest.TestCase):
    def test_none_left_at_the_limit(self):
        self.assertEqual(remaining(10, 10), 0)
PY
commit "quota: requests left this hour" >/dev/null

# round_comment <file> <round> <head> <base> <reviewed> <result> <finders> <rows>
round_comment() {
  cat >"$r/.scratch/pulls/1/$1" <<MD
<!-- code-review kind=round round=$2 level=Standard head=$3 base=$4 -->
## Code review: Round $2 of at most 3 (Standard)

Level: Standard (app/quota.py: changes what the quota functions return)
Reviewed: $5
Result: $6
Finders: $7

| id | Severity | Bug class | Locations | Claim | Status | Note |
|----|----------|-----------|-----------|-------|--------|------|
$8
MD
}

if [ "$case_" = merge ] || [ "$case_" = empty-round ]; then
  empty=0; [ "$case_" = empty-round ] && empty=1
  cat >"$r/.scratch/issues/01-block-over-limit.md" <<'MD'
Title: Block requests over the hour's limit
Labels: enhancement, ready-for-agent
Status: open

## What to build

- `allowed(used, limit)` says whether one more request fits: true while `used` is below `limit`, false once it reaches it.
- `remaining(used, limit)` is how many requests are left this hour, and never below zero.

## Acceptance criteria

- [ ] An account gets exactly `limit` requests in an hour.
- [ ] `remaining` reports the requests left, and 0 once the limit is reached or passed.
MD
  git -C "$r" switch -q -c quota
  cat >"$r/app/quota.py" <<'PY'
"""Request quotas for one account."""


def remaining(used, limit):
    """How many requests are left this hour; none once the limit is reached."""
    return limit - used if used < limit else 0


def allowed(used, limit):
    """Whether one more request fits in this hour."""
    return used <= limit
PY
  [ "$empty" = 1 ] && sed -i.bak 's/return used <= limit/return used < limit/' "$r/app/quota.py" && rm "$r/app/quota.py.bak"
  cat >>"$r/tests/test_quota.py" <<'PY'


class Allowed(unittest.TestCase):
    def test_first_request_fits(self):
        from app.quota import allowed
        self.assertTrue(allowed(0, 10))
PY
  r1="$(commit "Block requests over the hour's limit (#1)")"
  if [ "$empty" = 1 ]; then
    round_comment 01-round-1.md 1 "$r1" "$(git -C "$r" rev-parse main)" "the whole pull request" "clean" \
      "standards, spec, adversarial (bugs and edge cases)" \
      "| R1-1 | Nit (skip) | docstring wording | app/quota.py:5 | \"none once the limit is reached\" could say \"or passed\" | dismissed | Verifier: the code returns 0 past the limit too; wording only |"
  else
    line="$(grep -n 'return used <= limit' "$r/app/quota.py" | cut -d: -f1)"
    round_comment 01-round-1.md 1 "$r1" "$(git -C "$r" rev-parse main)" "the whole pull request" "not clean, 1 Important open" \
      "standards, spec, adversarial (bugs and edge cases)" \
      "| R1-1 | Important | off-by-one at the limit | app/quota.py:$line | a request is allowed when \`used\` equals \`limit\`, so an account gets \`limit + 1\` requests | open | adversarial Finder |
| R1-2 | Nit (skip) | docstring wording | app/quota.py:5 | \"none once the limit is reached\" could say \"or passed\" | dismissed | Verifier: the code returns 0 past the limit too; wording only |"
    sed -i.bak 's/return used <= limit/return used < limit/' "$r/app/quota.py" && rm "$r/app/quota.py.bak"
    cat >>"$r/tests/test_quota.py" <<'PY'

    def test_the_limit_itself_is_refused(self):
        from app.quota import allowed
        self.assertFalse(allowed(10, 10))
PY
    commit "fix: refuse the request that reaches the limit (R1-1)" >/dev/null

  fi
  git -C "$r" switch -q main
  cat >"$r/app/quota.py" <<'PY'
"""Request quotas for one account."""


def remaining(used, limit):
    """How many requests are left this hour, never below zero."""
    return max(0, limit - used)
PY
  cat >"$r/app/report.py" <<'PY'
"""The usage line on the account page."""


def usage_percent(used, limit):
    """How much of this hour's quota is used, as a percentage."""
    return used / limit * 100
PY
  commit "quota: never report fewer than zero requests left; usage percent" >/dev/null

  git -C "$r" switch -q quota
  git -C "$r" merge -q main >/dev/null 2>&1 && { echo "the merge was meant to conflict" >&2; exit 1; }
  cat >"$r/app/quota.py" <<'PY'
"""Request quotas for one account."""


def remaining(used, limit):
    """How many requests are left this hour, never below zero."""
    return RESOLVED


def allowed(used, limit):
    """Whether one more request fits in this hour."""
    return used < limit
PY
  if [ "$empty" = 1 ]; then sed -i.bak 's/RESOLVED/max(0, limit - used)/' "$r/app/quota.py"; else sed -i.bak 's/RESOLVED/max(0, used - limit)/' "$r/app/quota.py"; fi
  rm "$r/app/quota.py.bak"
  git -C "$r" add -A
  git -C "$r" commit -q --no-edit
  git -C "$r" switch -q main
  cat >"$r/.scratch/pulls/1.md" <<'MD'
Title: Block requests over the hour's limit
Base: main
Head: quota
State: open

Closes #1 (`.scratch/issues/01-block-over-limit.md`). Adds `allowed`, and `remaining` stops at zero.
MD
  intro="Its Round 1 comment is posted. Since then the owner has committed a fix and merged \`main\` into the branch."
  [ "$empty" = 1 ] && intro="Its Round 1 comment is posted. Since then the owner has merged \`main\` into the branch."
  task="run the pull request's next Round, as the skills say"
else
  cat >"$r/.scratch/issues/01-burst-allowance.md" <<'MD'
Title: A burst allowance on top of the hourly limit
Labels: enhancement, ready-for-agent
Status: open

## What to build

- `allowed(used, limit, burst=0)`: one more request fits while `used` is below `limit + burst`.
- `remaining(used, limit, burst=0)`: the requests left this hour, the burst counted, and never below zero.

## Acceptance criteria

- [ ] An account with a burst of 5 and a limit of 10 gets exactly 15 requests in an hour.
- [ ] `remaining` reports 0, never a negative number, once the allowance is used up.
MD
  git -C "$r" switch -q -c fix
  cat >"$r/app/quota.py" <<'PY'
"""Request quotas for one account."""


def remaining(used, limit, burst=0):
    """How many requests are left this hour, the burst counted; never below zero."""
    return limit - used


def allowed(used, limit, burst=0):
    """Whether one more request fits in this hour."""
    return used <= limit + burst
PY
  h1="$(commit "A burst allowance on top of the hourly limit (#1)")"
  sed -i.bak 's/return used <= limit + burst/return used < limit + burst/' "$r/app/quota.py" && rm "$r/app/quota.py.bak"
  h2="$(commit "fix: refuse the request that reaches the allowance (R1-1)")"
  python3 - "$r/app/quota.py" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("    return limit - used\n", "    return limit + burst - used\n")
s = s.replace("    return used < limit + burst\n", "    n = limit + burst\n    return used < n\n")
open(p, "w").write(s)
PY
  cat >>"$r/tests/test_quota.py" <<'PY'


class Burst(unittest.TestCase):
    def test_burst_is_counted(self):
        from app.quota import allowed, remaining
        self.assertTrue(allowed(12, 10, 5))
        self.assertFalse(allowed(15, 10, 5))
        self.assertEqual(remaining(12, 10, 5), 3)
PY
  h3="$(commit "fix: count the burst in remaining (R2-1)")"
  base="$(git -C "$r" rev-parse main)"
  rl="$(grep -n 'return limit + burst - used' "$r/app/quota.py" | cut -d: -f1)"
  nl="$(grep -n 'n = limit + burst' "$r/app/quota.py" | cut -d: -f1)"
  al="$(grep -n 'return used < n' "$r/app/quota.py" | cut -d: -f1)"
  round_comment 01-round-1.md 1 "$h1" "$base" "the whole pull request" "not clean, 1 Important open" \
    "standards, spec, adversarial (bugs and edge cases)" \
    "| R1-1 | Important | off-by-one at the limit | app/quota.py:11 | a request is allowed when \`used\` equals \`limit + burst\`, one more than the allowance | open | adversarial Finder |"
  round_comment 02-round-2.md 2 "$h2" "$h1" "the new commits $h1..$h2" "not clean, 1 Important open" "standards and spec" \
    "| R1-1 | Important | off-by-one at the limit | app/quota.py:11 | a request is allowed when \`used\` equals \`limit + burst\`, one more than the allowance | fixed | fixed in $h2, confirmed by Verifier |
| R2-1 | Important | burst not counted | app/quota.py:6 | \`remaining\` ignores \`burst\`, so it reports too few requests left | open | spec Finder |"
  round_comment 03-round-3.md 3 "$h3" "$h2" "the new commits $h2..$h3" "not clean, 1 Important open" "standards and spec" \
    "| R2-1 | Important | burst not counted | app/quota.py:$rl | \`remaining\` ignores \`burst\`, so it reports too few requests left | fixed | fixed in $h3, confirmed by Verifier |
| R3-1 | Important | negative requests left | app/quota.py:$rl | \`remaining\` goes below zero once the allowance is used up: \`remaining(12, 10)\` is -2, and the spec says never below zero | open | spec Finder |
| R3-2 | Nit (fix) | mysterious name | app/quota.py:$nl-$al | \`n\` holds the allowance; \`allowance\` would say so | open | standards Finder |"
  git -C "$r" switch -q main
  cat >"$r/.scratch/pulls/1.md" <<'MD'
Title: A burst allowance on top of the hourly limit
Base: main
Head: fix
State: open

Closes #1 (`.scratch/issues/01-burst-allowance.md`). Adds a burst allowance to `allowed` and `remaining`.
MD
  intro="Its Round 3 comment has just been posted (\`.scratch/pulls/1/03-round-3.md\`), and the owner has committed nothing since."
  task="carry the review on from here, as the skills say, up to the point where the pull request is ready to merge or waits for someone"
fi

cat >"$out/PROMPT.md" <<MD
Give the text between the lines to a fresh top-level session that can start subagents, its working directory $r,
with <checkout> replaced by the path of a copy of this checkout's plugins/ folder.

---
You are the build thread of pull request 1 in this repo (\`.scratch/pulls/1.md\`). $intro

Load the agentic-review skill from <checkout>/dev-skills/skills/agentic-review/SKILL.md and $task. Start subagents where
the skills say to. Every tracker and pull request operation goes through \`docs/dev-skills/issue-tracker.md\`. Do not
merge the pull request; you are its owner, so make any fix or commit yourself on its branch.

Finally, report what you would report to your caller.
---
MD
echo "Loop fixture ($case_) ready in $out: repo and PROMPT.md"
