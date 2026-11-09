**Event 1: hourly check-in at 11:00, nothing else changed**

1. **Read the state again.** No pause is in effect and no merge-time request is waiting. The Milestone review gate does not hold, because neither #20 nor #25 has merged.
2. **Check-in.** No build worker and no Release worker is running, so the snapshot has no rows and nothing calls for action. This is a quiet check-in: I write nothing and tell no one. The check-in arranged at 08:30 still runs, so I keep it and do not record it again.
3. **Next starts (step 2, Releases).** All three conditions for starting a Release worker hold:
   - no Release worker is running;
   - no open, unparked issue carries `release-m1-r1`, since the user removed it from #20 and #25;
   - release issue #40 is open and names Milestone #1.

   So I start a Release worker through `worker-control`:
   - **Skill:** `release`
   - **Model tier:** the tier `release` names. I cannot read `release` here, so I am guessing **regular**. I start it on the model `model-tiers` maps that tier to, unless the project's own map says otherwise.
   - **Brief:**
     > Run the `release` skill (load it by name) for Milestone 1.
     > - Milestone issue: #1 (label `milestone-1`).
     > - Release doc: `docs/dev-skills/release.md`.
     > - Last release issue cut: none. This repo has never cut a Release. The open release issue is #40 "Release Milestone 1 · Release 1" (label `release-m1-r1`).
     >
     > Let the skill's "Find where you are" decide whether you cut the current Release or plan the next one. Nothing in this brief overrides it. Boundaries are the Boundary record's. Report to me when you finish, or when the cut is blocked, or when you planned nothing.
     > In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference. Write "unknown" where you cannot read one. As it becomes readable, keep the evidence that `milestone`'s report gathers ("Gather the evidence").
4. **Tracker write.** I post a comment on #40 with **Comment on an issue**:
   ```
   <!-- team-lead start -->
   Worker: <id as worker-control returned it>. Skill: `release`. Model tier: regular. Review level: none. Started: 11:00. Session: <session or history reference>.
   ```
5. **Build workers.** None start while the Release worker runs. No issue carries the release label anyway.

**Event 2: the user writes at 10:30 "Carried #20 and #25 over. Go on." Both #20 and #25 are now also blocked by #35**

1. **Read the state again.** "Go on" is not a resume, because no pause is in effect, so I post no `resume` record. No merge-time step is waiting and the Milestone review gate does not hold.
2. **Check-in.** This wake is the user writing, not a check-in, so there are no findings.
3. **Next starts (step 2, Releases).** The conditions hold as in Event 1: no Release worker is running, no open issue carries `release-m1-r1`, and #40 is open and names Milestone #1. The #35 blocker does not change this, because the open release issue alone satisfies the "either" clause. I start the Release worker through `worker-control`:
   - **Skill:** `release`
   - **Model tier:** the tier `release` names, guessed as regular for the same reason as Event 1.
   - **Brief:** exactly as in Event 1.
4. **Tracker write.** I post the same `<!-- team-lead start -->` comment on #40, with the start time 10:30.
5. **Message to the user (one line):**
   > I've started a Release worker on #40 "Release Milestone 1 · Release 1". It decides whether to cut it or plan the next Release. Note that #20 "Add a --quiet flag" and #25 "Document the hello command" are now both blocked by #35 "Pick a docs tool" (open, `needs-triage`, not in Milestone #1), so the next Release may not be able to take them until #35 is triaged.

   If the worker later reports that it planned nothing while features are still open, I will tell you then and post a `wait` record.

**Event 3: hourly check-in at 11:00. Only #25 was carried over; #20 still has `release-m1-r1` and `w20` is running with branch `t20` pushed at 10:50**

1. **Read the state again.** No pause is in effect, no merge-time request is waiting, and the Milestone review gate does not hold.
2. **Check-in.** `w20` is the only running build worker, so I run the snapshot for it:
   `python3 skill/team-lead/snapshot.py --worker 'id=w20;issue=20;branch=t20;started=<UTC start time from w20's start record>;state=running' --silent-after 60`

   It has no report or resume time to pass, and the command finds the pull request from the branch. Its last commit at 10:50 is within the hour, so the row reads **active** and needs nothing. No Release worker is running.
3. **Next starts.**
   - **Release worker:** none. #20 is open, unparked and carries the label of open release issue #40.
   - **Build worker:** none. There is one slot (the smaller of the thread limit of 2 and "one at a time"), and `w20` holds it. The only Order entry that still carries the label is #20, and it already has a running worker. #25 has no label and is blocked by #20.
4. **Result.** This is a quiet check-in. There are no tracker writes, no messages to workers or the user, and no workers started.
