---
name: milestone
description: "Plan and start a Milestone: write the Milestone issue with the user (goal, features with acceptance criteria, exclusions, budget, boundaries, membership label), add a feature mid-Milestone, and run Startup verification, which proves in this environment that a scheduled check-in fires, that a worker's real state can be read back from the tracker, that a stopped worker is confirmed stopped and that a fresh thread loads main's skill version, before autonomous delivery starts. Use when the user asks for a Milestone or to add a feature to one, when a Milestone is about to start autonomous delivery, or when the user asks whether this environment can run a Milestone unattended."
---

# Milestone

A **Milestone** is a product goal the user sets, written down in one Milestone issue, which agents deliver unattended across one or more Releases. This skill runs it in three phases, in order:

1. **Planning**, with the user: the Milestone issue is written and every feature in it is labelled.
2. **Startup verification**, once the Milestone issue exists: proof that this environment can run delivery unattended.
3. **Delivery**: agents build the planned features. It starts only once both phases before it are done (see "Delivery").

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

Delivery starts only when both hold: planning has settled, and the Startup verification result comment on the Milestone issue reads `Verdict: ready`. Until then nothing is built, labelled for a Release or started as a build thread for this Milestone; a `not ready` verdict waits on the user, as Step 7 of Startup verification says. Delivery's own steps (grouping the planned features into Releases, starting build threads, handing out version numbers) are not part of this skill yet; until they are, once both hold, the coordinator delivers as the project's own instructions say.
