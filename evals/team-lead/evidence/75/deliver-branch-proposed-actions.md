## Event 1

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium
Brief:
~~~
Run the `release` skill (load it by name) for Milestone 1, on the premium tier (model: <model>, the `model-tiers` default).

- Repo: <runs>/runs/branch-deliver/repo (main).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet).
- Release doc: docs/dev-skills/release.md.
- Last release issue cut: none; this would be the Milestone's first Release.

Let the skill's "Find where you are" decide whether you cut a Release or plan the next one; this brief overrides none of it.
Boundaries are the Boundary record's (docs/dev-skills/boundaries.md); a question about one is the user's, so bring it to me.
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md).

In your report on the release issue (or on the Milestone issue if you open none), record the plugin load source and
version you actually loaded, your permission and sandbox settings, and a readable session usage reference, writing
"unknown" for any you cannot read. Then report to me (the coordinator) what you planned or cut.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900 (Release worker, plans only so far)
Skill: release
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T09:00:00Z
Session: the harness's record for w-00-0900 in .scratch/harness/workers.md
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
Check-in arranged at 2026-11-03T09:20:00Z: every 1 hour (the Boundary record's interval), into the coordinator, through the dry-run harness (docs/dev-skills/harness.md). None arranged earlier was running (.scratch/harness/checkins.md was empty).
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular
Brief:
~~~
Build the Spec .scratch/issues/10-farewell.md (Add a farewell command) with the `implement-spec` skill (load it by name),
on the regular tier (model: <model>, the `model-tiers` default). Review level: Deep (the issue names it).

- Repo: <runs>/runs/branch-deliver/repo (main).
- Spec: .scratch/issues/10-farewell.md; its Tickets: .scratch/issues/11-bye-code.md, .scratch/issues/12-bye-usage.md.
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet). Release: .scratch/issues/40-release-m1-r1.md.

Boundaries are the Boundary record's (docs/dev-skills/boundaries.md); a question about one comes to me, the coordinator.
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md). Run `bash test.sh` before each push.
Merge-time steps are in CLAUDE.md: if your pull request changes a file under `skills/`, ask me for its version number just
before merging and make the bump the last commit; one that changes no such file merges with no bump.

In your report on the issue, record the plugin load source and version you actually loaded, your permission and
sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. Report to me
when you ask for a version, when the pull request merges, and when anything blocks you.
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
Session: the harness's record for w-10-0920 in .scratch/harness/workers.md
~~~

## Event 3

## Event 4

### 7. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- version hand-out -->
Version 0.4.0 for #7: merge it next, with the bump as its last commit.

Main's `VERSION` is 0.3.0; #7 changes `skills/greeting/SKILL.md` with a new farewell rule (a new skill rule), so the minor is raised. No other number is out and no pause is in effect.
~~~

### 8. Message a worker
Worker: w-10-0920
Body:
~~~
Your version number for #7 is 0.4.0 (recorded on .scratch/issues/10-farewell.md): main's VERSION 0.3.0 raised minor, for the
new farewell rule in skills/greeting/SKILL.md. Merge #7 next, with the VERSION bump to 0.4.0 as its last commit, then report to me.
~~~

## Event 5

### 9. Edit an issue body
Issue: .scratch/issues/20-quiet.md
Body:
~~~
`--quiet` before any command prints nothing and keeps the exit code. Follows the `greeting` skill (`skills/greeting/SKILL.md`) for how messages are printed: every message, farewells included, goes through its one `say` function, so `--quiet` silences them there, `bye` included. Model tier: regular.

_Re-read after #7 merged (version 0.4.0): the `greeting` skill now prints every message through one `say` function, so this Ticket names it and `bye`._
~~~

### 10. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular
Brief:
~~~
Build the lone Ticket .scratch/issues/20-quiet.md (Add a --quiet flag) with the `implement` skill (load it by name),
on the regular tier (model: <model>, the `model-tiers` default). No Review level is named.

- Repo: <runs>/runs/branch-deliver/repo (main, now at version 0.4.0).
- Ticket: .scratch/issues/20-quiet.md (re-read after #7 merged: it now names the greeting skill's `say` function).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet). Release: .scratch/issues/40-release-m1-r1.md.

Boundaries are the Boundary record's (docs/dev-skills/boundaries.md); a question about one comes to me, the coordinator.
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md). Run `bash test.sh` before each push.
Merge-time steps are in CLAUDE.md: if your pull request changes a file under `skills/`, ask me for its version number just
before merging and make the bump the last commit; one that changes no such file merges with no bump.

