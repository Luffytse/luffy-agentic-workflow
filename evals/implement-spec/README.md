# implement-spec eval

Build-flow checks of `implement-spec`. Each run gets an entry in [RESULTS.md](RESULTS.md).

## Merge-authority check

The same check as `implement`'s ([its README](../implement/README.md#merge-authority-check)), for the Spec thread's step 8: membership comes from the Spec's labels, the Spec pull request's Door is one-way if any ticket's is, only the Spec pull request bumps, and step 9's report lists the agent-merged ADR change.

Build each case with the `spec` flow: `bash evals/implement/merge-authority/make-fixture.sh <out-dir> <case> spec`. The work issue `.scratch/issues/10-work.md` is then a Spec (`Type: spec`) with two tickets, `11-code.md` (the code and test) and `12-adr.md` (the ADR, blocked by 11); only the Spec carries the Milestone label. Run, score and record it as `implement`'s README says (a decision-level run starts at step 8 and lists steps 1 to 7 as not exercised), with the Spec thread's prompt from `<out-dir>/PROMPT.md`, and the same three cases and Expected lines.
