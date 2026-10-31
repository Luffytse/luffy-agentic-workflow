# luffy-dev-skills

A Claude Code plugin marketplace, named `luffy-dev`. Each plugin lives under `plugins/<name>/` and is listed in `.claude-plugin/marketplace.json`.

- `dai-portal-data`: tooling for the local DAI Portal Postgres database.
- `dev-skills`: the development skill set used across projects, a fork of Matt Pocock's skills plus our own review pipeline. See `docs/adr/`.

Words used here (Finder, Verifier, Finding, Bug class, Review depth, Model tier and so on) are defined in `GLOSSARY.md`. Decisions are in `docs/adr/`. Start at `docs/index.md`, which says which doc to read for what.

## Working rules

- Skills name a **model tier** (cheap, regular, premium), never a vendor's model name, because other coding agents may load these plugins. See `docs/adr/0002-skills-name-model-tiers-not-models.md`.
- A pull request that changes the `agentic-review` skill is merged by the user, not by the thread that built it (the "repo's own rules" item of the merge list in `implement` and `implement-spec`). Rules like this one, which only fit this repo, live here and never in skill text, because every project that loads the plugin reads the skills.
- A change that touches only `evals/` (the skill evals, at the repo root, outside the plugin) is not a plugin change: it does not count as changing the `agentic-review` skill, so the thread that built it may merge it (issues #185, #195).
- Every change to text that came from Matt Pocock's upstream repo is listed in `plugins/dev-skills/PATCHES.md`, so upstream updates can be merged by hand.
- A plugin's `version` in `.claude-plugin/plugin.json` changes only in a Release's bump pull request (ADR 0008); while `plugins/dev-skills/PATCHES.md` exists, a `dev-skills` bump pull request also adds a "version X to Y" line to it, which `scripts/check-plugin.sh` compares with `plugin.json`. Every other pull request, under `plugins/<name>/` or not, leaves the version as it is on main and takes no number another branch could also take, so parallel branches never collide or renumber. A new Patch heading in `PATCHES.md` and a new check in `scripts/check-plugin.sh` takes a name, not a number: `## Patch: <short name> (<folders>)`, the check's `# <name>: <description>` header, and "new check `<name>`" wherever a Patch or another check points at it. `scripts/check-plugin.sh` is this repo's own tooling, outside the plugins: editing it changes no plugin, and the CI workflow line that runs it is committed by the user by hand.
- When a `dev-skills` skill runs in this repo, follow the checkout's copy (`plugins/dev-skills/upstream-skills/<name>/` or `plugins/dev-skills/skills/<name>/`) on main, not the installed one, because main may be ahead of the installed plugin cache. A pull request that changes a skill is reviewed with main's version of that skill unless the pull request says otherwise.
- Before each push, search the repo for every other place that states the rule you just changed and update them in the same commit as the change (if you find a miss after pushing, fix it in a new commit). This repo restates rules in places such as skills and their parallel sentences, in another skill's paraphrase (an "as in step N" reference imports every bullet of step N, so read each one in the new context), in `GLOSSARY.md`, in the ADRs under `docs/adr/`, in `PATCHES.md` bullets, in comments and messages in `scripts/check-plugin.sh`, and in `docs/index.md`. `REVIEW.md`'s "related text not updated" line catches the misses, but only a Round later.
- Run `claude plugin validate .` (Claude Code's checker for plugin files) before pushing a change to a plugin or to `marketplace.json`.

## Agent skills

Start at `docs/index.md`; it says which doc to read for what.

### Issue tracker

Issues and specs live in this repo's GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

5 state roles + 2 category roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, `bug`, `enhancement`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one root `GLOSSARY.md` and `docs/adr/`. See `docs/agents/domain.md`.
