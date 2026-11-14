# Docs index

Read this first, then open only the docs whose line fits your work. Specs and tickets are GitHub issues, not files here. Bare issue and pull request numbers in text written before the 2026-11-05 move (ADRs 0001 to 0013, changelog entries before the move entry, and issues moved from the archive, which link their original) refer to the private archive `Luffytse/luffy-dev-skills`; from then on a bare number is this repo's, and an archive issue is written in full as `Luffytse/luffy-dev-skills#<n>`. Commits recorded for past Releases are the archive's IDs (ADR 0014).

## Whole repo

- [docs/dev-skills/glossary.md](glossary.md): the glossary's map, one page per Area of the words used here (Plugin, Model tier, Spec, Ticket, Release, Finder, Verifier and more). Read when writing or reviewing any skill text, to find the page.
- [ADR 0013](adr/0013-skill-changes-are-tested-by-ci-evals-and-review.md): the earlier three layers (CI, model evals, review), kept as history. Read when asking how skill changes were tested before ADR 0015.
- [ADR 0015](adr/0015-model-evals-are-retired-and-skill-changes-merge-on-ci-review-and-acceptance-lines.md): why model evals were retired and a skill change now merges on CI, review and shown acceptance lines. Read when changing how a skill change is tested or shown ready to merge.

## Agent setup

- [docs/dev-skills/issue-tracker.md](issue-tracker.md): this repo's issues live on GitHub, and the commands for each tracker operation the skills use. Read when a skill creates, reads, edits, labels, parks or closes an issue, or merges a pull request.
- [docs/dev-skills/triage-labels.md](triage-labels.md): the label string for each triage role, the `next-release` role, the Repo labels table with the rule that applies them, and the other labels. Read when applying or filtering triage labels.
- [docs/dev-skills/domain.md](domain.md): the single-context doc layout and how skills read the glossary and ADRs. Read when a skill looks for domain docs or flags an ADR conflict.
- [docs/dev-skills/release.md](release.md): the release doc: version sources, versioning policy, Release size, change sizes, cut steps, naming and the whole-Release check. Read when running the `release` skill, raising the version at a cut or giving an issue a release label.
- [docs/dev-skills/boundaries.md](boundaries.md): this repo's Boundary record: approvals, budget, skill file size limit, check-in interval and Milestone label form. Read when a skill or thread decides whether an action needs the user, or when giving an issue a Milestone label.
- [Agent setup glossary](glossary/agent-setup.md): Repo labels, `next-release`, Boundary record and Door. Read when a skill labels an issue or decides who merges.
- [docs/dev-skills/upstream-watch.md](upstream-watch.md): the prompt of the Upstream watch, run by hand every 2 weeks, and how its reminder issue works. Read when running or changing the watch.

## Packaging

