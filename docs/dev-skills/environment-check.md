# Environment check

This repo's own test of the `worker-control` references: it proves, in each environment the plugin supports, that the methods a reference gives work, so a failed row is fixed in the reference before the plugin rolls out. It tests worker control only, never the skills end to end. When it runs, and where its result goes, is in `CLAUDE.md`.

## Environments

| Environment | Reference it proves | Run by |
|---|---|---|
| Cloud project (claude.ai project; workers are threads) | `claude-code-project-threads.md` | the project's coordinator |
| Local Claude Code session (workers are subagents, and on desktop other sessions) | `claude-code-sessions.md` | a session on the user's machine |

The local half is run through a session on the user's machine. Where that machine cannot be reached, the result says the local half did not run.

## Rules

**Probe.** Each row is one short, bounded action whose pass rests on the Harness's own record read afterwards, never on a call returning success, silence or a worker's own claim. A probe that cannot run here fails, with its limit: that is a valid result.

**Who acts.** Run each action in the agent that will take it during the work: the coordinator where it holds the tool, otherwise the agent the reference names (for example a worker the coordinator starts to hold a stop or scheduling tool it lacks). Split a probe whose tools are split, and record which agent took each action. An agent that lacks a probe's tool records the probe failed, with the missing tool as its limit. Probe the method the reference names; another mechanism that happens to work is a different capability.

**Scratch.** Each probe uses a fresh **token** (`wc-<probe>-` and 8 random hex characters). Probe workers run at the **cheap** tier, write only to a scratch directory outside the project, and end on their own after 15 minutes unless the probe needs them longer, so none outlives the run. Nothing else in the project changes.

**Records that are notifications.** Where the reference's state or read-back is a notification rather than a record that can be read on demand (for example a subagent's completion or stop notification), that notification is the record: "running" means started and no end notification yet, and "ended" means its end notification arrived. The passes below name both forms.

## Rows

**Runtime.** Before row 1, record the way workers run and the facts that matched it, the role and the parent it came from, the environment kind, the permission mode, whether a sandbox is on and how it was read, and the tools each acting agent holds. Write "unknown" for what the runtime does not report.

1. **Start a worker.** Start one probe worker with the reference's start method, briefed only to append a line with its token and the UTC time to a scratch file every 30 seconds, to answer a message beginning `Pause <token>` by stopping its loop and replying `paused <token>`, and one beginning `Resume <token>` by restarting it and replying `resumed <token>`. Pass: the start returned the worker's id, and the Harness's record lists that id within 5 minutes; where the record is a notification, a later notification names that id (recorded after row 4).
2. **Worker state.** Read the worker's state by the reference's method. Pass: a state from the reference's list, read under that id, showing it not ended (running or idle; idle is not ended). Where the record is a notification: no end notification for that id yet, corroborated by the scratch file growing. A probe worker may run in a container the runner cannot read (a project thread does): then its replies and its own state record are the evidence, and a missing file is not a failure.
3. **Pause and resume.** Pause the worker by the reference's method. Pass: its `paused <token>` reply reaches the coordinator through the Harness, and where the scratch file can be read (in a project it cannot: replies are the evidence), no line follows the reply by more than one interval. Then resume it. Pass: the `resumed <token>` reply arrives and the file grows again. Where the Harness has its own pause that only the user takes, record it as not probed.
4. **Confirmed stop.** Stop the worker by the reference's stop method for a worker that does not answer. Where that method runs through another worker (a **stop worker**), start one: it stops the probe worker, reads the stop back and reports both readings; the coordinator then reads the record again itself. Within 2 minutes of the stop read the state; if it still reads not ended, read once more a minute later. Pass: the reading before the stop showed not ended and the one after shows ended (stopped, killed, archived, or the Harness's word for it). Where the record is a notification: before, running with no notification; after, the stop's own notification for that id. A file that stops growing corroborates, never passes. Record any way the stop can be undone as a limit.
5. **End or failure notice.** Start a second probe worker briefed only to reply `done <token>` and end. Pass: the Harness wakes the coordinator with that reply, and the worker's state then reads ended. An ended state is whatever the reference counts as ended for this method (in a project, `done`, `failed` or `stopped`); a worker merely idle is not ended, and row 4's stop still needs the reference's stopped state. Record that a failure was not provoked, unless the Harness documents a safe way to provoke one.
6. **Recurring check-in.** Where the reference has no check-in method, the row reads "not relied on" with that as its limit. Where it has one, first list the scheduled tasks by the reference's method and end any an earlier run left (named with a `wc-checkin-` token). Then arrange a recurring check-in into the coordinator by it, named with and carrying this run's token, at the shortest interval the reference allows (in a project, one hour: the scheduler accepts no shorter, so this row takes about an hour and a half). Pass: the token arrives in the coordinator's own record (in a project, its session events read with `list_events` or `get_event`) at least once, by one interval plus 30 minutes after it was arranged. A check-in that arrives in another agent fails. Then end it by the reference's method and read back that it no longer runs; a check-in that cannot be ended fails too.

The runtime record is not a pass or fail. A reference change runs only the rows its change touches (see `CLAUDE.md`).

## Result

One table per environment, posted in the one comment headed "Environment check":

```
## Environment check

Environment: <cloud project | local Claude Code session> (<reference>) · Role: <coordinator | worker, and the parent it came from> · Runner: <agent(s)> · Run: <start>–<end> UTC
Runtime: <environment kind>; permission mode: <mode>; sandbox: <on | off | unknown> (<how read>); tools held: <per agent>

| Capability | Method and source | Result | Evidence | Limits |
|---|---|---|---|---|
| Start a worker | <method; doc page> | <pass or fail> | <id returned; record listing it> | <...> |
| Worker state | <...> | <...> | <state read, with time> | <...> |
| Pause and resume | <...> | <...> | <replies and times> | <...> |
| Confirmed stop | <...; the agent that stopped it> | <...> | <state before and after, with times> | <...> |
| End or failure notice | <...> | <...> | <wake and state read> | <failure not provoked...> |
| Scheduled check-in | <...; the agent that arranged it> | <...> | <each arrival in the coordinator's record; the end read back> | <...> |
```

A half that was not run says so in place of its table, with the reason. For each failed row, file a bug naming the reference line it disproves, and say what the failure means:

- **Start a worker**: the coordinator cannot start work, so nothing is delivered.
- **Worker state**: it cannot tell a working worker from a dead one, so it cannot trust a "done" or replace a worker safely.
- **Pause and resume**: a pause cannot hold running workers, so spending continues until they finish.
- **Confirmed stop**: it cannot tell a worker has stopped, so a replacement could write to the same branch at once.
- **End or failure notice**: it is not told when a worker ends or fails, so it must poll, and a dead worker can go unnoticed.
- **Scheduled check-in**: it cannot wake itself again and again, so between the user's messages a silent worker goes unnoticed.

## Clean up

Make sure every probe and stop worker has ended, and list the scheduled tasks to read back that every check-in this run arranged (named with its token) is ended.
