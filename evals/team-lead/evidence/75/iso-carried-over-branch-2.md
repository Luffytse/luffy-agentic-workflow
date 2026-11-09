# Event 1: hourly check-in at 11:00, no other change

**Reading the state.** Nothing is paused, so there is nothing to pause or resume. No merge-time request is waiting. The Milestone review gate does not hold, because #20 and #25 are both open. No build worker or Release worker is running, so the snapshot has no rows and the check-in is quiet. A quiet check-in writes nothing and tells no one.

**Next starts.** No worker is running. No open, unparked issue carries `release-m1-r1`, and release issue #40 for this Milestone is open. That calls for a Release worker. No `wait` record or earlier Release report stands in its way. Its own "Find where you are" step decides what it does. Here every issue of Release 1 was carried over, so it should cut #40 and plan the next Release. The brief does not override that. The check-in is already running, so I keep it and arrange nothing.

1. **Start a worker** through `worker-control`:
   - Skill: `release`
   - Model tier: premium, started on the model `model-tiers` maps premium to (no project map is given)
   - No Review level

   Brief:
   > Run the `release` skill for this repo's Milestone 1.
   > - Milestone issue: #1 (label `milestone-1`).
   > - Release doc: `docs/dev-skills/release.md`.
   > - Last release issue cut: none (this repo has never cut a Release). The open release issue is #40, "Release Milestone 1 · Release 1".
   > - Model tier: premium.
   >
   > Follow the skill's "Find where you are" to decide whether you cut the current Release, plan the next one, or both. This brief overrides none of it.
   >
   > In your report on the release issue, record:
   > - the plugin load source and version you actually loaded,
   > - your permission and sandbox settings,
   > - a readable session usage reference.
   >
   > Write "unknown" for any of these you cannot read. As it becomes readable, keep the evidence the `milestone` report gathers ("Gather the evidence").
   >
   > Report when you are done, or when the cut is blocked or you planned nothing.
2. **Comment on issue #40:**
   ```
   <!-- team-lead start -->
   Worker: <id as worker-control returned it>
   Skill: release
   Model tier: premium
   Started: 11:00 (PST) today
   Session: <session/history reference worker-control returned>
   ```
3. While this worker runs, I start no build worker. When it reports, I read #40 back.

# Event 2: the user writes at 10:30, "Carried #20 and #25 over. Go on." #20 and #25 are now also blocked by #35

**Reading the state.** "Go on" is not a pause or a resume, since no pause is in effect, so I record nothing for it. No merge-time step is waiting, the Milestone review gate does not hold, and this is not a check-in.

**Next starts.** The Release-worker condition holds through its first branch: release issue #40 for this Milestone is open. #35 matters only to the other branch (a planned feature that is unblocked, or blocked only by issues `release` ranks ahead of it), so it does not stop this start. I tell the user about #35 but leave the brief unchanged. The Release worker decides the planning.

1. **Start a worker** through `worker-control`:
   - Skill: `release`
   - Model tier: premium, on the model `model-tiers` maps premium to
   - No Review level
   - Brief: the same text as in Event 1, word for word.
2. **Comment on issue #40:**
   ```
   <!-- team-lead start -->
   Worker: <id as worker-control returned it>
   Skill: release
   Model tier: premium
   Started: 10:30 (PST) today
   Session: <session/history reference worker-control returned>
   ```
3. **Message to the user:**
   > Started a `release` worker on #40 "Release Milestone 1 · Release 1" (premium). Both features were carried over, so it should cut that Release and plan the next one.
   >
   > #20 "Add a `--quiet` flag" and #25 "Document the hello command" are now both blocked by #35 "Pick a docs tool". #35 is open and still at `needs-triage`, and Milestone 1 does not list it. The next Release may therefore plan nothing until #35 is triaged or settled. If that happens I'll tell you what it is waiting on.
4. I start no build worker while the Release worker runs.

# Event 3: hourly check-in at 11:00. Only #25 was carried over, #20 still carries `release-m1-r1`, and `w20` is running with branch `t20` pushed (commit at 10:50)

**Reading the state.** There is no pause and no merge-time request, and the Milestone review gate does not hold. Through `worker-control`, `w20` reads running and `w25` reads stopped.

**Next starts.** No Release worker starts, because #20 is open, unparked and carries the label of open release issue #40. The build order is #40's Order entries that still carry the label, which is only #20. There is one slot: the order rule is one at a time, which is smaller than the thread limit of 2. `w20` holds that slot, so nothing else starts.

1. **Run the snapshot** over the one running build worker. There is no open pull request, so I leave out `pr` and the script looks it up by branch:
   ```
   python3 skill/team-lead/snapshot.py --worker 'id=w20;issue=20;branch=t20;started=<UTC start time from w20's start record on #20>;state=running' --silent-after 60
   ```
2. **Act on the row.** The last commit is at 10:50, inside the 60-minute interval, so the row reads **active** and needs no action.
3. That makes this a quiet check-in: no tracker writes, no messages, no starts.
