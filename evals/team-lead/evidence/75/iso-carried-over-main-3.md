# Milestone 1 delivery: what I do at each of the three wakes

## Event 1: hourly check-in at 11:00, nothing else changed

**What I read.** Release issue #40 is open, but no issue carries `release-m1-r1` any more, so there is no current Release. No worker is running, either a build worker or a Release worker. #20 is open, not parked, has no release label and has no open blocker, so it qualifies for Release planning. #25 also qualifies, because its only blocker, #20, is open at `ready-for-agent` and ranks ahead of it. There is no pause, and no merge-time request waits. The Milestone review gate does not hold, because neither feature has merged.

**Check-in.** No build worker is running, so there is nothing to put in the snapshot and no Release worker to read. The check-in finds nothing to act on, so it writes nothing and tells no one. It keeps running.

**Start work (step 2, Releases).** The conditions for planning a Release hold, so I start a Release worker.

1. **Worker started** through `worker-control`:
   - Skill: `release`.
   - Model tier: premium. That is the tier the release doc gives `release`. I start it on the model `model-tiers` maps premium to in this agent.
   - Review level: none.
   - Full brief:

   > Run the `release` skill to plan the next Release of Milestone 1.
   > - Milestone issue: #1 (label `milestone-1`). Goal: a quieter greeter. Planned features, in order: #20 "Add a `--quiet` flag" and #25 "Document the hello command". #25 is blocked by #20. Order rule: one at a time.
   > - Release doc: `docs/dev-skills/release.md`.
   > - Last release issue cut: none. No release issue has ever been closed; this is the repo's first Release.
   > - Facts to weigh:
   >   - Release issue #40 "Release Milestone 1 · Release 1" is open, and no issue carries its label `release-m1-r1` now.
   >   - At 10:20 the user wrote this in #40's `## Carried over` section: "#20 Add a --quiet flag: the user wants it in the next Release" and "#25 Document the hello command: waits for #20". At 10:21 the user removed the label from both issues.
   >   - Main holds PR #7 "chore: tidy the usage line", which closed no issue.
   >   - #40's issues were carried over by the user. It is not a release issue that "holds no issue yet", so this brief does not override `release`'s "Rerun first" or any other rule of `release`. `release`'s own rules decide what happens to #40 and to the carried-over issues, and the user's carry-over words must be honoured.
   >   - If nothing qualifies, open no release issue, label nothing and say so (`release` step 5).
   > - Do not start build workers.
   > - Report on #1, and on any release issue you write. In your report, record:
   >   - the plugin load source and version you actually loaded;
   >   - your permission and sandbox settings;
   >   - a readable session usage reference.
   >
   >   Say "unknown" wherever you cannot read one. As it becomes readable, preserve the evidence that `milestone`'s report gathers ("Gather the evidence").

2. **Tracker write:** **Comment on an issue** on #1 (this worker only plans):

   > `<!-- team-lead start -->`
   > Worker: `<id as worker-control returned it>`
   > Skill: `release`
   > Model tier: premium
   > Review level: none
   > Started: 11:00
   > Session: `<session/history reference from worker-control>`

No message goes to the user.

## Event 2: the user writes at 10:30, "Carried #20 and #25 over. Go on."

**What I read.** #20 and #25 are each also blocked by #35 "Pick a docs tool". #35 is open, at `needs-triage`, and is not a planned feature of the Milestone. There is no current Release and no worker running.

- No planned feature qualifies for a Release. #20's blocker #35 is not at `ready-for-agent`, so `release` cannot rank it ahead. #25 is blocked by #20 and by #35.
- So I start no Release worker, and there is nothing to build.
- No pause is in effect, so "Go on" resumes nothing and records nothing.
- No merge-time step waits, the Milestone review gate does not hold, and the check-in keeps running.

**Tracker writes:** none. **Workers started:** none.

**Message to the user** (one question, since it touches the Milestone's plan):

> Noted the carry-over of #20 "Add a `--quiet` flag" and #25 "Document the hello command". Nothing can start yet: both are now blocked by #35 "Pick a docs tool", an enhancement still at `needs-triage` that Milestone 1 (#1) does not list. #20 is also #25's blocker. To go on, one of these has to happen:
> - triage #35 to `ready-for-agent` and add it to Milestone 1 (with `milestone`), so a Release can plan it ahead of them; or
> - remove #35 as a blocker of #20 and #25.
>
> Which do you want?

## Event 3: hourly check-in at 11:00, and `w20` was never stopped

**What I read.**
- #20 still carries `release-m1-r1`, so #40 is the current Release.
- `w20` reads running through `worker-control`. Its branch `t20` is pushed, with its last commit at 10:50.
- `w25` reads stopped, and #25 is still blocked by #20.
- There is no pause, no merge-time request and no Release worker. The review gate does not hold.

**Check-in.** I run the snapshot over the one running build worker:

`python3 skill/team-lead/snapshot.py --worker 'id=w20;issue=20;branch=t20;started=<start time from w20's start record on #20>;state=running' --silent-after 60`

There is no `pr`, so the script looks the pull request up by branch. With a commit 10 minutes ago, the verdict is **active**, so nothing needs doing.

**Starts.** There is one slot: the smaller of the thread limit (2) and the "one at a time" order rule. `w20` holds it. #25 is blocked by #20 anyway. There is a current Release, so no Release worker starts.

**Result.** This is a quiet check-in: no tracker writes, no messages to a worker or to the user, and no workers started.
