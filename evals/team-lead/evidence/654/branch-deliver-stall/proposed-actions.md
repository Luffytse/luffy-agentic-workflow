## Event 1

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium (<model>, by the `model-tiers` default map)
Brief:
~~~
You are the Release worker for Milestone 1. Run the `release` skill to plan the next Release (there is none yet), at the premium tier.

- Repo: <runs>/branch-deliver-stall/repo
- Milestone issue: .scratch/issues/00-milestone.md (features and their order)
- Release doc: docs/dev-skills/release.md (Release name, label and bump mode)
- Last release issue cut: none; this is the Milestone's first Release.
- Tracker: docs/dev-skills/issue-tracker.md, in dry-run mode.

Plan the next Release by `release`'s own rule. Where an open release issue for this Milestone holds no issue yet, fill that one instead of opening another (for that issue this overrides `release`'s "Rerun first"). Where nothing qualifies, open no release issue, label nothing and say so. Plan only: build nothing.

In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" for any you cannot read. Report to the coordinator when the release issue is written.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900
Skill: release (plans Milestone 1's first Release only)
Model tier: premium
Review level: none
Started: 2026-11-03T09:00:00Z
Session reference: dry-run harness record, .scratch/harness/workers.md line for w-00-0900
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
Check-in arranged: every 1 hour (the Boundary record's interval), into the coordinator, at 2026-11-03T09:20:00Z, before the first build worker starts. None ran before (.scratch/harness/checkins.md was empty).
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular (<model>, by the `model-tiers` default map)
Brief:
~~~
Build the Spec .scratch/issues/10-farewell.md (Add a farewell command) as its Spec thread with the `implement-spec` skill: its Tickets 11-bye-code.md and 12-bye-usage.md, then the Spec pull request, its review and the merge.

- Repo: <runs>/branch-deliver-stall/repo
- Spec issue: .scratch/issues/10-farewell.md
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; Release: .scratch/issues/40-release-m1-r1.md)
- Model tier: regular
- Review level: Deep (the Spec names it)
- Tracker: docs/dev-skills/issue-tracker.md. Boundaries: docs/dev-skills/boundaries.md. Merge-time steps: CLAUDE.md, "Merge-time steps" (ask the coordinator for the version number just before merging a pull request that changes a file under skills/).

In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" for any you cannot read.
~~~

### 6. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead start -->
Worker: w-10-0920
Skill: implement-spec
Model tier: regular
Review level: Deep
Started: 2026-11-03T09:20:00Z
Session reference: dry-run harness record, .scratch/harness/workers.md line for w-10-0920
~~~

## Event 3

## Event 4

### 7. Message a worker
Worker: w-10-0920
Body:
~~~
Check-in at 2026-11-03T11:00Z: nothing has reached the tracker or branch t10 from you since your start at 09:20Z, and the Harness reads you idle since 09:40Z. Where are you on .scratch/issues/10-farewell.md, and what blocks you? Answer with a comment on .scratch/issues/10-farewell.md, then carry on with the Spec.
~~~

### 8. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-10-0920 at 2026-11-03T11:00:00Z: the check-in snapshot read it silent since its start at 09:20Z (no commit on t10, no comment, no pull request; Harness state idle since 09:40Z). Asked where it is and what blocks it, answered by a comment here.
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
Parked at 2026-11-03T12:05:00Z: worker w-10-0920 stalled and its stop does not read back. It was nudged at 11:00Z and was still silent at the 12:00Z check-in; the stop was asked at 12:00Z and the Harness reports it taken, but .scratch/harness/workers.md still reads `w-10-0920 10-farewell.md branch t10: idle since 2026-11-03T09:40:00Z`, not `stopped`.
A writer may remain: w-10-0920 has not read back stopped and could still push to branch t10 (nothing is pushed there yet). Before any fresh worker starts here, its state is read again and it is stopped and read back first.
Start record: the `<!-- team-lead start -->` comment of 2026-11-03T09:20:00Z on this issue. Nudge record: the `<!-- team-lead nudge -->` comment of 2026-11-03T11:00:00Z on this issue. Pull request: none opened.
Tickets 11-bye-code.md and 12-bye-usage.md are this Spec's and wait with it. Remove the `parked` label to lift the park.
~~~

### 12. Message the user
Body:
~~~
Parked .scratch/issues/10-farewell.md (farewell Spec): its worker w-10-0920 went silent, a nudge got no answer, and the stop I asked for does not read back (the Harness still reads it idle, not stopped), so it may still write to branch t10; see the parked comment there. Delivery goes on with 20-quiet.md; remove the `parked` label to lift it.
~~~

### 13. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (<model>, by the `model-tiers` default map)
Brief:
~~~
Build the lone Ticket .scratch/issues/20-quiet.md (Add a --quiet flag) as its Ticket thread with the `implement` skill: Implementer, pull request, review, merge.

- Repo: <runs>/branch-deliver-stall/repo
- Ticket: .scratch/issues/20-quiet.md
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; Release: .scratch/issues/40-release-m1-r1.md)
- Model tier: regular
- Tracker: docs/dev-skills/issue-tracker.md. Boundaries: docs/dev-skills/boundaries.md. Merge-time steps: CLAUDE.md, "Merge-time steps" (ask the coordinator for the version number just before merging a pull request that changes a file under skills/).

