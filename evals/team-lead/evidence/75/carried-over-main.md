Each event is worked from `STATE.md` on its own, with only that event's change applied.

**Where the two skills disagree.** In all three states, Release issue #40 is open. Every issue in its Order is either listed under `## Carried over` or still labelled. `CHANGELOG.md` has no entry for it.
- `team-lead` says a Release is "current" only while some issue carries its label. Read that way, events 1 and 2 have no current Release, and its "fill that one" rule could send a worker to re-plan #40.
- `release`'s own "Find where you are", case 2, says #40 is the current Release and must be cut, even when every issue was carried over. That cut lists only what merged since, which is #7.

`team-lead` says Release grouping belongs to `release`, so I follow `release`'s reading. The brief tells the worker not to fill #40 again and not to re-label the carried-over issues.

---

## Event 1: hourly check-in at 11:00, nothing else changed

1. **Check-in.** No build worker and no Release worker is running, so the snapshot has no rows. Nothing comes out of it, so the check-in itself writes nothing and tells no one.
2. **Start work.** There is no pause and no merge-time step waiting. #40 is due its cut: neither issue in its Order carries `release-m1-r1` any more, both are listed under `## Carried over`, and the changelog has no `## Milestone 1 · Release 1` entry. No Release worker is running. I start a **Release worker**:
   - **Skill:** `release`
   - **Model tier:** premium, which `release` names (<model> in Claude Code)
   - **No check-in to arrange.** This is not a build worker, and the 08:30 check-in still runs.
   - **Brief:**
     > Run the `release` skill in this repo, at the premium tier.
     > - Milestone issue: #1 (Milestone 1, "a quieter greeter").
     > - Release doc: `docs/dev-skills/release.md`.
     > - Last release issue cut: none. This is the repo's first Release.
     >
     > Open release issue #40, "Release Milestone 1 · Release 1", lists 1. #20 and 2. #25 in its Order. The user listed both under its `## Carried over` section at 10:20 and removed `release-m1-r1` from both at 10:21. No issue carries that label now.
     >
     > Start from the skill's "Find where you are" exactly as written. This brief does **not** override "Rerun first":
     > - Do not write a new plan into #40.
     > - Do not put `release-m1-r1` back on #20 or #25.
     >
     > As I read it, this is case 2:
     > - Step 1 is done: nothing is left with the label, and both issues are carried over.
     > - Step 2: changelog entry with "nothing shipped", plus "Also merged" for #7 "chore: tidy the usage line".
     > - Step 3: post the notes on #40 and close it.
     > - Step 4: run `triage`'s Triage batch and `retro-planning` for this Release.
     > - Step 5: plan Release 2. #20 and #25 are carried-over candidates, and the user wants #20 in the next Release.
     >
     > If the skill leads you somewhere else, follow the skill and say why in your report.
     >
     > - **Boundaries:** the Boundary record allows every irreversible action an agent may take.
     > - **Version numbers:** `CLAUDE.md` says the coordinator hands out a version number for each skill-changing pull request. If your changelog pull request needs one, ask me before you merge. Don't pick one yourself.
     >
     > In your report on #40, record:
     > - the plugin load source and the version you actually loaded
     > - your permission and sandbox settings
     > - a readable session usage reference
     >
     > Write "unknown" for any of these you can't read. Also keep the evidence `milestone`'s report gathers ("Gather the evidence") as it becomes readable.
3. **Tracker write.** "Comment on an issue" on **#40**:
   > `<!-- team-lead start -->`
   > Worker: `<id as worker-control returned it>`. Skill: `release`. Model tier: premium (<model>). Review level: none. Started: 11:00. Session: `<session reference>`.
4. **No message to the user.** Starting a Release worker needs none, and the user hears when it reports. No build worker starts while it runs.

## Event 2: the user writes at 10:30, "Carried #20 and #25 over. Go on." #20 and #25 are now also blocked by #35

I read the state again. There is no pause. #35 "Pick a docs tool" is open, at `needs-triage`, and the Milestone issue doesn't list it. Because #35 isn't at `ready-for-agent`, neither planned feature can be built in a new Release. The cut of #40 is still due, though, and the Triage batch inside that cut can reach #35. So:

1. **Start a Release worker:** `release`, premium (<model>). The brief is the same as in event 1, with this paragraph added:
   > Change since 10:21: #20 and #25 are each also blocked by #35 "Pick a docs tool" (open, `needs-triage`, an enhancement Milestone #1 does not list). Rank and propose it only by the skill's own rules, and add nothing to the Milestone. If step 5 takes nothing, follow "When nothing qualifies":
   > - open no release issue
   > - apply no label
   > - say in your report that #20 and #25 wait on #35, and why
2. **Tracker write.** "Comment on an issue" on **#40**:
   > `<!-- team-lead start -->`
   > Worker: `<id>`. Skill: `release`. Model tier: premium (<model>). Review level: none. Started: 10:30. Session: `<session reference>`.
3. **Message to the user:**
   > Going on. A Release thread is cutting Release 1 (#40). No Milestone feature shipped in it; it lists only #7 "chore: tidy the usage line". After the cut it plans Release 2.
   >
   > Heads-up: #20 "Add a `--quiet` flag" (adds the flag to the hello command) and #25 "Document the hello command" (writes its docs) are now both blocked by #35 "Pick a docs tool" (choose the tool the docs are written with). #35 is at `needs-triage` and Milestone 1 doesn't list it. So Release 2 probably can't take either feature until one of these happens:
   > - #35 reaches `ready-for-agent`. You may also want to add it to Milestone 1 with `milestone`.
   > - You remove the blocker link, if it's wrong. On #20 it looks doubtful.
4. **When the worker reports.** If it planned nothing while features are still open, I send the user one line saying which features wait and on what.

## Event 3: hourly check-in at 11:00. Only #25 was carried over, #20 keeps `release-m1-r1`, and `w20` is running with branch `t20` (last commit 10:50)

1. **Read the state.** #40 is the current Release, because #20 carries its label. #20 is open, not parked and unblocked. `worker-control` reads `w20` as running. `w25` reads stopped.
2. **Check-in snapshot:**
   `python3 <team-lead folder>/snapshot.py --worker 'id=w20;issue=20;branch=t20;started=<from w20's start record>;state=running' --silent-after 60`
   The commit at 10:50 is within the 60-minute window, and there's no pull request yet, so the row reads **active**: nothing to do.
3. **Start work.** Slots are the smaller of the thread limit (2) and the order rule (one at a time), so one slot, and `w20` holds it. #25 is carried over and still blocked by #20. No Release worker is due: there's a current Release and its labelled issue is still open.
4. **This is a quiet check-in.** No tracker write, no message to a worker or to the user, and no worker started.

One assumption here: I read "`w20` was never stopped" as meaning the user's stop at 10:15 covered only `w25`, which matches only #25 being carried over. If the user had in fact asked for `w20` to stop, the right step would be to stop it through `worker-control`, read the stop back, and tell the user. Nothing in that event's state says they did.

