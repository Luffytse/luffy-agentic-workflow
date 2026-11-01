# dev-skills

The development skills as one plugin for Claude Code and Codex: the path from `wayfinder` through specs, tickets and implementation to `agentic-review` and `retro`. The skills began as 22 of [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT) and are our own now. Every skill is model-invoked, so an agent in a project thread (where nobody types slash commands) can start any of them. See [ADR 0001](../../docs/adr/0001-dev-skills-is-one-plugin-forked-from-matt-pocock.md).

## Install

### Claude Code

From inside Claude Code:

```
/plugin marketplace add https://github.com/Luffytse/luffy-dev-skills
/plugin install dev-skills@luffy-dev
```

Or from the shell:

```bash
claude plugin marketplace add https://github.com/Luffytse/luffy-dev-skills
claude plugin install dev-skills@luffy-dev
```

Skills are namespaced, for example `dev-skills:wayfinder`. For a Claude project, add the plugin in Project settings.

### Codex

From the shell (verified with Codex CLI `0.166.0-alpha.5.1`):

```bash
codex plugin marketplace add https://github.com/Luffytse/luffy-dev-skills
codex plugin add dev-skills@luffy-dev
codex plugin list --marketplace luffy-dev --json
```

The list should show `dev-skills` installed and enabled. Start a new Codex session to load the skills. Both agents use the same `skills/` tree.

## Update

For Claude Code:

```bash
/plugin marketplace update luffy-dev
# Or from the shell:
claude plugin marketplace update luffy-dev
```

For Codex with the GitHub marketplace:

```bash
codex plugin marketplace upgrade luffy-dev
codex plugin add dev-skills@luffy-dev
```

Start a new Codex session after updating (restart the desktop app if using it).

## Local development

For Claude Code:

```bash
claude plugin marketplace add /path/to/luffy-dev-skills
claude plugin install dev-skills@luffy-dev
```

For Codex:

```bash
# If luffy-dev is already configured from GitHub, remove that source first:
codex plugin marketplace remove luffy-dev
codex plugin marketplace add /path/to/luffy-dev-skills
codex plugin add dev-skills@luffy-dev
```

Codex loads a cached copy. After editing the clone, repeat `codex plugin add dev-skills@luffy-dev` and start a new session (restart the desktop app if using it). `marketplace upgrade` applies to Git sources, not local paths. To return to GitHub, remove the local marketplace source, then repeat the Codex install steps. See the [official packaging docs](https://developers.openai.com/plugins/build/plugins#how-local-marketplaces-work).

Run `scripts/check-plugin.sh` and `claude plugin validate .` from the repo root before pushing.

## Layout

```
plugins/dev-skills/
├── .claude-plugin/plugin.json   # Claude Code manifest
├── .codex-plugin/plugin.json    # Codex manifest, same name, version and skills path
├── skills/                      # every skill
├── CHANGELOG.md                 # what each version brought; a Release adds one entry
└── LICENSE-mattpocock-skills    # Upstream's MIT notice
```

To add a skill, create `skills/<name>/SKILL.md` and `skills/<name>/agents/openai.yaml` with a readable `display_name` matching the folder name, a `short_description` and `policy.allow_implicit_invocation: true`; `plugin.json` already points at the folder. Keep a model-facing `description` in `SKILL.md` and omit `disable-model-invocation`. A Base skill may set `user-invocable: false` for Claude Code menu hiding while remaining model-loadable. Codex's implicit-invocation policy is separate from menu visibility; hiding is optional. See [skill mechanics](skills/writing-for-agents/SKILL-MECHANICS.md) for the metadata examples. Current consumers keep their instructions and references until the fresh-runtime gate and their migration pass (ADR 0009).

## Skills added since the copy

- `issue-absorption`: a Base skill owning source-report records and lifecycle meaning, loaded by Ticket writers, planning readers and closing-line/closure consumers. Tracker operations remain in project configuration.

- `setup-dev-skills`: derived from Upstream's setup skill. Sets up a GitHub repo for the skills: writes `docs/agents/` (issue tracker, labels, domain docs and, for a repo that cuts Releases, the release doc), the `## Agent skills` block, a starter `REVIEW.md` and `docs/index.md`, creates the labels the skills use, and reports the GitHub settings the build skills rely on without changing them. A re-run shows a diff first.
- `setup-project`: interviews the user with `grilling` and drafts the project instructions that tell the coordinator how to brief build threads and which model each Model tier maps to (how the project works, never the state of its work). After approval the thread sends the text to the coordinator to save; it never edits project settings itself.
- `retro-planning`: works through a snapshot of one repo's Retro backlog (ADR 0007): files an open `retro-planning` record, groups the Retro issues by root cause, walks the user through each group one at a time and carries out each call at once (a `ready-for-agent` Ticket up to the cap, a close, or a spin-off to its own planning thread), closes expired issues and issues whose Ticket has closed as completed in one list at the end, and closes the record.
- `release`: cuts a Release and plans the next one (ADR 0008), reading the repo's release doc (`docs/agents/release.md`): checks every issue with the release label is closed, picks the patch, minor or major bump from what shipped, opens the bump pull request with its `CHANGELOG.md` entry for the user to merge, then proposes the next Release's goal and at most 5 features and labels only what the user approves. An urgent fix runs as a patch Release of one issue.

## Model tiers

Skills name a tier, never a model ([ADR 0002](../../docs/adr/0002-skills-name-model-tiers-not-models.md)). The table maps tiers to each agent's models:

| Tier | Claude Code model | Codex model | Use for |
|------|-------------------|-------------|---------|
| cheap | Haiku | `gpt-6-luna` | trivial jobs: running tests, simple checks |
| regular | Sonnet | `gpt-6.1-sol` | most implementation work |
| premium | Opus | `gpt-6-astra` | planning, grilling, heavy or tricky work |

The Codex mapping is our recommendation based on the [official Codex models documentation](https://learn.chatgpt.com/docs/models), checked 2026-10-31: focused tasks, sustained complex work, and the hardest reasoning respectively. Availability depends on the account, client and workspace settings. In Codex, select a table entry with `codex -m <model>` or `/model` in an interactive session. A new model generation changes this table only.

## Credits and Upstream

Many of these skills began as [Matt Pocock's skills](https://github.com/mattpocock/skills) (`mattpocock/skills`, MIT; the notice is in `LICENSE-mattpocock-skills`). They are our own now: nothing is merged from Upstream by hand. A 2-week watch reads Upstream's new commits, and an idea worth taking goes through triage like any other issue.

- Last Upstream commit looked at: `a496f55` ("implement-spec: a fresh implementer subagent per ticket (#1342)", 2026-10-29)

The watch updates the commit above each time it looks.
