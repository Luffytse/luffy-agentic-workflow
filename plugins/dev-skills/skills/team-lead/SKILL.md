---
name: team-lead
description: "Run delivery as the coordinator's team lead: start workers, react to worker and Harness reports, hold check-ins, pause and resume. Use when planning is done and a Milestone's delivery starts, at every wake while it runs (worker report, Harness notice, check-in, user writing), or on a request to pause or resume delivery."
---

# Team lead

The coordinator runs this skill whenever it delivers planned work. Every plan is a Milestone (a small Release is a Milestone with one Release), so delivery is always a Milestone's. It manages the work, what starts and what is stuck or done, and leaves the machinery to the Harness: load `worker-control` by name at delivery start and take every worker action through it (start, read state, notice an end, message, stop and read back, pause, resume, check-in). The Harness's record, read through `worker-control`, is the only truth about a worker; tracker comments are an audit trail for the report. Release grouping is `release`'s rule.

A coordinator that cannot load this skill follows the project instructions `setup-project` writes for it.

## The work it delivers

The open Milestone issue (as `milestone`'s **No Milestone** test finds it) gives the features and the graph of what each waits for. Delivery starts only once `milestone`'s planning has settled and the Plugin version check holds, or the user's word to go on is recorded, both read from the Milestone issue. With no open Milestone issue there is nothing to deliver: tell the user that the next plan starts one, with `milestone`.

**Boundaries** are the Boundary record's; a Milestone issue holds none. A pull request that crosses one goes to the user, and a question about one is the user's.

The project's own instructions add their thread limit, if any, tier map and what else a brief carries. Do every tracker read and write with the tracker doc's operations (`docs/dev-skills/issue-tracker.md`), cited by name below.

An open issue **waits with** a parked issue when it has at least one open blocker (**Count open blockers**) and each is parked (**Park**), is listed under a release issue's `## Left the Release`, or itself waits with a parked issue; a Spec and its open Tickets go together, as `release` step 1 says. A **setup Ticket** is an issue at `ready-for-human` that planning published for an account, product or credential the person must provide for a live step.

## Wakes

Delivery is **event-driven**. A wake is a worker reporting or asking, a Harness notice (a worker ended, failed or needs an answer), a scheduled check-in, or the user writing. At each wake read the state afresh: the tracker (the Milestone issue, the current Release and its issues, **Park** and **Count open blockers** for each), the branches, and every worker's state through `worker-control`. A worker's message is a reason to read, never the state itself. Then take every step below that the state calls for, in order: pause or resume on the user's word, the end of delivery, the check-in's findings, then the next starts.

**Audit trail.** Post each record with **Comment on an issue**, first line `<!-- team-lead <kind> -->`:

- `start`, on the issue the worker builds (a Release worker's on its release issue, or on the Milestone issue when it only plans; a guiding thread's on its setup Ticket): the worker's id as `worker-control` returned it, its skill, model tier, Review level if any, start time and session or history reference. A replacement's record adds `Takes over from <worker>; <its stop read back, or its end as read>, at <time>.`
- `nudge`, `wait` and `parked` (with the **Park** operation), on the issue that holds the worker's `start` record; `pause`, `resume` and `check-in` (when arranged or ended), on the Milestone issue.

Preserve, as it becomes readable, the evidence that `milestone`'s report gathers (its reporting reference, "Gather the evidence").

## 1. Start delivery

Arrange the **check-in** through `worker-control` just before the first build-worker start (never for a Release worker that only plans), again at the first build-worker start after it was ended, and at a resume that finds build workers running and none: at the Boundary record's check-in interval (one hour when it names none), keeping one arranged earlier that `worker-control` reads as still running. Record it. Where it cannot be arranged, or the Harness has no check-in, tell the user in one line, record it, and go on woken by workers and the user only; where the Harness also pushes no worker events, say that delivery then moves only when the user writes.

**Guiding threads.** When delivery starts, and at any later wake, start one guiding thread for each open setup Ticket that blocks an issue of the Milestone and has none running (read through `worker-control` for each `start` record on it): it runs `wizard` with the person, briefed as step 2's Brief says, outside any thread limit. It waits on the person: it is not in the check-in's snapshot and is never nudged. Once a second one has ended with the Ticket still open, start none again: park the Ticket (**Park**, its comment the `parked` record naming both ended threads) and tell the user once. What it blocks then waits with a parked issue. Everything the Ticket does not block builds meanwhile.

## 2. Start work

Start nothing while a pause is in effect.

- **Releases.** Start a Release worker with `release` when none runs, every open issue carrying the label of an open release issue is parked, waits with a parked issue or is listed under its `## Left the Release`, and either a release issue naming this Milestone is open or at least one planned feature is open, carries no release label, is not parked and does not wait with a parked issue. Start it at the tier that skill names, briefed with the Milestone issue, the release doc, and the last release issue cut, if any. Its "Find where you are" decides whether it cuts or plans; the brief overrides none of it. Start no build worker while a Release worker runs; read the release issue back when it reports. When it reports that the cut is blocked, or that it planned nothing while a planned feature is open that is not parked and does not wait with a parked issue, tell the user in one line what waits and on what, post that line as a `wait` record, and start no Release worker again until one of those changes or the user writes.
- **Build workers.** Start one for every entry of the current release issue's Order that carries its label, is open, is not parked, has no running worker and has no open blocker (a Spec's: of the Spec, and of its Tickets outside the Spec). A Spec whose only open blockers are setup Tickets, each blocking some but not all of its open Tickets, starts too: its worker builds the Tickets they do not block. Where the project's instructions give a thread limit, start within it, in the Order's order, an entry that started before (its worker ended, or its park was lifted) ahead of one that has not; with none, start them all. A Spec's Ticket parked and lifted while its Spec worker runs is that worker's: tell it to take the Ticket up.
- **Kind:** a Spec gets `implement-spec`; a lone Ticket gets `implement`; related issues get `implement` one after another, in one worker.
- **Brief:** the skill, the issue link, the Milestone issue link, the model tier (a Spec worker regular, its Implementers on their Tickets' tiers; otherwise the issue's Model tier line, regular when it has none), a Review level only when the issue or the user names one, and what the project's instructions add. Start it on the model its tier maps to (load `model-tiers` by name; the project's own map overrides it), through `worker-control`, and post its `start` record.
- **A bug Ticket filed after Round 3** that a build worker reports has a line `Joins the running Release: severe`, `blocks #<n>`, `breaks an acceptance criterion of #<n>` or `no`. Unless it reads `no`, apply the current release label, then add a line naming the Ticket and its pull request at the end of the release issue's `## Order` (**Add a line to an issue body**; your only write to a release issue): it is then an entry, starts at this wake, and holds the cut. With `no`, or no such line, it gets no label and no worker; the next Release planning places it. Judge nothing yourself.

