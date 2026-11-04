## Event 1

Delivery starts (09:00Z). State read: Milestone issue `00-milestone.md` open, planning settled, latest Startup verification reads `Verdict: ready` (fallback harness, the dry-run harness page). No release issue exists, no worker runs (`.scratch/harness/workers.md` is empty), no check-in runs. Planned features `10-farewell.md` and `20-quiet.md` are open, not parked, unblocked and carry no release label, so a Release worker plans Milestone 1 · Release 1 first. It only plans, so no check-in is arranged yet (it is arranged at the first build-worker start). No build worker starts while it runs.

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium (Claude Code: <model>, the `model-tiers` default)
Brief:
~~~
Run the `release` skill as the Release worker of Milestone 1, at the premium tier. Plan the next Release (no Release has been cut yet, so this is Milestone 1 · Release 1) by `release`'s own rule, inside a Milestone: choose the scope yourself from the Milestone issue's order, asking nobody.

- Repo: <runs>/tlmain-deliver-lift/repo (branch main).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet).
- Release doc: docs/dev-skills/release.md (pull requests bump; name `Milestone <m> · Release <n>`, label `release-m<m>-r<n>`).
- Last release issue cut: none.
- Tracker: docs/dev-skills/issue-tracker.md (dry run: every write is a block in .scratch/proposed-actions.md).
- If an open release issue already exists that holds no issue yet, fill that one instead of opening another; for that issue this overrides `release`'s "Rerun first".
- Where no planned feature qualifies, open no release issue, label nothing, and say so in your report.
- Report to the coordinator when the release issue is open and read back, naming it.
- In your report on the issue, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference; write "unknown" for any you cannot read.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900 (id as the dry-run harness assigns it: issue file number 00, event clock 09:00)
Skill: release (Release worker: plans Milestone 1 · Release 1)
Model tier: premium
Review level: none
Started: 2026-11-03T09:00Z
Session or history reference: the harness's line for w-00-0900 in .scratch/harness/workers.md (the dry-run harness gives no other session reference)
~~~

## Event 2

Release worker w-00-0900 reported; its harness line reads `ended since 09:19`. Release issue `40-release-m1-r1.md` read back: open, `**Milestone:** 00-milestone.md`, scope 10-farewell.md (with Tickets 11, 12) and 20-quiet.md, maintenance fixes none; those issues carry `release-m1-r1`. No Release worker runs now. Slots: the smaller of the thread limit (3) and the order rule (one at a time) = 1. Build order: no maintenance fixes; first feature `10-farewell.md`, a Spec with Tickets, open, not parked, unblocked, no worker: `implement-spec`, tier regular, Review level Deep (both from the issue). This is the first build-worker start, so the check-in is arranged first: `.scratch/harness/checkins.md` lists none running, so one is arranged at the Boundary record's interval (1 hour).

### 3. Arrange a check-in
Every: 1 hour
Into: coordinator

