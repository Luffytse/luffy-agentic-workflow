# `release` is version-free and command-free, and a Release is a step of a Milestone

The `release` skill knows no version policy and names no tracker command. It checks the current Release shipped, writes the changelog entry for everything merged since the last Release, runs the **cut steps** and whole-Release check the repo's release doc lists, closes the Release, runs `triage` (the Triage batch) and `retro-planning`, and plans the next Release from one **ranked list**, picked from the top up to the release doc's **Release size**. Every plan is a Milestone: a small Release is a Milestone with one Release. Settled with the user on 2026-11-03 in the planning thread "Plan splitting the release skill" (Spec #633, answering #617).

## Why

`release` had grown to 6,919 words, over the Boundary record's 5,000-word limit, and most of it was not Release work: two whole versioning policies (semver sizes, the bump pull request, label renames, version collisions between open Releases, the urgent patch Release), a separate "inside a Milestone" path whose detection rule was copied into `triage` and `retro-planning`, and 19 GitHub commands. Each repo versions differently or not at all, a repo with no version could not use `release`, and parsing `triage`'s and `retro-planning`'s records tied `release` to their layout.

## Decisions

- **Version-free.** A Release has a name (the release doc's name form; setup's default `Release <n>`), never a version. Each repo's versioning policy (none, pull requests bump, Releases bump) is written into its own release doc by `setup-dev-skills`, as cut steps the skill runs in order; a cut step wins over the skill's own text. A repo that bumps records the versions delivered in the changelog entry. No label renames, no version comparisons.
- **No urgent Release.** A fix that cannot wait is built and merged like any issue, and the next Release's changelog lists it. A release doc may give a step between Releases.
- **Command-free.** The skill says what to find or do; agents already know how to list, read and label issues. Rules with real meaning stay as rules, such as the shipped test (a merged pull request into the default branch closed the issue with a closing keyword; a close by hand or "does not close #n" does not count). The tracker doc keeps only the traps an agent would not know.
- **A Release is a step of a Milestone.** Planning always involves the user (the Milestone's goal and features, with `milestone`); everything after it is agentic. There is no separate "inside a Milestone" path.
- **One shared mark.** `next-release`, a role in the triage label doc, is set by `triage` and `retro-planning` and read and cleared by `release`, so no skill parses another skill's records.
- **One ranked list.** Group 1: severe issues and issues marked `next-release`. Group 2: the Milestone's features, re-ordered at every planning (dependencies first, then what moves the goal furthest, the original order breaking ties), each preceded by its open blockers. Group 3: `ready-for-agent` bugs, oldest first. An issue meeting several conditions goes in its highest group, first within it. A feature the Milestone issue does not list is never ranked.
- **Release size.** Items of any kind (a Spec with its Tickets is 1, a lone Ticket 1, a bug 1), set per repo (setup's default 5, this repo 10). A severe issue joins past it. The release issue records the order with a reason per entry, the size used, and what was left out and why.

## Considered options

- **Split `release` into a main file and mode references** (#617's first proposal). It kept two version policies in the plugin and the separate Milestone path, and only moved the words.
- **Keep the 5-feature cap and maintenance fixes outside it.** Bugs outside the Milestone's features never shipped until planned, and "touches a feature" fitted almost every fix (Retro #461).

## Consequences

- `release/SKILL.md` is back under 5,000 words and off `known_over` in `scripts/check-plugin.sh`.
- ADR 0008's version rule for this repo stands; its "How a Release works" is amended by this ADR. This repo's version hand-out and Ticket re-read stay in `CLAUDE.md` and `docs/dev-skills/release.md`.
- Existing repos rerun `setup-dev-skills` to gain the release doc's new fields (versioning policy, Release size, cut steps) and the `next-release` label.
