## Event 1

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium (<model>)
Brief:
~~~
Run the `release` skill to plan the next Release of Milestone 1.
Repo: <runs>/tl-deliver/repo
Milestone issue: .scratch/issues/00-milestone.md (features, order rule "one at a time", acceptance, exclusions).
Release doc: docs/dev-skills/release.md (bump mode: pull requests bump; Release name `Milestone <m> · Release <n>`, label `release-m<m>-r<n>`).
Last release issue cut: none; this is the Milestone's first Release.
Tracker: docs/dev-skills/issue-tracker.md (dry run: every write is a block in .scratch/proposed-actions.md).
Model tier: premium. Review level: none named.
Plan the next Release by `release`'s own rule. Where an open release issue holds no issue yet, fill that one instead of opening another (this overrides `release`'s "Rerun first" for that issue). Where nothing qualifies, open no release issue, label nothing and say so.
This project does not run the `triage` skill.
Build nothing: no build worker starts while you run. Report to the coordinator when you are done.
In your issue report record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900 (id as the dry-run harness gives it)
Skill: release (plans Milestone 1's first Release; builds nothing)
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T09:00:00Z
Session or history reference: dry-run harness record, .scratch/harness/workers.md line for w-00-0900
~~~

## Event 2

Read: w-00-0900 reads `ended` since 09:19Z in .scratch/harness/workers.md. Release issue 40-release-m1-r1.md read back: open, label `release-m1-r1` on 10, 11, 12 and 20; it has no Order list, so the build order is its maintenance fixes (none), then its features in the Milestone issue's order: 10-farewell.md, then 20-quiet.md. Slots: smaller of 3 (project) and one at a time = 1. No check-in runs (.scratch/harness/checkins.md is empty), so it is arranged before the first build-worker start.

### 3. Arrange a check-in
Every: 1 hour
Into: coordinator

### 4. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead check-in -->
Check-in arranged at 2026-11-03T09:20:00Z: every 1 hour (the Boundary record's interval), into the coordinator, through the dry-run harness (docs/dev-skills/harness.md). None ran before (.scratch/harness/checkins.md empty).
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular (<model>)
Brief:
~~~
Run the `implement-spec` skill to build the Spec .scratch/issues/10-farewell.md (Add a farewell command) and its Tickets 11-bye-code.md and 12-bye-usage.md.
Repo: <runs>/tl-deliver/repo
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; Release: .scratch/issues/40-release-m1-r1.md).
Model tier: regular. Review level: Deep (named by the issue).
Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md.
Merge-time steps: the PR changes skills/greeting/SKILL.md, so just before merging ask the coordinator for your version number (CLAUDE.md, "Merge-time steps") and add the VERSION bump as the pull request's last commit.
In your issue report record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when the pull request is ready, when you need the version number, and when it is merged.
~~~

### 6. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead start -->
Worker: w-10-0920 (id as the dry-run harness gives it)
Skill: implement-spec
Model tier: regular (<model>)
Review level: Deep
Started: 2026-11-03T09:20:00Z
Session or history reference: dry-run harness record, .scratch/harness/workers.md line for w-10-0920
~~~

## Event 3

## Event 4

Read: PR #7 (.scratch/pulls/7.md) builds 10-farewell.md, open and ready, checks passing, changes skills/greeting/SKILL.md (a new farewell rule, per 11-bye-code.md), so it takes a number. Main's VERSION is 0.3.0; no number is out. Version hand-out: 0.3.0 raised minor = 0.4.0.

### 7. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- version hand-out -->
Version 0.4.0 for #7: merge it next, with the bump as its last commit.
Given by the coordinator at 2026-11-03T10:40:00Z to w-10-0920: main's VERSION 0.3.0 raised minor for a changed skill rule (skills/greeting/SKILL.md, the farewell rule).
~~~

### 8. Message a worker
Worker: w-10-0920
Body:
~~~
Your version number for #7 is 0.4.0 (main's VERSION 0.3.0 raised minor for the changed `greeting` skill rule), recorded on 10-farewell.md. Add the VERSION bump to 0.4.0 as the pull request's last commit, merge #7, and report the merge to me.
~~~

## Event 5

Read: PR #7 reads merged at 10:52Z; w-10-0920 reads `ended` since 10:53Z; 10-farewell.md, 11-bye-code.md and 12-bye-usage.md read closed. Main's VERSION reads 0.4.0, the number given, so the number is no longer out. #7 changed skills/greeting/SKILL.md; main's new text adds: "A farewell is `Goodbye, <name>!`; every message, farewells included, is printed by one `say` function."
Ticket re-read after the skill merge (before any further start): the open Milestone 1 issues no running thread builds are 20-quiet.md and 25-hello-doc.md. 20-quiet.md names the `greeting` skill (skills/greeting/SKILL.md) for how messages are printed: the new rule makes it incomplete, since `--quiet` must now silence the one `say` function that prints every message; it is updated below. 25-hello-doc.md names neither the changed skill nor a changed file (skills/greeting/SKILL.md, src/greet.sh, test.sh): not re-read.

### 9. Edit an issue body
Issue: .scratch/issues/20-quiet.md
Body:
~~~
`--quiet` before any command prints nothing and keeps the exit code. Follows the `greeting` skill (`skills/greeting/SKILL.md`) for how messages are printed: every message goes through the one `say` function, so `--quiet` silences it there. Model tier: regular.

_Updated after #7 merged (version 0.4.0): the `greeting` skill now prints every message through one `say` function, so `--quiet` is applied in `say`._
~~~

Next start: Release 1 (40-release-m1-r1.md) still has 20-quiet.md open, so it is not cut yet. Build order: 10-farewell.md closed; 20-quiet.md is open, not parked, unblocked, with no running worker. One slot, now free. 20-quiet.md is a lone Ticket: `implement`. The check-in still runs (.scratch/harness/checkins.md).

### 10. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (<model>)
Brief:
~~~
Run the `implement` skill to build the lone Ticket .scratch/issues/20-quiet.md (Add a --quiet flag). Read its body as updated after #7's merge: `--quiet` is applied in the one `say` function the `greeting` skill now requires.
Repo: <runs>/tl-deliver/repo
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; Release: .scratch/issues/40-release-m1-r1.md).
Model tier: regular. Review level: none named; let the review size it.
Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md.
Merge-time steps: if your pull request changes a file under skills/, ask the coordinator for your version number just before merging (CLAUDE.md, "Merge-time steps"); if it changes none, merge with no bump.
In your issue report record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when the pull request is ready and when it is merged.
~~~

