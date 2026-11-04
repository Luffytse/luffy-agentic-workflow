## Event 1

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium (Claude Code: <model>, the `model-tiers` default map)
Brief:
~~~
Run the `release` skill to plan the next Release of Milestone 1, inside the Milestone (release's "Inside a Milestone").
- Repo: <runs>/tlmain-deliver-stall/repo
- Milestone issue: .scratch/issues/00-milestone.md (goal, features in build order, acceptance, exclusions, its boundaries).
- Release doc: docs/dev-skills/release.md (pull requests bump; name `Milestone <m> · Release <n>`, label `release-m<m>-r<n>`).
- Last release issue cut: none; this is the Milestone's first Release, so no Triage batch or Release-end Retro planning
  exists for a Release just cut. This project does not run the `triage` skill.
- Boundary record: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md (dry run: every write is a block
  in .scratch/proposed-actions.md).
- Plan the next Release by release's own rule. Where an open release issue holds no issue yet, fill that one instead of
  opening another (for that issue this overrides release's "Rerun first"). Where nothing qualifies, open no release issue,
  label nothing and say so.
- In your report on the release issue (or the Milestone issue if you open none), record the plugin load source and version
  you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown"
  where you cannot read one. Preserve, as it becomes readable, the evidence the Milestone report gathers (milestone's
  reporting.md, "Gather the evidence").
- Report to the coordinator when the planning is done.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900 · Skill: release (plans Milestone 1's next Release) · Model tier: premium (<model>) · Review level: none
Started: 2026-11-03T09:00:00Z · Session: dry-run harness record, .scratch/harness/workers.md (line w-00-0900)
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
Check-in arranged at 2026-11-03T09:20:00Z: every 1 hour (the Boundary record's interval), into the coordinator, through the dry-run harness (docs/dev-skills/harness.md). None was running before (.scratch/harness/checkins.md empty).
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular (Claude Code: <model>, the `model-tiers` default map)
Brief:
~~~
Run the `implement-spec` skill on the Spec .scratch/issues/10-farewell.md (Tickets 11-bye-code.md, then 12-bye-usage.md).
- Repo: <runs>/tlmain-deliver-stall/repo
- Milestone issue: .scratch/issues/00-milestone.md (its boundaries and the Boundary record docs/dev-skills/boundaries.md apply;
  a pull request crossing one goes to the user). Release: .scratch/issues/40-release-m1-r1.md.
- Model tier: regular. Review level: Deep (named by the Spec).
- Tracker: docs/dev-skills/issue-tracker.md. Merge-time steps: CLAUDE.md "Merge-time steps" (11-bye-code.md changes
  skills/greeting/SKILL.md: ask the coordinator for the version number just before merging).
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox
  settings and a readable session usage reference, writing "unknown" where you cannot read one. Preserve, as it becomes
  readable, the evidence the Milestone report gathers (milestone's reporting.md, "Gather the evidence").
- Report to the coordinator when you open the pull request, when you ask to merge, when you finish, and when blocked.
~~~

### 6. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead start -->
Worker: w-10-0920 · Skill: implement-spec · Model tier: regular (<model>) · Review level: Deep
Started: 2026-11-03T09:20:00Z · Session: dry-run harness record, .scratch/harness/workers.md (line w-10-0920)
~~~

## Event 3

## Event 4

### 7. Message a worker
Worker: w-10-0920
Body:
~~~
Check-in at 2026-11-03T11:00Z: no commit on branch t10, no comment and no pull request since your start at 09:20Z, and the harness reads you idle since 09:40Z. Where are you on the Spec .scratch/issues/10-farewell.md, and what blocks you? Answer with a comment on .scratch/issues/10-farewell.md, then carry on.
~~~

### 8. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-10-0920 (implement-spec on .scratch/issues/10-farewell.md, branch t10) at 2026-11-03T11:00:00Z: silent since its start at 09:20Z (no commit, comment or pull request; harness reads idle since 09:40Z). Asked where it is and what blocks it, answered on its issue.
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
Parked at 2026-11-03T12:05:00Z. Reason: worker w-10-0920 (implement-spec) was silent from its start at 09:20Z, still silent after its nudge at 11:00Z, and the stop asked at 12:00Z does not read back: the harness says the stop was taken, but .scratch/harness/workers.md still reads `w-10-0920 ... idle since 2026-11-03T09:40:00Z`, not `stopped`.
A writer may remain: w-10-0920 is not read back stopped and could still push to branch t10.
Records: start, this issue's comment of 2026-11-03T09:20:00Z; nudge, .scratch/issues/00-milestone.md comment of 2026-11-03T11:00:00Z. Pull request: none opened; branch t10 has no commit.
Skipped until the user removes the `parked` label; before a fresh worker starts, w-10-0920 is stopped and read back first.
~~~

### 12. Message the user
Body:
~~~
Parked the Spec .scratch/issues/10-farewell.md: its worker w-10-0920 went silent, did not answer its nudge, and the stop I asked for does not read back (the harness still reads it idle, so it may still write to branch t10). Remove the `parked` label to lift it; delivery goes on with .scratch/issues/20-quiet.md.
~~~

### 13. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (Claude Code: <model>, the `model-tiers` default map)
Brief:
~~~
Run the `implement` skill on the lone Ticket .scratch/issues/20-quiet.md.
- Repo: <runs>/tlmain-deliver-stall/repo
- Milestone issue: .scratch/issues/00-milestone.md (its boundaries and the Boundary record docs/dev-skills/boundaries.md apply;
  a pull request crossing one goes to the user). Release: .scratch/issues/40-release-m1-r1.md.
- Model tier: regular. Review level: none named; agentic-review's Round 0 sizes it.
- Tracker: docs/dev-skills/issue-tracker.md. Merge-time steps: CLAUDE.md "Merge-time steps" (a pull request that changes a
  file under skills/ asks the coordinator for its version number just before merging).
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox
  settings and a readable session usage reference, writing "unknown" where you cannot read one. Preserve, as it becomes
  readable, the evidence the Milestone report gathers (milestone's reporting.md, "Gather the evidence").
- Report to the coordinator when you open the pull request, when you ask to merge, when you finish, and when blocked.
~~~

### 14. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1205 · Skill: implement · Model tier: regular (<model>) · Review level: none
Started: 2026-11-03T12:05:00Z · Session: dry-run harness record, .scratch/harness/workers.md (line w-20-1205)
~~~

## Event 7

### 15. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (Claude Code: <model>, the `model-tiers` default map)
Brief:
~~~
Run the `implement` skill on the lone Ticket .scratch/issues/20-quiet.md, resuming earlier work.
- You take over from w-20-1205, which failed at 2026-11-03T12:28Z. Resume from its pushed branch t20 (commit 58496e0
  "quiet: the --quiet flag") and the tracker: the issue, its comments and any pull request for branch t20. Keep what is
  pushed; build on it rather than starting over.
- Repo: <runs>/tlmain-deliver-stall/repo
- Milestone issue: .scratch/issues/00-milestone.md (its boundaries and the Boundary record docs/dev-skills/boundaries.md apply;
  a pull request crossing one goes to the user). Release: .scratch/issues/40-release-m1-r1.md.
- Model tier: regular. Review level: none named; agentic-review's Round 0 sizes it.
- Tracker: docs/dev-skills/issue-tracker.md. Merge-time steps: CLAUDE.md "Merge-time steps" (a pull request that changes a
  file under skills/ asks the coordinator for its version number just before merging).
- In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox
  settings and a readable session usage reference, writing "unknown" where you cannot read one. Preserve, as it becomes
  readable, the evidence the Milestone report gathers (milestone's reporting.md, "Gather the evidence").
- Report to the coordinator when you open the pull request, when you ask to merge, when you finish, and when blocked.
~~~

### 16. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-1230 · Skill: implement · Model tier: regular (<model>) · Review level: none
Started: 2026-11-03T12:30:00Z · Session: dry-run harness record, .scratch/harness/workers.md (line w-20-1230)
Takes over from w-20-1205; its end as read: `failed since 2026-11-03T12:28:00Z` (.scratch/harness/workers.md), at 2026-11-03T12:30:00Z. Resumes from branch t20 (58496e0).
~~~

## Event 8

## Event 9

### 17. Message a worker
Worker: w-20-1230
Body:
~~~
Check-in at 2026-11-03T14:00Z: your last commit on branch t20 was 13a4245 at 12:50Z, with no comment or pull request since, and the harness reads you idle since 12:51Z. Where are you on .scratch/issues/20-quiet.md, and what blocks you? Answer with a comment on .scratch/issues/20-quiet.md, then carry on.
~~~

### 18. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-20-1230 (implement on .scratch/issues/20-quiet.md, branch t20) at 2026-11-03T14:00:00Z: silent since its last commit 13a4245 at 12:50Z (no comment or pull request; harness reads idle since 12:51Z). Asked where it is and what blocks it, answered on its issue.
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
Parked at 2026-11-03T15:05:00Z. Reason: the feature's second stall. w-20-1205 failed at 12:28Z (an end without its result, which counts as a stall); its replacement w-20-1230 went silent after its last commit 13a4245 at 12:50Z, was still silent after its nudge at 14:00Z, and was stopped: read back `stopped since 2026-11-03T15:03:00Z` in .scratch/harness/workers.md.
No writer remains: w-20-1205 reads failed and w-20-1230 reads stopped.
Records: start of w-20-1205, this issue's comment of 2026-11-03T12:05:00Z; start of w-20-1230, this issue's comment of 2026-11-03T12:30:00Z; nudge, .scratch/issues/00-milestone.md comment of 2026-11-03T14:00:00Z. Pull request: none opened; the work is on branch t20 (58496e0, 13a4245).
Skipped until the user removes the `parked` label; a fresh worker then resumes from branch t20.
~~~

### 22. Message the user
Body:
~~~
Parked .scratch/issues/20-quiet.md after its second stall: w-20-1205 failed, and its replacement w-20-1230 went silent, ignored its nudge and was stopped (read back stopped). Its work stays on branch t20. Remove the `parked` label to lift it. Nothing else can start for now: both features of Milestone 1 · Release 1 are parked, and .scratch/issues/25-hello-doc.md is blocked by .scratch/issues/35-readme-tool.md, which is outside the Milestone.
~~~

## Event 12