## 3. React

- **A worker reports or asks.** Read its issue, branch and pull request, then act on what they show: a finished build; a build worker's check against main (already fixed or obsolete: open its evidence, then close the issue as completed with the reason and where on main, or re-plan it; changed scope or cannot tell: update the issue or say what it lacks, and answer the worker; closing a planned feature or a Ticket of a planned Spec, or changing the Milestone's goal, acceptance or exclusions, is one question to the user, and that issue starts no worker until answered, while other work goes on); a question within the boundaries (answer it; a crossing goes to the user).
- **A worker waits on the user's action** (it asked once, named the action, and goes on with what it can): post a `wait` record on its issue naming the action. Until it comments or pushes again, pass that record's time as its `waiting` at check-ins (step 4): it is neither nudged nor replaced. The report lists what still waits.
- **A worker ended without its result** (build or Release, as `worker-control` reads an end; no stop is needed; a guiding thread: step 1). One that is no replacement (its `start` record takes over from none) and has no `nudge` record after that record: where `worker-control`'s reference gives a way to message a worker that ended, message it, by the id in its `start` record, to carry on, and post the `nudge` record. Otherwise (no such way, the message fails, or it ended again) start one fresh worker as "Replace a stalled worker" steps 3 and 4 say. A replacement that ended parks a build issue (step 4 there); a Release worker is never parked: where step 4 would park, tell the user once, as step 2's `wait` record.
- **A pull request is merged, or is ready and it has had no comment or push since,** with no report: act as if the worker had reported, and tell it what you decided. A ready pull request whose worker still comments or pushes (a Spec thread reviewing it) is a working worker.

