# Skill changes are tested by CI, evals and review, each with its own job

A change to skill text is tested in three layers. **CI** answers questions with one right answer from the files, by a script with no model, on every pull request. An **Eval** shows what a skill makes an agent do: a fresh agent runs the skill on a fixture, scored by scripts first and a judge only for what scripts cannot see, run when a pull request changes how a skill behaves, against main's skill as the baseline. **Review** is judgement on the text. The method lives in this repo's [evals guide](../evals.md); the plugin carries only a short rule. Settled with the user on 2026-11-03 in the planning thread "Plan CI, evals and review for skills" (Spec #626, answering #615).

## Why

Most changes here are skill text, but the checks were built for code. CI ran only the structure checker and `claude plugin validate`, while the deterministic tests that need no model never ran in it (#614). Nothing said what a test is when the change is instructions for an agent, so model runs were left "owed" with no stated way to make them (#606), some tests checked only that a sentence exists in a skill and broke when it was reworded (#618), and a case's self-test passed while the case was wrong (#606).

## Decisions

- **Three layers, one sorting rule.** If a script can catch it, it is CI; if you must watch an agent use the skill, it is an eval; if it needs reading for meaning, it is review. A Bug class that keeps coming back moves to the cheapest layer that can catch it.
- **CI is deterministic only.** Every deterministic test runs in CI (`scripts/run-tests.sh`, Ticket #627; a new test joins by its file name; the workflow step that calls it is committed by hand, and until it is in the workflow those tests run by hand with that script). A check tests structure and banned names, never that a skill holds a given sentence, so rewording a skill fails CI only if it adds a banned name. Model evals do not run in CI.
- **An eval run is due on a behaviour change.** The pull request runs the changed skill's cases on its own skill and on main's, and links the results. A wording-only, docs, ADR or eval-only change skips the run and says which kind it is.
- **No owed runs.** The one allowed gap is a run that cannot be made, stated with its reason. A behaviour change to a skill with no eval adds one small case that fails on main and passes on the pull request; a case that is hard to write is a stated gap. A real gap that a review completeness check of the text finds also adds an eval case for that path.
- **Cases are checked before they are paid for.** Each new case and each changed expected result gets a fresh premium-tier check (keep, fix or drop) before any model run, and a fixture builder's self-test checks each case's rendered input against its meaning.
- **The plugin carries a short rule; the repo holds the method.** `tdd` and the Implementer briefs say only that the test for instructions to an agent is an eval compared with main's version, and that the repo's own docs say how to run one (Ticket #631). Each project tests differently, and the plugin stays project-independent.

## Considered options

- **Run model evals in CI, or rerun every eval on a schedule.** No peer project does this: their CI is deterministic only, and a behaviour change is judged by a run against the old version (peer research, 2026-11-03). Model runs are slow, costly and not repeatable enough to gate every pull request.
- **Keep sentence-presence tests as the test of a skill change.** They break on every rewording and pass when the agent still does the wrong thing.
- **Put the method in the plugin.** It would name this repo's paths, tiers and eval layout in text every project loads.

## Consequences

- `CLAUDE.md` points threads at the evals guide when a change touches skill text, and `docs/dev-skills/index.md` lists the guide and this ADR.
- Runs listed as owed in `RESULTS.md` entries written before the guide are history; making them is out of Spec #626's scope.
- Eval READMEs keep saying which cases cover which rules, the run level and the tier; the guide says when and how a thread runs them.