### 11. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1055 (id as the dry-run harness gives it)
Skill: implement
Model tier: regular (<model>)
Review level: none
Started: 2026-11-03T10:55:00Z
Session or history reference: dry-run harness record, .scratch/harness/workers.md line for w-20-1055
~~~

## Event 6

Check-in snapshot at 12:00Z: w-20-1055 (20-quiet.md, branch t20) reads `idle`; PR #8 ready since 11:55Z and not reported. Acted on as a report: #8 builds 20-quiet.md, checks passing, changes src/greet.sh and test.sh only, no file under skills/, so it takes no version number and merges with no bump (CLAUDE.md, "Merge-time steps"). No number is out. The next check-in passes 12:00Z as its `reported` time.

### 12. Message a worker
Worker: w-20-1055
Body:
~~~
I read #8 as ready (checks passing). It changes no file under skills/, so it takes no version number: merge it with no VERSION bump once your review lets you, then report the merge to me.
~~~

## Event 7

Read: PR #8 merged at 12:15Z, changing no file under skills/ (no hand-out, no Ticket re-read); VERSION stays 0.4.0; w-20-1055 reads `ended` since 12:16Z; 20-quiet.md closed. Every issue carrying `release-m1-r1` (10, 11, 12, 20) is closed, so Release 1 is cut by a Release worker; no build worker starts while it runs. Milestone review gate: 25-hello-doc.md is open and unparked, so it stays closed.

