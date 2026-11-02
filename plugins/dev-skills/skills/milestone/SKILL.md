---
name: milestone
description: "Run a Milestone's Startup verification: before autonomous delivery starts, prove in this environment that a scheduled check-in fires and that a worker's real state can be read back from the tracker, and post the result on the Milestone issue. Use when a Milestone is about to start autonomous delivery, or the user asks whether this environment can run a Milestone unattended."
---

# Milestone

A **Milestone** is a product goal the user sets, written down in one Milestone issue, which agents deliver unattended across one or more Releases. This skill holds only **Startup verification** for now. Writing the Milestone issue and running its delivery arrive in a later version of this skill; until then, run Startup verification, hand the result back, and go no further.

## Startup verification

Autonomous delivery assumes the coordinator can wake itself on a schedule and can see what a worker really did. **Startup verification** proves both, in this environment, before delivery starts: each **probe** is one short, bounded action whose pass rule rests on evidence observed afterwards, never on a tool's name or on a call returning success. A probe that cannot run here fails, with its limit; that is a valid result.

### Who runs it

The probes are coordinator actions, so run each one in the **runner** that will take that action during delivery: the agent that will schedule the check-ins and start the workers. Where the coordinator itself holds the tools to schedule a message to itself and to start a worker, the coordinator runs the probes. Where only a thread holds them (some environments give a project thread its own scheduling and subagent tools while the coordinator only starts and messages threads), the coordinator starts one **verification thread** with this skill, and that thread runs the probes and is the runner. Run it at the **regular** tier; load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it.

A runner that lacks the tool for a probe records that probe as failed, with the missing tool as its limit. Probe the mechanism delivery will use; a different mechanism that happens to work is a different capability.

### Scratch area

The probes install nothing and change no settings, branch, label or file of the project. They write only:

- one one-shot scheduled check-in to the runner (deleted if it has not fired by the end of the run);
- one **marker** comment on the Milestone issue, written by the probe worker;
- files in a scratch directory outside the project, if any.

Each probe uses a fresh **token**: a prefix and random hex (`sv-checkin-` or `sv-worker-` followed by 8 hex characters), so evidence from an earlier run never passes this one.

### Step 1: Runtime settings

Record, from the runtime's own reports (a session-details call, the environment, settings files), never from memory: the environment kind (for example a cloud container or a local machine), the permission mode, whether a sandbox is on and how you read it, and the tools the runner holds for each probe. Write "unknown" for what the runtime does not report.

### Step 2: Probe the scheduled check-in

- **Action:** schedule one one-shot check-in to the runner itself, carrying the token, at the earliest time the scheduler allows (at most 10 minutes out). Note the scheduled time, then end the turn: many schedulers deliver only once the runner is idle.
- **Pass:** the check-in arrives in the runner carrying the token, by the scheduled time plus 15 minutes. Record the arrival time, and the scheduler's own record of the firing if it keeps one.
- **Fail:** the schedule call errors, or the token has not arrived by that bound. The schedule call succeeding is not a pass. If the runner is woken by anything else past the bound with no check-in seen, record the fail then. If nothing wakes it, the coordinator records the fail: a verification thread that has not reported by the bound has failed this probe.

### Step 3: Probe the real worker state

- **Action:** start one worker, of the kind delivery will use (a subagent or a thread), at the **cheap** tier, with this brief and nothing else: post one comment on the Milestone issue whose first line is `<!-- startup-verification marker <token> -->` and whose second line says it is a Startup verification probe and needs no action; then stop. With no Milestone issue yet, the worker has nowhere to write: record Real worker state as failed with that limit, or run this probe once the issue exists.
- **Read back:** once the worker reports done, or 10 minutes after it started, whichever is first, read the Milestone issue's comments from the tracker and look for the token. If it is missing, read once more a minute later before failing.
- **Pass:** a comment carrying the exact token exists, created after the probe started. Record its link and author.
- **Fail:** no such comment. The worker's own report does not count either way: a worker that says it posted the comment while the tracker shows none is the failure this probe guards against, and its report goes in the evidence as "worker said: ...".

### Step 4: Post the result

Post one comment on the Milestone issue in this shape (with no Milestone issue yet, hand the comment to whoever writes it, to post once it exists). Each later probe adds a row; the shape stays.

```
## Startup verification

Runner: <coordinator | thread <id or link>> · Run: <start>–<end> UTC
Runtime: <environment kind>; permission mode: <mode>; sandbox: <on | off | unknown> (<how read>); probe tools held: <list>

| Capability | Essential | How probed | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Scheduled check-in | yes | <tool and target; scheduled for <time>> | <pass or fail> | <arrival time with token, or what was seen by the bound> | <minimum delay, delivery only between turns, missing tool...> |
| Real worker state | yes | <worker kind and tier; marker token> | <pass or fail> | <marker comment link, or "no comment with token" plus "worker said: ..."> | <...> |

Verdict: ready | not ready: <each failed essential capability>
```

**Limits** says what a pass does not show (for example that a check-in waits for the runner's current turn to end) or why a probe failed. Delete the scheduled check-in if it never fired, so it cannot fire in the middle of delivery; leave the marker comment as evidence.

### Step 5: Report a failure before delivery starts

When an essential capability failed, tell the user before any delivery starts, naming each one with what it means and the limit seen:

- **Scheduled check-in** failed: the coordinator cannot wake itself, so between the user's messages nothing moves forward and a stalled worker goes unnoticed.
- **Real worker state** failed: the coordinator cannot confirm what a worker did, so it cannot trust a "done" or a ready pull request and cannot safely move on or take over.

Delivery does not start until the user says how to go on. With every essential capability passing, say so in one line with a link to the result comment.
