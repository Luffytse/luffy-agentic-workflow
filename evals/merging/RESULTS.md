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

### 2026-11-04, commit ad8ab26 (the Spec branch, claude/project-thread-vk76z1), dev-skills 0.62.0 (no bump yet): #642 six cases, branch's and main's skills

Run level: decision-level in a session.
Setup: each of the six cases (`no-record`, `approval`, `review-md`, `reported-not-merged`, `no-release-doc`, `release-bump`) ran twice, on fresh dry-run fixtures built by the evals' own `make_fixture.py` into a scratch runs directory: 12 runs, each a fresh premium-tier subagent given only the prompt text. The branch's skills were a `git archive` of the `plugins/` folder at `ad8ab26`; main's were a `git archive` of `origin/main` at `9367726`, where `implement` step 7 holds the rule itself.
Score: `score.py` exit 0 on all 12 runs, every check PASS. Passing checks per run, the same on both sides, as the README predicts: `approval` 7, `no-record` 11, `no-release-doc` 11, `release-bump` 16, `reported-not-merged` 6, `review-md` 13.
Not exercised: the premium case check of Spec #626 (not landed; still owed); a full build-flow in a top-level session with real tracker writes; the subagents' own reports, read only through `score.py`'s report text checks; the `release` and `implement-spec` callers of `merging`.
Pass: yes, decision-level. Lessons: none. The branch's `merging` skill and main's `implement` step 7 gave the same scored behaviour in all six cases.

### 2026-11-04, branch `ticket-642` off `9367726` (the Spec branch, claude/project-thread-vk76z1), dev-skills 0.62.0 (no bump): #642 new cases, self-test, model runs recorded above

Run level: no model session.
Setup: `python3 evals/merging/test_cases.py`, which builds all six cases with `make_fixture.py` and scores a reference run and planted wrong runs for each.
Score: `OK: 6 cases, 46 scored runs`: every reference run passes, and every planted wrong run (34) and every real-write run (6) fails, each on the check it plants (`-v` lists them).
Not exercised: everything a model run covers; the model runs are recorded in the entry above. Still owed: the premium case check of Spec #626 for each case, once #626 lands.
Pass: n/a (self-test only). Lessons: none yet.
