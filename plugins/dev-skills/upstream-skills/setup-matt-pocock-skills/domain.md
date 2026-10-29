# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`docs/index.md`**: start here. It lists the repo's docs by Area, each with a "read when..." line. Open only the docs whose line fits your work.
- If there is no `docs/index.md`, fall back to:
  - **`GLOSSARY.md`** at the repo root, or **`GLOSSARY-MAP.md`** at the repo root if it exists: it points at one glossary page per Area (or per context). Read each one relevant to the topic.
  - **`docs/adr/`**: read ADRs that touch the area you're about to work in. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved. Any skill that writes a doc adds or fixes its line in `docs/index.md` in the same commit.

## File structure

Small repo (most repos):

```
/
├── GLOSSARY.md
├── docs/
│   ├── index.md
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

Once `GLOSSARY.md` passes about 10 KB, `domain-modeling` splits it into one page per Area. The repo keeps one `docs/adr/`:

```
/
├── GLOSSARY-MAP.md                    ← lists one page per Area
├── docs/
│   ├── index.md                       ← links GLOSSARY-MAP.md
│   ├── glossary/
│   │   ├── ordering.md
│   │   └── billing.md
│   └── adr/
└── src/
```

Multi-context repo (a `GLOSSARY-MAP.md` that points into `src/`):

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in the glossary. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders), but worth reopening because…_
