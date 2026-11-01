# Shared rules have one owner skill

A **Shared rule** is one that two or more skills must follow the same way: a record contract, a rule of a workflow they invoke, or a project configuration rule. The revised plan in [#348](https://github.com/Luffytse/luffy-dev-skills/issues/348) gives each one an owner, using complete workflows when they fit and focused **Base skills** for shared contracts. This is a planned migration: existing skill instructions, links, copies and repository checks govern until their respective migration Tickets land.

## Ownership

- **Complete workflows:** a caller runs another skill when it needs that skill's task. The workflow owns its procedures; the caller keeps its surrounding coordination and independent policies. Build skills already run `agentic-review`, so review Rounds stay there while assigning fixes, integration and merge decisions stay with the builders.
- **Focused contracts:** when consumers need a small rule that must agree, they load its Base skill by name at the relevant point. The base holds the shared meaning, not the larger workflow that happened to contain it.
- **Project configuration:** tracker operations, label mappings and release settings remain in the project's files. Skills read those files; they hold only rules that fit any project.
- **Independent rules:** similar wording does not require a common owner. Repeated composition is also valid: callers may keep using `grilling` and `domain-modeling` directly, while `grill-with-docs` remains their convenient combined entry point.

The `docs-index` Base skill owns index format and update requirements; its writers and standards Finder load it by name, preserving caller triggers and exceptions (migrated in #364). The `issue-absorption` Base skill owns absorption records and the meaning of completed versus abandoned fixes (migrated in #368). The `review-record` Base skill owns review markers, fields, Finding identifiers, statuses and record interpretation (migrated in #365). Writers and readers migrate together; callers keep their triggers and exceptions. Review orchestration stays in `agentic-review`, and the procedure for turning repeated Findings into preventive checks stays in `retro`.

## Workflow handoff

The planned `retro-planning` handoff moves earlier: it selects one problem with the user, then `to-tickets` prepares, discusses and publishes the concrete Ticket. Retro planning keeps the snapshot, order, cap, closes, spin-offs and record, and updates that record before moving on.

The ordinary handoff aims for one complete Ticket. If several are needed, it returns to planning before publication so the larger effort can be spun off, rather than forcing an oversized Ticket or silently raising the cap. Partial publication is reconciled on resume instead of duplicated. The absorption contract and this handoff land separately.

## Considered options

- **Unify look-alike rules:** rejected. Independent merge policies or Implementer briefs may evolve separately.
- **Move all of retro's bug-class reference into a base:** rejected. Reviewers need shared record meaning, not retro's preventive-check workflow.
- **A shared folder outside the skill system:** rejected in favor of named skills, whose loading must be demonstrated rather than assumed.
- **Require hidden menus everywhere:** rejected. Hiding is preferred where supported; model discovery, loading and application are required.

Upstream deliberately separated reusable interview and domain-modeling capabilities from their wrappers ([documented rationale](https://github.com/mattpocock/skills/commit/995fceec7a185754dbc2f32bc9b4f461b14578f2)). Repeated calls to those capabilities do not duplicate their rules.

## Migration and verification

This narrows ADR 0006's rejected separate index skill: the trigger stays with each writer or checker. The docs-index migration is implemented after successful loading/application evidence in #360; unrelated migrations below retain their transition safeguards.

After this decision is recorded, #363 establishes authoring guidance and packaging support. #360 must demonstrate fresh-session discovery, loading and actual application of both workflow and reference dependencies before consumers switch. Closing that issue after a failed check is insufficient. Visibility is reported separately; a visible base may pass when hiding is unsupported.

The migrations are #364 (docs index), #365 (review records), #368 (absorption), #369 (retro handoff, after #368) and #366 (redundant review/configuration rules, after #365). #370 reconciles the transition after those migrations. Behavioral checks cover record interpretation, caller exceptions, workflow handoffs and resumption, alongside repository and plugin validation.

Until each migration lands, keep its current references and consistency protections. Preserve checks for remaining statements that must agree, contradictions within a skill and stale repository descriptions; remove only interim notes whose migration is complete. The deferred retro follow-up build redesign and independent interview composition are outside this effort, so completion is not a blanket ban on every cross-skill link.

The #365 migration loads `review-record` in review writers and retro readers. It owns comment meaning and the reviewer’s Bug class/Always-check vocabulary; ranking, Rounds and Nit fix timing remain in `agentic-review`, and aggregation and guardrail work remain in `retro/BUG-CLASSES.md`. Other migrations retain their transition rules above.

The #366 migration removes duplicated review procedures from build callers. They invoke the complete review workflow with worktree, branch, base and prior-check context, and keep fix assignment, integration and independent merge policies. Build callers read blocker and closure operations from the project tracker doc; publication callers map triage roles through the configured triage-label doc. Deferred follow-up builds and direct interview composition remain unchanged.
