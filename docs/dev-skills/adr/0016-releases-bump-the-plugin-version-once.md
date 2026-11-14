# Releases bump the plugin version once; a pull request never does

Supersedes [ADR 0008](0008-each-skill-change-bumps-the-plugin-version.md) for this repo's version rule. A pull request never changes the `dev-skills` version, a skill pull request included. The Release's changelog pull request raises it once, in every manifest that holds it, by the biggest size among the Release's changes, and the Release thread merges that pull request as the Boundary record allows. The version hand-out and the Ticket re-read after a skill merge, the two merge-time steps of ADR 0008, leave this repo's docs. Settled with the user on 2026-11-10 in the Milestone 4 workflow review (#99) and on decision cards of 2026-11-13 (#150).

## Why

ADR 0008 chose a bump per pull request on 2026-11-01 so that "a merged skill change governs the next session straight from main". That reason is gone and its costs stayed:

- **Cloud threads load the skills from the checkout** since 2026-11-08, so a merged change is in use at the next session with no bump. The version number was never what got a change loaded.
- **Skill pull requests no longer queue on the version files.** Every skill pull request edited the same two manifests, so any two conflicted and merged in a row, each waiting for a number from the coordinator (7 to 8 minutes to get one in two cases checked in Milestone 3). Builds that start side by side would have waited in a row.
- **The Ticket re-read cost more than it found.** It ran 8 times in Milestone 3, changed one issue, held new starts for 1 to 2 minutes each and cost about $0.43 a run. Every builder already reads its own issue against freshly fetched main before it builds.
- **The rules were long.** About 650 words of `CLAUDE.md` and about 1,090 words of the release doc, repeated in the coordinator instructions.

## The rule

- **A pull request leaves the version as it is on main**, whatever files it changes. It asks nobody for a number, adds no bump commit and waits for no other pull request.
- **The Release raises it once**, in the changelog pull request, in every manifest that holds it (`.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`, both, to the same version). The Claude Code manifest is the canonical source; the Codex manifest is a synchronized copy that `scripts/check-plugin.sh` checks for drift. The `Versions:` line of the changelog entry names the one new version.
- **The size is the biggest among the Release's changes**: major for a breaking change, minor for a new or changed skill, patch for fixes or reverts only. A Release that changed no file under `plugins/dev-skills/skills/` leaves the version, and its `Versions:` line says so. The release doc holds the cut steps.
- **The Release thread merges the changelog pull request** as the Boundary record allows; no cut waits for the user. A merged version bump is not a one-way door in this repo: a bad merged change is reverted on main at once and the revert is a patch-size change in the next Release. The plugin's own "Releases bump" text, which has the user merge a bump pull request as a one-way door, stays a first draft for other projects; this repo's release doc stands on its own.
- **No Ticket re-read after a skill merge.** An issue nobody is building stays as written until its builder's check against main, or a triage, reads it.

## What each part of X.Y.Z means

Carried over from ADR 0008. Versions follow semantic versioning (semver.org), with "breaking" defined for skills:

- **patch (Z):** a fix. A skill now does what it already promised, and no project using the plugin has to change anything. A revert is a patch.
- **minor (Y):** a new or changed skill that breaks nothing, such as a new skill or a new step or option in one.
- **major (X):** a breaking change, meaning a project using the plugin must do something: a skill is renamed or removed, the format of a repo doc that `setup-dev-skills` writes changes, or a label the skills need changes.

While the plugin was below 1.0.0, a breaking change bumped the minor part instead. From 1.0.0 on it bumps the major part. Either way, the Release's `CHANGELOG.md` entry says what a project must do.

**1.0** is the autonomous Milestone workflow. The user declared it stable on 2026-11-04 at the end of Milestone 1 (#396), before the three proof Milestone runs; those still follow Milestone 1 and a failed run is filed as a bug, but they no longer gate the version.

## What is given up

- A Retro names the pull request or commit that went wrong, not a version.
- A revert takes no number of its own.
- An installed copy (another project, a local install) updates once per Release, not once per skill merge.
- The notes the re-read left for builders on issues nobody was building.

## Considered options

- **Keep a bump per pull request** (ADR 0008). Kept the queue and the re-read for a benefit cloud threads no longer need.
- **Drop `version` from `plugin.json`.** Claude Code would then version the plugin by commit, but a commit hash is not a version a Release or a project can name and order.
- **The user merges the bump pull request**, as the plugin's "Releases bump" text says. This repo's Boundary record needs no approval for a merged version bump, so a cut would wait for the user for no boundary.

## Consequences

- ADR 0008 is marked superseded and keeps its text as history; its "How a Release works" Release definition still stands, amended by ADR 0012 and this one.
- ADR 0012 gets an amendment note: this repo's versioning policy is Releases bump, and the cut steps add the bump and the `Versions:` line.
- `scripts/check-plugin.sh` drops its `no-repo-merge-rules` check, which guarded skill text against naming the two rules above, with its test cases.
- The plugin's `release` and `setup-dev-skills` text is not changed here; #143 removes versioning policy text from the plugin later, and the Codex manifest goes with #123, so the cut still names both manifests.
- The project's coordinator instructions describe the hand-out and the re-read until `setup-project` is re-run at the end of Milestone 4.
- Past changelog entries, which record versions delivered one per pull request, stay as written.

*Amendment note, 2026-11-14, Spec #151.* Removing the Codex packaging is a breaking change: a project that installed the plugin in Codex must do something, because that install stops updating (ADR 0001). The Release that carries Spec #151 is therefore cut as a major version (2.0.0), whatever else it holds. The Codex manifest is gone, so the cut names one manifest, `.claude-plugin/plugin.json`, and the drift check against a synchronized copy, with the `codex-packaging` check, is gone with it.
