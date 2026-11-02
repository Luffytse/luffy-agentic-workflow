---
name: milestone
description: "Plan, start and deliver a Milestone: write the Milestone issue with the user (goal, features with acceptance criteria, exclusions, budget, boundaries, membership label) and add a feature mid-Milestone; run Startup verification, which proves in this environment that a scheduled check-in reaches the coordinator by the mechanism delivery uses, that a worker's real state can be read back from the tracker, that a stopped worker is confirmed stopped and that a fresh thread loads main's skill version; then run delivery as the coordinator: arrange its scheduled check-ins until delivery is done and hold a Stand-up at each (read every running thread's real state, act on work finished without a report, nudge a silent thread once), take over from a build thread still silent after its nudge only once its stop is confirmed by the means Startup verification proved, parking the work where it cannot be confirmed or the feature stalls a second time, skip parked work, group the features into Releases, start build threads within the limits and in order, hand out version numbers, re-read open Tickets after a skill merge and start each Release thread. Use when the user asks for a Milestone or to add a feature to one, when a Milestone is about to start or is running autonomous delivery, or when the user asks whether this environment can run a Milestone unattended."
---

# Milestone

A **Milestone** is a product goal the user sets, written down in one Milestone issue, which agents deliver unattended across one or more Releases. This skill runs it in three phases, in order:

1. **Planning**, with the user: the Milestone issue is written and every feature in it is labelled.
2. **Startup verification**, once the Milestone issue exists: proof that this environment can run delivery unattended.
3. **Delivery**, run by the coordinator: woken by scheduled check-ins until it is done, each a Stand-up on its running threads (a build thread still silent after its nudge is taken over once its stop is confirmed, or its work parked), it groups the planned features into Releases, starts build threads within the limits and in order, hands out version numbers, re-reads open Tickets after a skill merge and starts each Release thread. It starts only once both phases before it are done (see "Delivery").

**No Milestone.** A project is inside a Milestone only while its Milestone issue is open: an open issue carrying a label in the Boundary record's Milestone label form, whose body is the Milestone rather than a feature. Until the user asks for one, this skill changes nothing: the project's own instructions and the other skills behave as they do with no Milestone.

## Planning

The coordinator runs it with the user, when the user asks for a Milestone. The Milestone issue is the user's agreement: everything agents later decide on their own inside the Milestone (who merges, what goes into a Release, how a design question is answered) rests on it, so every field in it comes from the user or from a feature's issue the user planned, never from a guess.

**The features are the user's.** A feature is a Spec with its Tickets, a lone Ticket with the issues it absorbs, or a few related issues the user agrees to treat as one. Agents may **propose** a feature: an open issue that serves the goal, or a gap between the goal and the features listed. Ask about each proposal as one question, saying why it might belong. Only the user adds a feature: a proposal the user does not take stays out, and nothing is listed or labelled for it.

### Steps

