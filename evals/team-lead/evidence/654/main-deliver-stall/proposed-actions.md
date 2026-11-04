## Event 1

### 1. Start a worker
Issue: 00-milestone.md
Skill: release
Tier: premium
Brief:
~~~
You are the Release worker for Milestone 1. Run the `release` skill at the premium tier (<model>, from the `model-tiers`
default map) to plan the Milestone's first Release.

- Repo: <runs>/main-deliver-stall/repo
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet)
- Release doc: docs/dev-skills/release.md
- Last release issue cut: none; this is the repo's first Release.
- Tracker: docs/dev-skills/issue-tracker.md (local Markdown, dry run: every write is a block in .scratch/proposed-actions.md).

Plan the next Release by `release`'s own rule. Where nothing qualifies, open no release issue, label nothing and say so.
Report back to the coordinator when the release issue is open and labelled, naming its file.

In your report on the issue, record the plugin load source and version you actually loaded, your permission and sandbox
settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 2. Comment on an issue
Issue: 00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900 · Skill: release · Model tier: premium · Review level: none · Started: 2026-11-03T09:00:00Z
Session: the dry-run harness's record for w-00-0900 (.scratch/harness/workers.md)
Release worker: plans Milestone 1's first Release; no build worker starts while it runs.
~~~

## Event 2

### 3. Arrange a check-in
Every: 1 hour
Into: coordinator

### 4. Comment on an issue
Issue: 00-milestone.md
Body:
~~~
<!-- team-lead check-in -->
Check-in arranged: every 1 hour (the Boundary record's interval), into the coordinator, at 2026-11-03T09:20:00Z,
before the first build worker starts. No earlier check-in was running (.scratch/harness/checkins.md was empty).
~~~

### 5. Start a worker
Issue: 10-farewell.md
Skill: implement-spec
Tier: regular
Brief:
~~~
Build the Spec .scratch/issues/10-farewell.md (Add a farewell command) as its Spec thread with the `implement-spec`
skill: its Tickets 11-bye-code.md and 12-bye-usage.md, then the Spec pull request, review and merge.

- Repo: <runs>/main-deliver-stall/repo
- Spec: .scratch/issues/10-farewell.md
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet); Release: .scratch/issues/40-release-m1-r1.md
- Model tier: regular (<model>, from the `model-tiers` default map). Review level: Deep (the Spec names it).
- Tracker: docs/dev-skills/issue-tracker.md; Boundary record: docs/dev-skills/boundaries.md; merge-time steps: CLAUDE.md.
  Ticket 11 changes `skills/greeting/SKILL.md`: just before merging, ask the coordinator for its version number.

In your report on the issue, record the plugin load source and version you actually loaded, your permission and sandbox
settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 6. Comment on an issue
Issue: 10-farewell.md
Body:
~~~
<!-- team-lead start -->
Worker: w-10-0920 · Skill: implement-spec · Model tier: regular · Review level: Deep · Started: 2026-11-03T09:20:00Z
Session: the dry-run harness's record for w-10-0920 (.scratch/harness/workers.md)
~~~

## Event 3

## Event 4

### 7. Message a worker
Worker: w-10-0920
Body:
~~~
Check-in at 2026-11-03T11:00:00Z: nothing from you on 10-farewell.md since your start at 09:20Z (no commit on t10, no
comment, no pull request), and the harness reads you idle since 09:40Z. Where are you, and what blocks you? Answer with
a comment on .scratch/issues/10-farewell.md, and push what you have.
~~~

### 8. Comment on an issue
Issue: 10-farewell.md
Body:
~~~
<!-- team-lead nudge -->
Worker w-10-0920 nudged at 2026-11-03T11:00:00Z: silent since its start at 2026-11-03T09:20:00Z (no commit on t10, no
comment, no pull request; harness state idle since 09:40Z). Asked where it is and what blocks it, answered here.
~~~

## Event 5

### 9. Stop a worker
Worker: w-10-0920

## Event 6

### 10. Apply / remove labels
Issue: 10-farewell.md
Add: parked
Remove: none

### 11. Comment on an issue
Issue: 10-farewell.md
Body:
~~~
<!-- team-lead parked -->
Parked at 2026-11-03T12:05:00Z: the stop of w-10-0920 does not read back. Its worker was silent since its start at
09:20Z, nudged at 11:00Z and still silent at the 12:00Z check-in, so a stop was asked at 12:00Z; at the harness's
12:05Z notice that the stop was taken, .scratch/harness/workers.md still reads
`w-10-0920 10-farewell.md branch t10: idle since 2026-11-03T09:40:00Z`, not `stopped`.
A writer may remain: w-10-0920 is not read back as stopped and could still push to t10, so no replacement starts.
Branch t10 holds no pushed commit; no pull request exists.
Records: start (2026-11-03T09:20:00Z comment above), nudge (2026-11-03T11:00:00Z comment above).
Lift by removing the `parked` label; before a fresh worker starts, w-10-0920 is stopped and read back first.
~~~

### 12. Message the user
Body:
~~~
Parked .scratch/issues/10-farewell.md (Add a farewell command): its worker w-10-0920 went silent, did not answer its
nudge, and the stop I asked for does not read back (the harness still reads it idle, not stopped), so it may still
write to t10. Remove the `parked` label to lift it; delivery goes on with 20-quiet.md.
~~~

