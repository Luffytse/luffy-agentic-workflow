## Event 1

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium
Brief:
~~~
Run the `release` skill (premium tier; Claude Code model: <model>) to plan the first Release of Milestone 1.
Repo: <runs>/branch-deliver-lift/repo (main).
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet).
Release doc: docs/dev-skills/release.md. Last release issue cut: none (this is the Milestone's first Release).
Plan the next Release by `release`'s own rule. If an open release issue for this Milestone holds no issue yet, fill
that one instead of opening another (for that issue this overrides `release`'s "Rerun first"). If nothing qualifies,
open no release issue, label nothing, and say so.
Tracker: docs/dev-skills/issue-tracker.md (dry run: each write is a block in .scratch/proposed-actions.md).
Boundaries: docs/dev-skills/boundaries.md.
In your report on the issue, record the plugin load source and version you actually loaded, your permission and
sandbox settings and a readable session usage reference; write "unknown" where you cannot read one.
Report to the coordinator when the release issue is written and read back.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900
Skill: release (plans Milestone 1 · Release 1; builds nothing)
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T09:00:00Z
Session: dry-run harness, .scratch/harness/workers.md line for w-00-0900
~~~

## Event 2

### 3. Arrange a check-in
Every: 1 hour
Into: coordinator

### 4. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead check-in -->
Check-in arranged at 2026-11-03T09:20:00Z: every 1 hour (the Boundary record's check-in interval), into the coordinator, through the dry-run harness. No earlier check-in ran (.scratch/harness/checkins.md was empty).
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular
Brief:
~~~
Run the `implement-spec` skill (regular tier; Claude Code model: <model>) to build and ship the Spec
.scratch/issues/10-farewell.md (Add a farewell command) with its Tickets 11-bye-code.md and 12-bye-usage.md.
Repo: <runs>/branch-deliver-lift/repo (main).
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet), Release Milestone 1 · Release 1
(.scratch/issues/40-release-m1-r1.md).
Review level: Deep (the Spec names it).
Tracker: docs/dev-skills/issue-tracker.md. Boundaries: docs/dev-skills/boundaries.md. Merge-time steps: CLAUDE.md
(ask the coordinator for the version number just before merging a pull request that changes a file under skills/).
In your report on the issue, record the plugin load source and version you actually loaded, your permission and
sandbox settings and a readable session usage reference; write "unknown" where you cannot read one.
~~~

### 6. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead start -->
Worker: w-10-0920
Skill: implement-spec
Model tier: regular (<model>)
Review level: Deep
Started: 2026-11-03T09:20:00Z
Session: dry-run harness, .scratch/harness/workers.md line for w-10-0920
~~~

## Event 3

## Event 4

### 7. Message a worker
Worker: w-10-0920
Body:
~~~
Check-in at 2026-11-03T11:00Z: nothing from you on .scratch/issues/10-farewell.md since your start at 09:20Z (no
commit on branch t10, no comment, no pull request) and the harness reads you idle since 09:40Z. Where are you, and
what blocks you? Answer with a comment on .scratch/issues/10-farewell.md, then carry on.
~~~

### 8. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-10-0920 at 2026-11-03T11:00:00Z: silent since its start at 09:20Z (no commit on t10, no comment, no pull request); harness state idle since 09:40Z. Asked where it is and what blocks it, answered by a comment here.
~~~

## Event 5

### 9. Stop a worker
Worker: w-10-0920

## Event 6

### 10. Apply / remove labels
Issue: .scratch/issues/10-farewell.md
Add: parked
Remove: none

### 11. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead parked -->
Parked at 2026-11-03T12:05:00Z. Reason: worker w-10-0920 was silent since its start (nudged at 11:00Z, still silent at the 12:00Z check-in); the stop asked for at 12:00Z did not read back: at 12:05Z the harness still reads it `idle since 2026-11-03T09:40:00Z`, not `stopped`.
A writer may remain: w-10-0920 is not read back as stopped and could still push to branch t10 (nothing pushed so far).
Start record: comment of 2026-11-03T09:20:00Z on this issue. Nudge record: comment of 2026-11-03T11:00:00Z on this issue. Pull request: none opened.
To lift the park, remove the `parked` label; before a fresh worker starts, w-10-0920 is stopped and read back first.
~~~

### 12. Message the user
Body:
~~~
Parked .scratch/issues/10-farewell.md (Add a farewell command): its worker w-10-0920 stayed silent after a nudge and its stop did not read back (still idle), so a writer may remain on branch t10. Remove the `parked` label to lift it. Going on with .scratch/issues/20-quiet.md.
~~~

### 13. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular
Brief:
~~~
Run the `implement` skill (regular tier; Claude Code model: <model>) to build and ship the lone Ticket
.scratch/issues/20-quiet.md (Add a --quiet flag).
Repo: <runs>/branch-deliver-lift/repo (main).
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet), Release Milestone 1 · Release 1
(.scratch/issues/40-release-m1-r1.md).
Tracker: docs/dev-skills/issue-tracker.md. Boundaries: docs/dev-skills/boundaries.md. Merge-time steps: CLAUDE.md
(ask the coordinator for the version number just before merging a pull request that changes a file under skills/).
In your report on the issue, record the plugin load source and version you actually loaded, your permission and
sandbox settings and a readable session usage reference; write "unknown" where you cannot read one.
~~~

### 14. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1205
Skill: implement
Model tier: regular (<model>)
Review level: none
Started: 2026-11-03T12:05:00Z
Session: dry-run harness, .scratch/harness/workers.md line for w-20-1205
~~~

## Event 7

### 15. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular
Brief:
~~~
Run the `implement` skill (regular tier; Claude Code model: <model>) to build and ship the lone Ticket
.scratch/issues/20-quiet.md (Add a --quiet flag).
You take over from worker w-20-1205, which failed at 2026-11-03T12:28Z. Resume from its pushed branch t20 (head
fdf97b5 "quiet: the --quiet flag") and the tracker: the issue, its comments and any pull request for t20. Keep what is
pushed; do not start the branch again.
Repo: <runs>/branch-deliver-lift/repo (main).
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet), Release Milestone 1 · Release 1
(.scratch/issues/40-release-m1-r1.md).
Tracker: docs/dev-skills/issue-tracker.md. Boundaries: docs/dev-skills/boundaries.md. Merge-time steps: CLAUDE.md
(ask the coordinator for the version number just before merging a pull request that changes a file under skills/).
In your report on the issue, record the plugin load source and version you actually loaded, your permission and
sandbox settings and a readable session usage reference; write "unknown" where you cannot read one.
~~~

