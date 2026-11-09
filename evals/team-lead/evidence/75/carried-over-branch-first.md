## Event 1: hourly check-in at 11:00, no other change

I read the state again: the Milestone issue #1, release issue #40 and its issues, **Park** and **Count open blockers** for #20 and #25, the branches, and each worker through `worker-control`. No pause is in effect. No merge-time request is waiting. The end-of-delivery gate (`milestone`'s "Milestone review") does not hold, because #20 and #25 are open. The check-in is still arranged, so I keep it and arrange nothing new.

**1. Check-in findings.** No build worker is running, so the snapshot has no rows and no Release worker is running. This part of the check-in is quiet: it writes nothing and tells no one.

**2. Next starts: a Release worker.** Every condition in team-lead's "Releases" rule holds:
- no worker is running;
- no open, unparked issue carries `release-m1-r1` (the user removed it from #20 and #25);
- release issue #40 names this Milestone and is open.

No build can start, because the Order has no entry that still carries the label. I don't decide whether this worker cuts or plans; its "Find where you are" does that.

- **Worker start** through `worker-control`: skill `release`, tier **premium** (the tier `release` names), on <model> (the `model-tiers` map; the project gives no map of its own). The brief:

  > Run the `release` skill for this repo.
  > - Release issue: #40 "Release Milestone 1 · Release 1" (label `release-m1-r1`).
  > - Milestone issue: #1 (label `milestone-1`, goal: a quieter greeter).
  > - Release doc: `docs/dev-skills/release.md`.
  > - Last release issue cut: none. No release issue has ever been closed, so this is the repo's first Release.
  > - Model tier: premium. No Review level is named.
  >
  > Start at the skill's "Find where you are" and follow it from freshly fetched main and the tracker. This brief overrides none of it.
  >
  > The Boundary record holds every boundary. A pull request that crosses one goes to the user.
  >
  > In your report on the release issue, record:
  > - the plugin load source and version you actually loaded;
  > - your permission and sandbox settings;
  > - a readable session usage reference.
  >
  > Write "unknown" for any of these you cannot read. Also keep, as each becomes readable, the evidence that `milestone`'s report gathers (its "Gather the evidence"). When you finish, or if you stop, report on #40 and say what you did and what waits.

- **Tracker write.** **Comment on an issue** on #40 (the worker cuts this Release, so the record goes on its release issue):

  > `<!-- team-lead start -->`
  > Worker: `<id as worker-control returned it>`. Skill: `release`. Model tier: premium. Review level: none. Started: 2026-11-09 11:00 (PST). Session: `<session or history reference from worker-control>`.

I send no message to the user. I start no build worker while this Release worker runs, and I read #40 back when it reports.

## Event 2: the user writes at 10:30, "Carried #20 and #25 over. Go on."

The one change: #20 and #25 are each also blocked by #35 "Pick a docs tool", which is open, at `needs-triage`, and an enhancement the Milestone issue does not list.

I read the state again. The user's words are not a pause or a resume, so I post no record for them. No merge-time step is waiting. The end-of-delivery gate does not hold. This is not a check-in, so I run no snapshot.

**Next starts: a Release worker.** The rule holds for the same reasons as in event 1. Release issue #40 is open and names this Milestone, which is enough on its own, so the new blockers do not change it. The Order has no labelled entry, so no build can start.

- **Worker start:** skill `release`, tier premium, on <model>. The brief is word for word the one in event 1.
- **Tracker write.** **Comment on an issue** on #40:

  > `<!-- team-lead start -->`
  > Worker: `<id as worker-control returned it>`. Skill: `release`. Model tier: premium. Review level: none. Started: 2026-11-09 10:30 (PST). Session: `<session or history reference from worker-control>`.

- **Message to the user:**

  > Started a Release worker on #40 "Release Milestone 1 · Release 1". With #20 and #25 carried over, it closes that Release and then plans the next one. Heads-up: #20 "Add a --quiet flag" and #25 "Document the hello command" are now both blocked by #35 "Pick a docs tool". #35 is at `needs-triage` and the Milestone doesn't list it. The worker will report what it can plan.

The check-in stays arranged. Nothing else starts.

## Event 3: hourly check-in at 11:00

The changes: only #25 was carried over. #20 still carries `release-m1-r1`. Its build worker `w20` was never stopped: it is running, and its branch `t20` is pushed with a commit at 10:50.

I read the state again. No pause is in effect, no merge-time request is waiting, and the end-of-delivery gate does not hold.

**1. Check-in findings.** I run the snapshot over the one running build worker:

`python3 <team-lead folder>/snapshot.py --worker 'id=w20;issue=20;branch=t20;started=<UTC from #20's start record>;state=running' --silent-after 60`

I leave out `pr`, because no report named one; the command looks it up by the branch. The commit at 10:50 falls inside the 60-minute window, so the row reads **active** and nothing is needed. No Release worker is running. The check-in is quiet: it writes nothing and tells no one.

**2. Next starts: none.**
- **Releases:** an open, unparked issue (#20) carries the label of open release issue #40, so no Release worker starts.
- **Slots:** one. The thread limit is 2 and the order rule is one at a time, so the slot count is one, and `w20` holds it. #20 is the only Order entry still carrying the label, and it already has its running worker.
- **#25** is carried over and has no label, so it is not in the build order (it also waits for #20).

I make no tracker writes, send no messages and start no workers.