### 13. Start a worker
Issue: 20-quiet.md
Skill: implement
Tier: regular
Brief:
~~~
Build the lone Ticket .scratch/issues/20-quiet.md (Add a --quiet flag) as its Ticket thread with the `implement`
skill: Implementer, pull request, review, merge.

- Repo: <runs>/main-deliver-stall/repo
- Ticket: .scratch/issues/20-quiet.md
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet); Release: .scratch/issues/40-release-m1-r1.md
- Model tier: regular (<model>, from the `model-tiers` default map).
- Tracker: docs/dev-skills/issue-tracker.md; Boundary record: docs/dev-skills/boundaries.md; merge-time steps: CLAUDE.md.
  If your pull request changes a file under `skills/`, ask the coordinator for its version number just before merging.

In your report on the issue, record the plugin load source and version you actually loaded, your permission and sandbox
settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 14. Comment on an issue
Issue: 20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1205 · Skill: implement · Model tier: regular · Review level: none · Started: 2026-11-03T12:05:00Z
Session: the dry-run harness's record for w-20-1205 (.scratch/harness/workers.md)
~~~

## Event 7

### 15. Start a worker
Issue: 20-quiet.md
Skill: implement
Tier: regular
Brief:
~~~
Build the lone Ticket .scratch/issues/20-quiet.md (Add a --quiet flag) as its Ticket thread with the `implement`
skill: Implementer, pull request, review, merge. You replace worker w-20-1205, which failed at 2026-11-03T12:28:00Z.

Resume from the pushed branch `t20` (its commit 58496e0 "quiet: the --quiet flag") and the tracker: the issue, its
comments and any pull request for `t20` under .scratch/pulls/. Keep what is pushed; do not start over from main.

- Repo: <runs>/main-deliver-stall/repo
- Ticket: .scratch/issues/20-quiet.md
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet); Release: .scratch/issues/40-release-m1-r1.md
- Model tier: regular (<model>, from the `model-tiers` default map).
- Tracker: docs/dev-skills/issue-tracker.md; Boundary record: docs/dev-skills/boundaries.md; merge-time steps: CLAUDE.md.
  If your pull request changes a file under `skills/`, ask the coordinator for its version number just before merging.

In your report on the issue, record the plugin load source and version you actually loaded, your permission and sandbox
settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 16. Comment on an issue
Issue: 20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1230 · Skill: implement · Model tier: regular · Review level: none · Started: 2026-11-03T12:30:00Z
Session: the dry-run harness's record for w-20-1230 (.scratch/harness/workers.md)
Takes over from w-20-1205; its end as read: `failed since 2026-11-03T12:28:00Z` in .scratch/harness/workers.md, at 2026-11-03T12:30:00Z.
Resumes from branch t20 (58496e0).
~~~

## Event 8

## Event 9

### 17. Message a worker
Worker: w-20-1230
Body:
~~~
Check-in at 2026-11-03T14:00:00Z: nothing from you on 20-quiet.md since your push of 13a4245 to t20 at 12:50Z (no
comment, no pull request), and the harness reads you idle since 12:51Z. Where are you, and what blocks you? Answer with
a comment on .scratch/issues/20-quiet.md, and push what you have.
~~~

### 18. Comment on an issue
Issue: 20-quiet.md
Body:
~~~
<!-- team-lead nudge -->
Worker w-20-1230 nudged at 2026-11-03T14:00:00Z: silent since its push of 13a4245 to t20 at 2026-11-03T12:50:00Z (no
comment, no pull request; harness state idle since 12:51Z). Asked where it is and what blocks it, answered here.
~~~

## Event 10

### 19. Stop a worker
Worker: w-20-1230

## Event 11

### 20. Apply / remove labels
Issue: 20-quiet.md
Add: parked
Remove: none

### 21. Comment on an issue
Issue: 20-quiet.md
Body:
~~~
<!-- team-lead parked -->
Parked at 2026-11-03T15:05:00Z: the feature's second stall. w-20-1205 failed at 12:28Z; its replacement w-20-1230,
started 12:30Z, went silent after pushing 13a4245 to t20 at 12:50Z, was nudged at 14:00Z and was still silent at the
15:00Z check-in. Its stop reads back: .scratch/harness/workers.md shows
`w-20-1230 20-quiet.md branch t20: stopped since 2026-11-03T15:03:00Z`.
No writer remains: w-20-1205 reads failed and w-20-1230 reads stopped.
Branch t20 holds 58496e0 and 13a4245; no pull request exists.
Records: start of w-20-1205 (2026-11-03T12:05:00Z comment above), start of w-20-1230 (2026-11-03T12:30:00Z comment
above), nudge (2026-11-03T14:00:00Z comment above).
Lift by removing the `parked` label; a fresh worker then resumes from t20.
~~~

### 22. Message the user
Body:
~~~
Parked .scratch/issues/20-quiet.md (Add a --quiet flag) after its second stall: w-20-1205 failed and its replacement
w-20-1230 went silent after pushing to t20 and was stopped (read back stopped at 15:03Z). With 10-farewell.md parked too,
nothing in Release 1 can start, so delivery waits on you to lift a park; 25-hello-doc.md waits for the next Release.
~~~

## Event 12

