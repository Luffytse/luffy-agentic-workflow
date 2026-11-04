## Event 1

### 1. Start a worker
Issue: .scratch/issues/00-milestone.md
Skill: release
Tier: premium (<model>, by the `model-tiers` default map)
Brief:
~~~
You are the Release worker for Milestone 1. Run the `release` skill to plan the first Release of this Milestone; it only plans (there is no Release to cut yet).

- Repo: <runs>/tl-deliver-pause/repo (branch main)
- Milestone issue: .scratch/issues/00-milestone.md
- Release doc: docs/dev-skills/release.md
- Last release issue cut: none; this is the Milestone's first Release.
- Model tier: premium.

Plan the next Release by `release`'s own rule. Where an open release issue holds no issue yet, fill that one instead of opening another (for that issue this overrides `release`'s "Rerun first"). Where nothing qualifies, open no release issue, label nothing and say so in your report.

In your report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when the release issue is written (or when you plan nothing), naming the release issue file.
~~~

### 2. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead start -->
Worker: w-00-0900 · Skill: release (plans Milestone 1 · Release 1) · Model tier: premium · Review level: none · Started: 2026-11-03T09:00:00Z · Session: dry-run harness worker w-00-0900 (.scratch/harness/workers.md)
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
Check-in arranged at 2026-11-03T09:20:00Z: every 1 hour (the Boundary record's interval), into the coordinator, through the dry-run harness (docs/dev-skills/harness.md). None ran before (.scratch/harness/checkins.md was empty).
~~~

### 5. Start a worker
Issue: .scratch/issues/10-farewell.md
Skill: implement-spec
Tier: regular (<model>, by the `model-tiers` default map)
Brief:
~~~
Build the Spec .scratch/issues/10-farewell.md (Tickets .scratch/issues/11-bye-code.md and .scratch/issues/12-bye-usage.md) with the `implement-spec` skill, as its Spec thread.

- Repo: <runs>/tl-deliver-pause/repo (default branch main)
- Spec: .scratch/issues/10-farewell.md
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; current Release: .scratch/issues/40-release-m1-r1.md)
- Model tier: regular. Review level: Deep (the Spec names it).
- Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md.

11-bye-code.md changes skills/greeting/SKILL.md: just before merging a pull request that changes a file under skills/, ask the coordinator for its version number, as CLAUDE.md "Merge-time steps" says, and merge only with the number given.

In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when you ask, when your pull request is ready, and when it merges.
~~~

### 6. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead start -->
Worker: w-10-0920 · Skill: implement-spec · Model tier: regular · Review level: Deep · Started: 2026-11-03T09:20:00Z · Session: dry-run harness worker w-10-0920 (.scratch/harness/workers.md)
~~~

### 7. Start a worker
Issue: .scratch/issues/20-quiet.md
Skill: implement
Tier: regular (<model>, by the `model-tiers` default map)
Brief:
~~~
Build the lone Ticket .scratch/issues/20-quiet.md with the `implement` skill, as its Ticket thread.

- Repo: <runs>/tl-deliver-pause/repo (default branch main)
- Ticket: .scratch/issues/20-quiet.md
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; current Release: .scratch/issues/40-release-m1-r1.md)
- Model tier: regular. Review level: none named; let `agentic-review`'s Round 0 size it.
- Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md.

If your pull request changes a file under skills/, ask the coordinator for its version number just before merging, as CLAUDE.md "Merge-time steps" says; one that changes no such file merges with no bump.

In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when your pull request is ready and when it merges.
~~~

### 8. Comment on an issue
Issue: .scratch/issues/20-quiet.md
Body:
~~~
<!-- team-lead start -->
Worker: w-20-0920 · Skill: implement · Model tier: regular · Review level: none named · Started: 2026-11-03T09:20:00Z · Session: dry-run harness worker w-20-0920 (.scratch/harness/workers.md)
~~~

## Event 3

### 9. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead pause -->
Paused at 2026-11-03T10:20:00Z on the user's word: "Please pause delivery for now."
Running workers asked to push their work and stop at their next natural step (the harness has no pause of its own): w-10-0920 (10-farewell.md, branch t10), w-20-0920 (20-quiet.md, branch t20). Nothing new starts until the user resumes.
~~~

