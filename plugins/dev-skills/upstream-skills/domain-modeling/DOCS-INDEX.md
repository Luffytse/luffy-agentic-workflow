# Docs Index

Each repo keeps one **docs index**, `docs/index.md`. It lists the docs the skills keep in the repo, so an agent can open only the ones that fit its work instead of loading them all.

## Format

Group docs by **Area** (each repo picks its own, for example site, hub, trip plugin; use "Whole repo" for docs that cover everything). Under each Area heading, one bullet per doc: a link, a colon, what the doc is, then a "Read when..." sentence.

```md
# Docs index

Read this first, then open only the docs whose line fits your work.

## Whole repo

- [GLOSSARY.md](../GLOSSARY.md): the words used here (Order, Invoice, Customer...). Read when writing or naming anything.

## Billing

- [ADR 0003](adr/0003-invoices-are-immutable.md): why an issued Invoice is never edited. Read when changing how Invoices are corrected.
- [Billing glossary](glossary/billing.md): Billing's terms. Read when working in Billing.
- [.out-of-scope/dark-mode.md](../.out-of-scope/dark-mode.md): why dark mode was rejected. Read when a request touches theming.
```

Keep each line to one sentence of "what" and one "Read when". The "Read when" is the part that matters: it is how the agent decides whether to open the file.

## What is listed

Listed: glossary pages (or `GLOSSARY-MAP.md`), ADRs, `docs/agents/` setup files, `.out-of-scope/` notes, `REVIEW.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, README files, and research notes that are merged.

In a multi-context repo, per-context glossaries and per-context ADR folders also get lines in the one root `docs/index.md`.

Not listed: `CLAUDE.md` and `AGENTS.md` files, `SKILL.md` files, code, and specs, tickets and review comments that live on the issue tracker. Research findings on a throwaway branch that is never merged get no line; a note committed to a branch that merges does.

## How agents read it

Read `CLAUDE.md` (or `AGENTS.md`) and `docs/index.md`, then open only the docs whose line fits the work. If the repo has no `docs/index.md`, fall back to `GLOSSARY.md` (or `GLOSSARY-MAP.md`) and `docs/adr/`.

## Update rule

Any skill that creates or edits a doc updates `docs/index.md` in the same commit:

- A **new doc** gets a line under its Area.
- An **edited doc** gets its line fixed if its subject changed.
- A **superseded ADR's** line says which ADR replaced it.
- A **deleted or renamed doc** has its line removed or re-pointed.

If there is no `docs/index.md` when a skill writes a doc, create it in the same commit, with a line for every doc of the kinds listed above that already exists.
