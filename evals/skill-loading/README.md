# Skill dependency loading check

Run this manual behavioral check before migrating shared contracts, and after changes to dependency loading. Use [RESULTS.md](RESULTS.md) for dated outcomes, exact source/runtime identity and limits. This tests fresh-runtime discovery, by-name loading and actual application; packaging checks alone cannot pass it.

## Install the candidate

Follow the isolated-home/authentication and GitHub installation procedure in [the install check](../codex-install/README.md), selecting the current remote Spec ref and recording the immutable SHA actually fetched. For #360 the ref is `codex/spec-348-shared-base`. Require the actual candidate containing #363, not a live or copied published cache. Start with an empty home and preserve the live installation. Compare the installed plugin files with the fetched source, recording mismatches before running any session.

Use the regular Codex tier from the candidate plugin README, provider `openai`, with fallback disabled. Every runtime uses the same isolated `CODEX_HOME`; each case has a separate fixture directory and new app-server process. Supplementary fixtures live outside the installed plugin cache. Copy only the relevant folder(s) from `fixtures/` into each case's `.agents/skills/`.

## Workflow case

Copy `gate-interview/`. Start a fresh app-server and discover skills using `skills/list`, `forceReload: true`, with the case's absolute cwd. Compare installed plugin names against the source skill folders, normalizing `dev-skills:`; record errors and disabled/missing/unexpected skills. Select the discovered `gate-interview` path.

Use the [install check's app-server protocol](../codex-install/README.md#run-the-interview-to-completion): experimental initialize, `thread/start` with an ephemeral thread, recorded model, `allowProviderModelFallback: false`, approvals `never`, then `turn/start` with one text item and one skill item for the **caller only**. Use `sandbox: "read-only"` for interview-only reruns; the recorded run used `workspace-write`, with no writes observed. Initial text is the first user turn in [workflow.txt](workflow.txt). The caller names `dev-skills:grilling`; the evaluator must not inject the dependency's body or skill item. Observe the assistant actually reading/loading its installed body.

Answer the assistant's actual questions as the simulated user; the transcript is a worked example, not a fixed-output assertion. Include a changed recommendation, a missed-session policy, success criteria and explicit final confirmation. Pass when the dependent workflow asks/recommends/waits, carries decisions forward, asks for shared-understanding confirmation and receives it, then closes. Record exact turns, statuses/errors, tool actions and fixture writes. EOF before confirmation is incomplete. Unavailable tools or policy deviations must be reported independently.

## Focused reference case

Copy `gate-caller/` and `gate-contract/` to a second fixture, then start a new runtime. The contract uses the candidate's supported Base-skill shape: `user-invocable: false`, no disable-model-invocation, and `agents/openai.yaml` with implicit invocation true. This supplementary fixture is project-scoped; it tests named dependency loading without waiting for production contract migrations.

Select only the discovered `gate-caller` in the first turn. Use the first user turn in [reference.txt](reference.txt). The prompt, caller and contract description do not supply the acceptance rule. Require discovery of the contract, an observable body read, and correct classification: R11 then R2 accepted; done, pending, absent and wrong-prefix receipts excluded, priority ignored. Score meaning and ordering, not an exact sentence.

Report model discovery/loading/application separately from user-menu hiding. `skills/list` availability and display metadata prove no menu behavior. If UI visibility is not inspected, say unmeasured; it cannot alone block migration. This run does not establish that Claude's `user-invocable` flag hides a Codex menu item.

## Existing cross-folder references

In a third fresh runtime select the installed production `dev-skills:grill-with-docs` caller only, using the first user turn in [production-composition.txt](production-composition.txt). Authorize fixture-only documentation writes, then answer the actual interview through explicit confirmation. Check installed sibling dependency reads, including the caller's by-name `docs-index` load for documentation writes. Observe resulting glossary and index links, rather than accepting the assistant's claim that it read the rule. Retain any unrelated workflow limitation; this does not certify every branch of those workflows.

## Evidence and cleanup

Preserve exact user/assistant turns plus completed tool commands, statuses and relevant outputs, source/cache provenance and discovery. The committed JSON tool summaries retain only the first 300 output characters and explicitly flag truncation; they exclude reasoning, authentication and transport metadata. The transcript paths are sanitized placeholders. `production-output/` contains observed generated test data, not project guidance.

If required loading or application fails, keep downstream migrations blocked; record the limitation and arrange the tracker follow-up before calling the gate passed. Optional visibility and unrelated unexercised branches do not establish such a failure. Stop app-server processes and remove temporary authentication and raw runtime material after safe evidence is saved. Run repository checks, Claude plugin validation and whitespace validation; no screenshot is needed for this protocol/text seam. Before the final Spec leaves draft, repeat the separate clean-install check against the then-current remote Spec tip; the SHA in this directory is an earlier gate candidate.
