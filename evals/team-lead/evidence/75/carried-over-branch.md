I didn't run anything. All three wakes are worked from `STATE.md` plus each event's single change, as `PROMPT.md` says. Placeholders in angle brackets (`<…>`) stand for values that only `worker-control` returns at start time.

## Event 1: hourly check-in, 11:00 (no other change)

**What I read.** Milestone #1 is open and the gate for ending delivery is closed, because #20 and #25 are open and not parked. No pause is in effect and no merge-time request waits. No worker is running, so the check-in has no rows to act on and writes nothing. The check-in itself is still running, so I keep it.

**Rule that applies (step 2, "Releases").** I start a Release worker when all of these hold:
- No Release worker is running.
- No open, unparked issue carries the label of an open release issue. Here nothing carries `release-m1-r1` any more.
- A release issue naming this Milestone is open. #40 is.

Whether that worker cuts Release 1 or plans the next one is decided by `release`'s "Find where you are". A Release whose issues were all carried over counts as the current Release and gets cut. The brief doesn't override that. No build worker may start while the Release worker runs.

**Actions, in order:**

1. **Start a worker** through `worker-control`:
   - Skill: `release`
   - Model tier: premium (the tier `release` names), which `model-tiers` maps to <model> in Claude Code. The project gives no tier map of its own.
   - No Review level.
   - Brief:
     > Run the `release` skill for this repo.
     > Milestone issue: #1 (label `milestone-1`), <link to #1>.
     > Release doc: `docs/dev-skills/release.md`.
     > Last release issue cut: none (this is the repo's first Release). The open release issue is #40 "Release Milestone 1 · Release 1", <link to #40>.
     > Let the skill's "Find where you are" decide what this run does; this brief overrides none of it.
     > In your report on the release issue, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference. Write "unknown" for any of these you cannot read. Report to me when you finish or when you are blocked.

2. **Tracker write: comment on #40** (the `start` record):
   ```
   <!-- team-lead start -->
   Worker: <id as worker-control returned it>
   Skill: release
   Model tier: premium (<model>)
   Review level: none
   Started: 2026-11-09 11:00
   Session: <session or history reference>
   ```

3. **No message to the user.** No build worker starts.

## Event 2: the user writes at 10:30, "Carried #20 and #25 over. Go on."
(Change: #20 and #25 are each also blocked by #35 "Pick a docs tool", which is open, at `needs-triage`, and not listed in the Milestone issue.)

**What I read.** The tracker matches what the user said: #40's `## Carried over` lists #20 and #25, and both have lost the label. No pause is in effect and the ending gate is still closed. The new #35 blockers don't change the Release-worker rule, because the open release issue #40 already meets it. Whether #20 can go into a later Release, given a blocker an agent can't take, is `release`'s call when it plans. I don't make that call.

**Actions, in order:**

1. **Start a worker**: `release` at premium (<model>), no Review level, with the same brief as in Event 1, word for word.
2. **Tracker write: comment on #40**: the same `start` record as in Event 1, with `Started: 2026-11-09 10:30`.
3. **Message to the user:**
   > Started a Release worker on #40 "Release Milestone 1 · Release 1". With #20 and #25 carried over, `release` decides whether to cut Release 1 and plan the next one. Heads-up: #20 "Add a --quiet flag" and #25 "Document the hello command" are both now blocked by #35 "Pick a docs tool". #35 is at `needs-triage` and isn't in Milestone 1, so no agent can build #20 or #25 until it's settled. I'll tell you what the Release worker reports.

No build worker starts.

## Event 3: hourly check-in, 11:00
(Change: only #25 was carried over. #20 still carries `release-m1-r1`, and its worker `w20` was never stopped. `w20` is running, and its branch `t20` is pushed with a commit at 10:50.)

**What I read.** I took "never stopped" to mean no stop was asked for in this version of events, so the user isn't waiting on a stop that didn't happen. No pause is in effect, no merge-time request waits, and the ending gate is closed.

**Releases.** I start no Release worker. #20 is open, unparked and still carries the label of open release issue #40, so the rule's condition fails.

**Building.** The build order is #40's Order entries that still carry its label, which leaves only #20. There is one slot, the smaller of the thread limit (2) and the order rule (one at a time). `w20` holds it. #25 is carried over and blocked by #20 anyway.

**Check-in.** I run the snapshot over the one running build worker:
```
python3 <team-lead folder>/snapshot.py --worker 'id=w20;issue=20;branch=t20;started=<UTC time from its start record>;state=running' --silent-after 60
```
The 10:50 commit on `t20` falls inside the 60-minute window, so the row reads **active** and calls for nothing. That makes this a quiet check-in.

**Actions:** none. There are no tracker writes, no messages to `w20` or the user, and no workers started.

