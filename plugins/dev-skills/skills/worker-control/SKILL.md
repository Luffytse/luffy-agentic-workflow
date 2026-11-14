---
name: worker-control
description: "Start, check, stop, pause and resume workers in the tool you run in. Use when a coordinator starts, reads, stops, pauses or schedules workers."
user-invocable: false
---

# Worker control

A coordinator runs its workers through the tool it runs in (its **Harness**): the runtime that starts sessions, wakes the coordinator and keeps their state. This skill holds how; deciding what work starts, when and why stays with the caller. The Harness's own record is the only source of a worker's state, its end and its failure; tracker comments are an audit trail, never that source. Every method comes from the Harness's docs, cited, or is marked runtime-reported; never from a tool's name alone, a dry run or memory.

## 1. Detect how workers run here

Read what the runtime itself reports: first the names of the tools you hold (a coordinator may have no shell), then the session-details record where you can read it, then a shell's environment where one exists, as a second signal only. Never decide from memory, the project's instructions or the tracker.

| Tools you hold (first match wins) | Way workers run | Reference |
|---|---|---|
| `mcp__hearthbot__start_thread` | claude.ai project: you are its coordinator; workers are threads | [claude-code-project-threads.md](claude-code-project-threads.md) |
| `mcp__hearthbot__message_coordinator`, without `start_thread` | claude.ai project: you are a thread, a worker | [claude-code-project-threads.md](claude-code-project-threads.md) |
| `ccd_session` / `ccd_session_mgmt` tools | Claude Code desktop: subagents and other sessions | [claude-code-sessions.md](claude-code-sessions.md) |
| the Agent tool, none of the above | Claude Code session (CLI, web, desktop): subagents | [claude-code-sessions.md](claude-code-sessions.md) |

Then confirm against the reference's **Detect** section and record each fact you matched, with where you read it. The tool names decide: a fact the reference has not seen before (an unfamiliar environment kind, say) is recorded, not a reason to fall back. Only tools that match no row, or tools that contradict the reference's Detect section, make the Harness unknown: use the fallback.

**Role** comes from explicit runtime lineage only: a parent session in the session-details record, a hand-back tool that returns to a caller, or a tool for messaging your coordinator. Being able to start workers never makes you the coordinator; workers can start workers too. A worker never takes the coordinator's role.

## 2. Load the reference

Read the whole reference. **What the harness does by itself** is what the coordinator relies on and never rebuilds in records of its own. **Methods the coordinator adds** are the only lifecycle actions it takes: start a worker, read its state, notice it ended or failed, stop it and read the stop back, pause and resume, arrange and end a check-in. A line marked runtime-reported is not on a doc page: it was seen in use, so treat it as less certain than a cited method.

## 3. Fallback: a Harness with no reference

Say this tool has no reference for its workers, tell the user, and stop: take no worker action from memory, another tool's reference or a guess.
