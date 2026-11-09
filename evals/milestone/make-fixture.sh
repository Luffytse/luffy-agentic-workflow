#!/usr/bin/env bash
# Builds one fixture for the milestone skill's dry run of its planning phase (plan, plan-small, plan-setaside,
# add-feature, add-feature-excluded). The delivery cases moved to evals/team-lead/ with the team-lead skill.
# Usage: make-fixture.sh <out-dir> <plan|plan-small|plan-setaside|add-feature|add-feature-excluded>
# Makes <out-dir>/repo (a git repo, one commit on main, with a dry-run local tracker) and <out-dir>/PROMPT.md
# (the scripted prompt for a fresh coordinator session). See evals/milestone/README.md.
set -eu
out="$1"; case_="$2"
case "$case_" in plan|plan-small|plan-setaside|add-feature|add-feature-excluded) ;; *) echo "unknown case: $case_" >&2; exit 2 ;; esac
[ -e "$out" ] && { echo "$out exists" >&2; exit 2; }
mkdir -p "$out"
out="$(cd "$out" && pwd)"
r="$out/repo"
mkdir -p "$r/docs/dev-skills" "$r/src" "$r/.scratch/issues"
git init -q -b main "$r"

cat > "$r/CLAUDE.md" <<'MD'
# greeter

A tiny shell greeter. Run `bash test.sh` before each push.

## Agent skills

Start at `docs/dev-skills/index.md`.

### Issue tracker

Local Markdown issues under `.scratch/issues/`, in dry-run mode. See `docs/dev-skills/issue-tracker.md`.

### Boundaries

See `docs/dev-skills/boundaries.md`.

### Releases

The version lives in `VERSION`. See `docs/dev-skills/release.md` for who bumps it.
MD


cat > "$r/docs/dev-skills/index.md" <<'MD'
# Docs index

- [docs/dev-skills/issue-tracker.md](issue-tracker.md): the local Markdown tracker, in dry-run mode, and its operations. Read before any tracker operation.
- [docs/dev-skills/boundaries.md](boundaries.md): the Boundary record. Read when deciding whether an action needs the user, or when giving an issue a Milestone label.
- [docs/dev-skills/release.md](release.md): the release doc (its bump mode says who bumps `VERSION`). Read when planning or cutting a Release, or before a merge that may bump the version.
MD

cat > "$r/docs/dev-skills/issue-tracker.md" <<'MD'
# Issue tracker: local Markdown, dry run

Issues are files under `.scratch/issues/`, one per issue, named `NN-slug.md`. Each starts with header lines:
`Title:`, `Type:` (milestone, spec or ticket), `Labels:` (comma-separated), `Status:` (open or closed),
`Parent:` (an issue file, or none) and `Blocked by:` (issue files, or none). Comments follow a `## Comments` heading.
The labels that exist are listed in `.scratch/labels.md`, one per line.

**Dry run.** This tracker is in dry-run mode: read operations read the files, and **no write operation changes any
file under `.scratch/issues/` or `.scratch/labels.md`**. Instead, each write is appended to
`.scratch/proposed-actions.md` as one block, numbered in the order you would take it:

    ### <k>. <Operation name>
    Issue: <issue file, or "new">
    <the operation's fields, as listed below>

Starting a thread or a subagent is a write too: record it as `### <k>. Start a thread` with a `Skill:` line, then
`Brief:` followed by the whole brief between `~~~` lines. A message to a thread you started is one too: `### <k>. Message a
thread` with a `Thread:` line (the issue file the thread works on) and `Body:` followed by the message between `~~~` lines.
In delivery, a message to the user is one too: `### <k>. Message the user` with `Body:` followed by the message between
`~~~` lines.

