#!/usr/bin/env bash
# Builds one fixture for the milestone skill's dry run: its planning phase (plan, add-feature) or its delivery loop (deliver).
# Usage: make-fixture.sh <out-dir> <plan|add-feature|deliver|deliver-checkin-failed|deliver-stall>
# Makes <out-dir>/repo (a git repo, one commit on main, with a dry-run local tracker) and <out-dir>/PROMPT.md
# (the scripted prompt for a fresh coordinator session). See evals/milestone/README.md.
set -eu
out="$1"; case_="$2"
case "$case_" in plan|add-feature|deliver|deliver-checkin-failed|deliver-stall) ;; *) echo "unknown case: $case_" >&2; exit 2 ;; esac
# deliver-checkin-failed is the deliver fixture, cut to events 1 to 4, in which the check-in thread cannot arrange the check-ins.
# deliver-stall is the deliver fixture with its own world from event 3 on: threads that stall, a stop that does not
# take, a takeover, and a second stall.
kind="$case_"; case "$case_" in deliver-*) kind=deliver ;; esac
[ -e "$out" ] && { echo "$out exists" >&2; exit 2; }
mkdir -p "$out"
out="$(cd "$out" && pwd)"
r="$out/repo"
mkdir -p "$r/docs/agents" "$r/src" "$r/.scratch/issues"
git init -q -b main "$r"

cat > "$r/CLAUDE.md" <<'MD'
# greeter

A tiny shell greeter. Run `bash test.sh` before each push.

## Agent skills

Start at `docs/index.md`.

### Issue tracker

Local Markdown issues under `.scratch/issues/`, in dry-run mode. See `docs/agents/issue-tracker.md`.

### Boundaries

See `docs/agents/boundaries.md`.

### Releases

The version lives in `VERSION`. See `docs/agents/release.md` for who bumps it.
MD

cat > "$r/docs/index.md" <<'MD'
# Docs index

- [docs/agents/issue-tracker.md](agents/issue-tracker.md): the local Markdown tracker, in dry-run mode, and its operations. Read before any tracker operation.
- [docs/agents/boundaries.md](agents/boundaries.md): the Boundary record. Read when deciding whether an action needs the user, or when giving an issue a Milestone label.
- [docs/agents/release.md](agents/release.md): the release doc (its bump mode says who bumps `VERSION`). Read when planning or cutting a Release, or before a merge that may bump the version.
MD

cat > "$r/docs/agents/issue-tracker.md" <<'MD'
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
- **Read a branch**: read `.scratch/branches/<issue file name>`: the commits a thread has pushed for that issue, one
  per line with its UTC time. No such file means nothing has been pushed.
- **Read a PR**: read `.scratch/pulls/<n>.md`: its state, whether it is ready for review since when, its changed files,
  its checks and its comments, each with its time.
- **Count open blockers**: read the issue's `Blocked by:` header and the `Status:` of each issue it names. A blocker whose
  status is `closed` is cleared, unless its file has a `Closed as: not planned` line. The issue is startable when no
  named blocker is open or uncleared.
- **Park**: mark an issue parked, or read whether it is. To mark it, add the `parked` label (**Apply / remove labels**),
  then comment on the issue (**Comment on an issue**) with a link to the attempt history. An issue is parked when its
  `Labels:` include `parked`; the user lifts the park by removing the label.

## The environment's record of a thread

Not a tracker operation: this dry run's stand-in for the environment's own record of a thread's session (its
session-details call). **Read a thread's state**: read `.scratch/sessions/<issue file name>`: one line per thread that
has worked on that issue, by its start time, with its state now (`running`, `idle` or `archived`) and since when. No such
file means no thread on that issue has a session record yet.
MD

cat > "$r/docs/agents/boundaries.md" <<'MD'
# Boundary record

What the user has agreed agents may do on their own in this repo, which actions are the user's to decide, and the limits agents work within.

- **Irreversible actions agents may take**: delete test data that agents generate while implementing.
- **Actions that need the user's approval**: sending any message to customers.
- **Budget**: none.
- **Check-in interval**: 1 hour.
- **Milestone label form**: `milestone-<n>` (for example `milestone-1`). An issue belongs to a Milestone when it carries that Milestone's label, and the Milestone issue carries the same label.

