# Releases

How this repo versions `dev-skills` and cuts a Release with the `release` skill: where the version lives, how a Release raises it, where the changelog goes, how Releases and their labels are named, and the whole-Release check (see [ADR 0016](adr/0016-releases-bump-the-plugin-version-once.md), which replaced ADR 0008).

- **Bump mode**: Releases bump. A pull request never changes the version, a skill pull request included: it merges like any other, with no number to ask for. The Release's changelog pull request raises it once, in the plugin manifest, by the biggest size among the Release's changes (see the cut steps).
- **Version file**: `plugins/dev-skills/.claude-plugin/plugin.json`, the `"version"` field. This is the canonical source for reading the current version, and for locating Releases up to 0.25.0 in git history.
- **Changelog**: `plugins/dev-skills/CHANGELOG.md`, newest entry first. One entry per Release, covering everything since the last Release, listing the versions it delivered and its start and end commits (its `Versions:` and `Commits:` line).
- **Versioning policy**: Releases bump (the **Bump mode** line above is the same fact under its earlier name).
- **Label prefix**: `release-`.
- **Release name**: `Milestone <m> · Release <n>`, with the label `release-m<m>-r<n>` (for example `release-m1-r1`) on every issue in it and a release issue titled `Release Milestone <m> · Release <n>`. A Release is named, not numbered; the next Release in the same Milestone raises `<n>`, and a new Milestone starts again at `<n>` = 1. Releases up to 0.25.0 were numbered (`release-X.Y.Z`, titled `Release X.Y.Z`).
- **Release size**: 10. A Release takes at most 10 items, counted of any kind: a Spec with its Tickets is 1, a lone Ticket is 1, a bug is 1. A severe issue (a security hole, lost data, delivery stopped) joins past the size.
- **Size of each change**, by what a project using the plugin must do (ADR 0016):
  - **patch (Z)**: a fix. A skill now does what it already promised; no project has to change anything. A revert is a patch.
  - **minor (Y)**: a new or changed skill that breaks nothing, such as a new skill or a new step or option in one.
  - **major (X)**: a breaking change: a project using the plugin must do something, because a skill was renamed or removed, the format of a repo doc that `setup-dev-skills` writes changed, or a label the skills need changed. Below 1.0.0 a breaking change raised the minor part; the plugin has been at 1.0.0 or later since 2026-11-04.
  - **rides along**: changes outside `plugins/dev-skills/skills/` (the README, the changelog, ADRs, the glossary, scripts, tooling) never decide the size.
- **Cut steps**: after the changelog entry is written, in this order:
  1. Read every change the Release delivers (the merged pull requests since the last Release's end commit) and give it a size. The Release's size is the biggest among them: major for a breaking change, minor for a new or changed skill, patch when the skill changes are fixes or reverts only. A Release that changed no file under `plugins/dev-skills/skills/` leaves the version as it is.
  2. Raise the version in the changelog pull request, in `plugins/dev-skills/.claude-plugin/plugin.json`, from the current version with every part after the raised one set to 0, and change nothing else in it.
  3. Put the line `Versions: <the one new version, or "none, the version stays X.Y.Z" for a Release that changed no skill file>. Commits: <start>..<end>.` under the entry's goal.
  4. Run the whole-Release check below on that pull request's branch.
  5. The Release thread merges the changelog pull request as the Boundary record allows. A merged version bump is no one-way door here, and no cut waits for the user.
- **Whole-Release check**: on the changelog pull request's branch, run `bash scripts/check-plugin.sh`, `bash scripts/run-tests.sh` and `claude plugin validate .`, then a clean-up pass: search the repo for sentences that wait on an issue this Release closed (such as "until #<n>") and for text its merges left stale. Fix such text outside `plugins/dev-skills/skills/` in the changelog pull request; file stale skill text as an issue for the next Release planning. The version change of the cut (step 2) is the only version change the pull request makes.
- **Recovery**: a bad merged change is reverted on main at once and fixed properly; the revert is a patch-size change in the next Release. The user is told; nobody waits for them.

Releases here cover the `dev-skills` plugin, the only plugin in this repo.

Bare issue and pull request numbers in text written before the move on 2026-11-05 (ADRs 0001 to 0013, changelog entries before the move entry, and the issues moved from the archive, which link their original) refer to the private archive `Luffytse/luffy-dev-skills`; from the move on, a bare number means this repo's issue, and a reference to an archive issue is written in full as `Luffytse/luffy-dev-skills#<n>`. The commits recorded for past Releases (`Commits:` lines) are the archive's IDs; the history here was rewritten (ADR 0014), so those IDs do not resolve in this repo.
