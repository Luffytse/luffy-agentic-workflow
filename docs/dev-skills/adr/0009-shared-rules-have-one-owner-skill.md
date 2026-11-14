# Shared rules have one owner skill

A **Shared rule** is one that two or more skills must follow the same way: a record contract, a rule of a workflow they invoke, or a project configuration rule. The revised plan in [#348](https://github.com/Luffytse/luffy-dev-skills/issues/348) gives each one an owner, using complete workflows when they fit and focused **Base skills** for shared contracts. The scoped migrations are implemented; the ownership and consumer inventory below records their boundaries. Existing instructions and protections still govern any shared copies outside this scope.

## Ownership

- **Complete workflows:** a caller runs another skill when it needs that skill's task. The workflow owns its procedures; the caller keeps its surrounding coordination and independent policies. Build skills already run `agentic-review`, which hands its Rounds to `review-rounds`, so review Rounds stay there while assigning fixes, integration and merge decisions stay with the builders.
- **Focused contracts:** when consumers need a small rule that must agree, they load its Base skill by name at the relevant point. The base holds the shared meaning, not the larger workflow that happened to contain it.
- **Project configuration:** tracker operations, label mappings and release settings remain in the project's files. Skills read those files; they hold only rules that fit any project.
- **Independent rules:** similar wording does not require a common owner. Repeated composition is also valid: callers may keep using `grilling` and `domain-modeling` directly, while `grill-with-docs` remains their convenient combined entry point.

The `docs-index` Base skill owns index format and update requirements; its writers and standards Finder load it by name, preserving caller triggers and exceptions (migrated in #364). The `issue-absorption` Base skill owns absorption records and the meaning of completed versus abandoned fixes (migrated in #368). The `review-record` Base skill owns review markers, fields, Finding identifiers, statuses and record interpretation (migrated in #365). The `worker-control` Base skill owns detecting how workers run, one reference per way workers run (what that harness does by itself and the worker methods a coordinator adds, each citing its doc page), the fallback to an unknown harness's own docs and the short check that proves those methods (#527); `milestone`'s Plugin version check loads it only to start its one cheap worker (it once loaded it for Startup verification's probes), and the `team-lead` skill takes every worker lifecycle action through it (ADR 0010). Writers and readers migrate together; callers keep their triggers and exceptions. Review orchestration stays in `agentic-review` and the `review-rounds` skill it hands its Rounds to, and the procedure for turning repeated Findings into preventive checks stays in `retro`.

## Workflow handoff

The `retro-planning` handoff migrated in #369 moves earlier: it selects one problem with the user, then `to-tickets` prepares, discusses and publishes the concrete Ticket. Retro planning keeps the snapshot, order, cap, closes, spin-offs and record, and updates that record before moving on.

The ordinary handoff aims for one complete Ticket. If several are needed, it returns to planning before publication so the larger effort can be spun off, rather than forcing an oversized Ticket or silently raising the cap. Partial publication is reconciled on resume instead of duplicated. The absorption contract and this handoff land separately.

## Considered options

- **Unify look-alike rules:** rejected. Independent Implementer briefs may evolve separately. The merge rule is no longer an example: see the amendment note below.
- **Move all of retro's bug-class reference into a base:** rejected. Reviewers need shared record meaning, not retro's preventive-check workflow.
- **A shared folder outside the skill system:** rejected in favor of named skills, whose loading must be demonstrated rather than assumed.
- **Require hidden menus everywhere:** rejected. Hiding is preferred where supported; model discovery, loading and application are required.

Upstream deliberately separated reusable interview and domain-modeling capabilities from their wrappers ([documented rationale](https://github.com/mattpocock/skills/commit/995fceec7a185754dbc2f32bc9b4f461b14578f2)). Repeated calls to those capabilities do not duplicate their rules.

## Implemented scope and verification

This narrows ADR 0006's rejected separate index skill: the trigger stays with each writer or checker. #363 established authoring guidance and packaging support. #360 passed the required fresh-runtime discovery, loading and actual application gate for complete-workflow and focused-reference dependencies. Its production composition proved reference readability/application, but its reported fact-finding subagent failure was unverified and is not a complete production workflow pass. User-menu hiding was unmeasured and remains optional; visibility is separate from model reachability.

| Owner | Consumers and load point | Migration |
| --- | --- | --- |
| `docs-index` | Document writers (`domain-modeling`, `grill-with-docs`, `improve-codebase-architecture`, `research`, `retro`, `setup-dev-skills`, `triage`, including their supporting-file branches) at index updates; `review-rounds/FINDERS.md` standards branch when checking the index | #364 |
| `review-record` | `review-rounds` before reading/writing comments and briefing Finders (`agentic-review` writes Round 0's one-line None record inline, in the shape `review-record` gives); the standards Finder, `retro` (step 3 loads it by name) and the `retro/BUG-CLASSES.md` reader apply its record meaning | #365, Spec #555 |
| `issue-absorption` | `to-tickets` before source-based drafting/publication; `retro-planning` before lifecycle classification and absorption; `pr` when selecting closing lines; builders when maintaining lines or completing absorbed sources | #368 |
| `to-tickets` complete workflow | `retro-planning` after problem approval, including publication repair on resume; planning retains budget, order and record ownership | #369 |
| `agentic-review` complete workflow | `implement` and `implement-spec` at review with worktree, branch, base and prior-check context; Round 0 loads `review-rounds` when a Round will run; builders retain fixes, integration and a corrective check's Retro origin (the merge is `merging`'s, below) | #366, Spec #555 |
| `merging` | `implement` (step 7 and the retro check), `implement-spec` (step 8) and `release` (the changelog pull request) at their merge step; `review-rounds` "When a person is needed" defines a boundary crossing by it; callers keep their method, title, committer, readiness and pre-merge step | Spec #641 (#642, #643, #644) |
| `worker-control` | `milestone`'s Plugin version check, to start its one cheap worker where the runner is not a fresh session; `team-lead` for every worker start, state check, end, stop, pause, resume and check-in | #527, #529, #530 |
| Project tracker and triage docs | Builders read blocker/closure operations; `to-spec` and `to-tickets` read publication operations and role mappings | #366 |
| Triage-labels doc's Repo labels rule | `triage`, `to-spec`, `to-tickets` and `review-rounds` read it there; `triage` no longer holds it | #156 |

## Remaining references and consistency

Owner-local supporting files remain behind their owner's pointers: `review-rounds` and its `FINDERS.md`, `VERIFY.md` and `DEEP.md` own review procedure; `retro/BUG-CLASSES.md` owns aggregation and preventive checks. References to complete workflows retain their task and caller context. Direct `grilling`/`domain-modeling` composition remains valid. Retro's follow-up build redesign is deferred; its existing build references remain live. Release's feature-membership use of absorption and prototype's unrelated word sense are outside the absorption contract. Implementer briefs may differ; the merge rule does not (see the amendment note).

No blanket link-count target applies. For shared rules, check owners, consumers and any unmigrated copies together. For every changed rule, also check parallel statements within its skill and repository descriptions for contradictions or stale claims. These are continuing protections, not migration-only work.

Local migration evidence covers index writing/checking, record interpretation, absorption lifecycle/publication, caller exceptions and retro handoff/resumption. Standard/Deep fixture results and their limits are recorded in `evals/agentic-review/RESULTS.md`; Standard's known discovery miss remains a failure. Two independent final integrated remote clean-install evaluations passed against published candidate `339a3be935f0622e03928aa831da52ea591e0940`: all 29 skills discovered and both grilling interviews explicitly confirmed and closed. These verify the Spec ref; default-ref verification awaits merge, and the bounded dependency/workflow limits above remain. See `evals/codex-install/RESULTS.md` for exact turns and provenance. See `evals/shared-rules/RESULTS.md` for the final evidence reconciliation.

*Amendment note, 2026-11-04, Spec #641.* After #533 the merge rule is one shared rule, not an independent merge policy: who merges (read from the Boundary record alone), the `Agent-merged rules:` line, the repo's merge-time steps, syncing main, the merge and closing issues were written out in full in `implement` and `implement-spec`, with a third, shorter rule in `release`. The `merging` Base skill now owns it and its three callers load it by name at their merge step, so "Unify look-alike rules: rejected" no longer covers merging. The merge method, title, committer, closing-line reconcile and a caller's own pre-merge step stay with each caller.

*Amendment note, 2026-11-14, Spec #151.* The Codex clean-install evidence cited above (`evals/codex-install/RESULTS.md`) is history: the plugin is Claude Code only for now (ADR 0001), the per-skill agent metadata files and the Codex manifest are gone, and the eval folder was deleted earlier (ADR 0015).

*Amendment note, 2026-11-14, Spec [#162](https://github.com/Luffytse/luffy-agentic-workflow/issues/162).* `worker-control` no longer holds a short check or a fallback to an unknown harness's own docs: with no reference for the runtime it tells the user and stops, and its probes are this repo's Environment check (`docs/dev-skills/environment-check.md`). `milestone` keeps only the Plugin version check, which still loads `worker-control` to start its one cheap worker.
