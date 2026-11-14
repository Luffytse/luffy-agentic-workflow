# Packaging

The marketplace, the plugin and its skills, and the rules for how skills name models and share rules. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Marketplace**:
The catalog in this repo (`luffy-agentic-workflow`) that lists the plugins an agent can install.
_Avoid_: store, registry

**Plugin**:
One installable bundle of skills listed in the Marketplace, turned on as a whole.
_Avoid_: package, extension

**Skill**:
One instruction file (`SKILL.md` plus helper files) that an agent follows for one kind of task.
_Avoid_: command, prompt

**Upstream**:
Matt Pocock's public skills repo (`mattpocock/skills`), where the `dev-skills` skills began; they are our own now. How it is watched and an idea taken from it is ADR 0001's and the Upstream watch's (`docs/dev-skills/upstream-watch.md`).
_Avoid_: original, source

**Model tier**:
How strong a model a step needs: **cheap**, **regular**, **premium** or **top**. `top` is for planning a feature with the user and for Release planning advice; Milestone planning stays on premium. A skill names a tier, never a vendor's model; the plugin's default map is the `model-tiers` skill, and a project's own map overrides it (ADR 0002).
_Avoid_: model size, model class

**Model-invoked skill**:
A Skill the agent may start by itself when a task fits its description; hiding it from the user menu (`user-invocable: false` in Claude Code) keeps that model access. A **user-only skill** (`disable-model-invocation: true`) starts only when a person types its name; `improve-codebase-architecture` is the one, and the plugin checker's `model-invoked` check lists it. The settings are in `writing-for-agents` (`SKILL-MECHANICS.md`) and, for a Base skill, in `docs/dev-skills/shared-skill-rules.md`.
_Avoid_: auto skill, manual skill

**Shared rule**:
A rule two or more skills must follow the same way, such as a record contract, an invoked workflow's rule or a project configuration rule; independent rules may differ even when their wording matches. It names who owns a rule, not what review checks: contradictions and stale descriptions are still fixed (`CLAUDE.md`, `REVIEW.md`). ADR 0009 records the owners and consumers; existing links and unmigrated copies stay in force.
_Avoid_: common rule, duplicated rule

**Base skill**:
A Skill holding one focused Shared rule, which consumers load by name instead of a larger workflow, hidden from the menu where supported: `docs-index`, `review-record`, `issue-absorption`, `worker-control` and `merging` (ADR 0009); how one is shared and its frontmatter are in `docs/dev-skills/shared-skill-rules.md`.
_Avoid_: library skill, helper skill
