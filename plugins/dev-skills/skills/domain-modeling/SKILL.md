---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing the glossary (docs/dev-skills/glossary.md or its Area pages), or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* the glossary for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Every file this skill writes lives under `docs/dev-skills/`, the folder only the skills use, so it never mixes with the repo's own docs. Most repos have a single context:

```
/
├── docs/
│   └── dev-skills/
│       ├── index.md
│       ├── glossary.md
│       └── adr/
│           ├── 0001-event-sourced-orders.md
│           └── 0002-postgres-for-write-model.md
└── src/
```

A repo whose glossary was split per Area keeps `docs/dev-skills/glossary.md` as the entry point, now the map, with one page per Area in `docs/dev-skills/glossary/`, still with one `docs/dev-skills/adr/`:

```
/
├── docs/
│   └── dev-skills/
│       ├── index.md
│       ├── glossary.md               ← the map: one page per Area
│       ├── glossary/
│       │   ├── ordering.md
│       │   └── billing.md
│       └── adr/
└── src/
```

If `docs/dev-skills/glossary.md` is a map that points into `src/`, the repo has multiple contexts. The map points to where each one lives, and each context keeps its glossary beside its code:

```
/
├── docs/
│   └── dev-skills/
│       ├── glossary.md               ← the map: one entry per context
│       └── adr/                      ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

If `docs/dev-skills/glossary.md` holds terms and grows past about 10 KB (10,240 bytes; check with `wc -c`) when you add a term, split it per Area (see [Splitting the glossary](#splitting-the-glossary)). The repo still keeps one `docs/dev-skills/adr/`.

Create files lazily: only when you have something to write. If `docs/dev-skills/glossary.md` does not exist, create it when the first term is resolved. If no `docs/dev-skills/adr/` exists, create it when the first ADR is needed.

## Splitting the glossary

Do this only in a single-context repo whose `docs/dev-skills/glossary.md` holds the terms, when you are adding a term and that file is over about 10 KB. Check the size with `wc -c docs/dev-skills/glossary.md`; do not split before then.

1. Group the terms by Area (the same Areas the docs index uses).
2. `git mv docs/dev-skills/glossary.md` to the first Area's page (`docs/dev-skills/glossary/<area>.md`) so history follows, then move the other groups into their own pages.
3. Write a new `docs/dev-skills/glossary.md` as the map, listing one page per Area (format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)). The entry point keeps its path, so skills that read `docs/dev-skills/glossary.md` find the pages from it.
4. Change the glossary's line in the docs index to say it is now the map, add a line for each Area page, and fix any other doc that links a term's old place. Load `docs-index` for the index update, including creation when absent.

If `docs/dev-skills/glossary.md` is already a map (split per Area, or a multi-context layout), add the term to the page the map points to for its Area or context; never put terms back into the map or split again just because a map exists. A page that grows past about 10 KB splits again by sub-area, and the map gets the new page.

## Keeping the docs index current

When creating or editing a glossary or ADR, load `docs-index` and apply its contract.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in the glossary, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update the glossary inline

When a term is resolved, update the glossary (`docs/dev-skills/glossary.md`, or the Area page it points to once it is the map) right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

The glossary should be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
