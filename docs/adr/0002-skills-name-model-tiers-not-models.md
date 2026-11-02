# Skills name model tiers, not models

A skill that picks a model for a subagent names a tier: **cheap**, **regular** or **premium**. It never names a vendor's model, because other coding agents (Codex, Copilot and others) may load these plugins. Each agent maps the tiers to its own models.

The plugin ships that mapping as the `model-tiers` skill (`plugins/dev-skills/skills/model-tiers/SKILL.md`): one column per coding agent, and the only file in the plugin that names vendor models. Every skill that runs a step or subagent on a tier tells the agent to load it by name. A map in the project's own instructions overrides it (`setup-project` drafts that map), so a new model generation changes one table, not every skill. The plugin README points at the file and holds no table of its own.
