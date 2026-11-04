---
name: team-lead
description: "Run delivery as the coordinator's team lead: start build workers in order within the limits and start Release workers, react to what workers and the Harness report, hold a check-in only as a safety net (one snapshot command, a quiet check-in writes nothing), nudge a silent worker once and then replace it or park its work, pause and resume on the user's word, and follow the merge-time steps the repo's own docs give; every worker start, state check, end, stop, pause, resume and check-in goes through `worker-control`. Use when planning is done and a Milestone's delivery starts, at every wake while it runs (a worker reporting, a Harness notice, a check-in, the user writing), and when the user asks to pause or resume it."
---

# Team lead

The coordinator runs this skill whenever it delivers planned work. Every plan is a Milestone (a small Release is a Milestone with one Release), so delivery is always a Milestone's. It manages the work (what starts next, what is stuck, what is done) and leaves the machinery to the Harness: load `worker-control` by name at delivery start and take every worker lifecycle action through it (start a worker, read its state, notice that it ended or failed, stop it and read the stop back, pause and resume it, arrange and end the check-in). The Harness's record, read through `worker-control`, is the only truth about a worker; tracker comments are an audit trail for the report, never a worker's state. Release grouping is `release`'s rule; this skill never restates it.

## The work it delivers

The open Milestone issue (as `milestone`'s **No Milestone** test finds it) gives the features in build order and its order rule (one at a time, or up to some number at once). Delivery starts only once `milestone`'s planning has settled and the latest Startup verification result on the Milestone issue reads `Verdict: ready`, or, after a failed one, the user's word to go on is recorded there, naming each failed capability. If that result's Runtime line plainly names another environment than this one, tell the user. With no open Milestone issue there is nothing to deliver: tell the user that the next plan starts one, with `milestone`.

**Boundaries** are the Boundary record's, for every issue; a Milestone issue holds none of its own. A worker's pull request that crosses one goes to the user, and a question about one is the user's to answer.

The project's own instructions add their thread limit, tier map and what else a brief carries. Do every tracker read and write with the tracker doc's operations (`docs/dev-skills/issue-tracker.md`), cited by name below.

## Wakes

Delivery is **event-driven**. A wake is a worker reporting or asking, a Harness notice (a worker ended, failed or needs an answer), a scheduled check-in, or the user writing. At each wake read the state afresh: the tracker (the Milestone issue, the current Release and its issues, **Park** and **Count open blockers** for each), the branches, and every worker's state through `worker-control`. A worker's message is a reason to read, never the state itself. Then take every step below that the state calls for, in order: pause or resume on the user's word, the merge-time steps, the end of delivery, the check-in's findings, then the next starts.

**Audit trail.** Post each record with **Comment on an issue**, first line `<!-- team-lead <kind> -->`:

- `start`, on the issue the worker builds (a Release worker's on its release issue, or on the Milestone issue when it only plans): the worker's id as `worker-control` returned it, its skill, model tier, Review level if any, start time and session or history reference. A replacement's record adds `Takes over from <worker>; <its stop read back, or its end as read>, at <time>.`
- `nudge`, `parked` (with the **Park** operation), `pause` and `resume` (on the Milestone issue), `check-in` when it is arranged or ended (the same issue).

Records of the earlier `<!-- milestone ... -->` forms on an issue count as their team-lead counterparts: `delivery thread` as `start` (its second line names the worker), `delivery thread ended` as that worker's end, `nudge`, `stall` (a nudged worker found still silent), `parked`, `park lifted` (the user's lift), `pause` and `resume`, and `check-in`, `check-in ended` and `stand-up` as `check-in`. A worker such a record names is read through `worker-control` like any other: while it reads running, it holds its slot and no second worker starts.

Brief every worker to record, in its issue report, the plugin load source and version it actually loaded, its permission and sandbox settings and a readable session usage reference, saying "unknown" where it cannot read one. Also preserve, as it becomes readable, the evidence that the report of `milestone` gathers (its reporting reference, "Gather the evidence").

## 1. Start delivery

Delivery starts once planning with the user is done, never while it still runs. Arrange the **check-in** at the wake where the team lead starts its first build worker (never for a Release worker that only plans), before that start, again at the first build-worker start after the check-in was ended, and at a resume that finds build workers running and no check-in: arrange it through `worker-control` at the Boundary record's check-in interval (one hour when it names none), first asking `worker-control` whether one arranged earlier still runs, and keeping it if so. Record it. Where it cannot be arranged, or the Harness has no check-in, tell the user in one line, record it, and go on woken by workers and the user only; where the Harness also pushes no worker events, say that delivery then moves only when the user writes.

## 2. Start work

Start nothing while a pause is in effect or a merge-time step holds further starts.

- **Releases.** With no current Release (an open release issue, naming this Milestone, whose label at least one issue carries), no Release worker running, and at least one planned feature that is open, not parked and carries no release label, and is unblocked or blocked only by open issues `release` ranks ahead of it (at `ready-for-agent`, not parked), start a Release worker with `release`, at the tier that skill names, briefed with the Milestone issue, the release doc, and the last release issue cut, if any. It plans the next Release by `release`'s own rule; where an open release issue holds no issue yet, it fills that one instead of opening another (for that issue this overrides `release`'s "Rerun first"; say so in its brief); where nothing qualifies, it opens no release issue, labels nothing and says so. When every issue carrying the current Release's label is closed, start a Release worker with `release` to cut it and plan the next one. Start no build worker while a Release worker runs; read the release issue back when it reports. A Release worker is watched by Harness events (its report, its end or failure), and at a check-in only as step 5 says: it is never nudged or replaced. When it reports that it planned nothing while planned features are still open, tell the user in one line which wait and on what.
- **Slots** are the smaller of the project's thread limit and the order rule (one at a time is one; up to k is k); with neither, one. Each running build worker takes one.
- **Build order:** the entries of the current release issue's Order, in its order (a release issue written before the Order list: its maintenance fixes, then its features in the Milestone issue's order). While a slot is free, start the first that is open, not parked and unblocked and has no running worker: a started one that has none (its worker ended without finishing, or its park was lifted) before any that has not started. Under one at a time the next starts only once each one before it has closed or is parked. A Spec's Ticket parked and lifted while its Spec worker runs is that worker's: tell it to take the Ticket up.
- **Kind:** a Spec with Tickets gets `implement-spec`; a Spec without gets `to-tickets` first, in the same slot; a lone Ticket gets `implement`; related issues get `implement` one after another in one slot.
- **Brief:** the skill, the issue link, the Milestone issue link, the model tier (the issue's Model tier line, regular when it has none), a Review level only when the issue or the user names one, and what the project's instructions add. Start it on the model its tier maps to (load `model-tiers` by name; the project's own map overrides it), through `worker-control`, and post its `start` record.

## 3. React

- **A worker reports or asks.** Read its issue, branch and pull request, then act on what they show: a merge-time request (step 4), a finished build (its slot frees), a question within the boundaries (answer it; a boundary crossing goes to the user, as above), a request for another agent's worker on a Ticket (a continuation handoff: start that agent on it through `worker-control` where the Harness can, otherwise tell the user once which agent to run on which handoff; tell the asking worker which; when that worker finishes, tell the owning Spec worker, or restart it from its pushed branch if it ended).
- **A worker ended without its result,** as `worker-control` reads an end: no stop is needed. Start a fresh worker from its pushed branch and the tracker as "Replace a stalled worker" steps 3 and 4 say; it counts as a stall, so a replacement that ended parks the issue.
- **A pull request is merged, or is ready and it has had no comment or push since,** with no report: act as if the worker had reported, and tell it what you decided. A ready pull request whose worker still comments or pushes (a Spec thread reviewing it) is a working worker.

## 4. Merge-time steps

A build worker merges its own pull request (the build skills say when). Where the repo's own docs (its `CLAUDE.md` or `AGENTS.md` and the release doc, `docs/dev-skills/release.md`) give steps for the coordinator at or after a merge, take them as those docs say, at the wake where a worker asks or reports and at any later wake while the docs say a request still waits. This skill states none of them. A step those docs say holds further starts holds the slots until it is done. Where they give none, tell a worker that asks to merge with no extra step.

## 5. The check-in (Stand-up)

A check-in is the safety net for a worker that is silent but nominally working; where the Harness pushes worker events it should rarely find anything. Run the snapshot over the running workers:

`python3 <this skill's folder>/snapshot.py --worker 'id=<id>;issue=<n>;branch=<branch>[;pr=<n>];started=<UTC>[;reported=<UTC>][;resumed=<UTC>];state=<Harness state>' ... --silent-after <interval in minutes>`

one `--worker` per running build worker, its state from `worker-control` and its last report time from what reached you: once you have acted on its ready or merged pull request, pass that time as `reported`, so the next check-in tests it for silence; after a resume, pass the resume time as `resumed`, so a nudge before the pause is void and the worker gets a full interval. `pr` is the worker's pull request; when no report named it, find it by the worker's branch with the tracker doc's **Read a PR** operation, or leave `pr` out and the command looks it up by the branch. It prints one row per worker: last commit, last comment, pull request and a verdict. Exit 3, a row reading `read by hand`, or no shell to run it in: read those columns by hand with the tracker doc's operations and git. Then act on each row:

- **pull request ready but not reported:** as step 3 says.
- **silent since T:** nudge it once: message it by the means `worker-control`'s reference gives, asking where it is and what blocks it, answered by a comment on its issue, and post the `nudge` record.
- **still silent after its nudge:** replace it, below.
- **ended** by `worker-control`'s reading: as step 3 says.
- **active,** or **nudged, waiting:** nothing.

A running Release worker is not in the snapshot: read its state through `worker-control` and its release issue's comments by hand. If it has been silent a whole interval with no report, tell the user once, with the link to its release issue; take no other step and write no record.

A **quiet check-in**, one where no row calls for an action, writes nothing and tells no one.

## Replace a stalled worker

1. **Nudge once** (step 5).
2. **Still silent:** stop it through `worker-control` and read the stop back from the Harness's record. A call returning success, silence or a worker still reading as running is not a stop.
3. **Read back stopped** (or ended on its own): start a fresh worker on the same issue with the same skill, tier and Review level, briefed to resume from the pushed branch (name it) and the tracker (the issue, its comments, its pull request), keeping what is pushed. Its `start` record names the worker it takes over from.
4. **Park instead** when the stop does not read back, when the stalled worker was itself a replacement started since the issue's latest park record (the feature's second stall), or when the fresh start fails: mark the issue with the **Park** operation, its comment the `parked` record naming the reason, whether a writer may remain, and links to the nudge and start records and the pull request. Tell the user once, with the link, and go on with other work.

Parked work is skipped until the user removes the label. A lifted issue keeps its place in the order; before its fresh worker starts, read its last worker's state through `worker-control`: one not ended is stopped and read back first, as step 2 says, and one that does not read back stopped parks the issue again, telling the user once.

## Pause and resume

The user's word is the only trigger.

- **Pause:** post the `pause` record with the user's words, start nothing new, and pause each running worker through `worker-control`: the Harness's own pause where it has one, otherwise a message to push its work and stop at its next natural step. Tell the user in one line. While a pause is in effect, start, nudge, replace and park nothing; a check-in writes nothing; worker reports are still read; merge-time steps run as the repo's docs say they run during a pause.
- **Resume:** post the `resume` record with the user's words, resume each paused worker through `worker-control`, then carry on from the tracker and the branches as at any wake. At the next check-ins pass the resume time as each resumed worker's `resumed` (step 5): activity counts from the resume. A worker that does not carry on is handled at the check-ins like any silent one.

A pause is in effect from the latest pause record until a resume record follows it. A word to pause while paused, or to resume when not, records nothing: tell the user so.

## End of delivery

At every wake, apply `milestone`'s "Milestone review" gate. Once it holds and any final Release cut has reported, start nothing further; if a report for this state already waits, do nothing more. Otherwise end the check-in through `worker-control`, read back that it no longer runs and record it, then follow `milestone`'s report and stop for the user's review. A one-Release Milestone ends the same way.
