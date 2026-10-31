# Releases

How this repo cuts a Release with the `release` skill: where the version lives, where the changelog goes, and how the release labels are named. Ordinary pull requests leave the version alone; only a Release's bump pull request changes it (see [ADR 0008](../adr/0008-plugin-versions-change-only-at-a-release.md)).

- **Version file**: `plugins/dev-skills/.claude-plugin/plugin.json`, the `"version"` field. The bump pull request changes only this value in it.
- **Changelog**: `plugins/dev-skills/CHANGELOG.md`, newest entry first.
- **Label prefix**: `release-`, so a Release's label is `release-X.Y.Z` (for example `release-0.23.0`) and its release issue is titled `Release X.Y.Z`.

Releases here cover the `dev-skills` plugin only. `dai-portal-data` has no release doc of its own yet, so its version is left as it is.

## Extra steps in the bump pull request

- Before pushing, run `bash scripts/check-plugin.sh` and `claude plugin validate .`.
