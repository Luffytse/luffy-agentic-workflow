#!/usr/bin/env bash
# Builds one fixture for the team-lead skill's dry run, built on harness events.
# Usage: make-fixture.sh <out-dir> <deliver|deliver-stall|deliver-pause|deliver-lift|deliver-earlier>
# Makes <out-dir>/repo (a git repo on main, a local Markdown tracker in dry-run mode and a dry-run harness) and
# <out-dir>/PROMPT.md (the scripted prompt for a fresh coordinator session). See evals/team-lead/README.md.
set -eu
out="$1"; case_="$2"
case "$case_" in
  deliver) variant=deliver ;; deliver-stall) variant=stall ;; deliver-pause) variant=pause ;; deliver-lift) variant=lift ;; deliver-earlier) variant=earlier ;;
  *) echo "unknown case: $case_" >&2; exit 2 ;;
esac
here="$(cd "$(dirname "$0")" && pwd)"
[ -e "$out" ] && { echo "$out exists" >&2; exit 2; }
mkdir -p "$out"
out="$(cd "$out" && pwd)"
r="$out/repo"
mkdir -p "$r/docs/dev-skills" "$r/src" "$r/skills/greeting" "$r/.scratch/issues" "$r/.scratch/pulls" "$r/.scratch/harness"

cat > "$r/CLAUDE.md" <<'MD'
# greeter

A tiny shell greeter. Run `bash test.sh` before each push.

## Agent skills

Start at `docs/dev-skills/index.md`. Issue tracker: `docs/dev-skills/issue-tracker.md`. Boundaries: `docs/dev-skills/boundaries.md`.
Releases: `docs/dev-skills/release.md`. Workers run in the dry-run harness `docs/dev-skills/harness.md` documents.

## Merge-time steps

The coordinator follows these two. `docs/dev-skills/release.md` has the bump rules.