In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" for any you cannot read.
~~~

### 14. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1205
Skill: implement
Model tier: regular
Review level: none
Started: 2026-11-03T12:05:00Z
Session reference: dry-run harness record, .scratch/harness/workers.md line for w-20-1205
~~~

## Event 7

### 15. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (<model>, by the `model-tiers` default map)
Brief:
~~~
Build the lone Ticket .scratch/issues/20-quiet.md (Add a --quiet flag) as its Ticket thread with the `implement` skill: Implementer, pull request, review, merge. You take over from worker w-20-1205, which failed at 2026-11-03T12:28Z.

- Resume from the pushed branch t20 (its commit 58496e0 "quiet: the --quiet flag") and the tracker: the issue, its comments and any pull request for t20. Keep what is pushed; do not start over.
- Repo: <runs>/branch-deliver-stall/repo
- Ticket: .scratch/issues/20-quiet.md
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; Release: .scratch/issues/40-release-m1-r1.md)
- Model tier: regular
- Tracker: docs/dev-skills/issue-tracker.md. Boundaries: docs/dev-skills/boundaries.md. Merge-time steps: CLAUDE.md, "Merge-time steps" (ask the coordinator for the version number just before merging a pull request that changes a file under skills/).

In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" for any you cannot read.
~~~

### 16. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1230
Skill: implement
Model tier: regular
Review level: none
Started: 2026-11-03T12:30:00Z
Session reference: dry-run harness record, .scratch/harness/workers.md line for w-20-1230
Takes over from w-20-1205; its end as read: `failed since 2026-11-03T12:28:00Z` in .scratch/harness/workers.md, at 2026-11-03T12:30:00Z. Resumes from branch t20 (58496e0).
~~~

## Event 8

## Event 9

### 17. Message a worker
Worker: w-20-1230
Body:
~~~
Check-in at 2026-11-03T14:00Z: your last activity was the push to t20 at 12:50Z ("quiet: keep the exit code"); nothing since, no pull request, and the Harness reads you idle since 12:51Z. Where are you on .scratch/issues/20-quiet.md, and what blocks you? Answer with a comment on .scratch/issues/20-quiet.md, then carry on.
~~~

### 18. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-20-1230 at 2026-11-03T14:00:00Z: the check-in snapshot read it silent since its last push to t20 at 12:50Z (no comment, no pull request; Harness state idle since 12:51Z). Asked where it is and what blocks it, answered by a comment here.
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
Parked at 2026-11-03T15:05:00Z: the feature's second stall. The first worker, w-20-1205, failed at 12:28Z (an end without its result, counted as a stall); its replacement w-20-1230 pushed 13a4245 to t20 at 12:50Z, then went silent, was nudged at 14:00Z and was still silent at the 15:00Z check-in. It was stopped, and the stop reads back: `w-20-1230 20-quiet.md branch t20: stopped since 2026-11-03T15:03:00Z` in .scratch/harness/workers.md.
No writer remains: w-20-1205 reads failed and w-20-1230 reads stopped. Branch t20 keeps the pushed work (58496e0, 13a4245).
Start records: the `<!-- team-lead start -->` comments of 2026-11-03T12:05:00Z (w-20-1205) and 2026-11-03T12:30:00Z (w-20-1230) on this issue. Nudge record: the `<!-- team-lead nudge -->` comment of 2026-11-03T14:00:00Z on this issue. Pull request: none opened for t20.
Remove the `parked` label to lift the park.
~~~

### 22. Message the user
Body:
~~~
Parked .scratch/issues/20-quiet.md (--quiet flag): its first worker failed and its replacement went silent after pushing to t20, so this is its second stall; the stop read back, no writer remains, and the work is kept on branch t20 (see the parked comment there). With 10-farewell.md also parked, delivery now has nothing to start: Release 1's open work is all parked, and 25-hello-doc.md waits on 35-readme-tool.md (outside the Milestone) and on the next Release. Remove a `parked` label to lift a park.
~~~

## Event 12