In your report on the issue, record the plugin load source and version you actually loaded, your permission and
sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. Report to me
when you ask for a version, when the pull request merges, and when anything blocks you.
~~~

### 11. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1055
Skill: implement
Model tier: regular (<model>)
Review level: none
Started: 2026-11-03T10:55:00Z
Session: the harness's record for w-20-1055 in .scratch/harness/workers.md
~~~

## Event 6

### 12. Message a worker
Worker: w-20-1055
Body:
~~~
The check-in found your pull request #8 ready since 11:55Z with no report, so I read it as ready to merge. It changes
src/greet.sh and test.sh only, no file under skills/, so by CLAUDE.md's merge-time steps it gets no version number:
merge #8 with no VERSION bump, close .scratch/issues/20-quiet.md as its build skill says, then report to me.
~~~

## Event 7

### 13. Start a worker
Issue: .scratch/issues/40-release-m1-r1.md
Skill: release
Tier: premium
Brief:
~~~
Run the `release` skill (load it by name) for Milestone 1, on the premium tier (model: <model>, the `model-tiers` default).

- Repo: <runs>/runs/branch-deliver/repo (main, version 0.4.0).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet).
- Release doc: docs/dev-skills/release.md.
- Last release issue cut: none yet. The open release issue is .scratch/issues/40-release-m1-r1.md (Release Milestone 1 · Release 1);
  every issue carrying its label is now closed (#7 merged for 10-farewell.md and its Tickets, #8 for 20-quiet.md).

Let the skill's "Find where you are" decide whether you cut a Release or plan the next one; this brief overrides none of it.
Boundaries are the Boundary record's (docs/dev-skills/boundaries.md); a question about one is the user's, so bring it to me.
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md).

In your report on the release issue, record the plugin load source and version you actually loaded, your permission
and sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. Then report
to me (the coordinator) what you cut and planned, and anything that blocks the cut.
~~~

### 14. Comment on an issue
Issue: .scratch/issues/40-release-m1-r1.md
Body:
~~~
<!-- team-lead start -->
Worker: w-40-1220 (Release worker)
Skill: release
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T12:20:00Z
Session: the harness's record for w-40-1220 in .scratch/harness/workers.md
~~~

## Event 8

## Event 9

### 15. Comment on an issue
Issue: .scratch/issues/40-release-m1-r1.md
Body:
~~~
<!-- team-lead wait -->
Waiting at 2026-11-03T13:30:00Z: w-40-1220 cut Milestone 1 · Release 1 and planned no next Release, because the last open feature, 25-hello-doc.md (Document the commands in the README), is blocked by 35-readme-tool.md (Pick the README format checker), an issue outside the Milestone. No Release worker starts again until that blocker or the feature changes, or the user writes.
~~~

### 16. Message the user
Body:
~~~
Milestone 1 waits: Release 1 is cut, but no next Release could be planned, because the last feature, 25-hello-doc.md (Document the commands in the README), is blocked by 35-readme-tool.md (Pick the README format checker, outside the Milestone); nothing more starts until that blocker changes or you write.
~~~

## Event 10

### 17. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium
Brief:
~~~
Run the `release` skill (load it by name) for Milestone 1, on the premium tier (model: <model>, the `model-tiers` default).

- Repo: <runs>/runs/branch-deliver/repo (main, version 0.4.0).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet).
- Release doc: docs/dev-skills/release.md.
- Last release issue cut: .scratch/issues/40-release-m1-r1.md (Release Milestone 1 · Release 1, closed 13:28Z). Its planning
  waited on 35-readme-tool.md, which blocked 25-hello-doc.md; the user closed 35-readme-tool.md at 13:50Z.

Let the skill's "Find where you are" decide whether you cut a Release or plan the next one; this brief overrides none of it.
Boundaries are the Boundary record's (docs/dev-skills/boundaries.md); a question about one is the user's, so bring it to me.
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md).

In your report on the release issue (or on the Milestone issue if you open none), record the plugin load source and
version you actually loaded, your permission and sandbox settings, and a readable session usage reference, writing
"unknown" for any you cannot read. Then report to me (the coordinator) what you planned.
~~~

### 18. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-1400 (Release worker, plans only so far)
Skill: release
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T14:00:00Z
Session: the harness's record for w-00-1400 in .scratch/harness/workers.md
The wait recorded on 40-release-m1-r1.md at 13:30Z ended: the user closed its blocker 35-readme-tool.md at 13:50Z.
~~~

## Event 11