## Milestone issues

A Milestone issue may name extra allowed or forbidden actions for its own issues. For an issue that belongs to the Milestone, the Milestone issue wins over this record; for every other issue, this record applies as written.
MD

if [ "$kind" = deliver ]; then
  cat > "$r/docs/agents/release.md" <<'MD'
# Releases

- **Bump mode**: pull requests bump. Every pull request that changes a file under `skills/` bumps `VERSION` as its last commit, with the number the coordinator hands out just before merge: minor for a new or changed skill rule, patch for a fix to one. Any other pull request leaves `VERSION` as it is. A Release opens no bump pull request; it writes the changelog entry for everything since the last Release.
- **Version file**: `VERSION`, its only line.
- **Changelog**: `CHANGELOG.md`, newest entry first.
- **Label prefix**: `release-`.
- **Release name**: `Milestone <m> · Release <n>`, with the label `release-m<m>-r<n>` on every issue in it and a release issue titled `Release Milestone <m> · Release <n>`.

## The bump commit

The merging thread changes `VERSION` to the number handed out, as the pull request's last commit.
MD
else
  cat > "$r/docs/agents/release.md" <<'MD'
# Releases

- **Bump mode**: Releases bump. A Release opens one bump pull request that changes `VERSION` and adds its changelog entry.
- **Version file**: `VERSION`, its only line.
- **Changelog**: `CHANGELOG.md`, newest entry first.
- **Label prefix**: `release-`, as `release-X.Y.Z`.
MD
fi

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
printf 'enhancement\nneeds-triage\nbug\n' > "$r/.scratch/labels.md"

# The open Milestone 1 (add-feature and deliver), with its Startup verification passed. $1 is the order rule;
# $2, if given, is one more feature row.
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

- Translations.

## Boundaries

- **Budget:** none.
- Also needs the user's approval: publishing a release to the package registry.

## Comments

<!-- startup-verification result -->
## Startup verification

Runner: thread verify-1 · Run: 2026-11-02 09:00–09:20 UTC

| Capability | Essential | How probed | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Scheduled check-in | yes | the verification thread's one-shot scheduled task bound to the coordinator's session (the coordinator holds no scheduler; threads do) | pass | token arrived in the coordinator at 09:07 | the coordinator cannot schedule; a thread arranges its check-ins |
| Real worker state | yes | cheap-tier thread; marker token | pass | marker comment read back | none |
| Confirmed stop | yes | cheap-tier thread, archived by a thread | pass | idle before, archived after | an archive can be undone |
| Loaded skill version | yes | the verification thread | pass | versions equal | none |

Verdict: ready
MD
}

if [ "$case_" = add-feature ]; then
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


if [ "$kind" = deliver ]; then
  # Delivery starts: Milestone 1 planned (one feature at a time), Startup verification passed, no Release planned yet.
  printf 'milestone-1\nparked\n' >> "$r/.scratch/labels.md"
  for f in 10-farewell 11-bye-code 12-bye-usage 20-quiet; do
    sed -i.bak 's/^Labels: enhancement$/Labels: enhancement, milestone-1/' "$r/.scratch/issues/$f.md"
  done
  sed -i.bak 's/^Parent: none$/Parent: .scratch\/issues\/00-milestone.md/' "$r/.scratch/issues/10-farewell.md" "$r/.scratch/issues/20-quiet.md"
  rm -f "$r/.scratch/issues/"*.bak
  write_milestone "One at a time, in this order." '| 3 | `25-hello-doc.md` Document the commands in the README | lone Ticket | the README lists `hello` and `bye` with one example each |'
  printf '\nModel tier: regular. Review depth: Deep.\n' >> "$r/.scratch/issues/10-farewell.md"
  # A third planned feature, blocked by an issue outside the Milestone: left out of Release 1, planned once it is free.
  cat > "$r/.scratch/issues/25-hello-doc.md" <<'MD'
