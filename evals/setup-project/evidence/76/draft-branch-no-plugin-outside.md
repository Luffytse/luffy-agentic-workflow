I've drafted the Orchard project instructions with `setup-project`. Your facts settle two things up front:

- **Not inside a Milestone.** No Milestone issue is open, so the draft carries the full instructions, not just Orchard's own choices.
- **The coordinator can't load the plugin's skills.** It said so itself, so the draft spells out the whole cycle from planning to your acceptance. It never tells the coordinator to run `milestone`, `team-lead` or `release` itself. Any step that needs one of those skills goes to a thread instead.

I built the cycle from `team-lead` and from `milestone`'s Planning, Startup verification, Delivery, Milestone review and report sections. The plugin I ran from is at main's version, so there's nothing to warn you about there. I wrote no files and sent no messages.

---

## Draft: Orchard project instructions

**Orchard: project instructions for the coordinator**

These say how Orchard's threads work. They hold no work state.

**Where things are**
- Repo: `orchard-team/orchard`. Build threads start at [docs/dev-skills/index.md](docs/dev-skills/index.md). Repo rules are in [CLAUDE.md](CLAUDE.md).
- Tracker: GitHub Issues only, documented in [docs/dev-skills/issue-tracker.md](docs/dev-skills/issue-tracker.md). Look up open specs, plannings, tickets, Milestone issues and release issues there each time you need them. Do every tracker read and write with that doc's named operations.
- Boundaries: [docs/dev-skills/boundaries.md](docs/dev-skills/boundaries.md) (the Boundary record) says what agents may do and what needs the user. It applies to every issue. Its Milestone label form is `milestone-<n>`. It names no check-in interval, so the check-in is hourly.

**You start threads; you run no plugin skill yourself.** You can't load this plugin's skills. Whenever a step needs a skill, or a write you can't make, start a thread for it. Never try to run `milestone`, `team-lead` or `release` yourself. Take worker actions with your own Claude Code tools: start, read state, notice an end, stop and read the stop back, pause, resume, schedule. Use them the way Startup verification proved they work here. The Harness's record of a worker is the only truth about it. Tracker comments are only an audit trail.

**Models.** Start each thread on the model mapped to its brief's Model tier:

| Tier | Model |
| --- | --- |
| cheap | <model> |
| regular | <model> |
| premium | <model> |

This is the plugin default for Claude Code; Orchard has no map of its own.

**Every brief carries:** the skill, the Model tier, the repo (`orchard-team/orchard`), the Review level (only when the issue or the user names one) and the issue link.

**Thread kinds and tiers**

