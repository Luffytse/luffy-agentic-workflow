---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing the glossary (GLOSSARY.md, GLOSSARY-MAP.md or its pages), or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* the glossary for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

A repo whose glossary was split per Area has a `GLOSSARY-MAP.md` and `docs/glossary/<area>.md` pages instead of the root `GLOSSARY.md`, still with one `docs/adr/`:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   ├── index.md
│   ├── glossary/
│   │   ├── ordering.md
│   │   └── billing.md
│   └── adr/
```

If a `GLOSSARY-MAP.md` exists at the root and points into `src/`, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

If the root `GLOSSARY.md` grows past about 10 KB (10,240 bytes; check with `wc -c`) when you add a term, split it per Area (see [Splitting the glossary](#splitting-the-glossary)). The repo still keeps one `docs/adr/`.

Create files lazily: only when you have something to write. If neither `GLOSSARY.md` nor a `GLOSSARY-MAP.md` exists, create a root `GLOSSARY.md` when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## Splitting the glossary

Do this only in a repo with a single root `GLOSSARY.md`, when you are adding a term and that file is over about 10 KB. Check the size with `wc -c GLOSSARY.md`; do not split before then.

1. Group the terms by Area (the same Areas the docs index uses).
2. `git mv GLOSSARY.md` to the first Area's page (`docs/glossary/<area>.md`) so history follows, then move the other groups into their own pages. The root `GLOSSARY.md` goes away.
3. Write `GLOSSARY-MAP.md` at the repo root, listing one page per Area (format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)). Skills that already read `GLOSSARY-MAP.md` find the pages from it.
4. Replace the `GLOSSARY.md` line in the docs index with a line linking `GLOSSARY-MAP.md`, and fix any other doc that links `GLOSSARY.md`. If there is no `docs/index.md` yet, create it now ([DOCS-INDEX.md](./DOCS-INDEX.md)).

If `GLOSSARY-MAP.md` already exists (split per Area, or a multi-context layout), add the term to the page the map points to for its Area or context; never create a root `GLOSSARY.md` or split again just because a map exists. A page that grows past about 10 KB splits again by sub-area, and the map gets the new page.

## Keeping the docs index current

When you create a doc, or edit one whose subject changed, update its line in `docs/index.md` in the same commit (see [DOCS-INDEX.md](./DOCS-INDEX.md)).

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

When a term is resolved, update the glossary (`GLOSSARY.md`, or the Area page `GLOSSARY-MAP.md` points to) right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

The glossary should be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
