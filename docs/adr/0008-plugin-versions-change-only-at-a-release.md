# Plugin versions change only at a release

A plugin's version changes only when the user cuts a **Release**, never in an ordinary pull request. Until now every pull request under `plugins/<name>/` bumped the version, took the next Patch and check numbers, wrote `TBD-N` placeholders during review and took the real numbers at merge time. Any two parallel pull requests collided on all three counters, so the numbering step, its retake-on-repeat rule, four checks in `check-plugin.sh` and a review Round for the numbers commit grew up around that collision, and CI was red by design on every push in review (Retro issues #171, #182, #227, #239). A Release groups a few features and bumps once, so ordinary pull requests carry no number another branch could take. It also slows how often the plugin changes, which the user wants as the skills settle.

Amended 2026-10-31 for Codex packaging (#342): `dev-skills` has a Claude Code manifest at `.claude-plugin/plugin.json` and a Codex compatibility manifest at `.codex-plugin/plugin.json`, both under `plugins/dev-skills/`. They read the same `skills/` tree. The Claude Code manifest remains the canonical source for reading the current version and locating the last Release in git history; the Codex manifest is a synchronized copy whose creation is not a Release boundary. Their name and version stay equal, and only a Release's bump pull request changes both version fields together. The second manifest makes Codex's skill path explicit without changing Claude Code's manifest or duplicating skills; `scripts/check-plugin.sh` checks identity and path drift. Ordinary pull requests leave both versions alone.

## How a release works

- A Release has one release issue (its goal in one sentence, and later its notes) and a label, `release-X.Y.Z`, on every issue it ships. The label, not a sub-issue link, marks membership, because an issue has only one parent and a Spec's Tickets already have theirs. A Release holds at most 5 features, unless the user raises the cap for that Release. A feature is one piece of work the user would name as one thing: a Spec with all its Tickets, a lone Ticket with the issues it absorbs, or a few related issues the user agrees to treat as one; every issue in it carries the label. (Amended 2026-10-31: the cap first counted issues, a Spec as one. The user chose to count features, because small fixes that triage bundles and related bugs each took a slot and filled the cap with pieces of one thing.)
- Each issue in it is built as before, by its own Ticket or Spec thread, and merges to main with no version change. Installed copies of the plugin do not update until the version changes, so main can run ahead of the last Release.
- The coordinator starts Build threads only on issues carrying the current release label. Any issue filed during a Release, by hand or by a skill such as `to-spec`, `to-tickets`, `triage` or `retro-planning`, waits for the next Release planning, except Tickets split from a Spec already in the Release, which take its label.
- Once every labelled issue is closed, a **Release thread** (premium tier) opens the bump pull request with a `CHANGELOG.md` entry; the user merges it. The same thread then runs the **Release planning** for the next Release: it proposes a goal and a scope of features from the open `ready-for-agent` issues and anything carried over, and labels only what the user approves.
- A fix that cannot wait gets its own patch Release, cut as soon as it merges if everything on main since the last Release fits a patch. If larger changes are already on main, wait for the planned Release to be cut, then reconsider the urgent Release from fresh main; an urgent Release always stays patch-only (clarified 2026-10-31, #327).
- The general flow lives in a `release` skill. Each repo's specifics (where its version lives, its changelog path, its label prefix) live in a repo doc that `setup-dev-skills` writes, so the skill names no project.

## What each part of X.Y.Z means

Versions follow semantic versioning (semver.org), with "breaking" defined for skills:

- **patch (Z):** fixes only. A skill now does what it already promised, and no project using the plugin has to change anything.
- **minor (Y):** something new that breaks nothing, such as a new skill or a new step or option in one.
- **major (X):** a breaking change, meaning a project using the plugin must do something: a skill is renamed or removed, the format of a repo doc that `setup-dev-skills` writes changes, or a label the skills need changes.
- Typos, ADRs and repo-only changes ride along in the next Release and never decide its size.

The Release thread picks the bump from the biggest change that shipped, and the user confirms it in the bump pull request. While the plugin is below 1.0.0, a breaking change bumps the minor part instead, and its `CHANGELOG.md` entry says what a project must do. 1.0.0 is cut only when the user declares the skills stable.

## Considered options

- **Drop `version` from `plugin.json`.** Claude Code then versions a plugin in a git-hosted marketplace by its commit, so every merge would update installed copies. It removes the collision, but every merge would still ship to every project at once, which is what the user wants to slow down.
- **Keep per-pull-request bumps and let CI write them after merge.** It removes the placeholders but keeps a version per merge, and needs workflow changes the cloud cannot push.
- **One Spec branch per Release.** `implement-spec` merges a Spec at its end (ADR 0005), so every merge in the Release would wait for the last one and bring back the conflicts this decision removes.
- **GitHub milestones for membership.** No skill reads them, and the user may move to another tracker; a label exists almost everywhere.

## Consequences

- `CLAUDE.md`'s bump and `TBD-N` rules, the numbering steps of `implement` and `implement-spec`, and the checks that enforce them go away in a switch-over Ticket. Until it merges, they still govern every pull request.
- With the version gone from pull requests, the Patch and check numbers are the only counters left. The user decided in the same planning to make Upstream's skills our own (moving them into `skills/` and dropping `PATCHES.md`, changing ADR 0001) and to keep only structural checks in `check-plugin.sh`, so neither counter survives.
- `CHANGELOG.md` becomes the record of what changed, shipped with the plugin.
