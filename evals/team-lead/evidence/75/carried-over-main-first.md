All three events are worked out below. I ran nothing, as `PROMPT.md` says.

In events 1 and 2, every issue in Release 1 (#40) has been carried over, so I start a worker to close out Release 1 and plan Release 2. In event 3, Release 1 still holds #20 and its worker is active, so the check-in does nothing.

Two ways the skill text could fall short in event 2:
- **The skill's literal text starts nothing.** Its definitions miss this case, and Release 1 would sit open with no worker to close it.
- **The fix is one sentence in my brief.** It stops the worker from writing Release 2's plan into #40.

## Event 1: hourly check-in at 11:00, no other change

**What I read:**
- **Pause:** none in effect.
- **Merge-time steps:** no request waits.
- **End-of-delivery check:** fails, because #20 and #25 are open and not parked.
- **Check-in:** no build workers are running, so there are no rows. No Release worker is running either. A quiet check-in writes nothing.
- **Is there a current Release?** `team-lead` says no. Its test is "an open release issue … whose label at least one issue carries", and no issue carries `release-m1-r1`.
- **Does a Release worker start?** Yes. No Release worker is running, and #20 is a planned feature that is open, not parked, has no release label and has no open blocker. The `release` skill's own "Find where you are" sorts out the rest. #40 is its case 2: every issue in its Order is listed under Carried over. Its step 1 says that case is "cut and closed as usual, also when no issue carries the label any more", and that Release ships only what merged since the last Release (PR #7). After that the worker plans Release 2.
- **Builds:** none start, because there is no current Release and a Release worker will be running.

**What I do, in order:**

1. **Start a worker.** I start it through `worker-control`, with the `release` skill, at the premium tier (<model>, using `model-tiers`' default map; the project gives no map of its own). Its full brief:

   > Run the `release` skill.
   > - Model tier: premium.
   > - Milestone issue: #1 (Milestone 1, label `milestone-1`).
   > - Release doc: `docs/dev-skills/release.md`.
   > - Last release issue cut: none. This is the repo's first Release.
   >
   > Open release issue: #40 "Release Milestone 1 · Release 1" (label `release-m1-r1`). Its Order lists #20 and #25. Its `## Carried over` section lists both, and no issue carries `release-m1-r1` any more.
   >
   > Run `release` from "Find where you are" exactly as it is written. #40 is the current Release (case 2): every issue in its Order is accounted for. So:
   > 1. Check that it is done.
   > 2. Write its changelog entry and run the cut steps. Nothing labelled shipped; PR #7 goes under "Also merged".
   > 3. Close #40 with its notes.
   > 4. Run the end-of-Release pass.
   > 5. Plan the next Release.
   >
   > #40 is not "a release issue that holds no issue yet". Do not write the next Release's plan into it. The next Release gets its own release issue, or none when nothing qualifies (step 5, "When nothing qualifies").
   >
   > Boundaries are the Boundary record's, and it allows every irreversible action an agent may take. Merge the changelog pull request yourself through `merging`. The release doc says pull requests carry the version bump, and a changelog pull request changes no skill, so ask me for a version number only if yours does change one.
   >
   > When you finish, report to me:
   > - that #40 is closed, with its notes;
   > - the next release issue, or that nothing qualified and why;
   > - each question or proposal waiting on the user.
   >
   > In your report comment on #40, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference. Write "unknown" where you cannot read one. Keep your start time, end time and session link readable for the Milestone report.

2. **Post the start record.** I write it on #40 with **Comment on an issue**:

   > `<!-- team-lead start -->`
   > Worker `<id as worker-control returned it>`, skill `release`, model tier premium, no Review level, started 11:00, session `<reference worker-control returned>`. It cuts Release 1 (#40, every issue carried over) and plans the next Release.

There is no message to the user. The hourly check-in already exists and keeps running.

## Event 2: the user writes at 10:30, "Carried #20 and #25 over. Go on."

The one change: #20 and #25 are each also blocked by #35 "Pick a docs tool". #35 is open, at `needs-triage`, and Milestone 1 does not list it.

**What I read:**
- **The user's words:** neither a pause nor a resume, and there is no pause to lift. They confirm what the tracker already shows, so there is nothing to record.
- **End-of-delivery check:** fails.
- **Does a Release worker start under the planning rule?** No. #20 is now blocked by #35, which is not at `ready-for-agent`, so `release` won't rank it. #25 is blocked by #20 and #35.
- **Does one start under the cut rule?** `team-lead`'s other rule ("every issue carrying the current Release's label is closed") also doesn't fire, because `team-lead` sees no current Release.
- **My reading:** read literally, nothing starts, and #40 stays open with no worker to cut it. `team-lead` leaves Release grouping to `release`, and `release` says a fully carried-over Release is cut and closed. So I start a Release worker to cut it.
- **Why the cut matters now:** its end-of-Release Triage batch is also what will look at #35. Its planning step will most likely find nothing that qualifies, and when nothing qualifies it opens no release issue.
- **Builds:** none start.

**What I do, in order:**

1. **Start a worker.** Same skill and tier as event 1, through `worker-control`. The brief is event 1's text with one paragraph added after the "Open release issue" paragraph:

   > The user wrote at 10:30: "Carried #20 and #25 over. Go on."

   It ends with the same "When you finish, report to me" paragraph as in event 1.

2. **Post the start record** on #40, as in event 1, with start time 10:30.

3. **Message the user:**

   > Release 1 (#40) has everything carried over. I've started a Release worker to cut it: a changelog entry for PR #7, then close it, run the triage and retro pass, and plan Release 2.
   >
   > Heads-up: #20 "Add a --quiet flag" and #25 "Document the hello command" are both now blocked by #35 "Pick a docs tool". #35 is at `needs-triage` and isn't in Milestone 1, so no agent can take it. Until #35 is triaged and you decide whether it joins the Milestone (with `milestone`), Release 2 has nothing to plan and no build can start.

## Event 3: hourly check-in at 11:00

The one change: only #25 was carried over. #20 still carries `release-m1-r1`, and its build worker `w20` is still running, with branch `t20` pushed (last commit 10:50).

**What I read:**
- **Pause, merge-time steps, end-of-delivery check:** no pause, no request waiting, and the check fails.
- **Current Release:** #40 is now current, because #20 carries its label.
- **No cut:** #20 is still open, so it isn't every issue closed, and I start no Release worker.
- **Slots:** the smaller of the thread limit (2) and the order rule (one at a time) is 1. `w20` holds that slot.
- **#25:** it is carried over and outside this Release, so it gets nothing.

**Check-in:** I run the snapshot for the single running build worker:

`python3 <team-lead folder>/snapshot.py --worker 'id=w20;issue=20;branch=t20;started=<UTC time from w20's start record>;state=running' --silent-after 60`

There is no `pr` (the command finds it by branch) and no `reported` or `resumed`. The last commit, at 10:50, falls inside the one-hour window, so the row reads **active**, which needs no action.

**What I do:** nothing. This is a quiet check-in, so there are no tracker writes, no messages to a worker or the user, and no worker starts.

