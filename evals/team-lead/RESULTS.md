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

### 2026-11-04, commit `578842d` (`claude/project-thread-l41n5a`), dev-skills 0.71.0 (unbumped): `deliver-stall` and `deliver-lift` after Ticket #654

Run level: decision-level in a subagent
Runner: the Ticket thread. One fresh premium-tier subagent per case per skill version, each given the checkout's skill text (the branch's, which is `fd2c798`'s `SKILL.md`, unchanged by `578842d`; main's from a `git archive` of `7dc6244`, 0.71.0), the case's fixture prompt and nothing else; `evals/` was kept away from it. Scored with the final `score.py` of `578842d`.
Ran: `score.py` on each run. Evidence: [`evidence/654/`](evidence/654/), one folder per run with `proposed-actions.md` and `score.txt`. In the copied evidence, the run directory's path reads `<runs>` and model names read `<model>`, so that the `vendor-model-names` check in `scripts/check-plugin.sh` passes. The scores were rerun on the edited files.

| Case | Branch | Main |
| --- | --- | --- |
| `deliver-stall` | 28/28 | 28/28 |
| `deliver-lift` | 37/37 | 37/37 |

Pass: yes. The change is to where the `nudge` and `parked` records go (the worker's issue; the Milestone issue keeps `pause`, `resume` and `check-in`). The branch's four nudge records (two per run) are all on the worker's issue (10-farewell.md, 20-quiet.md). Main's two runs this time also put them on the worker's issue and so passed. The #638 baseline's two main runs put the nudge on the Milestone issue and failed 2 checks each, so the ambiguity in main's line shows in only some runs; this run does not show the change moving a result, and the line's value is that it removes the chance of the other reading.
The scorer change: the mention rule of the check "events 7 to 12". The scorer on main (before the fix) fails `branch-deliver-stall`, `main-deliver-stall` and `main-deliver-lift`: their event 11 park notice for 20 mentions 10-farewell.md as context ("With 10-farewell.md also parked, ..."). It would pass `branch-deliver-lift`, whose event 11 notice does not mention 10. The final scorer passes all four. The #638 evidence has the same failure ("events 7 to 12" in its `deliver-stall` and `deliver-lift` runs).
Not exercised: `deliver`, `deliver-pause` and `deliver-earlier` were not re-run. Their `pause`, `resume` and `check-in` records did not move, but `deliver` and `deliver-pause` also check a nudge record on the worker's issue, which the changed line now states, and those two checks were not run against it. Real workers, a real Harness and a real tracker. Case check (premium subagent that did not write the cases): the changed check "events 7 to 12": fix, fixed in `578842d` (the three escapes closed: a repeat notice that also names 20-quiet.md, one that names 00-milestone.md, one with no file name); the mention-beside-20 test: keep; the second-notice test: fix, moved to event 10 with three escape tests added; the `SKILL.md` line: keep, covered by the existing nudge-record checks (events 4 and 9) and the park-record check. Lessons: none.

### 2026-11-04, commit `0027423` (`ticket-638`), dev-skills 0.61.0 (unbumped): the five delivery dry runs after Ticket #638

Run level: decision-level in a subagent
Runner: the coordinator. One fresh premium-tier subagent per case was given only the prompt text between the `---` lines, with `<checkout>` set to a `git archive` copy of `0027423` with `evals/` removed.
Ran: `score.py` on each case. Evidence: [`evidence/638/`](evidence/638/), one folder per case with `proposed-actions.md` and `score.txt`. In the copied evidence, the run directory's path reads `<runs>` and model names read `<model>`, so that the `vendor-model` check in `scripts/check-plugin.sh` passes. The scores were rerun on the edited files and are unchanged.

| Case | Score |
| --- | --- |
| `deliver` | 33/33 |
| `deliver-pause` | 20/20 |
| `deliver-earlier` | 7/7 |
| `deliver-stall` | 27/28: FAIL "events 7 to 12: nothing written for 10 and the user not told of it again" |
| `deliver-lift` | 36/37: FAIL, the same check |

In both failing branch runs, the event 11 message to the user about parking 20 says "With 10-farewell.md also parked, nothing more in Release 1 can start". It names 10 again, so the check fails, although the sentence gives the context for why delivery waits rather than a second notice about 10.

**Baseline on main.** The coordinator ran the same two cases on main's skills. Each fresh premium-tier subagent got the branch fixture (built with `b3134cc`'s `make-fixture.sh`) and a `git archive` of main `c29d3b1` (0.61.0), and was scored with the same `score.py`. Evidence: `evidence/638/main-deliver-stall/` and `evidence/638/main-deliver-lift/`, redacted the same way, with the scores rerun on the edited files and unchanged.

| Case | Main | Main's failures |
| --- | --- | --- |
| `deliver-stall` | 26/28 | "event 4: one nudge record on 10-" and "event 9: one nudge record on 20-": the run put both nudge records on the Milestone issue |
| `deliver-lift` | 34/37 | the same two nudge checks, and "events 7 to 12: nothing written for 10 and the user not told of it again" |

The check the branch runs fail also fails on main, and the steps involved are unchanged in #638's diff. The park line of "Replace a stalled worker" and the scorer are untouched. The audit-trail line kept its "(on the Milestone issue)" and lost only "or the release issue with no Milestone". So the branch's stall and lift FAILs are **Pre-existing**. They come from model variance on a wording-strict check and from an ambiguous record location, not from #638.
Pass: no for `deliver-stall` and `deliver-lift` on the branch (one Pre-existing check each, read above); yes for the other three. Not exercised: real workers, a real Harness and a real tracker. Follow-up, outside #638: (1) the scorer's "user not told of 10 again" check counts a mention of 10 inside another notice as a second notice; (2) team-lead's audit-trail line lists `nudge` among the records posted "on the Milestone issue", while the scorer and `snapshot.py` look for a nudge record on the worker's issue.

### 2026-11-04, branch `ticket-638` off `006570d`, dev-skills 0.61.0 (unbumped): Ticket #638, the lone-Release path removed

Run level: no model session (unit tests)
Runner: the Implementer subagent of Ticket #638, by script.
Ran: `test_snapshot.py` (31 tests) and `test_cases.py` (6 tests), both OK. The fixture's Milestone issue lost its `## Boundaries` section (a Milestone issue holds none now); no case or scorer check read it.
Pass: yes, for what ran. The five delivery dry runs, owed when this entry was written, are in the entry above (`0027423`).

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