### 13. Start a worker
Issue: .scratch/issues/40-release-m1-r1.md
Skill: release
Tier: premium (<model>)
Brief:
~~~
Run the `release` skill to cut Milestone 1 · Release 1 (.scratch/issues/40-release-m1-r1.md; every issue carrying `release-m1-r1` is closed) and then plan the next Release of Milestone 1.
Repo: <runs>/tl-deliver/repo
Milestone issue: .scratch/issues/00-milestone.md. Release doc: docs/dev-skills/release.md (pull requests bump: the cut opens no bump pull request; it writes the changelog entry for everything since the last Release). Last release issue cut: none before this one; this cut is 40-release-m1-r1.md. Merged in it: #7 (10-farewell.md with 11 and 12, VERSION 0.4.0) and #8 (20-quiet.md, no version change).
Tracker: docs/dev-skills/issue-tracker.md (dry run).
Model tier: premium. Review level: none named.
Plan the next Release by `release`'s own rule. Where an open release issue holds no issue yet, fill that one instead of opening another (this overrides `release`'s "Rerun first" for that issue). Where nothing qualifies, open no release issue, label nothing and say so.
This project does not run the `triage` skill.
Build nothing. Report to the coordinator when the cut and the planning are done.
In your issue report record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 14. Comment on an issue
Issue: .scratch/issues/40-release-m1-r1.md
Body:
~~~
<!-- team-lead start -->
Worker: w-40-1220 (id as the dry-run harness gives it)
Skill: release (cuts Milestone 1 · Release 1, then plans the next)
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T12:20:00Z
Session or history reference: dry-run harness record, .scratch/harness/workers.md line for w-40-1220
~~~

## Event 8

## Event 9

Read: w-40-1220 reads `ended` since 13:28Z; 40-release-m1-r1.md read back closed; no other release issue is open. The one planned feature left open, 25-hello-doc.md, is unparked but blocked by 35-readme-tool.md (open, outside the Milestone, no worker on it), so no Release worker can plan it and no build worker starts. Milestone review gate: closed (25-hello-doc.md open, not parked). The check-in keeps running.

### 15. Message the user
Body:
~~~
Milestone 1 waits: Release 1 is cut, and the last feature, 25-hello-doc.md (Document the commands), cannot be planned or built until 35-readme-tool.md (Pick the README format checker, outside the Milestone) is closed.
~~~

## Event 10

Read: 35-readme-tool.md now reads closed (the user, 13:50Z), so 25-hello-doc.md has no open blocker. No current Release (40-release-m1-r1.md closed, no other release issue), no Release worker running (w-40-1220 ended), and 25-hello-doc.md is open, unparked, unblocked and carries no release label: a Release worker plans the next Release. No build workers run, so the snapshot has no rows. Milestone review gate: closed.