Times: a comment in an issue's file, a commit and a pull request comment carry their UTC time. Each event gives the clock;
a block you append counts as written at that clock time (read your earlier blocks in `.scratch/proposed-actions.md` as the
tracker's record of your own writes).

When the prompt gives you **events**, append a line `## Event <k>` to `.scratch/proposed-actions.md` before the blocks of
event `<k>` (also when it leads to no write), and keep numbering the blocks on from the event before.

- **Read an issue**: read its file.
- **List issues**: read every file under `.scratch/issues/`.
- **Create an issue**: fields `Title:`, `Labels:`, `Parent:`, then `Body:` followed by the whole body between `~~~` lines. The new issue's file name is the next free `NN-slug.md`; give it in the `Issue:` line as `new (NN-slug.md)`.
- **Edit an issue body**: fields `Body:` followed by the WHOLE new body between `~~~` lines (never only the changed part).
- **Create a label**: field `Label:`.
- **Apply / remove labels**: fields `Add:` and `Remove:` (comma-separated, or none).
- **Make an issue a sub-issue of a parent**: field `Parent:` (the parent's issue file). An issue has at most one parent.
- **Comment on an issue**: field `Body:` followed by the comment between `~~~` lines.
- **Close**: field `Outcome:` (completed or not planned) and a one-line `Reason:`.
- **Read a PR**: read `.scratch/pulls/<n>.md`: its state, whether it is ready for review since when, its changed files,
  its checks and its comments, each with its time.
- **List PRs**: read every file under `.scratch/pulls/`; each starts with a `Builds:` line naming the issue file it
  builds (or `none`), then the fields **Read a PR** lists.
- **Count open blockers**: read the issue's `Blocked by:` header and the `Status:` of each issue it names. A blocker whose
  status is `closed` is cleared, unless its file has a `Closed as: not planned` line. The issue is startable when no
  named blocker is open or uncleared.
- **Park**: mark an issue parked, or read whether it is. To mark it, add the `parked` label (**Apply / remove labels**),
  then comment on the issue (**Comment on an issue**) saying why, with a link to the records of what parked it. An issue is parked when its
  `Labels:` include `parked`; the user lifts the park by removing the label. Your own label writes land only in
  `.scratch/proposed-actions.md`, so a label the user removes shows as a comment `User removed label parked at <time>.`
  on the issue, which undoes your own earlier `Add: parked` for that issue. A label a thread adds shows as a comment `Label parked added by <thread> at <time>.`, next to the
  comment that links the records of what parked it; a thread's own label write reaches the tracker, yours does not.
MD

cat > "$r/docs/dev-skills/boundaries.md" <<'MD'
# Boundary record

What the user has agreed agents may do on their own in this repo, which actions are the user's to decide, and the limits agents work within.

- **Irreversible actions agents may take**: delete test data that agents generate while implementing.
- **Actions that need the user's approval**: sending any message to customers.
- **Budget**: none.
- **Check-in interval**: 1 hour.
- **Milestone label form**: `milestone-<n>` (for example `milestone-1`). An issue belongs to a Milestone when it carries that Milestone's label, and the Milestone issue carries the same label.
MD

cat > "$r/docs/dev-skills/release.md" <<'MD'
# Releases

- **Bump mode**: Releases bump. A Release opens one bump pull request that changes `VERSION` and adds its changelog entry.
- **Version file**: `VERSION`, its only line.
- **Changelog**: `CHANGELOG.md`, newest entry first.
- **Label prefix**: `release-`, as `release-X.Y.Z`.
MD

printf '0.3.0\n' > "$r/VERSION"
printf '# Changelog\n' > "$r/CHANGELOG.md"
cat > "$r/src/greet.sh" <<'SH'
#!/usr/bin/env bash
# usage: greet.sh hello <name>
case "${1:-}" in
  hello) echo "Hello, ${2:-world}!" ;;
  *) echo "usage: greet.sh hello <name>" >&2; exit 2 ;;
esac
SH
cat > "$r/test.sh" <<'SH'
#!/usr/bin/env bash
set -e
[ "$(bash src/greet.sh hello Ada)" = "Hello, Ada!" ]
echo "OK"
SH

# The two planned features: a Spec with its two Tickets, and a lone Ticket.
cat > "$r/.scratch/issues/10-farewell.md" <<'MD'
Title: Add a farewell command
Type: spec
Labels: enhancement
Status: open
Parent: none
Blocked by: none

## What to build

`greet.sh bye <name>` prints `Goodbye, <name>!` to standard output and exits 0.

## Acceptance criteria

- [ ] `greet.sh bye Ada` prints `Goodbye, Ada!` and exits 0.
- [ ] `greet.sh bye` with no name prints `Goodbye, world!`.
- [ ] `bash test.sh` covers both.

## Tickets

- `.scratch/issues/11-bye-code.md`: the command and its test.
- `.scratch/issues/12-bye-usage.md`: the usage line.
MD
cat > "$r/.scratch/issues/11-bye-code.md" <<'MD'
Title: Add a farewell command: code and test
Type: ticket
Labels: enhancement
Status: open
Parent: .scratch/issues/10-farewell.md
Blocked by: none

The `bye` command and its test. Model tier: regular.
MD
cat > "$r/.scratch/issues/12-bye-usage.md" <<'MD'
Title: Add a farewell command: usage line
Type: ticket
Labels: enhancement
Status: open
Parent: .scratch/issues/10-farewell.md
Blocked by: .scratch/issues/11-bye-code.md