### 19. Start a worker
Issue: .scratch/issues/25-hello-doc.md
Skill: implement
Tier: cheap
Brief:
~~~
Build the lone Ticket .scratch/issues/25-hello-doc.md (Document the commands in the README) with the `implement` skill
(load it by name), on the cheap tier (model: <model>, the `model-tiers` default; the issue's Model tier line is cheap). No Review level is named.

- Repo: <runs>/runs/branch-deliver/repo (main, version 0.4.0).
- Ticket: .scratch/issues/25-hello-doc.md; its blocker 35-readme-tool.md is closed.
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet). Release: .scratch/issues/41-release-m1-r2.md.

Boundaries are the Boundary record's (docs/dev-skills/boundaries.md); a question about one comes to me, the coordinator.
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md). Run `bash test.sh` before each push.
Merge-time steps are in CLAUDE.md: if your pull request changes a file under `skills/`, ask me for its version number just
before merging and make the bump the last commit; one that changes no such file merges with no bump.

In your report on the issue, record the plugin load source and version you actually loaded, your permission and
sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. Report to me
when you ask for a version, when the pull request merges, and when anything blocks you.
~~~

### 20. Comment on an issue
Issue: .scratch/issues/25-hello-doc.md
Body:
~~~
<!-- team-lead start -->
Worker: w-25-1420
Skill: implement
Model tier: cheap (<model>)
Review level: none
Started: 2026-11-03T14:20:00Z
Session: the harness's record for w-25-1420 in .scratch/harness/workers.md
~~~

## Event 12

## Event 13

### 21. Message a worker
Worker: w-25-1420
Body:
~~~
Check-in at 16:00Z: your last activity on .scratch/issues/25-hello-doc.md was the commit "readme: hello and bye" on t25 at
14:40Z, with no comment or pull request since. Where are you, and what blocks you? Answer with a comment on
.scratch/issues/25-hello-doc.md.
~~~

### 22. Comment on an issue
Issue: .scratch/issues/25-hello-doc.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-25-1420 at 2026-11-03T16:00:00Z: the check-in found it silent since 2026-11-03T14:40:00Z (last commit "readme: hello and bye" on t25; no comment, no pull request; the harness reads it idle since 14:41Z). Asked where it is and what blocks it, answered by a comment on this issue.
~~~

## Event 14

### 23. Stop a worker
Worker: w-25-1420

## Event 15

### 24. Start a worker
Issue: .scratch/issues/25-hello-doc.md
Skill: implement
Tier: cheap
Brief:
~~~
Build the lone Ticket .scratch/issues/25-hello-doc.md (Document the commands in the README) with the `implement` skill
(load it by name), on the cheap tier (model: <model>, the `model-tiers` default; the issue's Model tier line is cheap). No Review level is named.

You take over from worker w-25-1420, which went silent after 14:40Z and was stopped (the harness read it stopped at 17:03Z).
Resume from its pushed branch `t25` (last commit 7006f51 "readme: hello and bye", 14:40Z) and from the tracker: the issue,
its comments and any pull request for `t25` (none was open at 17:05Z). Keep what is pushed; do not start the branch over.

- Repo: <runs>/runs/branch-deliver/repo (main, version 0.4.0).
- Ticket: .scratch/issues/25-hello-doc.md; its blocker 35-readme-tool.md is closed.
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet). Release: .scratch/issues/41-release-m1-r2.md.

Boundaries are the Boundary record's (docs/dev-skills/boundaries.md); a question about one comes to me, the coordinator.
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md). Run `bash test.sh` before each push.
Merge-time steps are in CLAUDE.md: if your pull request changes a file under `skills/`, ask me for its version number just
before merging and make the bump the last commit; one that changes no such file merges with no bump.

In your report on the issue, record the plugin load source and version you actually loaded, your permission and
sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. Report to me
when you ask for a version, when the pull request merges, and when anything blocks you.
~~~

### 25. Comment on an issue
Issue: .scratch/issues/25-hello-doc.md
Body:
~~~
<!-- team-lead start -->
Worker: w-25-1705
Skill: implement
Model tier: cheap (<model>)
Review level: none
Started: 2026-11-03T17:05:00Z
Session: the harness's record for w-25-1705 in .scratch/harness/workers.md
Takes over from w-25-1420; its stop read back as `stopped since 2026-11-03T17:03:00Z` in .scratch/harness/workers.md, at 2026-11-03T17:05:00Z.
Resumes from branch t25 (7006f51) and the tracker. Replaced after the nudge at 16:00Z found it still silent at the 17:00Z check-in.
~~~

## Event 16