Title: Document the commands in the README
Type: ticket
Labels: enhancement, milestone-1
Status: open
Parent: .scratch/issues/00-milestone.md
Blocked by: .scratch/issues/35-readme-tool.md

The README lists `hello` and `bye`, with one example each. Model tier: cheap.
MD
  cat > "$r/.scratch/issues/35-readme-tool.md" <<'MD'
Title: Pick the README format checker
Type: ticket
Labels: enhancement
Status: open
Parent: none
Blocked by: none

Outside the Milestone: the README format is checked by a tool still to be chosen.
MD
  sed -i.bak 's/^The `bye` command and its test. Model tier: regular.$/The `bye` command and its test; it also gives the `greeting` skill (`skills\/greeting\/SKILL.md`) a farewell rule. Model tier: regular./' "$r/.scratch/issues/11-bye-code.md"
  cat >> "$r/.scratch/issues/20-quiet.md" <<'MD'

Follows the `greeting` skill (`skills/greeting/SKILL.md`) for how messages are printed. Model tier: regular.
MD
  rm -f "$r/.scratch/issues/"*.bak
  mkdir -p "$r/skills/greeting"
  cat > "$r/skills/greeting/SKILL.md" <<'MD'
---
name: greeting
description: How the greeter's messages are worded and printed. Use when adding or changing a message.
---

- A greeting is `Hello, <name>!`, with `world` when no name is given.
- Print every message with `echo` to standard output; errors go to standard error.
MD
  # The world moves on between events: the threads' work and merges. The coordinator never runs writes; this script does.
  cat > "$r/.scratch/world.sh" <<'SH'
#!/usr/bin/env bash
# Usage: bash .scratch/world.sh <event>. Moves the fixture to the state the tracker shows when event <event> arrives.
# Run events 2 onward in order, from the repo root: the fixture is built at event 1's state, so event 1 needs no run.
# Not the coordinator's write: it stands in for the threads and the merges.
set -eu
k="$1"; cur="$(cat .scratch/stage)"
[ "$k" = 1 ] && [ "$cur" = 1 ] && { echo "world at event 1 (the fixture starts here; nothing to run)"; exit 0; }
[ "$k" -eq $((cur + 1)) ] || { echo "at stage $cur; next is $((cur + 1))" >&2; exit 2; }
i=.scratch/issues
s=.scratch/sessions
mkdir -p "$s" .scratch/branches .scratch/pulls
# The deliver-stall world: from event 3 on, the Spec thread of 10 stalls and its archive does not take; the Ticket
# thread of 20 stalls, is stopped and taken over, and its fresh thread stalls too.
if [ -e .scratch/variant ] && [ "$k" -ge 3 ]; then
  case "$k" in
    3) printf 'Thread started 10:05Z: running since 10:05Z\n' > "$s/10-farewell.md" ;;
    4) printf 'Thread started 10:05Z: idle since 10:30Z\n' > "$s/10-farewell.md" ;;
    5) ;; # still silent after its nudge
    6) ;; # the stop thread says it archived the session; the record still reads idle (read 13:09Z and 13:10Z)
    7) printf '13:30Z quiet: the --quiet flag\n' > .scratch/branches/20-quiet.md
       printf 'Thread started 13:10Z: running since 13:10Z\n' > "$s/20-quiet.md" ;;
    8) printf 'Thread started 13:10Z: idle since 13:31Z\n' > "$s/20-quiet.md" ;;
    9) ;; # still silent after its nudge
    10) printf 'Thread started 13:10Z: archived since 16:06Z\n' > "$s/20-quiet.md" ;;
    11) printf 'Thread started 16:10Z: running since 16:10Z\n' >> "$s/20-quiet.md" ;;
    12) printf 'Thread started 13:10Z: archived since 16:06Z\nThread started 16:10Z: idle since 16:12Z\n' > "$s/20-quiet.md" ;;
    13) ;; # the fresh thread still silent after its nudge: the feature's second stall
    14) ;;
    *) echo "no event $k" >&2; exit 2 ;;
  esac
  rm -f "$i/"*.bak
  echo "$k" > .scratch/stage
  echo "world at event $k"
  exit 0
