# Results

One entry per dry run of `release`, newest first. A dry run follows `SKILL.md` step by step against a real repo but only proposes: it merges, labels, renames, opens and closes nothing. Rerun when `release` changes, and record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`. An entry written inside an open pull request names the commit and plugin version it ran on as its base; anything that happens after the entry's last commit (later Rounds, merges, the merge itself) is recorded on the pull request, not in the file.

## Template

```
### <date>, commit <sha>, dev-skills <version>

Setup: <repo, origin, tracker, release doc, current Release>
Steps: <what each step of SKILL.md did or would do, step by step>
Not exercised: <paths of the skill this run did not reach>
Pass: yes | no. Lessons: <what to change in release, if anything>
```

## Runs

### 2026-11-01, commit 2c9e333 (base), dev-skills 0.25.0 (base): "pull requests bump", Milestone 1 · Release 1

Setup: this repo, with a GitHub origin and the GitHub Issues tracker, run by the Implementer of #397 on its branch, with `release` and `docs/agents/release.md` as this branch writes them (bump mode "pull requests bump", Release name `Milestone <m> · Release <n>`, label `release-m<m>-r<n>`, title `Release Milestone <m> · Release <n>`, and a whole-Release check). The current Release is #414, `Release Milestone 1 · Release 1`. Proposal only: nothing was merged, labelled, renamed, opened or closed. Checks the expectations A to F of the failing run below.

- **Before you start:** the release doc gives the version file, the changelog, the prefix `release-`, the bump mode "pull requests bump", the three forms and the whole-Release check. Title pattern `^Release Milestone .+ · Release .+$`, label pattern `^release-m.+-r.+$`. Pick the path: no urgent request; `release-m1-r1` matches the label pattern, so not a first Release; steps 1 to 5.
- **Step 1:** the title query lists #414 only, `urgent` false, so #414 is the current Release and its `**Label:**` line gives `release-m1-r1` (**A**). The changelog on main has no `## Milestone 1 · Release 1` heading, so no shortcut. The label lists #391 (closed `completed`; shipped: #415 closes it and is merged into `main`), and #397, #398, #399 and #344, still **open** on 2026-11-01. In a real run the cut stops here. The run went on as if all four had closed as completed, shipped, none carried over.
- **Step 2:** the top changelog entry, `## 0.25.0 (2026-11-01)`, has no `Commits:` line, so it ends at the commit that added its heading: `git log -1 -S '## 0.25.0 (2026-11-01)' origin/main -- plugins/dev-skills/CHANGELOG.md` gives bdc7696 (PR #402), found from the changelog, not the version file (**B**). Range `bdc7696..2c9e333` today: 2c9e333, PR #415, closing #391. No commit in it touches the version file, so no version is kept and versions delivered: none, the version stays 0.25.0; at the real cut the same command lists the bump each of #397, #398, #399 and #344 adds as its last commit. No size, no rename (**C**).
- **Step 3 (proposed, not opened):** open-bump check: no open pull request title matches `release\S*\s+Milestone 1 · Release 1($|[^0-9])`. A branch from main, version files untouched, and this entry at the top of `CHANGELOG.md` (**D**):

  ```md
  ## Milestone 1 · Release 1 (<date of the cut>)

  Per-PR versions are in place and agents merge inside the Milestone's boundaries, so most later pieces of Milestone 1 need nothing from the user.

  Versions: none, the version stays 0.25.0. Commits: bdc7696..2c9e333.

  - Per-PR skill versions and sprint Releases in ADR 0008 and CLAUDE.md (Milestone 1, piece 0 + A1) (#391)
  - (at the real cut also #397, #398, #399 and #344, and their versions in the Versions line)
  ```

  No "Also merged" line (every commit in the range has a shipped issue). Whole-Release check: `bash scripts/check-plugin.sh` (OK), `python3 scripts/test-check-plugin.py` (5 tests OK), `claude plugin validate .` (passed); clean-up pass: the "until #397" sentences in `CLAUDE.md`, the release doc, ADR 0008, the glossary and `triage-labels.md` are this branch's to remove, so none is left at the cut. Pull request `docs(release): Milestone 1 · Release 1` by `pr`, naming #414, the range and versions, no dropped issues, Door two-way; the thread merges it itself once its checks pass, after re-fetching main and extending the end commit if main moved (**E**).
- **Step 4 (proposed):** after the merge, #414's title gives the name; the entry headed `## Milestone 1 · Release 1`, through the line before the next `## ` heading, is posted on #414 as its notes, carrying the Versions and Commits line, and #414 is closed (**E**).
- **Step 5 (proposed, nothing labelled):** the next name fills `Milestone <m> · Release <n>` from `m` = 1, `n` = 1 raised to 2: `Milestone 1 · Release 2`, label `release-m1-r2` (does not exist yet), release issue `Release Milestone 1 · Release 2`. Goal and scope not proposed in this run; step 5's scope rules are unchanged and belong to piece B7.
- **Urgent fix (on paper):** the user asks to ship a fix now. Pick the path's first bullet: there is no urgent Release when pull requests bump, so no `Release 0.25.1` issue and no bump pull request; the user is told the fix ships in its own pull request, which takes the next patch number at merge, and the next Release's entry lists it. No open release issue has the `**Urgent fix:**` line, so nothing to close (**F**).

Not exercised: the real cut (the four open issues), a carry-over, a dropped issue, a breaking change's "What to do" lines, a top entry with a `Commits:` line (the next Release's first run reads this one's), main moving before the merge, a failing whole-Release check, the missing-forms stop, and a repo whose rules say the user merges docs pull requests.

Pass: yes, as a proposal. Lessons: the first named Release's range starts from the last numbered Release's changelog heading, so the switch from "Releases bump" needs no hand-written marker; from now on each entry's `Commits:` line is that marker.

### 2026-11-01, commit c99f667 (base), dev-skills 0.24.1 (base): "Releases bump", the 0.25.0 cut replayed

Setup: this repo at c99f667 (main just before PR #402, the 0.25.0 bump), with the release doc as it was at that commit (`git show c99f667:docs/agents/release.md`: no bump-mode line, so "Releases bump") and `release` as this branch writes it. The current Release is 0.25.0: release issue #371 (open at that commit), label `release-0.25.0`. Proposal only. Compared with what the skill on main did for the same cut (PR #402) and with the 0.23.0 run below (G).

- **Before you start:** the release doc gives the version file, changelog, prefix `release-` and two extra steps (both manifests; the two checks); no bump mode, so "Releases bump", and a Release's name is its version. Path: steps 1 to 5. Same as before.
- **Step 1:** the title query, `^Release [0-9]+\.[0-9]+\.[0-9]+$` as before, lists #371; the label `release-0.25.0` (prefix plus version, as before). The version file at c99f667 reads 0.24.1 and the changelog has no `## 0.25.0` heading, so no shortcut. All 16 labelled issues closed as completed, each shipped by #373, #374, #375 or #378 (as PR #402 records). Same as before.
- **Step 2:** "Releases bump", so the last Release is found as before, by the commit that set the version: `git log -1 -S '0.24.1' c99f667 -- <version file>` gives aed6b9a; the 24 commits `aed6b9a..c99f667` take PR #402's sizes: minor (#378, #349 + #358, #341), patch (#374, #375), ride along (#373, #359, #372, #388). Biggest minor: 0.24.1 to **0.25.0**, the label's version, so no rename. Same as before.
- **Step 3:** a bump pull request `chore(release): 0.25.0` changing the version in both manifests (the extra step), with the entry `## 0.25.0 (<date>)`, goal, 16 list lines and the "Also merged" line, no Versions or Commits line, Door one-way, the user merges. Identical to PR #402's diff and body shape.
- **Step 4:** on the user's merge, the `## 0.25.0` entry (now ending at the next `## ` heading, the same line as "the next version heading" before) is posted on #371 and #371 closed. Same as before.
- **Step 5:** next version from 0.25.0, label prefix plus version, release issue `Release X.Y.Z` (the template's `<name>` is the version in this mode). Same as before.
- **Urgent fix:** the two urgent bullets and "Urgent fix" apply, marked "Releases bump"; text unchanged.

Compared with the 0.23.0 run below: the same steps in the same order (find `Release X.Y.Z`, shipped test, size from the commit that set the version, bump pull request for the user, notes on merge, next version). The only text changes on this path are the "Releases bump" markers, the heading test moved to the top (same test), and the template's title and label written as `<name>` and `<label>` (the same strings in this mode).

Not exercised: as in the 0.23.0 run, plus a rerun with the bump pull request already open.

Pass: yes. Lessons: none.

### 2026-11-01, commit 2c9e333 (base), dev-skills 0.25.0 (base): "pull requests bump" with the skill as on main (expected to fail)

Setup: this repo, with a GitHub origin and the GitHub Issues tracker, run by the Implementer of #397 before changing `release`, with `plugins/dev-skills/skills/release/SKILL.md` as on main and the release doc `docs/agents/release.md` as on main ("pull requests bump"). The current Release is the hand-written named Release #414, `Release Milestone 1 · Release 1`, label `release-m1-r1`. Proposal only: nothing was merged, labelled, renamed, opened or closed.

What this run and the run after the change must show (the test #397's acceptance criteria set):

- A. Release issue #414 is found by its named title, and `release-m1-r1` is its label, both read from the release doc.
- B. The last Release is found without the commit that set the version: 0.25.0, whose entry PR #402 added in bdc7696.
- C. No bump size is picked, no label is renamed to a version and no bump pull request is opened.
- D. One changelog entry, headed with the Release's name, covers `bdc7696..<main at the cut>`, and records the start and end commits and the versions delivered.
- E. The changelog pull request changes no version, and the thread merges it itself; the release issue is closed with the entry as its notes.
- F. The urgent-fix path says plainly what it does when pull requests bump.
- G. A "Releases bump" release doc (no bump-mode line) gives the same steps as before (the "Releases bump" run above, on the 0.25.0 cut).

- **Before you start:** the skill reads the version file, changelog and prefix `release-`; it has no idea of a bump mode, so the doc's "pull requests bump" line changes nothing. Labels starting with `release-` exist, so steps 1 to 5.
- **Step 1:** the query keeps titles matching `^Release [0-9]+\.[0-9]+\.[0-9]+$`; #414 (`Release Milestone 1 · Release 1`) does not match, so no release issue is open (**fails A**). The fallback takes "the release label of the highest version that an open issue carries": `release-m1-r1` carries no version, so "highest" has no answer; at best the skill would open a second release issue titled `Release X.Y.Z` beside #414 (**fails A**).
- **Step 2:** `git log -1 -S '0.25.0' origin/main -- <version file>` gives bdc7696, right this once only because no pull request has bumped since; once #397 merges with its own bump, the same command finds that bump's commit and the range drops every merge before it (**fails B**). It then picks a size (minor, from #415 riding along and #397's new mode) and proposes renaming `release-m1-r1` to `release-0.26.0` and retitling #414 `Release 0.26.0` (**fails C**).
- **Step 3:** it opens a bump pull request changing the version, which the release doc forbids, with an entry headed `## 0.26.0` and no start or end commit or versions delivered (**fails C, D**). The user is asked to merge it (**fails E**).
- **Step 4:** reads a version from #414's title, which has none.
- **Urgent fix:** opens a `Release 0.25.1` urgent release issue and a patch bump pull request, though in this repo a fix already ships with its own patch bump in its own pull request (ADR 0008) (**fails F**).

Not exercised: step 5.

Pass: no. Lessons: `release` needs a bump mode and a Release name read from the release doc, a way to find the last Release from the changelog rather than from the version file, and an urgent path that says what happens when pull requests bump. Built in #397; the runs above this one record the result.

### 2026-10-31, commit 7debc88 (base), dev-skills 0.22.27 (base)

Setup: this repo, with a GitHub origin and the GitHub Issues tracker, run by the Implementer of Ticket #259 on the Ticket branch, with the release doc `docs/agents/release.md` and the `release` skill as this branch writes them. The commit and version are the Spec branch's at the point the Ticket branch was made. The current Release is 0.23.0: release issue #263, label `release-0.23.0`, scope Spec #257 and its Tickets #258 to #262. Proposal only: nothing was merged, labelled, renamed, opened or closed.

- **Before you start:** the release doc gave the version file (`plugins/dev-skills/.claude-plugin/plugin.json`, `"version"`), the changelog (`plugins/dev-skills/CHANGELOG.md`), the prefix `release-` and two extra steps (a "version X to Y" line in `PATCHES.md` while it exists; run `scripts/check-plugin.sh` and `claude plugin validate .`). The repo has release labels and no urgent fix was named, so the path was steps 1 to 5.
- **Step 1:** the open issue titled `Release 0.23.0` is #263, so the current release label is `release-0.23.0` and the goal is #263's: "plugin versions change only at a Release, and no pull request takes a number another one could take". #263 carries no release label, and the label lists #257 to #262, all six **open** on 2026-10-31. In a real run the cut stops here (the user waits or carries issues over). The dry run went on as if all six had closed as completed and none was carried over.
- **Step 2:** `git log -1 --format=%H -S '0.22.27' origin/main -- plugins/dev-skills/.claude-plugin/plugin.json` gives 99f92ec, the commit that set the current version. After it: on main, #256 (ADR 0008, squash-merged as 29320bc); on the Spec branch, #256's own commits again, its retro's two `REVIEW.md` Always check lines (3ab3b91) and #258 (7debc88); and Tickets #259 to #262 once they land. Sizes: #258 (implement and implement-spec lose their numbering step) **minor**, arguably breaking for a project whose own rules take numbers at merge time, but below 1.0.0 a breaking change bumps minor too, so the size is minor either way and the entry gets a "What to do" line; #259 (a new skill, a new optional `setup-dev-skills` section) **minor**, since no existing doc's format changes; #260 (skills move from `upstream-skills/` to `skills/`, names unchanged) **patch** at most, no project must act; #261 (`scripts/check-plugin.sh`), #262 (Upstream watch), #256 (ADR) and the `REVIEW.md` and glossary lines **ride along** (repo-only). Biggest: minor, so 0.22.27 becomes **0.23.0**, the version the label names; no rename is proposed.
- **Step 3 (proposed, not opened):** a branch from main changing only `"version": "0.22.27"` to `"0.23.0"`, and this entry at the top of `CHANGELOG.md`: heading `## 0.23.0 (<date of the cut>)`, the goal sentence above, one line each for #257, #258, #259, #260, #261 and #262, "Also merged: ADR 0008, the decision behind this Release (#256); two REVIEW.md Always check lines from its retro.", and "What to do: a project whose own rules take a version or other numbers at merge time no longer gets a numbering step from `implement` or `implement-spec`; take them by hand, or cut Releases with `release` (run `setup-dev-skills` to write the release doc)." Extra steps: the `PATCHES.md` line "version 0.22.27 to 0.23.0" only if `PATCHES.md` still exists then (#260 deletes it), then both checks. Body by `pr`, naming #263, size minor with the lines above, no dropped issues, Door one-way. The user merges.
- **Step 4:** not run (nothing merged).
- **Step 5 (proposed, nothing labelled):** candidates, the open `ready-for-agent` issues with no release label: #267, #266, #250, #225, #224, #223, #222, #221 and #145; none carried over. Proposed goal: "`agentic-review`'s Rank step holds, merges and dismisses Findings correctly across Rounds." Proposed scope (5 of 5): #221, #222, #223, #224 and #225, all Pre-existing Findings on Rank and Verify from the review of #215, one area and one root cause (Finding matching across Rounds). All are fixes, so the next version is **0.23.1** and the label `release-0.23.1`. Each changes the `agentic-review` skill, so the user merges each (this repo's own rule). Left out: #267 (`to-tickets` absorbs several issues, new behaviour, minor) and #266 (a `REVIEW.md` Skip line, repo-only) for the Release after; #250 (the `PATCHES.md` header) is likely obsolete once #260 deletes `PATCHES.md`, so recheck it then rather than build it; #145 (glossary and wording) looks already done on main (the Question round entry, `codebase-design`'s description, the `PATCHES.md` heading), so `triage` should verify and close it rather than build it.

Not exercised: the carry-over branch of step 1, a dropped issue, a label rename in step 2, a breaking change at or above 1.0.0, steps 3 and 4 for real (opening the bump pull request, the user's merge, the notes comment and the close), labelling and opening the next release issue in step 5, a raised cap, the first-Release path, the missing-release-doc stop and the "Urgent fix" path.

Pass: yes, as a proposal. Lessons: the first run found that #263, written by hand before the skill existed, carries no release label, so the skill finds the release issue by its title and gives it no label of its own, and the release issue template in step 5 follows #263's shape (Goal, Label, Cap, Scope, Notes). The step 2 sizes of #258 and #260 are judgement calls for the user to confirm in the bump pull request.
