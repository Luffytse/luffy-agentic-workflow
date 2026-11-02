#!/usr/bin/env bash
# Builds a convergence fixture of the agentic-review eval.
# Usage: make-fixture.sh <out-dir> <returned|flip> <inside|outside>
# Makes <out-dir>/repo (a git repo with a local Markdown tracker under .scratch/) and <out-dir>/PROMPT.md (the scripted
# prompt for a decision-level run that carries on from Rank).
# `returned`: pull request 1 (branch backup) has had two Rounds; R1-1 (an unquoted path) was fixed and confirmed in
#   Round 2, and the fix commit since Round 2 adds a line above it and drops its quoting again. Round 3's Verify kept
#   the Finding that it is back (another Bug class name, its line shifted by one), a different claim on the same lines,
#   and a Pre-existing Finding.
# `flip`: pull request 2 (branch count) has had one Round; R1-1 (a missing list file read as an empty list) is fixed
#   since, and Round 2's Verify confirms it and kept a Finding whose fix would undo that fix, plus a different claim on
#   the same line. Pull request 1 is a closed first attempt; inside a Milestone, the issue holds its attempt record.
# `inside`: the issue carries the Milestone label the Boundary record names. `outside`: no label, no attempt record.
# The scoring (EXPECTED.md) stays in this folder, never in the repo. See evals/agentic-review/README.md,
# "Convergence check".
set -eu
usage="usage: make-fixture.sh <out-dir> <returned|flip> <inside|outside>"
out="${1:?$usage}"; fx="${2:?$usage}"; case_="${3:?$usage}"
case "$fx" in returned|flip) ;; *) echo "unknown fixture: $fx" >&2; exit 2 ;; esac
case "$case_" in inside|outside) ;; *) echo "unknown case: $case_" >&2; exit 2 ;; esac
[ -e "$out" ] && { echo "$out exists" >&2; exit 2; }
mkdir -p "$out"
out="$(cd "$out" && pwd -P)"
r="$out/repo"
mkdir -p "$r"
git -C "$r" init -q -b main
git -C "$r" config user.name fixture
git -C "$r" config user.email fixture@example.invalid
echo ".scratch/" >> "$r/.git/info/exclude"
mkdir -p "$r/docs/agents" "$r/src" "$r/tests" "$r/.scratch/issues" "$r/.scratch/pulls"
commit() { git -C "$r" add -A && git -C "$r" commit -q -m "$1" && git -C "$r" rev-parse HEAD; }

cat > "$r/CLAUDE.md" <<'MD'
# shoplist

A household shopping list kept as a plain text file, one item per line, with small shell tools. Run `bash test.sh` before each push.

## Agent skills

Start at `docs/index.md`.

### Issue tracker

Local Markdown issues under `.scratch/issues/`, pull requests under `.scratch/pulls/`. See `docs/agents/issue-tracker.md`.

### Boundaries

See `docs/agents/boundaries.md`.
MD

cat > "$r/REVIEW.md" <<'MD'
# Review rules

## Important

The default meaning of Important in `agentic-review` applies.
MD

cat > "$r/README.md" <<'MD'
# shoplist

The list lives in a text file, one item per line. The list file is created when the first item is added (`src/add.sh`).
MD

cat > "$r/docs/index.md" <<'MD'
# Docs index

- [docs/agents/issue-tracker.md](agents/issue-tracker.md): the local Markdown tracker and its operations. Read before any tracker operation.
- [docs/agents/boundaries.md](agents/boundaries.md): the Boundary record. Read when deciding whether an action needs the user, or whether work is inside a Milestone.
MD

cat > "$r/docs/agents/issue-tracker.md" <<'MD'
# Issue tracker: local Markdown

Issues are files under `.scratch/issues/`, one per issue, named `NN-slug.md`. Each starts with header lines:
`Title:`, `Type:` (milestone, spec or ticket), `Labels:` (comma-separated) and `Status:` (open or closed).

