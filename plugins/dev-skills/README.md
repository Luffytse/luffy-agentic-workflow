# dev-skills

The development skills as one Claude Code plugin: the path from `wayfinder` through specs, tickets and implementation to `agentic-review` and `retro`. It is a fork of [Matt Pocock's skills](https://github.com/mattpocock/skills) (22 of his 27) plus skills of our own. Every skill is model-invoked, so an agent in a project thread (where nobody types slash commands) can start any of them. See [ADR 0001](../../docs/adr/0001-dev-skills-is-one-plugin-forked-from-matt-pocock.md).

## Install

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

## Layout

```
plugins/dev-skills/
├── .claude-plugin/plugin.json   # lists both skill folders below
├── upstream-skills/             # forked from Upstream; every change is in PATCHES.md
├── skills/                      # our own skills: setup-project, retro-planning, setup-dev-skills, release
├── CHANGELOG.md                 # what each version brought; a Release adds one entry
├── PATCHES.md                   # what we changed in Upstream text, and the Upstream commit
└── LICENSE-mattpocock-skills    # Upstream's MIT licence
```

Forked and own skills live in separate folders so it is always clear which text came from Upstream. Never put our own skill in `upstream-skills/`. To add one, create `skills/<name>/SKILL.md`; `plugin.json` already points at the folder.

## Our own skills

- `setup-dev-skills`: derived from Upstream's setup skill. Sets up a GitHub repo for the skills: writes `docs/agents/` (issue tracker, labels, domain docs and, for a repo that cuts Releases, the release doc), the `## Agent skills` block, a starter `REVIEW.md` and `docs/index.md`, creates the labels the skills use, and reports the GitHub settings the build skills rely on without changing them. A re-run shows a diff first.
- `setup-project`: interviews the user with `grilling` and drafts the project instructions that tell the coordinator how to brief build threads and which model each Model tier maps to (how the project works, never the state of its work). After approval the thread sends the text to the coordinator to save; it never edits project settings itself.
- `retro-planning`: works through a snapshot of one repo's Retro backlog (ADR 0007): files an open `retro-planning` record, groups the Retro issues by root cause, walks the user through each group one at a time and carries out each call at once (a `ready-for-agent` Ticket up to the cap, a close, or a spin-off to its own planning thread), closes expired issues and issues whose Ticket has closed as completed in one list at the end, and closes the record.
- `release`: cuts a Release and plans the next one (ADR 0008), reading the repo's release doc (`docs/agents/release.md`): checks every issue with the release label is closed, picks the patch, minor or major bump from what shipped, opens the bump pull request with its `CHANGELOG.md` entry for the user to merge, then proposes the next Release's goal and at most 5 issues and labels only what the user approves. An urgent fix runs as a patch Release of one issue.

## Model tiers

Skills name a tier, never a model ([ADR 0002](../../docs/adr/0002-skills-name-model-tiers-not-models.md)). Other coding agents map the tiers to their own models. For Claude Code today:

| Tier | Claude Code model | Use for |
|------|-------------------|---------|
| cheap | Haiku | trivial jobs: running tests, simple checks |
| regular | Sonnet | most implementation work |
| premium | Opus | planning, grilling, heavy or tricky work |

A new model generation changes this table only.

## Updating from Upstream

Merge by hand, using [PATCHES.md](PATCHES.md). Run `scripts/check-plugin.sh` and `claude plugin validate .` (from the repo root) afterwards.
