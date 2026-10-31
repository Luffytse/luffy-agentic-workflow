# Docs are found through one index

Each repo keeps one **docs index**, `docs/index.md`, in the style of an LLM wiki. It lists every doc the skills keep in the repo, grouped by **Area** (each repo picks its own, for example site, hub, trip plugin), each with one line saying when to read it. That covers the glossary pages, ADRs, `docs/agents/` setup files, `.out-of-scope/` notes, `REVIEW.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, README files and research notes that are merged. `CLAUDE.md` files, `SKILL.md` files and code are not listed. Test fixtures (data an eval or test runs against) are not listed either, even when they are Markdown files: the doc that describes a fixture gets a line, the fixture's own files get none. An agent reads `CLAUDE.md` and the index, then opens only the docs whose line fits its work. We chose this because the docs Matt Pocock's skills write keep growing while each agent needs only a few of them, and every page loaded for nothing is context the agent can't use for its work.

## How it works

- **Glossary pages.** The glossary stays one `GLOSSARY.md`. When `domain-modeling` adds a term and `GLOSSARY.md` is over about 10 KB (its size in bytes), it splits the glossary into one page per Area, with Upstream's `GLOSSARY-MAP.md` listing the pages so the skills that already read the map find them, and the index links the map. Unlike Upstream's multi-context layout, the repo keeps one `docs/adr/`. luffydev's glossary is 8 KB today.
- **Every skill that creates or edits a doc updates the index** in the same commit: a new doc gets a line, an edited doc's line is fixed if its subject changed, and a superseded ADR's line says which ADR replaced it. The rule is written once, in `domain-modeling/DOCS-INDEX.md`, and each skill that writes docs links to it: `domain-modeling` (also used by `grill-with-docs`, `wayfinder` and `triage` for their glossary and ADR edits), `improve-codebase-architecture`, `triage` (`.out-of-scope/`), `retro` (`REVIEW.md`, `CODING_STANDARDS.md`), `setup-dev-skills` (`docs/agents/`, and it creates `docs/index.md` in a new repo) and `research`. Research findings on a throwaway branch that is never merged, as `wayfinder` uses, get no index line; only a note committed to a branch that merges does.
- **Every skill that reads docs starts at the index** instead of reading every glossary page or listing `docs/adr/`: `tdd`, `diagnosing-bugs`, `improve-codebase-architecture`, `pr`, `to-spec`, `to-tickets`, `triage`, `grill-with-docs`, `wayfinder`, `implement`, `implement-spec` and `agentic-review`. The shared rule they follow, Upstream's `docs/agents/domain.md` template, is changed to say "start at `docs/index.md`".
- **Drift check.** The standards Finder in `agentic-review` flags, as a Bug class, a doc added or renamed without its index line and an index line pointing at a missing file.
- Specs, tickets, the wayfinder map and review comments live on GitHub, so the index does not list them. `setup-project` writes project instructions, not repo files; the instructions it drafts tell build threads to start at `docs/index.md`.

## Considered options

- **Keep Upstream's habit** (read the whole glossary, list `docs/adr/` and guess from file names): fine for a few docs, but the glossary is read whole by nearly every skill and grows with every grilling.
- **A separate doc-index skill:** a skill that only runs when started would be forgotten; the rule has to live in the skills that write docs.
- **Split the glossary now:** with one 8 KB glossary the split saves little and adds pages to keep in step.

## Consequences

- `domain-modeling` gains `DOCS-INDEX.md` (the index format and update rule) and the glossary split. The writing and reading skills above link to it, and the `docs/agents/domain.md` template points at the index. All are Patches.
- luffydev gets a `docs/index.md` by hand, its `docs/agents/domain.md` is updated to match, and its `CLAUDE.md` points at the index, as this repo's does.
