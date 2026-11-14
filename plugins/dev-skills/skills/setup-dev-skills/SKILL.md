---
name: setup-dev-skills
description: "Configure a GitHub repo for the dev-skills plugin: tracker, label, domain, release and Boundary files, labels, settings. Use when the user sets up a repo for these skills, it has no tracker or triage labels configured, or those files need updating."
---

# Set up dev-skills

Derived from Matt Pocock's setup skill; the seed files in this folder are mostly his text (MIT, see `LICENSE-mattpocock-skills` in the plugin folder). Scaffold the per-repo configuration the other skills read. Every file it writes lives in `docs/dev-skills/`, the one folder only the skills use, so it never mixes with the repo's own docs; only `REVIEW.md` and the `## Agent skills` block in `CLAUDE.md` or `AGENTS.md` go at the repo root, where reviewers and coding agents expect them:

- **Issue tracker**: GitHub Issues, in `docs/dev-skills/issue-tracker.md`.
- **Labels**: the 5 state roles and 2 category roles that `triage` uses, the `next-release` role, the repo's own labels, if it has any, each with a line saying when it applies (the **Repo labels** table, which `triage`, `to-spec`, `to-tickets` and `review-rounds` apply), the `wayfinder:*` labels and the `parked` label (the tracker doc's **Park** operation uses it), in `docs/dev-skills/triage-labels.md` and on the repo.
- **Domain docs**: where the glossary (`docs/dev-skills/glossary.md`) and ADRs (`docs/dev-skills/adr/`) live and how skills read them, in `docs/dev-skills/domain.md`, plus the `docs/dev-skills/index.md` that lists the docs.
- **Review rules**: a starter `REVIEW.md` at the repo root, where the repo's own review rules go.
- **Releases**: the versioning policy (none, pull requests bump or Releases bump, with that policy's text), the Release name form, the Release size, the changelog path, the release label prefix, the cut steps and the whole-Release check, that `release` reads, in `docs/dev-skills/release.md`, for a repo that cuts Releases, versioned or not.
- **Boundaries**: which irreversible actions agents may take, which need the user's approval, the resource budget, the check-in interval and the Milestone label form, in the Boundary record, `docs/dev-skills/boundaries.md`.
- **GitHub settings**: checked and reported, never changed.

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write. It runs the same way on a fresh repo and on a re-run; a re-run shows a diff first (step 3).

## Process

### 1. Explore

Read whatever exists; assume nothing:

- `git remote -v`: which host and which `<owner>/<repo>`? Take it from either URL form, `https://github.com/<owner>/<repo>(.git)` or `git@github.com:<owner>/<repo>(.git)`, and drop a trailing `.git`. Only GitHub is supported. If the remote is not GitHub, tell the user the plugin does not support that tracker yet, and stop.
- Is the repo reachable? Use the **Check the repo is reachable** operation of the tracker doc, or of the seed `issue-tracker-github.md` where the repo has no tracker doc yet (a session without `gh` uses the GitHub tools it has for the same read). If the repo cannot be reached, stop and tell the user what is missing.
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section?
- `docs/dev-skills/glossary.md` (the glossary, or its map once split), and the legacy `CONTEXT.md` / `CONTEXT-MAP.md` at the repo root. If a legacy file exists, offer to `git mv` it to `docs/dev-skills/glossary.md` (a `CONTEXT-MAP.md` becomes the map).
- `docs/dev-skills/adr/` and any `src/*/docs/adr/` directories.
- `docs/dev-skills/`: do earlier output files exist? If so this is a re-run.
- `docs/dev-skills/release.md`, and the files a Release would touch: a version file (such as `package.json`, `pyproject.toml`, `Cargo.toml` or a plugin manifest) and a `CHANGELOG.md`.
- `docs/dev-skills/boundaries.md`: does the Boundary record exist, and which values has it filled in?
- `REVIEW.md` at the repo root: does it exist, and which of its sections (Important, Skip, Always check) does it have? An existing one is left as it is (step 3).
- `docs/dev-skills/index.md`: the docs index, if one exists, and the other docs it should list (`REVIEW.md`, `CONTRIBUTING.md` at the root, in `docs/` or in `.github/`, `docs/dev-skills/out-of-scope/`, README files).
- The repo's labels (the **List labels** operation of the tracker doc, or of the seed `issue-tracker-github.md` where the repo has no tracker doc yet).
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. Their absence means single-context, which is almost every repo.

Done when each item above is a fact or "none".

### 2. Present findings and ask

Summarise what is present and what is missing. Take the sections in order, one answer each, leading with the recommended answer so the user can accept it in a word. Skip a section when exploration settled it.

**Section A: Issue tracker.** GitHub, from the remote. Record it in `docs/dev-skills/issue-tracker.md` with the repo's `<owner>/<repo>` filled in. The seed carries a "PRs as a request surface" flag, defaulted **off**. Leave it off and do not raise it; a user who wants external PRs in the triage queue can flip it later.

**Section B: Triage label vocabulary.** Ask one question:

> Do you want to keep the default labels? (recommended: **yes**)

The defaults are the 5 state roles, `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, and the 2 category roles, `bug` and `enhancement`, plus the `next-release` role, each label string equal to its role name. On **yes**, write them as they are. Only if the user says no, usually because the repo already uses other names (for example `bug:triage` for `needs-triage`), collect the overrides so `triage` applies the existing labels instead of creating duplicates.

Then ask one more question:

> Does this repo have labels of its own, such as one per area of the code or kind of work? (recommended: **no**, **yes** when `docs/dev-skills/triage-labels.md` already has Repo labels rows)

On **no**, add no row: the seed's **Repo labels** table stays empty (a row an earlier run recorded stays until the user drops it), and the run goes on as if the question did not exist. On **yes**:

1. Take the tracker's labels from exploration (step 1). Offer as candidates those that no role, no `wayfinder:` label, not `parked`, `retro` or `retro-planning`, no release label (the release doc's label prefix, else `release-`), no Milestone membership label (the form in the Boundary record, else `milestone-<n>`) and no existing Repo labels row covers. Say which labels you left out and why. The user picks the ones to record.
2. For each picked label, draft its one-line "when it applies" from its name and the issues that carry it (the tracker doc's **List issues** with that label filter), and show it for the user to confirm or correct. Never record a line the user has not confirmed.
3. Ask whether to add labels the tracker does not have yet; for each, take its string and its line from the user. Step 4 creates them.

Record each label as a row of the table: the label string and its line. On a re-run, show the existing table first and offer to add (as above), edit a row's line, or drop a row; keep every row the user leaves alone, with its line. Dropping a row removes it from `docs/dev-skills/triage-labels.md` only: never delete the label from the tracker, and say so when the user drops one.

**Section C: Domain docs.** Default to **single-context** (one `docs/dev-skills/glossary.md` and one `docs/dev-skills/adr/`); write it without asking. Offer **multi-context** (`docs/dev-skills/glossary.md` as a map pointing to a glossary beside each context's code) only when exploration found monorepo signals.

**Section D: The repo's own rules for build threads.** Ask one question:

> Does this repo have rules of its own for the build threads, such as who merges which pull requests, or which files are special? (recommended: **no**, add them later)

On **yes**, ask the user for the rules' text, then record them in the repo's `CLAUDE.md` or `AGENTS.md` (the file step 4 picks) or, if they are about review, in `REVIEW.md`. Such rules never go into skill text: every project that loads the plugin reads the skills, so a rule that fits one repo belongs in that repo's own files.

**Section E: Releases.** Ask one question:

> Does this repo cut Releases with the `release` skill, with or without a version? (recommended: **yes**)

On **no**, write no release doc. On **yes**, ask these in order, one answer each, leading with the recommended answer and with what exploration found:

- the **versioning policy** (recommended: **pull requests bump** when exploration found a version file and the repo's pull requests already change it, **Releases bump** for any other repo with a version file, **none** for a repo with no version): **none**, where the repo keeps no version; **pull requests bump**, where each pull request that changes the files the repo names bumps the version as its last commit at merge; or **Releases bump**, where a Release's bump pull request changes the version and ordinary pull requests leave it alone. On pull requests bump or Releases bump, fill the version file and the field or line that holds the version from what exploration found; on pull requests bump, also ask which files make a pull request bump and how the number is given (the repo decides; the seed leaves it as a placeholder to fill in);
- the **Release name** form: the name, label and release issue title forms with `<...>` placeholders (recommended: the name `Release <n>`, the label `release-<n>` and the title `Release <n>`);
- the **Release size**, the most items one Release takes, counted of any kind (recommended: **5**);
- the **changelog path** (an existing `CHANGELOG.md`, else one at the repo root) and the **label prefix** (default `release-`);
- the **cut steps**: anything else the cut must change or run, after the changelog entry is written (recommended: **none**); on Releases bump, ask whether the bump pull request must change or run anything else, such as a second file that repeats the version, and on pull requests bump, whether the bump commit must (recommended: **nothing**);
- the **whole-Release check**: the checks to run on the changelog pull request's branch, and any clean-up pass (recommended: the repo's own checks).

Write the seed's matching "Policy:" section and delete the other two. A repo with no version still gets a release doc, with policy none and no version fields. The Releases bump section carries the semver sizes and the bump pull request's steps, and the pull requests bump section the bump each merge takes, so write them from the seed.

On a re-run over a release doc that has a "Bump mode" line and no versioning policy, take that mode as the policy (and its Version file, Release name and whole-Release check as the answers), and ask for every field the doc lacks: usually the Release size and the cut steps, and the Release name form too when the doc has none.

**Section F: Boundaries.** Ask the user for the Boundary record's values, one question each, leading with the recommended answer:

> Which irreversible actions may agents take without asking you, for example deleting test data they generated? (recommended: **none**)

> Which actions must come to you for approval, for example deleting production or customer data? (recommended: **none** for a repo with no data of value, else ask the user to name them)

An empty answer to the second question is valid. `merging` reads this record in place of a fixed list when it decides who merges, for every pull request, so never add actions the user did not name.

> Is there a budget agents must stay within, such as a paid service, an API quota or a token limit? (recommended: **none**)

> During a Milestone's delivery, how often should a scheduled check-in wake the coordinator to check on its threads? (recommended: **1 hour**)

> What should a Milestone's membership label look like? (recommended: **`milestone-<n>`**, for example `milestone-1`)

Never guess a value. Say that this record is the only one: a Milestone issue holds no boundaries of its own, so an action to allow or reserve for a Milestone goes here; the seed already says so.

On a re-run, fill the fresh draft of the record from the existing record's values before diffing it, so a value filled in earlier is never shown as a revert to the seed's placeholder; ask again only for a value the existing record lacks, or that the user wants to change.

### 3. Draft and diff

Build every file from the seeds in this folder:

- [issue-tracker-github.md](./issue-tracker-github.md) becomes `docs/dev-skills/issue-tracker.md`
- [triage-labels.md](./triage-labels.md) becomes `docs/dev-skills/triage-labels.md`
- [domain.md](./domain.md) becomes `docs/dev-skills/domain.md`
- [release.md](./release.md) becomes `docs/dev-skills/release.md`, only when Section E was **yes**
- [boundaries.md](./boundaries.md) becomes `docs/dev-skills/boundaries.md`
- [review.md](./review.md) becomes `REVIEW.md` at the repo root, but only when the repo has none, first run or re-run. An existing `REVIEW.md` (one `retro` made, or the user's own) is never drafted over: nothing in it is removed or rewritten, and only a missing section of Important, Skip and Always check is offered, alone, as a diff; with all three present, report "no change".
- the `## Agent skills` block (step 4)
- `docs/dev-skills/index.md`, new or updated, listing every `docs/dev-skills/` file, `REVIEW.md` (with a "read when reviewing a change or adding an Always check line" line) and every other doc found while exploring, by loading `docs-index` and applying its contract

On a re-run, diff each draft against the file in the repo. Keep the values the earlier run filled in (the repo link, the label strings, the Repo labels rows and their lines, the PR flag, the release doc's values, including its versioning policy, Release name form, Release size, cut steps and whole-Release check, and the Boundary record's values) and change only what drifted from the seeds. Show the user the diff, or "no change" per file. The rules the user gave in Section D are drafted into the diff of the file they go in (`CLAUDE.md` or `AGENTS.md`, or `REVIEW.md`) and shown before writing; adding a line to an existing `REVIEW.md` is an addition, not a rewrite. Let the user edit before anything is written.

Done when the user has approved the drafts, or approved "no change".

### 4. Write

**Pick the file to edit.** If `CLAUDE.md` exists, edit it. Else if `AGENTS.md` exists, edit it. If neither exists, ask the user which to create. Never create one when the other exists.

If an `## Agent skills` block already exists in the chosen file, update it in place and leave the user's edits to the surrounding sections alone. The block:

```markdown
## Agent skills

Start at `docs/dev-skills/index.md`; it says which doc to read for what.

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/dev-skills/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary, for example "5 state roles + 2 category roles: ...", plus the `next-release` role and the Repo labels table when the repo has them]. See `docs/dev-skills/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/dev-skills/domain.md`.

### Releases

[one-line summary: the versioning policy (none, pull requests bump or Releases bump), the Release size and the release label prefix]. See `docs/dev-skills/release.md`.
```

Leave out the `### Releases` part when the repo has no release doc.

Add a `### Boundaries` part to the block, after `### Domain docs` and before `### Releases`:

```markdown
### Boundaries

[one-line summary: what needs the user's approval ("nothing" if empty), the budget and the check-in interval]. See `docs/dev-skills/boundaries.md`.
```

Then write the approved files, and `docs/dev-skills/index.md` last.

**Create the labels.** Create every label the skills use that the repo lacks, whether or not `triage` is installed: the label string of each of the 5 state roles, `bug` and `enhancement`, `next-release`, each Repo labels row's label the repo lacks (a label the user added, or one a re-run's row names but the tracker lost), and `wayfinder:map`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, `wayfinder:task` and `parked`. Use the tracker doc's **Create a label** operation for each. Never delete a label. Leave `retro`, `retro-planning` and the release labels alone: `retro`, `retro-planning` and `release` create them when first needed.

