# Claude Code sessions

Workers run inside or beside one Claude Code session (desktop app, CLI or web), this reference's **Harness**: **subagents** started with the Agent tool, and, in the desktop app, **other sessions** started with the `ccd_session` tools. A subagent works within its parent session and cannot outlive it, so it suits work that ends within that session, not workers that wait hours for a wake. Docs read 2026-11-03. A line marked **runtime-reported** names a fact no doc page states; the check proves it here or records it as a limit.

## Detect

- **Desktop session:** tools from `ccd_session` (`start_session`) and `ccd_session_mgmt` (`list_sessions`, `get_session`, `send_message`, `stop_session`) are among your tools (runtime-reported). Remote Control state comes from `get_session` on yourself (`remoteControlState`), never from environment variables, which stay unset there (runtime-reported). Source: [work across sessions](https://code.claude.com/docs/en/desktop#work-across-sessions), [Remote Control](https://code.claude.com/docs/en/remote-control)
- **Plain session with subagents:** neither the project thread tools nor the `ccd_session` tools, and the Agent tool is among your tools. A subagent at the spawn-depth limit (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) has no Agent tool. Source: [tools reference](https://code.claude.com/docs/en/tools-reference), [nested subagents](https://code.claude.com/docs/en/sub-agents#let-subagents-spawn-their-own-subagents)
- **Role:** from an explicit parent only, never from being able to start workers (a worker can start workers too). A `SubagentHandback` tool means you are a subagent; a `parentSessionId` on `get_session` means you are a session started from another (both runtime-reported). Source: [subagents](https://code.claude.com/docs/en/sub-agents)
- **Second signal, only where a shell exists:** `CLAUDECODE` is `1`, and `CLAUDE_CODE_ENTRYPOINT` is `claude-desktop` in the desktop app (runtime-reported: not on the env-vars page). `CLAUDE_CODE_CHILD_SESSION=1` says nothing about role. Source: [environment variables](https://code.claude.com/docs/en/env-vars)
- **Not covered:** with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` set to `1`, a named Agent call launches a teammate instead; this reference does not cover teammates, so use the fallback with that page. Source: [agent teams](https://code.claude.com/docs/en/agent-teams#how-claude-starts-agent-teams)

## What the harness does by itself

- **Completion notification.** A background subagent's result reaches the coordinator as a completion notification in a later turn, marked as an automated event. Source: [results of background subagents](https://code.claude.com/docs/en/sub-agents#tools-permissions-and-results-of-background-subagents)
- **Failure notification.** A background subagent cut off by an API error is marked failed, and the message the coordinator receives names the error and carries its last output. Source: [API errors in subagents](https://code.claude.com/docs/en/sub-agents#api-errors-in-subagents)
- **Permission prompts.** A background subagent's permission prompt is surfaced in the main session, naming the subagent. Source: [foreground or background](https://code.claude.com/docs/en/sub-agents#run-subagents-in-foreground-or-background)
- **Background by default.** With nothing configured, a subagent started from the main conversation runs in the background. Source: [which subagents run in the background](https://code.claude.com/docs/en/sub-agents#which-subagents-run-in-the-background)
- **Limits.** At most 20 subagents running at once (the start fails beyond that); nesting up to the spawn-depth limit. Source: [concurrent subagent limit](https://code.claude.com/docs/en/sub-agents#concurrent-subagent-limit), [environment variables](https://code.claude.com/docs/en/env-vars)
- **Desktop: other sessions.** Claude can list the other Code tab sessions, read what each has been doing, message them, and rename or archive them; a message to a session mid-task waits until its current work finishes, and an archived session takes no message. The app sends the parent a note when a started session's turn ends (runtime-reported). Source: [work across sessions](https://code.claude.com/docs/en/desktop#work-across-sessions)
- **Environment expiry (cloud).** When a cloud session's machine is reclaimed, running subagents stop, and on reopening Claude Code says which stopped and which can be resumed. Source: [environment expired](https://code.claude.com/docs/en/claude-code-on-the-web#environment-expired)

## Methods the coordinator adds

### Start a worker

Subagent: the Agent tool with the brief, in the background; keep the agent ID or name it returns. Desktop session: `start_session` with the brief; keep the session id (`start_session` is runtime-reported, not on the page).
Source: [tools reference](https://code.claude.com/docs/en/tools-reference), [subagents](https://code.claude.com/docs/en/sub-agents), [work across sessions](https://code.claude.com/docs/en/desktop#work-across-sessions)

### Read a worker's state

Subagent: running until its completion notification arrives. There is no polling tool for it (the old output tool was removed; a background task's output file is read with Read), so the notification is the record. Desktop session: `get_session` or `list_sessions` on its id (runtime-reported, not on the doc page; unproven until the check passes).
Source: [results of background subagents](https://code.claude.com/docs/en/sub-agents#tools-permissions-and-results-of-background-subagents), [tools reference](https://code.claude.com/docs/en/tools-reference), [work across sessions](https://code.claude.com/docs/en/desktop#work-across-sessions)

### Notice a worker ended or failed

Subagent: its completion notification, or the failed notification with the error. Desktop session: the app's note that its turn ended, then its state read as above.
Source: [results of background subagents](https://code.claude.com/docs/en/sub-agents#tools-permissions-and-results-of-background-subagents), [API errors in subagents](https://code.claude.com/docs/en/sub-agents#api-errors-in-subagents)

### Stop a worker and read the stop back

Subagent: TaskStop with the agent ID or name; the stop's own notification (status killed, runtime-reported) is the read-back, since no other readable record of a stopped subagent exists. A stopped subagent can be resumed by a message once its stopped run has exited, so it stays stopped only while no one messages it. Desktop session: `stop_session`, then `get_session` reads it ended (runtime-reported).
Source: [tools reference](https://code.claude.com/docs/en/tools-reference), [resume subagents](https://code.claude.com/docs/en/sub-agents#resume-subagents)

### Pause and resume

No pause of its own. Pause: start no new worker, and ask each running one to stop at its next natural step, or stop it as above. Resume: SendMessage to the subagent's ID or name, which resumes it in the background with its history; for a desktop session, `send_message` (runtime-reported; unproven until the check passes). Pausing by a message is a convention the worker follows, not a Harness pause.
Source: [resume subagents](https://code.claude.com/docs/en/sub-agents#resume-subagents), [work across sessions](https://code.claude.com/docs/en/desktop#work-across-sessions)

### Arrange and end a check-in

A session-scoped recurring task in the coordinator's own session (`CronCreate`; end it with `CronDelete`). It fires only while the session is running and idle, a recurring task expires after 7 days, and missed runs are not caught up. Where the work must outlive the session, this reference has no check-in: record that as the row's limit.
Source: [scheduled tasks in a session](https://code.claude.com/docs/en/scheduled-tasks)