fi
case "$k" in
  2) printf 'release-m1-r1\n' >> .scratch/labels.md
     for f in 10-farewell 11-bye-code 12-bye-usage 20-quiet; do
       sed -i.bak 's/^Labels: \(.*milestone-1\)$/Labels: \1, release-m1-r1/' "$i/$f.md"
     done
     # The check-in thread started at event 1 arranged the check-ins and posted the check-in record.
     [ -e .scratch/checkin-refused ] || printf '\n<!-- milestone check-in -->\nEvery 1 hour into the coordinator'"'"'s session, scheduled by the check-in thread; schedule sched-01; next firing 2026-11-02T11:00Z.\n' >> "$i/00-milestone.md"
     cat > "$i/40-release-m1-r1.md" <<'MD'
Title: Release Milestone 1 · Release 1
Type: release
Labels: none
Status: open
Parent: none
Blocked by: none

**Goal:** the greeter says goodbye and runs quietly in scripts.

**Label:** `release-m1-r1`. Every issue in this Release carries it.

**Milestone:** 00-milestone.md

**Cap:** 5 features. Used: 2.

## Scope

- **Add a farewell command** (1st in the Milestone's order)
  - 10-farewell.md, 11-bye-code.md, 12-bye-usage.md
- **Add a --quiet flag** (2nd)
  - 20-quiet.md

Left out: 25-hello-doc.md (3rd), blocked by 35-readme-tool.md, which is open.

## Notes

Posted as a comment when the Release is cut.

Planned by the Release thread from the Milestone issue's order, without waiting for the user.
MD
     ;;
  3) sed -i.bak 's/^Status: open$/Status: closed/' "$i/11-bye-code.md" "$i/12-bye-usage.md" ;;
  4) ;;
  5) ;;
  6) printf '0.4.0\n' > VERSION
     printf -- '- Messages use plain ASCII punctuation.\n' >> skills/greeting/SKILL.md ;;
  7) sed -i.bak 's/^Status: open$/Status: closed/' "$i/10-farewell.md"
     printf '0.5.0\n' > VERSION
     cat >> skills/greeting/SKILL.md <<'MD'
- A farewell is `Goodbye, <name>!`, with `world` when no name is given. Every message, greetings and farewells alike, is printed through one `say` function in `src/greet.sh`, so a flag that silences output silences every message.
MD
     ;;
  8) ;;
  9) sed -i.bak 's/^Status: open$/Status: closed/' "$i/20-quiet.md" ;;
  10) ;;
  11) printf '# Changelog\n\n## Milestone 1 · Release 1\n\nVersions: 0.4.0, 0.5.0.\n' > CHANGELOG.md
     sed -i.bak 's/^Status: open$/Status: closed/' "$i/40-release-m1-r1.md"
     printf '\n## Comments\n\n## Milestone 1 · Release 1\n\nVersions: 0.4.0, 0.5.0. Release notes, posted at the cut.\n' >> "$i/40-release-m1-r1.md" ;;
  12) sed -i.bak 's/^Status: open$/Status: closed/' "$i/35-readme-tool.md" ;;
  13) # A new blocker for 25, filed meanwhile; the Release thread opened Release 2's issue before it found it, and
      # labelled nothing: an empty release issue.
      cat > "$i/36-readme-style.md" <<'MD'
Title: Agree the README style
Type: ticket
Labels: enhancement
Status: open
Parent: none
Blocked by: none

Outside the Milestone: the README needs an agreed style before any section is added.
MD
      sed -i.bak 's/^Blocked by: \.scratch\/issues\/35-readme-tool\.md$/Blocked by: .scratch\/issues\/35-readme-tool.md, .scratch\/issues\/36-readme-style.md/' "$i/25-hello-doc.md"
      printf 'release-m1-r2\n' >> .scratch/labels.md
      cat > "$i/41-release-m1-r2.md" <<'MD'
Title: Release Milestone 1 · Release 2
Type: release
Labels: none
Status: open
Parent: none
Blocked by: none

**Goal:** the README documents the commands.

**Label:** `release-m1-r2`. Every issue in this Release carries it.

**Milestone:** 00-milestone.md

