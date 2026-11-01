# Releases

How this repo versions `dev-skills` and cuts a Release with the `release` skill: where the version lives, how a pull request bumps it, where the changelog goes, and how Releases and their labels are named (see [ADR 0008](../adr/0008-each-skill-change-bumps-the-plugin-version.md)).

**Bump mode: pull requests bump, Releases do not.** In this repo every pull request that changes a file under `plugins/dev-skills/skills/` bumps the version as its last commit, with the number the coordinator hands out just before merge. A Release opens no bump pull request: it writes the changelog entry and runs the whole-Release check. Until piece #397 changes the `release` skill, its bump pull request step does not apply here. Until #397 changes `release`, it neither finds nor names a named Release (it looks for `Release X.Y.Z` titles and the commit that set the version), so no Release here is cut with today's `release` skill: the release issue and label are written by hand, as #414 was, and the cut follows #397.

- **Version file**: `plugins/dev-skills/.claude-plugin/plugin.json`, the `"version"` field. This is the canonical source for reading the current version, and for locating Releases up to 0.25.0 in git history.
- **Synchronized version copy**: `plugins/dev-skills/.codex-plugin/plugin.json`, the `"version"` field. A bump changes only the version field in both manifests, to the same version. Do not use this copy to locate Release history: its creation introduces the existing version without cutting a Release.
- **Changelog**: `plugins/dev-skills/CHANGELOG.md`, newest entry first. One entry per Release, covering everything since the last Release and listing the versions it delivered.
- **Label prefix**: `release-`. A Release is named, not numbered: `Milestone <m> · Release <n>`, with the label `release-m<m>-r<n>` (for example `release-m1-r1`) on every issue in it and a release issue titled `Release Milestone <m> · Release <n>`. The release issue records the Release's start and end commits and the versions it delivered. Releases up to 0.25.0 were numbered (`release-X.Y.Z`, titled `Release X.Y.Z`). Until #397, the release issue and label are written by hand (see above).

Releases here cover the `dev-skills` plugin only. `dai-portal-data` has no release doc of its own yet, so its version is left as it is.

## The bump commit

The merging thread adds it as the pull request's last commit, just before merge, with the number the coordinator handed out:

- Update both manifests to the same version; leave their other fields unchanged. The `codex-packaging` check rejects drift.
- Before pushing, run `bash scripts/check-plugin.sh` and `claude plugin validate .`.
