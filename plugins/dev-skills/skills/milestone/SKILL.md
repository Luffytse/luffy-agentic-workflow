---
name: milestone
description: "Plan, start and deliver a Milestone: write the Milestone issue with the user (goal, features with acceptance criteria, exclusions, budget, boundaries, membership label) and add a feature mid-Milestone; run Startup verification, which proves in this environment that a scheduled check-in fires, that a worker's real state can be read back from the tracker, that a stopped worker is confirmed stopped and that a fresh thread loads main's skill version; then run delivery as the coordinator: group the features into Releases, start build threads within the limits and in order, hand out version numbers, re-read open Tickets after a skill merge and start each Release thread. Use when the user asks for a Milestone or to add a feature to one, when a Milestone is about to start or is running autonomous delivery, or when the user asks whether this environment can run a Milestone unattended."
---

# Milestone

A **Milestone** is a product goal the user sets, written down in one Milestone issue, which agents deliver unattended across one or more Releases. This skill runs it in three phases, in order:

1. **Planning**, with the user: the Milestone issue is written and every feature in it is labelled.
2. **Startup verification**, once the Milestone issue exists: proof that this environment can run delivery unattended.
3. **Delivery**, run by the coordinator: it groups the planned features into Releases, starts build threads within the limits and in order, hands out version numbers, re-reads open Tickets after a skill merge and starts each Release thread. It starts only once both phases before it are done (see "Delivery").

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

A runner that lacks the tool for a probe records that probe as failed, with the missing tool as its limit. Probe the mechanism delivery will use; a different mechanism that happens to work is a different capability.

### Scratch area

The probes install nothing and change no settings, branch, label or file of the project. They write only:

- one one-shot scheduled check-in to the runner (deleted if it has not fired by the end of the run);
- one **marker** comment on the Milestone issue, written by the probe worker, and one more if the loaded-skill-version probe uses a worker thread;
- one throwaway **stop worker**, started by the confirmed-stop probe only to be stopped: it writes only token lines to a file in a scratch directory, and its brief ends it after 15 minutes, so it cannot outlive the run even if the stop fails;
- files in a scratch directory outside the project;
- one result comment on the Milestone issue, posted once by the runner in Step 6 (with no Milestone issue yet, only the rerun once the issue exists posts it).

Each probe uses a fresh **token**: a prefix and random hex (`sv-checkin-`, `sv-worker-`, `sv-stop-` or `sv-version-` followed by 8 hex characters), so evidence from an earlier run never passes this one.

### Step 1: Runtime settings

Record, from the runtime's own reports (a session-details call, the environment, settings files), never from memory: the environment kind (for example a cloud container or a local machine), the permission mode, whether a sandbox is on and how you read it, and the tools the runner holds for each probe. Write "unknown" for what the runtime does not report.

### Step 2: Probe the scheduled check-in

- **Action:** schedule one one-shot check-in to the runner itself, carrying the token, at the earliest time the scheduler allows (at most 10 minutes out). Note the scheduled time, then end the turn: many schedulers deliver only once the runner is idle.
- **Pass:** the check-in arrives in the runner carrying the token, by the scheduled time plus 15 minutes. Record the arrival time, and the scheduler's own record of the firing if it keeps one.
- **Fail:** the schedule call errors, or the token has not arrived by that bound. The schedule call succeeding is not a pass. If the runner is woken by anything else past the bound with no check-in seen, record the fail then. If nothing wakes it, the coordinator records the fail: a verification thread that has not reported by the bound has failed this probe. A coordinator that is itself the runner records the fail at its first wake past the bound, whether that wake is its own or the user writing, if no check-in was seen.

### Step 3: Probe the real worker state

- **Action:** start one worker, of the kind delivery will use (a subagent or a thread), at the **cheap** tier, with this brief and nothing else: post one comment on the Milestone issue whose first line is `<!-- startup-verification marker <token> -->` and whose second line says it is a Startup verification probe and needs no action; then stop. With no Milestone issue yet, the worker has nowhere to write: record Real worker state as failed with that limit, and rerun the whole verification once the issue exists.
- **Read back:** once the worker reports done, or 10 minutes after it started, whichever is first, read the Milestone issue's comments from the tracker and look for the token. If it is missing, read once more a minute later before failing.
- **Pass:** a comment carrying the exact token exists, created after the probe started. Record its link and author.
- **Fail:** no such comment. The worker's own report does not count either way: a worker that says it posted the comment while the tracker shows none is the failure this probe guards against, and its report goes in the evidence as "worker said: ...".

### Step 4: Probe the confirmed stop

