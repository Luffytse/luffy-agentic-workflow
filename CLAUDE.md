# luffy-dev-skills

A Claude Code plugin marketplace, named `luffy-dev`. Each plugin lives under `plugins/<name>/` and is listed in `.claude-plugin/marketplace.json`.

- `dai-portal-data`: tooling for the local DAI Portal Postgres database.
- `dev-skills`: the development skill set used across projects, a fork of Matt Pocock's skills plus our own review pipeline. See `docs/adr/`.

Words used here (Finder, Verifier, Finding, Bug class, Review depth, Model tier and so on) are defined in `GLOSSARY.md`. Decisions are in `docs/adr/`. Start at `docs/index.md`, which says which doc to read for what.

## Working rules

- Skills name a **model tier** (cheap, regular, premium), never a vendor's model name, because other coding agents may load these plugins. See `docs/adr/0002-skills-name-model-tiers-not-models.md`.
- A pull request that changes the `agentic-review` skill is merged by the user, not by the thread that built it (the "repo's own rules" item of the merge list in `implement` and `implement-spec`). Rules like this one, which only fit this repo, live here and never in skill text, because every project that loads the plugin reads the skills.
- A change that touches only `evals/` (the skill evals, at the repo root, outside the plugin) is not a plugin change: it needs no version bump and does not count as changing the `agentic-review` skill, so the thread that built it may merge it (issues #185, #195).
- Every change to text that came from Matt Pocock's upstream repo is listed in `plugins/dev-skills/PATCHES.md`, so upstream updates can be merged by hand.
- Every change under `plugins/<name>/` bumps that plugin's `version` in `.claude-plugin/plugin.json` to a higher one; no plugin change merges without it. The version, the number of a new Patch in `PATCHES.md` and the number of a new check in `check-plugin.sh` are taken only at merge time, after the last merge of main (the numbering step of `implement` and `implement-spec`), so parallel branches do not collide. Until then write `TBD-N` where such a number goes (in a Patch heading, in a "new check" line, in the check's `#` header and in every cross-reference) and leave the version as it is on main; both are expected during review, not Findings. `check-plugin.sh` fails on a leftover placeholder and on an unbumped version.
- When a `dev-skills` skill runs in this repo, follow the checkout's copy (`plugins/dev-skills/upstream-skills/<name>/` or `plugins/dev-skills/skills/<name>/`) on main, not the installed one, because main may be ahead of the installed plugin cache. A pull request that changes a skill is reviewed with main's version of that skill unless the pull request says otherwise.
- Run `claude plugin validate .` (Claude Code's checker for plugin files) before pushing a change to a plugin or to `marketplace.json`.

## Agent skills

Start at `docs/index.md`; it says which doc to read for what.

### Issue tracker

Issues and specs live in this repo's GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

5 state roles + 2 category roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, `bug`, `enhancement`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one root `GLOSSARY.md` and `docs/adr/`. See `docs/agents/domain.md`.
