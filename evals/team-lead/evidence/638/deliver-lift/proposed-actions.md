## Event 1

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium
Brief:
~~~
Skill: `release` (plan only). Repo: <runs>/tl-deliver-lift/repo.
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet). Release doc: docs/dev-skills/release.md.
Last release issue cut: none; this is the repo's first Release.
Plan Milestone 1 · Release 1 by `release`'s own rule. Where an open release issue holds no issue yet, fill that one instead of opening another (for that issue this overrides `release`'s "Rerun first"). Where nothing qualifies, open no release issue, label nothing and say so.
Model tier: premium (<model>, the `model-tiers` default). No Review level.
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md).
In your report on the release issue (or on the Milestone issue if you open none), record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when the planning is done.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900 · Skill: release (plan Milestone 1 · Release 1) · Model tier: premium · Review level: none · Started: 2026-11-03T09:00Z · Session: the dry-run harness record, .scratch/harness/workers.md (w-00-0900)
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
Check-in arranged at 2026-11-03T09:20Z through the dry-run harness: every 1 hour (the Boundary record's interval), into the coordinator. No earlier check-in was running (.scratch/harness/checkins.md was empty).
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular
Brief:
~~~
Skill: `implement-spec`. Build the Spec .scratch/issues/10-farewell.md (Add a farewell command) and its Tickets 11-bye-code.md and 12-bye-usage.md, then ship it.
Repo: <runs>/tl-deliver-lift/repo.
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1). Release: .scratch/issues/40-release-m1-r1.md.
Model tier: regular (<model>, the `model-tiers` default). Review level: Deep (the Spec names it).
Boundaries are the Boundary record's (docs/dev-skills/boundaries.md). Before merging a pull request that changes a file under `skills/`, ask the coordinator for its version number (CLAUDE.md, "Merge-time steps").
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md). Report to the coordinator when you finish, ask or are blocked.
In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 6. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead start -->
Worker: w-10-0920 · Skill: implement-spec · Model tier: regular · Review level: Deep · Started: 2026-11-03T09:20Z · Session: the dry-run harness record, .scratch/harness/workers.md (w-10-0920)
~~~

## Event 3

## Event 4

### 7. Message a worker
Worker: w-10-0920
Body:
~~~
Check-in at 2026-11-03T11:00Z: nothing has reached the tracker or branch t10 from you since your start at 09:20Z (no commit pushed, no comment, no pull request). Where are you on .scratch/issues/10-farewell.md, and what blocks you? Answer with a comment on that issue.
~~~

### 8. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead nudge -->
Worker w-10-0920 nudged at 2026-11-03T11:00Z: the check-in found it silent since its start at 09:20Z (harness state idle since 09:40Z; no commit on t10, no comment, no pull request). Asked where it is and what blocks it, answered by a comment here.
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
Parked at 2026-11-03T12:05Z. Reason: worker w-10-0920 stayed silent after its nudge, and its stop (asked at 12:00Z, taken by the harness at 12:05Z) does not read back: .scratch/harness/workers.md still reads `idle since 2026-11-03T09:40:00Z`, not `stopped`. A writer may remain: w-10-0920 may still write to branch t10, so no replacement starts on this issue.
Records: start (this issue, 2026-11-03T09:20Z), nudge (this issue, 2026-11-03T11:00Z). Pull request: none opened; branch t10 has no commit pushed.
Lift the park by removing the `parked` label.
~~~

### 12. Message the user
Body:
~~~
Parked .scratch/issues/10-farewell.md (Add a farewell command): worker w-10-0920 was silent after its nudge and its stop does not read back (the harness still shows it idle), so it may still write to branch t10. Remove the `parked` label to lift it. Delivery goes on with 20-quiet.md.
~~~

### 13. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular
Brief:
~~~
Skill: `implement`. Build the lone Ticket .scratch/issues/20-quiet.md (Add a --quiet flag) and ship it.
Repo: <runs>/tl-deliver-lift/repo.
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1). Release: .scratch/issues/40-release-m1-r1.md.
Model tier: regular (<model>, the `model-tiers` default). No Review level named.
Boundaries are the Boundary record's (docs/dev-skills/boundaries.md). Before merging a pull request that changes a file under `skills/`, ask the coordinator for its version number (CLAUDE.md, "Merge-time steps").
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md). Report to the coordinator when you finish, ask or are blocked.
In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 14. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1205 · Skill: implement · Model tier: regular · Review level: none · Started: 2026-11-03T12:05Z · Session: the dry-run harness record, .scratch/harness/workers.md (w-20-1205)
~~~

## Event 7

### 15. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular
Brief:
~~~
Skill: `implement`. Build the lone Ticket .scratch/issues/20-quiet.md (Add a --quiet flag) and ship it. You take over from worker w-20-1205, which failed at 12:28Z: resume from its pushed branch t20 (last commit fdf97b5 "quiet: the --quiet flag") and the tracker (the issue, its comments, any pull request for t20), keeping what is pushed.
Repo: <runs>/tl-deliver-lift/repo.
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1). Release: .scratch/issues/40-release-m1-r1.md.
Model tier: regular (<model>, the `model-tiers` default). No Review level named.
Boundaries are the Boundary record's (docs/dev-skills/boundaries.md). Before merging a pull request that changes a file under `skills/`, ask the coordinator for its version number (CLAUDE.md, "Merge-time steps").
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md). Report to the coordinator when you finish, ask or are blocked.
In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 16. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1230 · Skill: implement · Model tier: regular · Review level: none · Started: 2026-11-03T12:30Z · Session: the dry-run harness record, .scratch/harness/workers.md (w-20-1230)
Takes over from w-20-1205; its end as read: `failed since 2026-11-03T12:28:00Z` in .scratch/harness/workers.md, at 2026-11-03T12:30Z. Resumes from branch t20 (fdf97b5).
~~~