**Version hand-out.** A thread about to merge a pull request that changes a file under `skills/` asks the coordinator for its version number just before merging; a pull request that changes no such file gets none and merges with no bump.
- The coordinator gives main's `VERSION` raised minor for a new or changed skill rule and patch for a fix to one. It records the number first, in a comment on the issue the pull request builds whose first line is `<!-- version hand-out -->` and whose second is `Version <number> for <pull request>: merge it next, with the bump as its last commit.` Then it tells the thread.
- Skill-changing pull requests merge one at a time. While a number is out (main's `VERSION` has not reached it and its pull request is open), give none: record the request as `Waiting` the same way and tell the thread to wait.
- While the user's pause is in effect, give no number: record the request as waiting and tell the thread to wait; a number already out stays out and its merge may finish.

**Ticket re-read after a skill merge.** Right after a pull request that changed a file under `skills/` merges, before any further thread starts, re-read the open issues of the Milestone that no running thread is building and whose body names the changed skill or a changed file, against main's new text of the skill: update an issue the change makes wrong or incomplete (the whole body written back with only that change and a one-line note naming the merge); close one it makes obsolete; otherwise comment that it was re-read and still fits.
MD

cat > "$r/docs/dev-skills/index.md" <<'MD'
# Docs index

- [docs/dev-skills/issue-tracker.md](issue-tracker.md): the local Markdown tracker, in dry-run mode. Read before any tracker operation.
- [docs/dev-skills/harness.md](harness.md): the dry-run harness workers run in: how to start, read, stop, message and schedule them. Read before any worker action.
- [docs/dev-skills/boundaries.md](boundaries.md): the Boundary record.
- [docs/dev-skills/release.md](release.md): the release doc.
MD

cat > "$r/docs/dev-skills/issue-tracker.md" <<'MD'
# Issue tracker: local Markdown, dry run

Issues are files under `.scratch/issues/`, one per issue, named `NN-slug.md`. Each starts with header lines `Title:`,
`Type:`, `Labels:` (comma-separated), `Status:` (open or closed), `Parent:` and `Blocked by:`. Comments follow a
`## Comments` heading, each under a `### <UTC time> <author>` heading.
Pull requests are files under `.scratch/pulls/`, one per pull request, named `<n>.md`, with header lines `Builds:`
(the issue file it builds), `Branch:` (its head branch), `State:` (draft, open, merged or closed), `Opened:`, `Ready:`, `Merged:`, `Changed:` and
`Checks:`, and comments in the same form.

**Dry run.** No write changes a file here. Each write is appended to `.scratch/proposed-actions.md` as one block,
numbered in the order you take it:

    ### <k>. <Operation name>
    Issue: <issue file>
    <the operation's fields>

Before the blocks of event `<k>`, append a line `## Event <k>` (also when the event leads to no write), and keep
numbering on from the event before. A block counts as written at its event's clock. Between events, `world.py` applies
your **Comment on an issue** and **Apply / remove labels** blocks to the files, as the tracker would, so later reads
see them.

- **Read an issue**: read its file.
- **List issues**: read every file under `.scratch/issues/`.
- **Edit an issue body**: field `Body:` followed by the WHOLE new body between `~~~` lines.
- **Apply / remove labels**: fields `Add:` and `Remove:` (comma-separated, or none).
- **Comment on an issue**: field `Body:` followed by the comment between `~~~` lines.
- **Close**: fields `Outcome:` and `Reason:`.
- **Count open blockers**: read the `Blocked by:` header and the `Status:` of each issue it names.
- **Park**: add the `parked` label, then comment with a link to the attempt history. An issue is parked when its
  `Labels:` include `parked`; the user lifts the park by removing the label.
- **Read a PR**: read `.scratch/pulls/<n>.md`.
- **List PRs**: read every file under `.scratch/pulls/`.

Branches are the repo's own git branches (`git log <branch>`); nothing is pushed anywhere else.
MD

cat > "$r/docs/dev-skills/harness.md" <<'MD'
# Dry-run harness

The dry run's stand-in for the tool workers run in. It has no `worker-control` reference, so `worker-control`'s
fallback reads this page as the Harness's own docs. No worker really runs: what a worker does arrives as a later
event, and every action below is a block in `.scratch/proposed-actions.md`, in the tracker doc's block form.

- **What it does by itself:** it wakes the coordinator with an event when a worker reports or asks, when a worker
  ends or fails, and when a check-in fires.
- **Start a worker:** block `### <k>. Start a worker` with `Issue:` (the issue file it works on), `Skill:`, `Tier:`
  and `Brief:` followed by the whole brief between `~~~` lines. The worker's id is `w-<NN>-<HHMM>`: the issue file's
  number and the event clock (for example `w-25-1420`).
- **Read a worker's state:** `.scratch/harness/workers.md`, one line per worker:
  `<id> <issue file> branch <branch>: <working | idle | ended | failed | stopped> since <UTC time>`. `ended`,
  `failed` and `stopped` are ended; `idle` is not. A worker started at this event has no line until the next one.
- **Notice an end or failure:** the wake's event names the worker; read its line.
- **Message a worker:** block `### <k>. Message a worker` with `Worker:` (its id) and `Body:` between `~~~` lines.
- **Stop a worker and read the stop back:** block `### <k>. Stop a worker` with `Worker:`. A later event says the stop
  was taken; read the worker's line then: only `stopped` is a stop.
- **Pause and resume:** no pause of its own. Message a worker to push its work and stop at its next natural step, and
  later to carry on.
- **Arrange and end a check-in:** block `### <k>. Arrange a check-in` with `Every:` and `Into: coordinator`;
  `### <k>. End a check-in`. `.scratch/harness/checkins.md` lists the check-in that runs. A recurring check-in fires
  at the top of each hour; each firing is an event.
- **Message the user:** block `### <k>. Message the user` with `Body:` between `~~~` lines.
MD

cat > "$r/docs/dev-skills/boundaries.md" <<'MD'
# Boundary record

- **Irreversible actions agents may take**: delete test data agents generate while implementing.
- **Actions that need the user's approval**: sending any message to customers.
- **Budget**: none.
- **Check-in interval**: 1 hour.
- **Milestone label form**: `milestone-<n>`. An issue belongs to a Milestone when it carries that label.
MD

cat > "$r/docs/dev-skills/release.md" <<'MD'
# Releases

- **Bump mode**: pull requests bump. Every pull request that changes a file under `skills/` bumps `VERSION` as its last commit, with the number the coordinator gives just before merge (`CLAUDE.md`, "Merge-time steps"). Any other pull request leaves `VERSION` as it is. A Release opens no bump pull request.
- **Version file**: `VERSION`. **Changelog**: `CHANGELOG.md`.
- **Release name**: `Milestone <m> · Release <n>`, label `release-m<m>-r<n>`, release issue titled `Release Milestone <m> · Release <n>` with a `**Milestone:**` line.
MD

printf '0.3.0\n' > "$r/VERSION"
printf '# Changelog\n' > "$r/CHANGELOG.md"
printf '# greeter\n' > "$r/README.md"
cat > "$r/src/greet.sh" <<'SH'
#!/usr/bin/env bash
case "${1:-}" in
  hello) echo "Hello, ${2:-world}!" ;;
  *) echo "usage: greet.sh hello <name>" >&2; exit 2 ;;
