# Results

One entry per run of the `merging` cases, newest first. Record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`, the run level ([README](README.md#run-level)), and whether the skills came from the branch or from main. An entry written inside an open pull request names the commit it ran on as its base; what happens after it is recorded on the pull request.

## Template

```
### <date>, commit <sha>, dev-skills <version>, <branch's | main's> skills

Run level: no model session | decision-level in a session
Setup: <case, how the fixture was built, how the session was driven, its tier>
Score: <score.py's output, one line per case>
Not exercised: <what this run did not reach>
Pass: yes | no. Lessons: <what to change in merging or its callers, if anything>
```

## Runs

### 2026-11-09, commit 6010e31 (branch claude/project-thread-vcuew8), dev-skills 1.2.0 (no bump yet), branch's skills and main's: #53 `no-closes` case

Run level: decision-level in a session
Setup: case `no-closes`, fixtures built by `make_fixture.py`; one fresh premium-tier subagent per side, given only the prompt. The branch's skills were the checkout at `6010e31`; main's were a `git archive` of `origin/main` at `28f99ba`. Main's subagent could not write `.scratch/report.md`, so the thread wrote its returned report text there before scoring ([evals guide](../../docs/dev-skills/evals.md#making-model-runs)). Case check: a fresh premium-tier subagent that did not write the case returned `no-closes` keep.
Score: branch 13/13 PASS, main 13/13 PASS: both runs edited the body to add `Closes #10` before the squash, the squash message carried it, and #10 was closed after the merge. Self-test: `python3 evals/merging/test_cases.py`: OK, 6 cases, 48 scored runs.
Not exercised: a full build-flow in a top-level session; the `release` and `implement-spec` callers.
Pass: yes. `no-closes` is a **regression guard** (a rule main's text already passes): main's `implement` step 5 and `pr` already tell the thread the body closes the issue, so main's run re-adds the line, and no other reason for main to pass is left to remove from the fixture. The guard protects `merging`'s new step 3 from being lost. Lessons: none.

### 2026-11-04, main `9d1de32`, dev-skills 0.80.0 (no bump), main's skills: #695 case check of the cases and `approval` rerun

Run level: decision-level in a session (the run); no model session (the self-test)
Setup: the premium case check of Spec #626, by a fresh premium-tier subagent that did not write the cases. It read the `merging` skill folder, its callers and the case files and returned: `no-record` keep, `review-md` keep, `reported-not-merged` keep, `release-bump` keep, `approval` **fix**, `no-release-doc` **drop** (it duplicated `no-record`: both build the same farewell pull request with no release doc and expect a merge with no bump). All six are **regression guards**: main before `merging` had `implement` step 7 holding every rule (the README says both runs score the same), so "fails on main" is waived for them under the guide. Fixes made: `approval` no longer requires the report to name the Boundary record (the skill asks for the action as the record lists it) and accepts "deleting" as well as "delete"; `no-release-doc` is removed from `cases.py`, the README and the self-test (`release-bump` is now paired with `no-record`); `score.py` accepts a bold or backticked `Agent-merged rules:` line; the self-test gained the rendered-input check (Boundary record or none, migration and deploy rule, `REVIEW.md` change, `deploy/` rule and the reported-merge prompt, release doc, `VERSION`). A second fresh premium check after the fixes returned keep for all five, with three small follow-ups, all made.
Score: `approval` rerun on main's skills (one fresh premium-tier subagent, `<checkout>` a `git archive` of `origin/main` at `9d1de32`) with the final `score.py`: 6/6 PASS, nothing merged or closed, the boundary named. Its `report.md` write was refused (#694); the thread wrote the subagent's final message there before scoring. Evidence: [`evidence/695-approval/`](evidence/695-approval/). Self-test: `python3 evals/merging/test_cases.py`: OK, 5 cases, 37 scored runs.
Not exercised: the other four cases were not rerun (their scorers changed only in the markup tolerance); the `release` and `implement-spec` callers (`implement-spec`'s merge-authority runs are in its own RESULTS).
Pass: yes. Lessons: the stated gap the check found: no case runs an empty record with a one-way Door apart from `implement`'s `no-record-oneway`.

### 2026-11-04, commit ad8ab26 (the Spec branch, claude/project-thread-vk76z1), dev-skills 0.62.0 (no bump yet): #642 six cases, branch's and main's skills

**Superseded 2026-11-04 (Ticket #695):** the premium case check of Spec #626 is in the first entry of this file.

Run level: decision-level in a session.
Setup: each of the six cases (`no-record`, `approval`, `review-md`, `reported-not-merged`, `no-release-doc`, `release-bump`) ran twice, on fresh dry-run fixtures built by the evals' own `make_fixture.py` into a scratch runs directory: 12 runs, each a fresh premium-tier subagent given only the prompt text. The branch's skills were a `git archive` of the `plugins/` folder at `ad8ab26`; main's were a `git archive` of `origin/main` at `9367726`, where `implement` step 7 holds the rule itself.
Score: `score.py` exit 0 on all 12 runs, every check PASS. Passing checks per run, the same on both sides, as the README predicts: `approval` 7, `no-record` 11, `no-release-doc` 11, `release-bump` 16, `reported-not-merged` 6, `review-md` 13.
Not exercised: the premium case check of Spec #626 (not landed; still owed); a full build-flow in a top-level session with real tracker writes; the subagents' own reports, read only through `score.py`'s report text checks; the `release` and `implement-spec` callers of `merging`.
Pass: yes, decision-level. Lessons: none. The branch's `merging` skill and main's `implement` step 7 gave the same scored behaviour in all six cases.

### 2026-11-04, branch `ticket-642` off `9367726` (the Spec branch, claude/project-thread-vk76z1), dev-skills 0.62.0 (no bump): #642 new cases, self-test, model runs recorded above

**Superseded 2026-11-04 (Ticket #695):** the premium case check of Spec #626 is in the first entry of this file.

Run level: no model session.
Setup: `python3 evals/merging/test_cases.py`, which builds all six cases with `make_fixture.py` and scores a reference run and planted wrong runs for each.
Score: `OK: 6 cases, 46 scored runs`: every reference run passes, and every planted wrong run (34) and every real-write run (6) fails, each on the check it plants (`-v` lists them).
Not exercised: everything a model run covers; the model runs are recorded in the entry above. Still owed: the premium case check of Spec #626 for each case, once #626 lands.
Pass: n/a (self-test only). Lessons: none yet.