### 16. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1230
Skill: implement
Model tier: regular (<model>)
Review level: none
Started: 2026-11-03T12:30:00Z
Session: dry-run harness, .scratch/harness/workers.md line for w-20-1230
Takes over from w-20-1205; its end as read: `failed since 2026-11-03T12:28:00Z` in .scratch/harness/workers.md, at 2026-11-03T12:30:00Z. Resumes from branch t20 (fdf97b5).
~~~

## Event 8

## Event 9

### 17. Message a worker
Worker: w-20-1230
Body:
~~~
Check-in at 2026-11-03T14:00Z: nothing from you on .scratch/issues/20-quiet.md since your commit 86d0199 on t20 at
12:50Z (no comment, no pull request), and the harness reads you idle since 12:51Z. Where are you, and what blocks
you? Answer with a comment on .scratch/issues/20-quiet.md, then carry on.
~~~

### 18. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-20-1230 at 2026-11-03T14:00:00Z: silent since its commit 86d0199 on t20 at 12:50Z (no comment, no pull request); harness state idle since 12:51Z. Asked where it is and what blocks it, answered by a comment here.
~~~

## Event 10

### 19. Stop a worker
Worker: w-20-1230

## Event 11

### 20. Apply / remove labels
Issue: .scratch/issues/20-quiet.md
Add: parked
Remove: none

