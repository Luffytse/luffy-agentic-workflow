# dev-skills

The development skills as one plugin for Claude Code and Codex: the path from `wayfinder` through specs, tickets and implementation to `agentic-review` and `retro`. The skills began as 22 of [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT) and are our own now. Every skill is model-invoked, so an agent in a project thread (where nobody types slash commands) can start any of them. See [ADR 0001](../../docs/dev-skills/adr/0001-dev-skills-is-one-plugin-forked-from-matt-pocock.md).

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

- `model-tiers`: a Base skill holding the plugin's default map from Model tier to each coding agent's models; loaded by any skill that runs a step or subagent on a tier, overridden by a project's own map.
- `review-record`: a Base skill for the review's comment shape (the Round and Ticket-check comments) and how to read them back; loaded by review writers and retro readers. Review orchestration and retro preventive-check work stay with their workflows.
- `review-rounds`: a Base skill holding a review's Rounds (Find, Verify unless there is nothing to verify, Rank, at most 3 Rounds, then the sort of what is still open), loaded by `agentic-review` only when its Round 0 picks a level above None. Its Finder, Verifier and Deep briefs are reference files read only when used.
- `docs-index`: a Base skill owning the documentation-index contract (index format and update requirements), loaded by name by document writers and the standards Finder; it moved here from `domain-modeling/DOCS-INDEX.md`.
- `issue-absorption`: a Base skill owning source-report records and lifecycle meaning, loaded by Ticket writers, planning readers and closing-line/closure consumers. Tracker operations remain in project configuration.
- `worker-control`: a Base skill a coordinator loads to start, check, stop, pause and resume workers in the tool it runs in, and to arrange and end a check-in: it detects how workers run from its tool names first, takes its role from explicit runtime lineage, loads that way's reference (`claude-code-project-threads`, `claude-code-sessions`, `codex-subagents`; each method citing its doc page) or falls back to the Harness's own docs, and runs the short check that proves the methods before unattended work relies on them.

- `setup-dev-skills`: derived from Upstream's setup skill. Sets up a GitHub repo for the skills: writes `docs/dev-skills/` (issue tracker, labels, domain docs, the Boundary record and, for a repo that cuts Releases, the release doc), the `## Agent skills` block, a starter `REVIEW.md` and `docs/dev-skills/index.md`, creates the labels the skills use, and reports the GitHub settings the build skills rely on without changing them. A re-run shows a diff first.
- `setup-project`: interviews the user with `grilling` and drafts project instructions, never work state. Inside a Milestone it points to `milestone`, `team-lead` and the Boundary record and keeps only project-specific choices; without an open Milestone agreement it keeps the full thread/brief/model instructions. After approval the thread sends the text to the coordinator to save; it never edits project settings itself.
- `retro-planning`: works through a snapshot of one repo's Retro backlog (ADR 0007): files an open `retro-planning` record, groups the Retro issues by root cause, walks the user through each group one at a time and carries out each call at once (a `ready-for-agent` Ticket up to the cap, a close, or a spin-off to its own planning thread), closes expired issues and issues whose Ticket has closed as completed in one list at the end, and closes the record; at a Release end, agents decide every group with no cap, mark the Ticket of each group that joins the next Release `next-release`, and propose feature-sized fixes to the user.
- `release`: cuts a Release and plans the next one (ADR 0008), reading the repo's release doc (`docs/dev-skills/release.md`): checks every issue with the release label is closed; where Releases bump (the default), picks the patch, minor or major bump from what shipped and opens the bump pull request with its `CHANGELOG.md` entry for the user to merge; where pull requests bump, writes one `CHANGELOG.md` entry for everything since the last Release, with its start and end commits and the versions delivered, runs the whole-Release check and merges that changelog pull request itself; then proposes the next Release's goal and at most 5 features and labels only what the user approves (inside a Milestone, agents plan it with no approval, from the Milestone's feature order plus the maintenance fixes the Triage batch and Release-end Retro planning chose). Where Releases bump, an urgent fix runs as a patch Release of one issue.
- `milestone`: plans a Milestone and reports at its end. Its planning phase writes the Milestone issue with the user (goal, features in build order with their acceptance criteria, exclusions, budget, boundaries beyond the Boundary record, and the membership label in the record's form, put on every planned feature); agents may propose a feature, never add one, and a feature added mid-Milestone is planned with the user first, then listed, then labelled. Its Startup verification runs `worker-control`'s check (workers start, state read from the Harness, pause, confirmed stop, end notice, check-in) and proves that a fresh thread loads main's plugin version, posts the result (with the runtime's permission and sandbox settings) on the Milestone issue, and names a failed essential capability to the user. Delivery is `team-lead`'s. Once every feature is merged or parked, it posts the Milestone report (acceptance evidence, parked work, maintenance, the user's messages, measured time/tokens and gaps, loaded versions and Startup verification, environment settings, agent decisions and suggestions), then stops for the user's Milestone review with the Milestone open.
- `team-lead`: the coordinator's delivery role, for a Milestone or a lone Release (ADR 0010). It starts build threads in order within the limits and starts Release threads (Release grouping stays `release`'s), reacts to what workers and the Harness report, holds a check-in at the Boundary record's interval, arranged when the first build thread starts, only as a safety net for build threads (a silent Release thread is brought to the user once) (its `snapshot.py` prints one row per worker from the tracker and git: last commit, last comment, pull request, found by the branch when no report named it, and a verdict; a tracker it cannot read is read by hand; a quiet check-in writes nothing), nudges a silent worker once and then stops it and replaces it from the pushed branch and the tracker, or parks the work and tells the user once, pauses and resumes on the user's word, and follows the merge-time steps the repo's own docs give. Every worker start, state check, end, stop, pause, resume and check-in goes through `worker-control`; tracker comments are its audit trail. The project's own instructions add only their thread limit, tier map and extra rules.

## Model tiers

Skills name a tier, never a model ([ADR 0002](../../docs/dev-skills/adr/0002-skills-name-model-tiers-not-models.md)). The `model-tiers` skill (`skills/model-tiers/SKILL.md`) holds the map from each tier to each coding agent's models, and is the only place in the plugin that names them; a project's own map overrides it. A new model generation changes that file only.

## Credits and Upstream

Many of these skills began as [Matt Pocock's skills](https://github.com/mattpocock/skills) (`mattpocock/skills`, MIT; the notice is in `LICENSE-mattpocock-skills`). They are our own now: nothing is merged from Upstream by hand. A 2-week watch reads Upstream's new commits, and an idea worth taking goes through triage like any other issue.

- Last Upstream commit looked at: `a496f55` ("implement-spec: a fresh implementer subagent per ticket (#1342)", 2026-10-29)

The watch updates the commit above each time it looks.
