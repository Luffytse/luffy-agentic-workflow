# Milestone 1 delivery: what I do at each of the three wakes

## Event 1: hourly check-in at 11:00, nothing else changed

**What the state shows.** No build or Release worker is running. Release issue #40 is open, but no issue carries its label `release-m1-r1`. So by `team-lead`'s definition there is no current Release. #20 is open, not parked, has no release label and has no open blocker. #25 is blocked only by #20, which comes ahead of it, is `ready-for-agent` and is not parked. So step 2 calls for a Release worker.

`team-lead` has a rule for an open release issue that holds no issue yet: the Release worker fills it instead of opening another. That rule does not fit #40. #40 was not left unfilled. The user emptied it on purpose: they removed both labels and wrote in `## Carried over` that #20 goes to "the next Release" and that #25 waits for #20. So the worker does not fill #40. It cuts #40, which now holds only #7 "chore: tidy the usage line", and then plans Release 2. The check-in has no build worker to snapshot, so it writes nothing about itself. The check-in already runs, so I keep it.

1. **Start a worker** through `worker-control`:
   - **Skill:** `release`
   - **Model tier:** premium (the tier `release` names), on the model the project's tier map gives premium
   - **Review level:** none
   - **Brief:**
     > Run `release` for Milestone 1 (issue #1, label `milestone-1`). Release doc: `docs/dev-skills/release.md` (name `Milestone <m> · Release <n>`, label `release-m<m>-r<n>`, size 5, changelog `CHANGELOG.md`, pull requests bump). No release issue has been cut yet; this is the repo's first Release. Release issue #40 "Release Milestone 1 · Release 1" is open, but no issue carries `release-m1-r1` any more. The user carried #20 "Add a --quiet flag" and #25 "Document the hello command" over to the next Release: see #40's `## Carried over`, written by the user at 10:20, and the labels they removed at 10:21. Do not fill #40 with them, and do not put them back in Release 1. Cut #40 as Release 1 with what main holds since no Release, which is #7 "chore: tidy the usage line". Keep the user's `## Carried over` lines as written. Then plan the next Release, Milestone 1 · Release 2, by your own rule, from the Milestone's planned features #20 and #25 (order rule: one at a time). If nothing qualifies, open no release issue, label nothing and say so. The Boundary record allows every irreversible action an agent may take. Start no build worker. Report on #40 when done. In your report on the issue, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. As it becomes readable, keep the evidence that `milestone`'s report gathers.
2. **Tracker write:** use **Comment on an issue** to post on #40:
   > `<!-- team-lead start -->`
   > Worker: `<id as worker-control returned it>`. Skill: `release`. Model tier: premium. Review level: none. Started: 2026-11-09 11:00 PST. Session: `<session or history reference>`. Cuts Release 1 (no issue carries `release-m1-r1`; #20 and #25 carried over by the user) and plans Release 2.
3. **Message to the user:**
   > I read your carry-over on #40 as "cut Release 1 with #7 and put #20 and #25 in Release 2". A Release worker is doing that now. Say if you meant something else.

I start no build worker while the Release worker runs.

## Event 2: the user writes at 10:30, "Carried #20 and #25 over. Go on."; #35 now blocks both

**What the state shows.** The user's message is neither a pause nor a resume. #40 still has no labelled issue, so there is no current Release. Planning cannot qualify anything:
- #20 is blocked by #35 "Pick a docs tool". #35 is `needs-triage` (not `ready-for-agent`) and is not in Milestone 1.
- #25 is blocked by #20 and by #35.

So no Release worker starts to plan. The user's "Go on" does still cover cutting Release 1 (#7), which nothing blocks. So I start a Release worker to cut #40, and its planning step will find that nothing qualifies. Pulling #35 into the Milestone, or dropping it as a blocker, changes the Milestone's scope. That is the user's call, so I ask one question. No other work waits on the answer, because there is none.

1. **Start a worker** through `worker-control`:
   - **Skill:** `release`
   - **Model tier:** premium, on the model the project's tier map gives premium
   - **Review level:** none
   - **Brief:**
     > Run `release` for Milestone 1 (issue #1, label `milestone-1`). Release doc: `docs/dev-skills/release.md` (name `Milestone <m> · Release <n>`, label `release-m<m>-r<n>`, size 5, changelog `CHANGELOG.md`, pull requests bump). No release issue has been cut yet; this is the repo's first Release. Release issue #40 "Release Milestone 1 · Release 1" is open, and no issue carries `release-m1-r1`. The user carried #20 "Add a --quiet flag" and #25 "Document the hello command" over (their `## Carried over` lines on #40, and at 10:30: "Carried #20 and #25 over. Go on."). Do not fill #40 with them. Cut #40 as Release 1 with what main holds since no Release, which is #7 "chore: tidy the usage line". Keep the user's `## Carried over` lines as written. Then plan the next Release by your own rule. Expect nothing to qualify: #20 and #25 are both blocked by #35 "Pick a docs tool", which is `needs-triage` and not in the Milestone. If so, open no release issue, label nothing and say so (your step 5, "When nothing qualifies"). Do not triage #35 or add it to the Milestone. The Boundary record allows every irreversible action an agent may take. Start no build worker. Report on #40 when done. In your report on the issue, record the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference, writing "unknown" for any you cannot read. As it becomes readable, keep the evidence that `milestone`'s report gathers.
2. **Tracker write:** use **Comment on an issue** to post on #40:
   > `<!-- team-lead start -->`
   > Worker: `<id as worker-control returned it>`. Skill: `release`. Model tier: premium. Review level: none. Started: 2026-11-09 10:30 PST. Session: `<session or history reference>`. Cuts Release 1 (#7 only; #20 and #25 carried over by the user); next-Release planning expected to find nothing, since #35 blocks both features.
3. **Message to the user (one question):**
   > Going on: a Release worker is cutting Release 1 (#40, with #7 "chore: tidy the usage line"). Nothing can be planned after it. #20 "Add a --quiet flag" and #25 "Document the hello command" are both blocked by #35 "Pick a docs tool", which is still `needs-triage` and not in Milestone 1. Should #35 join Milestone 1 (it would need triage to `ready-for-agent` first), or should it stop blocking #20 and #25?

When the Release worker reports, I read #40 back. If it planned nothing, the user already has the one-line "what waits on what" in the question above, so I don't send it again.

## Event 3: hourly check-in at 11:00; only #25 was carried over, and w20 is running

**What the state shows.**
- #20 carries `release-m1-r1`, so #40 is the current Release. Its `## Carried over` lists only #25.
- Build worker `w20` reads running through `worker-control`. Its branch `t20` is pushed, last commit at 10:50. There is no pull request.
- No Release worker is running, and #20 is not closed, so there is no cut to start.
- Slots: the smaller of the thread limit (2) and "one at a time" is 1. `w20` holds it. #25 is blocked by #20 and is outside the current Release, so nothing else starts.
- The Milestone review gate does not hold.

**The check-in.** I run the snapshot over the one running build worker:

`python3 skill/team-lead/snapshot.py --worker 'id=w20;issue=20;branch=t20;started=<UTC start time from #20's start record>;state=running' --silent-after 60`

I leave `pr` out, so the command looks it up by branch. No report time and no resume apply. With a commit at 10:50 inside the 60-minute interval, the row reads **active**, so nothing is called for.

**Actions:** none. This is a quiet check-in: no tracker write, no message to `w20` or to the user, and no worker started.
