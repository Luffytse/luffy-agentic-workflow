---
name: model-tiers
description: "Map a Model tier (cheap, regular, premium, top) to a model in the coding agent you run in. Use when a skill tells you to run a step or subagent on a tier."
user-invocable: false
---

The plugin's default map from Model tier to model, one column per coding agent. This is the only file in the plugin that names vendor models; a skill that runs a step on a tier names the tier only.

A tier map in the project's own instructions (`CLAUDE.md`, `AGENTS.md` or the coordinator's brief) overrides this one: use the project's map where it has one, and this map for any tier or agent it does not cover. Pick the column for the coding agent you are running in. If your agent has no column or the named model is unavailable to the account, use the nearest tier you can run (premium for top) and say so; never guess a model name.

| Tier | Claude Code model | Use for |
|------|-------------------|---------|
| cheap | Haiku | trivial jobs: running tests, simple checks |
| regular | Sonnet | most implementation work |
| premium | Opus | Milestone planning, heavy or tricky work |
| top | Fable | planning a feature with the user (grilling, the Spec, the split into Tickets), and advice to Release planning on a dependency graph or another special planning case |

A new model generation changes this table only.
