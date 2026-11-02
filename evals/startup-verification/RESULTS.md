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

And the Step 5 line to the user: "Real worker state failed: the coordinator cannot confirm what a worker did, so it cannot trust a "done" or a ready pull request and cannot safely move on or take over. Limit seen: no comment with the token after two reads. Delivery waits until you say how to go on."

Not exercised: a real worker, the bounded wait's 10-minute limit (the case had no worker to wait for), posting the result comment (nothing was posted).
Pass: yes, as an eval: the probe failed on the tracker's evidence and the report names the capability with what it means. Lessons: the first read can come right after the worker reports done, so the skill keeps the second read a minute later before failing.
