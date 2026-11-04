# Releases

How this repo cuts a Release with the `release` skill: how Releases are named and sized, where the changelog goes, what the cut runs, and the repo's versioning policy.

- **Versioning policy**: none.
- **Release name**: the name `Release <n>`, the label `release-<n>` and the title `Release <n>`.
- **Release size**: 5.
- **Changelog**: `CHANGELOG.md`, newest entry first. One entry per Release, covering everything merged since the last Release, with its start and end commits.
- **Label prefix**: `release-`.
- **Cut steps**: what the cut runs after the changelog entry is written, in order; the policy section below adds its own. None.
- **Whole-Release check**: `npm test`.

## Policy text

 This repo keeps no version. A Release's changelog entry lists no versions, and no cut step changes a version.
