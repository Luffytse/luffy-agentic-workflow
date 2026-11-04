## Event 1

Wake 09:00Z: delivery starts. Read: Milestone 1 (`00-milestone.md`) open, planning settled, latest Startup verification reads `Verdict: ready` (Runtime: dry-run harness, this one). `worker-control`: no reference for this Harness; methods taken through its fallback from `docs/dev-skills/harness.md` (start, state via `workers.md`, wake on end/failure, message, stop + read-back, check-in; no pause of its own: pause by message). `workers.md` and `checkins.md` empty: no worker or check-in runs. No release issue exists, no issue carries a release label, and planned features 10-farewell (unblocked) and 20-quiet (unblocked) qualify, so a Release worker plans Release 1 first. No build worker starts, so no check-in is arranged yet. Tier: `release` names premium; the `model-tiers` default maps premium to <model> (Claude Code).

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium (<model>)
Brief:
~~~
Run the `release` skill (plugins/dev-skills/skills/release/SKILL.md, from the checkout's main) for this repo: <runs>/main-deliver-lift/repo.
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet).
Release doc: docs/dev-skills/release.md. Tracker doc: docs/dev-skills/issue-tracker.md (dry run: every write is a block in .scratch/proposed-actions.md).
Last release issue cut: none; this is the repo's first Release.
Task: plan the next Release (Milestone 1 · Release 1) by `release`'s own rule. Where an open release issue holds no issue yet, fill that one instead of opening another (for that issue this overrides `release`'s "Rerun first"). Where nothing qualifies, open no release issue, label nothing and say so.
Model tier: premium.
In your report on the release issue (or on the Milestone issue if you open none), record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference; write "unknown" where you cannot read one. Report back to the coordinator when done.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900 (id as the harness returns it: issue file 00, event clock 09:00)
Skill: release (plans Milestone 1 · Release 1)
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T09:00:00Z
Session: none readable (the dry-run harness gives no session reference; its record is .scratch/harness/workers.md)
~~~

## Event 2

