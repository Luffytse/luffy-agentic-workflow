# Skills name model tiers, not models

A skill that picks a model for a subagent names a tier: **cheap**, **regular** or **premium**. It never names a vendor's model such as Haiku, Sonnet or Opus, because other coding agents (Codex, Copilot and others) may load these plugins. Each agent maps the tiers to its own models; for Claude Code today that is Haiku, Sonnet and Opus. The plugin's README (`plugins/dev-skills/README.md`) holds that mapping, so a new model generation changes one table, not every skill.