- **Read an issue**: read its file, its `## Comments` section included.
- **Create an issue**: write a new file `.scratch/issues/NN-slug.md`, `NN` one more than the highest in use, with the header lines and the body.
- **Comment on an issue**: append to its `## Comments` section (add the heading at the end of the file if it is missing) a `### Comment <n>` heading, `<n>` one more than the last, and the comment's text under it. Its link is `<issue file>#comment-<n>`.
- **Pull requests**: there is no forge. A pull request is a file `.scratch/pulls/<n>.md` with `Title:`, `Base:`, `Head:`, `State:` and its body. Its comments are files `.scratch/pulls/<n>/NN-<slug>.md`, in order; editing a comment means editing its file. There is no CI.
MD

cat > "$r/docs/agents/boundaries.md" <<'MD'
# Boundary record

What the user has agreed agents may do on their own in this repo, which actions are the user's to decide, and the limits agents work within.

- **Irreversible actions agents may take**: none.
- **Actions that need the user's approval**: none beyond the merge rules.
- **Budget**: none.
- **Check-in interval**: 1 hour.
- **Milestone label form**: `milestone-<n>` (for example `milestone-1`). An issue belongs to a Milestone when it carries that Milestone's label, and the Milestone issue carries the same label.
MD

cat > "$r/test.sh" <<'SH'
#!/usr/bin/env bash
set -e
for t in tests/*.sh; do [ -e "$t" ] && bash "$t"; done
echo "OK"
SH

cat > "$r/src/add.sh" <<'SH'
#!/usr/bin/env bash
# usage: add.sh <list-file> <item>   adds one item to the list
set -eu
list="${1:?usage: add.sh <list-file> <item>}"; item="${2:?usage: add.sh <list-file> <item>}"
echo $item >> $list
SH
cat > "$r/tests/add.sh" <<'SH'
#!/usr/bin/env bash
set -e
f="$(mktemp)"; bash src/add.sh "$f" milk; bash src/add.sh "$f" bread
[ "$(cat "$f")" = "$(printf 'milk\nbread')" ]
rm -f "$f"
SH

cat > "$r/.scratch/issues/00-milestone.md" <<'MD'
Title: Milestone 1: a list the household can rely on
Type: milestone
Labels: milestone-1
Status: open

## Goal

The household's list is never lost and always says what is left to buy.

## Features

- Back up the list (`.scratch/issues/20-backup.md`).
- Count the list's items for the shopping reminder (`.scratch/issues/30-count.md`).

## Acceptance criteria

- A backup made today can be restored tomorrow.
- The reminder says how many items are left.

## Excluded

- Syncing the list between devices.
MD

labels="enhancement"; [ "$case_" = inside ] && labels="enhancement, milestone-1"
base="$(commit "shoplist: the list file, add.sh and the agent docs")"

if [ "$fx" = returned ]; then
  issue=".scratch/issues/20-backup.md"; pr=1; branch=backup
  cat > "$r/$issue" <<MD
Title: Back up the list
Type: ticket
Labels: $labels
Status: open

## What to build

\`src/backup.sh <list-file> <backup-dir>\` copies the list into the backup folder under a new name each time, with a test.

## Acceptance criteria

- **AC1**: It works for any list path and backup folder, spaces included.
- **AC2**: Two backups never overwrite each other.
- **AC3**: A missing list file is an error that names the script.
MD
  git -C "$r" switch -q -c "$branch"
  cat > "$r/src/backup.sh" <<'SH'
#!/usr/bin/env bash
# usage: backup.sh <list-file> <backup-dir>   copies the list into the backup folder
set -eu
list="${1:?usage: backup.sh <list-file> <backup-dir>}"
dir="${2:?usage: backup.sh <list-file> <backup-dir>}"
mkdir -p $dir
cp $list $dir/list-$(date +%Y%m%d).txt
echo "backed up to $dir"
SH
  cat > "$r/tests/backup.sh" <<'SH'
#!/usr/bin/env bash
set -e
t="$(mktemp -d)"; printf 'milk\n' > "$t/list.txt"
bash src/backup.sh "$t/list.txt" "$t/backups" >/dev/null
[ "$(ls "$t/backups" | wc -l)" -ge 1 ]
if bash src/backup.sh "$t/none.txt" "$t/backups" 2>/dev/null; then exit 1; fi
rm -rf "$t"
SH
  printf '\n`bash src/backup.sh <list-file> <backup-dir>` copies the list into a backup folder.\n' >> "$r/README.md"
  c0="$(commit "Back up the list ($issue)")"
  sed -i -e '6s/.*/mkdir -p "$dir"/' -e '7s/.*/cp "$list" "$dir\/list-$(date +%Y%m%d).txt"/' "$r/src/backup.sh"
  c1="$(commit "Quote the backup paths (R1-1)")"
  cat > "$r/src/backup.sh" <<'SH'
