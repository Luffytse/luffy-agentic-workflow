# Results

One entry per run of the `milestone` skill's Startup verification, newest first. A run carries out the steps of "Startup verification" in `plugins/dev-skills/skills/milestone/SKILL.md` in one environment (a Claude Code cloud project, Codex), either by a verification thread started with the skill or by hand by a runner reading the skill's text (say which), and records the runner, the runtime settings and each probe's evidence. Record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`; an entry written inside an open pull request names the commit and version it ran on as its base.

Each environment's run is followed by one **planted failure**: the real-worker-state probe told to expect a marker token that no worker is asked to write. It passes as an eval when the probe reports `fail` with "no comment with token", and the Verdict names the capability, which shows the failure report.

## Template

```
### <date>, commit <sha>, dev-skills <version>: <environment>, <real run | planted failure>

Runner: <who ran each probe, and why that runner>
Runtime: <environment kind; permission mode; sandbox; probe tools held; how each was read>
Probes: <per probe: action, times, evidence, result, limits>
Result comment: <link, or the comment text when it was not posted>
Not exercised: <what this run did not reach>
Pass: yes | no. Lessons: <what to change in the skill, if anything>
```

## Runs

### 2026-11-02, commit 7a97cb5 (base), dev-skills 0.34.0 (base): Claude Code cloud project, real run of all four probes