### 5. Check GitHub settings and report

Check, and report each failure to the user. Never change a setting, and never create a ruleset or branch rule. Read the settings with the tracker doc's **Read repo settings** operation.

| Check | How | A failure means |
| --- | --- | --- |
| Sub-issues and dependencies | (**Read repo settings**) Any issue's sub-issue and dependency summaries are present; report "not checked" when the repo has no issue to probe. Note whether the installed command-line tool has the native parent and blocked-by options, or only the routes in the seed | `to-tickets` and `wayfinder` fall back to `Part of #<n>` and `Blocked by:` lines |
| Draft PRs | The repo is public, which allows drafts. A private repo needs a paid plan: the "Upgrade to GitHub Pro" message from the branch protection read means a free plan, so fail; if the plan cannot be told, report "not checked" | `implement-spec` cannot open the Spec pull request as a draft |
| Merge methods | Both squash merging and merge commits are allowed | `implement` squash-merges and `implement-spec` merges with a merge commit, so one of them cannot merge |
| Default branch | The default branch is `main` | the build skills assume `main` |
| Branch protection | Neither classic protection nor branch rules require reviews or restrict who can merge in a way that stops the agent merging its own pull request | the agent cannot merge; the user must merge |

A repo with no classic protection passes. A free private repo, where the host says branch rules need a paid plan and cannot be enforced, also passes. Any other refusal means the session cannot read the settings: say "not checked", not "passed".

Done when each row is "ok", a failure with its effect, or "not checked" with the reason.

### 6. Done

Tell the user the setup is complete, which files changed, which labels were created, and the settings report. Mention they can edit `docs/dev-skills/*.md` directly; re-run this skill to bring the files up to date after the plugin changes them, or to switch to other label names. Then, if the project's instructions do not yet cover this repo, offer `setup-project`, which drafts them for the coordinator.
