# Releases

How this repo cuts a Release with the `release` skill: where the version lives, where the changelog goes, and how the release labels are named. Ordinary pull requests leave the version alone; only a Release's bump pull request changes it (see [ADR 0008](../adr/0008-plugin-versions-change-only-at-a-release.md)).

- **Version file**: `plugins/dev-skills/.claude-plugin/plugin.json`, the `"version"` field. This is the canonical source for reading the current version and locating the last Release in git history.
- **Synchronized version copy**: `plugins/dev-skills/.codex-plugin/plugin.json`, the `"version"` field. The bump pull request changes only the version field in both manifests, to the same version. Do not use this copy to locate Release history: its creation introduces the existing version without cutting a Release.
- **Changelog**: `plugins/dev-skills/CHANGELOG.md`, newest entry first.
- **Label prefix**: `release-`, so a Release's label is `release-X.Y.Z` (for example `release-0.23.0`) and its release issue is titled `Release X.Y.Z`.

Releases here cover the `dev-skills` plugin only. `dai-portal-data` has no release doc of its own yet, so its version is left as it is.

## Extra steps in the bump pull request

- Update both manifests to the same version; leave their other fields unchanged. The `codex-packaging` check rejects drift.
- Before pushing, run `bash scripts/check-plugin.sh` and `claude plugin validate .`.