Runner: the Spec thread of #405, playing the runner by hand from this branch's skill text (the `milestone` skill is not in the loaded plugin, see Loaded skill version), for the same reason as the entry below: the scheduled check-in and the stop must run in the session that holds the tools. Tools held, read from the session-details call: subagent start, `TaskStop`, one-shot scheduling, the scheduled-task list, tracker read and write; no tool that starts a thread.
Runtime (read at 2026-11-02T06:13Z): environment kind `anthropic_cloud`; permission mode `auto`; sandbox on (`IS_SANDBOX=1`); session `session_REMOVED`, created 2026-11-02T05:45:13Z, child of the coordinator session. Correction to the entry below: the project's `.claude/settings.json` turns off `dev-skills@luffy-dev` (the marketplace install), but the session still loads `dev-skills` 0.34.0 from the account's synced plugin folder under `/root/.claude/plugins/synced/` (account marketplace, sync record updated 2026-11-02T05:41:31Z), not from the checkout. Its skill files match main's at 7a97cb5 except for quoting in two descriptions' front matter, and it has no `milestone` skill.
Probes:
- Scheduled check-in: `send_later` to the thread's own session, token `sv-checkin-c5e20d4b`, at 2026-11-02T06:06:01Z, `delay_minutes: 2`, scheduled for 06:09:00Z; the turn ended and the runner kept working. The check-in arrived carrying the token at 06:13:14Z, 4m14s after the scheduled time (the runner was mid-turn, so delivery waited), inside the 15-minute bound. Scheduler record (`list_triggers` with completed tasks): `ROUTINE_RUN_STATUS_SUCCEEDED`, `fired_at` 06:13:14Z, `run_once_fired`. Pass. Limits: one-minute granularity; delivery only after the runner's turn ends.
- Real worker state: cheap-tier subagent, token `sv-worker-4d81a6f2`; the thread read #405's comments from the tracker (not the worker's report): https://github.com/Luffytse/luffy-dev-skills/issues/405#issuecomment-6570344254, created 06:06:09Z, author `Luffytse` (the tool acts as the user). Pass. Limits: marker on Spec #405, not the Milestone issue.
- Confirmed stop: worker a background cheap-tier subagent, token `sv-stop-9b3e07a1`, appending a line every 30 seconds to a file in the session scratchpad. Before the stop: the harness's task notification at about 06:07Z listed it as waiting on its own background work (running), and the file had 3 lines (the last `06:07:10Z`). Stop: `TaskStop` with its task id at about 06:07:18Z. After: no readable record of the worker's state: `TaskStop` only answered that the call succeeded, `TaskGet` returned "Task not found" (it reads a different task list), the session-details call lists no workers, and the subagent's output file is its transcript, not a status. Corroboration only: at 06:08:19Z the file still had 3 lines and no worker process remained. Result: fail, limit "no readable worker state after a stop" (a stop-call success and a quiet worker are not a pass). The worker was a subagent; the runner cannot start a thread, so a thread stop was not tried.
- Loaded skill version: read by the Spec thread itself at 06:08Z (its session started 05:45:13Z, after main's last plugin commit 7a97cb5 at 05:41:26Z, so it is a fresh thread). Invoking `dev-skills:model-tiers` printed the base directory `/root/.claude/plugins/synced/8e7fd854-f39e-4f5b-8f8a-51d71989d5b7_79d471f9-a365-47c8-a7a1-254320c39e4c/dev-skills/skills/model-tiers`; the manifest at that plugin root says 0.34.0; main's manifest, read from the remote (`get_file_contents`, ref main, 7a97cb5), says 0.34.0. Pass. The earlier reading by the #466 Implementer subagent (05:5x-06:05Z) agrees. Limits: equal versions do not show equal text where a skill change merges without a bump; the loaded copy is the account sync, not the marketplace install the project settings turn off.
Result comment: https://github.com/Luffytse/luffy-dev-skills/issues/405#issuecomment-6570450014 (Verdict: not ready: Confirmed stop)
Not exercised: stopping a thread rather than a subagent (the runner cannot start threads); a stale cache (the loaded version equals main's); the coordinator's own tools; a run in Codex (#467).
Pass: no for the Verdict, yes as an eval of the skill: three probes passed on observed evidence and the fourth failed with its limit named, which is the result the skill is built to give. Lessons: in this Claude Code cloud project a stopped subagent has no state record the runner can read, so the Confirmed stop probe fails here until delivery uses a worker kind that keeps one (a thread's session state) or the runner is given a way to read task state; the skill's pass rule is unchanged, and the user hears about the failure before delivery starts (Report a failure step).

### 2026-11-02, commit 7a97cb5 (base), dev-skills 0.34.0 (base): Claude Code cloud project, real run

Runner: the Spec thread of #405, playing the runner by hand from this branch's skill draft: the skill was not in the base and the installed plugin was off, so no verification thread was started with the skill. The probes ran in the Spec thread's session, not in the Implementer subagent, because the scheduled check-in must run in the session: a check-in scheduled from the session fires into the session after its turn ends, which the subagent never sees (the subagent ends when it reports). The session's own record lists the thread's tools as including subagent start, one-shot and recurring scheduling and the scheduled-task list (scheduling, scheduled-task list and session-details tools); the coordinator's tools were not read. So in this project the thread is the runner, as the skill's "Who runs it" says for a project thread that holds its own tools.
Runtime (read at 2026-11-02T05:47Z from the session-details call and the container environment): environment kind `anthropic_cloud`; permission mode `auto`; sandbox on (`IS_SANDBOX=1` in the environment); the session is a child of the project's coordinator session; the scheduled-task list was empty before the run. The user settings file turns the installed `dev-skills` plugin off, so the thread reads skills from the checkout (relevant to the later loaded-skill-version probe).
Probes:
- Scheduled check-in: `send_later` to the thread's own session with token `sv-checkin-3f9a1c7e` at 2026-11-02T05:50:45Z, `delay_minutes: 2`, scheduled for 05:53:00Z; the turn then ended. The check-in arrived in the session at 05:54:12Z carrying the token (the notification queue read it at 05:54:15Z), 1 minute 12 seconds after the scheduled time, well inside the 15-minute bound. The scheduler's own record (`list_triggers` with completed tasks) shows `ROUTINE_RUN_STATUS_SUCCEEDED`, `fired_at` 05:54:12Z, and the task disabled itself (`run_once_fired`). Pass. Limits: one-minute scheduler granularity; delivery only after the turn ends.
- Real worker state: a cheap-tier subagent was briefed to post one comment with first line `<!-- startup-verification marker sv-worker-b27d41e9 -->`. The thread then read the comments of #405 from the tracker at 05:51:01Z, not from the worker's report: the comment exists (created 05:50:54Z, after the probe started), link https://github.com/Luffytse/luffy-dev-skills/issues/405#issuecomment-6570129032, author `Luffytse` (the GitHub tool acts as the user, so the author does not tell worker from thread). Pass. Limits: the marker went on Spec #405 rather than the Milestone issue (#396), to keep the Milestone issue clean in this eval run.
Result comment: https://github.com/Luffytse/luffy-dev-skills/issues/405#issuecomment-6570176272
Not exercised: confirmed stop and loaded skill version (the next Ticket, #466); whether the coordinator itself holds the scheduling and worker tools (not read); a run in Codex (#467).
Pass: yes, for the two probes of this Ticket. Lessons: the author on a tracker comment cannot separate worker from thread here, so the token, not the author, is what ties the comment to the probe.

### 2026-11-02, commit 7a97cb5 (base), dev-skills 0.34.0 (base): Claude Code cloud project, planted failure

Runner: the Implementer subagent of #465, inside the Spec thread's session. Reading the tracker is all this case needs, and the subagent holds the tracker read tool.
Probes: real worker state only. Expected token `sv-planted-874d533c` on #465 (standing in for the Milestone issue, since no worker writes to it in this case). No worker was started and nobody was asked to write the token. First read of #465's comments at 2026-11-02T05:47:25Z returned an empty list; the second read, after the wait, at about 2026-11-02T05:48:50Z, also returned an empty list.

Failure report, in the result shape:

```
| Real worker state | yes | marker token sv-planted-874d533c expected on #465; no worker asked to write it (planted) | fail | no comment with token (2 reads, 05:47:25Z and ~05:48:50Z); worker said: none | planted case: the token was never meant to be written |

Verdict: not ready: Real worker state
```

And the line to the user, from the skill's "Report a failure before delivery starts" step: "Real worker state failed: the coordinator cannot confirm what a worker did, so it cannot trust a "done" or a ready pull request and cannot safely move on or take over. Limit seen: no comment with the token after two reads. Delivery waits until you say how to go on."

Not exercised: a real worker, the bounded wait's 10-minute limit (the case had no worker to wait for), posting the result comment (nothing was posted).
Pass: yes, as an eval: the probe failed on the tracker's evidence and the report names the capability with what it means. Lessons: the first read can come right after the worker reports done, so the skill keeps the second read a minute later before failing.
