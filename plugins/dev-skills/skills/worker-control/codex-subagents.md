# Codex subagents

## Detect

- The runtime exposes `collaboration.spawn_agent` and `collaboration.list_agents`. These exact names are runtime-reported, not a public stable API; use their current schemas and prove each relied-on operation with the check. The official docs describe spawning, steering, inspecting and stopping subagents without promising these tool names. Source: [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
- Role comes from the runtime's explicit task path: `/root` is this team's coordinator; `/root/<name>` and deeper descendants are workers with the enclosing path as parent. A worker may hold the same collaboration tools. If the runtime supplies no path or parent, record role unknown. This path convention is runtime-reported, not a public stable API. Source: [subagent orchestration](https://learn.chatgpt.com/docs/agent-configuration/subagents#orchestration-and-thread-controls).
- Record the host surface separately. Desktop tools and, where a shell exists, `CODEX_INTERNAL_ORIGINATOR_OVERRIDE=Codex Desktop` corroborate desktop identity when actually reported; neither is required to identify subagent methods. Record unknown when absent. Phone access requires a configured, awake, connected desktop host; subagent tools alone prove neither desktop identity nor remote pairing. Source: [remote connections](https://learn.chatgpt.com/docs/remote-connections).

## What the harness does by itself

- Codex orchestrates subagents and returns their results to the parent. In this runtime, worker messages and final results arrive in the parent conversation, and `collaboration.wait_agent` waits for updates; exact delivery behavior and names are runtime-reported and require the check. Source: [orchestration and thread controls](https://learn.chatgpt.com/docs/agent-configuration/subagents#orchestration-and-thread-controls).
- Local subagents inherit the parent's sandbox and permissions. Shared files can produce conflicts when several agents write; give each worker a distinct scope or checkout as the caller requires. Source: [subagent permissions](https://learn.chatgpt.com/docs/agent-configuration/subagents#approvals-and-sandbox-controls), [parallel work](https://learn.chatgpt.com/docs/agent-configuration/subagents#why-subagent-workflows-help).
- App-server publishes thread state and turn completion, including interrupted turns. Its protocol is a client integration, not evidence that this agent holds protocol tools. Read collaboration state in the runtime's own vocabulary rather than translating protocol thread states into agent states. Source: [app-server](https://learn.chatgpt.com/docs/app-server).
- In-chat scheduled tasks return to the same chat with its context; standalone tasks start new chats and cannot serve as this coordinator's check-in. Local project tasks need the computer on and app running. Remote access also stops when the host sleeps, loses its connection or closes the app. Source: [scheduled tasks](https://learn.chatgpt.com/docs/automations#schedule-a-task-inside-a-chat), [remote host availability](https://learn.chatgpt.com/docs/remote-connections#choose-what-to-connect).

## Methods the coordinator adds

### Start a worker

Use `collaboration.spawn_agent` with a task name and brief; retain the returned agent ID and canonical task path. Load the model-tiers skill for the requested tier. Follow the runtime schema for model overrides and context inheritance. This exact tool is runtime-reported and proved by the check, not a public stable API.
Source: [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#triggering-subagent-workflows).

### Read a worker's state

Use `collaboration.list_agents`, scoped to the task path where supported, and match the returned ID. Record the state exactly as returned. This runtime reports `running`, `interrupted` and `completed`; only a state the check has observed under the probe's ID may pass its corresponding row. `running` is not ended, `completed` is an ended turn, and `interrupted` confirms the stop of that run. Any unfamiliar state remains a limit until its meaning is established. The tool and state vocabulary are runtime-reported, not app-server protocol names.
Source: [manage subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#managing-subagents), [app-server state and turn lifecycle](https://learn.chatgpt.com/docs/app-server).

### Notice a worker ended or failed

Use the worker's final-result notification in the parent conversation, then read its state through the preceding method. `collaboration.wait_agent` can wait for an update; waiting itself is not completion evidence. Record a failure only from an explicit runtime notification or state. The exact notification envelope and tools are runtime-reported; the check proves normal completion and records a failure as unprovoked.
Source: [subagent orchestration](https://learn.chatgpt.com/docs/agent-configuration/subagents#orchestration-and-thread-controls), [app-server completion notifications](https://learn.chatgpt.com/docs/app-server).

### Stop a worker and read the stop back

Use `collaboration.interrupt_agent` on the ID or canonical path, then `collaboration.list_agents` to read `interrupted` for that same worker. The interrupt response reports its previous status; that response alone is not the stop read-back. These exact tools and the state are runtime-reported. Interruption stops a run, not the worker's future availability: a follow-up can restart it. Before replacement, finish the read-back and send no further task to the old worker. Record any independently running processes as a stop limit.
Source: [manage subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#managing-subagents), [app-server turn interruption](https://learn.chatgpt.com/docs/app-server).

### Pause and resume

Pause cooperatively with `collaboration.send_message` carrying `Pause <token>`; require the worker's acknowledgement and halted scratch loop. Stop an unresponsive worker by the preceding method. Resume a still-running cooperative loop with `collaboration.send_message`; resume an idle or interrupted worker with `collaboration.followup_task`, carrying `Resume <token>` and the remaining brief. A message to a running worker is steering, so acknowledgement is essential. This is a worker convention, not a native global pause; all exact tool names and restart behavior are runtime-reported and proved by the check.
Source: [steer and manage subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#managing-subagents), [orchestration](https://learn.chatgpt.com/docs/agent-configuration/subagents#orchestration-and-thread-controls).

### Arrange and end a check-in

Discover `mcp__codex_app__automation_update` by name or description and read its current schema. On desktop, its runtime description instructs inspection of `$CODEX_HOME/automations/*/automation.toml` to find existing tasks by name or prompt; read matching `wc-checkin-` probes and their IDs before creating another. Use `mode: "view"` with each resolved ID. End leftover probe tasks and read their status back.

Create a recurring `kind: "heartbeat"` with `destination: "thread"`, carrying the token and the caller's check-in work. This selects the current local chat; when acting elsewhere, use an explicit `targetThreadId` for the coordinator's existing chat as the schema supports. Read the persisted target thread ID and compare it with the coordinator's runtime thread ID. Preserve the returned automation ID. Standalone `kind: "cron"` jobs run in new chats and cannot pass this check.

For updates, supply the resolved ID and full fields from the existing record, preserving fields the caller did not change. End the check-in with an update setting `status: "PAUSED"`, then independently view that same ID and read its persisted status as `PAUSED`. When the view renders only a card, read the matching automation file as the runtime description directs. A completed probe may then be deleted with `mode: "delete"` and its ID; require the delete response and an independent absence read-back of its matching file. A rendered card alone proves neither persisted status nor absence. These tool names, fields and stored records are runtime-reported desktop behavior, not a public stable API: follow the discovered schema and record accepted calls. The public docs support the in-chat scheduling concept, not this exact tool contract.

A scheduler's success response, a standalone run or a shell timer is insufficient evidence of a same-chat scheduled wake. If no callable scheduler or supported UI method is available, record the row failed when delivery relies on it, naming the missing capability. An unavailable scheduler leaves subagent detection valid.
Source: [create or update scheduled tasks](https://learn.chatgpt.com/docs/automations#ask-chatgpt-to-create-or-update-scheduled-tasks), [tasks inside a chat](https://learn.chatgpt.com/docs/automations#schedule-a-task-inside-a-chat), [manage tasks](https://learn.chatgpt.com/docs/automations#managing-tasks).

## Codex check-in probe

For Step 4 probe 7, first request a recurring interval of 1 minute (or 2 minutes if that is the shortest offered by the current schema). Try a longer supported interval only after an explicit rejection, recording the rejected request, error and accepted interval. Minute-based in-chat schedules are documented; a minimum for this runtime is established by the scheduler, not guessed from another Harness.

Pass after **one scheduled arrival** carrying the token in the coordinator's own conversation, by the accepted interval plus 5 minutes, followed by ending the task and reading it back as disabled or absent. A manual run does not pass. Record the arrival timestamp and task ID, whether the coordinator was idle or busy, and any host availability limit. If no interval is accepted or no arrival is observed, fail with that evidence. The one-arrival requirement is shared across Harnesses; this probe supplies Codex-specific timing and missing-tool handling.

Source: [minute-based in-chat scheduled tasks](https://learn.chatgpt.com/docs/automations#schedule-a-task-inside-a-chat).
