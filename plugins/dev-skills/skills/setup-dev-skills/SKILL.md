---
name: setup-dev-skills
description: "Configure a GitHub repo for the dev-skills plugin: write its issue tracker, triage label, domain doc, release doc and Boundary record files, create the labels the skills use, and check the GitHub settings the build skills rely on. Use when the user sets up a repo for these skills, or the repo has no issue tracker or triage labels configured yet, or asks to update the repo's tracker, label, domain-doc, release-doc or Boundary-record files."
---

# Set up dev-skills

Derived from Matt Pocock's setup skill; the seed files in this folder are mostly his text (MIT, see `LICENSE-mattpocock-skills` in the plugin folder). Scaffold the per-repo configuration the other skills read:

- **Issue tracker**: GitHub Issues, in `docs/agents/issue-tracker.md`.
- **Labels**: the 5 state roles and 2 category roles that `triage` uses, the optional agent-only role (one label per coding agent) when the user wants it, and the `wayfinder:*` labels, in `docs/agents/triage-labels.md` and on the repo.
- **Domain docs**: where `GLOSSARY.md` and ADRs live and how skills read them, in `docs/agents/domain.md`, plus the `docs/index.md` that lists the docs.
- **Review rules**: a starter `REVIEW.md` at the repo root, where the repo's own review rules go.
- **Releases**: where the version lives, who bumps it (the bump mode), the changelog path, the release label prefix, and for pull-requests-bump repos the Release name form and the whole-Release check, that `release` reads, in `docs/agents/release.md`, for a repo that cuts versioned Releases.
- **Boundaries**: which irreversible actions agents may take, which need the user's approval, the resource budget, the check-in interval and the Milestone label form, in the Boundary record, `docs/agents/boundaries.md`.
- **GitHub settings**: checked and reported, never changed.

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write. It runs the same way on a fresh repo and on a re-run; a re-run shows a diff first (step 3).

## Process

### 1. Explore

Read whatever exists; assume nothing:

- `git remote -v`: which host and which `<owner>/<repo>`? Take it from either URL form, `https://github.com/<owner>/<repo>(.git)` or `git@github.com:<owner>/<repo>(.git)`, and drop a trailing `.git`. Only GitHub is supported. If the remote is not GitHub, tell the user the plugin does not support that tracker yet, and stop.
- Is the repo reachable? Run `gh api repos/<owner>/<repo>`. Use this REST call, not `gh repo view`: some cloud sessions have `gh` without GraphQL, and `gh repo view`, `gh issue view` and `gh label list` fail there with "GraphQL is not available", and so do the other `gh issue` subcommands (list, create, comment, edit, close): use the session's GitHub tools or the `gh api repos/<owner>/<repo>/issues...` REST routes. A session without `gh` uses the GitHub tools it has for the same reads and writes. If the repo cannot be reached, stop and tell the user what is missing.
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section?
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root, and the legacy `CONTEXT.md` / `CONTEXT-MAP.md`. If a legacy file exists, offer to `git mv` it to its `GLOSSARY` name and rewrite those names in `docs/agents/domain.md`.
- `docs/adr/` and any `src/*/docs/adr/` directories.
- `docs/agents/`: do earlier output files exist? If so this is a re-run.
- `docs/agents/release.md`, and the files a Release would touch: a version file (such as `package.json`, `pyproject.toml`, `Cargo.toml` or a plugin manifest) and a `CHANGELOG.md`.
- `docs/agents/boundaries.md`: does the Boundary record exist, and which values has it filled in?
- `REVIEW.md` at the repo root: does it exist, and which of its sections (Important, Skip, Always check) does it have? An existing one is left as it is (step 3).
- `docs/index.md`: the docs index, if one exists, and the other docs it should list (`REVIEW.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `.out-of-scope/`, README files).
- The repo's labels: `gh api repos/<owner>/<repo>/labels --paginate --jq '.[].name'`.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. Their absence means single-context, which is almost every repo.

Done when each item above is a fact or "none".

### 2. Present findings and ask

Summarise what is present and what is missing. Take the sections in order, one answer each, leading with the recommended answer so the user can accept it in a word. Skip a section when exploration settled it.

**Section A: Issue tracker.** GitHub, from the remote. Record it in `docs/agents/issue-tracker.md` with the repo's `<owner>/<repo>` filled in. The seed carries a "PRs as a request surface" flag, defaulted **off**. Leave it off and do not raise it; a user who wants external PRs in the triage queue can flip it later.

**Section B: Triage label vocabulary.** Ask one question:

> Do you want to keep the default labels? (recommended: **yes**)

The defaults are the 5 state roles, `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, and the 2 category roles, `bug` and `enhancement`, each label string equal to its role name. On **yes**, write them as they are. Only if the user says no, usually because the repo already uses other names (for example `bug:triage` for `needs-triage`), collect the overrides so `triage` applies the existing labels instead of creating duplicates.

Then ask one more question:

> Do you want labels that mark an issue for one coding agent only, so that the other agent leaves it alone? (recommended: **yes** when `docs/agents/triage-labels.md` already has agent rows or more than one coding agent works the repo, else **no**)

On **no**, the seed's agent-only section is left out of `docs/agents/triage-labels.md`. On **yes**, ask the user for each agent's label string (suggest `<agent>-only`), and fill the seed's agent-only table with one row per agent. Never guess agent names.

**Section C: Domain docs.** Default to **single-context** (one `GLOSSARY.md` and `docs/adr/` at the repo root); write it without asking. Offer **multi-context** (a root `GLOSSARY-MAP.md` pointing to per-context `GLOSSARY.md` files) only when exploration found monorepo signals.

**Section D: The repo's own rules for build threads.** Ask one question:

> Does this repo have rules of its own for the build threads, such as who merges which pull requests, or which files are special? (recommended: **no**, add them later)

On **yes**, ask the user for the rules' text, then record them in the repo's `CLAUDE.md` or `AGENTS.md` (the file step 4 picks) or, if they are about review, in `REVIEW.md`. Such rules never go into skill text: every project that loads the plugin reads the skills, so a rule that fits one repo belongs in that repo's own files.

**Section E: Releases.** Ask one question:

> Does this repo cut versioned Releases with the `release` skill? (recommended: **yes** when exploration found a version file, otherwise **no**)

On **yes**, fill the release doc's values, leading with what exploration found: the version file and the field or line that holds the version, the changelog path (an existing `CHANGELOG.md`, else one beside the version file), and the label prefix (default `release-`). Then ask three more things, which `release` reads:

- the **bump mode** (recommended: **Releases bump**): either a Release's bump pull request changes the version and ordinary pull requests leave it alone, or **pull requests bump**, where each pull request that changes the files the repo names bumps the version as its last commit at merge, with a number handed out then. On pull requests bump, ask which files make a pull request bump;
- on pull requests bump only, the **Release name** form: the name, label and release issue title forms with `<...>` placeholders, such as the name `Phase <n>`, the label `release-p<n>` and the title `Release Phase <n>` (a Release is named, not numbered);
- on pull requests bump only, the **whole-Release check**: the checks to run on the changelog pull request's branch (recommended: the repo's own checks), and any clean-up pass.

