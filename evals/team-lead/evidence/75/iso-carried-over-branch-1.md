I didn't run anything. Each event below starts from `STATE.md` with only the change that event names. Placeholders in `<…>` stand for values `worker-control` would return.

## Event 1: hourly check-in at 11:00, no other change

1. **Read the state.** Milestone #1 is open and no pause is in effect. Release #40 is open, but no issue carries `release-m1-r1` any more. #20 and #25 are open, unparked and carry no release label. `worker-control` shows no worker running. There is no open pull request. `CHANGELOG.md` has no Release 1 heading.
2. **End-of-delivery check.** It fails: neither feature has merged. Nothing to do there.
3. **Check-in findings.** No build worker and no Release worker is running, so the snapshot has no rows. This is a quiet check-in: no record and no message. The check-in itself is still running, so I keep it.
4. **Next starts.** A Release worker is due. None is running, no open unparked issue carries the open release issue's label, and release issue #40 (which names this Milestone) is open. Whether it cuts #40 or plans the next Release is for `release` to decide, not the brief. I start no build worker while it runs.
   - **Worker started:** skill `release`, Model tier **premium** (the tier the release doc names). It runs on the model `model-tiers` maps premium to, started through `worker-control`.
   - **Brief:**
     > Run the `release` skill for this repo. Milestone issue: #1 (label `milestone-1`). Release doc: `docs/dev-skills/release.md`. Last release issue cut: none (this is the repo's first Release). Follow the skill's "Find where you are" to decide what to do. Model tier: premium. In your issue report, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference; write "unknown" for any you cannot read. Also keep, as it becomes readable, the evidence the `milestone` report gathers (its "Gather the evidence" list). Report to me when you finish or if you are blocked.
   - **Tracker write:** a comment on #40, the `start` record:
     > `<!-- team-lead start -->`
     > Worker: `<id returned by worker-control>`
     > Skill: `release`
     > Model tier: premium (`<model>`)
     > Review level: none
     > Started: 11:00
     > Session: `<session or history reference>`
5. **No message to the user.**

## Event 2: the user writes at 10:30, "Carried #20 and #25 over. Go on."

Change: #20 and #25 are each also blocked by #35 "Pick a docs tool" (open, `needs-triage`, not in the Milestone).

1. **Read the state.** As in event 1, plus #35 now blocks #20 and #25. No worker is running and the check-in is still running.
2. **Pause or resume.** None. No pause is in effect, so "Go on" is not a resume and gets no `resume` record.
3. **End-of-delivery check.** It fails. There are no merge-time steps and no check-in findings to act on.
4. **Next starts.** The same Release worker as in event 1 is due. The rule only needs release issue #40 to be open, so the blockers on #20 and #25 don't stop it.
   - **Worker started:** skill `release`, premium tier, started through `worker-control`.
   - **Brief:** the same as event 1, with one line added before the last sentence:
     > The user wrote at 10:30: "Carried #20 and #25 over. Go on."
   - **Tracker write:** a comment on #40, the same `start` record as event 1, with `Started: 10:30`.
5. **Message to the user:**
   > Starting a Release worker (`release`, premium) on Release #40. Note: #20 Add a --quiet flag and #25 Document the hello command are now both blocked by #35 Pick a docs tool. #35 is open at `needs-triage` and isn't in Milestone #1, so neither feature can be built until it closes. I'll tell you what the Release worker plans.

## Event 3: hourly check-in at 11:00

Change: only #25 was carried over. #20 still carries `release-m1-r1`. Build worker `w20` is running, and branch `t20` is pushed with a commit at 10:50.

1. **Read the state.** Release #40 is open, and #20 still carries its label. #25 has no label and is blocked by #20. `worker-control` shows `w20` running. There is no pull request on `t20`.
2. **End-of-delivery check.** It fails. There are no merge-time steps.
3. **Check-in.** I run the snapshot for `w20`:
   `python3 skill/team-lead/snapshot.py --worker 'id=w20;issue=20;branch=t20;started=<w20 start time from its start record>;state=running' --silent-after 60`
   - The 10:50 commit falls within the 60-minute window, so the verdict is **active** and there is nothing to do.
   - It is a quiet check-in: no record, no nudge, no message.
4. **Next starts.** None.
   - No Release worker: an open, unparked issue (#20) still carries the open release issue's label.
   - Slots: the thread limit is 2 and the order rule is one at a time, so there is one slot, and `w20` holds it.
   - #25 isn't in the build order: it carries no label and is blocked by #20.
5. **No tracker writes, no worker messages, no worker starts, no message to the user.**