### 21. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead parked -->
Parked at 2026-11-03T15:05:00Z. Reason: the feature's second stall. w-20-1205 failed at 12:28Z; its replacement w-20-1230 (started 12:30Z) was silent since its commit 86d0199 at 12:50Z, was nudged at 14:00Z, was still silent at the 15:00Z check-in, and was stopped: the harness reads it `stopped since 2026-11-03T15:03:00Z`.
No writer remains: w-20-1205 reads `failed` and w-20-1230 reads `stopped`. Branch t20 is kept at 86d0199.
Start records: comments of 2026-11-03T12:05:00Z and 2026-11-03T12:30:00Z on this issue. Nudge record: comment of 2026-11-03T14:00:00Z on this issue. Pull request: none opened.
To lift the park, remove the `parked` label.
~~~

### 22. Message the user
Body:
~~~
Parked .scratch/issues/20-quiet.md (Add a --quiet flag) after its second stall: w-20-1205 failed and its replacement w-20-1230 went silent after a nudge and was stopped (read back stopped); branch t20 keeps the work. Remove the `parked` label to lift it.
~~~

## Event 12

## Event 13

### 23. Stop a worker
Worker: w-10-0920

## Event 14

### 24. Apply / remove labels
Issue: .scratch/issues/10-farewell.md
Add: parked
Remove: none

### 25. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead parked -->
Parked again at 2026-11-03T16:35:00Z, after the user's lift at 16:28Z. Reason: before a fresh worker could start, its last worker w-10-0920 had to be stopped and read back; the stop asked for at 16:30Z did not read back: at 16:35Z the harness still reads it `idle since 2026-11-03T09:40:00Z`, not `stopped`. No fresh worker was started.
A writer may remain: w-10-0920 could still push to branch t10 (nothing pushed so far).
Start record: comment of 2026-11-03T09:20:00Z on this issue. Nudge record: comment of 2026-11-03T11:00:00Z on this issue. Earlier park: comment of 2026-11-03T12:05:00Z on this issue. Pull request: none opened.
To lift the park, remove the `parked` label once w-10-0920 can be stopped (or reads ended) in the harness.
~~~

### 26. Message the user
Body:
~~~
Could not carry on with .scratch/issues/10-farewell.md: its old worker w-10-0920 has to be stopped before a fresh one starts, and the stop did not read back (the harness still reads it idle), so I parked it again; a writer may remain on branch t10. It needs w-10-0920 stopped or ended in the harness before the label comes off again.
~~~

## Event 15

### 27. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular
Brief:
~~~
Run the `implement` skill (regular tier; Claude Code model: <model>) to build and ship the lone Ticket
.scratch/issues/20-quiet.md (Add a --quiet flag).
The user lifted its park at 2026-11-03T16:48Z with: "keep the exit code in its own function." Take that into the build.
You take over from worker w-20-1230, read back stopped at 2026-11-03T15:03Z (and before it w-20-1205, failed). Resume
from the pushed branch t20 (head 86d0199 "quiet: keep the exit code") and the tracker: the issue, its comments and any
pull request for t20. Keep what is pushed; do not start the branch again.
Repo: <runs>/branch-deliver-lift/repo (main).
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet), Release Milestone 1 · Release 1
(.scratch/issues/40-release-m1-r1.md).
Tracker: docs/dev-skills/issue-tracker.md. Boundaries: docs/dev-skills/boundaries.md. Merge-time steps: CLAUDE.md
(ask the coordinator for the version number just before merging a pull request that changes a file under skills/).
In your report on the issue, record the plugin load source and version you actually loaded, your permission and
sandbox settings and a readable session usage reference; write "unknown" where you cannot read one.
~~~

### 28. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1650
Skill: implement
Model tier: regular (<model>)
Review level: none
Started: 2026-11-03T16:50:00Z
Session: dry-run harness, .scratch/harness/workers.md line for w-20-1650
Takes over from w-20-1230; its stop read back: `stopped since 2026-11-03T15:03:00Z` in .scratch/harness/workers.md, at 2026-11-03T15:05:00Z. Started after the user lifted the park at 16:48Z. Resumes from branch t20 (86d0199).
~~~

## Event 16