Wake 09:20Z: w-00-0900 reports. Read: `workers.md` reads w-00-0900 `ended` since 09:19Z. Release issue `40-release-m1-r1.md` read back: open, `**Milestone:** 00-milestone.md`, written before an Order list; its label `release-m1-r1` is on 10-farewell (with Tickets 11, 12) and 20-quiet; 25-hello-doc carries none (blocked by 35-readme-tool, outside the Milestone). Current Release: Milestone 1 · Release 1. Build order (no Order list: maintenance fixes, none; then features in the Milestone issue's order): 10-farewell, then 20-quiet. Slots: smaller of the project's 3 and "one at a time" = 1. Milestone review gate: not held (10, 20, 25 open, unparked). No pause in effect. No PRs, no branches besides main. First build worker starts at this wake, so the check-in is arranged first: `checkins.md` lists none running, so arrange one at the Boundary record's 1 hour. 10-farewell is a Spec with Tickets: `implement-spec`, tier regular (<model>), Review level Deep (the issue names it).

### 3. Arrange a check-in
Every: 1 hour
Into: coordinator

### 4. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead check-in -->
Check-in arranged at 2026-11-03T09:20:00Z: every 1 hour (the Boundary record's interval), into the coordinator, through the dry-run harness (`Arrange a check-in`; listed in .scratch/harness/checkins.md). None was running before.
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular (<model>)
Brief:
~~~
Run the `implement-spec` skill (plugins/dev-skills/skills/implement-spec/SKILL.md, from the checkout's main) as this Spec's Spec thread.
Repo: <runs>/main-deliver-lift/repo
Spec: .scratch/issues/10-farewell.md (Add a farewell command), Tickets .scratch/issues/11-bye-code.md and .scratch/issues/12-bye-usage.md.
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet). Release: .scratch/issues/40-release-m1-r1.md.
Model tier: regular. Review level: Deep (named by the Spec).
Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md (dry run). Merge-time steps: CLAUDE.md, "Merge-time steps" (a pull request changing a file under skills/ asks the coordinator for its version number just before merging).
In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when you finish, ask, or are blocked.
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
Session: none readable (the dry-run harness gives no session reference; its record is .scratch/harness/workers.md)
~~~

## Event 3

Check-in 10:00Z. Read: no pause; release-m1-r1 open; 10-farewell, 20-quiet, 25-hello-doc open, none parked; w-10-0920 `working` since 09:20Z, branch t10 not pushed, no PR. Snapshot (`--now 2026-11-03T10:00:00Z --silent-after 60`): w-10-0920 active. Milestone review gate not held. Slot taken (one at a time). Quiet check-in: nothing written, no one told.

## Event 4

Check-in 11:00Z. Read: no pause; tracker unchanged (10, 20, 25 open, none parked); w-10-0920 `idle` since 09:40Z (idle is not ended), branch t10 not pushed, no PR, no comment from it on 10, 11 or 12. Snapshot (`--now 2026-11-03T11:00:00Z --silent-after 60`): w-10-0920 silent since 09:20Z, not nudged before. Nudge it once. Milestone review gate not held; slot still taken.

### 7. Message a worker
Worker: w-10-0920
Body:
~~~
Check-in 11:00Z: nothing has reached the tracker or a branch from you since your start at 09:20Z (no push to t10, no pull request, no comment). Where are you on the Spec 10-farewell, and what blocks you? Answer with a comment on .scratch/issues/10-farewell.md, and push what you have.
~~~

### 8. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead nudge -->
Worker w-10-0920 nudged at 2026-11-03T11:00:00Z: silent since its start at 09:20Z (no commit on t10, no comment, no pull request); harness state `idle` since 09:40Z. Asked where it is and what blocks it, answered by a comment on this issue.
~~~

## Event 5

Check-in 12:00Z. Read: no pause; tracker unchanged apart from my nudge record; w-10-0920 still `idle` since 09:40Z, t10 not pushed, no PR, no answer to the 11:00Z nudge. Snapshot (`--now 2026-11-03T12:00:00Z --silent-after 60`): still silent after its nudge. Replace a stalled worker, step 2: stop it through the harness and read the stop back when the harness says it was taken. Nothing starts on 10-farewell until the stop reads back; the slot stays held.

### 9. Stop a worker
Worker: w-10-0920

## Event 6

Wake 12:05Z: the harness says the stop of w-10-0920 was taken. Read the stop back: `workers.md` still reads w-10-0920 `idle` since 09:40Z, not `stopped`, so the stop did not read back (only `stopped` is a stop). Replace a stalled worker, step 4: park 10-farewell instead of starting a replacement; a writer (w-10-0920) may remain on branch t10. Tell the user once. Then go on with other work: under one at a time the next feature may start once each one before it is closed or parked; 10-farewell is now parked, and the stalled worker is no longer counted as building, so the slot goes to 20-quiet (open, unblocked, not parked, carries release-m1-r1, no worker yet). 20-quiet is a lone Ticket: `implement`, tier regular (<model>), no Review level named. The check-in still runs (`checkins.md`), so it is kept. Milestone review gate not held (20, 25 open, unparked).

### 10. Apply / remove labels
Issue: .scratch/issues/10-farewell.md
Add: parked
Remove: none

### 11. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead parked -->
Parked at 2026-11-03T12:05:00Z. Reason: worker w-10-0920 stayed silent after its nudge, and its stop did not read back: the harness reported the stop taken at 12:05Z, but .scratch/harness/workers.md still reads it `idle` since 09:40Z, not `stopped`.
A writer may remain: w-10-0920 has not read back stopped and could still write to branch t10 (nothing pushed there yet).
Records: start, this issue's comment of 2026-11-03T09:20:00Z; nudge, this issue's comment of 2026-11-03T11:00:00Z. Pull request: none.
Skipped until the user removes the `parked` label. Before any fresh worker starts here, w-10-0920 is stopped and read back first.
~~~

### 12. Message the user
Body:
~~~
Parked 10-farewell.md (Add a farewell command): worker w-10-0920 went silent, and my stop of it did not read back (the harness still shows it idle, not stopped), so a writer may remain on branch t10. Details: the parked comment on .scratch/issues/10-farewell.md. Remove the `parked` label to have it picked up again. Going on with 20-quiet.md.
~~~

### 13. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (<model>)
Brief:
~~~
Run the `implement` skill (plugins/dev-skills/skills/implement/SKILL.md, from the checkout's main) as this Ticket's Ticket thread.
Repo: <runs>/main-deliver-lift/repo
Ticket: .scratch/issues/20-quiet.md (Add a --quiet flag).
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet). Release: .scratch/issues/40-release-m1-r1.md.
Model tier: regular. Review level: none named; Round 0 sizes it.
Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md (dry run). Merge-time steps: CLAUDE.md, "Merge-time steps" (a pull request changing a file under skills/ asks the coordinator for its version number just before merging).
In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when you finish, ask, or are blocked.
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
Session: none readable (the dry-run harness gives no session reference; its record is .scratch/harness/workers.md)
~~~

## Event 7

Wake 12:30Z: the harness says w-20-1205 failed. Read: `workers.md` reads w-20-1205 `failed` since 12:28Z (an end; no stop needed). Branch t20 has one pushed commit (fdf97b5, 12:20Z, "quiet: the --quiet flag"); no pull request; no report comment on 20-quiet. It ended without its result: start a fresh worker from the pushed branch and the tracker ("Replace a stalled worker" steps 3 and 4). This counts as a stall; 20-quiet has no park record, so this is its first stall and a replacement starts, same skill, tier and Review level. 10-farewell stays parked (w-10-0920 still reads `idle`). No pause; check-in still runs; Milestone review gate not held.

### 15. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (<model>)
Brief:
~~~
Run the `implement` skill (plugins/dev-skills/skills/implement/SKILL.md, from the checkout's main) as this Ticket's Ticket thread, taking over from worker w-20-1205, which failed at 12:28Z.
Repo: <runs>/main-deliver-lift/repo
Ticket: .scratch/issues/20-quiet.md (Add a --quiet flag).
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet). Release: .scratch/issues/40-release-m1-r1.md.
Resume from the pushed branch t20 (its last commit fdf97b5, "quiet: the --quiet flag") and the tracker (the issue, its comments; no pull request yet). Keep what is pushed; do not restart from main.
Model tier: regular. Review level: none named; Round 0 sizes it.
Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md (dry run). Merge-time steps: CLAUDE.md, "Merge-time steps" (a pull request changing a file under skills/ asks the coordinator for its version number just before merging).
In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when you finish, ask, or are blocked.
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
Session: none readable (the dry-run harness gives no session reference; its record is .scratch/harness/workers.md)
Takes over from w-20-1205; its end as read: `failed` since 2026-11-03T12:28:00Z in .scratch/harness/workers.md, at 2026-11-03T12:30:00Z. Resumes from branch t20 (fdf97b5).
~~~

## Event 8

Check-in 13:00Z. Read: no pause; 10-farewell parked (w-10-0920 still `idle`, its issue skipped until the user lifts the park); 20-quiet open, w-20-1230 `working` since 12:30Z, t20 at 86d0199 (12:50Z), no PR; 25-hello-doc open, no release label, blocked by open 35-readme-tool. Snapshot (`--now 2026-11-03T13:00:00Z --silent-after 60`, the build worker on unparked work): w-20-1230 active. Milestone review gate not held. Quiet check-in: nothing written, no one told.

## Event 9

Check-in 14:00Z. Read: no pause; 10-farewell parked (w-10-0920 `idle`); w-20-1230 `idle` since 12:51Z, t20 last commit 86d0199 at 12:50Z, no PR, no comment on 20-quiet. Snapshot (`--now 2026-11-03T14:00:00Z --silent-after 60`): w-20-1230 silent since 12:50Z, not nudged. Nudge it once. Milestone review gate not held.

### 17. Message a worker
Worker: w-20-1230
Body:
~~~
Check-in 14:00Z: nothing has reached the tracker or t20 from you since your last commit at 12:50Z (86d0199), and there is no pull request. Where are you on 20-quiet, and what blocks you? Answer with a comment on .scratch/issues/20-quiet.md, and push what you have.
~~~

### 18. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead nudge -->
Worker w-20-1230 nudged at 2026-11-03T14:00:00Z: silent since its last commit on t20 at 12:50Z (86d0199); no comment, no pull request; harness state `idle` since 12:51Z. Asked where it is and what blocks it, answered by a comment on this issue.
~~~

## Event 10

Check-in 15:00Z. Read: no pause; 10-farewell parked; w-20-1230 still `idle` since 12:51Z, t20 unchanged at 86d0199, no PR, no answer to the 14:00Z nudge. Snapshot (`--now 2026-11-03T15:00:00Z --silent-after 60`): still silent after its nudge. Replace a stalled worker, step 2: stop it and read the stop back when the harness reports it taken. w-20-1230 is itself a replacement (of w-20-1205) with no park record on 20-quiet before it, so this is the feature's second stall: once the stop reads back, 20-quiet parks rather than getting another worker. Milestone review gate not held.

### 19. Stop a worker
Worker: w-20-1230

## Event 11

Wake 15:05Z: the harness says the stop of w-20-1230 was taken. Read the stop back: `workers.md` reads w-20-1230 `stopped` since 15:03Z: the stop reads back. It was a replacement (of w-20-1205, failed 12:28Z) started with no park record on 20-quiet before it: the feature's second stall, so park 20-quiet instead of starting another worker (step 4). No writer remains: w-20-1205 `failed`, w-20-1230 `stopped`. Pushed work stays on t20 (86d0199). Tell the user once.
Next starts: the current Release's build order is 10-farewell (parked) and 20-quiet (now parked): nothing in it to start. 25-hello-doc carries no release label and is blocked by open 35-readme-tool (outside the Milestone); a current Release exists with open issues, so no Release worker starts. Milestone review gate not held: 25-hello-doc is open and unparked. No build worker runs; the check-in still runs and is kept.

### 20. Apply / remove labels
Issue: .scratch/issues/20-quiet.md
Add: parked
Remove: none

### 21. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead parked -->
Parked at 2026-11-03T15:05:00Z. Reason: second stall. w-20-1205 failed at 12:28Z; its replacement w-20-1230 stayed silent after its nudge and was stopped (read back `stopped` since 15:03Z in .scratch/harness/workers.md).
Writer: none remains (w-20-1205 `failed`, w-20-1230 `stopped`). Pushed work kept on branch t20 (fdf97b5, 86d0199).
Records: start of w-20-1205, this issue's comment of 2026-11-03T12:05:00Z; start of w-20-1230, comment of 2026-11-03T12:30:00Z; nudge, comment of 2026-11-03T14:00:00Z. Pull request: none.
Skipped until the user removes the `parked` label.
~~~

### 22. Message the user
Body:
~~~
Parked 20-quiet.md (Add a --quiet flag) after its second stall: w-20-1205 failed and its replacement w-20-1230 went silent and was stopped (read back stopped); its work is kept on branch t20. Details: the parked comment on .scratch/issues/20-quiet.md. Remove the `parked` label to have it picked up again. With 10-farewell.md parked too, nothing in Release 1 can start, and 25-hello-doc.md waits on 35-readme-tool.md, which is outside the Milestone.
~~~

## Event 12

Check-in 16:00Z. Read: no pause; 10-farewell and 20-quiet parked (labels still on); 25-hello-doc open, no release label, blocked by open 35-readme-tool; no PRs; no build worker running (w-10-0920 `idle` on parked 10-farewell; w-20-1205 `failed`, w-20-1230 `stopped`), so the snapshot has no rows. Nothing to start; Milestone review gate not held (25-hello-doc open, unparked). Quiet check-in: nothing written, no one told.

## Event 13

Wake 16:30Z: the user writes "I removed the parked label from 10-farewell.md. Carry on with it." Read: 10-farewell no longer carries `parked` (user comment 16:28Z: the farewell wording is settled); 20-quiet still parked; no build worker running; no pause. A lifted issue keeps its place: 10-farewell is first in Release 1's order, started and with no running worker, so it takes the free slot. Before its fresh worker starts, its last worker's state: w-10-0920 reads `idle` since 09:40Z, not ended, so stop it and read the stop back first (step 2); the fresh worker starts only once it reads `stopped`; if it does not, 10-farewell parks again and the user is told once. Milestone review gate not held. Check-in still runs.

### 23. Stop a worker
Worker: w-10-0920

## Event 14

Wake 16:35Z: the harness says the stop of w-10-0920 was taken. Read the stop back: `workers.md` still reads w-10-0920 `idle` since 09:40Z, not `stopped`: the stop does not read back, a second time. Per the lift rule, 10-farewell parks again (no fresh worker starts while a writer may remain on t10), and the user is told once. Next starts: 20-quiet still parked; 25-hello-doc outside Release 1 and blocked by open 35-readme-tool: nothing to start. Milestone review gate not held (25-hello-doc open, unparked). Check-in still runs.

### 24. Apply / remove labels
Issue: .scratch/issues/10-farewell.md
Add: parked
Remove: none

### 25. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead parked -->
Parked again at 2026-11-03T16:35:00Z, after the user's lift at 16:28Z. Reason: before a fresh worker could start, its last worker w-10-0920 had to be stopped and read back; the harness reported the stop taken at 16:35Z, but .scratch/harness/workers.md still reads w-10-0920 `idle` since 09:40Z, not `stopped`. This is the second stop of it that did not read back (the first: 12:05Z).
A writer may remain: w-10-0920 could still write to branch t10 (nothing pushed there yet).
Records: start, this issue's comment of 2026-11-03T09:20:00Z; nudge, comment of 2026-11-03T11:00:00Z; first park, comment of 2026-11-03T12:05:00Z; the user's lift, comment of 2026-11-03T16:28:00Z. Pull request: none.
Skipped until the user removes the `parked` label; w-10-0920 needs to read stopped (or ended) in the harness before any fresh worker starts here.
~~~

### 26. Message the user
Body:
~~~
Parked 10-farewell.md again: before starting a fresh worker on it I stopped its old worker w-10-0920, but the stop did not read back for the second time (the harness still shows it idle, not stopped), so it could still write to branch t10 and a new worker would race it. It needs w-10-0920 ended in the harness (stopped by hand, if the harness allows) before the park is lifted again. Details: .scratch/issues/10-farewell.md.
~~~

## Event 15

Wake 16:50Z: the user writes "I removed the parked label from 20-quiet.md too." Read: 20-quiet no longer carries `parked` (user comment 16:48Z: keep the exit code in its own function); 10-farewell parked (w-10-0920 still `idle`); no build worker running; no pause; the check-in still runs (`checkins.md`), so it is kept. 20-quiet keeps its place in Release 1's order; 10-farewell before it is parked, so under one at a time it may start, and the slot is free. Its last worker w-20-1230 reads `stopped` since 15:03Z (ended), so no stop is needed first. Start a fresh worker with the same skill, tier and Review level, from pushed branch t20 and the tracker. Milestone review gate not held.

### 27. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (<model>)
Brief:
~~~
Run the `implement` skill (plugins/dev-skills/skills/implement/SKILL.md, from the checkout's main) as this Ticket's Ticket thread, taking over after the user lifted its park.
Repo: <runs>/main-deliver-lift/repo
Ticket: .scratch/issues/20-quiet.md (Add a --quiet flag). Read all its comments: the user's of 16:48Z says to keep the exit code in its own function.
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet). Release: .scratch/issues/40-release-m1-r1.md.
Resume from the pushed branch t20 (fdf97b5, 86d0199) and the tracker (the issue, its comments; no pull request yet). Keep what is pushed; do not restart from main. Earlier workers: w-20-1205 (failed 12:28Z), w-20-1230 (stopped 15:03Z); neither writes any more.
Model tier: regular. Review level: none named; Round 0 sizes it.
Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md (dry run). Merge-time steps: CLAUDE.md, "Merge-time steps" (a pull request changing a file under skills/ asks the coordinator for its version number just before merging).
In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when you finish, ask, or are blocked.
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
Session: none readable (the dry-run harness gives no session reference; its record is .scratch/harness/workers.md)
Takes over from w-20-1230; its stop read back: `stopped` since 2026-11-03T15:03:00Z in .scratch/harness/workers.md, at 2026-11-03T16:50:00Z. Starts after the user's lift of the park (comment of 2026-11-03T16:48:00Z). Resumes from branch t20 (86d0199).
~~~

## Event 16

Check-in 17:00Z. Read: no pause; 10-farewell parked (w-10-0920 still `idle`); 20-quiet open, unparked, w-20-1650 `working` since 16:50Z on t20, no PR; 25-hello-doc open, no release label, blocked by open 35-readme-tool. Snapshot (`--now 2026-11-03T17:00:00Z --silent-after 60`): w-20-1650 active. Slot taken; Milestone review gate not held. Quiet check-in: nothing written, no one told.
