# Results

One entry per run of the `worker-control` skill's check or its unknown-harness case (entries before 2026-11-03 04:00 UTC ran on its working name `harness-team`, with the references `claude-code-project.md` and `claude-code-subagents.md`, since replaced by `claude-code-project-threads.md` and `claude-code-sessions.md`), newest first, in the shape of `evals/startup-verification/RESULTS.md`. [README.md](README.md) says how to run each case and what passes.

## Template

Every new entry records its run level (see [Run level](README.md#run-level)); earlier entries have no such line and are not rewritten.

```
### <date>, commit <sha>, dev-skills <version>: <harness>, <check run | unknown-harness case>

Run level: decision-level in a subagent | full build-flow in a top-level session
Runner: <who took each action, and why that agent>
Runtime: <environment kind; permission mode; sandbox; tools held; how each was read>
Docs used: <the reference's pages this run relied on>
Probes: <per probe: action, times, evidence, result, limits>
Result: <the result table, or its rows>
Not exercised: <what this run did not reach>
Pass: yes | no. Lessons: <what to change in the skill, if anything>
```

## Runs


### 2026-11-03 07:37–07:42:48 UTC, base f14e51f, dev-skills 0.48.0: Codex desktop subagents, check run (Case 1)

Skill text: desktop rework recorded in this commit on `codex/worker-control-528-desktop`, based on `f14e51f`; version unchanged. Runner: the desktop coordinator `/root` took the lifecycle and scheduling actions; Implementer `/root/implement_528_desktop` wrote this record from the parent's live results. The earlier failed Codex run below remains valid for its different runtime.

## Worker control check

Harness: Codex desktop subagents (`codex-subagents.md`) · Role: coordinator (explicit `/root`) · Runner: `/root` · Run: 2026-11-03 07:37–07:42:48 UTC

Runtime: explicit root task path `/root`; probe A reported its descendant path and the same six collaboration tools. Desktop identity: `CODEX_INTERNAL_ORIGINATOR_OVERRIDE=Codex Desktop`, version `0.166.0-alpha.5.1`, sandbox `seatbelt`; runtime permission profile workspace-write with automatic escalation review. The tool inventory exposes `mcp__codex_app__automation_update`; its discovered schema and description supplied exact fields and the instruction to inspect `$CODEX_HOME/automations/*/automation.toml`. These are observed runtime contracts, not public stable API promises. Phone pairing was not inspected.

Docs used: [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [app-server](https://learn.chatgpt.com/docs/app-server), [automations](https://learn.chatgpt.com/docs/automations), [remote connections](https://learn.chatgpt.com/docs/remote-connections), fetched by the coordinator for this rework. They support the capabilities; exact tool names, task paths, fields and statuses below come from the live runtime.

| Capability | Essential | Method and source | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Start a worker | yes | `collaboration.spawn_agent`; subagents page above | pass | A `/root/wc_probe_desktop`, token `wc-start-528-8b4d7e20`, spawned by 07:38:17; parent read running | Runtime-reported path and tools |
| Worker state | yes | `collaboration.list_agents`; subagents and app-server pages above | pass | Parent read A running after start and at 07:39:32; scratch file `/tmp/wc-desktop-528-8b4d7e20/heartbeat.txt` corroborated activity | File is corroboration, not worker state |
| Pause and resume | yes | `send_message`, `followup_task`; subagents page above | pass | Pause sent about 07:38:31 and acknowledged; file reads 07:38:38 and 07:39:05 unchanged. Resume sent 07:39:05, acknowledged and appended 07:39:10. After interruption, follow-up Resume about 07:39:42 retained token/path and appended 07:39:45 | Cooperative pause, no native global pause |
| Confirmed stop | yes | `interrupt_agent`, independent `list_agents`; subagents and app-server pages above | pass | Interrupt after running read 07:39:32 returned previous_status running; independent list about 07:39:38 read interrupted for A | That run stopped; follow-up restarted it. No independent background processes |
| End or failure notice | yes | Automatic final-result notification and `list_agents`; subagents and app-server pages above | pass | A final `done wc-start-528-8b4d7e20 retained context` received; B `/root/wc_end_desktop` spawned about 07:39:59, automatic final `done wc-end-528-927c618f` received by 07:40:02. Parent list about 07:40:45 read both completed with their exact final strings | Failure not provoked |
| Scheduled check-in | yes | Desktop heartbeat; automations page above and discovered runtime schema | pass | At 07:37:35 create without destination rejected: `targetThreadId: Missing targetThreadId or destination=thread.` Retry `kind: "heartbeat"`, `mode: "create"`, `destination: "thread"`, `rrule: "FREQ=MINUTELY;INTERVAL=1"`, `status: "ACTIVE"` accepted; ID `wc-checkin-528-d7a290e4`, persisted creation 07:37:52.907 UTC. Persisted target_thread_id equals coordinator CODEX_THREAD_ID `01a1a055-44bd-7751-82be-51322411b1f5`. Scheduled heartbeat envelope with this automation ID arrived in the same chat at 07:42:09.383 UTC, retaining context; independent `mcp__codex_app__read_thread` returned that same thread ID and turn `01a1a05b-bdec-7b41-83c0-3891ad60074c` (startedAt `1793691729`) with the heartbeat ID/token and timestamp. Arrival was 4m16.476s after creation and before deadline 07:43:52.907. | No interval rejection; arrival observed after coordinator yielded idle about 07:41:14; no arrival observed while active, without establishing busy-turn semantics |

Cleanup: update accepted with `mode: "update"`, the original ID, `kind: "heartbeat"`, original name/prompt/rrule, the same `targetThreadId`, `destination: "thread"` and `status: "PAUSED"`; persisted update 07:42:31.808 UTC. Independent `mode: "view"` rendered a card; matching automation file read at 07:42:39 confirmed `PAUSED` and unchanged target. Then `mode: "delete"` with that ID returned `deleteStatus: deleted`; independent file-existence read at 07:42:47.846 returned false. A subsequent view still rendered a card, so absence rests on the delete response and file read, not the card. Lifecycle probes read completed; no independent background processes remained.

Verdict: **ready**. All six essential capabilities passed in this desktop runtime, including one scheduled same-chat arrival and termination read-back. Pass as an evidence eval: yes. Not exercised: failure notification or phone pairing/reachability. This result supplies the desktop scheduling proof missing from the earlier runtime; it does not change that earlier run's honest failure.

### 2026-11-03 07:24:24–07:26:12 UTC, base f5593f0, dev-skills 0.48.0: Codex subagents, check run (Case 1)

Skill text: uncommitted #528 changes on `claude/project-thread-r67ntb`, based on `f5593f0db65ef5ee1e7c2973ee77d8fe01f64de9`; version unchanged on the user's instruction. Runner: the parent coordinator `/root` took every lifecycle action; its Implementer `/root/implement_528` wrote this record from the parent's live tool results. No tracker comment supplied a worker state.

Docs used (fetched 2026-11-03): [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [app-server](https://learn.chatgpt.com/docs/app-server), [scheduled tasks](https://learn.chatgpt.com/docs/automations), [remote connections](https://learn.chatgpt.com/docs/remote-connections). The pages document the capabilities; exact collaboration tool names, task paths and statuses below are runtime-reported, not a public stable API.

## Worker control check

Harness: Codex subagents (`codex-subagents.md`) · Role: coordinator (runtime's explicit `/root`; Implementer is descendant `/root/implement_528`) · Runner: `/root` · Run: approximately 2026-11-03 07:24:24–07:26:12 UTC
Runtime: local macOS shell, desktop surface unknown; permission mode: workspace-write with auto_review (runtime instructions); sandbox: on (`CODEX_SANDBOX=seatbelt`); `CODEX_VERSION=0.166.0`, `CODEX_INTERNAL_ORIGINATOR_OVERRIDE` unset. Coordinator and Implementer hold `collaboration.spawn_agent`, `list_agents`, `send_message`, `followup_task`, `interrupt_agent`, `wait_agent`; repeated runtime tool inventory exposes no `mcp__codex_app__*` tools or callable scheduler. Network enabled per runtime instructions. Phone pairing not inspected.

| Capability | Essential | Method and source | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Start a worker | yes | `collaboration.spawn_agent`; [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | pass | Cheap probe A returned `/root/wc_probe_a`, token `wc-start-c82f04a9`; `list_agents` at 07:24:33 read that path running | Start time approximately 07:24:24; exact names runtime-reported |
| Worker state | yes | `collaboration.list_agents`; [manage subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#managing-subagents) | pass | Probe A running at 07:24:33 and 07:25:42; scratch `/tmp/wc-probe-c82f04a9/heartbeat.txt` grew at 07:24:37 and 07:24:41 | State comes from tool read, file only corroborates |
| Pause and resume | yes | `collaboration.send_message`, `followup_task`; [steering](https://learn.chatgpt.com/docs/agent-configuration/subagents#managing-subagents) | pass | Pause sent about 07:24:42; parent received `paused wc-start-c82f04a9` by 07:24:49. File reads 07:24:49 and 07:25:23 unchanged since 07:24:41. Cooperative resume sent 07:25:24; acknowledgement by 07:25:40, file grew 07:25:37. After interruption, `followup_task` about 07:25:51 resumed retained context; acknowledgement and file append at 07:25:55 | Cooperative pause, no native global pause. Initial loop used shorter intervals than the shared 30-second brief; halted over a full 30-second interval |
| Confirmed stop | yes | Coordinator `collaboration.interrupt_agent`, independent `list_agents` read-back; [stop subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#managing-subagents), [turn interruption](https://learn.chatgpt.com/docs/app-server) | pass | Before: running at 07:25:42. Interrupt about 07:25:45 returned previous_status running; next independent `list_agents` read interrupted under `/root/wc_probe_a` | Stops that run; follow-up restarted it in the same context. No independent background process was left |
| End or failure notice | yes | Parent final-result notification and `list_agents`; [orchestration](https://learn.chatgpt.com/docs/agent-configuration/subagents#orchestration-and-thread-controls) | pass | Probe A final `done wc-start-c82f04a9 retained context`, completed about 07:26:02. Cheap probe B `/root/wc_probe_b`, token `wc-end-5e16bd70`, spawned about 07:26:00 with reply-and-end brief; parent received `done wc-end-5e16bd70`; state completed with exact final at 07:26:12 | Failure not provoked; no failure behavior proved |
| Scheduled check-in | yes | Discover in-chat scheduler; [in-chat scheduled tasks](https://learn.chatgpt.com/docs/automations#schedule-a-task-inside-a-chat) | fail | Repeated tool inventory exposed no scheduling tool. Computer Use `getApp` for `com.openai.codex` refused access “for safety reasons” | No 1–2 minute request could be issued, no rejection of an interval, no longer fallback, no scheduled arrival, no termination/read-back proof; not a scheduler pass |

Verdict: **not ready: Scheduled check-in**. The coordinator cannot prove it can wake itself on a schedule, so a silent worker may go unnoticed between user messages. Subagent detection and the other five capabilities passed; this run does not establish the target desktop session's identity or phone access.

Cleanup: both probe workers read completed; no background processes remained. No scheduled task was created in this run. Scheduler listing and cleanup read-back were unavailable, so this run cannot certify the absence of tasks left by earlier runs. Not exercised: scheduled arrival and termination, failure notice, desktop/phone reachability. The requested shortest schedule remains untried because scheduling access is absent.

Pass as an evidence eval: yes (including the failed essential capability and its consequence). Readiness: no. The #528 scheduling proof remains open. The incoming user decision accepts one arrival across Harnesses; it does not change this run's missing scheduling evidence.

### 2026-11-03 06:05-07:06 UTC, commit fd8b853 (branch `claude/project-thread-r67ntb`, PR #531), dev-skills 0.48.0 (base): claude.ai project, check run (Case 1), and unknown-harness case (Case 2)

Source: the coordinator's recorded run, [#527 comment 6597596744](https://github.com/Luffytse/luffy-dev-skills/issues/527#issuecomment-6597596744), copied here. Supersedes the "check still owed" entries below for the check. On 2026-11-03 the user accepted one scheduled arrival as enough, so nothing is still owed for the check.

#### Case 1: Claude Code project, check run

Runner: a project thread (session `session_REMOVED`, parent `session_REMOVED` = the coordinator), not the coordinator: the coordinator reported it held no `get_session` in that turn and cannot create timers. Worker starts went through the coordinator, which started 3 cheap-tier threads (probe A, probe B, stop thread) from the runner's exact briefs. The coordinator read the check-in arrival itself.
Runtime (probe 1): `get_session` on the runner's session: `environment_kind` `anthropic_cloud`, permission mode `auto`, `parent_session_id` = the coordinator. Tools: `message_coordinator` present, `start_thread` absent: thread/worker row 2 of the detection table, matches the reference. Shell: `CLAUDECODE=1`, `IS_SANDBOX=1` (sandbox on), `CLAUDE_CODE_CHILD_SESSION=1`. Held: `create_trigger`, `list_triggers`, `update_trigger`, `delete_trigger`, `send_later`, `archive_session` (via claude-code-remote), `get_session`, `list_events`.
Docs used: the pages cited in `claude-code-project-threads.md` (projects, scheduled tasks, cloud sessions).

```
| Capability | Essential | Method | Result | Evidence | Limits |
| Start a worker | yes | coordinator start_thread | pass | A: thread cmsg_...SN6n2t..., session cse_REMOVED; B: cmsg_...Va8iaw..., cse_REMOVED; both created 06:05:44-46 and readable by get_session at 06:05:57 | none |
| Worker state | yes | get_session | pass | A at 06:05:57: RUNNING / bucket WORKING; after its turn IDLE / WORKING | read by a thread; the coordinator said it had no get_session that turn, so "get_session from the coordinator" is unproven |
| Pause and resume | yes | message_thread "Pause/Resume <token>" | pass | pause sent 06:05:59, A stopped its loop (TaskStop 06:06:07, one line written 06:05:58) and replied "paused wc-start-41bdf5b7" 06:06:10; resume sent ~06:06:20, loop restarted 06:06:24, "resumed ..." reply 06:06:24 | scratch file is in A's container and could not be read; growth rests on A's own tool output and replies |
| Confirmed stop | yes | stop thread (wc-stop-07d4a46a, session cse_REMOVED) | pass | stop thread: before IDLE/WORKING, archive_session, after ARCHIVED/COMPLETED (06:06:32-06:07:01); the runner then read A itself: session_status ARCHIVED, bucket COMPLETED | an archive can be undone with unarchive_session |
| End or failure notice | yes | thread reply wakes coordinator | pass | B replied "done wc-end-21c72645" 06:05:57; the coordinator got it as a wake; get_session on B: IDLE, bucket COMPLETED (post_turn_summary completed) | list_threads did not show B for about a minute after it ended (coordinator's read at 06:06); only get_session showed it. Failure not provoked |
| Scheduled check-in | yes | thread creates recurring task aimed at the coordinator | pass (one arrival; the user accepted it on 2026-11-03) | created trig_REMOVED 06:05:33 ("0 * * * *" stored as "5 * * * *", aimed at the coordinator via persistent_session_id). Arrived in the coordinator's own events 07:05:40.997Z, triggerFireReason scheduled, inbound_origin trigger_fire, its own turn, not a wake; last_run SUCCEEDED, session cse_REMOVED. Ended: delete_trigger, then list_triggers(enabled=true) empty | the second arrival (due 08:05) was skipped on the user's word, and the user later accepted one arrival as enough (the earlier rule "at least twice" is dropped): a 5-minute schedule was rejected ("minimum interval is 1 hour"), so the test cannot be made shorter. Arrival was about 35 s after the cron minute |
```

Also created and deleted: `trig_REMOVED` (a one-shot `send_later` reminder to the runner); `list_triggers` shows no scheduled task of this run left.
Cleanup: probe A archived, probe B ended (COMPLETED), stop thread ended; no scheduled task left.
Verdict: ready. Start, state, pause/resume, confirmed stop, end notice and scheduled check-in pass. The check-in method works: one scheduled arrival in the coordinator's own record, ended and read back. Note 2026-11-03: the run first read "ready except one row" because the skill then required two arrivals; the user decided one arrival is enough and the rule was changed in the skill, so the verdict is ready.

#### Case 2: unknown harness

A fresh subagent was given only `SKILL.md` and `FACTS.md` (it found `DOCS.md` from the runtime help line). Against the README's pass list:
- Step 1: no row matched; harness named Example Runner 3.2 from `EXAMPLE_RUNNER_VERSION`. Pass.
- Step 3 from DOCS.md: start `spawn_worker`; state `worker_status`; `message_worker` NOT taken as stop or pause. Not available: stop, pause/resume, end/failure notification (polling only), scheduled check-in. Pass.
- Nothing taken from a Claude Code reference. Pass.
- One user line: "No reference for Example Runner; I read its methods from DOCS.md... Not available: stop, harness pause and resume, a worker-to-coordinator reply channel, end or failure notification, and scheduled check-in." Pass.
- Planned Verdict: not ready: Pause and resume, Confirmed stop, End or failure notice, each with its meaning. Confirmed stop and End notice named, as required. Scheduled check-in was marked "not relied on" (allowed by Step 4 probe 7); the README lists it as a failure "where the work relies on them".
- Minor: it added a "worker-to-coordinator reply channel" limit the docs do not state outright, and left the role "unknown". Neither changes the verdict.

Not exercised: a provoked failure; Remote Control threads.
Pass: yes for Case 2; Case 1 ready (above). Lessons: (1) `list_threads` can lag about a minute after an end and the coordinator may not hold `get_session`: the reference now names the read the coordinator can use and lets a thread read `get_session` for it. (2) The scheduler's minimum interval is one hour, so the check-in probe takes about 1.5 hours with one arrival required (the rule first read two arrivals, about 2.5 hours; the user dropped it on 2026-11-03): recorded in probe 7. (3) Probe workers run in separate containers, so "scratch file grows" is not available from outside; replies are the evidence for a project check: now stated in probes 3 and 4.

### 2026-11-03, commit 583b965 (branch `t527-harness-team`; base 36a2530), dev-skills 0.48.0 (base): claude.ai project, detection by tool names and the check still owed (check superseded by the 06:05 UTC run above)

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
| Scheduled check-in | yes | a thread creates one recurring task aimed at the coordinator's session; routines#add-a-schedule-trigger | not run | - | owed: one arrival in the coordinator had never been shown; at least an hourly interval, so the probe takes over an hour (shown at 07:05 UTC in the run above) |

Verdict: not ready: every capability, since the check has not run
```

Not exercised: every probe. **Still owed:** the coordinator's run of the check with the threads it starts, including the recurring check-in arriving and a stop thread stopping another thread and reading it back. A subagent of a worker cannot run it: it is not the coordinator and starts no thread.
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
