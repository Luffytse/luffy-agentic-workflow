# Skills name model tiers, not models

A skill that picks a model for a subagent names a tier: **cheap**, **regular** or **premium** (a fourth, `top`, is added in the note below). It never names a vendor's model, because other coding agents (Codex, Copilot and others) may load these plugins. Each agent maps the tiers to its own models.

The plugin ships that mapping as the `model-tiers` skill (`plugins/dev-skills/skills/model-tiers/SKILL.md`): one column per coding agent, and the only file in the plugin that names vendor models. Every skill that runs a step or subagent on a tier tells the agent to load it by name. A map in the project's own instructions overrides it (`setup-project` drafts that map), so a new model generation changes one table, not every skill. The plugin README points at the file and holds no table of its own.

## Note (Spec #151)

The tier rule stands. The plugin supports one coding agent for now, Claude Code, so `model-tiers` holds one model column. A second agent's column returns when it is supported again.

## Note (Ticket #166, replacing #92)

There are four tiers: cheap, regular, premium and `top`, above premium. `top` is for planning a feature with the user (grilling, the Spec, the split into Tickets) and for advice to Release planning on a dependency graph or another special planning case. The Release thread and the Milestone planning thread run on premium; a Ticket is never `top`. A session without the `top` model uses premium and says so. The tier rule is unchanged, and the `vendor-model-names` check also rejects the new model's name outside the tier map.