The usage line names `bye`. Model tier: cheap.

## Acceptance criteria

- [ ] `greet.sh` with no command prints exactly `usage: greet.sh hello|bye <name>` to standard error and exits 2.
- [ ] `bash test.sh` checks that exact line.
MD
cat > "$r/.scratch/issues/20-quiet.md" <<'MD'
Title: Add a --quiet flag
Type: ticket
Labels: enhancement
Status: open
Parent: none
Blocked by: none

## What to build

`--quiet` before any command prints nothing and keeps the exit code, for use in scripts.

## Acceptance criteria

- [ ] `greet.sh --quiet hello Ada` prints nothing and exits 0.
- [ ] `greet.sh --quiet nope` prints nothing and exits 2.
MD
# A raw request nobody has planned: an agent may propose it, never add it.
cat > "$r/.scratch/issues/30-colour.md" <<'MD'
Title: Colour output would be nice
Type: ticket
Labels: needs-triage
Status: open
Parent: none
Blocked by: none

Someone asked for coloured greetings. Not looked at yet.
MD
# Work set aside for a later Milestone (plan-setaside): nobody has planned it for this one.
if [ "$case_" = plan-setaside ]; then
  cat > "$r/.scratch/issues/31-translations.md" <<'MD'
Title: Translations (next Milestone)
Type: ticket
Labels: enhancement
Status: open
Parent: none
Blocked by: none

Greetings in French and Spanish. Set aside by the user for a later Milestone.
MD
fi
printf 'enhancement\nneeds-triage\nbug\n' > "$r/.scratch/labels.md"

