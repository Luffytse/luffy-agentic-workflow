# Delivery is split into Milestone planning, a team lead and harness references

The `milestone` skill had grown to 69 KB and its review fixes no longer converged: it held planning with the user, Startup verification and the coordinator's whole delivery loop, and more than half of that loop was unattended safeguards built as 17 kinds of tracker-comment record that every wake re-derived. A trace of about 50 Milestone bugs and review findings found about 21 caused by thread lifecycle guessed from tool descriptions and dry runs (no Harness doc was ever cited; a thread that died stayed "running" because running was inferred from tracker comments) and about 16 by the skill's own record kinds colliding (pause during a takeover, a lifted park while paused). Decided with the user in Spec [#523](https://github.com/Luffytse/luffy-dev-skills/issues/523) (2026-11-02/03), with the name and the check-in timing settled in [#523's comments](https://github.com/Luffytse/luffy-dev-skills/issues/523#issuecomment-6593196770) and [#529's](https://github.com/Luffytse/luffy-dev-skills/issues/529#issuecomment-6595067028).

## Three roles

- **Milestone planning** (`milestone`): the user and an agent write the Milestone issue, add a feature mid-Milestone, run Startup verification and, at the end, write the report for the user's Milestone review. Its delivery loop is gone; its Delivery section points at the team lead.
- **The team lead** (`team-lead`): the role the coordinator runs whenever it delivers planned work, always a Milestone's (amended 2026-11-04, [ADR 0012](0012-release-is-version-free-and-command-free.md): a small Release is a one-Release Milestone, so the separate lone-Release path is gone). It manages work, not machinery: it starts build threads in order within the limits and starts Release threads (Release grouping stays `release`'s rule), reacts to what workers and the Harness report, holds a check-in only as a safety net, replaces a stalled worker, pauses and resumes on the user's word, and follows the merge-time steps the repo's own docs give (this repo has none since ADR 0016, which replaced ADR 0008's hand-out and re-read). "Coordinator" stays the name of the project's own agent.
- **Harness references** (`worker-control`, a Base skill, ADR 0009): it detects how workers run from what the runtime reports, loads one reference per way workers run, and runs the short check that proves those methods here. Every worker lifecycle action the team lead takes (start, check state, notice an end, stop, pause, resume, arrange and end a check-in) goes through it by name, so no Harness tool name or thread state sits in the team-lead text.

## Harness state is the truth

A worker's state, its end and its failure come from the Harness's own record, read through `worker-control`. Tracker comments are an audit trail for the Milestone report: a start record per worker, a nudge, a park, a pause and a resume, and a check-in arranged or ended. None is read back as a worker's state; the pause record is read back only because a pause is the user's word, which no Harness holds where it has no pause of its own.

## Event-driven, with a check-in as the safety net

Where the Harness pushes events (a Claude Code project wakes its coordinator on every thread report, failed turn, stopped machine and permission prompt), the team lead reacts to them. A scheduled check-in at the Boundary record's interval is only the safety net for a worker that is silent but nominally working; in a Harness that pushes nothing it carries more of the load. It is arranged when the first build worker starts (not when a Milestone is planned, and never for a Release worker that only plans; a Release worker is watched by Harness events, and at a check-in only to tell the user once when it has been silent a whole interval) and ends when delivery ends; the team lead decides when, `worker-control` arranges and ends it.

A check-in reads one **snapshot**: a command shipped with the team-lead skill (`snapshot.py`) that reads the tracker the way the tracker doc says it is kept (GitHub through `gh`'s REST routes, or a local Markdown tracker) and git, and prints one row per worker: its Harness state as `worker-control` gave it, last commit, last comment, pull request and a verdict (active, silent since a time, nudged and waiting, still silent after its nudge, or pull request ready but not reported: merged, or ready with no worker activity since, because a Spec thread marks its pull request ready before its review). A tracker the command cannot read, a failed read or no shell falls back to reading the same columns by hand. A check-in that finds nothing to act on writes nothing.

## Takeover and pause, kept simple

- **Takeover:** nudge once; still silent, stop it through `worker-control` and read the stop back from the Harness; then start a fresh worker from the pushed branch and the tracker. A worker the Harness reads as ended without its result is replaced the same way, without a stop. A second stall, a stop that does not read back or a fresh start that fails parks the feature and tells the user once. No stop-thread records, stall records, lift records or adopted review parks: a lifted park is an issue whose last worker's state is read through `worker-control` before a fresh one starts.
- **Pause:** start nothing new and ask running workers to stop at their next natural step, using the Harness's own pause where it has one. Resume carries on from the tracker and the branches, with activity counted from the resume (the snapshot's `resumed`, so a nudge before it is void); a worker that does not carry on is handled like any silent one. No safe-point or paused records.

## Harness references cite their docs

Each `worker-control` reference lists what the Harness does by itself and each method the coordinator adds, each with the doc page it comes from, or marked runtime-reported, and proved in this repo by its Environment check; `scripts/check-plugin.sh` (`worker-reference-sources`) checks that every method and Harness fact carries a link. Pages read for the Claude Code references: [projects](https://code.claude.com/docs/en/claude-projects), [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web), [scheduled tasks](https://code.claude.com/docs/en/routines), [sub-agents](https://code.claude.com/docs/en/sub-agents), [desktop](https://code.claude.com/docs/en/desktop) and [scheduled tasks in a session](https://code.claude.com/docs/en/scheduled-tasks); the Codex reference (#528) starts from [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [app-server](https://learn.chatgpt.com/docs/app-server) and [automations](https://learn.chatgpt.com/docs/automations). A Harness with no reference falls back to its own docs and names each method they do not give.

## Considered options

- **Keep one `milestone` skill and fix its record collisions one by one.** Each review Round found a new combination and the fix added a clause; the fixes did not converge.
- **A lifecycle agent that watches the workers for the coordinator.** It would remove the guessed lifecycle but not the record collisions, which would move to another agent, plus a hand-off and "who watches the watcher".
- **Keep the confirmed-stop takeover with its stop threads and per-step records.** The Harness's own state, read back after the stop, gives the same safety with no records to re-derive.

## Consequences

- `milestone`'s planning, adding a feature, Startup verification and report stay there (slimmed by #530); its delivery dry runs move to `evals/team-lead/`, rebuilt on Harness events, and cases for records that no longer exist are cut.
- Milestone issues opened under the earlier loop keep reading correctly: each earlier `<!-- milestone ... -->` record counts as its team-lead counterpart (a `delivery thread` record as a `start` naming its worker, `delivery thread ended` as that worker's end, `nudge`, `stall`, `parked`, `park lifted`, `pause` and `resume` as theirs, `check-in`, `check-in ended` and `stand-up` as `check-in`), and a worker such a record names is read through `worker-control` like any other, so a running one keeps its slot and no second worker starts beside it (the `deliver-earlier` case, Milestone 1's own #523).
- ADR 0008's "the Milestone loop lives in the `milestone` skill" now reads: delivery lives in the `team-lead` skill.

## Note (Spec #151)

Two references remain, both for Claude Code (`claude-code-project-threads.md` and `claude-code-sessions.md`). The Codex reference named above was deleted when the plugin came to support Claude Code only; `worker-reference-sources` checks the two that remain.

## Note (Spec [#162](https://github.com/Luffytse/luffy-agentic-workflow/issues/162), 2026-11-14)

`milestone` keeps only the Plugin version check; Startup verification is gone. `worker-control` no longer runs a short check: its probes are this repo's Environment check (`docs/dev-skills/environment-check.md`), and a Harness with no reference no longer falls back to its own docs: `worker-control` tells the user and stops.

## Note (Ticket [#167](https://github.com/Luffytse/luffy-agentic-workflow/issues/167), 2026-11-14)

`milestone` no longer adds a feature mid-Milestone: its features are named, sorted and planned in their own sessions before the Milestone issue is written, and are fixed once planning settles ([ADR 0017](0017-milestone-features-are-planned-in-their-own-sessions-and-fixed-once-planning-settles.md)).
