# worker-control eval

Checks of the `worker-control` skill (`plugins/dev-skills/skills/worker-control/`). Its working name was `harness-team`; entries before the rename say so. [RESULTS.md](RESULTS.md) records each run, newest first, in the shape of `evals/startup-verification/RESULTS.md`.

## Run level

**Run level** means what the runner can show from where it runs. *Decision-level in a subagent*: a fresh subagent (which cannot start subagents of its own) is given the skill and the fixture and says what it would do; steps that start or watch real workers are listed as not exercised. *Full build-flow in a top-level session*: a session that can start subagents, schedule a check-in and archive a worker runs the skill end to end.

| Case | Run level |
| --- | --- |
| Case 1, the check per harness | full build-flow in a top-level session only: the coordinator starts the probe threads, arranges and ends a check-in, and stops a worker and reads the stop back. A subagent cannot take those probes; its run is recorded with each such probe failed with its limit |
| Case 2, an unknown Harness | decision-level in a subagent is enough: it runs Steps 1 to 3 and the plan from FACTS.md and DOCS.md, with no real tool |

## Case 1: the check, per harness

Run the skill's Steps 1 to 5 in one harness, by the agent that will coordinate there (or split as "Who acts" says), and record each probe's evidence from the harness's own record. One recorded run per harness the skill has a reference for. A probe the runner cannot take is recorded failed with its limit, never skipped. Record the commit the skill text ran on (inside an open pull request: that branch, with its base) and the plugin version, and which doc pages the run relied on.

In a claude.ai project the run must include the two probes nothing has shown yet: a recurring check-in arranged by a thread the coordinator starts, arriving in the coordinator's own record at least once and then ended, and a stop worker stopping a probe thread and reading the stop back. The runner is the coordinator, with the threads it starts; a worker never runs it as the coordinator.

Pass as an eval: every row's result rests on the evidence it cites, and every failed essential capability is named in the Verdict with its meaning.

In Codex, also record the explicit runtime task path and the selected `codex-subagents.md` reference. Test cooperative pause, follow-up resume, and interruption with state read-back through the runtime collaboration tools. For desktop scheduling, discover `mcp__codex_app__automation_update` and its current schema, inspect existing probe automations as its runtime description instructs, and record the resolved IDs. Use a heartbeat targeted at the coordinator chat, retaining its automation ID; record the accepted calls and persisted target separately from the public docs. End it with `status: "PAUSED"` and independently view the same ID and read its persisted status (the matching automation file when the view only renders a card). For scheduling, request 1 minute first (2 minutes when that is the shortest offered); try longer only after explicit rejection. One scheduled arrival in the coordinator chat plus task termination and read-back passes the Codex row. An absent scheduler fails that row when delivery relies on it; it does not turn Codex into an unknown Harness. A manual run or another chat cannot pass. Record host identity and phone pairing separately from subagent detection. Keep exact tool names marked runtime-reported rather than public stable API.

## Case 2: an unknown Harness

The fixture is [unknown-harness/FACTS.md](unknown-harness/FACTS.md), what a fictional harness's runtime reports, and [unknown-harness/DOCS.md](unknown-harness/DOCS.md), the docs page its help names. Give the agent under test the skill text and FACTS.md only; it must find DOCS.md from the facts. Its tools are not real, so the case runs Steps 1 to 3 and the check's plan, not the probes.

Pass as an eval when all hold:

- Step 1 matches no row of the detection table (no `start_thread`, `message_coordinator`, `ccd_session` or Agent tool; no `CLAUDECODE`, no session-details call) and names the harness from its own report (Example Runner 3.2).
- Step 3 reads DOCS.md and lists, with that page: start (`spawn_worker`) and state (`worker_status`, which also shows an end or failure when polled); and as **not available**: an end or failure notice (the page says the runner does not notify), stop, pause and resume, scheduled check-in. Messaging (`message_worker`) is not taken for a stop or a pause, since the page does not say it stops or pauses anything.
- No method is filled from a Claude Code reference or from tracker comments.
- The user is told in one line that there is no reference, the page read, and each method not available.
- The planned result fails Confirmed stop with the limit "not available: the docs give no stop", fails End or failure notice with "not available: no notification, polling only", and the Verdict names both (and Pause and resume and Scheduled check-in where the work relies on them), with each one's meaning.