### 26. Message a worker
Worker: w-25-1705
Body:
~~~
The check-in found your pull request #11 ready since 17:50Z with no report, so I read it as ready to merge. It changes
README.md only, no file under skills/, so by CLAUDE.md's merge-time steps it gets no version number: merge #11 with no
VERSION bump, close .scratch/issues/25-hello-doc.md as its build skill says, then report to me.
~~~

## Event 17

### 27. Start a worker
Issue: .scratch/issues/41-release-m1-r2.md
Skill: release
Tier: premium
Brief:
~~~
Run the `release` skill (load it by name) for Milestone 1, on the premium tier (model: <model>, the `model-tiers` default).

- Repo: <runs>/runs/branch-deliver/repo (main, version 0.4.0).
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1: goodbye and quiet).
- Release doc: docs/dev-skills/release.md.
- Last release issue cut: .scratch/issues/40-release-m1-r1.md (Release Milestone 1 · Release 1). The open release issue is
  .scratch/issues/41-release-m1-r2.md (Release Milestone 1 · Release 2); every issue carrying its label is now closed
  (#11 merged for 25-hello-doc.md). Every planned feature of the Milestone is now merged, so this is its final Release.

Let the skill's "Find where you are" decide whether you cut a Release or plan the next one; this brief overrides none of it.
Boundaries are the Boundary record's (docs/dev-skills/boundaries.md); a question about one is the user's, so bring it to me.
Do every tracker read and write with the tracker doc's operations (docs/dev-skills/issue-tracker.md).

In your report on the release issue, record the plugin load source and version you actually loaded, your permission
and sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. Then report
to me (the coordinator) what you cut and planned, and anything that blocks the cut.
~~~

### 28. Comment on an issue
Issue: .scratch/issues/41-release-m1-r2.md
Body:
~~~
<!-- team-lead start -->
Worker: w-41-1810 (Release worker, final cut)
Skill: release
Model tier: premium (<model>)
Review level: none
Started: 2026-11-03T18:10:00Z
Session: the harness's record for w-41-1810 in .scratch/harness/workers.md
~~~

## Event 18

### 29. End a check-in

### 30. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead check-in -->
Check-in ended at 2026-11-03T18:40:00Z: delivery reached the Milestone review gate (every planned feature merged; the final Release, Milestone 1 · Release 2, cut by w-41-1810). The end was asked of the harness at this wake; its read-back (.scratch/harness/checkins.md listing no check-in) is not readable until the harness moves, so it is still to be read at the next wake. At 18:40Z the file still lists "Every 1 hour into the coordinator, on the hour."
~~~

### 31. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- milestone report -->
## Milestone report — ready for user review

Agreement: the Milestone issue body as planned (no change recorded since planning; Startup verification comment 2026-11-03T08:30Z). Report time: 2026-11-03T18:40:00Z.

### 1. Outcomes

| Feature | Accepted when | Merge record | Criterion |
|---|---|---|---|
| 1. 10-farewell.md Add a farewell command (Spec; Tickets 11-bye-code.md, 12-bye-usage.md) | `greet.sh bye Ada` prints `Goodbye, Ada!` | PR #7 (.scratch/pulls/7.md) State: merged 10:52Z, changed `skills/greeting/SKILL.md`, `src/greet.sh`, `test.sh`; version 0.4.0 (hand-out on 10-farewell.md, 10:40Z); Spec and both Tickets closed | **unmet on main as read**: run at 18:40Z, `bash src/greet.sh bye Ada` prints the usage line and exits 2 |
| 2. 20-quiet.md Add a --quiet flag (lone Ticket) | `--quiet` prints nothing and keeps the exit code | PR #8 State: merged 12:15Z, changed `src/greet.sh`, `test.sh`, no version; issue closed | **unmet on main as read**: `bash src/greet.sh --quiet hello Ada` prints the usage line and exits 2 |
| 3. 25-hello-doc.md Document the commands (lone Ticket) | the README lists `hello` and `bye` | PR #11 State: merged 18:08Z, changed `README.md`, no version; issue closed | **unmet on main as read**: README.md on main holds only `# greeter` |

- Every feature above is merged and its issue closed: the pull request records say merged and every issue is closed, but **git does not confirm it**: main is still at 9f07488 ("greeter at Milestone 1 start"), and branches t10, t20 and t25 are not merged into it. Only `VERSION` (0.4.0) and the farewell rule in `skills/greeting/SKILL.md` show on main's checkout. The user should check where the merged code is before accepting.
- No other end-of-Milestone check was run.

### 2. Parked and maintenance

- Nothing parked. One stall: 25-hello-doc.md's first worker w-25-1420, silent since 14:40Z, nudged at 16:00Z, still silent at 17:00Z, stopped (read back `stopped` 17:03Z) and replaced by w-25-1705 at 17:05Z; no writer remains.
- Release issues: 40-release-m1-r1.md (closed 13:28Z) and 41-release-m1-r2.md (closed 18:38Z) have no Release notes comment and no end-of-Release pass record, and `CHANGELOG.md` on main has no entry (a branch t40 holds "changelog: Milestone 1 · Release 1", unmerged; no branch t41 exists). Both release issues were written before the Order list and carry their own release label. This project does not run `triage`.
- Maintenance issues left open: none recorded.

### 3. User messages

| Time | Source | Message | Kind |
|---|---|---|---|
| 13:50Z | comment on 35-readme-tool.md | "Picked the checker; closing." (closed the issue) | unplanned step-in: it cleared the blocker of 25-hello-doc.md after the coordinator's 13:30Z wait message; 25-hello-doc.md was blocked, not parked |

Read: every issue and pull request file. Not readable: worker session histories (the dry-run harness keeps none). Please check this inventory at the review.

### 4. Time and tokens

| Worker | Kind | Start–end (UTC) | Elapsed |
|---|---|---|---|
| w-00-0900 | Release (planned Release 1) | 09:00–09:19 | 19 min |
| w-10-0920 | implement-spec, 10-farewell.md | 09:20–10:53 | 1 h 33 min |
| w-20-1055 | implement, 20-quiet.md | 10:55–12:16 | 1 h 21 min |
| w-40-1220 | Release (cut Release 1) | 12:20–13:28 | 1 h 08 min |
| w-00-1400 | Release (planned Release 2) | 14:00–14:18 | 18 min |
| w-25-1420 | implement, 25-hello-doc.md | 14:20–17:03 (stopped) | 2 h 43 min |
| w-25-1705 | implement, 25-hello-doc.md (replacement) | 17:05–18:09 | 1 h 04 min |
| w-41-1810 | Release (cut Release 2) | 18:10–18:38 | 28 min |

Times are the harness's lines in .scratch/harness/workers.md. Delivery wall time 09:00–18:40Z: 9 h 40 min. Summed worker time: 8 h 54 min. Coordinator: Startup verification 08:00–08:30Z, then delivery to 18:40Z. Tokens: unknown for every worker and the coordinator (the harness records no session usage); skill-loading usage: unknown, no record to estimate from.

### 5. Versions and Startup verification

- Startup verification (comment 2026-11-03T08:30Z): Verdict ready; every row passed, Pause and resume not relied on (a message convention), failure not provoked, dry-run limits.
- Plugin load source and version, permission and sandbox settings per worker: unknown; every brief asked for them and no worker recorded them.
- Repo `VERSION`: 0.3.0 at start, 0.4.0 after #7.

### 6. Agent decisions

- Version 0.4.0 handed to #7 (minor: new farewell rule in the `greeting` skill), comment on 10-farewell.md at 10:40Z.
- Ticket re-read after #7: 20-quiet.md's body rewritten to name the skill's one `say` function and `bye` (proposed 10:55Z).
- #8 and #11 found ready but unreported at the 12:00Z and 18:00Z check-ins; their workers were told to merge with no version (no `skills/` file changed).
- Wait recorded on 40-release-m1-r1.md at 13:30Z (no next Release: 25-hello-doc.md blocked by 35-readme-tool.md); ended when the user closed 35-readme-tool.md.
- w-25-1420 replaced after nudge and confirmed stop (records on 25-hello-doc.md).
- No review records or `Agent-merged rules:` lines are readable on #7, #8 or #11 (no comments); design answers, if any, are not recorded.

### 7. Next Milestone

- Find out why the merged code of #7, #8 and #11 is not on main, and land it, before or as part of acceptance.
- Have the `release` cut write its changelog entry, notes and end-of-Release records (both Releases lack them).
- Make worker reports record load source, version and settings (none did).

Ready for the user's Milestone review; acceptance pending.
~~~

### 32. Message the user
Body:
~~~
Milestone 1 (goodbye and quiet) has reached its review: all three features are recorded merged (#7 as 0.4.0, #8, #11) and both Releases are cut, and the report is on .scratch/issues/00-milestone.md. Before you accept, note that main's checkout does not show the merged code: `greet.sh bye Ada`, `--quiet` and the README criteria all fail there, the Releases left no changelog entry or notes, and the check-in end is still to be read back. The Milestone stays open for your review.
~~~
