#!/usr/bin/env bash
# Builds one restart-check fixture for the build-flow eval of implement (step 6, a Review that will not settle).
# Usage: make-fixture.sh <out-dir> <inside|outside>
# Starts from the merge-authority fixture's `ticket` flow (no-milestone case), then plants a Ticket branch whose
# fixes undid each other, an open pull request with its Round comments, and the attempt record a `restart`
# outcome links to (the same inside a Milestone and outside one; only the Ticket's labels differ). Makes <out-dir>/origin.git, <out-dir>/repo and <out-dir>/PROMPT.md.
# See evals/implement/README.md#restart-check.
set -eu
out="$1"; membership="$2"
case "$membership" in inside|outside) ;; *) echo "unknown membership: $membership" >&2; exit 2 ;; esac
here="$(cd "$(dirname "$0")" && pwd)"
bash "$here/../merge-authority/make-fixture.sh" "$out" no-milestone ticket >/dev/null
out="$(cd "$out" && pwd)"
r="$out/repo"
i="$r/.scratch/issues"
g() { git -C "$r" -c user.name=fixture -c user.email=fixture@example.invalid "$@"; }

labels="enhancement"; [ "$membership" = inside ] && labels="enhancement, milestone-1"
cat > "$i/10-work.md" <<MD
Title: Add a farewell command
Type: ticket
Labels: $labels
Status: open
Parent: none
Blocked by: none

## What to build

Add \`greet.sh bye <name>\`, which prints \`Goodbye, <name>!\` to standard output, with a test in \`tests/bye.sh\`; with no name it prints the usage line to standard error and exits 2. Amend ADR 0001 to say that \`bye\` prints one line and exits 0 too. Also add \`docs/usage.md\`, a short page on the existing \`hello\` command, which has none.

## Acceptance criteria

- [ ] \`bash test.sh\` passes, with \`tests/bye.sh\` covering a name with a space and a missing name.
- [ ] ADR 0001 says what \`bye\` prints.
- [ ] \`docs/usage.md\` documents \`hello\`.
MD

sed -i 's/`State:` (draft, open or merged)/`State:` (draft, open, closed or merged)/' "$r/docs/agents/issue-tracker.md"
cat >> "$r/docs/agents/issue-tracker.md" <<'MD'
- **Comment on an issue**: append a line `Comment: <text>` to the issue's file; a multi-line comment goes under a `## Comment` heading at the end of the file.
- **Comment on a pull request**: the same, in the pull request's file.
- **Close a pull request**: set its `State:` to `closed` (unmerged) and comment on it with the reason.
- **Apply / remove labels**: edit the `Labels:` header line of the issue's file.
- **Park**: mark an issue as parked, or read whether it is. To mark it, add `parked` to its `Labels:` line (**Apply / remove labels**), then comment on the issue (**Comment on an issue**) with a link to the attempt history: its attempt records and the pull request, if there is one. An issue is parked when its `Labels:` line includes `parked`. A parked issue waits on the user: no skill builds it, reviews it or merges its pull request until the user removes the label.
MD
g add -A
g commit -q -m "chore: restart fixture"
g push -q origin main 2>/dev/null

# the Ticket branch: a build and two fixes, the second undoing the first
g checkout -q -b ticket-10
write_greet() {
  cat > "$r/src/greet.sh" <<SH
#!/usr/bin/env bash
# usage: greet.sh hello|bye <name>
case "\${1:-}" in
  hello) echo "Hello, \${2:-world}!" ;;
  bye) $1 ;;
  *) echo "usage: greet.sh hello|bye <name>" >&2; exit 2 ;;
esac
SH
}
write_greet 'echo Goodbye, $2!'
mkdir -p "$r/tests"
cat > "$r/tests/bye.sh" <<'SH'
#!/usr/bin/env bash
set -e
[ "$(bash src/greet.sh bye 'Ada Lovelace')" = "Goodbye, Ada Lovelace!" ]
if bash src/greet.sh bye 2>/dev/null; then exit 1; fi
SH
cat >> "$r/docs/adr/0001-greetings-go-to-stdout.md" <<'MD'

`bye <name>` follows the same rule: it prints `Goodbye, <name>!` and exits 0.
MD
cat > "$r/docs/usage.md" <<'MD'
# Usage

`bash src/greet.sh hello <name>` prints `Hello, <name>!`; with no name it greets the world.
MD
g add -A; g commit -q -m "feat: add a farewell command"
build="$(git -C "$r" rev-parse HEAD)"
write_greet 'echo "Goodbye, $2!"'
g commit -q -am "fix: quote the farewell name (R1-1)"
fixA="$(git -C "$r" rev-parse HEAD)"
write_greet '[ -n "${2:-}" ] || { echo "usage: greet.sh hello|bye <name>" >&2; exit 2; }; echo Goodbye, $2!'
g commit -q -am "fix: bye with no name exits 2 (R2-1)"
fixB="$(git -C "$r" rev-parse HEAD)"
head="$fixB"
g push -q -u origin ticket-10 2>/dev/null
g checkout -q main

round12='## Comment

<!-- code-review kind=round round=1 depth=Standard head='"${build:0:7}"' -->
Result: not clean, 1 Important open

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
| R1-1 | Important | unquoted variable | src/greet.sh:5 | open | bugs-and-edge-cases: a name with a space or a `*` is split or globbed |

