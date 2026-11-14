# dev-skills

The development skills as one plugin for Claude Code: the path from `wayfinder` through specs, tickets and implementation to `agentic-review` and `retro`. The skills began as 22 of [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT) and are our own now. Every skill is model-invoked, so an agent in a project thread (where nobody types slash commands) can start any of them. See [ADR 0001](../../docs/dev-skills/adr/0001-dev-skills-is-one-plugin-forked-from-matt-pocock.md).

## Install

From inside Claude Code:

```
/plugin marketplace add https://github.com/Luffytse/luffy-agentic-workflow
/plugin install dev-skills@luffy-agentic-workflow
```

Or from the shell:

```bash
claude plugin marketplace add https://github.com/Luffytse/luffy-agentic-workflow
claude plugin install dev-skills@luffy-agentic-workflow
```

Skills are namespaced, for example `dev-skills:wayfinder`. For a Claude project, add the plugin in Project settings.

## Update

```bash
/plugin marketplace update luffy-agentic-workflow
# Or from the shell:
claude plugin marketplace update luffy-agentic-workflow
```

## Local development

```bash
claude plugin marketplace add /path/to/luffy-agentic-workflow
claude plugin install dev-skills@luffy-agentic-workflow
```

Run `scripts/check-plugin.sh` and `claude plugin validate .` from the repo root before pushing.

## Layout

```
plugins/dev-skills/
├── .claude-plugin/plugin.json   # plugin manifest, the version source
├── skills/                      # every skill
├── CHANGELOG.md                 # what each version brought; a Release adds one entry
└── LICENSE-mattpocock-skills    # Upstream's MIT notice
```

To add a skill, create `skills/<name>/SKILL.md`; `plugin.json` already points at the folder. Keep a model-facing `description` in `SKILL.md` and omit `disable-model-invocation`. A Base skill may set `user-invocable: false` for menu hiding while remaining model-loadable; hiding is optional. See [skill mechanics](skills/writing-for-agents/SKILL-MECHANICS.md) for the frontmatter examples. Current consumers keep their instructions and references until the fresh-runtime gate and their migration pass (ADR 0009).

## Skills

One line per skill under `skills/`; each skill's own `SKILL.md` has the rest.

- `agentic-review`: sizes a review (Round 0) and picks its level.
- `ask-matt`: routes you to the right skill, from idea to ship.
- `codebase-design`: shared vocabulary for designing deep modules.
- `diagnosing-bugs`: a diagnosis loop for hard bugs and performance regressions.
- `docs-index`: the documentation-index contract (a Base skill).
- `domain-modeling`: builds the glossary and ADRs of a project's domain model.
- `grill-with-docs`: interviews you about a plan, recording glossary terms and ADRs as decisions settle.
- `grilling`: interviews you about a plan with nothing written down.
- `handoff`: compacts the conversation into a handoff document for a fresh agent.
- `implement`: builds one lone Ticket as its thread, writing the code itself, from branch to merge.
- `implement-spec`: builds one Spec as its thread, Tickets first, then the Spec pull request.
- `improve-codebase-architecture`: scans a codebase for refactors that deepen shallow modules.
- `issue-absorption`: records and reads the issues a Ticket absorbs (a Base skill).
- `merging`: finishes a pull request: who merges, the review-record check, the merge, closing issues (a hidden Base skill).
- `milestone`: plans a Milestone (names its features, sorts them by dependency and has each planned in its own session before the Milestone issue is written), checks the plugin version and reports at its end, key points first and the detail trimmed.
- `model-tiers`: maps a Model tier to the models of each coding agent (a Base skill).
- `pr`: writes a pull request title and body.
- `prototype`: builds a throwaway prototype to answer a design question.
- `release`: cuts a Release and plans the next one.
- `research`: investigates a question against primary sources and writes the findings to a file.
- `retro`: reviews a finished session or pull request and files environment improvements as Retro issues.
- `retro-planning`: sorts a repo's Retro backlog by root cause, closing one-offs and handing repeated problems to triage.
- `review-record`: the shape and reading of review comments (a Base skill).
- `review-rounds`: runs a review's Rounds, Finders to Rank (a hidden Base skill).
- `setup-dev-skills`: configures a GitHub repo for the plugin.
- `setup-project`: drafts a project's coordinator instructions.
- `tdd`: test-driven development, red-green-refactor.
- `team-lead`: runs a Milestone's delivery as the coordinator: starts every unblocked entry, check-ins, pause and resume, and the stop for the Milestone review.
- `to-spec`: turns the current conversation into a published spec.
- `to-tickets`: splits a plan or spec into tracer-bullet tickets.
- `triage`: moves issues and external pull requests through triage roles.
- `wayfinder`: charts foggy, large work as decision tickets.
- `wizard`: generates an interactive bash wizard for steps only a human can do.
- `worker-control`: starts, checks, stops, pauses and resumes workers in the tool you run in (a Base skill).
- `writing-for-agents`: how to write skills, `AGENTS.md` and `CLAUDE.md`.

## Model tiers

Skills name a tier (cheap, regular, premium or top), never a model ([ADR 0002](../../docs/dev-skills/adr/0002-skills-name-model-tiers-not-models.md)). The `model-tiers` skill (`skills/model-tiers/SKILL.md`) holds the map from each tier to each coding agent's models, and is the only place in the plugin that names them; a project's own map overrides it. A new model generation changes that file only.

## Credits and Upstream

Many of these skills began as [Matt Pocock's skills](https://github.com/mattpocock/skills) (`mattpocock/skills`, MIT; the notice is in `LICENSE-mattpocock-skills`). They are our own now: nothing is merged from Upstream by hand. A 2-week watch reads Upstream's new commits, and an idea worth taking goes through triage like any other issue.

- Last Upstream commit looked at: `a496f55` ("implement-spec: a fresh implementer subagent per ticket (#1342)", 2026-10-29)

The watch updates the commit above each time it looks.
