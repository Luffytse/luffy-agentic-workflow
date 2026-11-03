# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`docs/dev-skills/index.md`**: start here. It lists the repo's docs by Area, each with a "read when..." line. Open only the docs whose line fits your work.
- If there is no `docs/dev-skills/index.md`, fall back to:
  - **`docs/dev-skills/glossary.md`**: the glossary, or, once it is split, the map that points at one glossary page per Area (or per context). Read each one relevant to the topic.
  - **`docs/dev-skills/adr/`**: read ADRs that touch the area you're about to work in. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved. When writing a doc, load `docs-index` and apply its contract.

## File structure

Every file the skills keep lives under `docs/dev-skills/`, so it never mixes with the repo's own docs. Small repo (most repos):

```
/
├── docs/
│   └── dev-skills/
│       ├── index.md
│       ├── glossary.md
│       └── adr/
│           ├── 0001-dev-skills-is-one-plugin-forked-from-matt-pocock.md
│           └── 0002-skills-name-model-tiers-not-models.md
└── plugins/
```

Once `glossary.md` passes about 10 KB, `domain-modeling` splits it into one page per Area, and `glossary.md` stays the entry point as the map. The repo keeps one `docs/dev-skills/adr/`:

```
/
├── docs/
│   └── dev-skills/
│       ├── index.md                   ← links glossary.md and each page
│       ├── glossary.md                ← the map: one page per Area
│       ├── glossary/
│       │   ├── ordering.md
│       │   └── billing.md
│       └── adr/
└── plugins/
```

Multi-context repo (a `glossary.md` map that points into `src/`):

```
/
├── docs/
│   └── dev-skills/
│       ├── glossary.md                ← the map: one entry per context
│       └── adr/                       ← system-wide decisions
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

> _Contradicts ADR 0002 (skills name model tiers, not models), but worth reopening because…_
