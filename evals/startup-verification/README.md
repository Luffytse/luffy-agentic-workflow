# startup-verification eval

Checks of the `milestone` skill's **Startup verification** reuse rule: a row of the Harness check passed in the last result on an earlier Milestone issue is linked instead of re-run, while the Harness and every Runtime-line field match, `worker-control`'s reference for the Harness is unchanged on main since the result was posted, the result is under 30 days old and no failure of that capability was recorded since; **Loaded skill version** always re-runs. The loaded-skill-version probe itself and the real-environment runs of the check are recorded in [RESULTS.md](RESULTS.md); the Harness check is `worker-control`'s ([`../worker-control/`](../worker-control/README.md)).

## Run level and tier

*Decision-level in a subagent*, **regular** tier (the tier Startup verification runs at): a fresh subagent is given the skill text and the fixture's records, decides which rows to run, and writes the comment it would post, assuming every probe it runs passes. No worker starts and no tracker is called, so what a real probe would show is not exercised.

## Cases

[`make-fixture.sh`](make-fixture.sh) builds `<out-dir>/records` (an earlier `## Startup verification` result with seven passing rows, the Harness and Runtime line now, the commit history of the Harness's reference, the failures recorded since) and `<out-dir>/PROMPT.md`: `bash evals/startup-verification/make-fixture.sh <out-dir> <case>`. Today is 2026-11-09 and the earlier result was posted 2026-10-20 (20 days) unless the case says otherwise.

| Case | What differs | Expected: rows run now |
| --- | --- | --- |
| `same` | same Harness and Runtime line, reference unchanged since the result, no failure recorded | only Loaded skill version; the other six reused, each Evidence `reused from` the earlier result's link |
| `runtime` | permission mode now differs from the earlier result's | all seven |
| `reference` | the Harness's reference changed on main after the result was posted | all seven |
| `old` | the earlier result is 45 days old | all seven |
| `failure` | a Retro since records a failure of Confirmed stop | Confirmed stop and Loaded skill version; Start a worker and Worker state may be marked either way (re-running Confirmed stop needs a probe worker), the other three reused |
| `failedrow` | the earlier result's Scheduled check-in row failed (Essential `not relied on`, Result `fail`, Evidence `no arrival by 11:05`) | Scheduled check-in and Loaded skill version; the other five reused |

## Running it

1. Build the case into a scratch directory outside this repo.
2. Start a **fresh** regular-tier session (load `model-tiers` for the model), give it only the text between the `---` lines of `<out-dir>/PROMPT.md` with `<checkout>` replaced by the checkout under test (for the baseline, a `git archive` of main). Keep this README, `score.py` and `test_score.py` away from it.
3. Score it: `python3 evals/startup-verification/score.py <out-dir> <case>`. One line per check; exits 1 when any fails. It reads `.scratch/result.md`; if the run cannot write it, the thread writes the run's returned text there first ([evals guide](../../docs/dev-skills/evals.md#making-model-runs)). Read the comment too: the scorer checks the Evidence cells, the link, a reused row's Result staying `pass` and the clause that says which rows run now (in the Run line or a line of its own; `all`, `every row` or `all seven` counts for every row), not the Limits.

After changing `score.py` or `make-fixture.sh`, run `python3 evals/startup-verification/test_score.py`: it builds every case, scores a hand-written reference result (which must pass) and planted wrong ones (everything re-run when rows may be reused, a reused row whose Result is not pass, Loaded skill version reused, reused rows with no link, a Run line naming no rows, a row reused whose conditions fail, one row too many re-run), each of which must fail. It also reads each built fixture's rendered records and asserts the case's condition holds or fails there (`runtime`: the Runtime line differs; `reference`: the newest reference commit is later than the posted date; `old`: posted 30 or more days before 2026-11-09; `failure`: the recorded failure names Confirmed stop; `failedrow`: the Scheduled check-in Result is not pass; `same`: all five conditions hold). `scripts/run-tests.sh` runs it.

Main's text has no reuse rule and its Run line names no rows. `same`, `failure` and `failedrow` are expected to fail on main for re-running every row. `runtime`, `reference` and `old` expect every row re-run, which main does, so they are expected **regression guards** on the changed condition (the reuse rule must not apply there): main fails them only at the run-now clause, and the case check records them as such.