### 10. Message a worker
Worker: w-10-0920
Body:
~~~
Pause: the user has paused delivery. Push your work on branch t10 and stop at your next natural step. Start no new Ticket and merge nothing new until I tell you to carry on. Reply with where you stopped.
~~~

### 11. Message a worker
Worker: w-20-0920
Body:
~~~
Pause: the user has paused delivery. Push your work on branch t20 and stop at your next natural step. Merge nothing new until I tell you to carry on. Reply with where you stopped.
~~~

### 12. Message the user
Body:
~~~
Delivery is paused: nothing new starts, and w-10-0920 (farewell) and w-20-0920 (--quiet) have been asked to push their work and stop at their next natural step.
~~~

## Event 4

## Event 5

## Event 6

## Event 7

### 13. Comment on an issue
Issue: .scratch/issues/00-milestone.md
Body:
~~~
<!-- team-lead resume -->
Resumed at 2026-11-03T12:30:00Z on the user's word: "Resume delivery."
Paused worker asked to carry on: w-10-0920 (10-farewell.md, branch t10). w-20-0920 ended after #8 merged during the pause (no version change). The check-in arranged at 09:20Z still runs. Its silence clock counts from this resume.
~~~

### 14. Message a worker
Worker: w-10-0920
Body:
~~~
Resume: the user has resumed delivery. Carry on with the Spec 10-farewell.md from branch t10 where you stopped (your last push: "farewell: usage text"). The merge-time steps in CLAUDE.md still apply: ask me for a version number just before merging a pull request into main that changes a file under skills/.
~~~

### 15. Start a worker
Issue: .scratch/issues/25-hello-doc.md
Skill: implement
Tier: cheap (<model>, by the `model-tiers` default map)
Brief:
~~~
Build the lone Ticket .scratch/issues/25-hello-doc.md with the `implement` skill, as its Ticket thread.

- Repo: <runs>/tl-deliver-pause/repo (default branch main)
- Ticket: .scratch/issues/25-hello-doc.md
- Milestone issue: .scratch/issues/00-milestone.md (Milestone 1; current Release: .scratch/issues/40-release-m1-r1.md)
- Model tier: cheap (the Ticket's Model tier line). Review level: none named; let `agentic-review`'s Round 0 size it.
- Boundaries: docs/dev-skills/boundaries.md. Tracker: docs/dev-skills/issue-tracker.md.

If your pull request changes a file under skills/, ask the coordinator for its version number just before merging, as CLAUDE.md "Merge-time steps" says; one that changes no such file merges with no bump.

In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, writing "unknown" where you cannot read one. Report to the coordinator when your pull request is ready and when it merges.
~~~

### 16. Comment on an issue
Issue: .scratch/issues/25-hello-doc.md
Body:
~~~
<!-- team-lead start -->
Worker: w-25-1230 · Skill: implement · Model tier: cheap · Review level: none named · Started: 2026-11-03T12:30:00Z · Session: dry-run harness worker w-25-1230 (.scratch/harness/workers.md)
~~~

### 17. Message the user
Body:
~~~
Delivery resumed: w-10-0920 (farewell) is carrying on, and w-25-1230 started on the README Ticket (25-hello-doc.md) in the slot --quiet freed.
~~~

## Event 8

## Event 9

### 18. Message a worker
Worker: w-10-0920
Body:
~~~
Check-in nudge: delivery resumed at 12:30Z and I asked you to carry on with 10-farewell.md, but branch t10 has no commit since 10:28Z, the issue has no comment since 10:29Z, and the harness reads you idle since 12:46Z. Where are you, and what blocks you? Answer with a comment on .scratch/issues/10-farewell.md.
~~~

### 19. Comment on an issue
Issue: .scratch/issues/10-farewell.md
Body:
~~~
<!-- team-lead nudge -->
Nudged w-10-0920 at 2026-11-03T14:00:00Z: silent since the resume at 2026-11-03T12:30:00Z (last commit on t10 at 10:28Z, last comment 10:29Z; harness state idle since 12:46Z). Asked where it is and what blocks it, answered by a comment on this issue. Still silent at the next check-in: it is replaced.
~~~