- [README.md](../../README.md): Claude Code marketplace install, update and local-development steps. Read when changing install steps.
- [LICENSE](../../LICENSE): the MIT license for our own work. Read when asking what the repo's license covers.
- [dev-skills README](../../plugins/dev-skills/README.md): the plugin's install, update and development steps, folder layout, one line per skill and the last Upstream commit looked at. Read when installing the plugin or adding a skill of our own.
- [scripts/run-tests.sh](../../scripts/run-tests.sh): the test runner CI runs; it runs every `test*` file under `scripts/` and names each failure ([scripts/test-run-tests.sh](../../scripts/test-run-tests.sh) tests it). Read when pushing a change under `scripts/`.
- [scripts/test_review_briefs.py](../../scripts/test_review_briefs.py): scratch-repo tests of the plugin's `review_briefs.py`, which writes each Round's briefs. Read when changing `review_briefs.py` or the brief files it cuts from.
- [scripts/test_snapshot.py](../../scripts/test_snapshot.py): tests of the `team-lead` snapshot command `snapshot.py` on disposable repos. Read when changing `snapshot.py`.
- [scripts/test-check-plugin.py](../../scripts/test-check-plugin.py): the checker's own tests in disposable repositories, one planted bad case per named check, including `index-line-length`. Read when changing a check.
- [scripts/check-public-history.py](../../scripts/check-public-history.py): the pre-publish check that walks every commit for private traces (Spec #712); [scripts/test-check-public-history.py](../../scripts/test-check-public-history.py) tests it. Read when publishing a rewritten history.
- [scripts/rewrite-public-history.py](../../scripts/rewrite-public-history.py): the history rewrite the user runs on a fresh clone (Spec #712); [scripts/test-rewrite-public-history.py](../../scripts/test-rewrite-public-history.py) tests it. Read when running the move's history push.
- [scripts/check-plugin.sh](../../scripts/check-plugin.sh): this repo's own checker for the plugin layout and repo-wide rules, each check named in its header, among them `index-line-length` (no index bullet over 60 words). Read when adding or changing a check, or before pushing a plugin change.
- [ADR 0001](adr/0001-dev-skills-is-one-plugin-forked-from-matt-pocock.md): why `dev-skills` is one plugin that began as Matt Pocock's skills, and which skills it keeps. Read when adding or dropping a skill, or when the Upstream watch finds an idea.
- [ADR 0002](adr/0002-skills-name-model-tiers-not-models.md): skills name cheap, regular or premium tiers, never models; the `model-tiers` skill holds the default map. Read when a skill picks a model or the map changes.
- [Packaging glossary](glossary/packaging.md): Marketplace, Plugin, Skill, Upstream, Model tier, Shared rule and Base skill. Read when writing skill text or sharing a rule.
- [ADR 0009](adr/0009-shared-rules-have-one-owner-skill.md): shared rules have one owner skill, with workflow reuse and consumer inventory. Read when sharing a rule, composing skills or adding a Base skill.

## Building

- [Delivery glossary](glossary/delivery.md): Milestone, project threads, Startup verification, Harness, Worker control, Team lead, Takeover, Parked and Pause. Read when working on `milestone`, `team-lead` or `worker-control`.
- [Releases glossary](glossary/releases.md): Release, Release size, Main check, Ranked list, Cut steps, Triage batch and Release thread. Read when working on `release` or the Triage batch.
- [Build glossary](glossary/building.md): Spec, Ticket, build threads, branches, Build check, Implementer and Merging. Read when working on `implement`, `implement-spec` or `merging`.
- [ADR 0004](adr/0004-build-threads-coordinate-and-subagents-code.md): build threads coordinate and Implementer subagents code; a pull request goes to the user only at a boundary crossing; a build thread reads its issue against main first. Read when working on `implement`, `implement-spec`, `to-tickets` or `setup-project`.
- [ADR 0005](adr/0005-a-spec-is-one-long-lived-branch.md): the spec branch model, ticket worktrees and merges. Read when working on `implement-spec` or anything about branches.
- [ADR 0010](adr/0010-delivery-is-split-into-planning-a-team-lead-and-harness-references.md): delivery is split into `milestone` (plans and reports), `team-lead` (runs delivery) and `worker-control` (Harness references). Read when working on those skills or their callers.
- [ADR 0016](adr/0016-releases-bump-the-plugin-version-once.md): a pull request never changes the plugin version; the Release's changelog pull request raises it once, by the biggest change size. Read when working on versions, `CHANGELOG.md` or a Release cut.
- [ADR 0008](adr/0008-each-skill-change-bumps-the-plugin-version.md): superseded by ADR 0016 and kept as history: the earlier bump-per-pull-request rule; its Release naming still stands. Read when asking why the old rule was chosen or how a Release is named.

## Code review

- [Code review glossary](glossary/code-review.md): CI, Review, Round, Review level, Finder, Verifier, Finding and Severity. Read when working on the review skills or how skill changes are tested.
- [REVIEW.md](../../REVIEW.md): this repo's review rules: what Important means, what to skip, the Always check lines and the Review levels. Read when reviewing a change or adding an Always check line.
- [ADR 0003](adr/0003-code-review-runs-find-verify-rank-in-rounds.md): Round 0, Review levels, Find, Verify and Rank in at most 3 Rounds, and the review stopping for a person only at a boundary crossing. Read when working on `agentic-review`, `review-rounds`, `review-record`, `retro` or `pr`.

## Retros

- [Retros glossary](glossary/retros.md): Retro issue, Retro backlog, Retro planning, Necessity check and Spin-off. Read when working on `retro` or `retro-planning`.
- [ADR 0007](adr/0007-retro-issues-pile-up-per-repo-and-are-planned-in-batches.md): how `retro` files Retro issues by Scope and how `retro-planning` works through the backlog. Read when working on `retro`, `retro-planning`, or the end of `implement` and `implement-spec`.

## Out of scope

- [docs/dev-skills/out-of-scope/architecture-report-location.md](out-of-scope/architecture-report-location.md): why `improve-codebase-architecture` keeps its report in the OS temp directory. Read when triaging a request to move or share that report.

## Docs

- [Docs glossary](glossary/docs.md): Skill docs folder, Docs index and Area. Read when a skill writes or reads docs.
- [ADR 0006](adr/0006-docs-are-found-through-one-index.md): this index and the glossary pages per area, and which skills keep the index up to date; its layout part is replaced by ADR 0011. Read when a skill writes or reads docs.
- [ADR 0011](adr/0011-skill-files-live-in-docs-dev-skills.md): every file the skills require lives at a fixed path in `docs/dev-skills/`. Read when a skill names a path to a doc it writes or reads, or when setting up a repo.
- [ADR 0012](adr/0012-release-is-version-free-and-command-free.md): `release` is version-free and command-free; every plan is a Milestone, and the next Release is picked from one ranked list (amended by ADR 0016). Read when changing `release`, the Triage batch, the release doc seed or how the next Release is chosen.
- [ADR 0014](adr/0014-dev-skills-moved-to-its-own-public-repo-with-a-rewritten-history.md): why `dev-skills` moved to its own public repo with a rewritten history, and the archive numbering. Read when asking why issue numbers or past Release commits do not resolve here.
