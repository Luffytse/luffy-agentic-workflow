# Testing a skill change

How this repo tests a change to skill text: three layers, each with its own job, and the eval rules every build thread follows (Spec #626, [ADR 0013](adr/0013-skill-changes-are-tested-by-ci-evals-and-review.md)). Read it before opening a pull request that touches `plugins/dev-skills/skills/` or `evals/`. It applies from the commit that adds it: runs that a `RESULTS.md` entry written before it lists as owed are history and stay as written.

## The rule in the plugin

`tdd` and the Implementer briefs of `implement` and `implement-spec` carry one project-independent line: when the change is instructions for an agent (a skill, a prompt, an agent instructions file), its test is an eval, not a grep for a sentence, compared with the default branch's version and scored by scripts first, and the repo's own docs say how to run one; the Implementer chooses that seam without the user and reports the eval run, or its stated gap, as evidence instead of a failing-then-passing code test. This guide is the repo's own doc it points to. The case that tests the rule is the [eval-test check](../../evals/implement/README.md#eval-test-check).

## Three layers

- **CI**: questions with one right answer from the files, answered by a script with no model, on every pull request. The workflow runs `scripts/check-plugin.sh` and `claude plugin validate .`; every deterministic test (fixture self-tests, scorer tests, the checker's own tests) is run by `scripts/run-tests.sh`, which finds each `test*` file under `evals/` and `scripts/` by its name (Ticket #627). The workflow step that calls it is committed by hand, and until it is in the workflow CI does not run those tests, so run `scripts/run-tests.sh` before pushing. A check tests structure, never a skill's wording, so rewording a skill never fails CI.
- **Eval**: what a skill makes an agent do. A fresh agent runs the skill on a fixture; its output is scored by scripts first, and by a judge only for what scripts cannot see. Each skill's cases live in `evals/<skill>/`, whose README names each case's run level and tier.
- **Review**: judgement on the text, by `agentic-review` with this repo's [REVIEW.md](../../REVIEW.md). It reviews eval files like any other file.

**Sorting rule.** If a script can catch it, it is CI; if you must watch an agent use the skill, it is an eval; if it needs reading for meaning, it is review. A Bug class that keeps coming back moves to the cheapest layer that can catch it.

## When a run is due

Sort the pull request into one kind, and name the kind on an `**Eval:**` line of its body:

- **behaviour change**: it changes what an agent following a skill does (a step, a condition, a record it writes, a default, who does what). A run is due.
- **wording-only** (the skill's behaviour stays the same), **docs**, **ADR** or **eval-only** (`evals/` alone): no run; the `**Eval:**` line names the kind and that is all.

A pull request that is unsure, or mixes kinds, is a behaviour change.

For a behaviour change, run the changed skill's cases (its eval README says which cases cover which rules) twice: on the pull request's skill and on main's, the **baseline**, taken from a `git archive` of main. Record both runs in the eval's `RESULTS.md` with the commit, plugin version, tier and run level, and link the entry on the `**Eval:**` line. The pull request's run passes; main's run shows what the change moved.

## No owed runs

A pull request merges with its runs made. The one allowed gap is a run that **cannot be made** from where the thread runs (a case whose run level needs a top-level session, a real Harness or a tool the thread does not hold), stated with its reason on the `**Eval:**` line and in the `RESULTS.md` entry. Time and cost are not reasons.

An Implementer that reports a criterion as owed to its thread (ADR 0004's evidence owner) is handing the run over, not leaving a gap: the thread makes that run before the pull request opens or the Ticket lands.

## A behaviour change to a skill with no eval

Add one small case in `evals/<skill>/`: a README naming its run level and tier, the fixture prompt, and a scorer or an `EXPECTED.md`. The case fails on main's skill and passes on the pull request's, and both runs are recorded as above. A case that is hard to write (a planning or interview skill, where the behaviour lives in a conversation with the user) is the stated gap: the `**Eval:**` line says why.

A real gap that one of the review's completeness checks of the text finds (the two [REVIEW.md](../../REVIEW.md) Always check lines on fields, conditions and rerun states) also adds an eval case for that path, in the pull request that fixes it; if no case can be written, that is the same stated gap.

## Case check

Each new case, and each changed expected result (an `EXPECTED.md`, a scorer's expected values, a case's stated meaning), is checked after it is written and before any model run. A fresh **premium**-tier subagent that did not write it reads the whole skill folder, its workflow (the skills it loads and the skills that load it on that path) and the case files, and returns **keep**, **fix** or **drop** for each case, on three questions:

- **valid**: the prompt and fixture test what the case's meaning says, and the expected result is what the skill text gives;
- **fails on main for the right reason**: main's skill gets it wrong because of the rule the pull request changes, not because of the fixture (for a changed expected result: it changed because that rule changed);
- **needed**: no existing case already covers it.

A case marked fix is fixed and checked again; a case marked drop is removed. Each case's verdict goes in the pull request body. The Review still reviews the eval files as usual.

## Making model runs

Start fresh subagents in **one parallel batch** of agent calls: one call per case per skill version, the pull request's and main's, all sent together. Give each the checkout's skill text (the branch's, or main's from the archive; never the installed plugin cache), the case's fixture prompt and whatever else the eval's README says it gets, nothing more, at the tier the eval's README names; keep `EXPECTED.md` and the scorer away from it. Score each output with the eval's scorer. No workflow script is needed. The eval's README says how to build each fixture and how to score it; where it says a fresh session, a fresh subagent does unless its run level needs a top-level session. A subagent run is decision-level; a case its README marks as needing a full build-flow in a top-level session is the stated gap above unless the coordinator makes the run.

## Fixture self-tests

A fixture builder's self-test checks that each case's **rendered input** (the files the agent reads, such as a `SPEC.md`) says what the case's meaning says, not only that the builder's internal fields are set. Retro #606 is the origin: the `to-tickets-agent-label` case `inherited` passed its self-test while its rendered Spec still described the other runtime, and only a model run showed it. A new fixture builder carries this check, and an existing one gains it when it next changes.