# The open Milestone 1 (add-feature cases), with its Startup verification passed. $1 is the order rule;
# $2, if given, is one more feature row. $excluded is the Excluded list.
excluded='- Translations.'
[ "$case_" = add-feature-excluded ] && excluded='- Colour output (`30-colour.md`).
- Translations.'
write_milestone() {
  cat > "$r/.scratch/issues/00-milestone.md" <<MD
Title: Milestone 1: goodbye and quiet
Type: milestone
Labels: milestone-1
Status: open
Parent: none
Blocked by: none

## Goal

By the end, the greeter can say goodbye and can run silently in scripts, so it can ship as 1.0.

## Features, in build order

$1 Each feature is its own issue carrying \`milestone-1\`.

| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | \`10-farewell.md\` Add a farewell command | Spec | \`greet.sh bye Ada\` prints \`Goodbye, Ada!\`; no name greets the world; tests cover both |
| 2 | \`20-quiet.md\` Add a --quiet flag | lone Ticket | \`--quiet\` prints nothing and keeps the exit code |
${2:-}

## Acceptance

- Every feature above is merged and its issue closed.
- The user runs \`greet.sh --quiet bye Ada\` at the Milestone review and sees nothing, exit 0.

## Excluded

$excluded

## Comments

<!-- startup-verification result -->
## Startup verification

Harness: claude.ai project, workers are threads (claude-code-project-threads) · Role: coordinator · Runner: coordinator and thread verify-1 · Run: 2026-11-02 09:00–09:20 UTC
Runtime: cloud container; permission mode: acceptEdits; sandbox: unknown; tools held: coordinator starts and reads threads, threads hold scheduling and stop

| Capability | Essential | Method and source | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Start a worker | yes | start a thread; project doc | pass | id listed by the Harness | none |
| Worker state | yes | read the thread's state | pass | running read under that id | none |
| Pause and resume | not relied on | not probed | not probed | none | the Harness's own pause is the user's |
| Confirmed stop | yes | a thread stops it; state read back by the coordinator | pass | running before, stopped after | an archive can be undone |
| End or failure notice | yes | a thread replies and ends | pass | wake and ended state read | failure not provoked |
| Scheduled check-in | yes | a thread arranges it into the coordinator | pass | two arrivals in the coordinator's record; ended | none |
| Loaded skill version | yes | the verification thread | pass | versions equal | none |

Verdict: ready
MD
}

if [ "$case_" = add-feature ] || [ "$case_" = add-feature-excluded ]; then
  printf 'milestone-1\nrelease-0.4.0\n' >> "$r/.scratch/labels.md"
  for f in 10-farewell 11-bye-code 12-bye-usage 20-quiet; do
    sed -i.bak 's/^Labels: enhancement$/Labels: enhancement, milestone-1, release-0.4.0/' "$r/.scratch/issues/$f.md"
    rm -f "$r/.scratch/issues/$f.md.bak"
  done
  sed -i.bak 's/^Parent: none$/Parent: .scratch\/issues\/00-milestone.md/' "$r/.scratch/issues/10-farewell.md" "$r/.scratch/issues/20-quiet.md"
  rm -f "$r/.scratch/issues/"*.bak
  write_milestone "In this order, up to 2 at once."
  cat > "$r/.scratch/issues/40-release-0.4.0.md" <<'MD'
Title: Release 0.4.0
Type: ticket
Labels: release-0.4.0
Status: open
Parent: none
Blocked by: none

**Milestone:** 00-milestone.md

Goal: the farewell command and the quiet flag. Scope: 10-farewell.md, 20-quiet.md.
MD
fi



git -C "$r" add -A
git -C "$r" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "fixture: greeter ($case_)"

# The scripted prompt. The runner gets only the text between the --- lines.
{
  echo "# Prompt for case $case_"
  echo
  echo "Give a fresh session only the text between the lines, with <checkout> replaced by the checkout under test."
  echo
  echo "---"
  cat <<'TXT'
You are the coordinator of the project in this working directory. Load the `milestone` skill from
<checkout>/plugins/dev-skills/skills/milestone/SKILL.md (that copy, not an installed one) and follow it. Load any other
skill it names from the same checkout's `plugins/dev-skills/skills/`.

This is a dry run. The tracker doc, `docs/dev-skills/issue-tracker.md`, says how every write is recorded in
`.scratch/proposed-actions.md` instead of being made: follow it for every tracker write and every thread you would
start. Change no other file. The user is scripted: append every question you ask the user to `.scratch/questions.md`,
one `- ` line each, then take the answer from "The user's answers" below; when a question is not covered there, add
` (unanswered)` to its line, treat it as unanswered, and do not guess an answer. Today is 2026-11-02.

When you stop, write `.scratch/report.md` (if you cannot write that file, return the same text as your final message): the last message you would send the user, and what the skill says comes
next and what it waits for.
TXT
  if [ "$case_" = plan ]; then
    cat <<'TXT'

The user's message: "Let's start a Milestone. I want the greeter to say goodbye and to stay quiet in scripts."

The user's answers:
- Goal: "By the end, the greeter can say goodbye and can run silently in scripts, so it can ship as 1.0."
- Features: "Two: the farewell command (issue 10, a Spec, already split into Tickets 11 and 12) and the quiet flag
  (issue 20, a lone Ticket). I planned both already; their acceptance criteria are in the issues."
- Any feature an agent proposes: "No, not in this Milestone."
- Order: "Farewell first, then quiet. Two at once is fine."
- Milestone acceptance: "Both merged and closed, and at the review I run `greet.sh --quiet bye Ada` and see nothing."
- Excluded: "Colour output (issue 30) and translations."
- The draft Milestone issue: "Yes, that's it. Write it."
- Startup verification: "It has not run in this environment yet."

Stop when the skill would hand over to its next phase.
TXT
  elif [ "$case_" = plan-small ] || [ "$case_" = plan-setaside ]; then
    cat <<'TXT'

The user's message: "Let's plan a small Release: just the quiet flag (issue 20). I planned it already; its acceptance
criteria are in the issue."

The user's answers:
- Goal: "Scripts can run the greeter silently."
- Any feature an agent proposes: "No."
TXT
    [ "$case_" = plan-setaside ] && cat <<'TXT'
- Any question about other open issues joining this Milestone: "None of them join this one."
TXT
    cat <<'TXT'
- The draft Milestone issue: "Yes, that's it. Write it."
- Startup verification: "It has not run in this environment yet."

Stop when the skill would hand over to its next phase.
TXT
  else
    cat <<'TXT'

The user's message, in a planning thread: "I want colour output (issue 30). Let's plan it."

The user's answers:
- When asked to plan issue 30: "Colour the name in `hello` green only when standard output is a terminal;
  `--no-color` turns it off, and the usage line becomes exactly `usage: greet.sh [--no-color] hello|bye <name>`.
  Accepted when a test covers
  the terminal case and `--no-color`. It is one lone Ticket."
- Its place in the order: "Third, after the quiet flag."
- Whether it joins the open Release 0.4.0: "Leave that to the rules."
TXT
    [ "$case_" = add-feature-excluded ] && cat <<'TXT'
- Whether colour output can come out of Milestone 1's exclusions: "Yes, take it out of Excluded."
TXT
    cat <<'TXT'

Stop when the feature is added, or when the skill says it must wait.
TXT
  fi
  echo "---"
} > "$out/PROMPT.md"

echo "built $case_ fixture in $out"
