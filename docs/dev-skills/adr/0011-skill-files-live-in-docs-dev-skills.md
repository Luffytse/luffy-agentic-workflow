# The files the skills require live in docs/dev-skills/

Every file the `dev-skills` skills write or read in a repo lives in one folder that only they use, the **Skill docs folder** `docs/dev-skills/`, at fixed paths the skills name directly. This replaces the layout part of [ADR 0006](0006-docs-are-found-through-one-index.md) (where the index and the glossary live); the rest of ADR 0006 stands. Decided with the user in Spec [#551](https://github.com/Luffytse/luffy-dev-skills/issues/551), from the map [#537](https://github.com/Luffytse/luffy-dev-skills/issues/537) (2026-11-03), and built in [#552](https://github.com/Luffytse/luffy-dev-skills/issues/552).

The paths came with the skills we took from Upstream and were scattered: rule files partly at the root (`REVIEW.md`, `CODING_STANDARDS.md`) and partly in `docs/agents/`, records at the root (`GLOSSARY.md`, `GLOSSARY-MAP.md`, `.out-of-scope/`) and loose in `docs/` (`docs/index.md`, `docs/adr/`, `docs/glossary/`). The user wants the skills to be public one day and to fit teammates' existing repos, not only new ones. `docs/` is a name many repos already use: `docs/index.md` is the home page of common docs-site tools, and `docs/adr/` or `docs/agents/` may already hold the repo's own records. A repo that ran `setup-dev-skills` got our files mixed into its own, at paths that can clash.

## The layout

| File | Lives | Why |
|---|---|---|
| docs index | `docs/dev-skills/index.md` | lists the docs inside the folder and outside it |
| setup rule files (tracker, triage labels, domain, release, Boundary record) | `docs/dev-skills/` | |
| glossary | `docs/dev-skills/glossary.md`; after a split its Area pages are `docs/dev-skills/glossary/<area>.md` and `glossary.md` becomes the map | the path an agent reads never moves |
| ADRs | `docs/dev-skills/adr/` | |
| out-of-scope notes | `docs/dev-skills/out-of-scope/` | no longer hidden, and indexed |
| `CLAUDE.md`, `AGENTS.md` | repo root | the coding agents load them from there; they point at the index |
| `REVIEW.md` | repo root | Claude's managed Code Review reads the same root file for the same kind of rules, with no setting to point it elsewhere |
| changelog | repo root, or each module's root when modules carry their own versions, at the path the release doc records | common convention |
| `CONTRIBUTING.md` | wherever the repo keeps it (root, `docs/`, `.github/`), never moved | it belongs to the repo's people; GitHub reads all three |
| `CODING_STANDARDS.md` | dropped | no skill seeded it, and it overlapped `REVIEW.md`'s Always check lines |

A multi-context repo keeps a glossary and ADR folder per context beside its code, as before; `docs/dev-skills/glossary.md` is then the map that points to them.

## Considered options

- **Keep the upstream paths:** they clash with existing repos' `docs/`, which is what a public skill set must avoid.
- **A configurable folder:** every skill would have to read the setting before it could find anything, and a check could not tell a right path from a wrong one. A fixed folder named after the plugin is simple to follow and to check.
- **Move `REVIEW.md` in too:** Claude's managed Code Review reads only the root file, so one file at the root keeps one set of review rules for both reviewers.

## Consequences

- No skill keeps a fallback to an old path and `setup-dev-skills` has no migration step: before Milestone 1 rolls out, this repo is the only one that uses the skills, and it moved its own files with `git mv` in #552.
- The release doc and the Boundary record are found at their fixed paths, not as "the one `CLAUDE.md` points to".
- Until "Decide when retro's proposed review rules land in REVIEW.md" ([#548](https://github.com/Luffytse/luffy-dev-skills/issues/548)) is decided, `retro` files a judgement-call rule as a Retro issue, since it no longer has `CODING_STANDARDS.md` to write.
