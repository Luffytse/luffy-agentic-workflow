# Results

One entry per run of the `worker-control` skill's check or its unknown-harness case (entries before 2026-11-03 04:00 UTC ran on its working name `harness-team`, with the references `claude-code-project.md` and `claude-code-subagents.md`, since replaced by `claude-code-project-threads.md` and `claude-code-sessions.md`), newest first, in the shape of `evals/startup-verification/RESULTS.md`. [README.md](README.md) says how to run each case and what passes.

## Template

```
### <date>, commit <sha>, dev-skills <version>: <harness>, <check run | unknown-harness case>

Runner: <who took each action, and why that agent>
Runtime: <environment kind; permission mode; sandbox; tools held; how each was read>
Docs used: <the reference's pages this run relied on>
Probes: <per probe: action, times, evidence, result, limits>
Result: <the result table, or its rows>
Not exercised: <what this run did not reach>
Pass: yes | no. Lessons: <what to change in the skill, if anything>
```

## Runs

### 2026-11-03, commit 583b965 (branch `t527-harness-team`; base 36a2530), dev-skills 0.48.0 (base): claude.ai project, detection by tool names and the check still owed

Runner: the #527 Implementer, a subagent of the Spec thread (session `session_REMOVED`), applying Step 1 of the renamed skill by hand at 04:02 UTC. It ran no probe.
Detection, by the table's order:
- `mcp__hearthbot__start_thread`: absent from this agent's tools.
- `mcp__hearthbot__message_coordinator`: present, `start_thread` absent: a claude.ai project thread, a worker. Reference: `claude-code-project-threads.md`.
- Role from an explicit parent: `SubagentHandback` is among this agent's tools (a subagent, reporting to the Spec thread), and the Spec thread's session-details record names the project coordinator `session_REMOVED` as `parent_session_id` (read 00:43Z). So this agent is a worker twice over and never the coordinator, though it could start no worker anyway (no Agent tool, spawn depth 1).
- Second signal (a shell exists here): `CLAUDE_CODE_ENTRYPOINT=remote_projects`, `CLAUDECODE=1`; `CLAUDE_CODE_CHILD_SESSION=1`, read as no role signal.
- Agreeing facts from the probe reports for #534: the coordinator's tools include `start_thread` and none of `send_later`, `create_trigger`, `archive_session`, `interrupt_session`; a thread holds them.
Docs used: [projects](https://code.claude.com/docs/en/claude-projects), [scheduled tasks](https://code.claude.com/docs/en/routines), [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web), [environment variables](https://code.claude.com/docs/en/env-vars), read 2026-11-03.
Result: detection only.

```
| Start a worker | yes | start_thread; claude-projects#send-work-and-read-results | not run | - | owed: coordinator run |
| Worker state | yes | list_threads, every page; get_session | not run | - | owed |
| Pause and resume | yes | message_thread | not run | - | owed |
| Confirmed stop | yes | stop thread archives the probe thread, reads it back; claude-code-on-the-web#archive-sessions | not run | - | owed: one thread stopping another has never been shown |
| End or failure notice | yes | the thread's report wakes the coordinator | not run | - | owed |
| Scheduled check-in | yes | a thread creates one recurring task aimed at the coordinator's session; routines#add-a-schedule-trigger | not run | - | owed: two arrivals in the coordinator have never been shown; at least an hourly interval, so the probe takes over two hours |

Verdict: not ready: every capability, since the check has not run
```

Not exercised: every probe. **Still owed:** the coordinator's run of the check with the threads it starts, including the recurring check-in arriving at least twice and a stop thread stopping another thread and reading it back. A subagent of a worker cannot run it: it is not the coordinator and starts no thread.
Pass: yes as a by-hand detection trace; no as the check.

### 2026-11-03, commit f410be8 (branch `t527-harness-team`; base 25708c4), dev-skills 0.48.0 (base): unknown harness, unknown-harness case

Runner: the #527 Implementer, a subagent of the Spec thread, applying the skill text by hand to [unknown-harness/FACTS.md](unknown-harness/FACTS.md). Not an independent agent: this runner holds no Agent tool (see the run below), so no fresh agent could be started for it. A rerun by an agent given only the skill text and FACTS.md is still owed.
Trace, by the skill's steps:
- Step 1: facts read from FACTS.md: no `CLAUDECODE`, no session-details call, no Agent tool, no thread tools. Neither Detect section matches (both need `CLAUDECODE`). Harness unknown; named from its own report: Example Runner 3.2 (`EXAMPLE_RUNNER_VERSION`).
- Step 2: no reference loaded.
- Step 3: the help names [unknown-harness/DOCS.md](unknown-harness/DOCS.md). Methods with that page: start a worker (`spawn_worker`, returns `worker_id`); read its state (`worker_status`: queued, running, finished, errored, kept 24 hours). Not available: end or failure notice ("does not notify the coordinator"; an end is seen only by polling `worker_status`); stop (the page gives none; `message_worker` only delivers a message); pause and resume (none); scheduled check-in (none). Nothing was taken from the Claude Code references.
- User line, as written: "No harness reference for Example Runner 3.2: I read its workers page (unknown-harness/DOCS.md); it gives start and status only, so end or failure notice (polling only), stop, pause and resume, and scheduled check-in are not available here."
- Step 4, planned: Start a worker and Worker state run with `spawn_worker` and `worker_status`; Pause and resume, Confirmed stop, End or failure notice and Scheduled check-in fail without running.

Result (planned rows; the fixture's tools are not real, so no probe ran):

```
| Start a worker | yes | spawn_worker; unknown-harness/DOCS.md | not run (fixture) | - | fixture tools only |
| Worker state | yes | worker_status; unknown-harness/DOCS.md | not run (fixture) | - | fixture tools only |
| Pause and resume | yes | none | fail | - | not available: the docs give no pause |
| Confirmed stop | yes | none | fail | - | not available: the docs give no stop |
| End or failure notice | yes | none | fail | - | not available: no notification, polling only |
| Scheduled check-in | yes | none | fail | - | not available: the docs give no scheduler |

Verdict: not ready: Pause and resume, Confirmed stop, End or failure notice, Scheduled check-in
```

Each named with its meaning as the skill's Step 5 lists them (for Confirmed stop: a replacement could write to the same branch at once).
Not exercised: an independent agent under test; the probes themselves.
Pass: yes, as a by-hand trace against README's case 2. Lessons: the Detect sections decide on `CLAUDECODE` first, so a non-Claude-Code harness can never half-match a Claude Code reference.

### 2026-11-03, commit f410be8 (branch `t527-harness-team`; base 25708c4), dev-skills 0.48.0 (base): Claude Code project, check run (partial, by a worker's subagent)

Runner: the #527 Implementer, a subagent of the Spec thread "Build the milestone skill redesign" (session `session_REMOVED`, `cse_REMOVED`), running Steps 1 to 5 by hand from the skill text. It is **not** the agent that will coordinate: the project coordinator is session `session_REMOVED`. So each probe whose tool this runner lacks is recorded failed with that limit, as the skill's "Who acts" says; this run proves detection only; its state reading of an existing thread corroborates the method without passing it. Run: 2026-11-03 00:35–00:44 UTC.
Runtime: read at 00:35:49Z and again at 00:43Z.
- Session-details call on this session: `environment_kind` `anthropic_cloud`, `SESSION_STATUS_RUNNING`, bucket WORKING, permission mode `auto`, `parent_session_id` `session_REMOVED`, tags include `hearth-thread` and `config:hearth-projects-session`, lineage depth 1. (`anthropic_cloud` is the thread kind the project reference accepts.)
- On the coordinator's session: `environment_kind` `ccs`, `SESSION_STATUS_IDLE`, bucket REVIEW_READY, tag `hearth-overview`, `connection_status` `disconnected`, its reported tool list empty. `ccs` is the coordinator kind the project reference accepts. The coordinator's `CLAUDE_CODE_REMOTE_SESSION_ID` is unread: this runner has no shell in the coordinator's session.
- Shell environment: `CLAUDECODE=1`, `CLAUDE_CODE_REMOTE_SESSION_ID` set (`cse_REMOVED`, this thread's), `CLAUDE_CODE_BRIDGE_SESSION_ID` unset (no Remote Control), `IS_SANDBOX=1` (sandbox on), `CLAUDE_CODE_PROJECTS_SESSION=1` and `CLAUDE_CODE_ENTRYPOINT=remote_projects` (not on the doc page: corroboration only), `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` unset. `CLAUDE_CODE_COORDINATOR_EXTRA_TOOLS` names one-shot and recurring scheduling and the session-event list among the coordinator's extra tools; not confirmed from the coordinator's own record, which listed none.
- Tools this runner holds: the thread-listing and thread-reading tools, the session-details, session-list, session-events, archive and interrupt calls, one-shot scheduling into its own session. Not held: thread start, the Agent tool (depth limit 1), a scheduler into the coordinator's session.
Docs used: [projects](https://code.claude.com/docs/en/claude-projects), [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web), [environment variables](https://code.claude.com/docs/en/env-vars), [scheduled tasks](https://code.claude.com/docs/en/routines), [subagents](https://code.claude.com/docs/en/sub-agents), [tools reference](https://code.claude.com/docs/en/tools-reference), [agent teams](https://code.claude.com/docs/en/agent-teams), all read 2026-11-03.
Probes:
- Detect: Claude Code project matched. This runner is a subagent of a thread, so it matched the first two Detect lines (`CLAUDECODE=1`; `CLAUDE_CODE_REMOTE_SESSION_ID` set and `environment_kind` `anthropic_cloud`) and the third line's alternative only (a thread whose session-details record names the project coordinator as parent), not the thread tools a coordinator holds. The coordinator's own record reads `environment_kind` `ccs`; its `CLAUDE_CODE_REMOTE_SESSION_ID` is unread (no shell there). Claude Code sessions (then the subagents reference) does not match for this runner: no Agent tool. Pass for detection by this runner only.
- Worker state: thread-listing tool, all pages. First page (limit 20, no filter, 00:37Z): 20 threads, all `done`. With `state: working` (00:43:07Z), the first page returned **no threads** and a next cursor; the second page returned this Spec thread as `working` (last activity 00:42:29Z). Unfiltered pages since 2026-11-02T18:00Z (00:38Z): states `done` (several), `blocked` (two threads, `need_input`), `working` (this one). No `failed`, `stopped` or `review_ready` thread existed to read. Session-details on this thread's session at 00:43Z: RUNNING, bucket WORKING, agreeing with `working`. Fail: no probe worker was started (Start a worker failed), so no probe worker's state was read; this reading of an existing thread only corroborates the method. Limits: the worker read was not one this runner started; a state filter answers page by page, so a one-page read misses threads (the reference now says to read every page).
- Confirmed stop (read-back half only): session-details on the 2026-11-02 stop worker `session_REMOVED` (archived in that day's Startup verification) reads `SESSION_STATUS_ARCHIVED`, bucket COMPLETED, `updated_at` 2026-11-02T10:24:36Z, a day later. Corroborates that an archive reads back as ended and stays so while no one unarchives. No stop was taken: fail, limit "no probe worker started (runner holds no thread-start tool)".
- Start a worker: fail. Limit: this runner holds no thread-start tool and no Agent tool; the coordinator holds thread start.
- Pause and resume: fail. Limit: no probe worker to message; the project Pause is the user's.
- End or failure notice: fail. Limit: a subagent receives no thread wakes; only the coordinator can show that a thread's report wakes it.
- Scheduled check-in: fail. Limit: this runner can schedule only into its own session, which wakes the Spec thread, not the coordinator (a different mechanism).

Result:

```
## Harness check

Harness: Claude Code project (claude-code-project.md) · Runner: #527 Implementer (subagent of thread session_REMOVED) · Run: 2026-11-03 00:35–00:44 UTC
Runtime: anthropic_cloud; permission mode: auto; sandbox: on (IS_SANDBOX=1); tools held: thread list/read, session details/list/events, archive, interrupt, one-shot into own session; no thread start, no Agent tool

| Capability | Essential | Method and source | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Start a worker | yes | thread start; claude-projects#send-work-and-read-results | fail | - | runner holds no thread-start tool |
| Worker state | yes | thread list, every page, plus session details; claude-projects#see-what-needs-you-in-overview | fail | no probe worker; corroboration only: Spec thread `working` on page 2 at 00:43:07Z, session RUNNING/WORKING | Start a worker failed; filter answers page by page |
| Pause and resume | yes | message the thread; claude-projects#pause-archive-or-delete-a-project | fail | - | no probe worker |
| Confirmed stop | yes | archive, read back with session details; claude-code-on-the-web#archive-sessions | fail | earlier archived probe still reads ARCHIVED/COMPLETED | no stop taken; read-back only |
| End or failure notice | yes | thread report wakes the coordinator; claude-projects#how-a-project-is-organized | fail | - | a subagent receives no thread wakes |
| Scheduled check-in | yes | scheduled task into the coordinator's session; routines#schedule-a-one-off-run | fail | - | runner can schedule only into its own session |

Verdict: not ready: Start a worker, Worker state, Pause and resume, Confirmed stop, End or failure notice, Scheduled check-in
```

Not exercised: a failed or stopped thread state; Claude Code sessions (then the subagents reference) (this runner has no Agent tool). **Still owed:** a run of the check by the coordinator, or by a thread it starts for the check; this partial run does not stand in for it.
Pass: yes as a by-hand eval (every row rests on its evidence; every failure named with its limit), no as the check. Lessons: the run must be taken by the coordinator or a thread it starts, never by a worker's subagent; a thread listing filtered by state must be read to its last page.
