# Results

One entry per run of the `team-lead` eval, newest first ([README](README.md) says how to build, run and score it).

## Template

Every new entry records its run level (see [Run level](README.md#run-level)); earlier entries have no such line and are not rewritten.

```
### <date>, commit <sha>, dev-skills <version>: <case or check>

Run level: decision-level in a subagent | full build-flow in a top-level session | no model session (unit tests)
Runner: <a fresh premium-tier session, or by hand; the coding agent>
Ran: <what was run, and its output in short>
Pass: yes | no. Not exercised: <what this run did not reach>. Lessons: <what to change>
```

## Runs

### 2026-11-03, branch `t529-team-lead`, dev-skills 0.48.0 (unbumped): Ticket #529 after Ticket check 3

Runner: the Implementer subagent of Ticket #529, by script.

Ran: snapshot unit tests, 31. Two new tests failed before the change and pass after:
- a nudge 57 minutes old with a 60-minute window reads "still silent after its nudge" (a 10-minute grace, since the nudge record is written minutes after its check-in);
- a replacement started after its predecessor's pull request merged reads active (the ready time is compared with the later of `reported` and `started`).

The case self-test still passes (6 tests).

Pass: yes, for what ran. Still owed: as in the entry below.

### 2026-11-03, branch `t529-team-lead`, dev-skills 0.48.0 (unbumped): Ticket #529 after Ticket check 2

Runner: the Implementer subagent of Ticket #529, by script.

Ran: snapshot unit tests, 29. Four new tests failed before the change and pass after:
- a `### Round 2 summary` heading inside a comment body, which crashed the Markdown reader before;
- a resume restarting the silence clock and voiding an earlier nudge;
- an earlier `<!-- milestone nudge -->` record counting as a nudge;
- an earlier `<!-- milestone stand-up -->` record not counting as activity.

Case self-test: 6 tests passed. In `deliver-pause`, the resumed worker now pushes nothing after the resume. At event 8 its row reads silent without `resumed` and active with it; at event 9 it reads silent since the resume and is nudged. A running Release worker's silence is now read by hand at a check-in and brought to the user once; no case covers that yet (owed).

Pass: yes, for what ran. Still owed: model runs of the five cases, a silent-Release-worker case, a run through a real Harness reference, and the snapshot against the real GitHub API.

### 2026-11-03, branch `t529-team-lead`, dev-skills 0.48.0 (unbumped): Ticket #529 after Ticket check 1

Runner: the Implementer subagent of Ticket #529, by hand and by script, as below.

Ran:

- **Snapshot unit tests:** 25 tests. The three new ones (a lost report found by the branch on the Markdown tracker and through the REST API, and a ready pull request acted on and then tested for silence through `reported`): the two branch-lookup tests failed before the change and pass after; the `reported` sequence already passed and now guards it.
- **Case self-test:** 6 tests passed. Five reference runs scored clean (`deliver` 33/33, `deliver-stall` 28/28, `deliver-lift` 37/37, `deliver-pause` 20/20, the new `deliver-earlier` 7/7), with 26 check-in snapshot readings as built. Five planted wrong runs failed at the planted event, two of them new: a second worker on 10 beside its old delivery-thread record, and a check-in arranged for a Release worker that only plans.
- **Milestone 1, read again:** the earlier entry's trace stands with two changes. The team lead no longer requires a Startup verification result from the Harness it detects now; when the latest result's Runtime line plainly names another environment (Codex desktop here, if delivery resumes in a Claude Code project), it tells the user. And every earlier `<!-- milestone ... -->` record on #396 and its features counts as its team-lead counterpart, so a worker an old delivery-thread record names and the Harness reads running holds its slot (the `deliver-earlier` case). The check-in is arranged when delivery resumes with a build worker running, or at the next build-worker start.

Pass: yes, for what ran. Still owed, as in the entry below: model runs of the five cases, a run through a real Harness reference, and the snapshot against the real GitHub API.

### 2026-11-03, branch `t529-team-lead` off the Spec branch of #523, dev-skills 0.48.0 (unbumped): Ticket #529

Runner: the Implementer subagent of Ticket #529, in a Claude Code cloud session (a worker, not a coordinator).

Ran:

- **Snapshot unit tests** (`test_snapshot.py`): 21 tests. Before `snapshot.py` existed: 21 failed (9 failures, 12 errors). After: 21 passed, including the five hand-read fallbacks.
- **Case self-test** (`test_cases.py`): 4 tests passed. The four cases' reference runs, written by hand from the skill text, scored clean (`deliver` 33/33, `deliver-stall` 27/27, `deliver-lift` 36/36, `deliver-pause` 18/18), and every check-in's snapshot printed the verdict the world is built to show (17 snapshot readings across the cases). The three planted wrong runs failed at the planted event.
- **Milestone 1 under the new skill** (the user's story 26), read-only on [#396](https://github.com/Luffytse/luffy-dev-skills/issues/396) and [#514](https://github.com/Luffytse/luffy-dev-skills/issues/514) on 2026-11-03. The No Milestone test holds (#396 is open, carries `milestone-1`, its body is the Milestone). Its order rule reads "one at a time, in this order": one slot. Its feature table has the columns Piece, Kind, What it changes and Who merges, not `milestone`'s shape, but the team lead reads only the features, their order and the boundaries, all present; row 14 is #523. The latest `<!-- milestone pause -->` record (2026-11-02 23:26Z, "please stop here") has no resume record after it, so a pause is in effect: the team lead starts nothing until the user says to resume, which is what the user asked for. The latest Startup verification result (2026-11-02 16:20Z) reads `Verdict: ready` but was run in Codex desktop; a coordinator in a Claude Code project is another Harness, so the team lead asked for Startup verification again there (superseded the same day: see the entry above). The current Release is #514 (`release-m1-r4`, carried by open issues): its maintenance fixes are all closed or moved out, and its one open feature is #523, whose Spec worker is running, so that worker holds the slot and nothing else starts. The earlier check-in, Stand-up, pause and paused records stay as history; the old check-in was ended on 2026-11-02, so the team lead arranges a new one through `worker-control` when delivery resumes.
- `bash scripts/check-plugin.sh`, `python3 scripts/test-check-plugin.py` and `claude plugin validate .` passed (see the pull request's Evidence).

Pass: yes, for what ran. Not exercised, and owed: a model run of each of the four cases by a fresh premium-tier session (the reference runs are by hand, so they show the cases can be passed, not that the skill's text leads a model to pass them); a run against a real harness through a `worker-control` reference rather than the dry-run fallback; the snapshot command against the real GitHub API (only a stub `gh` was used); the `milestone` planning and report cases, unchanged here.