## 4. The check-in (Stand-up)

A check-in is the safety net for a worker that is silent but nominally working; where the Harness pushes worker events it rarely finds anything. Run the snapshot over the running build workers:

`python3 <this skill's folder>/snapshot.py --worker 'id=<id>;issue=<n>;branch=<branch>[;pr=<n>];started=<UTC>[;reported=<UTC>][;resumed=<UTC>][;waiting=<UTC>];state=<Harness state>' ... --silent-after <interval in minutes>`

one `--worker` per running build worker, its state from `worker-control`. Pass as `reported` the time you acted on its ready or merged pull request, so the next check-in tests it for silence; as `resumed` its resume time, so a nudge before the pause is void; as `waiting` its `wait` record's time. Leave `pr` out when no report named the pull request: the command looks it up by the branch. It prints one row per worker: last commit, last comment, pull request and a verdict. Exit 3, a row reading `read by hand`, or no shell: read those columns by hand with the tracker doc's operations and git. Then act on each row:

- **pull request ready but not reported:** as step 3 says.
- **silent since T:** nudge it once: message it by the means `worker-control`'s reference gives, asking where it is and what blocks it, answered by a comment on its issue, and post the `nudge` record.
- **still silent after its nudge:** replace it, below.
- **ended** by `worker-control`'s reading: as step 3 says.
- **active,** **nudged, waiting,** or **waiting on the user:** nothing.

A running Release worker is not in the snapshot: read its state through `worker-control` and its release issue's comments by hand. If it has been silent a whole interval with no report, tell the user once, with the link to its release issue; take no other step and write no record.

A **quiet check-in**, one where no row calls for an action, writes nothing and tells no one.

## Replace a stalled worker

1. **Nudge once** (step 4).
2. **Still silent:** stop it through `worker-control` and read the stop back from the Harness's record. A call returning success, silence or a worker still reading as running is not a stop.
3. **Read back stopped** (or ended on its own): start a fresh worker on the same issue with the same skill, tier and Review level, briefed to resume from the pushed branch (name it) and the tracker (the issue, its comments, its pull request), keeping what is pushed. Its `start` record names the worker it takes over from.
4. **Park instead** when the stop does not read back, when the stalled worker was itself a replacement started since the issue's latest park record (the feature's second stall), or when the fresh start fails: mark the issue with the **Park** operation, its comment the `parked` record naming the reason, whether a writer may remain, and links to the nudge and start records and the pull request. Tell the user once, with the link, and go on with other work.

Parked work is skipped until the user removes the label. A lifted issue keeps its Order entry; before its fresh worker starts, read its last worker's state through `worker-control`: one not ended is stopped and read back first, as step 2 says, and one that does not read back stopped parks the issue again, telling the user once.

## Pause and resume

The user's word is the only trigger. **Pause:** post the `pause` record with their words, start nothing, pause each running worker through `worker-control` (the Harness's pause, or a message to push and stop), and tell the user. While paused, nudge, replace and park nothing. **Resume:** post the `resume` record, resume each worker through `worker-control`, pass its `resumed` time (step 4), and carry on from the tracker. A pause holds from the latest `pause` record until a `resume` follows; a word that changes nothing records nothing.

## End of delivery

At every wake, read each planned feature's issues, pull requests and Park state. Delivery stops for review when every planned feature is merged, parked or waits with a parked issue, and the report lists each that waits and with what; a closed issue with no merge evidence has its merge checked (**Read whether a PR merged**). A pause holds the report. While a release issue naming this Milestone is open and step 2 lets its Release worker start, start it first, then test again. Once the gate holds and no such cut is left, start nothing further. If an unchanged report already waits, do nothing more, as `milestone`'s reporting reference says. Otherwise end the check-in through `worker-control`, read back that it no longer runs and record it, then follow `milestone`'s report (its `reporting.md`) and stop for the user's Milestone review.
