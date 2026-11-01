# Review record interpretation fixture

The seam is the persisted comment record consumed by review continuation and retro. This fixture preserves existing behavior while the owner moves; it does not test review orchestration or preventive-check selection.

## Producer and consumer inventory

| Consumer | Needs | Kept with workflow |
| --- | --- | --- |
| agentic-review/SKILL.md continuation | Markers, current IDs, Severity/status and prior locations | Diff selection, depth, open-Important verification |
| agentic-review/ROUNDS.md writer | Comment shape, immutable IDs, status and Note semantics, filing receipts | Rank matching, caps, fix timing, posting, Round loop and filing |
| agentic-review/FINDERS.md standards brief | Bug class and Always-check meaning | Whole-diff checks, each-line reporting, Finding format |
| retro/BUG-CLASSES.md reader | Included comments, latest state, historical locations and dismissal interpretation | Class-name aggregation, repeated-instance count, guardrail choice and PR work |
| evals/agentic-review/briefs.sh | Candidate contract meaning when constructing standards briefs | Eval-only brief generation |

The base loads no workflow. Review and retro explicitly load it by name where they need record meaning. VERIFY.md, default Important and Finding format stay in their existing owners. Build callers still use the review workflow; their separate migration is #366.

## Run

Copy comments.json into a fresh isolated directory. Keep expected.json outside the agent's directory. Use the isolated-home, fresh app-server procedure in [skill-loading](../skill-loading/README.md), regular tier, provider openai and provider fallback disabled. For a baseline, supply the original ROUNDS.md and BUG-CLASSES.md from the recorded source SHA. For a candidate, copy only review-record into .agents/skills/review-record and discover it with skills/list. Send prompt.txt, adding “First read ROUNDS.md and BUG-CLASSES.md for the existing record rules” for baseline or “First load the review-record skill by name and apply its contract” for candidate. Do not supply the expected answer or the candidate's body in the prompt. Require an observed body read, completed turn and no mutation.

Save the actual JSON response, then run `python3 evals/review-record/score.py <answer.json>`. The scorer compares semantic fields and unordered location/ID sets against a worked expectation, not instruction prose. The inputs cover a Ticket check and three Rounds, repeated IDs, escalation from Nit, partial and full fixes, omitted IDs, historical location accumulation, a false-positive dismissal, skipped Nit, kept design, merged row and a filing receipt. Merged-away IDs are omitted from retro; their locations survive under the holding ID. The filing receipt leaves the Pre-existing row open.

## Observed 2026-10-31 (America/Los_Angeles)

Baseline: existing owners at Spec commit 8ff823f913b951cb3c48b476ec1eda08c35d4601. Candidate: local review-record extraction, SHA-256 `5788a29f66ce2b2361d32f22290fee1e2454fad7d9cc2b20159572745f0cdd80` for SKILL.md; local project-scoped skill, not a clean installed-plugin claim. Both fresh isolated Codex CLI `0.166.0-alpha.5.1` app-server sessions used the regular Codex tier from the [pinned source table](https://github.com/Luffytse/luffy-dev-skills/blob/8ff823f913b951cb3c48b476ec1eda08c35d4601/plugins/dev-skills/README.md#model-tiers), provider openai, fallback disabled, ephemeral threads, read-only sandbox and approvals never. Both completed and matched every expected field. Candidate discovery found the enabled review-record metadata, and the tool trace records its actual body read. The saved answer/evidence pairs retain the complete responses and tool commands/statuses; discovery evidence is scoped to the contract, with unrelated system skills and runtime transport omitted. Temporary authentication was removed after each process stopped.

This is a passing baseline/passing candidate preservation check, not a claimed failing-before/fixed-after bug test. No workflow or issue was started by these probes. Menu visibility is unmeasured. Full Standard/Deep review fixture evals and clean installed-runtime validation remain the Spec coordinator's gates.

Validation initially caught literal vendor model names in evidence; changed only their representation to the immutable tier-table reference, consistent with the earlier loading eval.
