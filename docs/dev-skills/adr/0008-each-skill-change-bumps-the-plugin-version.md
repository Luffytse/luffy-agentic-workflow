# Each skill change bumps the plugin version

> **Superseded by [ADR 0016](0016-releases-bump-the-plugin-version-once.md)** (2026-11-14, Ticket #150, absorbing #99): a pull request no longer bumps the version; the Release's changelog pull request raises it once, and the version hand-out and the Ticket re-read are dropped. This ADR keeps its text below as history; the semver meanings of X.Y.Z and the 1.0 declaration carried over to ADR 0016.

Every pull request that changes a skill bumps the `dev-skills` version when it merges, so a merged skill change governs the next session straight from main and a retro can name the version that went wrong. A **Release** no longer marks a version: it is a named step inside a Milestone, with its own name, and it writes the changelog for the versions it delivered. Settled with the user on 2026-11-01 in [Define safe adoption of each evolving skill revision](https://github.com/Luffytse/luffy-dev-skills/issues/384#issuecomment-6556373083) and item 7 of [Reconcile delivery approvals with Milestone authority](https://github.com/Luffytse/luffy-dev-skills/issues/385#issuecomment-6556848716).

## History

On 2026-10-31 this ADR said the opposite: a version changed only when the user cut a Release, in a bump pull request. Before that, every pull request under `plugins/<name>/` bumped the version during review, wrote `TBD-N` placeholders and took the real numbers at merge, so any two parallel pull requests collided (Retro issues #171, #182, #227, #239). Release-only bumps ended the collisions and slowed how often the plugin changed. The Patch and check counters went away in the same planning (ADR 0001; checks in `scripts/check-plugin.sh` take names), and they stay gone.

On 2026-11-01 the user chose speed instead: a skill change should be in use from the next session, so a bad one shows up fast, and retros "mention in which version the skills has a problem". The collisions stay away because the number is handed out once, at merge time, not held on a branch during review.

## The version rule

- **What counts as a skill change.** A pull request that changes any file under `plugins/dev-skills/skills/`. Other files under `plugins/dev-skills/` (the README, `CHANGELOG.md`, the manifests' other fields) take no bump of their own and ride along with the next bump. Files outside the plugin (ADRs, the glossary, `evals/`, `scripts/`) never take a bump. `dai-portal-data` has no release doc, so its version is left as it is.
- **During review** a branch leaves the version as it is on main, so no number is held and parallel branches never collide.
- **At merge.** Just before merge, the coordinator hands out the next number (main's version, raised by the change's kind below) and merges skill-changing pull requests one at a time. The merging thread adds the bump as the pull request's last commit, then merges. These steps, and the re-read of open Tickets after a skill merge, are this repo's own rules (settled with the user on 2026-11-03: "it's specific for this repo and specific for this period of time"): they live in `CLAUDE.md` ("Merge-time steps") and `docs/dev-skills/release.md`, and no skill states them. The "pull requests bump" mode stays generic, a project may choose it in its release doc; skills only say to follow the merge-time steps the repo's own docs give.
- **Both manifests.** `dev-skills` has a Claude Code manifest at `.claude-plugin/plugin.json` and a Codex compatibility manifest at `.codex-plugin/plugin.json` (amended 2026-10-31 for Codex packaging, #342). They read the same `skills/` tree, and their name and version stay equal: a bump changes both version fields together. The Claude Code manifest is the canonical source for the current version; the Codex manifest is a synchronized copy, and its creation was not a Release. `scripts/check-plugin.sh` checks identity and path drift.
- **Recovery.** A bad merged change is reverted on main at once, and the revert takes the next number. It is then fixed properly. The user is told; nobody waits for them.
- **Which version governs.** A merged skill change governs the next session, from main; there is one branch and no `develop` branch. A pull request that edits a skill is built and reviewed under main's version of that skill. A running thread keeps the version it started with until its Ticket or Spec is done ([#384](https://github.com/Luffytse/luffy-dev-skills/issues/384#issuecomment-6556373083), items 3 and 5).
- **Sessions verify what they loaded.** Before starting work, a session verifies and records the skill version and source revision it actually loaded, refreshes them if they are not the intended ones, and reports a blocker if it cannot ([follow-up](https://github.com/Luffytse/luffy-dev-skills/issues/384#issuecomment-6563760462)). The version number alone is not evidence of what was loaded.

## What each part of X.Y.Z means

Versions follow semantic versioning (semver.org), with "breaking" defined for skills:

- **patch (Z):** a fix. A skill now does what it already promised, and no project using the plugin has to change anything. A revert is a patch.
- **minor (Y):** a new or changed skill that breaks nothing, such as a new skill or a new step or option in one.
- **major (X):** a breaking change, meaning a project using the plugin must do something: a skill is renamed or removed, the format of a repo doc that `setup-dev-skills` writes changes, or a label the skills need changes.

While the plugin was below 1.0.0, a breaking change bumped the minor part instead. From 1.0.0 on, a breaking change bumps the major part. Either way, the Release's `CHANGELOG.md` entry says what a project must do.

**1.0** is the autonomous Milestone workflow ([Define the Milestone agreement and completion boundary](https://github.com/Luffytse/luffy-dev-skills/issues/383)). It was to be cut after the three proof Milestone runs of [Define the evidence required to declare 1.0 stable](https://github.com/Luffytse/luffy-dev-skills/issues/387#issuecomment-6563675991) passed and the user declared it (amended below); a failed run is filed as a bug and repeated after the fix ([#391 comment](https://github.com/Luffytse/luffy-dev-skills/issues/391#issuecomment-6563676756)).

Amended 2026-11-04: the user declared 1.0 stable at the end of Milestone 1 (#396), after its last Release was cut, and asked to ship it as 1.0.0. The three proof Milestone runs had not run yet. They still follow Milestone 1, as #396's exclusions say, and a failed run is still filed as a bug. They no longer gate the version.

## How a Release works

Amended 2026-11-04 by [ADR 0012](0012-release-is-version-free-and-command-free.md): `release` is version-free and command-free, every plan is a Milestone, and the next Release is picked from one ranked list up to the release doc's Release size. The bullets below are updated to match.

- **A Release is a named step inside a Milestone.** Agents plan each one from the ranked list, up to the release doc's Release size (10 here), counted in items: a Spec with all its Tickets is 1, a lone Ticket 1, a bug 1; a severe issue joins past the size. (Amended 2026-10-31: the cap first counted issues; amended 2026-11-04, ADR 0012: the 5-feature cap became the Release size.)
- **Its identity is independent of the version** ([follow-up](https://github.com/Luffytse/luffy-dev-skills/issues/385#issuecomment-6563881387)). A Release has its own name, for example "Milestone 1 · Release 1", and one release issue holding its goal and later its notes. At its end it records its start and end commits and the versions it delivered. Per-PR bumps do not rename it or change its membership.
- **Membership is a label**, `release-m<milestone>-r<n>` (for example `release-m1-r1`), on every issue in it. A label, not a sub-issue link, because an issue has only one parent and a Spec's Tickets already have theirs. The coordinator starts Build threads only on issues carrying the current release label. An issue filed during a Release waits for the next Release planning, except Tickets split from a Spec already in the Release, which take its label. Agents plan each Release's scope themselves from the ranked list; issues the Triage batch or Release-end Retro planning mark `next-release` (since 2026-11-14, Ticket #160, only the Triage batch marks) rank first and fill places like any item, and the user plans any feature the Milestone issue does not list.
- **The Release thread** (premium tier) runs once every labelled issue is closed. It writes the `CHANGELOG.md` entry for everything since the last Release, listing the versions delivered, and runs a whole-Release check, including a clean-up pass. It then closes the release issue, runs the Triage batch and the Release-end Retro planning, and plans the next Release.
- **Whether a Release also bumps is set per project**, in its release doc's versioning policy (none, pull requests bump, Releases bump), whose text becomes the cut steps. In this repo skill-changing pull requests bump, so a Release opens no bump pull request. In a typical product the Release bumps.
- **No urgent patch Release.** A fix ships in its own pull request with its own patch bump, and the next Release's changelog lists it; the urgent patch Release (clarified 2026-10-31, #327) is gone from `release` for every repo (ADR 0012).
- The general Release flow lives in the `release` skill; Milestone planning and its report live in the `milestone` skill (#385 item 1, implemented by #406), and delivery in the `team-lead` skill (ADR 0010). Each repo's specifics (its versioning policy, changelog path, name form, Release size and cut steps) live in a repo doc that `setup-dev-skills` writes, so the skill names no project.

## Considered options

- **Bump only at a Release.** Chosen on 2026-10-31, reversed on 2026-11-01: a change waited for the next Release before any session used it, and each Release added a bump pull request for the user to merge.
- **Adopt at the next Release, through a `develop` branch.** Chosen first in the #384 grilling, then reversed for speed.
- **Bump on each branch during review.** The practice before 2026-10-31: parallel branches collided on numbers. Handing out the number at merge removes that.
- **Drop `version` from `plugin.json`.** Claude Code would then version the plugin by commit. It removes collisions, but a commit hash is not a version a retro or a session record can name and order.
- **Let CI write the bump after merge.** It needs workflow changes the cloud cannot push, and the number would arrive after the merge, not with it.
- **GitHub milestones for Release membership.** No skill reads them, and the user may move to another tracker; a label exists almost everywhere.

## Consequences

- Every skill merge is a new version that installed copies can update to, so the latest version stays close to main.
- The `release` skill reads no version policy (ADR 0012, replacing #397's two bump modes in the skill): it writes the changelog entry in a changelog pull request and runs the release doc's cut steps, which here add the `Versions:` line and change no version. The skills `implement` and `implement-spec` follow the repo's merge-time steps, which add the bump at merge here (#421), and `setup-dev-skills`' release doc seed holds the text of each versioning policy.
- Release history up to 0.25.0 is found by version changes in the Claude Code manifest. From Milestone 1 · Release 1 on, it is found in each Release's changelog entry and release issue notes, whose `Versions:` and `Commits:` line records the versions delivered and the start and end commits.
- `CHANGELOG.md` stays the record of what changed, one entry per Release, shipped with the plugin.