- **Action:** start one stop worker, of the kind delivery would take over from (a subagent or a thread), at the **cheap** tier, in the background, with this brief and nothing else: every 30 seconds, append one line holding the token and the current UTC time to a file in a scratch directory; write nothing else; end on your own after 15 minutes. Read its state from the environment's own record (its task or session state) and see it running. Then stop it with the mechanism delivery will use for a takeover, and note the time. A call that only interrupts a thread's current turn leaves the thread able to resume, so it is a stop only if delivery's takeover relies on it too.
- **Read back:** within 2 minutes of the stop, read the worker's state from the environment's own record again. If it still reads running, read once more a minute later before failing.
- **Pass:** the record read before the stop shows the worker running, and the record read after shows it ended (stopped, killed, archived, or the environment's own word for it). Record both readings with their times. Where the runner can read the scratch file, a file with no line later than the stop time plus one interval corroborates the pass; it never makes one.
- **Fail:** the record still shows the worker running after the second read; the environment keeps no record of this worker kind the runner can read (limit: no readable worker state); or the record shows the worker had already ended before the stop (limit: ended before the stop, so the stop was not tested). The stop call returning success, the worker going quiet, or its file ceasing to grow is not a pass. On a fail, record whether the worker was seen to end by its 15-minute cap.

### Step 5: Probe the loaded skill version

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
| Confirmed stop | yes | <worker kind and tier; stop mechanism; token> | <pass or fail> | <state read before and after the stop, with times; scratch file's last line, if read> | <no readable worker state, ended before the stop, interrupt only...> |
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

The coordinator then runs delivery as a **loop**. Each time it wakes (delivery starting, a thread reporting or asking, a scheduled check-in, the user writing), it reads the state afresh, as "Read the state" says, and takes every step below that the state calls for: first what the wake brings to steps 3 and 4 (a number to hand out, a merge to check, a re-read), then step 5, then steps 1 and 2. What a thread says it did is a reason to read, never the state itself. The project's own instructions add only what is the project's: its thread limit, its model tier map, what else a brief carries, and its own extra rules; where they say nothing, this loop is the whole job. Checking in on a thread that has gone quiet, and taking over from it, are not part of this skill yet.

Do every tracker read and write with the tracker doc's operations, cited by name below. A **delivery thread** is one this loop starts: a Release thread, a planning thread, or a build thread. Record each start on the tracker as you make it: a comment (**Comment on an issue**) on the issue the thread works on, whose first line is `<!-- milestone delivery thread -->` and whose second names the thread, its skill, its model tier and any Review depth its brief carries. A build thread's record goes on the issue it builds (a Spec thread's and a `to-tickets` thread's on the Spec's own issue; for related issues, each issue's own); a Release thread's on the release issue it cuts, or, for a Release thread that only plans, on the Milestone issue. A feature has **started** when its first issue (the Spec's own issue, the lone Ticket, or the first of its related issues) has a record. A feature already being built when the loop first runs, by a thread started before it, gets its record then, from that thread's report or an open pull request for it, before any slot is counted. When a delivery thread reports that it ended without the result this loop waits for (a Release thread that planned no Release, for example), record that too, in a comment whose first line is `<!-- milestone delivery thread ended -->`.

- A **build thread is running** while the issue it builds has its record and is open and not parked. A `to-tickets` thread is running until the Spec's Tickets read back; its Spec thread then starts in the same slot.
- A **Release thread is running** from its record until an open release issue naming this Milestone, created after the record, reads back, or until an ended record follows it.

### Read the state

At each wake, read:

- the **Milestone issue** (**Read an issue**): its features in order and its order rule (one at a time, or up to some number at once);
- the **release doc** (the one the project's `CLAUDE.md` or `AGENTS.md` points to, usually `docs/agents/release.md`): its bump mode, its version file, what it says bumps, and its Release name and label forms;
- the **current Release**: the open release issue whose `**Milestone:**` line names this Milestone issue and whose label at least one issue carries, and every issue carrying its label, open and closed (**List issues**, filtered by that label). An open release issue naming this Milestone whose label no issue carries is **empty**: its planning chose nothing, so it is never done or cut;
- for each maintenance fix and feature of the current Release, in its build order (step 2): whether each of its issues is open, whether it is parked (**Park**), whether it is unblocked (**Count open blockers**), and its delivery-thread record;
- on a report of a merge or a request for a version number, or while a `Waiting:` hand-out record has no number after it, the pull request (its changed files and whether it merged) and the version file on the main branch, freshly fetched.

### 1. Plan a Release

When there is no current Release (an empty release issue does not count as one), no Release thread is running, and the grouping below is not empty, group the Milestone's features into a Release and hand it to the `release` skill's Release planning, which owns the scope rule and the release labels. That is the first Release when delivery has just started (no closed release issue names this Milestone yet), and a later one when the last Release was cut and planned nothing because every feature left was blocked or parked, and one has since become free. Every other Release is planned by the Release thread of the one before it (step 5). The **grouping**: the Milestone's planned features that are still open, carry no release label, are not parked and are unblocked, in the Milestone issue's order, at most 5 (only the user raises the cap, and only for one Release), never passing over a qualifying feature to take a later one; a feature blocked only by one taken earlier in the same group qualifies. A Spec counts with its Tickets, as one feature.

Start one Release thread with the `release` skill, at the tier that skill names, briefed with the Milestone issue, the release doc, and your grouping in order (each feature with its issues), and with what was cut before: for the first Release, that no Release of this Milestone has been cut yet, so there is no Triage batch or Release-end Retro planning to read and the plan is the feature scope only; for a later one, the last release issue cut, whose Triage batch and Release-end Retro planning it reads. Where an empty release issue names this Milestone, the brief names it too: its planning chose nothing, so the thread chooses the scope now and fills that issue, opening no second one. The brief also says: if no planned feature qualifies and no maintenance fix joins, open no release issue, label nothing, and report that it planned no Release. It labels the issues and opens the release issue; you label nothing. Start no build thread until its report, then read the release issue and the issues carrying its label back from the tracker: from then on they are the current Release. If they differ from your grouping, tell the user in one line how; the release issue stands.

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

When the Release thread reports that it planned no Release, or the release issue it opened reads back empty, record that it ended (above) and read the Milestone issue's features. An empty release issue is left as it is: start no Release thread for it, and tell the user in one line that it holds no issue, so it is no Release to cut; step 1 fills it once a feature is free. With none left open, delivery is done: tell the user in one line, with the Milestone issue's link. The Milestone review follows; its report is not part of this skill yet. With some still open (each blocked or parked), tell the user which, with what holds each; step 1 plans the next Release once one of them is free.
