# Claude Code project threads

Workers run as **threads** of a claude.ai Claude Code project, this reference's **Harness**: the coordinator is the project conversation, and each thread is a separate cloud session (or a session on the user's machine through Remote Control) with its own branch. Docs read 2026-11-03. A line marked **runtime-reported** names a fact no doc page states but the runtime's own tools showed; the check proves it here or records it as a limit.

## Detect

Read the tool list first: the project coordinator has no shell, so it cannot read environment variables.

- **Coordinator:** `mcp__hearthbot__start_thread` is among your tools (runtime-reported). Source: [how a project is organized](https://code.claude.com/docs/en/claude-projects#how-a-project-is-organized)
- **A thread (a worker, never the coordinator):** `mcp__hearthbot__message_coordinator` is among your tools and `start_thread` is not; the session-details call (`get_session`, no id) names the coordinator's session as `parent_session_id` (runtime-reported). Source: [how a project is organized](https://code.claude.com/docs/en/claude-projects#how-a-project-is-organized)
- **Second signal, only where a shell exists (a thread):** `CLAUDE_CODE_ENTRYPOINT` is `remote_projects` (runtime-reported: not on the env-vars page) and `CLAUDECODE` is `1`. `CLAUDE_CODE_CHILD_SESSION=1` is set in every kind of session and says nothing about role. Source: [environment variables](https://code.claude.com/docs/en/env-vars)
- **Where a thread runs:** the session-details record reports `environment_kind` `anthropic_cloud` for a cloud thread and `ccs` for the coordinator (both runtime-reported). The tool names above decide; an `environment_kind` not seen before (for example a Remote Control thread's) is recorded, not a reason to fail Detect or to fall back. A thread on the user's machine runs through Remote Control: read that from the session-details record or the thread's Remote Control status, not from environment variables. Source: [run a thread on your own computer](https://code.claude.com/docs/en/claude-projects#run-a-thread-on-your-own-computer)

## What the harness does by itself

The coordinator relies on these and does not rebuild them in tracker records:

- **A thread reports back when it finishes.** Each thread does one piece of work and reports back to the conversation; the coordinator sees what threads report, not every step. Source: [how a project is organized](https://code.claude.com/docs/en/claude-projects#how-a-project-is-organized)
- **Wakes.** A thread's report wakes the coordinator. A failed turn, a stopped machine and a waiting permission prompt also reach it as wakes (runtime-reported: the doc page names desktop notifications to the user for an error or a thread needing input, not coordinator wakes). Source: [see what needs you](https://code.claude.com/docs/en/claude-projects#see-what-needs-you-in-overview)
- **Thread states.** The Overview groups threads as ready for review, waiting on you (needs a reply or approval, or failed), working, landing, idle and resolved. The thread-listing tool reports each thread as `working`, `blocked` (waiting on the user), `review_ready`, `done`, `failed` or `stopped` (its machine stopped) (runtime-reported). Source: [see what needs you](https://code.claude.com/docs/en/claude-projects#see-what-needs-you-in-overview)
- **Silence is not a stall.** A thread shown as running with no new messages is usually still working; a new cloud thread provisions its environment first. Source: [a thread looks stuck](https://code.claude.com/docs/en/claude-projects#a-thread-looks-stuck)
- **Pull request watching.** A thread that opened a pull request watches it: an idle thread wakes on a CI failure or a review comment. A base-branch conflict sends no event. Source: [review a thread's pull request](https://code.claude.com/docs/en/claude-projects#review-a-threads-pull-request), [auto-fix](https://code.claude.com/docs/en/claude-code-on-the-web#auto-fix-pull-requests)
- **Project Pause.** Pause interrupts every running thread and the conversation, starts no new thread, runs no scheduled task and accepts no message until Resume; a paused thread continues when it is sent a message after that. The user takes it from the project's settings. Source: [pause, archive, or delete a project](https://code.claude.com/docs/en/claude-projects#pause-archive-or-delete-a-project)
- **Sandbox between turns.** A cloud thread's sandbox pauses between turns; if it cannot resume, the thread continues from a fresh clone and uncommitted changes are lost, so workers push work in progress. Source: [limitations](https://code.claude.com/docs/en/claude-projects#limitations)
- **Usage limits.** A thread at the plan's limit retries on its own and continues when it resets; one a scheduled task started stops with a limit error instead. Source: [a thread hit the usage limit](https://code.claude.com/docs/en/claude-projects#a-thread-hit-the-usage-limit)

The coordinator itself holds no tool to set a timer or to stop a thread (no `send_later`, `create_trigger`, `archive_session` or `interrupt_session`; runtime-reported). Its threads hold them, so the check-in and the stop below go through threads.

## Methods the coordinator adds

### Start a worker

`mcp__hearthbot__start_thread`, briefed with the task; record the thread's id and its session's id from the answer (the tool is runtime-reported: the doc page says the coordinator starts threads, not with which tool; unproven until the check passes). The new thread starts from the repository's default branch unless the brief names another.
Source: [send work and read results](https://code.claude.com/docs/en/claude-projects#send-work-and-read-results), [review a thread's pull request](https://code.claude.com/docs/en/claude-projects#review-a-threads-pull-request)

### Read a worker's state

`list_threads`, reading **every page** until it returns no next cursor: a state filter applies page by page, so one page can miss a thread. For a finer reading, `get_session` on the thread's session gives its session status (running, idle, archived) and status bucket (runtime-reported; unproven from the coordinator until the check passes). Running and idle are not ended. Tracker comments and the thread's last message are never the state.
Source: [see what needs you](https://code.claude.com/docs/en/claude-projects#see-what-needs-you-in-overview), [work with sessions](https://code.claude.com/docs/en/claude-code-on-the-web#work-with-sessions)

### Notice a worker ended or failed

Act on the wake: a thread's report, or a wake for its failed turn or stopped machine. At each wake read the state as above, never inferred from a pull request or a comment. For this method `done`, `failed` and `stopped` from `list_threads` count as ended, and `review_ready` as finished for now; `idle` from `get_session` is still not ended, and a confirmed stop still needs `archived`.
Source: [how a project is organized](https://code.claude.com/docs/en/claude-projects#how-a-project-is-organized), [see what needs you](https://code.claude.com/docs/en/claude-projects#see-what-needs-you-in-overview)

### Stop a worker and read the stop back

1. Ask the thread (`message_thread`) to push its work and stop itself; read its state back.
2. If it does not answer, start a short **stop thread** briefed with the hung thread's session: it archives that session (`archive_session`), reads it back with `get_session` (archived is ended), reports both readings and ends. One thread archiving another's session is runtime-reported and unproven until the check passes. The coordinator then reads the record again itself.

The user's **Stop** only interrupts the current turn and leaves the thread resumable; `interrupt_session` is the same. An archived session accepts no message. An archive can be undone by unarchiving, so it is a stop only while no one undoes it.
Source: [archive sessions](https://code.claude.com/docs/en/claude-code-on-the-web#archive-sessions), [errors when sending to a cloud session](https://code.claude.com/docs/en/claude-code-on-the-web#errors-when-sending-to-a-cloud-session), [open a thread when you need control](https://code.claude.com/docs/en/claude-projects#open-a-thread-when-you-need-control)

### Pause and resume

The Harness's own pause is the project Pause, which only the user takes. The coordinator's pause: start no new thread, and message each running thread (`message_thread`) to push its work and stop at its next natural step. Resume: message each paused thread to carry on, and read the tracker and branches for the next work.
Source: [pause, archive, or delete a project](https://code.claude.com/docs/en/claude-projects#pause-archive-or-delete-a-project), [open a thread when you need control](https://code.claude.com/docs/en/claude-projects#open-a-thread-when-you-need-control)

### Arrange and end a check-in

Arrange: start a short thread briefed to create one recurring scheduled task (`create_trigger` with a cron expression, aimed at the coordinator's session by `persistent_session_id`, named with the run's token) at the interval the caller gives, report its id and end. These tools are runtime-reported; a recurring task arriving more than once in the coordinator is unproven until the check passes. Before arranging, list the tasks (`list_triggers`) and end any left by an earlier run. The task outlives that thread, and its target followed the coordinator when the coordinator's session was recycled (runtime-reported). A recurring schedule runs at most hourly, and a run waits until its target session is idle. Read each arrival from the coordinator's own session events (`list_events` or `get_event` on its session, runtime-reported), never from the scheduler's success record alone.
End: start a short thread briefed to delete that task (`delete_trigger`, runtime-reported) and read back with `list_triggers` that it no longer runs. When to arrange and end it is the caller's decision.
Source: [scheduled tasks](https://code.claude.com/docs/en/routines#add-a-schedule-trigger), [edit and control scheduled tasks](https://code.claude.com/docs/en/routines#edit-and-control-scheduled-tasks), [how projects relate to other features](https://code.claude.com/docs/en/claude-projects#how-projects-relate-to-other-claude-code-features)