### 16. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium (<model>)
Brief:
~~~
Run the `release` skill to plan the next Release of Milestone 1.
Repo: <runs>/tl-deliver/repo
Milestone issue: .scratch/issues/00-milestone.md. Release doc: docs/dev-skills/release.md. Last release issue cut: .scratch/issues/40-release-m1-r1.md (Milestone 1 · Release 1).
25-hello-doc.md's blocker, 35-readme-tool.md, closed at 13:50Z.
Tracker: docs/dev-skills/issue-tracker.md (dry run).
Model tier: premium. Review level: none named.
Plan the next Release by `release`'s own rule. Where an open release issue holds no issue yet, fill that one instead of opening another (this overrides `release`'s "Rerun first" for that issue). Where nothing qualifies, open no release issue, label nothing and say so.
This project does not run the `triage` skill.
Build nothing. Report to the coordinator when you are done.
In your issue report record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 17. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-1400 (id as the dry-run harness gives it)
Skill: release (plans Milestone 1's next Release; builds nothing)
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T14:00:00Z
Session or history reference: dry-run harness record, .scratch/harness/workers.md line for w-00-1400
~~~

## Event 11

Read: w-00-1400 reads `ended` since 14:18Z. Release issue 41-release-m1-r2.md read back: open, `release-m1-r2` on 25-hello-doc.md; no Order list, so the order is its maintenance fixes (none), then 25-hello-doc.md. The check-in arranged at 09:20Z still runs (.scratch/harness/checkins.md), so it is kept. One slot, free. 25-hello-doc.md is a lone Ticket, open, unparked, unblocked (35-readme-tool.md closed): `implement` at its Model tier line, cheap.

### 18. Start a worker
Issue: .scratch/issues/25-hello-doc.md
Skill: implement
Tier: cheap (<model>)
Brief:
~~~
Run the `implement` skill to build the lone Ticket .scratch/issues/25-hello-doc.md (Document the commands in the README).
Repo: <runs>/tl-deliver/repo
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; Release: .scratch/issues/41-release-m1-r2.md).
Model tier: cheap (the issue's Model tier line). Review level: none named; let the review size it.
Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md.
Merge-time steps: if your pull request changes a file under skills/, ask the coordinator for your version number just before merging (CLAUDE.md, "Merge-time steps"); if it changes none, merge with no bump.
In your issue report record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when the pull request is ready and when it is merged.
~~~

### 19. Comment on an issue
Issue: .scratch/issues/25-hello-doc.md
Body:
~~~
<!-- team-lead start -->
Worker: w-25-1420 (id as the dry-run harness gives it)
Skill: implement
Model tier: cheap (<model>)
Review level: none
Started: 2026-11-03T14:20:00Z
Session or history reference: dry-run harness record, .scratch/harness/workers.md line for w-25-1420
~~~

## Event 12

## Event 13

Check-in snapshot at 16:00Z: w-25-1420 (25-hello-doc.md, branch t25) reads `idle` since 14:41Z; last commit 14:40Z, no comment, no pull request: silent since 14:40Z, past the 60-minute interval, never nudged. Nudge it once.

### 20. Message a worker
Worker: w-25-1420
Body:
~~~
Check-in at 16:00Z: nothing from you since your 14:40Z commit on t25 (no comment, no pull request). Where are you on 25-hello-doc.md and what blocks you? Answer with a comment on .scratch/issues/25-hello-doc.md.
~~~

### 21. Comment on an issue
Issue: .scratch/issues/25-hello-doc.md
Body:
~~~
<!-- team-lead nudge -->
Worker: w-25-1420, nudged at 2026-11-03T16:00:00Z by the check-in: silent since 2026-11-03T14:40:00Z (last commit on t25; no comment, no pull request; Harness state idle since 14:41Z). Asked where it is and what blocks it, to answer here.
~~~

## Event 14

Check-in snapshot at 17:00Z: w-25-1420 reads `idle` since 14:41Z, no commit after 14:40Z, no answer on 25-hello-doc.md, no pull request: still silent after its 16:00Z nudge. Replace a stalled worker, step 2: stop it and read the stop back from the Harness's record before any fresh start. 25-hello-doc.md has no park record, so this is its first stall.

### 22. Stop a worker
Worker: w-25-1420

## Event 15

Read: w-25-1420 reads `stopped` since 17:03Z in .scratch/harness/workers.md: the stop reads back. Branch t25 holds 177c8fd "readme: hello and bye" (14:40Z); no pull request. Start a fresh worker on 25-hello-doc.md with the same skill, tier and Review level, resuming from t25.

### 23. Start a worker
Issue: .scratch/issues/25-hello-doc.md
Skill: implement
Tier: cheap (<model>)
Brief:
~~~
Run the `implement` skill to finish the lone Ticket .scratch/issues/25-hello-doc.md (Document the commands in the README). You take over from w-25-1420, which went silent and was stopped (read back stopped at 17:03Z).
Resume from the pushed branch t25 (last commit 177c8fd "readme: hello and bye", 14:40Z) and the tracker: the issue, its comments (start and nudge records) and any pull request for t25 (none yet). Keep what is pushed; do not start over.
Repo: <runs>/tl-deliver/repo
Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; Release: .scratch/issues/41-release-m1-r2.md).
Model tier: cheap (the issue's Model tier line). Review level: none named; let the review size it.
Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md.
Merge-time steps: if your pull request changes a file under skills/, ask the coordinator for your version number just before merging (CLAUDE.md, "Merge-time steps"); if it changes none, merge with no bump.
In your issue report record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when the pull request is ready and when it is merged.
~~~

### 24. Comment on an issue
Issue: .scratch/issues/25-hello-doc.md
Body:
~~~
<!-- team-lead start -->
Worker: w-25-1705 (id as the dry-run harness gives it)
Skill: implement
Model tier: cheap (<model>)
Review level: none
Started: 2026-11-03T17:05:00Z
Session or history reference: dry-run harness record, .scratch/harness/workers.md line for w-25-1705
Takes over from w-25-1420; its stop read back `stopped` since 2026-11-03T17:03:00Z in .scratch/harness/workers.md, at 2026-11-03T17:05:00Z. Resumes from branch t25 (177c8fd).
~~~

## Event 16

Check-in snapshot at 18:00Z: w-25-1705 (25-hello-doc.md, branch t25) reads `idle` since 17:51Z; PR #11 ready since 17:50Z and not reported. Acted on as a report: #11 builds 25-hello-doc.md, checks passing, changes README.md only, no file under skills/, so it takes no version number and merges with no bump. The next check-in passes 18:00Z as its `reported` time.

### 25. Message a worker
Worker: w-25-1705
Body:
~~~
I read #11 as ready (checks passing). It changes no file under skills/, so it takes no version number: merge it with no VERSION bump once your review lets you, then report the merge to me.
~~~

## Event 17

Read: PR #11 merged at 18:08Z, changing README.md only (no hand-out, no Ticket re-read); VERSION stays 0.4.0; w-25-1705 reads `ended` since 18:09Z; 25-hello-doc.md closed. Milestone review gate: every planned feature is merged (#7 for 10-farewell.md with 11 and 12, #8 for 20-quiet.md, #11 for 25-hello-doc.md) and none is parked, so the gate holds; but the final Release still needs its cut: every issue carrying `release-m1-r2` is closed. Start that Release worker first and await its report before the report.

### 26. Start a worker
Issue: .scratch/issues/41-release-m1-r2.md
Skill: release
Tier: premium (<model>)
Brief:
~~~
Run the `release` skill to cut Milestone 1 · Release 2 (.scratch/issues/41-release-m1-r2.md; every issue carrying `release-m1-r2` is closed) and then plan the next Release of Milestone 1.
Repo: <runs>/tl-deliver/repo
Milestone issue: .scratch/issues/00-milestone.md. Release doc: docs/dev-skills/release.md (pull requests bump: the cut opens no bump pull request; it writes the changelog entry for everything since the last Release). Last release issue cut: .scratch/issues/40-release-m1-r1.md. Merged in this Release: #11 (25-hello-doc.md, no version change; VERSION 0.4.0).
Tracker: docs/dev-skills/issue-tracker.md (dry run).
Model tier: premium. Review level: none named.
Plan the next Release by `release`'s own rule. Where an open release issue holds no issue yet, fill that one instead of opening another (this overrides `release`'s "Rerun first" for that issue). Where nothing qualifies, open no release issue, label nothing and say so.
This project does not run the `triage` skill.
Build nothing. Report to the coordinator when the cut and the planning are done.
In your issue report record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one.
~~~

