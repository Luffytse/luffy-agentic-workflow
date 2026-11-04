---
name: model-tiers
description: "Map a Model tier (cheap, regular, premium) to a model in the coding agent you run in. Use when a skill tells you to run a step or subagent on a tier."
user-invocable: false
---

The plugin's default map from Model tier to model, one column per coding agent. This is the only file in the plugin that names vendor models; a skill that runs a step on a tier names the tier only.

A tier map in the project's own instructions (`CLAUDE.md`, `AGENTS.md` or the coordinator's brief) overrides this one: use the project's map where it has one, and this map for any tier or agent it does not cover. Pick the column for the coding agent you are running in. If your agent has no column or the named model is unavailable to the account, use the nearest tier you can run and say so; never guess a model name.

| Tier | Claude Code model | Codex model | Use for |
|------|-------------------|-------------|---------|
| cheap | Haiku | `gpt-6-luna` | trivial jobs: running tests, simple checks |
| regular | Sonnet | `gpt-6.1-sol` | most implementation work |
| premium | Opus | `gpt-6-astra` | planning, grilling, heavy or tricky work |

The Codex mapping is our recommendation based on the [official Codex models documentation](https://learn.chatgpt.com/docs/models), checked 2026-10-31: focused tasks, sustained complex work, and the hardest reasoning respectively. Availability depends on the account, client and workspace settings. In Codex, select a table entry with `codex -m <model>` or `/model` in an interactive session. A new model generation changes this table only.
