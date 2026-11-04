# implement-spec eval

Build-flow checks of `implement-spec`. Each run gets an entry in [RESULTS.md](RESULTS.md).

## Merge-authority check

**Run level**, as in [`implement`'s README](../implement/README.md#run-level): the six merge-authority cases are decision-level in a subagent (from step 8) or full build-flow in a top-level session (a session that can start the Implementers and the reviewers); the three membership cases are decision-level in a subagent only. Record the level in every RESULTS entry.

The same check as `implement`'s ([its README](../implement/README.md#merge-authority-check)), for the Spec thread's step 8, which loads `merging` (the rule is `merging`'s; the cases are its [own eval](../merging/README.md), here run through the Spec thread): one merge rule for every Spec pull request, whether the Spec carries a Milestone label or not (the Boundary record applies as written; a Milestone issue holds no boundaries of its own); the Spec pull request's Door is one-way if any ticket's is; any bump is the release doc's merge-time step, taken for the Spec pull request only; the `Agent-merged rules:` line is written in the body on every agent merge that changes a rules file or carries a design answer, and step 9's report names the same items.

Build each case with the `spec` flow: `bash evals/implement/merge-authority/make-fixture.sh <out-dir> <case> spec`. The work issue `.scratch/issues/10-work.md` is then a Spec (`Type: spec`) with two tickets, `11-code.md` (the code and test) and `12-adr.md` (the ADR, blocked by 11); only the Spec carries the Milestone label. Run, score and record it as `implement`'s README says (a decision-level run starts at step 8 and lists steps 1 to 7 as not exercised), with the Spec thread's prompt from `<out-dir>/PROMPT.md`, and the same six cases and Expected lines: `no-milestone`, `inside-deep-adr`, `inside-boundary`, `outside-boundary`, `no-record-twoway` and `no-record-oneway`. The shared fixture also has the corrective-check membership decisions described in that README: run all three additional cases (`retro-inside`, `retro-outside`, `unrelated-no-issue`) with `spec`, whose membership source is the originating Spec, not its child Tickets; under the one rule all three end in a merge by the thread, listed on the `Agent-merged rules:` line. The fixture test (`bash evals/implement/merge-authority/test-fixture.sh`) also checks that both skills name that line and that `implement-spec` keeps no inside/outside merge list.

## Closing check

**Run level**: decision-level in a session (every tracker, pull request and git write is a block in `.scratch/proposed-actions.md`). Only landed Tickets and the Spec close after the merge; a dropped Ticket stays open. [`closing/`](closing/) holds a fixture builder (`make_fixture.py`: Spec 20, Tickets 21 and 22 landed on `spec-20`, Ticket 23 dropped by the user but still in the Spec pull request's `Closes` lines), the Spec thread's prompt (`PROMPT.md`, written into the output directory), a scorer (`score.py`) and a self-test (`test_cases.py`). The expected behaviour: step 8 removes Ticket 23's line from the body just before the merge (the fixture's body still carries it, as when a Ticket is dropped while the pull request waits); then the merge is a merge commit titled with the pull request's typed title; only after it are #20, #21 and #22 closed as completed, naming the pull request; #23 is never closed. It scores behaviour on the dry-run blocks, never the skill's sentences.

1. `python3 evals/implement-spec/closing/make_fixture.py <out-dir>`.
2. Start a **fresh** premium-tier session (load `model-tiers`) in `<out-dir>/repo` with the text of `<out-dir>/PROMPT.md` between its `---` lines, `<checkout>` replaced by the checkout under test. Keep `closing/score.py` and `test_cases.py` away from it.
3. `python3 evals/implement-spec/closing/score.py <out-dir>`. Run it twice on fresh fixtures, on the branch's skills and on main's (a `git archive` of main). Record both in [RESULTS.md](RESULTS.md).

`python3 evals/implement-spec/closing/test_cases.py` (add `-v`) scores a reference run, which must pass, and planted wrong runs, each of which must fail: the dropped Ticket's line left in the body, no body edit, the dropped Ticket closed (completed or not planned), a landed Ticket or the Spec left open, a close before the merge, a squash, the tracker's default merge title, no merge, and a real file write. It is not a model run.

## Evidence-owner check

See [`implement`'s README](../implement/README.md#evidence-owner-check); the case applies to the Spec thread's steps 3 and 4. Model-run results: owed.

## Mixed-agent check

**Run level**: decision-level in a subagent. Case files in [`mixed-agent/`](mixed-agent/): `SPEC.md` (a Spec whose ticket 42 carries the other agent's label and blocks 43), `PROMPT.md` (the Spec thread writes what it does in five scenarios: mixed-agent siblings, a closed Spec with an open ticket, a same-agent Spec, re-entry after a foreign ticket landed, no authorized dispatch; then the other agent's worker side), `EXPECTED.md` (pass and fail per scenario; keep it away from the session under test) and `test.sh`, which checks the files exist and that `implement-spec`, `implement`, `team-lead` and ADR 0005 carry the continuation mechanism. Give the subagent `implement-spec`, `implement` and `team-lead` from the checkout (each skill's whole folder, `implement-spec/continuation.md` included), `SPEC.md` and `PROMPT.md`, and score its answer against `EXPECTED.md`. Model-run results: owed.
