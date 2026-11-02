#!/usr/bin/env bash
# Builds one fixture for the milestone skill's planning-phase dry run.
# Usage: make-fixture.sh <out-dir> <plan|add-feature>
# Makes <out-dir>/repo (a git repo, one commit on main, with a dry-run local tracker) and <out-dir>/PROMPT.md
# (the scripted prompt for a fresh coordinator session). See evals/milestone/README.md.
set -eu
out="$1"; case_="$2"
case "$case_" in plan|add-feature) ;; *) echo "unknown case: $case_" >&2; exit 2 ;; esac
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

The version lives in `VERSION`; Releases bump it. See `docs/agents/release.md`.
MD

cat > "$r/docs/index.md" <<'MD'
# Docs index

- [docs/agents/issue-tracker.md](agents/issue-tracker.md): the local Markdown tracker, in dry-run mode, and its operations. Read before any tracker operation.
- [docs/agents/boundaries.md](agents/boundaries.md): the Boundary record. Read when deciding whether an action needs the user, or when giving an issue a Milestone label.
- [docs/agents/release.md](agents/release.md): the release doc (Releases bump `VERSION`). Read when planning or cutting a Release.
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

Starting a thread or a subagent is a write too: record it as `### <k>. Start a thread` with `Skill:` and `Brief:` lines.

- **Read an issue**: read its file.
- **List issues**: read every file under `.scratch/issues/`.
- **Create an issue**: fields `Title:`, `Labels:`, `Parent:`, then `Body:` followed by the whole body between `~~~` lines. The new issue's file name is the next free `NN-slug.md`; give it in the `Issue:` line as `new (NN-slug.md)`.
- **Edit an issue body**: fields `Body:` followed by the WHOLE new body between `~~~` lines (never only the changed part).
- **Create a label**: field `Label:`.
- **Apply / remove labels**: fields `Add:` and `Remove:` (comma-separated, or none).
- **Make an issue a sub-issue of a parent**: field `Parent:` (the parent's issue file). An issue has at most one parent.
- **Comment on an issue**: field `Body:` followed by the comment between `~~~` lines.
- **Close**: field `Outcome:` (completed or not planned) and a one-line `Reason:`.
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

cat > "$r/docs/agents/release.md" <<'MD'
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

if [ "$case_" = add-feature ]; then
  printf 'milestone-1\nrelease-0.4.0\n' >> "$r/.scratch/labels.md"
  for f in 10-farewell 11-bye-code 12-bye-usage 20-quiet; do
    sed -i.bak 's/^Labels: enhancement$/Labels: enhancement, milestone-1, release-0.4.0/' "$r/.scratch/issues/$f.md"
    rm -f "$r/.scratch/issues/$f.md.bak"
  done
  sed -i.bak 's/^Parent: none$/Parent: .scratch\/issues\/00-milestone.md/' "$r/.scratch/issues/10-farewell.md" "$r/.scratch/issues/20-quiet.md"
  rm -f "$r/.scratch/issues/"*.bak
  cat > "$r/.scratch/issues/00-milestone.md" <<'MD'
Title: Milestone 1: goodbye and quiet
Type: milestone
Labels: milestone-1
Status: open
Parent: none
Blocked by: none

## Goal

By the end, the greeter can say goodbye and can run silently in scripts, so it can ship as 1.0.

## Features, in build order

In this order, up to 2 at once. Each feature is its own issue carrying `milestone-1`.

| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | `10-farewell.md` Add a farewell command | Spec | `greet.sh bye Ada` prints `Goodbye, Ada!`; no name greets the world; tests cover both |
| 2 | `20-quiet.md` Add a --quiet flag | lone Ticket | `--quiet` prints nothing and keeps the exit code |

## Acceptance

- Every feature above is merged and its issue closed.
- The user runs `greet.sh --quiet bye Ada` at the Milestone review and sees nothing, exit 0.

## Excluded

- Translations.

## Boundaries

- **Budget:** none.
- Also needs the user's approval: publishing a release to the package registry.

## Comments

<!-- startup-verification result -->
## Startup verification

Verdict: ready
MD
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
  else
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
  fi
  echo "---"
} > "$out/PROMPT.md"

echo "built $case_ fixture in $out"
