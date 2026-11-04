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

### 2026-11-04, branch `ticket-642` off `9367726` (the Spec branch, claude/project-thread-vk76z1), dev-skills 0.62.0 (no bump): #642 new cases, model runs owed

Run level: no model session.
Setup: `python3 evals/merging/test_cases.py`, which builds all six cases with `make_fixture.py` and scores a reference run and planted wrong runs for each.
Score: `OK: 6 cases, 46 scored runs`: every reference run passes, and every planted wrong run (34) and every real-write run (6) fails, each on the check it plants (`-v` lists them).
Not exercised: everything a model run covers. **Owed:** one fresh premium-tier run of each of the six cases on the branch's skills and one on main's (12 runs), scored with `score.py`. The Implementer that wrote this entry could not start a session or subagent to act as the Ticket thread, so none was made. Also owed: the premium case check of Spec #626 for each case, once #626 lands.
Pass: n/a (self-test only; model runs owed). Lessons: none yet.
