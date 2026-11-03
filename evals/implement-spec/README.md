# implement-spec eval

Build-flow checks of `implement-spec`. Each run gets an entry in [RESULTS.md](RESULTS.md).

## Merge-authority check

**Run level**, as in [`implement`'s README](../implement/README.md#run-level): the six merge-authority cases are decision-level in a subagent (from step 8) or full build-flow in a top-level session (a session that can start the Implementers and the reviewers); the three membership cases are decision-level in a subagent only. Record the level in every RESULTS entry.

The same check as `implement`'s ([its README](../implement/README.md#merge-authority-check)), for the Spec thread's step 8: one merge rule for every Spec pull request, whether the Spec carries a Milestone label or not (the label only decides whether a Milestone issue's boundaries apply); the Spec pull request's Door is one-way if any ticket's is; only the Spec pull request bumps; the `Agent-merged rules:` line is written in the body on every agent merge that changes a rules file or carries a design answer, and step 9's report names the same items.

Build each case with the `spec` flow: `bash evals/implement/merge-authority/make-fixture.sh <out-dir> <case> spec`. The work issue `.scratch/issues/10-work.md` is then a Spec (`Type: spec`) with two tickets, `11-code.md` (the code and test) and `12-adr.md` (the ADR, blocked by 11); only the Spec carries the Milestone label. Run, score and record it as `implement`'s README says (a decision-level run starts at step 8 and lists steps 1 to 7 as not exercised), with the Spec thread's prompt from `<out-dir>/PROMPT.md`, and the same six cases and Expected lines: `no-milestone`, `inside-deep-adr`, `inside-boundary`, `outside-boundary`, `no-record-twoway` and `no-record-oneway`. The shared fixture also has the corrective-check membership decisions described in that README: run all three additional cases (`retro-inside`, `retro-outside`, `unrelated-no-issue`) with `spec`, whose membership source is the originating Spec, not its child Tickets; under the one rule all three end in a merge by the thread, listed on the `Agent-merged rules:` line. The fixture test (`bash evals/implement/merge-authority/test-fixture.sh`) also checks that both skills name that line and that `implement-spec` keeps no inside/outside merge list.

## Evidence-owner check

See [`implement`'s README](../implement/README.md#evidence-owner-check); the case applies to the Spec thread's steps 3 and 4. Model-run results: owed.

## Mixed-agent check

**Run level**: decision-level in a subagent. Case files in [`mixed-agent/`](mixed-agent/): `SPEC.md` (a Spec whose ticket 42 carries the other agent's label and blocks 43), `PROMPT.md` (the Spec thread writes what it does in five scenarios: mixed-agent siblings, a closed Spec with an open ticket, a same-agent Spec, re-entry after a foreign ticket landed, no authorized dispatch; then the other agent's worker side), `EXPECTED.md` (pass and fail per scenario; keep it away from the session under test) and `test.sh`, which checks the files exist and that `implement-spec`, `implement`, `team-lead` and ADR 0005 carry the continuation mechanism. Give the subagent `implement-spec`, `implement` and `team-lead` from the checkout, `SPEC.md` and `PROMPT.md`, and score its answer against `EXPECTED.md`. Model-run results: owed.