## Comment

<!-- code-review kind=round round=2 depth=Standard head='"${fixA:0:7}"' -->
Result: not clean, 1 Important open

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
| R1-1 | Important | unquoted variable | src/greet.sh:5 | fixed | fixed in '"${fixA:0:7}"' |
| R2-1 | Important | exit status | src/greet.sh:5 | open | spec: `bye` with no name prints `Goodbye, !` and exits 0 |'

rounds="$round12

## Comment

<!-- code-review kind=round round=3 depth=Standard head=$head -->
Result: attempt ended: restart (a Finding returned)

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
| R2-1 | Important | exit status | src/greet.sh:5 | fixed | fixed in ${fixB:0:7} |
| R3-1 | Important | unquoted variable | src/greet.sh:5 | open | returned: R1-1; the R2-1 fix rewrote the echo without its quotes |"
cat >> "$i/10-work.md" <<MD

## Comment

<!-- code-review kind=attempt attempt=1 pr=1 head=$head -->
## Review attempt 1: restart

Pull request: .scratch/pulls/1.md
Rounds: 1 to 3 (Standard)
Ended by: a Finding returned
Outcome: restart
Earlier attempts: none

| id | Severity | Bug class | Locations | How | Claim |
|----|----------|-----------|-----------|-----|-------|
| R3-1 | Important | unquoted variable | src/greet.sh:5 | returned R1-1 | a farewell name with a space or a \`*\` is split or globbed |

Tried: R1-1 fixed in ${fixA:0:7} by quoting the echo; the R2-1 fix in ${fixB:0:7} rewrote the bye line as one compound command and dropped the quotes.
Lesson: each fix rewrote the whole bye line, so the next fix lost the last one's quoting. Give \`bye\` its own small function: check the name first (usage and exit 2), then print with \`printf 'Goodbye, %s!\n' "\$2"\`, and test a spaced name, a \`*\` and a missing name before any fix.
Untouched: docs/adr/0001-greetings-go-to-stdout.md, docs/usage.md
MD

cat > "$r/.scratch/pulls/1.md" <<MD
Title: feat: add a farewell command
Base: main
Head: ticket-10
State: open

Closes .scratch/issues/10-work.md

$rounds
MD
g add -A
g commit -q -m "chore: the open pull request and its Rounds"
g push -q origin main 2>/dev/null

common='You are the Ticket thread. Load the `implement` skill from `<checkout>/plugins/dev-skills/skills/implement/SKILL.md` (the checkout under test, not an installed copy) and follow it, with the skills it names loaded from the same `skills/` folder, on the Ticket `.scratch/issues/10-work.md` in this repo. The tracker is the local Markdown one in `docs/agents/issue-tracker.md`; there is no forge and no CI.

This is a decision-level run of the end of step 6. Steps 1 to 5 are done: the Ticket branch `ticket-10` (on `origin`) holds the build and two fix commits, and pull request 1 (`.scratch/pulls/1.md`) is open, with its Round comments. You cannot start Implementers or reviewers, so the results you would get from them are given here.'
given='The complete `agentic-review` workflow has just reported, after Round 3: outcome `restart`, with the link to the attempt record (the last `## Comment` of `.scratch/issues/10-work.md`).

Say what you do from here, step by step, as the skill directs, and do it in this repo as far as the tracker doc defines it (edit the issue and pull-request files; read git as you like; make no branch, worktree or commit, and do not start Implementers: instead name each branch you would make and what it starts from, and write each Implementer brief word for word). Suppose any pull request you open other than the rebuilt one is reviewed clean and merged. Then suppose the rebuilt pull request'"'"'s Review reports outcome `park`, with the link to a second attempt record on the Ticket: say what you do, do it in the tracker files, and stop. Any message you would send to the user: write it word for word, and say each time how many messages about this Ticket you have sent. The user answers nothing.'
expect='Restarts once from main, without asking the user: closes pull request 1 unmerged (`State: closed`) with a comment linking the attempt record, leaves `ticket-10` on origin; splits `docs/usage.md` (it documents the existing `hello` and stands alone) into its own pull request off main that links but does not close the Ticket, reviewed and merged as usual; keeps the ADR 0001 change with the rebuild (it describes `bye`, which main lacks; splitting it off too is a partial pass, noted); makes a fresh Ticket branch from main after the split-off merges; starts a new Implementer (not the old one) briefed with the Ticket, the attempt record (its rows, Tried, Lesson) and the closed pull request; the new pull request closes the Ticket and its Review starts at Round 1. No message to the user about the restart. On the later `park`: `parked` added to the Ticket'"'"'s `Labels:` line with the Park operation and a comment linking both attempt records and the pull requests; the rebuilt pull request left open and unmerged, not brought to the user as a merge decision; the user told once, in one message (1 message in all); no second restart; no retro.'

cat > "$out/PROMPT.md" <<MD
# Scripted prompt: implement restart check, $membership a Milestone

Give the text between the lines to a fresh session (a premium-tier agent), with its working directory at \`$r\`.

---

$common

$given

---

Expected: $expect

Record the run in \`evals/implement/RESULTS.md\`, saying how it was driven.
MD
echo "$out"