1. **Read the setup.** Read the Boundary record (the one the project's `CLAUDE.md` or `AGENTS.md` points to, usually `docs/agents/boundaries.md`) for its Milestone label form, its approvals and its budget, and the tracker doc (`docs/agents/issue-tracker.md`) for its operations. With no Boundary record, or one that names no Milestone label form, tell the user to run `setup-dev-skills`, which writes it, and stop: without the form there is no membership label. Then look for an open Milestone issue. If one exists, carry on from what it holds: to add a feature, go to "Adding a feature mid-Milestone"; to finish an interrupted planning, do only the steps whose result is missing.
2. **Goal.** Ask for the outcome the user wants by the Milestone's end. Done when the user agrees a one-paragraph goal in their own words.
3. **Features.** Ask which features deliver the goal. The user plans each one with an agent the usual way: `grill-with-docs` (or `grilling`), then `to-spec` and `to-tickets` for a multi-session feature, or one lone Ticket, in its own thread or here, as the user prefers. An existing issue counts as a feature once the user names it and says it is planned. Done when every feature the user named has its own issue holding its acceptance criteria, and the user has answered every proposal.
4. **Order.** Ask the build order, and whether features are built one at a time or several at once (and how many).
5. **Acceptance and limits.** Ask how the user will accept the Milestone at its review, what is excluded, the budget (the Boundary record's, or a tighter one for this Milestone), and any boundaries beyond the Boundary record: an action this Milestone's issues may also take, or one that needs the user's approval. "None beyond the Boundary record" is an answer; silence is not.
6. **Agree the draft.** Show the user the whole Milestone issue, its title and its label, in the shape below, and change it until the user agrees it.
7. **Write it.** The membership label fills the Boundary record's form with the next Milestone number: one more than the highest number among the labels already in that form (1 when there are none). Create the label if the tracker lacks it. Create the Milestone issue with the tracker doc's **Create an issue** operation, carrying the label, with the agreed text. Then, for each feature in order, apply the label (**Apply / remove labels**) to every open issue it holds (its own issue, its Tickets, the issues it absorbs or its related issues), and make its own issue a sub-issue of the Milestone issue (**Make an issue a sub-issue of a parent**) where it has no parent yet: the label, not the link, makes it a member. Read the Milestone issue and every labelled issue back from the tracker.

Planning **settles** when the Milestone issue reads back as the user agreed it and every open issue of every feature it lists carries the label. Tell the user in one line, with the issue's link, and go on to Startup verification. A feature planned after this point joins as "Adding a feature mid-Milestone" says.

### The Milestone issue

Title: `Milestone <n>: <name>`, with the number of its label. Body:

```
## Goal

<the outcome the user wants by the Milestone's end, in the user's words>

## Features, in build order

<One at a time, in this order. | In this order, up to <k> at once.> Each feature is its own issue carrying `<label>`.

| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | <issue link> <short name> | <Spec, lone Ticket or related issues> | <its acceptance criteria as the user agreed them, in short; its issue holds them in full> |

## Acceptance

- Every feature above is merged and its issue closed.
- <what the user will check at the Milestone review>

## Excluded

- <what is left out, and where it goes instead, if anywhere>

## Boundaries

- **Budget:** <the limit, or none>
- <each boundary beyond the Boundary record, or: None beyond the Boundary record.>
```

Keep the headings, their order and the table's first four columns: the skills that run inside the Milestone read its goal, its features in order, their acceptance criteria, its exclusions and its boundaries from them. Extra columns and notes are fine.

### Adding a feature mid-Milestone

When the user asks to add a feature while the Milestone runs, or takes one an agent proposed:

1. **Plan it with the user first**, as planning step 3 says. Until it is planned, nothing about it changes in the Milestone issue or its labels.
2. **List it.** Ask where it goes in the order. Rewrite the Milestone issue's body with its row in that place, marked `(added <date> by the user)`: read the whole body first, write it whole back with only that change, and read it back.
3. **Label it**, only after the row is in: apply the label to every open issue it holds and link its own issue as a sub-issue, as in planning step 7.

Listing before labelling keeps every labelled issue one the Milestone issue lists. A Release already planned keeps its scope; the new feature waits for the next Release planning. Tell the user in one line what was added and where. A change to the goal, the acceptance, an exclusion or a boundary is the user's too: write it the same way, once the user agrees it.

## Startup verification

Autonomous delivery assumes the coordinator can wake itself on a schedule, can see what a worker really did, can confirm a worker has stopped before another takes over, and runs threads on the skill version on main. **Startup verification** proves each, in this environment, before delivery starts: each **probe** is one short, bounded action whose pass rule rests on evidence observed afterwards, never on a tool's name or on a call returning success. A probe that cannot run here fails, with its limit; that is a valid result.

### Who runs it

The probes are coordinator actions, so run each one in the **runner** that will take that action during delivery: the agent that will schedule the check-ins and start and stop the workers. Where the coordinator itself holds the tools to schedule a message to itself and to start and stop a worker, the coordinator runs the probes. Where only a thread holds them (some environments give a project thread its own scheduling and subagent tools while the coordinator only starts and messages threads), the coordinator starts one **verification thread** with this skill, and that thread runs the probes and is the runner. Run it at the **regular** tier; load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it.

Where the tools for one probe are split between agents (for example, the coordinator starts a thread and reads its state, while only a thread holds the tool that stops one), split that probe the same way: each action runs in the agent that will take it during delivery, the result names which agent took each action, and the evidence is still read from the environment's own record, by the coordinator where it can read it.

A runner that lacks the tool for a probe records that probe as failed, with the missing tool as its limit. Probe the mechanism delivery will use; a different mechanism that happens to work is a different capability.

### Scratch area

The probes install nothing and change no settings, branch, label or file of the project. They write only:

- one one-shot scheduled check-in, from the runner into Step 2's target (deleted if it has not fired by the end of the run);
- one **marker** comment on the Milestone issue, written by the probe worker, and one more if the loaded-skill-version probe uses a worker thread;
- one throwaway **stop worker**, started by the confirmed-stop probe only to be stopped: it writes only token lines to a file in a scratch directory, and its brief ends it after 15 minutes, so it cannot outlive the run even if the stop fails;
- files in a scratch directory outside the project;
- one result comment on the Milestone issue, posted once by the runner in Step 6 (with no Milestone issue yet, only the rerun once the issue exists posts it).

Each probe uses a fresh **token**: a prefix and random hex (`sv-checkin-`, `sv-worker-`, `sv-stop-` or `sv-version-` followed by 8 hex characters), so evidence from an earlier run never passes this one.

### Step 1: Runtime settings

Record, from the runtime's own reports (a session-details call, the environment, settings files), never from memory: the environment kind (for example a cloud container or a local machine), the permission mode, whether a sandbox is on and how you read it, and the tools the runner holds for each probe. Write "unknown" for what the runtime does not report.

### Step 2: Probe the scheduled check-in

Probe the mechanism delivery's check-ins use ("Check-ins" under Delivery): the same scheduler, used by the same kind of agent (the coordinator, or a thread), firing into the agent that takes the check-ins during delivery. That agent is the probe's **target**: the coordinator, unless delivery hands its check-ins to another agent, which the result then names. Where the runner is not the target, split the probe as "Who runs it" says: the runner schedules, and the target sees the arrival.

- **Codex desktop:** discover the scheduler's current targeting rules and target this runner's existing chat. A heartbeat can implement the one-shot check-in only when the scheduler's records prove it expires after that firing; a next-run timestamp alone does not prove this. Record the scheduled time, confirm the token arrives here, and read back that no future firing remains. Delete the probe automation after the run. Record any requirement for the desktop app and machine to stay running as a limit.
- **Claude Code cloud project:** the runner is a thread, since the coordinator holds no scheduler. It reads the coordinator's session as the parent session in its own session details, and schedules a one-shot scheduled task bound to that session. A one-shot into the runner's own session wakes only the runner, so it is a different mechanism: it does not pass this probe.
- **Action:** schedule one one-shot check-in into the target, carrying the token, at the earliest time the scheduler allows (at most 10 minutes out). Its message reads `Startup verification check-in <token>: note the time this arrives; no other action.` Note the scheduled time, then end the turn: many schedulers deliver only once the target is idle.
- **Pass:** the check-in arrives in the target carrying the token, by the scheduled time plus 15 minutes. Record the arrival time, as the target saw it or as the target's own record shows it (its session's or chat's events), and the scheduler's own record of the firing if it keeps one. The scheduler recording a delivery is not a pass on its own, and neither is the token arriving in any agent other than the target.
- **Fail:** the schedule call errors, the scheduler refuses the target, or the token has not arrived in the target by that bound. The schedule call succeeding is not a pass. The target records the fail at its first wake past the bound (its own, a thread reporting, or the user writing) if no check-in carrying the token was seen; a verification thread that has not reported by the bound has failed this probe too.

### Step 3: Probe the real worker state

- **Action:** start one worker, of the kind delivery will use (a subagent or a thread), at the **cheap** tier, with this brief and nothing else: post one comment on the Milestone issue whose first line is `<!-- startup-verification marker <token> -->` and whose second line says it is a Startup verification probe and needs no action; then stop. With no Milestone issue yet, the worker has nowhere to write: record Real worker state as failed with that limit, and rerun the whole verification once the issue exists.
- **Read back:** once the worker reports done, or 10 minutes after it started, whichever is first, read the Milestone issue's comments from the tracker and look for the token. If it is missing, read once more a minute later before failing.
- **Pass:** a comment carrying the exact token exists, created after the probe started. Record its link and author.
- **Fail:** no such comment. The worker's own report does not count either way: a worker that says it posted the comment while the tracker shows none is the failure this probe guards against, and its report goes in the evidence as "worker said: ...".

### Step 4: Probe the confirmed stop

- **Action:** start one stop worker, of the kind delivery would take over from (a subagent or a thread), at the **cheap** tier, in the background, with this brief and nothing else: every 30 seconds, append one line holding the token and the current UTC time to a file in a scratch directory; write nothing else; end on your own after 15 minutes. Read its state from the environment's own record (its task or session state) and see it has not ended. Then stop it with the mechanism delivery will use for a takeover, and note the time. A call that only interrupts a thread's current turn leaves the thread able to resume, so it is a stop only if delivery's takeover relies on it too. A worker that is only **idle** (between turns, resumable by a message, its background work possibly still writing) has not ended.
- **Claude Code cloud project:** a project thread's record is its session's state from the session-details call. Running and idle are not ended; archiving the session ends it as archived and releases its machine.
- **Codex desktop:** for a worker thread with a runtime-managed background command, probe the runtime's archive operation. Read back its persisted archived state, its unloaded runtime state and the command's completion record. An interrupted turn or an unloaded thread alone does not prove a stop; a command still running after archive fails the probe. Record the tested worker kind and command, and limit the result to them: it does not establish what happens to detached descendants or a worker someone unarchives or resumes.
- **Read back:** within 2 minutes of the stop, read the worker's state from the environment's own record again. If it still reads not ended, read once more a minute later before failing.
- **Pass:** the record read before the stop shows the worker not ended (running, or idle), and the record read after shows it ended (stopped, killed, archived, or the environment's own word for it). Record both readings with their times. Where the runner can read the scratch file, a file with no line later than the stop time plus one interval corroborates the pass; it never makes one.
- **Fail:** the record still shows the worker not ended after the second read; the environment keeps no record of this worker kind that can be read (limit: no readable worker state); or the record shows the worker had already ended before the stop (limit: ended before the stop, so the stop was not tested). The stop call returning success, the worker going quiet, or its file ceasing to grow is not a pass. On a fail, record whether the worker was seen to end by its 15-minute cap.
- **Limits** to record even on a pass: a stop that can be undone (for example an archive that can be unarchived) stays a stop only while no one undoes it.

### Step 5: Probe the loaded skill version

- **Codex:** use a fresh consuming project's runtime skill catalog to identify the enabled plugin's path, then invoke that skill and read its installed root's manifest. Record the consumer's runtime and configuration. A source-checkout path does not pass the installed-plugin check. An isolated installation can test a proposed setup, but its result stays separate from the delivery runtime's result; a stale installed copy there still fails. Bring any required setup to the user during Milestone planning.
A **fresh thread** is one whose session started after the plugin's last change on main: it loaded the plugin the way a new delivery thread would. A verification thread started for this run usually is one; check it by comparing its session start time with the time of main's last commit to the plugin. A subagent shares its parent's session, so it reads its parent's load, never a fresh one.

- **Action:** in a fresh thread, invoke by name one skill of this plugin that only loads text (for example `model-tiers`), and read where the runtime says it loaded the skill from (its base directory). The plugin's root is the folder that holds that skill's `skills` folder; read the version in the plugin manifest there. Then read the version in the same manifest on the main branch of the plugin's source repository, from the remote: a local checkout may be behind. If the runner is a fresh thread, it does this itself. Otherwise it starts one fresh worker thread at the **cheap** tier, briefed to do the reading and post it in one comment on the Milestone issue whose first line is `<!-- startup-verification marker <token> -->`, followed by the load path and the version exactly as read, and reads that comment back from the tracker as in Step 3's read back. With no Milestone issue yet, the worker thread has nowhere to write: record Loaded skill version as failed with that limit, and rerun the whole verification once the issue exists.
- **Pass:** the runtime reported a load path, and the version in that plugin root's manifest equals main's. Record the load path, both versions, main's commit and the thread's session start time.
- **Fail:** the versions differ (limit: loaded `<version>`, main `<version>`, a stale cache); the runtime does not say where it loaded the skill from (limit: load path not reported); no fresh thread can be read (limit: not a fresh thread, with the thread's session start time); or main's manifest cannot be read (limit). The skill's name showing in the thread's skill list is not a pass: a stale copy carries the same names.
- **Limits** to record even on a pass: a load path inside a source checkout, rather than an installed or synced plugin folder, means threads here load that checkout, so record its branch and commit and say the version is the checkout's, not an installed one's; equal versions do not show equal text where a skill change can merge without a version bump; a worker thread's reading is its own report of what its runtime said, read from the tracker.

### Step 6: Post the result

Post one comment on the Milestone issue in this shape (with no Milestone issue yet, post nothing and hand nothing on: Steps 3 and 5 have failed, the whole verification is rerun once the issue exists, and only that rerun's comment is posted). The shape stays: one row per probe.

```
## Startup verification

Runner: <coordinator | thread <id or link>> · Run: <start>–<end> UTC
Runtime: <environment kind>; permission mode: <mode>; sandbox: <on | off | unknown> (<how read>); probe tools held: <list>

| Capability | Essential | How probed | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Scheduled check-in | yes | <tool and target; scheduled for <time>> | <pass or fail> | <arrival time with token, or what was seen by the bound> | <minimum delay, delivery only between turns, missing tool...> |
| Real worker state | yes | <worker kind and tier; marker token> | <pass or fail> | <marker comment link, or "no comment with token" plus "worker said: ..."> | <...> |
| Confirmed stop | yes | <worker kind and tier; stop mechanism and the agent that stopped it; token> | <pass or fail> | <state read before and after the stop, with times; scratch file's last line, if read> | <no readable worker state, ended before the stop, interrupt only, stop can be undone...> |
| Loaded skill version | yes | <fresh thread (runner or worker) and its session start; skill invoked> | <pass or fail> | <load path; loaded version; main's version and commit> | <loaded from a checkout, equal version is not equal text, worker's own report...> |

Verdict: ready | not ready: <each failed essential capability>
```

**Limits** says what a pass does not show (for example that a check-in waits for the runner's current turn to end) or why a probe failed. Delete the scheduled check-in if it never fired, so it cannot fire in the middle of delivery; make sure the stop worker has ended; leave the marker comments as evidence.

### Step 7: Report a failure before delivery starts

When an essential capability failed, tell the user before any delivery starts, naming each one with what it means and the limit seen:

- **Scheduled check-in** failed: the coordinator cannot wake itself, so between the user's messages nothing moves forward and a stalled worker goes unnoticed.
- **Real worker state** failed: the coordinator cannot confirm what a worker did, so it cannot trust a "done" or a ready pull request and cannot safely move on or take over.
- **Confirmed stop** failed: the coordinator cannot tell that a worker has stopped, so a takeover could leave two workers writing to the same branch or issue at once.
- **Loaded skill version** failed: threads here may run other skill text than main's, so they can follow rules main has since changed, and a stale cache goes unnoticed.

Delivery does not start until the user says how to go on. With every essential capability passing, say so in one line with a link to the result comment.

## Delivery

Delivery starts only when both hold: planning has settled, and the latest Startup verification result comment on the Milestone issue reads `Verdict: ready`. Until then nothing is built, labelled for a Release or started as a build thread for this Milestone; a `not ready` verdict waits on the user, as Step 7 of Startup verification says, until the user orders a rerun or says to go on, which the coordinator records as a comment on the Milestone issue quoting the user before delivery starts, naming each failed capability it starts without.

The coordinator then runs delivery as a **loop**. Each time it wakes (delivery starting, a thread reporting or asking, a scheduled check-in, the user writing), it reads the state afresh, as "Read the state" says, and takes every step below that the state calls for: first the check-ins, where "Check-ins" says they are due to be arranged, then, at a scheduled check-in, the Stand-up ("Stand-up"), then every takeover in progress ("Takeover"), then what the wake brings to steps 3 and 4 (a number to hand out, a merge to check, a re-read), then step 5, then steps 1 and 2. What a thread says it did, or fails to say, is a reason to read, never the state itself. The project's own instructions add only what is the project's: its thread limit, its model tier map, what else a brief carries, and its own extra rules; where they say nothing, this loop is the whole job.

Do every tracker read and write with the tracker doc's operations, cited by name below. A **delivery thread** is one this loop starts: a Release thread, a planning thread, a build thread, a check-in thread, or a stop thread ("Takeover"). Record each start on the tracker as you make it: a comment (**Comment on an issue**) on the issue the thread works on, whose first line is `<!-- milestone delivery thread -->` and whose second names the thread, its skill, its model tier and any Review depth its brief carries. A build thread's record goes on the issue it builds (a Spec thread's and a `to-tickets` thread's on the Spec's own issue; for related issues, each issue's own); a Release thread's on the release issue it cuts, or, for a Release thread that only plans, on the Milestone issue; a check-in thread's on the Milestone issue; a stop thread's on the issue the thread it stops works on. A feature has **started** when its first issue (the Spec's own issue, the lone Ticket, or the first of its related issues) has a record. A feature already being built when the loop first runs, by a thread started before it, gets its record then, from that thread's report or an open pull request for it, before any slot is counted. When a delivery thread reports that it ended without the result this loop waits for (a Release thread that planned no Release, for example), record that too, in a comment whose first line is `<!-- milestone delivery thread ended -->`.

- A **build thread is running** while the issue it builds has its record, is open and not parked, and holds no park record ("Takeover") newer than that record. Where an issue holds several build-thread records (a takeover adds one), the latest names its running thread. A `to-tickets` thread is running until the Spec's Tickets read back; its Spec thread then starts in the same slot.
- A **Release thread is running** from its record until an open release issue naming this Milestone, created after the record, reads back, or until an ended record follows it. One briefed to fill an empty release issue ends with its report, so there is no ended record to wait for; if it reports it planned no Release, the ended record above applies as for any Release thread.

### Read the state

At each wake, read:

- the **Milestone issue** (**Read an issue**): its features in order, its order rule (one at a time, or up to some number at once), its latest Startup verification result, its check-in records ("Check-ins") and its Stand-up records ("Stand-up");
- the **release doc** (the one the project's `CLAUDE.md` or `AGENTS.md` points to, usually `docs/agents/release.md`): its bump mode, its version file, what it says bumps, and its Release name and label forms;
- the **current Release**: the open release issue whose `**Milestone:**` line names this Milestone issue and whose label at least one issue carries, and every issue carrying its label, open and closed (**List issues**, filtered by that label). An open release issue naming this Milestone whose label no issue carries is **empty**: its planning chose nothing, so it is never done or cut;
- for each maintenance fix and feature of the current Release, in its build order (step 2): whether each of its issues is open, whether it is parked (**Park**), whether it is unblocked (**Count open blockers**), and its delivery-thread record;
- at a scheduled check-in, for each running build thread and Release thread, its real state, as "Stand-up" says;
- for each issue with a takeover in progress ("Takeover"), its takeover records and, until a stop record follows the stall, the stalled thread's state from the environment's own record;
- on a report of a merge or a request for a version number, or while a `Waiting:` hand-out record has no number after it, the pull request (its changed files and whether it merged) and the version file on the main branch, freshly fetched.

### Check-ins

From delivery's start until delivery is done, a schedule wakes the coordinator at the Boundary record's **check-in interval** (one hour when the record names none), with no step-in by the user. Each **scheduled check-in** is a wake of this loop like any other.

- **The mechanism** is the one the latest Startup verification result's Scheduled check-in row names, which passed only once its token arrived in the agent that takes the check-ins: the same scheduler, used by the same kind of agent (the coordinator, or a thread), into the same target, now recurring at the interval. Where that row failed and the user's go-on (the comment quoting the user, above) names Scheduled check-in among the capabilities delivery starts without, arrange none: the loop then wakes only on a thread reporting or the user writing.
  - Where the coordinator holds a scheduler that fires into its own chat or session, it schedules its check-ins itself. **Codex desktop:** a recurring heartbeat on the coordinator's existing chat, with no end bound; it fires only while the desktop app and the machine keep running.
  - Where only a thread holds a scheduler that can fire into the coordinator's session, the coordinator starts a **check-in thread** with this skill at the **cheap** tier, briefed with the Milestone issue, the interval and what to do (arrange, or end, as below), and records its start as above. **Claude Code cloud project:** the thread reads the coordinator's session as the parent session in its own session details, and creates a recurring scheduled task bound to that session. A thread's schedule into its own session wakes only that thread, so it is not this mechanism.
- **Arrange them** at the wake that starts delivery, before step 1: schedule a recurring firing at the interval (at the scheduler's shortest interval where that is longer: record that as a limit and tell the user in one line), each firing carrying `Milestone check-in: <Milestone issue link>`. Read the schedule back from the scheduler's own record: its id, its target, its interval and its next firing. Then post the **check-in record** (**Comment on an issue**) on the Milestone issue: first line `<!-- milestone check-in -->`, second `Every <interval> into <target>, scheduled by <coordinator | check-in thread <id>>; schedule <id>; next firing <time>.` The scheduler's own recurrence keeps the check-ins going: no agent stays awake for them, and a check-in thread's work ends with its report.
- **Read them** at every wake: check-ins are **running** while a check-in record has no `<!-- milestone check-in ended -->` comment after it, and **off** while a `<!-- milestone check-in failed -->` comment is on the Milestone issue or the user's go-on names Scheduled check-in. A check-in thread is running from its start record until a check-in record, a failed record or an ended record newer than it reads back. Until delivery is done, with check-ins neither running nor off and no check-in thread running, arrange them, also at the first wake of a delivery that began without them.
- **A failed arrangement** is a check-in thread reporting that it could not arrange them, or reporting with no check-in record to read back, or a coordinator's own schedule that errors or does not read back. Record it at that wake (**Comment on an issue**) on the Milestone issue: first line `<!-- milestone check-in failed -->`, second the limit seen. Then record the thread's end (above), where a thread tried, and tell the user in one line with the limit. From then on check-ins are off: delivery goes on, woken only by threads and the user, and no later wake arranges them.
- **End them** when delivery is done (step 5), before telling the user: end the schedule (the scheduler's delete, or disable where delete is not allowed), read back from the scheduler's own record that no future firing remains, and post `<!-- milestone check-in ended -->` on the Milestone issue, with that read-back on its second line. Where a thread arranged them, start a check-in thread to do this, briefed with the schedule's id from the check-in record. A check-in that still arrives after delivery is done finds nothing to do.

### Stand-up

Each **scheduled check-in** holds a **Stand-up** (the wake that starts delivery and a thread's or the user's wake are not one; a check-in that arrives once delivery is done, with the check-ins ended, holds none and posts no record). For every running build thread and Release thread (a check-in thread's work ends with its report), read its real state from the tracker and the branch, never its last message: the issue it works on (**Read an issue**), its branch (the commits pushed), its pull request if any (**Read a PR**). Activity **since the last check-in** is a commit pushed, a comment on the issue or the pull request, or a pull request change (opened, ready, merged, closed), none of them written by the coordinator itself (its nudge, stall, stop and park records are not activity); a thread's answer to a nudge counts as its comment on the issue, and an answer sent only as a message is not activity, since the next Stand-up cannot read it from the tracker; the last check-in is the latest Stand-up record's time, or delivery's start when there is none. The one exception is the thread's own start record, which counts as activity at its start time. Decide for each thread:

- **Being taken over**: its issue holds a takeover in progress ("Takeover"). No other decision: "Takeover" goes on with it.
- **Finished without reporting**: its pull request is ready or merged, or its issue closed, and the thread has not said so (a lost callback). Act as if it had reported: take the steps below that report would have brought (step 3 for a ready pull request, step 4 for a merged skill change, step 5 for a closed Release) and tell the thread what you decided, as on a report.
- **Active**: there is activity since the last check-in. No step.
- **Silent**: there is none, and no nudge to it is newer than its last activity. Nudge it once: send it a message asking where it is and what blocks it, to be answered by a comment on the issue it works on (an answer by message only does not count, so it would stall at the next check-in), and post the **nudge record** (**Comment on an issue**) on the issue it works on: first line `<!-- milestone nudge -->`, second `Nudged <thread> at <time>: nothing pushed, commented or changed on a pull request since <last check-in>.`
- **Still silent**: its nudge record has no activity after it. It has **stalled**. A build thread is taken over, as "Takeover" says. A Release thread is not: post its stall record (as "Takeover" step 1 does, with `a Release thread, not taken over` in place of the stall count) and tell the user in one line at that wake; while that record has no activity after it, the thread waits on the user and the Stand-up takes no step for it.

Parked work is not a running thread's, so the Stand-up decides nothing for it: see "Parked work".

Then post one **Stand-up record** (**Comment on an issue**) on the Milestone issue, after the decisions: first line `<!-- milestone stand-up -->`, second `Check-in <time>; previous <last check-in>.`, then one line per running thread, `- <issue>: <thread> (started <time>): <finished | active | being taken over | silent | still silent>; <the decision, or "no decision">`, or `No delivery thread is running; <the decision, or "no decision">` when none runs, then, when an issue of the current Release is parked, `Parked, skipped: <each parked issue>`. The Stand-up writes nothing but its nudges (message and nudge record), its stall records and this record, and the Milestone report reads the records for its decisions; the steps it brings, a takeover's included, write their own records as they do on a report.

### Takeover

A build thread that has **stalled** (still silent at a Stand-up after its nudge) may still be writing: idle is not ended, and a stop call returning success, or the thread going quiet, is no evidence that it stopped. Two workers on one branch is the failure a takeover guards against, so a fresh thread starts on a stalled thread's issue only once the environment's own record shows the stalled thread ended; where that cannot be shown, the work is parked instead. Each step writes a record on the issue the stalled thread works on, and every later wake reads the latest of them to know where the takeover stands: a **takeover is in progress** from a build thread's stall record until a park record, a takeover thread's start record or a takeover-ended record follows it.

1. **Record the stall**, at the Stand-up (**Comment on an issue**): first line `<!-- milestone stall -->`, second `<thread> still silent at <time> after its nudge of <time>; stall <n> of this feature.`, where `<n>` counts the stall records on the feature's issues (its own issue, its Tickets, its related issues), this one included. On a feature's second stall, park (step 5) at once and take no other step: a feature that stalls twice goes to the user.
2. **Find the proven stop.** It is the stop named by the Confirmed stop row of the latest Startup verification result, where that row passed: the same mechanism, taken by the same kind of agent, on the same kind of worker as the stalled thread. Where that row failed, where the stalled worker is of another kind than the one it stopped, or where this stop would need a different mechanism from the one it names, there is no proven stop: park (step 5), naming the stop that needs its own probe first. Otherwise stop the stalled thread at this wake:
   - Where the coordinator holds that stop, it takes it itself. **Codex desktop:** archive the worker thread.
   - Where only a thread holds it, start a **stop thread** with this skill at the **cheap** tier, briefed with the stalled thread and the stop to take, to write nothing on the tracker, and to report what the stop call returned, and record its start (above); its work ends with its report. **Claude Code cloud project:** the stop thread archives the stalled thread's session with the session archive call.
3. **Confirm the stop** from the environment's own record of the stalled thread, read the way the Confirmed stop row read it: right after the coordinator's own stop, or after a stop thread's start that errors, or at the stop thread's report, or, where none of these has come by then, at the first scheduled check-in after the stall record. A reading that shows it not ended is read once more a minute later. **Claude Code cloud project:** the coordinator reads `ARCHIVED` from the session-details call on the stalled thread's session; running and idle are not ended. **Codex desktop:** the worker thread reads back archived and unloaded, with its runtime-managed command ended.
   - **Ended:** post the **stop record** (**Comment on an issue**): first line `<!-- milestone stop confirmed -->`, second `<thread> read <state> at <time>, from <the record read>.` Then step 4.
   - **Not confirmed:** the second read still shows it not ended, whatever the stop call returned or the stop thread reported (that it took the stop, that it could not, or nothing by that check-in). Park (step 5), with the reading, unless the issue has closed meanwhile: then end the takeover as step 4 does for a closed issue.
4. **Start the fresh thread**, at the wake that posts the stop record, or at any later wake where a stop record has no takeover thread's start record after it, while the issue is still open (a ready or merged pull request included: the fresh thread finishes its review, merge or close from where it stands): a build thread with the skill, model tier and Review depth of the stalled thread's start record, on the same issue, briefed as "2. Start build threads" says and also with the thread it takes over from, that its stop is confirmed, and to resume from the pushed branch (name it) and the tracker (the issue, its comments and attempt records, its pull request), keeping what is pushed. Its start record (above) has a third line, `Takes over from <thread>; stop confirmed at <time>.` From then on it is the issue's running thread, in the same slot. A start that errors is parked (step 5), with the error. Where the issue has closed by then, start none: post the **takeover-ended record** (**Comment on an issue**), first line `<!-- milestone takeover ended -->`, second `<issue> closed at <time>: the work finished; no fresh thread.`, and take the steps its finish brings, as "Finished without reporting" says, with no thread to tell.
5. **Park** the work, on the issue the stalled thread works on, with the tracker doc's **Park** operation: the `parked` label, and its comment, the **park record**: first line `<!-- milestone parked -->`, second the reason (second stall; no proven stop: <the stop that needs its own probe>; stop not confirmed: <the reading>; takeover start failed: <the error>), then whether the stalled thread's stop was confirmed (where it was not, a writer may remain), and links to the nudge, stall and stop records and the pull request, if any, as the attempt history. Tell the user in one line, with the link, at the wake that posts the park record and at no later one. Then go on with the rest of delivery.

### Parked work

An issue is parked when the tracker doc's **Park** operation reads it so: parked by a takeover, or by a build thread whose review would not settle. Parked work is skipped at every wake until the user lifts the park: no nudge, stall or takeover for it, no build thread for it (step 2), no place in a Release grouping (step 1), and the work it blocks is not started, since a parked issue is open. Under one at a time it holds no slot (step 2). Resuming a feature once the user lifts its park is not part of this skill yet: after a takeover's park, the issue reads as started with no running thread (its park record is newer than its thread's record), so it keeps its place in the order and starts nothing.

### 1. Plan a Release

When there is no current Release (an empty release issue does not count as one), no Release thread is running, and the grouping below is not empty, group the Milestone's features into a Release and hand it to the `release` skill's Release planning, which owns the scope rule and the release labels. That is the first Release when delivery has just started (no closed release issue names this Milestone yet), and a later one when the last Release was cut and planned nothing because every feature left was blocked or parked, and one has since become free. Every other Release is planned by the Release thread of the one before it (step 5). The **grouping**: the Milestone's planned features that are still open, carry no release label, are not parked and are unblocked, in the Milestone issue's order, at most 5 (only the user raises the cap, and only for one Release), never passing over a qualifying feature to take a later one; a feature blocked only by one taken earlier in the same group qualifies. A Spec counts with its Tickets, as one feature.

Start one Release thread with the `release` skill, at the tier that skill names, briefed with the Milestone issue, the release doc, and your grouping in order (each feature with its issues), and with what was cut before: for the first Release, that no Release of this Milestone has been cut yet, so there is no Triage batch or Release-end Retro planning to read and the plan is the feature scope only; for a later one, the last release issue cut, whose Triage batch and Release-end Retro planning it reads. Where an empty release issue names this Milestone, the brief names it too: its planning chose nothing, so the thread chooses the scope now and fills that issue, opening no second one; for that issue this overrides the `release` skill's "Rerun first". The brief also says: if no planned feature qualifies and no maintenance fix joins, open no release issue, label nothing, and report that it planned no Release. It labels the issues and opens the release issue; you label nothing. Start no build thread until its report, then read the release issue and the issues carrying its label back from the tracker: from then on they are the current Release. If they differ from your grouping, tell the user in one line how; the release issue stands.

### 2. Start build threads

The **slots** are the smaller of the project's thread limit and the Milestone issue's order rule (one at a time is one slot; up to k at once is k slots); with neither, one. Each running build thread takes a slot. While a re-read is due (step 4) or a Release thread is running, start no build thread.

The current Release's **build order** is its maintenance fixes (the release issue's "Maintenance fixes" list, each a lone Ticket), in the order the release issue gives and, where it gives none, before the features, since each fixes something a feature relies on or is severe; then its features, in the Milestone issue's order. While a slot is free, start the **next** one: the first in that build order that is open, has not started, is not parked and is unblocked. A started feature of related issues, once the issue its last thread built has closed, continues with its next open issue in the same slot, before any later one. Under one at a time, the next starts only once each one before it in the build order has closed or is parked: a parked one waits on the user and holds no slot. One still blocked by an open issue waits; a later one may take a free slot meanwhile only where the order rule allows several at once.

The thread follows the feature's kind:

- a **Spec** whose Tickets are filed (its sub-issues, or issues naming it as their parent): a Spec thread with `implement-spec`;
- a **Spec** with no Tickets yet: first a planning thread with `to-tickets`, which takes the feature's slot; its Spec thread starts once the Tickets read back from the tracker;
- a **lone Ticket**: a Ticket thread with `implement`, for the Ticket and the issues it absorbs;
- **related issues** treated as one feature: one Ticket thread with `implement` per issue, one after another in the feature's order, in the feature's one slot.

Every brief carries: the skill; a link to the issue; a link to the Milestone issue, so the thread knows it is inside it; the **model tier** (the issue's Model tier line, regular when it has none); a **Review depth** only when the issue or the user names one (with none, leave it out, so `agentic-review` chooses the depth); and what the project's instructions add. Start the thread on the model its tier maps to: load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it. Record the start as above.

### 3. Hand out version numbers

A build thread asks for a version number just before it merges a pull request. Hand one out only where the release doc's bump mode says **pull requests bump**. Where it says Releases bump, or there is no release doc, tell the thread to merge with no version change: the Release's own bump covers it.

Where pull requests bump:

1. **Does it bump?** Read the pull request's changed files. If it changes nothing the release doc says bumps, give no number and tell the thread to merge with no bump.
2. **One at a time.** A number is **out** while main's version file has not reached it, its pull request is open, and the thread it was handed to is running. Read the version file on main and the hand-out records on the current Release's issues (and on a pull request that builds no issue, where its record is): a record is out when all three hold. A record whose pull request closed unmerged, or whose issue or pull request is parked, is void, and so is one whose thread has ended. While one is out, hand out none: record the request on the same issue, in the same comment form with the second line `Waiting: <pull request> asked while <number> was out.`, and tell the thread to wait. At the first wake when no number is out (a void one counts as not out) and a waiting request has no number after it, hand out to the waiting requests, one at a time, in the order they asked. So pull requests that bump merge one at a time, each on top of the one before.
3. **The number** is the version on main raised by the part the release doc's rule gives for what this pull request changes, or, where the release doc gives no such rule, the part the `release` skill's bump-size rule gives. Record it first, on the issue the pull request builds (for a Spec pull request, the Spec; for one that builds no issue, the pull request itself), in a comment (**Comment on an issue**) whose first line is `<!-- milestone version hand-out -->` and whose second reads `Version <number> for <pull request>: merge it next, with the bump as its last commit, as the release doc says.` Then tell the thread its number.
4. **A repeat.** A thread that asks again because main's version moved under it gets a new number from the new main, recorded the same way; its earlier record says nothing more and is void.
5. **After the merge**, read the version file on main. It should read the number. If it reads anything else, hand out no further number and tell the merging thread to put main right first.

### 4. Re-read Tickets after a skill merge

A **skill merge** is a merged pull request that changed a skill the project's threads load (its `SKILL.md` or a file in its folder). Right after one, before any further thread starts, re-read the open issues of the Milestone (carrying its membership label) that no running thread is building, whose body names the changed skill or a file the merge changed. A running thread keeps the skill version it started with until its Ticket or Spec is done.

Read each against main's new text of the skill, then:

- where the change makes the issue wrong or incomplete, update it: read the whole body (**Read an issue**), write it whole back with only that change and a one-line note naming the merge, and read it back. A change to the issue's acceptance criteria that would change the Milestone's agreement (its goal, acceptance or exclusions) goes to the user instead, one question, and that feature waits for the answer;
- where the change makes it obsolete, close it (**Close**) with a note naming the merge;
- otherwise comment (**Comment on an issue**) that it was re-read after the merge and still fits.

Then read the blockers again (**Count open blockers**) and take the next start from what they now say. Where the project runs `triage` (its instructions say so), start a thread with `triage` for the re-read instead, briefed with the merge, the changed skill, the version main now reads, the issues above, and the three outcomes above to take for each one (update it with its re-read note, close it as obsolete with its note, or comment that it still fits, with a change to the agreement going to the user), and start nothing further until its report.

### 5. Start the Release thread

When the current Release has at least one issue carrying its label and every one of them is closed, the Release is done; an empty release issue is never done, so it starts no Release thread. If a Release thread is already running (as defined above), it is cutting this Release: start none. Otherwise start one Release thread with the `release` skill, at the tier that skill names, briefed with the release issue and the Milestone issue, and with this: if no planned feature qualifies and no maintenance fix joins, open no release issue, label nothing, and report that it planned no Release. It runs the Triage batch and the Release-end Retro planning for this Release, cuts it, and plans the next Release from the Milestone issue's order; that skill says how. Record the start on the release issue. Start no build thread until it reports; then read the new release issue back, as in step 1, and go on from step 2.

When the Release thread reports that it planned no Release, or the release issue it opened reads back empty, record that it ended (above) and read the Milestone issue's features. An empty release issue is left as it is: start no Release thread for it, and tell the user in one line that it holds no issue, so it is no Release to cut; step 1 fills it once a feature is free, and that Release thread ends with its report, with no ended record to wait for. With none left open, delivery is done: end the check-ins ("Check-ins"), then tell the user in one line, with the Milestone issue's link. The Milestone review follows; its report is not part of this skill yet. With some still open (each blocked or parked), tell the user which, with what holds each; step 1 plans the next Release once one of them is free.