**Cap:** 5 features. Used: 0.

## Scope

None.

Left out: 25-hello-doc.md (3rd), blocked by 36-readme-style.md, which is open.
MD
      ;;
  14) ;;
  15) sed -i.bak 's/^Status: open$/Status: closed/' "$i/36-readme-style.md" ;;
  16) # The Release thread filled the empty 41 with 25.
      sed -i.bak 's/^Labels: enhancement, milestone-1$/Labels: enhancement, milestone-1, release-m1-r2/' "$i/25-hello-doc.md"
      cat > "$i/41-release-m1-r2.md" <<'MD'
Title: Release Milestone 1 · Release 2
Type: release
Labels: none
Status: open
Parent: none
Blocked by: none

**Goal:** the README documents the commands.

**Label:** `release-m1-r2`. Every issue in this Release carries it.

**Milestone:** 00-milestone.md

**Cap:** 5 features. Used: 1.

## Scope

- **Document the commands in the README** (3rd in the Milestone's order)
  - 25-hello-doc.md
MD
      ;;
  17) # The Ticket thread of 25 (started 14:10) pushed a commit at 14:40.
      printf '14:40Z README: the commands section\n' > .scratch/branches/25-hello-doc.md
      printf 'Thread started 14:10Z: running since 14:10Z\n' > "$s/25-hello-doc.md" ;;
  18) # the thread did nothing since 14:40: a silent thread
      printf 'Thread started 14:10Z: idle since 14:41Z\n' > "$s/25-hello-doc.md" ;;
  19) ;; # still silent after its nudge: a stall
  20) # The stop thread archived the thread's session at 17:06.
      printf 'Thread started 14:10Z: archived since 17:06Z\n' > "$s/25-hello-doc.md" ;;
  21) # The fresh thread (started 17:10) pushed and turned its pull request ready at 17:50, and reported nothing: a lost
      # callback.
      printf 'Thread started 14:10Z: archived since 17:06Z\nThread started 17:10Z: running since 17:10Z\n' > "$s/25-hello-doc.md"
      printf '17:35Z README: one example each\n' >> .scratch/branches/25-hello-doc.md
      printf 'State: open. Ready for review since 17:50Z.\nChanged: README.md\nChecks: passing\nComments: none\n' > .scratch/pulls/11.md ;;
  22) sed -i.bak 's/^Status: open$/Status: closed/' "$i/25-hello-doc.md"
      printf 'README lists hello and bye.\n' > README.md
      printf 'State: merged 18:05Z, with no version change.\nChanged: README.md\nChecks: passing\nComments: none\n' > .scratch/pulls/11.md ;;
  23) printf '# Changelog\n\n## Milestone 1 · Release 2\n\nVersions: none (no skill changed).\n\n## Milestone 1 · Release 1\n\nVersions: 0.4.0, 0.5.0.\n' > CHANGELOG.md
      sed -i.bak 's/^Status: open$/Status: closed/' "$i/41-release-m1-r2.md" ;;
  *) echo "no event $k" >&2; exit 2 ;;
esac
rm -f "$i/"*.bak
echo "$k" > .scratch/stage
echo "world at event $k"
SH
  echo 1 > "$r/.scratch/stage"
  [ "$case_" = deliver-stall ] && printf 'b\n' > "$r/.scratch/variant"
  # The variant's world: the scheduler refuses the coordinator's session, so no check-in record ever appears.
  [ "$case_" = deliver-checkin-failed ] && printf 'world.sh: the scheduler refuses the target\n' > "$r/.scratch/checkin-refused"
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

This is a dry run. The tracker doc, `docs/agents/issue-tracker.md`, says how every write is recorded in
`.scratch/proposed-actions.md` instead of being made: follow it for every tracker write and every thread you would
start. Change no other file. The user is scripted: when the skill has you ask the user something, take the answer
from "The user's answers" below; when a question is not covered there, append it to `.scratch/questions.md`, treat it
as unanswered, and do not guess an answer. Today is 2026-11-02.