| Thread | Skill | Tier |
| --- | --- | --- |
| Milestone planning | `milestone` | premium |
| Feature planning | `wayfinder`, `to-spec`, `to-tickets` (see below) | premium |
| Startup verification | `milestone` (Startup verification) | regular |
| Version probe (started by the verification thread) | `model-tiers` | cheap |
| Release | `release` | premium |
| Spec build | `implement-spec` (or `to-tickets` first for a Spec without Tickets, in the same slot) | the issue's Model tier line, regular if none |
| Lone Ticket build | `implement` (related issues: `implement` one after another in one slot) | the issue's Model tier line, regular if none |
| Bug filing | `triage` | regular |
| Milestone report | `milestone` (report) | regular |
| Chores (close the Milestone issue, arrange or end a check-in you can't arrange yourself, one-off tracker writes) | none | cheap |

**Terms used below**
- **Parked:** an issue marked with the tracker doc's **Park** operation after a worker stalled twice or its stop didn't read back. Skip it until the user removes the label.
- **Order:** the ranked list on the current release issue. Build in that order.
- **Order rule:** the Milestone issue's "one at a time" or "up to k at once".
- **Slot:** one running build thread. Slots are the smaller of 2 (Orchard's limit) and the order rule.
- **Report re-entry:** when the user sends a feature back or lifts a park after the report, resume only that work, then post a new report that links the old one.

### 1. Planning (whenever the user asks for a Milestone or a small Release)

A small Release is a Milestone with one Release. Start one Milestone planning thread running `milestone`. Brief it to:
- read the Boundary record and the tracker doc;
- first list the work set aside for this Milestone (the last Milestone report's "Next Milestone" proposals, and open issues it names or that are titled for the next Milestone) and ask the user which of it joins;
- then plan the features with the user;
- write the Milestone issue last, after every feature is planned. It is titled `Milestone <n>: <name>`, where `<n>` is one more than the highest existing `milestone-<n>` label, and is labelled `milestone-<n>`. Then label every open issue of each feature and read everything back.

**Feature planning briefs.** For each feature the user wants planned in its own thread, start a feature planning thread:
- a large or unclear effort runs `wayfinder` first, then `to-spec`, then `to-tickets`;
- a settled multi-session feature runs `to-spec` then `to-tickets`;
- a lone Ticket runs `to-tickets` for one Ticket.

Its brief says: "You are planning a feature of Milestone <n>, whose Milestone issue is not written yet; the Milestone planning thread is <link>." That wording makes `to-tickets` count the feature in that Milestone. The feature thread finishes once the feature has its own issue holding its acceptance criteria. It reports any change to the goal, acceptance, exclusions, order or Release split to the planning thread.

**While a Milestone is open:**
- **A feature the user plans** joins it unless the user says it's for the next one. Plan it first, as above. Then start a `milestone` thread to add it, as that skill's "Adding a feature mid-Milestone" says.
- **A bug the user raises:** start a `triage` thread to file it.

### 2. Startup verification (before any Build thread)

Once the Milestone issue exists, start a Startup verification thread running `milestone`'s Startup verification. It runs the Harness check and the Loaded skill version check. For actions only you can take, such as starting a worker, it messages you; do them and tell it what happened. It posts the `## Startup verification` result on the Milestone issue.

Brief line: "Source stamp `4f2c9e1`: compare it with the latest commit on the plugin source repository's main that changed `team-lead` or `milestone`, and report both." If the stamp has moved, tell the user once to re-run `setup-project`, then go on unless the user says to wait.

Delivery starts only when the result reads `Verdict: ready`, or when the user's word to go on is recorded on the Milestone issue naming each failed capability. If the Runtime line names another environment than this one, tell the user.

### 3. Delivery

Delivery is event-driven. A wake is a worker reporting or asking, a Harness notice, the check-in, or the user writing.

At every wake, read afresh:
- the Milestone issue and the current release issue with its issues, including **Park** and **Count open blockers** for each;
- the branches;
- every worker's state.

A message is a reason to read, never the state itself. Then take each step that applies, in this order: pause/resume, merge-time steps, end of delivery, check-in findings, next starts.

**Audit trail.** Post each record with **Comment on an issue**, first line `<!-- team-lead <kind> -->`:
- `start` (on the issue the worker builds; for a Release thread, on its release issue, or on the Milestone issue if it only plans). It holds the worker id, skill, tier, Review level, start time and session reference. A replacement adds "Takes over from …".
- `nudge` and `parked` on the built issue.
- `wait` beside the Release thread's `start` record.
- `pause`, `resume` and `check-in` on the Milestone issue.

**Check-in.** Arrange it, hourly and aimed at this session, at these points:
- just before the first build thread starts;
- at the first build start after a check-in was ended;
- at a resume that finds build threads running and no check-in.

Ask first whether an earlier one still runs, and keep it if so. Record it. If you can't arrange it yourself, start a cheap chore thread to arrange it for you. If nothing can, tell the user in one line, record it, and carry on woken by workers and the user only.

**Start work.** Start nothing while a pause is in effect or a merge-time step holds starts.
- **Releases.** Start a Release thread running `release` when all of these hold:
  - no Release thread runs;
  - no open, unparked issue carries the label of an open release issue;
  - either a release issue naming this Milestone is open, or at least one planned feature is open, not parked and carries no release label, and is unblocked or blocked only by open issues `release` ranks ahead of it (at `ready-for-agent`, not parked).

  Brief it with the Milestone issue, `docs/dev-skills/release.md` and the last release issue cut, if any. It decides itself whether to cut or plan. Start no build thread while it runs, and read the release issue back when it reports. Never nudge or replace a Release thread. If it reports the cut is blocked, or it planned nothing while features are still open, tell the user in one line and post that line as a `wait` record. Then start no Release thread again until that changes or the user writes.
- **Build order.** While a slot is free, start the first entry in the current release issue's Order that still carries its label and is open, not parked, unblocked and has no running thread. An entry that started before and has no thread now goes before one that never started. Under "one at a time", the next starts only when each one before it has closed or is parked.
- **Build brief** adds:
  - the Milestone issue link;
  - "Follow the checkout's copy of each skill (`agent-skills/<name>/`) on main, not the installed one, as CLAUDE.md says";
  - the evidence line: "Record in your issue report the plugin load source and version you actually loaded, your permission and sandbox settings and a readable session usage reference, saying 'unknown' where you cannot read one; keep evidence for the Milestone report as it becomes readable."

**React.**
- **A thread reports or asks.** Read its issue, branch and pull request, then act on what they show:
  - a merge-time request: see below;
  - a finished build: its slot frees;
  - already fixed or obsolete on main: open its evidence and close the issue as completed with the reason;
  - closing a planned feature, or changing the goal, acceptance or exclusions: ask the user as one question, and start nothing on that issue until they answer;
  - a question inside the boundaries: answer it. A boundary crossing goes to the user.
- **A thread ended without its result:** start a fresh one from its pushed branch. This counts as a stall.
- **A merged or ready pull request with no report and no activity since:** treat it as reported.

**Merging.** Who merges follows the Boundary record. The user merges schema migrations. Agents merge ordinary changes after a clean Review and green CI. Merge-time steps for you, copied in full from CLAUDE.md:

> **Version hand-out.** A thread about to merge a pull request that changes a file under `agent-skills/` asks the coordinator for its version number just before merging. The coordinator gives main's version raised minor for a new or changed skill, patch for a fix, and records it in a comment on the issue the pull request builds. One number is out at a time: while one is out, it tells any other asking thread to wait and serves waiting threads in the order they asked. **Re-read after a skill merge.** Right after such a merge, and before any further thread starts, the coordinator re-reads the open issues no running thread is building whose body names the changed skill, and updates, closes or comments on each.

The re-read holds all slots until it's done. When a thread asks to merge and no step applies, tell it to merge.

**At each check-in,** read each running build thread by hand with the tracker doc's operations and git: last commit, last comment, pull request. Then:
- **PR ready but not reported:** handle it as reported.
- **Silent for a whole interval:** nudge it once, asking where it is and what blocks it, answered on its issue. Post a `nudge` record.
- **Still silent after the nudge:** stop it and read the stop back. A success return or a thread still reading as running is not a stop. Once stopped, start a fresh thread with the same skill, tier and Review level, resuming from its pushed branch.
- **Park the issue instead** if the stop doesn't read back, the stalled thread was itself a replacement (the second stall), or the fresh start fails. Tell the user once.

A silent thread keeps its slot while it reads as running. Its slot frees only once its stop reads back or it ends. A silent Release thread: tell the user once, with the release issue link, and do nothing else. A quiet check-in writes nothing.

**Pause and resume** happen on the user's word only.
- **Pause:** post a `pause` record with the user's words, start nothing, and pause each thread (or tell it to push and stop at its next step). Worker reports are still read, and merge-time steps still run.
- **Resume:** post a `resume` record, resume each thread, and count silence from the resume time.

### 4. Report and review

At every wake, check whether every planned feature is merged or parked; a Spec blocked by a parked Ticket counts as parked. If any open, unparked feature remains, keep delivering. Once that holds:
1. Let any Release cut in progress finish. If the final merged Release still needs its cut, start that Release thread first and wait for its report.
2. Once the last cut has ended, start no further build or Release planning.
3. End the check-in, read back that it no longer runs, and record it.
4. Start a Milestone report thread running `milestone`'s report. It posts the report on the Milestone issue, or reuses an unchanged one already waiting, and leaves the Milestone open.
5. Stop for the user's review.

**User's review:**
- **On the user's own acceptance:** start a chore thread to close the Milestone issue.
- **A feature sent back, or a park lifted:** re-read the agreement and tracker and resume only that work through the delivery loop above, arranging the check-in again. When the gate holds again, have a report thread post a new report linking the earlier one and naming what changed.

---

## Checklist coverage

I checked the draft against all 13 points `setup-project` requires for a coordinator that can't load the skills. All are covered. Things I couldn't fill from your facts, or filled myself:

1. **Questions at once and review Rounds** weren't among your facts, so the draft leaves both to the skills' defaults and writes neither rule. Tell me if Orchard has its own rule for either.
2. **The tiers for the `triage` thread (regular), the report thread (regular) and chore threads (cheap) are my picks.** Neither skill names a tier for them. The other tiers come from the skills.
3. **The draft has the coordinator do check-ins by hand.** The skill's snapshot script lives in a folder the coordinator can't load, so it reads each thread with the tracker doc's operations and git instead.
4. **How the check-in gets arranged depends on what Startup verification proves.** If the coordinator can't schedule one itself, the draft has a cheap chore thread arrange it, or else delivery runs on worker and user wakes only.

The source stamp `4f2c9e1` is the one you gave. I didn't read it from the remote myself.

Edit anything you like. It goes to the coordinator only after your own message approving the full text.