### 27. Comment on an issue
Issue: .scratch/issues/41-release-m1-r2.md
Body:
~~~
<!-- team-lead start -->
Worker: w-41-1810 (id as the dry-run harness gives it)
Skill: release (cuts Milestone 1 · Release 2, then plans the next)
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T18:10:00Z
Session or history reference: dry-run harness record, .scratch/harness/workers.md line for w-41-1810
~~~

## Event 18

Read: w-41-1810 reads `ended` since 18:38Z; 41-release-m1-r2.md read back closed; no release issue is open and no planned feature is left open, so no further Release starts. Milestone review gate: every planned feature is merged and closed (10-farewell.md with 11-bye-code.md and 12-bye-usage.md by #7, 20-quiet.md by #8, 25-hello-doc.md by #11), none parked, and the final Release cut has reported. No Milestone report exists on 00-milestone.md. No pause is in effect. End of delivery: start nothing further; end the check-in through the harness. .scratch/harness/checkins.md, read at 18:40Z, still lists it ("Every 1 hour into the coordinator, on the hour"); the end is read back from that file at the next wake, and only then are the `check-in` record and the Milestone report (milestone's reporting.md) posted.

### 28. End a check-in

### 29. Message the user
Body:
~~~
Milestone 1's features are all merged (#7, #8, #11) and Release 2 is cut; I have asked the harness to end the hourly check-in, and I post the Milestone report for your review once its end reads back.
~~~