#!/usr/bin/env bash
# usage: backup.sh <list-file> <backup-dir>   copies the list into the backup folder
set -eu
list="${1:?usage: backup.sh <list-file> <backup-dir>}"
dir="${2:?usage: backup.sh <list-file> <backup-dir>}"
mkdir -p "$dir"
stamp="$(date +%Y%m%d-%H%M%S)-$$"
cp "$list" "$dir/list-$stamp.txt"
echo "backed up to $dir"
SH
  c2="$(commit "Name each backup by the second and the process (R1-2)")"
  cat > "$r/src/backup.sh" <<'SH'
#!/usr/bin/env bash
# usage: backup.sh <list-file> <backup-dir>   copies the list into the backup folder
set -eu
list="${1:?usage: backup.sh <list-file> <backup-dir>}"
dir="${2:?usage: backup.sh <list-file> <backup-dir>}"
[ -f "$list" ] || { echo "backup: no list file: $list" >&2; exit 1; }
mkdir -p "$dir"
stamp="$(date +%Y%m%d-%H%M%S)-$$"
cp -- $list "$dir/list-$stamp.txt"
echo "backed up to $dir"
SH
  c3="$(commit "Guard the list path (R2-1, R2-2)")"
  s1="${c1:0:7}"; s2="${c2:0:7}"; s3="${c3:0:7}"
  cat > "$r/.scratch/pulls/1.md" <<MD
Title: Back up the list
Base: main
Head: backup
State: open

