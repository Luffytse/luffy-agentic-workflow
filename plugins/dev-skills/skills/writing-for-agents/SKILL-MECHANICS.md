# Skill mechanics

The skill-specific branch of [`writing-for-agents`](SKILL.md): what changes when the document is a skill (frontmatter, the invocation choice, and router skills). Everything else about writing it is the universal reference in `SKILL.md`.

## Invocation

Model reachability and user-menu visibility are separate choices:

- A **model-invoked** skill has a model-facing `description` with trigger branches, so the agent can discover it and other skills can reach it. Its description spends context load; its body loads when needed. Omit `disable-model-invocation` to retain model reachability.
- A **user-only** skill sets `disable-model-invocation: true` in Claude Code. Its description is not in the model's discovery context, so callers cannot rely on it as an autonomous dependency. Its human-facing description is a summary, and remembering it spends cognitive load.
- A **Base skill** is model-invoked even when hidden from a user menu. In Claude Code, `user-invocable: false` hides the command while retaining model access. Keep the description and omit `disable-model-invocation`. Hiding is preferred where supported, but discovery, loading and application are required; visible bases are valid when the host cannot hide them.

Choose model invocation whenever another skill needs the dependency, including a dependency shared by user-only workflows. Package a shared contract as a named Base skill, not as an external shared folder. Supporting files can stay beside their owning skill, behind pointers from it.

### Metadata for a Base skill

Use the contract's real name and trigger in `SKILL.md`; this example shows the shape:

```yaml
---
name: example-contract
description: Interpret example records. Use when a caller writes or reads an example record.
user-invocable: false
---
```

See the [Claude Code invocation reference](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) for how the visibility flag behaves. Metadata validation does not replace the fresh-runtime dependency check described in `SKILL.md`.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `SKILL.md`): split off a model-invoked skill when you have a distinct leading word that should trigger it on its own (a trigger word you actually use in your prompts), or another skill must reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Router skills

When user-only skills multiply past what you can remember, that piled-up cognitive load is cured by a **router skill**: one user-only skill that names the others and when to reach for each, so the human has one skill to remember instead of many. For user-only targets, it directs the human to invoke them; model-invoked targets remain available for an agent to load.