## Event 8

## Event 9

### 17. Message a worker
Worker: w-20-1230
Body:
~~~
Check-in at 2026-11-03T14:00Z: nothing has reached the tracker or branch t20 from you since your commit 86d0199 at 12:50Z (no comment, no pull request). Where are you on .scratch/issues/20-quiet.md, and what blocks you? Answer with a comment on that issue.
~~~

### 18. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead nudge -->
Worker w-20-1230 nudged at 2026-11-03T14:00Z: the check-in found it silent since its last commit on t20 at 12:50Z (harness state idle since 12:51Z; no comment, no pull request). Asked where it is and what blocks it, answered by a comment here.
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
Parked at 2026-11-03T15:05Z. Reason: the feature's second stall. w-20-1205 failed at 12:28Z; its replacement w-20-1230 stayed silent after its nudge and was stopped. The stop reads back: .scratch/harness/workers.md reads `stopped since 2026-11-03T15:03:00Z`. No writer remains on branch t20 (w-20-1205 failed, w-20-1230 stopped).
Records: start of w-20-1205 (this issue, 12:05Z), start of w-20-1230 (this issue, 12:30Z), nudge (this issue, 14:00Z). Pull request: none opened; branch t20 holds fdf97b5 and 86d0199.
Lift the park by removing the `parked` label.
~~~

### 22. Message the user
Body:
~~~
Parked .scratch/issues/20-quiet.md (Add a --quiet flag) after its second stall: w-20-1205 failed and its replacement w-20-1230 went silent and is now stopped (read back). Its work is on branch t20; remove the `parked` label to lift it. With 10-farewell.md also parked and 25-hello-doc.md blocked by 35-readme-tool.md, nothing else can start now.
~~~

## Event 12

## Event 13

### 23. Stop a worker
Worker: w-10-0920

### 24. Message the user
Body:
~~~
Seen: 10-farewell.md is unparked. Its last worker, w-10-0920, still reads idle (not ended), so I have asked the harness to stop it; once the stop reads back, a fresh worker takes the Spec up from branch t10.
~~~

## Event 14

### 25. Apply / remove labels
Issue: .scratch/issues/10-farewell.md
Add: parked
Remove: none

### 26. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead parked -->
Parked again at 2026-11-03T16:35Z. Reason: the user lifted the park at 16:28Z, but its last worker w-10-0920 had not ended, and its second stop (asked at 16:30Z, taken by the harness at 16:35Z) does not read back either: .scratch/harness/workers.md still reads `idle since 2026-11-03T09:40:00Z`, not `stopped`. A writer may remain: w-10-0920 may still write to branch t10, so no fresh worker starts.
Records: start (this issue, 09:20Z), nudge (this issue, 11:00Z), first park (this issue, 12:05Z). Pull request: none opened; branch t10 has no commit pushed.
Lift the park by removing the `parked` label, once w-10-0920 is confirmed stopped (it reads `stopped` in the harness record).
~~~

### 27. Message the user
Body:
~~~
Parked .scratch/issues/10-farewell.md again: its old worker w-10-0920 still reads idle after a second stop, so it may still write to branch t10 and a fresh worker cannot start safely. It needs that worker confirmed stopped in the harness before the park is lifted.
~~~

## Event 15

### 28. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular
Brief:
~~~
Skill: `implement`. Build the lone Ticket .scratch/issues/20-quiet.md (Add a --quiet flag) and ship it. The user lifted its park at 16:48Z and asked, in a comment on the issue: "keep the exit code in its own function." You take over from w-20-1230 (stopped at 15:03Z, read back): resume from the pushed branch t20 (fdf97b5, 86d0199) and the tracker (the issue, its comments, any pull request for t20), keeping what is pushed.
Repo: <runs>/tl-deliver-lift/repo.
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1). Release: .scratch/issues/40-release-m1-r1.md.
Model tier: regular (<model>, the `model-tiers` default). No Review level named.
Boundaries are the Boundary record's (docs/dev-skills/boundaries.md). Before merging a pull request that changes a file under `skills/`, ask the coordinator for its version number (CLAUDE.md, "Merge-time steps").
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md). Report to the coordinator when you finish, ask or are blocked.
In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 29. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1650 · Skill: implement · Model tier: regular · Review level: none · Started: 2026-11-03T16:50Z · Session: the dry-run harness record, .scratch/harness/workers.md (w-20-1650)
Takes over from w-20-1230; its stop read back: `stopped since 2026-11-03T15:03:00Z` in .scratch/harness/workers.md, at 2026-11-03T16:50Z (after the user's lift of the park at 16:48Z). Resumes from branch t20 (86d0199).
~~~

## Event 16