When you stop, write `.scratch/report.md`: the last message you would send the user, and what the skill says comes
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
- Budget: "None."
- Boundaries beyond the Boundary record: "Publishing a release to the package registry needs my approval."
- The draft Milestone issue: "Yes, that's it. Write it."
- Startup verification: "It has not run in this environment yet."

Stop when the skill would hand over to its next phase.
TXT
  elif [ "$case_" = add-feature ]; then
    cat <<'TXT'

The user's message: "Add colour output (issue 30) to Milestone 1, after the quiet flag."

The user's answers:
- When asked to plan issue 30 first: "Yes. Colour the name green only when standard output is a terminal;
  `--no-color` turns it off. Accepted when a test covers the terminal case and `--no-color`. It is one lone Ticket."
- Its place in the order: "Third, after the quiet flag."
- Whether it joins the open Release 0.4.0: "Leave that to the rules."
- Any change to the goal, acceptance, exclusions or boundaries: "No."

Stop when the feature is added, or when the skill says it must wait.
TXT
  else
    cat <<'TXT'

Your project instructions (the coordinator's own) say: "Build threads: at most 3 at once. Tier map: the `model-tiers`
default. Briefs also link the repo. This project does not run the `triage` skill."

Planning has settled and the Startup verification result on the Milestone issue reads `Verdict: ready`: you are in
delivery. The clock reads 2026-11-02T10:00Z at event 1, and each event gives its own time. Events arrive one at a time, below. For each event, in order: from event 2 on, first run
`bash .scratch/world.sh <k>` from the repo root (it moves the fixture to what the tracker shows when the event arrives;
it is not your write; event 1 needs no run, since the fixture starts in its state), then write `## Event <k>` and the
actions the skill has you take, reading the state from the tracker each time. A thread you start
does not run in a dry run: what it does arrives as a later event. A pull request named in an event exists only in that
event's text, with the changed files it lists. Ask the user nothing: no answers are scripted.

- Event 1 (10:00Z): delivery starts.
- Event 2 (10:05Z): the Release thread reports that it has planned the Release, and the check-in thread, if you started one,
  reports that it arranged the check-ins.
- Event 3 (10:15Z): the Spec thread of `10-farewell.md` reports that its Spec pull request #7 is ready to merge and asks for its
  version number. #7 changes `skills/greeting/SKILL.md` (a new farewell rule), `src/greet.sh` and `test.sh`.
- Event 4 (10:20Z): the Spec thread of `10-farewell.md` asks for a version number for pull request #10, which builds no issue
  (a check its retro found): #10 changes `skills/greeting/SKILL.md` (a new wording rule) only.
- Event 5 (10:25Z): the Spec thread of `10-farewell.md` reports that #7 was closed unmerged (its branch had to be rebuilt) and
  that its new Spec pull request #9, with the same changes, is ready to merge; it asks for its version number.
- Event 6 (10:30Z): the Spec thread of `10-farewell.md` reports that #10 is merged, with the number you handed out as its last
  commit.
- Event 7 (10:35Z): the Spec thread of `10-farewell.md` reports that #9 is merged, with the number you handed out as its last
  commit, and that its Spec is closed.
- Event 8 (10:40Z): the Ticket thread of `20-quiet.md` reports that its pull request #8 is ready to merge and asks whether it needs
  a version number. #8 changes `src/greet.sh` and `test.sh` only.
- Event 9 (10:50Z): the Ticket thread of `20-quiet.md` reports that #8 is merged and its Ticket closed.
- Event 10 (11:00Z): a scheduled check-in fires; no thread has reported since event 9.
- Event 11 (11:15Z): the Release thread reports that it cut Milestone 1 · Release 1 and planned no next Release, because the one
  planned feature left, `25-hello-doc.md`, is blocked by `35-readme-tool.md`.
- Event 12 (12:00Z): a scheduled check-in fires; no thread has reported since event 11.
- Event 13 (12:20Z): the Release thread started at event 12 reports that it planned no Release: `25-hello-doc.md` is now also
  blocked by `36-readme-style.md`, filed meanwhile. It had opened `41-release-m1-r2.md` before it found that, and
  labelled no issue.
- Event 14 (13:00Z): a scheduled check-in fires; no thread has reported since event 13.
- Event 15 (14:00Z): a scheduled check-in fires: `36-readme-style.md` has closed; no thread has reported since event 13.
- Event 16 (14:10Z): the Release thread started at event 15 reports that it filled `41-release-m1-r2.md` with `25-hello-doc.md`.
- Event 17 (15:00Z): a scheduled check-in fires; no thread has reported since event 16.
- Event 18 (16:00Z): a scheduled check-in fires; no thread has reported since event 16.
- Event 19 (17:00Z): a scheduled check-in fires; no thread has reported since event 16.
- Event 20 (17:10Z): the stop thread started at event 19, if you started one, reports that it archived the session of the
  Ticket thread of `25-hello-doc.md` (the one started at 14:10Z).
- Event 21 (18:00Z): a scheduled check-in fires; no thread has reported since event 20.
- Event 22 (18:10Z): the Ticket thread of `25-hello-doc.md` reports that its pull request #11, which changes `README.md`
  only, merged with no version change, and that its Ticket is closed.
- Event 23 (18:20Z): the Release thread reports that it cut Milestone 1 · Release 2 and planned no next Release: no
  planned feature of the Milestone is left open.

Stop after event 23.
TXT
  fi
  echo "---"
} > "$out/PROMPT.md"