Then ask whether the bump pull request (Releases bump) or the bump commit (pull requests bump) must change or run anything else, such as a second file that repeats the version (recommended: **nothing**). On **no**, write no release doc.

**Section F: Boundaries.** Ask the user for the Boundary record's values, one question each, leading with the recommended answer:

> Which irreversible actions may agents take without asking you, for example deleting test data they generated? (recommended: **none**)

> Which actions must come to you for approval, for example deleting production or customer data? (recommended: **none** for a repo with no data of value, else ask the user to name them)

An empty answer to the second question is valid. The build skills read this record in place of a fixed list when they decide who merges inside a Milestone, so never add actions the user did not name.

> Is there a budget agents must stay within, such as a paid service, an API quota or a token limit? (recommended: **none**)

> How often should a running thread check in with you? (recommended: **1 hour**)

> What should a Milestone's membership label look like? (recommended: **`milestone-<n>`**, for example `milestone-1`)

Never guess a value. Say that a Milestone issue may add allowed or forbidden actions for its own issues and wins over the record for them; the seed already says so.

On a re-run, fill the fresh draft of the record from the existing record's values before diffing it, so a value filled in earlier is never shown as a revert to the seed's placeholder; ask again only for a value the existing record lacks, or that the user wants to change.

### 3. Draft and diff

Build every file from the seeds in this folder:

