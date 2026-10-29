# Docs index

Read this first, then open only the docs whose line fits your work. Specs and tickets are GitHub issues, not files here.

## Whole repo

- [GLOSSARY.md](../GLOSSARY.md): the words used here (Plugin, Patch, Model tier, Spec, Ticket, Implementer, Finder, Verifier, Round...). Read when writing or reviewing any skill text.

## Packaging

- [README.md](../README.md): how to add the marketplace and install its plugins. Read when changing install steps.
- [dai-portal-data README](../plugins/dai-portal-data/README.md): the DAI Portal database plugin. Read only when working on that plugin.
- [dev-skills README](../plugins/dev-skills/README.md): what the plugin is, install steps, the model-tier table and the forked/own folder layout. Read when installing the plugin, adding a skill of our own, or mapping a tier to a model.
- [dev-skills PATCHES.md](../plugins/dev-skills/PATCHES.md): the Upstream commit and every change we made to Upstream text. Read before changing anything under `upstream-skills/` or merging an Upstream update.
- [ADR 0001](adr/0001-dev-skills-is-one-plugin-forked-from-matt-pocock.md): why `dev-skills` is one plugin forked from Matt Pocock's skills, and which skills it keeps. Read when adding, dropping or patching a skill.
- [ADR 0002](adr/0002-skills-name-model-tiers-not-models.md): skills name cheap, regular or premium tiers, never models. Read when a skill picks a model.

## Building

- [ADR 0004](adr/0004-build-threads-coordinate-and-subagents-code.md): build threads coordinate, Implementer subagents code, and when Lufei must review. Read when working on `implement`, `implement-spec`, `to-tickets` or `setup-project`.
- [ADR 0005](adr/0005-a-spec-is-one-long-lived-branch.md): the spec branch model, ticket worktrees and merges. Read when working on `implement-spec` or anything about branches.

## Code review

- [ADR 0003](adr/0003-code-review-runs-find-verify-rank-in-rounds.md): Find, Verify, Rank, depths and Rounds. Read when working on `code-review`, `retro` or `pr`.

## Docs

- [ADR 0006](adr/0006-docs-are-found-through-one-index.md): this index, glossary pages per area, and which skills keep the index up to date. Read when a skill writes or reads docs.
