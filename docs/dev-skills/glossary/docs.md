# Docs

Where the skills keep their files in a repo and how an agent finds them. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Skill docs folder**:
The one folder in a repo that only the skills use, `docs/dev-skills/`, holding every file they require at a fixed path: the Docs index, the setup files, the glossary and its Area pages, ADRs and out-of-scope notes. Files that coding agents, other tools or people expect elsewhere stay outside it, such as `CLAUDE.md`, `AGENTS.md`, `REVIEW.md` and the changelog (ADR 0011).
_Avoid_: skills folder (the plugin's own `skills/`), agents folder

**Docs index**:
The page `docs/dev-skills/index.md`, in the Skill docs folder, that lists every doc the skills keep in a repo and the repo's own docs an agent may need, inside the folder and outside it, grouped by Area, each with one line saying when to read it. Agents read it first and open only what their work needs. Owned by `docs-index`.
_Avoid_: README, table of contents

**Area**:
One part of a project that docs are grouped by in the Docs index, such as site, hub or trip plugin. A large glossary is split into one page per Area (`domain-modeling`).
_Avoid_: section, module
