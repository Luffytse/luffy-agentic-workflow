---
name: grill-with-docs
description: "Interview the user relentlessly about a plan or design, recording glossary terms and ADRs as decisions settle. Use when the user says \"grill me\" or wants a plan or design stress-tested while working in a repo."
---

Call the Skill tool twice, for "grilling" and "domain-modeling".

When you explore the repo, start at `docs/index.md` and open only the docs that fit (with no index, fall back to `GLOSSARY.md` or `GLOSSARY-MAP.md`, and `docs/adr/`). For glossary and ADR edits, follow `domain-modeling` and load `docs-index`.

When the plan renames or reworks a skill, the first fact to gather is what every other skill expects of that skill (what they call it, load it for, or rely on it to do).
