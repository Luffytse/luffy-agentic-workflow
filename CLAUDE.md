# luffy-dev-skills

A Claude Code plugin marketplace, named `luffy-dev`. Each plugin lives under `plugins/<name>/` and is listed in `.claude-plugin/marketplace.json`.

- `dai-portal-data`: tooling for the local DAI Portal Postgres database.
- `dev-skills`: the development skill set used across projects, a fork of Matt Pocock's skills plus our own review pipeline. See `docs/adr/`.

Words used here (Finder, Verifier, Finding, Bug class, Review depth, Model tier and so on) are defined in `GLOSSARY.md`. Decisions are in `docs/adr/`. Start at `docs/index.md`, which says which doc to read for what.

## Working rules

- Skills name a **model tier** (cheap, regular, premium), never a vendor's model name, because other coding agents may load these plugins. See `docs/adr/0002-skills-name-model-tiers-not-models.md`.
- Every change to text that came from Matt Pocock's upstream repo is listed in `plugins/dev-skills/PATCHES.md`, so upstream updates can be merged by hand.
- Run `claude plugin validate .` (Claude Code's checker for plugin files) before pushing a change to a plugin or to `marketplace.json`.

## Agent skills

### Issue tracker

Issues and specs live in this repo's GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one root `GLOSSARY.md` and `docs/adr/`. See `docs/agents/domain.md`.