### 4. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead check-in -->
Check-in arranged at 2026-11-03T09:20Z through the dry-run harness: every 1 hour (the Boundary record's interval), into the coordinator. No earlier check-in was running.
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular (Claude Code: <model>, the `model-tiers` default)
Brief:
~~~
Run the `implement-spec` skill as the Spec thread for .scratch/issues/10-farewell.md (Add a farewell command; Tickets .scratch/issues/11-bye-code.md and .scratch/issues/12-bye-usage.md), at the regular tier, Review level Deep (named on the issue).

- Repo: <runs>/tlmain-deliver-lift/repo (branch main).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1); release issue .scratch/issues/40-release-m1-r1.md.
- Tracker: docs/dev-skills/issue-tracker.md; boundaries: docs/dev-skills/boundaries.md and the Milestone issue's own.
- A pull request that changes a file under `skills/` asks the coordinator for its version number just before merging (CLAUDE.md, "Merge-time steps").
- Report to the coordinator at each Ticket landing, when the Spec pull request is ready, and when merged; ask if blocked.
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. As it becomes readable, preserve the evidence the Milestone report gathers (`milestone`'s reporting reference, "Gather the evidence"): your start and end times, session usage, versions and settings, user messages you see, and agent decisions (design answers, rules-file merges) with links.
~~~

### 6. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead start -->
Worker: w-10-0920 (id as the dry-run harness assigns it)
Skill: implement-spec
Model tier: regular
Review level: Deep
Started: 2026-11-03T09:20Z
Session or history reference: the harness's line for w-10-0920 in .scratch/harness/workers.md (the dry-run harness gives no other session reference)
~~~

## Event 3

Check-in 10:00Z. Snapshot (`--now 2026-11-03T10:00:00Z`): w-10-0920, working, no commit, no comment, no PR, verdict `active`. Quiet check-in: no write.

## Event 4

Check-in 11:00Z. Harness: w-10-0920 `idle since 09:40` (not ended). Snapshot (`--now 2026-11-03T11:00:00Z`): no commit on `t10`, no comment, no PR, verdict `silent since 2026-11-03T09:20:00Z`. No earlier nudge: nudge it once.

### 7. Message a worker
Worker: w-10-0920
Body:
~~~
Check-in from the coordinator: nothing has reached the tracker or branch t10 since your start at 09:20Z. Where are you on .scratch/issues/10-farewell.md, and what blocks you? Answer with a comment on .scratch/issues/10-farewell.md, and push any work you have to t10.
~~~

### 8. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-10-0920 (implement-spec on .scratch/issues/10-farewell.md) at 2026-11-03T11:00Z: harness state idle since 09:40Z; no commit on t10, no comment and no pull request since its start at 09:20Z. Asked where it is and what blocks it, answered by a comment on 10-farewell.md.
~~~

## Event 5

Check-in 12:00Z. Harness: w-10-0920 `idle since 09:40` (not ended). Snapshot (`--now 2026-11-03T12:00:00Z`): still no commit on `t10`, no comment on 10-farewell.md, no PR; verdict `silent since 09:20`. It was nudged at 11:00Z (the `nudge` record on the Milestone issue, which the snapshot does not read) and has not answered: still silent after its nudge, so it is replaced. It is the feature's first worker (no park record on 10-farewell.md), so step 2 of "Replace a stalled worker": stop it and read the stop back at the harness's next wake.

### 9. Stop a worker
Worker: w-10-0920

## Event 6

The harness says the stop of w-10-0920 was taken. Read back: `.scratch/harness/workers.md` still reads `w-10-0920 10-farewell.md branch t10: idle since 2026-11-03T09:40:00Z`. Only `stopped` is a stop, so the stop does not read back: park 10-farewell.md instead of replacing (step 4 of "Replace a stalled worker"); a writer may remain on t10. Then go on with other work: the slot goes to the next feature in order, `20-quiet.md` (lone Ticket, open, not parked, unblocked, no worker): `implement`, tier regular (its Model tier line), no Review level named. The check-in arranged at 09:20Z still runs (checkins.md lists it).

### 10. Apply / remove labels
Issue: .scratch/issues/10-farewell.md
Add: parked
Remove: none

### 11. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead parked -->
Parked at 2026-11-03T12:05Z. Reason: its worker w-10-0920 (implement-spec) was silent from its start at 09:20Z (no commit on t10, no comment, no pull request), stayed silent after its nudge at 11:00Z, and the stop asked for at 12:00Z does not read back: the harness reported the stop taken, but its record still reads `idle since 09:40Z`, not `stopped`.
A writer may remain: w-10-0920 is not read as ended and could still push to branch t10.
Records: start record on this issue (2026-11-03T09:20Z); nudge record on .scratch/issues/00-milestone.md (2026-11-03T11:00Z). Pull request: none.
Remove the `parked` label to lift the park; before a fresh worker starts, w-10-0920 is stopped and read back first.
~~~

### 12. Message the user
Body:
~~~
Parked .scratch/issues/10-farewell.md (Add a farewell command): its worker w-10-0920 stayed silent after a nudge and its stop does not read back (the harness still reads it idle, not stopped), so it may still write to branch t10. Remove the `parked` label to lift it. Delivery goes on with .scratch/issues/20-quiet.md.
~~~

### 13. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (Claude Code: <model>, the `model-tiers` default)
Brief:
~~~
Run the `implement` skill as the Ticket thread for .scratch/issues/20-quiet.md (Add a --quiet flag), a lone Ticket, at the regular tier. No Review level is named: let agentic-review's Round 0 size it.

- Repo: <runs>/tlmain-deliver-lift/repo (branch main).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1); release issue .scratch/issues/40-release-m1-r1.md.
- Tracker: docs/dev-skills/issue-tracker.md; boundaries: docs/dev-skills/boundaries.md and the Milestone issue's own.
- A pull request that changes a file under `skills/` asks the coordinator for its version number just before merging (CLAUDE.md, "Merge-time steps").
- Report to the coordinator when the pull request is open, when it is ready and when merged; ask if blocked.
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. As it becomes readable, preserve the evidence the Milestone report gathers (`milestone`'s reporting reference, "Gather the evidence"): your start and end times, session usage, versions and settings, user messages you see, and agent decisions with links.
~~~

### 14. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1205 (id as the dry-run harness assigns it)
Skill: implement
Model tier: regular
Review level: none named
Started: 2026-11-03T12:05Z
Session or history reference: the harness's line for w-20-1205 in .scratch/harness/workers.md (the dry-run harness gives no other session reference)
~~~

## Event 7

The harness reports w-20-1205 failed. Its line reads `w-20-1205 20-quiet.md branch t20: failed since 2026-11-03T12:28:00Z`: ended without its result, so no stop is needed. Branch t20 has one pushed commit (fdf97b5, 12:20Z, "quiet: the --quiet flag"); no pull request. It counts as a stall; w-20-1205 was the issue's first worker (no park record on 20-quiet.md), so a fresh worker takes over on the same issue with the same skill and tier, resuming from t20. 10-farewell.md stays parked; w-10-0920 still reads idle.

### 15. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (Claude Code: <model>, the `model-tiers` default)
Brief:
~~~
Run the `implement` skill as the Ticket thread for .scratch/issues/20-quiet.md (Add a --quiet flag), a lone Ticket, at the regular tier. No Review level is named: let agentic-review's Round 0 size it.

You take over from worker w-20-1205, which failed at 12:28Z. Resume from its pushed branch t20 (last commit fdf97b5, "quiet: the --quiet flag") and from the tracker (the issue, its comments; no pull request is open yet), keeping what is pushed: do not restart from main.

- Repo: <runs>/tlmain-deliver-lift/repo (branch main; work branch t20).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1); release issue .scratch/issues/40-release-m1-r1.md.
- Tracker: docs/dev-skills/issue-tracker.md; boundaries: docs/dev-skills/boundaries.md and the Milestone issue's own.
- A pull request that changes a file under `skills/` asks the coordinator for its version number just before merging (CLAUDE.md, "Merge-time steps").
- Report to the coordinator when the pull request is open, when it is ready and when merged; ask if blocked.
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. As it becomes readable, preserve the evidence the Milestone report gathers (`milestone`'s reporting reference, "Gather the evidence"): your start and end times, session usage, versions and settings, user messages you see, and agent decisions with links.
~~~

### 16. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1230 (id as the dry-run harness assigns it)
Skill: implement
Model tier: regular
Review level: none named
Started: 2026-11-03T12:30Z
Session or history reference: the harness's line for w-20-1230 in .scratch/harness/workers.md (the dry-run harness gives no other session reference)
Takes over from w-20-1205; its end as read (`failed since 2026-11-03T12:28:00Z` in .scratch/harness/workers.md), at 2026-11-03T12:30Z. Resumes from branch t20 (fdf97b5).
~~~

## Event 8

Check-in 13:00Z. Snapshot (`--now 2026-11-03T13:00:00Z`): w-20-1230 working, last commit 12:50Z on t20, no PR, verdict `active`. 10-farewell.md still parked (w-10-0920 still reads idle). Quiet check-in: no write.

## Event 9

Check-in 14:00Z. Harness: w-20-1230 `idle since 12:51` (not ended). Snapshot (`--now 2026-11-03T14:00:00Z`): last commit 12:50Z on t20, no comment, no PR, verdict `silent since 2026-11-03T12:50:00Z`. Not nudged before: nudge it once. 10-farewell.md still parked (w-10-0920 still reads idle).

### 17. Message a worker
Worker: w-20-1230
Body:
~~~
Check-in from the coordinator: nothing has reached the tracker or branch t20 since your commit at 12:50Z. Where are you on .scratch/issues/20-quiet.md, and what blocks you? Answer with a comment on .scratch/issues/20-quiet.md, and push any work you have to t20.
~~~

### 18. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-20-1230 (implement on .scratch/issues/20-quiet.md, replacement for w-20-1205) at 2026-11-03T14:00Z: harness state idle since 12:51Z; last commit on t20 at 12:50Z, no comment and no pull request. Asked where it is and what blocks it, answered by a comment on 20-quiet.md.
~~~

## Event 10

Check-in 15:00Z. Harness: w-20-1230 `idle since 12:51` (not ended). Snapshot (`--now 2026-11-03T15:00:00Z`): last commit 12:50Z, no comment on 20-quiet.md, no PR; verdict `silent since 12:50`. Nudged at 14:00Z with no answer: still silent after its nudge. Step 2 of "Replace a stalled worker": stop it and read the stop back at the harness's next wake. w-20-1230 is itself a replacement started since the issue's latest park record (the issue has none), so this is the feature's second stall: once the stop is read, the issue is parked rather than given a third worker. 10-farewell.md still parked; 25-hello-doc.md is blocked by open 35-readme-tool.md; nothing else can start.

### 19. Stop a worker
Worker: w-20-1230

## Event 11

The harness says the stop of w-20-1230 was taken. Read back: `w-20-1230 20-quiet.md branch t20: stopped since 2026-11-03T15:03:00Z`, a confirmed stop (it read idle, not ended, at 15:00Z). It was the feature's second stall (a replacement, started 12:30Z, with no park record on the issue before it), so 20-quiet.md is parked instead of getting a third worker (step 4). No writer remains: w-20-1205 reads failed and w-20-1230 reads stopped. Then: 10-farewell.md is parked, 20-quiet.md is parked, 25-hello-doc.md is open, unparked and blocked by the open 35-readme-tool.md (outside the Milestone), so nothing can start and the Milestone review gate stays closed (25-hello-doc.md is an open, unparked feature). The check-in keeps running.

### 20. Apply / remove labels
Issue: .scratch/issues/20-quiet.md
Add: parked
Remove: none

### 21. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead parked -->
Parked at 2026-11-03T15:05Z. Reason: the feature's second stall. Its first worker w-20-1205 failed at 12:28Z; its replacement w-20-1230 went silent after its commit at 12:50Z, stayed silent after its nudge at 14:00Z, and was stopped (read back `stopped since 2026-11-03T15:03:00Z` in .scratch/harness/workers.md).
No writer remains: w-20-1205 reads failed and w-20-1230 reads stopped.
Work kept: branch t20 (fdf97b5 "quiet: the --quiet flag", 86d0199 "quiet: keep the exit code"). Pull request: none.
Records: start records on this issue (w-20-1205 at 2026-11-03T12:05Z; w-20-1230 at 2026-11-03T12:30Z); nudge record on .scratch/issues/00-milestone.md (2026-11-03T14:00Z).
Remove the `parked` label to lift the park; a fresh worker then resumes from t20.
~~~

### 22. Message the user
Body:
~~~
Parked .scratch/issues/20-quiet.md (Add a --quiet flag): its second worker stalled too (the first failed; the replacement went silent after a nudge and is now stopped). No writer remains; its work is kept on branch t20. Remove the `parked` label to lift it. With 10-farewell.md also parked and 25-hello-doc.md blocked by 35-readme-tool.md (outside the Milestone), nothing more can start until a park is lifted or that blocker closes.
~~~

## Event 12

Check-in 16:00Z. No build worker runs (w-10-0920 reads idle but its issue is parked; w-20-1230 stopped), so the snapshot has no rows. State unchanged: 10-farewell.md and 20-quiet.md parked, 25-hello-doc.md blocked by open 35-readme-tool.md, gate closed. Quiet check-in: no write.

## Event 13

The user lifted the park on 10-farewell.md (label removed; their comment at 16:28Z). It keeps its place: first in the build order, and under one at a time it takes the one slot (20-quiet.md is still parked). Before its fresh worker starts, its last worker's state is read: `w-10-0920 10-farewell.md branch t10: idle since 2026-11-03T09:40:00Z`, not ended, so it is stopped and read back first (step 2). No worker starts at this wake.

### 23. Stop a worker
Worker: w-10-0920

### 24. Message the user
Body:
~~~
Picking 10-farewell.md back up. Its old worker w-10-0920 still reads idle, so I am stopping it and reading the stop back before a fresh worker starts; if the stop does not read back, the issue parks again.
~~~

## Event 14

The harness says the stop of w-10-0920 was taken. Read back: `w-10-0920 10-farewell.md branch t10: idle since 2026-11-03T09:40:00Z`: still not `stopped`, so the stop does not read back a second time. A fresh worker could then write to the same branch alongside it, so 10-farewell.md is parked again and no worker starts on it. 20-quiet.md is still parked and 25-hello-doc.md still blocked: nothing starts; the gate stays closed (25-hello-doc.md open, unparked).

### 25. Apply / remove labels
Issue: .scratch/issues/10-farewell.md
Add: parked
Remove: none

### 26. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead parked -->
Parked again at 2026-11-03T16:35Z, after the user's lift at 16:28Z. Reason: before a fresh worker could start, its last worker w-10-0920 had to be stopped and read back. The stop was asked for at 16:30Z and the harness reported it taken, but its record still reads `idle since 2026-11-03T09:40:00Z`, not `stopped` (the same as at the first park).
A writer may remain: w-10-0920 is not read as ended and could still push to branch t10.
Records: start record on this issue (2026-11-03T09:20Z); nudge record on .scratch/issues/00-milestone.md (2026-11-03T11:00Z); first parked record on this issue (2026-11-03T12:05Z). Pull request: none.
A fresh worker starts only once w-10-0920 reads ended (stopped, ended or failed) in the harness's record; lifting the park again leads to the same stop and read-back first.
~~~

### 27. Message the user
Body:
~~~
Parked .scratch/issues/10-farewell.md again: the stop of its old worker w-10-0920 still does not read back (the harness still reads it idle since 09:40Z, not stopped), so a fresh worker could share branch t10 with it. It needs w-10-0920 to read ended in the harness before anyone builds it.
~~~

## Event 15

The user lifted the park on 20-quiet.md (label removed; their comment at 16:48Z: "keep the exit code in its own function"). Its last worker's state: `w-20-1230 20-quiet.md branch t20: stopped since 2026-11-03T15:03:00Z`, already ended, so no stop is needed. 10-farewell.md, ahead of it in the order, is parked (since 16:35Z), so under one at a time 20-quiet.md may take the one free slot: a started feature with no running worker. A fresh `implement` worker at the regular tier resumes from t20. The check-in arranged at 09:20Z still runs (checkins.md lists it), so none is arranged.

### 28. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (Claude Code: <model>, the `model-tiers` default)
Brief:
~~~
Run the `implement` skill as the Ticket thread for .scratch/issues/20-quiet.md (Add a --quiet flag), a lone Ticket, at the regular tier. No Review level is named: let agentic-review's Round 0 size it.

The user lifted this issue's park at 16:48Z. Resume from the pushed branch t20 (fdf97b5 "quiet: the --quiet flag", 86d0199 "quiet: keep the exit code") and from the tracker (the issue and all its comments, including the user's at 16:48Z: "keep the exit code in its own function"; no pull request is open yet), keeping what is pushed: do not restart from main. Earlier workers w-20-1205 (failed) and w-20-1230 (stopped) have both ended; neither writes to t20.

