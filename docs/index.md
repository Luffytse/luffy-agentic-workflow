# Docs index

Read this first, then open only the docs whose line fits your work. Specs and tickets are GitHub issues, not files here.

## Whole repo

- [GLOSSARY.md](../GLOSSARY.md): the words used here (Plugin, Model tier, Spec, Ticket, Release, Implementer, Finder, Verifier, Round, Retro issue...). Read when writing or reviewing any skill text.

## Agent setup

- [docs/agents/issue-tracker.md](agents/issue-tracker.md): this repo's issues live on GitHub, and the commands for issues, sub-issues, blocking and adding a line to an existing issue body. Read when a skill creates, reads, edits the body of, labels or closes an issue.
- [docs/agents/triage-labels.md](agents/triage-labels.md): the label string for each triage role, the optional agent-only role with this repo's `claude-only` and `codex-only` labels, and the labels that are not triage roles. Read when applying or filtering triage labels, or before working an issue that carries an agent label.
- [docs/agents/domain.md](agents/domain.md): the single-context doc layout and how skills read the glossary and ADRs. Read when a skill looks for domain docs or flags an ADR conflict.
- [docs/agents/release.md](agents/release.md): the release doc: `dev-skills`' canonical version and Release history source, its synchronized Codex version copy, its `CHANGELOG.md` path, the `release-` label prefix and the extra steps of a bump pull request. Read when running the `release` skill or giving an issue a release label.
- [docs/agents/upstream-watch.md](agents/upstream-watch.md): the prompt of the Upstream watch, run by hand every 2 weeks from a reminder issue (reads `mattpocock/skills` since the README's last commit, files one `needs-triage` issue), the access it needs, how the commit is recorded, and how the reminder issue that starts each run works. Read when running or changing the watch.

## Packaging

- [README.md](../README.md): Claude Code and Codex marketplace install, update and local-development steps. Read when changing install steps.
- [dai-portal-data README](../plugins/dai-portal-data/README.md): the DAI Portal database plugin. Read only when working on that plugin.
- [dev-skills README](../plugins/dev-skills/README.md): what the plugin is, Claude Code and Codex install, update and local-development steps, the model-tier table, the folder layout and the last Upstream commit looked at. Read when installing the plugin, adding a skill of our own, or mapping a tier to a model.
- [DOCS-INDEX.md](../plugins/dev-skills/skills/domain-modeling/DOCS-INDEX.md): the docs index format and update rule every writing skill follows. Read when changing how skills keep `docs/index.md` current.
- [scripts/check-plugin.sh](../scripts/check-plugin.sh): this repo's own checker for the `dev-skills` layout and repo-wide rules (no vendor model names, no person names, no repo-only text in skill text, skill name matching its folder, Codex packaging matching Claude Code and sharing its skills tree); its header lists the checks, each identified by a name, never a number. A check tests structure, not a skill's wording. It lives outside the plugin so it does not ship to projects. Read when adding or changing a check, or before pushing a plugin change.
- [ADR 0001](adr/0001-dev-skills-is-one-plugin-forked-from-matt-pocock.md): why `dev-skills` is one plugin that began as Matt Pocock's skills and is now our own, and which skills it keeps. Read when adding or dropping a skill, or when the Upstream watch finds an idea.
- [ADR 0002](adr/0002-skills-name-model-tiers-not-models.md): skills name cheap, regular or premium tiers, never models. Read when a skill picks a model.
- [ADR 0009](adr/0009-shared-rules-have-one-owner-skill.md): planned ownership of shared contracts, complete workflow reuse, the loading gate and gradual migration; existing rules govern until their migrations land, and menu hiding is optional. Read when sharing a rule, composing skills or adding a Base skill.

## Building

- [ADR 0004](adr/0004-build-threads-coordinate-and-subagents-code.md): build threads coordinate, Implementer subagents code, and when the user must review. Read when working on `implement`, `implement-spec`, `to-tickets` or `setup-project`.
- [ADR 0005](adr/0005-a-spec-is-one-long-lived-branch.md): the spec branch model, ticket worktrees and merges. Read when working on `implement-spec` or anything about branches.
- [ADR 0008](adr/0008-plugin-versions-change-only-at-a-release.md): plugin versions change only at a Release, what each part of X.Y.Z means, and how a Release is planned and cut. Read when working on versions, `CHANGELOG.md`, release labels or a Release thread.
- [implement-spec eval RESULTS.md](../evals/implement-spec/RESULTS.md): one entry per build-flow check of `implement-spec`. Read to see how `implement-spec` did in its build-flow check.
- [implement eval RESULTS.md](../evals/implement/RESULTS.md): one entry per build-flow check of `implement`. Read to see how `implement` did in its build-flow check.
- [release eval RESULTS.md](../evals/release/RESULTS.md): one entry per dry run of `release` (a proposal only, nothing merged or labelled). Read to see how `release` did in its dry run.
- [Codex install eval README](../evals/codex-install/README.md): the clean GitHub install, fresh-runtime skill discovery and interactive `grilling` check. Read when rerunning the Codex install check.
- [Codex install eval RESULTS.md](../evals/codex-install/RESULTS.md): one dated entry per Codex install check, including source commit, discovered skills, exact interview turns and portability issues. Read to see what Codex support last verified.

## Code review

- [REVIEW.md](../REVIEW.md): this repo's review rules: what Important means, what to skip, and the Always check lines. Read when reviewing a change or adding an Always check line.
- [ADR 0003](adr/0003-code-review-runs-find-verify-rank-in-rounds.md): Find, Verify, Rank, depths and Rounds. Read when working on `agentic-review`, `retro` or `pr`.
- [agentic-review eval README](../evals/agentic-review/README.md): the planted-bugs fixture pull request and how to rerun it, the Verify-only check included. Read after changing `agentic-review`. The fixture's own files under `base/` and `after/` are test data and get no lines here.
- [agentic-review eval SPEC.md](../evals/agentic-review/SPEC.md): the ticket the fixture pull request builds, given to the Review as its spec. Read when changing the fixture.
- [agentic-review eval EXPECTED.md](../evals/agentic-review/EXPECTED.md): the planted Findings, false alarms and known extras a run is scored against, and the Verify-only check's scoring. Read when scoring a run or changing the fixture; keep it away from the reviewing session.
- [agentic-review eval VERIFY-ONLY.md](../evals/agentic-review/VERIFY-ONLY.md): the candidate Findings, two false alarms and two real ones, handed to the Verifier in the Verify-only check. Read when running that check or changing the fixture; keep it away from the reviewing session (Verifiers get its contents, never the file).
- [agentic-review eval RESULTS.md](../evals/agentic-review/RESULTS.md): one entry per eval run. Read to see how `agentic-review` did last time.

## Retros

- [ADR 0007](adr/0007-retro-issues-pile-up-per-repo-and-are-planned-in-batches.md): how `retro` files Retro issues, routes them to the repo where the fix lands, and how `retro-planning` works through a repo's Retro backlog. Read when working on `retro`, `retro-planning`, or the end of `implement` and `implement-spec`.

## Out of scope

- [.out-of-scope/architecture-report-location.md](../.out-of-scope/architecture-report-location.md): why `improve-codebase-architecture` keeps its report in the OS temp directory. Read when triaging a request to move or share that report.

## Docs

- [ADR 0006](adr/0006-docs-are-found-through-one-index.md): this index, glossary pages per area, and which skills keep the index up to date. Read when a skill writes or reads docs.
