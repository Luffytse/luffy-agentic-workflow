# Caller cleanup behavioral evaluation

The approved seam is the selected caller's review handoff and fix coordination, plus its application of configured tracker operations and role-to-label mappings. Use fixture files only; no real issue or PR writes.

Follow the isolated-home authentication, local candidate installation and fresh app-server protocol in [issue absorption](../issue-absorption/README.md) and [skill loading](../skill-loading/README.md). Each case gets an empty home and a copy of `fixture/`. Install the source with `codex plugin marketplace add <absolute-checkout>` and `codex plugin add dev-skills@luffy-dev`. This is a local-source check, not a GitHub install.

For the baseline, archive the recorded pre-migration commit, install it and select only `dev-skills:implement`. For each candidate case select only its named caller using the path returned by `skills/list` with forceReload. Send the retained `prompt.txt`; do not inject review bodies. Use a fresh ephemeral runtime, the regular tier, explicit provider `openai`, fallback disabled and fixture workspace-write access. Run app-server with network inference access; the fixture itself must not call the real tracker.

Score behavior, not exact prose:

- Baseline and both builders: exactly one finish operation, for T3 with delivered/PR-77; T4 gets no duplicate close. T1 remains a blocker because its receipt is missing despite closed state; T2 clears.
- `implement`: observable loading of the installed review workflow; route both text fixes to existing Implementer A and return commits/evidence. Continue review, handle final text Nit timing and an agreed design change differently, and bring a clean Deep review to the user.
- `implement-spec`: load the installed review workflow; choose a new premium Implementer on the Spec branch, keep push evidence and continuation policy, pass prior Ticket-check records including Pre-existing Findings. Preserve Ticket-check worktree/base/depth/destination and the Spec merge-commit policy, with Deep requiring the user.
- `local-completion`: select `implement-spec`; replace initial state with open S1/T1/T2 and declare no PR closing-keyword support in the tracker doc. S1 and landed T1 finish through configured operations; dropped T2 remains open despite there being no PR closing lines.
- `to-spec` and `to-tickets`: create the configured local publication artifact with mapped label `robot-queue`, not a literal role label.

Retain exact turns, completed tool actions, status, discovery, installed file hashes and output artifacts. Remove credentials and raw transport after extracting sanitized evidence. Completed command outputs are truncated at 1500 characters, with a flag; command text and final assistant text are retained. Inspect commands for actual dependency reads and tracker-file writes rather than accepting only claims. Read [RESULTS.md](RESULTS.md) for outcomes and limits. Full review dispatch and integration remain the separate review eval; this is a bounded decision probe, not a whole Review.