Adds \`src/backup.sh\` and its test. Builds \`$issue\`.
MD
  mkdir -p "$r/.scratch/pulls/1"
  cat > "$r/.scratch/pulls/1/01-round-1.md" <<MD
<!-- code-review kind=round round=1 depth=Standard head=$c0 base=$base -->
## Code review: Round 1 of at most 5 (Standard)

Reviewed: the whole pull request
Result: not clean, 2 Important open
Finders: standards, spec, adversarial (bugs and edge cases), adversarial (security and privacy)

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
| R1-1 | Important | unquoted path | src/backup.sh:6, src/backup.sh:7 | open | adversarial Finder: a list path or backup folder with a space splits into several arguments (AC1) |
| R1-2 | Important | backup overwritten | src/backup.sh:7 | open | spec Finder: a second backup the same day overwrites the first (AC2) |
MD
  cat > "$r/.scratch/pulls/1/02-round-2.md" <<MD
<!-- code-review kind=round round=2 depth=Standard head=$c2 base=$base -->
## Code review: Round 2 of at most 5 (Standard)

Reviewed: the whole pull request
Result: not clean, 1 Important open
Finders: standards, spec, adversarial (bugs and edge cases), adversarial (security and privacy)

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
| R2-1 | Important | option injection | src/backup.sh:8 | open | adversarial Finder: a list path starting with \`-\` is read by \`cp\` as an option |
| R2-2 | Nit (fix) | unclear error | src/backup.sh:4 | open | standards Finder: a missing list file ends in cp's own error, not one naming the script (AC3) |
| R1-1 | Important | unquoted path | src/backup.sh:6, src/backup.sh:8 | fixed | fixed in $s1, confirmed by Verifier |
| R1-2 | Important | backup overwritten | src/backup.sh:7, src/backup.sh:8 | fixed | fixed in $s2, confirmed by Verifier |
MD
  round=3
  findings="#### R2-1 (earlier open Important; Verifier: fixed in $s3, \`cp --\` at src/backup.sh:9)

Re-checked against the current code: the \`--\` ends the options, so a list path starting with \`-\` is read as a file.

#### R3-1 (adversarial Finder, bugs and edge cases; Verifier: keep, caused by this change, Important)

### A list path with a space splits into two arguments
- Severity (proposed): Important
- Bug class: unquoted variable
- Locations: src/backup.sh:9
- Claim: \`\$list\` is unquoted in the \`cp\` line, so a list path holding a space is split into two arguments.
- Failure scenario: \`backup.sh \"my list.txt\" backups\` runs \`cp -- my list.txt backups/list-...\`; cp fails with \"my: No such file or directory\" and no backup is made (AC1).
- Evidence: \`cp -- \$list \"\$dir/list-\$stamp.txt\"\` (src/backup.sh:9); AC1: \"It works for any list path and backup folder, spaces included.\"

#### R3-2 (adversarial Finder, security and privacy; Verifier: keep, caused by this change, Important)

### Backups are readable by every user on the machine
- Severity (proposed): Important
- Bug class: file permissions
- Locations: src/backup.sh:7, src/backup.sh:9
- Claim: \`mkdir -p\` and \`cp\` create the backup folder and each copy with the default umask, so on a shared machine every user can read the household's list.
- Failure scenario: with umask 022, \`backup.sh list.txt /srv/backups\` leaves \`/srv/backups/list-<stamp>.txt\` mode 644; another account on the machine reads what the household buys.
- Evidence: \`mkdir -p \"\$dir\"\` (src/backup.sh:7), \`cp -- \$list \"\$dir/list-\$stamp.txt\"\` (src/backup.sh:9); no \`umask\` or \`chmod\` in the script.

#### R3-3 (standards Finder; Verifier: keep, Pre-existing)

### add.sh writes an unquoted item to an unquoted path
- Severity (proposed): Pre-existing
- Bug class: unquoted path
- Locations: src/add.sh:5
- Claim: \`echo \$item >> \$list\` expands the item as a glob and splits a list path holding a space. \`add.sh\` is unchanged by this pull request.
- Failure scenario: \`add.sh list.txt '*'\` adds the names of the files in the current folder instead of \`*\`; \`add.sh \"my list.txt\" milk\` fails with an ambiguous redirect.
- Evidence: \`echo \$item >> \$list\` (src/add.sh:5)."
  heads="Round 3 reviews the commits since Round 2's head (\`git diff $c2..$branch\`); this run's head is branch \`$branch\` ($c3)."
else
  issue=".scratch/issues/30-count.md"; pr=2; branch=count
  cat > "$r/$issue" <<MD
Title: Count the list's items
Type: ticket
Labels: $labels
Status: open

## What to build

\`src/count.sh <list-file>\` prints how many items the list holds, for the shopping reminder; lines starting with \`#\` and blank lines are not items. With a test.

## Acceptance criteria

- **AC1**: It prints the number of items.
- **AC2**: An empty list prints 0.
MD
  # The first attempt's branch: its head is named by the attempt record (case inside).
  git -C "$r" switch -q -c count-1
  cat > "$r/src/count.sh" <<'SH'
#!/usr/bin/env bash
# usage: count.sh <list-file>   prints how many items the list holds
set -eu
wc -l < "${1:?usage: count.sh <list-file>}"
SH
  a1="$(commit "Count the list's items ($issue)")"
  git -C "$r" switch -q main
  git -C "$r" switch -q -c "$branch"
  cat > "$r/src/count.sh" <<'SH'
#!/usr/bin/env bash
# usage: count.sh <list-file>   prints how many items the list holds
set -eu
list="${1:?usage: count.sh <list-file>}"
[ -f "$list" ] || { echo 0; exit 0; }
grep -cv '^\(#\|$\)' "$list" || true
SH
  cat > "$r/tests/count.sh" <<'SH'
#!/usr/bin/env bash
set -e
f="$(mktemp)"; printf '# groceries\nmilk\n\nbread\n' > "$f"
[ "$(bash src/count.sh "$f")" = 2 ]
: > "$f"; [ "$(bash src/count.sh "$f")" = 0 ]
rm -f "$f"
SH
  c0="$(commit "Count the list's items, second attempt ($issue)")"
  sed -i '5s/.*/[ -f "$list" ] || { echo "count: no list file: $list" >\&2; exit 1; }/' "$r/src/count.sh"
  cat >> "$r/tests/count.sh" <<'SH'
if bash src/count.sh /nonexistent/list.txt 2>/dev/null; then exit 1; fi
SH
  c1="$(commit "Fail on a missing list file (R1-1)")"
  s1="${c1:0:7}"
  cat > "$r/.scratch/pulls/1.md" <<MD
Title: Count the list's items
Base: main
Head: count-1
State: closed

The first attempt at \`$issue\`, closed when its review ended.
MD
  cat > "$r/.scratch/pulls/2.md" <<MD
Title: Count the list's items
Base: main
Head: count
State: open

Adds \`src/count.sh\` and its test. Builds \`$issue\`, second attempt.
MD
  if [ "$case_" = inside ]; then
    cat >> "$r/$issue" <<MD

## Comments

### Comment 1

<!-- code-review kind=attempt attempt=1 pr=1 head=$a1 -->
## Review attempt 1: restart

Pull request: \`.scratch/pulls/1.md\`
Rounds: 1 to 3 (Standard)
Ended by: a Finding returned
Outcome: restart
Earlier attempts: none

| id | Severity | Bug class | Locations | How | Claim |
|----|----------|-----------|-----------|-----|-------|
| R3-1 | Important | comment lines counted | src/count.sh:4 | returned R1-1 | lines starting with \`#\` and blank lines are counted as items |

Tried: R1-1 was fixed by filtering with \`grep -v '^#'\` piped to \`wc -l\`; the Round 2 fix for blank lines went back to \`wc -l\` alone and dropped the comment filter.
Lesson: each fix rewrote the whole counting line and lost the other filter. Count with one expression that drops both kinds of line, and test a list holding both.
Untouched: none
MD
  fi
  mkdir -p "$r/.scratch/pulls/2"
  cat > "$r/.scratch/pulls/2/01-round-1.md" <<MD
<!-- code-review kind=round round=1 depth=Standard head=$c0 base=$base -->
## Code review: Round 1 of at most 5 (Standard)

Reviewed: the whole pull request
Result: not clean, 1 Important open
Finders: standards, spec, adversarial (bugs and edge cases), adversarial (security and privacy)

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
| R1-1 | Important | missing file read as empty | src/count.sh:5 | open | spec Finder: a mistyped list path prints 0 and exits 0, so the reminder says nothing is left to buy instead of failing |
MD
  round=2
  findings="#### R1-1 (earlier open Important; Verifier: fixed in $s1, \`exit 1\` at src/count.sh:5)

Re-checked against the current code: a missing list file now prints \"count: no list file\" to standard error and exits 1.

#### R2-1 (adversarial Finder, bugs and edge cases; Verifier: keep, caused by this change, Important)

### A first run fails before any item is added
- Severity (proposed): Important
- Bug class: first-run failure
- Locations: src/count.sh:5
- Claim: the list file is only created when the first item is added (README.md:3), so before that \`count.sh\` exits 1 with \"no list file\"; a household that has added nothing has an empty list, which AC2 says prints 0. When the file is missing, print 0 and exit 0.
- Failure scenario: a new household runs the reminder before adding anything; \`count.sh list.txt\` exits 1 and the reminder aborts instead of saying 0 items.
- Evidence: \`[ -f \"\$list\" ] || { echo \"count: no list file: \$list\" >&2; exit 1; }\` (src/count.sh:5); README.md:3: \"The list file is created when the first item is added\"; AC2: \"An empty list prints 0.\"

#### R2-2 (adversarial Finder, security and privacy; Verifier: keep, caused by this change, Important)

### An unreadable list file prints nothing and succeeds
- Severity (proposed): Important
- Bug class: hidden read error
- Locations: src/count.sh:5, src/count.sh:6
- Claim: \`[ -f ]\` passes for a list file the user cannot read; \`grep\` then fails with status 2 and \`|| true\` hides it, so \`count.sh\` prints nothing and exits 0. Check that the file is readable, and let a \`grep\` error fail the script.
- Failure scenario: the list file is mode 000; \`count.sh list.txt\` prints an empty line and exits 0, and the reminder shows a blank count as success.
- Evidence: \`[ -f \"\$list\" ]\` (src/count.sh:5); \`grep -cv '^\\(#\\|\$\\)' \"\$list\" || true\` (src/count.sh:6)."
  heads="Round 2 reviews the whole pull request (\`git diff main...$branch\`); this run's head is branch \`$branch\` ($c1)."
fi
git -C "$r" switch -q main

if [ "$case_" = inside ]; then
  if [ "$fx" = returned ]; then
    expect="Inside a Milestone (the issue carries \`milestone-1\`). The convergence check counts R3-1 as returned: R1-1 was fixed (Round 2), its location src/backup.sh:8 at Round 2's head is line 9 at this head, and R3-1 makes the same claim there under another Bug class name. R3-2 shares the lines but not the claim, and R3-3 is Pre-existing in another file: neither counts. The Round 3 comment's Result is the attempt-ended form with restart and the cause a returned Finding; R2-1 and R2-2 are fixed in $s3; R3-1, R3-2 and R3-3 are open. Nothing more is fixed and no Round 4 follows. An attempt record (attempt 1, pull request 1, Rounds 1 to 3, R3-1 returned from R1-1, R3-2 open, what was tried, the lesson that the R2-1 fix rewrote the cp line and lost R1-1's quoting, untouched: README.md and tests/backup.sh) is added to $issue with the Comment on an issue operation. R3-3 is filed as an issue with a filing receipt. The report says restart, with the record's link."
  else
    expect="Inside a Milestone (the issue carries \`milestone-1\`). The convergence check counts R2-1 as a flip: R1-1 is confirmed fixed by $s1, and R2-1's fix (print 0 and exit 0 for a missing file) would put back what that fix took out, at the same line. R2-2 shares the line but keeps the exit 1: it does not count. The issue already holds attempt 1's record, so the outcome is park. The Round 2 comment's Result is the attempt-ended form with park and the cause a fix that flipped back; R1-1 is fixed in $s1; R2-1 and R2-2 are open. Nothing more is fixed and no Round 3 follows. An attempt record (attempt 2, pull request 2, Rounds 1 to 2, R2-1 flipped from R1-1, R2-2 open, the earlier attempt's link, what was tried, a lesson naming the missing-versus-empty file question, untouched: tests/count.sh) is added to $issue as Comment 2. The report says park, with the record's link."
  fi
else
  expect="Outside a Milestone (the issue carries no label in the Boundary record's form). No convergence check, no attempt record, nothing written to $issue. The Round $round comment's Result is \`not clean, 2 Important open\`; the Importants go to the owner to fix and Round $((round + 1)) follows. No outcome (restart or park) is reported."
fi

cat > "$out/PROMPT.md" <<MD
# Scripted prompt: agentic-review convergence check, fixture $fx, case $case_

Give the text between the lines to a fresh top-level session, working directory \`$r\`, with \`<checkout>\` replaced by the path of the checkout under test.

---

You run the \`agentic-review\` skill from \`<checkout>/plugins/dev-skills/skills/agentic-review/SKILL.md\` (the checkout under test, not an installed copy), with the skills it names loaded from the same \`skills/\` folder, on pull request \`.scratch/pulls/$pr.md\` in this repo, which builds \`$issue\`. The tracker is the local Markdown one in \`docs/agents/issue-tracker.md\`; there is no forge and no CI. The earlier Rounds are recorded under \`.scratch/pulls/$pr/\`. $heads Round $round's Find and Verify have run at Standard depth: Verify's results are below. Carry on from Rank: write the Round $round comment as \`.scratch/pulls/$pr/0$round-round-$round.md\` and do every step the skill gives after it, through the end of this Round. The owner of the code commits nothing in this run: when the skill has the owner fix or commit, say what it would do and stop there, without starting another Round. Start no subagents. The user answers no question: when you would put a question to the user, write it word for word and stop. End with your report to the caller.

$findings

---

Expected: $expect

Score with \`evals/agentic-review/convergence/EXPECTED.md\` and record the run in \`evals/agentic-review/RESULTS.md\`, saying how it was driven.
MD
echo "$out"
