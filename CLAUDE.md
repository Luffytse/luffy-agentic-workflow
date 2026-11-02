# luffy-dev-skills

A Claude Code and Codex plugin marketplace, named `luffy-dev`. Each plugin lives under `plugins/<name>/`. The Claude Code catalog, `.claude-plugin/marketplace.json`, lists both plugins; the Codex catalog, `.agents/plugins/marketplace.json`, lists only `dev-skills`.

- `dai-portal-data`: tooling for the local DAI Portal Postgres database.
- `dev-skills`: the development skill set used across projects, skills that began as Matt Pocock's, now our own, plus our own review pipeline. See `docs/adr/`.

Words used here (Finder, Verifier, Finding, Bug class, Review depth, Model tier and so on) are defined in `GLOSSARY.md`. Decisions are in `docs/adr/`. Start at `docs/index.md`, which says which doc to read for what.

## Working rules

- Skills name a **model tier** (cheap, regular, premium), never a vendor's model name, because other coding agents may load these plugins. See `docs/adr/0002-skills-name-model-tiers-not-models.md`.
- Rules that only fit this repo live here and never in skill text, because every project that loads the plugin reads the skills.
- A change that touches only `evals/` (the skill evals, at the repo root, outside the plugin) is not a plugin change: it changes no skill and takes no version bump.
- Every pull request that changes a file under `plugins/dev-skills/skills/` bumps the `dev-skills` version: minor for a new or changed skill, patch for a fix or a revert; below 1.0.0 a breaking change bumps minor (ADR 0008). During review the branch leaves the version as it is on main. Just before merge the coordinator hands out the next number and merges such pull requests one at a time; the merging thread adds the bump as the pull request's last commit (`docs/agents/release.md` says how). `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` keep the same version, and the bump changes both together. Any other pull request, under `plugins/<name>/` or not, leaves the version as it is on main; its plugin files ride along with the next bump. A bad merged skill change is reverted on main at once, and the revert takes the next number. A Release here opens no bump pull request. A new check in `scripts/check-plugin.sh` takes a name, not a number: the check's `# <name>: <description>` header. `scripts/check-plugin.sh` is this repo's own tooling, outside the plugins: editing it changes no plugin, and the CI workflow line that runs it is committed by the user by hand.
- `release` reads this repo's bump mode ("pull requests bump") and Release name from `docs/agents/release.md`.
- When a `dev-skills` skill runs in this repo, follow the checkout's copy (`plugins/dev-skills/skills/<name>/`) on main, not the installed one, because main may be ahead of the installed plugin cache. A pull request that changes a skill is reviewed with main's version of that skill unless the pull request says otherwise.
- Before each push, search the edited file and repository for the changed rule's key terms. For a Shared rule, update its owner, consumers, record shapes and descriptions together, including any unmigrated shared copies. Independent policies may differ. For every changed rule, also resolve contradictions in parallel sentences within the skill and stale repository descriptions in the glossary, ADRs, index, READMEs and checker messages. An "as in step N" reference imports every bullet of that step: read it in the caller's context. Update related text in the same commit; a miss found after pushing gets a new commit. `REVIEW.md` checks the same consistency boundary.
- Run `claude plugin validate .` (Claude Code's checker for plugin files) before pushing a change to a plugin or to `marketplace.json`.

## Agent skills

Start at `docs/index.md`; it says which doc to read for what.

### Issue tracker

Issues and specs live in this repo's GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

5 state roles + 2 category roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, `bug`, `enhancement`; plus the optional agent-only role, mapped to `claude-only` and `codex-only` (an agent that sees the other agent's label leaves the issue alone). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one root `GLOSSARY.md` and `docs/adr/`. See `docs/agents/domain.md`.

### Boundaries

The agreed boundary: nothing needs the user's approval, no budget, one-hour check-ins, Milestone label `milestone-<n>`. Inside a Milestone, the merge step of `implement` and `implement-spec` reads it: a pull request crossing no boundary is an agent merge, Deep and ADR, glossary, `CLAUDE.md` and `REVIEW.md` changes included, unless the repo's own rules say a person merges it (a review that will not settle is parked, not brought to the user); outside one, the outside-a-Milestone merge list governs (ADR 0004). See `docs/agents/boundaries.md`.

### Releases

`dev-skills`' canonical version source is `plugins/dev-skills/.claude-plugin/plugin.json`; `plugins/dev-skills/.codex-plugin/plugin.json` keeps a synchronized version copy; a skill-changing pull request bumps the version and a Release does not; a Release is named, not numbered, with the label `release-m<milestone>-r<n>`, and its changelog entry records its start and end commits and the versions it delivered. See `docs/agents/release.md`.