if [ "$case_" = deliver-checkin-failed ]; then
  # Events 1 to 4 only, with event 2's check-in thread reporting that it could not arrange the check-ins.
  awk '
    /^- Event 2 \(/ { print "- Event 2 (10:05Z): the Release thread reports that it has planned the Release, and the check-in thread reports that"
                     print "  it could not arrange the check-ins: the scheduler refused the coordinator'"'"'s session as a target."; skip = 1; next }
    /^- Event 5 \(/ { drop = 1 }
    /^Stop after event 23\.$/ { print ""; print "Stop after event 4."; drop = 0; next }
    /^- Event / { skip = 0 }
    skip && /^  / { next }
    drop { next }
    { print }
  ' "$out/PROMPT.md" > "$out/PROMPT.md.new" && mv "$out/PROMPT.md.new" "$out/PROMPT.md"
fi

if [ "$case_" = deliver-stall ]; then
  # Events 1 and 2 as in deliver; then its own events, which the world's variant plays from event 3 on.
  awk '
    /^- Event 3 \(/ { drop = 1 }
    /^Stop after event 23\.$/ { drop = 0
      print "- Event 3 (11:00Z): a scheduled check-in fires; no thread has reported since event 2."
      print "- Event 4 (12:00Z): a scheduled check-in fires; no thread has reported since event 2."
      print "- Event 5 (13:00Z): a scheduled check-in fires; no thread has reported since event 2."
      print "- Event 6 (13:10Z): the stop thread started at event 5, if you started one, reports that it archived the session of the"
      print "  Spec thread of `10-farewell.md` (the one started at 10:05Z): the archive call returned success."
      print "- Event 7 (14:00Z): a scheduled check-in fires; no thread has reported since event 6."
      print "- Event 8 (15:00Z): a scheduled check-in fires; no thread has reported since event 6."
      print "- Event 9 (16:00Z): a scheduled check-in fires; no thread has reported since event 6."
      print "- Event 10 (16:10Z): the stop thread started at event 9, if you started one, reports that it archived the session of"
      print "  the Ticket thread of `20-quiet.md` (the one started at 13:10Z)."
      print "- Event 11 (17:00Z): a scheduled check-in fires; no thread has reported since event 10."
      print "- Event 12 (18:00Z): a scheduled check-in fires; no thread has reported since event 10."
      print "- Event 13 (19:00Z): a scheduled check-in fires; no thread has reported since event 10."
      print "- Event 14 (20:00Z): a scheduled check-in fires; no thread has reported since event 10."
      print ""
      print "Stop after event 14."; next }
    drop { next }
    { print }
  ' "$out/PROMPT.md" > "$out/PROMPT.md.new" && mv "$out/PROMPT.md.new" "$out/PROMPT.md"
fi

echo "built $case_ fixture in $out"
