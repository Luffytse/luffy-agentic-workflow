---
name: worker-control
description: "Start, check, stop, pause and resume workers in the tool you run in, and run the check that proves it here. Use when a coordinator starts, reads, stops, pauses or schedules workers, or a caller needs that check."
user-invocable: false
---

# Worker control

A coordinator runs its workers through the tool it runs in (its **Harness**): the runtime that starts sessions, wakes the coordinator and keeps their state. This skill holds how; deciding what work starts, when and why stays with the caller. The Harness's own record is the only source of a worker's state, its end and its failure; tracker comments are an audit trail, never that source. Every method comes from the Harness's docs, cited, or is marked runtime-reported and proved by the check; never from a tool's name alone, a dry run or memory.

The coordinator may run this skill as a subagent, at the **regular** tier, to keep its own context small (load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it). The subagent may detect, read the reference and read records. Every action of the check runs in the agent that will take it during the work (see "Who acts").

## 1. Detect how workers run here

Read what the runtime itself reports: first the names of the tools you hold (a coordinator may have no shell), then the session-details record where you can read it, then a shell's environment where one exists, as a second signal only. Never decide from memory, the project's instructions or the tracker.

| Tools you hold (first match wins) | Way workers run | Reference |
|---|---|---|
| `mcp__hearthbot__start_thread` | claude.ai project: you are its coordinator; workers are threads | [claude-code-project-threads.md](claude-code-project-threads.md) |
| `mcp__hearthbot__message_coordinator`, without `start_thread` | claude.ai project: you are a thread, a worker | [claude-code-project-threads.md](claude-code-project-threads.md) |
| `ccd_session` / `ccd_session_mgmt` tools | Claude Code desktop: subagents and other sessions | [claude-code-sessions.md](claude-code-sessions.md) |
| `collaboration.spawn_agent` and `collaboration.list_agents`, none of the above | Codex: subagents | [codex-subagents.md](codex-subagents.md) |
| the Agent tool, none of the above | Claude Code session (CLI, web, desktop): subagents | [claude-code-sessions.md](claude-code-sessions.md) |

Then confirm against the reference's **Detect** section and record each fact you matched, with where you read it. The tool names decide: a fact the reference has not seen before (an unfamiliar environment kind, say) is recorded, not a reason to fall back. Only tools that match no row, or tools that contradict the reference's Detect section, make the Harness unknown: use the fallback.

**Role** comes from explicit runtime lineage only: a parent session in the session-details record, a hand-back tool that returns to a caller, or a tool for messaging your coordinator. In Codex, use the runtime's explicit task path as the reference describes (`/root` versus a descendant); a missing path leaves the role unknown. Being able to start workers never makes you the coordinator; workers can start workers too. A worker never takes the coordinator's role; it may take an action of the check that the coordinator hands it.

## 2. Load the reference

Read the whole reference. **What the harness does by itself** is what the coordinator relies on and never rebuilds in records of its own. **Methods the coordinator adds** are the only lifecycle actions it takes: start a worker, read its state, notice it ended or failed, stop it and read the stop back, pause and resume, arrange and end a check-in. A line marked runtime-reported is not on a doc page: the check proves it, or it is a limit.

## 3. Fallback: a Harness with no reference

1. Name the Harness from what the runtime reports about itself.
2. Read that Harness's own docs on managing workers: starting them, their states, notifications, stopping, pausing, scheduling. Use the pages the runtime or its help names, or its official docs site.
3. For each method, write down what the docs give, with the page. A method the docs do not give is **not available**, with that as its limit. Never fill it from another Harness's reference, from tracker comments or from a guess.
4. Tell the user in one line: no reference for this Harness, the methods were read from those pages, and each one not available.
5. Run the check on the methods found. With no docs found, every method fails with the limit "no docs found".

## 4. The check

Before unattended work relies on them, prove here each method the coordinator will rely on. Each **probe** is one short, bounded action whose pass rests on the Harness's own record read afterwards, never on a call returning success, silence or a worker's own claim. A probe that cannot run here fails, with its limit: that is a valid result.

**Who acts.** Run each action in the agent that will take it during the work: the coordinator where it holds the tool, otherwise the agent the reference names (for example a worker the coordinator starts to hold a stop or scheduling tool it lacks). Split a probe whose tools are split, and record which agent took each action. An agent that lacks a probe's tool records the probe failed, with the missing tool as its limit. Probe the method the reference names; another mechanism that happens to work is a different capability.

**Scratch.** Each probe uses a fresh **token** (`wc-<probe>-` and 8 random hex characters). Probe workers run at the **cheap** tier, write only to a scratch directory outside the project, and end on their own after 15 minutes unless the probe needs them longer, so none outlives the run. Nothing else in the project changes.

**Records that are notifications.** Where the reference's state or read-back is a notification rather than a record the coordinator can read on demand (for example a subagent's completion or stop notification), that notification is the record: "running" means started and no end notification yet, and "ended" means its end notification arrived. The passes below name both forms.

