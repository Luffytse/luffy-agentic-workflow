## Event 1

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium (Claude Code model: <model>, the `model-tiers` default)
Brief:
~~~
Run the `release` skill to plan the next Release of Milestone 1.
- Repo: <runs>/tl-deliver-stall/repo (main).
- Milestone issue: .scratch/issues/00-milestone.md (features and build order there).
- Release doc: docs/dev-skills/release.md. Tracker doc: docs/dev-skills/issue-tracker.md (dry run: every write is a block in .scratch/proposed-actions.md). Boundary record: docs/dev-skills/boundaries.md.
- Last release issue cut: none; this is the Milestone's first Release.
- If you find an open release issue that holds no issue yet, fill that one instead of opening another: for that issue this overrides `release`'s "Rerun first". If nothing qualifies, open no release issue, label nothing and say so.
- Tier: premium.
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference; write "unknown" where you cannot read one.
- Report to the coordinator when the planning is done, naming the release issue.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900 (as the dry-run harness names it)
Skill: release (plans Milestone 1's first Release)
Model tier: premium
Review level: none
Started: 2026-11-03T09:00:00Z
Session: dry-run harness, .scratch/harness/workers.md line w-00-0900
~~~

## Event 2

### 3. Arrange a check-in
Every: 1 hour (the Boundary record's check-in interval)
Into: coordinator

### 4. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead check-in -->
Check-in arranged at 2026-11-03T09:20:00Z through the dry-run harness: every 1 hour (the Boundary record's interval), into the coordinator. None ran before (.scratch/harness/checkins.md was empty).
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular (Claude Code model: <model>, the `model-tiers` default)
Brief:
~~~
Run the `implement-spec` skill to build the Spec .scratch/issues/10-farewell.md (Tickets 11-bye-code.md, then 12-bye-usage.md, which 11 blocks).
- Repo: <runs>/tl-deliver-stall/repo (main).
- Milestone issue: .scratch/issues/00-milestone.md. Current Release: .scratch/issues/40-release-m1-r1.md.
- Model tier: regular. Review level: Deep (the Spec names it).
- Tracker doc: docs/dev-skills/issue-tracker.md (dry run: every write is a block in .scratch/proposed-actions.md). Boundary record: docs/dev-skills/boundaries.md.
- 11-bye-code.md changes skills/greeting/SKILL.md: just before merging the Spec pull request, ask the coordinator for its version number (CLAUDE.md, "Merge-time steps").
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference; write "unknown" where you cannot read one.
- Report to the coordinator when you open the pull request, when you need a merge-time step, when blocked, and when done.
~~~

### 6. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead start -->
Worker: w-10-0920 (as the dry-run harness names it)
Skill: implement-spec
Model tier: regular
Review level: Deep
Started: 2026-11-03T09:20:00Z
Session: dry-run harness, .scratch/harness/workers.md line w-10-0920
~~~

## Event 3

## Event 4

### 7. Message a worker
Worker: w-10-0920
Body:
~~~
Check-in at 2026-11-03T11:00:00Z: nothing from you on 10-farewell.md since your start at 09:20 (no commit on t10, no comment, no pull request), and the harness reads you idle since 09:40. Where are you, and what blocks you? Answer with a comment on .scratch/issues/10-farewell.md, then carry on.
~~~

### 8. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-10-0920 at 2026-11-03T11:00:00Z: silent since its start at 2026-11-03T09:20:00Z (no commit on t10, no comment, no pull request); harness state idle since 09:40. Asked where it is and what blocks it, answered here.
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
Parked at 2026-11-03T12:05:00Z: the stop of w-10-0920 did not read back. The harness took the stop at 12:05, but .scratch/harness/workers.md still reads `w-10-0920 10-farewell.md branch t10: idle since 2026-11-03T09:40:00Z`, not `stopped`, so no replacement may start.
A writer may remain: w-10-0920 is not ended and could still push to t10 (nothing is pushed there yet).
Records: start 2026-11-03T09:20:00Z and nudge 2026-11-03T11:00:00Z, both on this issue. Pull request: none.
Its Tickets 11-bye-code.md and 12-bye-usage.md wait with it. To lift, remove the `parked` label; before a fresh worker starts, w-10-0920 is stopped and read back first.
~~~

### 12. Message the user
Body:
~~~
Parked .scratch/issues/10-farewell.md (the farewell Spec): its worker w-10-0920 went silent after a nudge, and its stop did not read back (the harness still reads it idle), so a writer may remain on branch t10. Remove the `parked` label to lift it. Delivery goes on with 20-quiet.md.
~~~

### 13. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (Claude Code model: <model>, the `model-tiers` default)
Brief:
~~~
Run the `implement` skill to build the lone Ticket .scratch/issues/20-quiet.md.
- Repo: <runs>/tl-deliver-stall/repo (main).
- Milestone issue: .scratch/issues/00-milestone.md. Current Release: .scratch/issues/40-release-m1-r1.md.
- Model tier: regular. No Review level named.
- Tracker doc: docs/dev-skills/issue-tracker.md (dry run: every write is a block in .scratch/proposed-actions.md). Boundary record: docs/dev-skills/boundaries.md.
- If your pull request changes a file under skills/, ask the coordinator for its version number just before merging (CLAUDE.md, "Merge-time steps"); otherwise merge with no bump.
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference; write "unknown" where you cannot read one.
- Report to the coordinator when you open the pull request, when you need a merge-time step, when blocked, and when done.
~~~

### 14. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1205 (as the dry-run harness names it)
Skill: implement
Model tier: regular
Review level: none
Started: 2026-11-03T12:05:00Z
Session: dry-run harness, .scratch/harness/workers.md line w-20-1205
~~~

## Event 7

### 15. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (Claude Code model: <model>, the `model-tiers` default)
Brief:
~~~
Run the `implement` skill to finish the lone Ticket .scratch/issues/20-quiet.md. You take over from w-20-1205, which failed at 2026-11-03T12:28:00Z.
- Resume from its pushed branch t20 (last commit 58496e0 "quiet: the --quiet flag") and the tracker: the issue, its comments, and its pull request if one exists under .scratch/pulls/. Keep what is pushed; build on it.
- Repo: <runs>/tl-deliver-stall/repo (main).
- Milestone issue: .scratch/issues/00-milestone.md. Current Release: .scratch/issues/40-release-m1-r1.md.
- Model tier: regular. No Review level named.
- Tracker doc: docs/dev-skills/issue-tracker.md (dry run: every write is a block in .scratch/proposed-actions.md). Boundary record: docs/dev-skills/boundaries.md.
- If your pull request changes a file under skills/, ask the coordinator for its version number just before merging (CLAUDE.md, "Merge-time steps"); otherwise merge with no bump.
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference; write "unknown" where you cannot read one.
- Report to the coordinator when you open the pull request, when you need a merge-time step, when blocked, and when done.
~~~

### 16. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1230 (as the dry-run harness names it)
Skill: implement
Model tier: regular
Review level: none
Started: 2026-11-03T12:30:00Z
Session: dry-run harness, .scratch/harness/workers.md line w-20-1230
Takes over from w-20-1205; its end as read: `failed since 2026-11-03T12:28:00Z` in .scratch/harness/workers.md, at 2026-11-03T12:30:00Z.
Resumes from branch t20 (58496e0).
~~~

## Event 8

## Event 9

### 17. Message a worker
Worker: w-20-1230
Body:
~~~
Check-in at 2026-11-03T14:00:00Z: nothing from you on 20-quiet.md since your commit 13a4245 on t20 at 12:50 (no comment, no pull request), and the harness reads you idle since 12:51. Where are you, and what blocks you? Answer with a comment on .scratch/issues/20-quiet.md, then carry on.
~~~

### 18. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-20-1230 at 2026-11-03T14:00:00Z: silent since its last commit on t20 at 2026-11-03T12:50:00Z (no comment, no pull request); harness state idle since 12:51. Asked where it is and what blocks it, answered here.
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
Parked at 2026-11-03T15:05:00Z: the feature's second stall. w-20-1205 failed at 12:28 and was replaced; its replacement w-20-1230 went silent after its last commit at 12:50, stayed silent after the nudge at 14:00, and was stopped. The stop reads back: .scratch/harness/workers.md shows `w-20-1230 20-quiet.md branch t20: stopped since 2026-11-03T15:03:00Z`.
No writer remains: w-20-1205 reads failed and w-20-1230 reads stopped.
Work so far is pushed on branch t20 (58496e0, 13a4245). Pull request: none.
Records on this issue: start of w-20-1205 at 2026-11-03T12:05:00Z, start of w-20-1230 at 2026-11-03T12:30:00Z (takes over from w-20-1205), nudge at 2026-11-03T14:00:00Z.
To lift, remove the `parked` label; a fresh worker then resumes from t20.
~~~

### 22. Message the user
Body:
~~~
Parked .scratch/issues/20-quiet.md (the --quiet flag) on its second stall: its first worker failed, and its replacement w-20-1230 went silent after a nudge and was stopped (read back stopped; no writer remains). Its work is pushed on branch t20. Remove the `parked` label to lift it. With 10-farewell.md also parked, nothing more in Release 1 can start, and 25-hello-doc.md waits for the next Release (it is also blocked by 35-readme-tool.md), so delivery is waiting on you.
~~~

## Event 12
