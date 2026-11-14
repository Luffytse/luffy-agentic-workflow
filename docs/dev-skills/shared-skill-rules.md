# Shared skill rules

How this plugin shares a rule between skills. These are rules for building `dev-skills`, so they live here and not in `writing-for-agents`, which every project loads and which is the inherited text. The words Shared rule and Base skill are in the [Packaging glossary](glossary/packaging.md); the owners and consumers are in [ADR 0009](adr/0009-shared-rules-have-one-owner-skill.md).

## The one difference from the inherited advice

`writing-for-agents` (`SKILL-MECHANICS.md`) says a reference that two user-invoked skills both need goes to "a plain file outside the skill system". This plugin puts it in a hidden Base skill instead, because a named skill's discovery, loading and application can be shown in a fresh runtime, and a plain file's cannot (ADR 0009, "A shared folder outside the skill system: rejected"). Every skill here but one is model-invoked, so a Base skill has a description and another skill reaches it by name.

## Choose ownership by what must agree

- **Reuse a complete workflow** when the caller needs its task. The workflow owns its procedure; the caller keeps its trigger, surrounding coordination, exceptions and independent policies.
- **Extract a Base skill** when several consumers need a small contract they must interpret the same way. Give that focused contract a named, model-loadable home; consumers load it at the point of use. Loading a large workflow just to borrow a record format or definition hides the ownership boundary.
- **Keep independent rules independent.** Similar wording may express different policies. Repeated calls to the same capabilities also do not require a new wrapper or a shared owner for the callers' coordination.
- **Read project configuration** for tracker operations, label mappings and settings. Those belong to the project; reusable skills hold only project-independent rules.

Our own contracts, by name: `review-record` owns markers, fields, Finding identifiers, statuses and interpretation; `issue-absorption` owns absorption records and completed-versus-abandoned fix meaning; `docs-index` owns index format and update requirements; `merging` owns the merge rule; `worker-control` owns how workers are started and read; `model-tiers` owns the tier map. Review orchestration belongs to its review workflow, and turning repeated Findings into preventive checks belongs to its retro workflow. Extract only the shared contract, not a whole reference file containing those procedures.

## Before switching consumers

Verify in a fresh supported runtime that their named dependencies are discovered, loaded and actually applied. Test complete-workflow and reference dependencies; report menu visibility separately. Keep current instructions, links and copies until that gate passes and the corresponding migration is complete. Migrate record writers and readers together, preserving caller triggers and exceptions.

## Migration notes

For each changed rule, check remaining statements that must agree (including unmigrated shared copies), parallel sentences in the edited file, and repository descriptions of the changed behavior. Independent policies can differ, but contradictions within a skill and stale descriptions still need fixing. Remove a transition note only after its migration is complete. In a pruning pass, independent rules are not duplicate meanings merely because their wording matches.

## Metadata for a Base skill

Model reachability and user-menu visibility are separate choices:

- A **model-invoked** skill has a model-facing `description` with trigger branches, so the agent can discover it and other skills can reach it. Omit `disable-model-invocation` to retain model reachability.
- A **user-only** skill sets `disable-model-invocation: true` in Claude Code. Its description is not in the model's discovery context, so callers cannot rely on it as an autonomous dependency. `improve-codebase-architecture` is the one, and the plugin checker's `model-invoked` check lists it.
- A **Base skill** is model-invoked even when hidden from a user menu. In Claude Code, `user-invocable: false` hides the command while retaining model access. Keep the description and omit `disable-model-invocation`. Hiding is preferred where supported, but discovery, loading and application are required; visible bases are valid when the host cannot hide them.

Choose model invocation whenever another skill needs the dependency, including a dependency shared by user-only workflows. Package a shared contract as a named Base skill, not as an external shared folder. Supporting files can stay beside their owning skill, behind pointers from it.

Use the contract's real name and trigger in `SKILL.md`; this example shows the shape:

```yaml
---
name: example-contract
description: Interpret example records. Use when a caller writes or reads an example record.
user-invocable: false
---
```

See the [Claude Code invocation reference](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) for how the visibility flag behaves. Metadata validation does not replace the fresh-runtime check above.