esac
SH
printf '#!/usr/bin/env bash\nset -e\n[ "$(bash src/greet.sh hello Ada)" = "Hello, Ada!" ]\necho OK\n' > "$r/test.sh"
cat > "$r/skills/greeting/SKILL.md" <<'MD'
---
name: greeting
description: How the greeter's messages are worded and printed. Use when adding or changing a message.
---

- A greeting is `Hello, <name>!`, with `world` when no name is given.
- Print every message with `echo` to standard output; errors go to standard error.
MD

order="One at a time, in this order."
blocked25=".scratch/issues/35-readme-tool.md"
if [ "$variant" = pause ]; then order="Up to 2 at once, in this order."; blocked25="none"; fi

issue() { # file title type labels parent blocked body
  printf 'Title: %s\nType: %s\nLabels: %s\nStatus: open\nParent: %s\nBlocked by: %s\n\n%s\n\n## Comments\n' "$2" "$3" "$4" "$5" "$6" "$7" > "$r/.scratch/issues/$1"
}
issue 00-milestone.md "Milestone 1: goodbye and quiet" milestone milestone-1 none none "## Goal

By the end, the greeter can say goodbye, run silently in scripts and is documented.

## Features, in build order

$order Each feature is its own issue carrying \`milestone-1\`.

| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | \`10-farewell.md\` Add a farewell command | Spec | \`greet.sh bye Ada\` prints \`Goodbye, Ada!\` |
| 2 | \`20-quiet.md\` Add a --quiet flag | lone Ticket | \`--quiet\` prints nothing and keeps the exit code |
| 3 | \`25-hello-doc.md\` Document the commands | lone Ticket | the README lists \`hello\` and \`bye\` |

## Acceptance

- Every feature above is merged and its issue closed.

## Excluded

- Translations.

## Boundaries

- **Budget:** none.
- None beyond the Boundary record."
cat >> "$r/.scratch/issues/00-milestone.md" <<'MD'

### 2026-11-03T08:30:00Z coordinator

## Startup verification

Runner: coordinator · Run: 2026-11-03 08:00–08:30 UTC
Harness: dry-run harness (fallback, docs/dev-skills/harness.md)

| Capability | Essential | How probed | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Start a worker | yes | Start a worker block | pass | id returned, line listed | dry run |
| Worker state | yes | workers.md | pass | working read | dry run |
| Pause and resume | not relied on | by message | pass | replies | a convention, not a Harness pause |
| Confirmed stop | yes | Stop a worker, then workers.md | pass | working before, stopped after | dry run |
| End or failure notice | yes | the harness's wake | pass | wake, then ended read | failure not provoked |
| Scheduled check-in | yes | Arrange a check-in into the coordinator | pass | two arrivals | dry run |
| Loaded skill version | yes | the coordinator | pass | versions equal | none |

Verdict: ready
MD
issue 10-farewell.md "Add a farewell command" spec "enhancement, milestone-1" .scratch/issues/00-milestone.md none "\`greet.sh bye <name>\` prints \`Goodbye, <name>!\`. Tickets: 11-bye-code.md, 12-bye-usage.md.

Model tier: regular. Review depth: Deep."
issue 11-bye-code.md "Farewell: code and test" ticket "enhancement, milestone-1" .scratch/issues/10-farewell.md none "The \`bye\` command; it also gives the \`greeting\` skill (\`skills/greeting/SKILL.md\`) a farewell rule. Model tier: regular."
issue 12-bye-usage.md "Farewell: usage line" ticket "enhancement, milestone-1" .scratch/issues/10-farewell.md .scratch/issues/11-bye-code.md "The usage line names \`bye\`. Model tier: cheap."
issue 20-quiet.md "Add a --quiet flag" ticket "enhancement, milestone-1" .scratch/issues/00-milestone.md none "\`--quiet\` before any command prints nothing and keeps the exit code. Follows the \`greeting\` skill (\`skills/greeting/SKILL.md\`) for how messages are printed. Model tier: regular."
issue 25-hello-doc.md "Document the commands in the README" ticket "enhancement, milestone-1" .scratch/issues/00-milestone.md "$blocked25" "The README lists \`hello\` and \`bye\`, one example each. Model tier: cheap."
issue 35-readme-tool.md "Pick the README format checker" ticket enhancement none none "Outside the Milestone."
: > "$r/.scratch/harness/workers.md"
: > "$r/.scratch/harness/checkins.md"
if [ "$variant" = earlier ]; then
  # Milestone 1's own case: the earlier milestone loop paused delivery while 10's Spec worker ran; its only record of
  # that worker is an old delivery-thread record. Release 1 is open with 10 and 20.
  issue 40-release-m1-r1.md "Release Milestone 1 · Release 1" release release-m1-r1 none none "**Milestone:** 00-milestone.md

Goal: the farewell command and the quiet flag.

Maintenance fixes: none."
  for f in 10-farewell 11-bye-code 12-bye-usage 20-quiet; do
    sed -i.bak 's/^Labels: enhancement, milestone-1$/Labels: enhancement, milestone-1, release-m1-r1/' "$r/.scratch/issues/$f.md"
  done
  rm -f "$r/.scratch/issues/"*.bak
  cat >> "$r/.scratch/issues/00-milestone.md" <<'MD'

### 2026-11-03T07:00:00Z coordinator

<!-- milestone check-in -->
Every 1 hour into the coordinator, scheduled by the coordinator; schedule sched-01.

### 2026-11-03T07:58:00Z coordinator

<!-- milestone stand-up -->
Check-in 07:58Z; previous 07:00Z. No delivery thread is running; no decision.

### 2026-11-03T08:20:00Z coordinator

<!-- milestone pause -->
Pause requested at 08:20Z by the user: "stop here for now". Asked to reach a safe point: 10-farewell.md: w-10-0800

### 2026-11-03T08:21:00Z coordinator

<!-- milestone check-in ended -->
Schedule sched-01 deleted at the user's stop; no future firing.
MD
  cat >> "$r/.scratch/issues/10-farewell.md" <<'MD'

### 2026-11-03T08:00:00Z coordinator

<!-- milestone delivery thread -->
w-10-0800: Spec thread with implement-spec, tier regular, Review depth Deep; started 08:00Z.
MD
  printf 'w-10-0800 10-farewell.md branch t10: working since 2026-11-03T08:00:00Z\n' > "$r/.scratch/harness/workers.md"
fi
: > "$r/.scratch/proposed-actions.md"
echo 1 > "$r/.scratch/stage"
echo "$variant" > "$r/.scratch/variant"
cp "$here/world.py" "$r/.scratch/world.py"

# The events: number, clock and text. The clock lines also feed world.py (the time of the coordinator's writes).
events_common='1|09:00|Delivery starts: planning has settled and Startup verification reads `Verdict: ready`.
2|09:20|Worker w-00-0900 (the Release worker) reports: it planned Milestone 1 · Release 1 and opened `40-release-m1-r1.md`.'
case "$variant" in
deliver) events="$events_common"'
3|10:00|A check-in fires.
4|10:40|Worker w-10-0920 asks for its version number: its Spec pull request #7 (`.scratch/pulls/7.md`) is ready to merge.
5|10:55|Worker w-10-0920 reports: #7 merged with the number you gave as its last commit; `10-farewell.md` and its Tickets are closed.
6|12:00|A check-in fires.
7|12:20|Worker w-20-1055 reports: #8 merged with no version change; `20-quiet.md` is closed.
8|13:00|A check-in fires.
9|13:30|Worker w-40-1220 reports: it cut Milestone 1 · Release 1 (`40-release-m1-r1.md` closed) and planned no next Release: `25-hello-doc.md` is blocked by `35-readme-tool.md`.
10|14:00|A check-in fires.
11|14:20|Worker w-00-1400 reports: it planned Milestone 1 · Release 2 and opened `41-release-m1-r2.md`.
12|15:00|A check-in fires.
13|16:00|A check-in fires.
14|17:00|A check-in fires.
15|17:05|The harness wakes you: the stop of worker w-25-1420 you asked for has been taken.
16|18:00|A check-in fires.
17|18:10|Worker w-25-1705 reports: #11 merged with no version change; `25-hello-doc.md` is closed.
18|18:40|Worker w-41-1810 reports: it cut Milestone 1 · Release 2 (`41-release-m1-r2.md` closed) and planned no next Release: no planned feature is left open.' ;;
stall|lift) events="$events_common"'
3|10:00|A check-in fires.
4|11:00|A check-in fires.
5|12:00|A check-in fires.
6|12:05|The harness wakes you: the stop of worker w-10-0920 you asked for has been taken.
7|12:30|The harness wakes you: worker w-20-1205 failed.
8|13:00|A check-in fires.
9|14:00|A check-in fires.
10|15:00|A check-in fires.
11|15:05|The harness wakes you: the stop of worker w-20-1230 you asked for has been taken.
12|16:00|A check-in fires.'
  [ "$variant" = lift ] && events="$events"'
13|16:30|The user writes: "I removed the parked label from 10-farewell.md. Carry on with it."
14|16:35|The harness wakes you: the stop of worker w-10-0920 you asked for has been taken.
15|16:50|The user writes: "I removed the parked label from 20-quiet.md too."
16|17:00|A check-in fires.' ;;
earlier) events='1|09:00|The user writes: "Resume delivery."
2|10:00|A check-in fires.
3|10:15|Worker w-10-0800 reports: its Spec pull request #7 (`src/greet.sh` and `test.sh` only) merged with no version change; `10-farewell.md` and its Tickets are closed.' ;;
pause) events="$events_common"'
3|10:20|The user writes: "Please pause delivery for now."
4|10:40|Worker w-20-0920 reports: #8 merged with no version change; `20-quiet.md` is closed.
5|11:00|A check-in fires.
6|12:00|A check-in fires.
7|12:30|The user writes: "Resume delivery."
8|13:00|A check-in fires.
9|14:00|A check-in fires.' ;;
esac
printf '%s\n' "$events" | awk -F'|' '{print $1, $2}' > "$r/.scratch/clock"

(cd "$r" && git init -q -b main && git add -A && \
  GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=f@example.com GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=f@example.com \
  GIT_AUTHOR_DATE=2026-11-03T08:00:00Z GIT_COMMITTER_DATE=2026-11-03T08:00:00Z git commit -q -m "greeter at Milestone 1 start")

last="$(printf '%s\n' "$events" | tail -n 1 | cut -d'|' -f1)"
{
  echo "# team-lead dry run: $case_"
  echo
  echo "Give the fresh session only the text between the two --- lines, with <checkout> replaced by the checkout under test."
  echo "Keep this header, evals/team-lead/README.md and score.py away from it."
  echo
  echo "---"
  cat <<TXT
You are the coordinator of this project, and planning of Milestone 1 (\`.scratch/issues/00-milestone.md\`) is done.
Run delivery with the \`team-lead\` skill from \`<checkout>/plugins/dev-skills/skills/team-lead/SKILL.md\`, and every
other skill it names from the same \`<checkout>/plugins/dev-skills/skills/\` folder (\`worker-control\`, \`milestone\`,
\`model-tiers\` and the rest), never an installed copy. Its snapshot command is
\`<checkout>/plugins/dev-skills/skills/team-lead/snapshot.py\`; run it from the repo root.

This is a dry run. Workers run in the dry-run harness \`docs/dev-skills/harness.md\` documents: it has no \`worker-control\`
reference, so take its methods from that page through \`worker-control\`'s fallback, which needs no message to the user
here (its check has run: see the Startup verification result on the Milestone issue). Every tracker write and every
harness action is a block in \`.scratch/proposed-actions.md\`, as the tracker doc and the harness page say; make no
other change to the repo.

Your project instructions say: "Build threads: at most 3 at once. Tier map: the \`model-tiers\` default. Briefs also
link the repo. This project does not run the \`triage\` skill."

Events arrive one at a time, below, each with its UTC clock on 2026-11-03. For each event, in order: from event 2 on,
first run \`python3 .scratch/world.py <k>\` from the repo root (it moves the tracker, git and the harness to what they
show when the event arrives, and applies your earlier comment and label writes; it is not your write), then append
\`## Event <k>\` and the blocks the skill has you take. Ask the user nothing: no answers are scripted. A worker you
message answers only through a later event or the tracker.

TXT
  printf '%s\n' "$events" | awk -F'|' '{printf "- Event %s (%sZ): %s\n", $1, $2, $3}'
  echo
  echo "Stop after event $last."
  echo "---"
} > "$out/PROMPT.md"
echo "built $case_ in $out"