1. **Runtime.** Record the way workers run and the facts that matched it, the role and the parent it came from, the environment kind, the permission mode, whether a sandbox is on and how you read it, and the tools each acting agent holds. Write "unknown" for what the runtime does not report.
2. **Start a worker.** Start one probe worker with the reference's start method, briefed only to append a line with its token and the UTC time to a scratch file every 30 seconds, to answer a message beginning `Pause <token>` by stopping its loop and replying `paused <token>`, and one beginning `Resume <token>` by restarting it and replying `resumed <token>`. Pass: the start returned the worker's id, and the Harness's record lists that id within 5 minutes; where the record is a notification, a later notification names that id (this pass is then recorded after Step 5).
3. **Worker state.** Read the worker's state by the reference's method. Pass: a state from the reference's list, read under that id, showing it not ended (running or idle; idle is not ended). Where the record is a notification: no end notification for that id yet, corroborated by the scratch file growing. A probe worker may run in a container the runner cannot read (a project thread does): then its replies and its own state record are the evidence, and a missing file is not a failure.
4. **Pause and resume.** Pause the worker by the reference's method. Pass: its `paused <token>` reply reaches the coordinator through the Harness, and where the scratch file can be read (in a project it cannot: replies are the evidence), no line follows the reply by more than one interval. Then resume it. Pass: the `resumed <token>` reply arrives and the file grows again. Where the Harness has its own pause that only the user takes, record it as not probed.
5. **Confirmed stop.** Stop the worker by the reference's stop method for a worker that does not answer. Where that method runs through another worker (a **stop worker**), start one: it stops the probe worker, reads the stop back and reports both readings; the coordinator then reads the record again itself. Within 2 minutes of the stop read the state; if it still reads not ended, read once more a minute later. Pass: the reading before the stop showed not ended and the one after shows ended (stopped, killed, archived, or the Harness's word for it). Where the record is a notification: before, running with no notification; after, the stop's own notification for that id. A file that stops growing corroborates, never passes. Record any way the stop can be undone as a limit.
6. **End or failure notice.** Start a second probe worker briefed only to reply `done <token>` and end. Pass: the Harness wakes the coordinator with that reply, and the worker's state then reads ended. An ended state is whatever the reference counts as ended for this method (in a project, `done`, `failed` or `stopped`); a worker merely idle is not ended, and Step 5's stop still needs the reference's stopped state. Record that a failure was not provoked, unless the Harness documents a safe way to provoke one.
7. **Recurring check-in.** For Codex, apply the interval, deadline and missing-tool handling in the reference's **Codex check-in probe**; the one-arrival, cleanup and destination requirements still apply. Where the reference has no check-in method, the row reads "not relied on" with that as its limit, and the work must not rely on a scheduled wake. Where it has one, first list the scheduled tasks by the reference's method and end any an earlier run left (named with a `wc-checkin-` token). Then arrange a recurring check-in into the coordinator by it, named with and carrying this run's token, at the shortest interval the reference allows (in a project, one hour: the scheduler accepts no shorter, so this probe takes about an hour and a half). Pass: the token arrives in the coordinator's own record (in a project, its session events read with `list_events` or `get_event`) at least once, by one interval plus 30 minutes after it was arranged. A check-in that arrives in another agent fails. Then end it by the reference's method and read back that it no longer runs; a check-in that cannot be ended fails too.

## 5. The result

Report one table, kept as the result's shape:

```
## Worker control check

Harness: <way workers run> (<reference, or fallback with pages>) · Role: <coordinator | worker, and the parent it came from> · Runner: <agent(s)> · Run: <start>–<end> UTC
Runtime: <environment kind>; permission mode: <mode>; sandbox: <on | off | unknown> (<how read>); tools held: <per agent>

| Capability | Essential | Method and source | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Start a worker | yes | <method; doc page> | <pass or fail> | <id returned; record listing it> | <...> |
| Worker state | yes | <...> | <...> | <state read, with time> | <...> |
| Pause and resume | <yes or not relied on> | <...> | <...> | <replies and times> | <...> |
| Confirmed stop | yes | <...; the agent that stopped it> | <...> | <state before and after, with times> | <...> |
| End or failure notice | yes | <...> | <...> | <wake and state read> | <failure not provoked...> |
| Scheduled check-in | <yes or not relied on> | <...; the agent that arranged it> | <...> | <each arrival in the coordinator's record; the end read back> | <...> |

Verdict: ready | not ready: <each failed essential capability>
```

Name each failed essential capability to the user before unattended work starts, with what it means:

- **Start a worker**: the coordinator cannot start work, so nothing is delivered.
- **Worker state**: it cannot tell a working worker from a dead one, so it cannot trust a "done" or replace a worker safely.
- **Pause and resume**: a pause cannot hold running workers, so spending continues until they finish.
- **Confirmed stop**: it cannot tell a worker has stopped, so a replacement could write to the same branch at once.
- **End or failure notice**: it is not told when a worker ends or fails, so it must poll, and a dead worker can go unnoticed.
- **Scheduled check-in**: it cannot wake itself again and again, so between the user's messages a silent worker goes unnoticed.

Clean up: make sure every probe and stop worker has ended, and list the scheduled tasks to read back that every check-in this run arranged (named with its token) is ended.
