---
name: docs-index
description: Apply the documentation-index contract. Use when a document-writing workflow needs index format or update requirements, or when a checker assesses documentation-index drift.
user-invocable: false
---

# Docs Index

Each repo keeps one **docs index**, `docs/dev-skills/index.md`, in the folder only the skills use. It lists the docs the skills keep in the repo and the repo's own docs an agent may need, inside that folder and outside it, so an agent can open only the ones that fit its work instead of loading them all.

## Format

Group docs by **Area** (each repo picks its own, for example site, hub, trip plugin; use "Whole repo" for docs that cover everything). Under each Area heading, one bullet per doc: a link, a colon, what the doc is, then a "Read when..." sentence.

See [EXAMPLE.md](EXAMPLE.md) for a complete index with Area headings and repository-relative links.

Keep each line to one sentence of "what" and one "Read when". The "Read when" is the part that matters: it is how the agent decides whether to open the file.

## What is listed

Listed: the glossary `docs/dev-skills/glossary.md` (the map, once split) and its Area pages in `docs/dev-skills/glossary/`, ADRs in `docs/dev-skills/adr/`, the setup files in `docs/dev-skills/`, notes in `docs/dev-skills/out-of-scope/`, `REVIEW.md` at the repo root, `CONTRIBUTING.md` wherever the repo keeps it, README files, and research notes that are merged.

In a multi-context repo, per-context glossaries and per-context ADR folders also get lines in the one `docs/dev-skills/index.md`.

Not listed: `CLAUDE.md` and `AGENTS.md` files, `SKILL.md` files, code, and specs, tickets and review comments that live on the issue tracker. Research findings on a throwaway branch that is never merged get no line; a note committed to a branch that merges does. Test fixtures (data an eval or test runs against) are not listed either, even when they are Markdown files: the doc that describes a fixture gets a line, the fixture's own files get none.

## Update rule

Any skill that creates or edits a doc updates `docs/dev-skills/index.md` in the same commit:

- A **new doc** gets a line under its Area.
- An **edited doc** gets its line fixed if its subject changed.
- A **superseded ADR's** line says which ADR replaced it.
- A **deleted or renamed doc** has its line removed or re-pointed.

If there is no `docs/dev-skills/index.md` when a skill writes a doc, create it in the same commit, with a line for every doc of the kinds listed above that already exists.