- Repo: <runs>/tlmain-deliver-lift/repo (branch main; work branch t20).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1); release issue .scratch/issues/40-release-m1-r1.md.
- Tracker: docs/dev-skills/issue-tracker.md; boundaries: docs/dev-skills/boundaries.md and the Milestone issue's own.
- A pull request that changes a file under `skills/` asks the coordinator for its version number just before merging (CLAUDE.md, "Merge-time steps").
- Report to the coordinator when the pull request is open, when it is ready and when merged; ask if blocked.
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. As it becomes readable, preserve the evidence the Milestone report gathers (`milestone`'s reporting reference, "Gather the evidence"): your start and end times, session usage, versions and settings, user messages you see, and agent decisions with links.
~~~

### 29. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1650 (id as the dry-run harness assigns it)
Skill: implement
Model tier: regular
Review level: none named
Started: 2026-11-03T16:50Z
Session or history reference: the harness's line for w-20-1650 in .scratch/harness/workers.md (the dry-run harness gives no other session reference)
Takes over from w-20-1230; its stop read back (`stopped since 2026-11-03T15:03:00Z` in .scratch/harness/workers.md), at 2026-11-03T16:50Z. Started after the user lifted the park at 16:48Z; resumes from branch t20 (86d0199).
~~~

## Event 16

Check-in 17:00Z. Snapshot (`--now 2026-11-03T17:00:00Z`): w-20-1650 working since 16:50Z, last commit 12:50Z (before its start), no PR, verdict `active`. 10-farewell.md still parked (w-10-0920 still reads idle); 25-hello-doc.md still blocked by 35-readme-tool.md; gate closed. Quiet check-in: no write.