- [issue-tracker-github.md](./issue-tracker-github.md) becomes `docs/agents/issue-tracker.md`
- [triage-labels.md](./triage-labels.md) becomes `docs/agents/triage-labels.md`
- [domain.md](./domain.md) becomes `docs/agents/domain.md`
- [release.md](./release.md) becomes `docs/agents/release.md`, only when Section E was **yes**
- [boundaries.md](./boundaries.md) becomes `docs/agents/boundaries.md`
- [review.md](./review.md) becomes `REVIEW.md` at the repo root, but only when the repo has none, first run or re-run. An existing `REVIEW.md` (one `retro` made, or the user's own) is never drafted over: nothing in it is removed or rewritten, and only a missing section of Important, Skip and Always check is offered, alone, as a diff; with all three present, report "no change".
- the `## Agent skills` block (step 4)
- `docs/index.md`, new or updated, listing every `docs/agents/` file, `REVIEW.md` (with a "read when reviewing a change or adding an Always check line" line) and every other doc found while exploring, by loading `docs-index` and applying its contract

On a re-run, diff each draft against the file in the repo. Keep the values the earlier run filled in (the repo link, the label strings, the PR flag, the release doc's values, including its bump mode, Release name form and whole-Release check, and the Boundary record's values) and change only what drifted from the seeds. Show the user the diff, or "no change" per file. The rules the user gave in Section D are drafted into the diff of the file they go in (`CLAUDE.md` or `AGENTS.md`, or `REVIEW.md`) and shown before writing; adding a line to an existing `REVIEW.md` is an addition, not a rewrite. Let the user edit before anything is written.

Done when the user has approved the drafts, or approved "no change".

### 4. Write

**Pick the file to edit.** If `CLAUDE.md` exists, edit it. Else if `AGENTS.md` exists, edit it. If neither exists, ask the user which to create. Never create one when the other exists.

If an `## Agent skills` block already exists in the chosen file, update it in place and leave the user's edits to the surrounding sections alone. The block:

```markdown
## Agent skills

Start at `docs/index.md`; it says which doc to read for what.

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary, for example "5 state roles + 2 category roles: ...", plus the agent-only labels when the repo has them]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### Releases

[one-line summary: the version file, the bump mode (Releases bump or pull requests bump) and the release label prefix]. See `docs/agents/release.md`.
```

Leave out the `### Releases` part when the repo has no release doc.

Add a `### Boundaries` part to the block, after `### Domain docs` and before `### Releases`:

```markdown
### Boundaries

[one-line summary: what needs the user's approval ("nothing" if empty), the budget and the check-in interval]. See `docs/agents/boundaries.md`.
```

Then write the approved files, and `docs/index.md` last.

**Create the labels.** Create every label the skills use that the repo lacks, whether or not `triage` is installed: the label string of each of the 5 state roles, `bug` and `enhancement`, each agent-only label from the table (only when Section B was **yes**), and `wayfinder:map`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling` and `wayfinder:task`. Use `gh api --method POST repos/<owner>/<repo>/labels -f name=<label>` (or the session's GitHub tools); `gh label create` needs GraphQL. Leave `retro`, `retro-planning` and the release labels alone: `retro`, `retro-planning` and `release` create them when first needed.

### 5. Check GitHub settings and report

Check, and report each failure to the user. Never change a setting, and never create a ruleset or branch rule. Use `gh api` or the session's GitHub tools.

| Check | How | A failure means |
| --- | --- | --- |
| Sub-issues and dependencies | `gh api repos/<owner>/<repo>/issues/<n>` on any issue returns `issue_dependencies_summary` and `sub_issues_summary`; report "not checked" when the repo has no issue to probe. Note `gh --version` too: 2.94+ has the `--parent` and `--blocked-by` flags, and older `gh` uses the REST routes in the seed | `to-tickets` and `wayfinder` fall back to `Part of #<n>` and `Blocked by:` lines |
| Draft PRs | `gh api repos/<owner>/<repo> --jq .private`: `false` passes (public repos allow drafts). A private repo needs a paid plan: the "Upgrade to GitHub Pro" message from the branch protection call below means a free plan, so fail; if the plan cannot be told, report "not checked" | `implement-spec` cannot open the Spec pull request as a draft |
| Merge methods | `gh api repos/<owner>/<repo> --jq '{allow_squash_merge, allow_merge_commit}'` shows both `true` | `implement` squash-merges and `implement-spec` merges with a merge commit, so one of them cannot merge |
| Default branch | `gh api repos/<owner>/<repo> --jq .default_branch` is `main` | the build skills assume `main` |
| Branch protection | `gh api repos/<owner>/<repo>/branches/<default>/protection` and `gh api repos/<owner>/<repo>/rules/branches/<default>`: no required reviews or restriction that stops the agent merging its own pull request | the agent cannot merge; the user must merge |

A 404 from the protection call means no classic protection, which passes. A 403 with the "Upgrade to GitHub Pro" message means a free private repo, where branch rules cannot be enforced, which also passes. Any other 403 means the session cannot read it: say "not checked", not "passed".

Done when each row is "ok", a failure with its effect, or "not checked" with the reason.

### 6. Done

Tell the user the setup is complete, which files changed, which labels were created, and the settings report. Mention they can edit `docs/agents/*.md` directly; re-run this skill to bring the files up to date after the plugin changes them, or to switch to other label names. Then, if the project's instructions do not yet cover this repo, offer `setup-project`, which drafts them for the coordinator.
