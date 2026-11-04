# Releases

How this repo cuts a Release with the `release` skill: how Releases are named and sized, where the changelog goes, what the cut runs, and the repo's versioning policy.

- **Versioning policy**: pull requests bump.
- **Release name**: the name `Release <n>`, the label `release-<n>` and the title `Release <n>`.
- **Release size**: 5.
- **Changelog**: `CHANGELOG.md`, newest entry first. One entry per Release, covering everything merged since the last Release, with its start and end commits.
- **Label prefix**: `release-`.
- **Cut steps**: what the cut runs after the changelog entry is written, in order; the policy section below adds its own. None.
- **Whole-Release check**: `npm test`.

## Policy text

 Each pull request that changes `src/` bumps the version as its last commit, with the number given as the person who merges. A Release opens no pull request to bump: its changelog pull request changes no version.

- **Version file**: `package.json`, the `"version"` field. A bump changes only this value in it.
- **Extra cut step**: the changelog entry carries the line `Versions: <the versions delivered, oldest first, each once, or "none, the version stays X.Y.Z">. Commits: <start>..<end>.` under the goal. The versions delivered are each value the version file reached since the last Release's end commit.

### The bump commit

The merging thread adds it as the pull request's last commit, just before merge:

- Change the version in the version file, and nothing else in it.
- Anything else the bump commit must change or run, such as a second file that repeats the version or a check to run before pushing. None.
