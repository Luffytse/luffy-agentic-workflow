# Releases

How this repo versions `dev-skills` and cuts a Release with the `release` skill: where the version lives, how a pull request bumps it, where the changelog goes, how Releases and their labels are named, and the whole-Release check (see [ADR 0008](../adr/0008-each-skill-change-bumps-the-plugin-version.md)).

- **Bump mode**: pull requests bump. Every pull request that changes a file under `plugins/dev-skills/skills/` bumps the version as its last commit, with the number the coordinator hands out just before merge (see "The bump commit" below). A Release opens no bump pull request: the `release` skill writes the changelog entry in a changelog pull request, runs the whole-Release check and closes the release issue with its notes.
- **Version file**: `plugins/dev-skills/.claude-plugin/plugin.json`, the `"version"` field. This is the canonical source for reading the current version, and for locating Releases up to 0.25.0 in git history.
- **Synchronized version copy**: `plugins/dev-skills/.codex-plugin/plugin.json`, the `"version"` field. A bump changes only the version field in both manifests, to the same version. Do not use this copy to locate Release history: its creation introduces the existing version without cutting a Release.
- **Changelog**: `plugins/dev-skills/CHANGELOG.md`, newest entry first. One entry per Release, covering everything since the last Release, listing the versions it delivered and its start and end commits (its `Versions:` and `Commits:` line).
- **Label prefix**: `release-`.
- **Release name**: `Milestone <m> · Release <n>`, with the label `release-m<m>-r<n>` (for example `release-m1-r1`) on every issue in it and a release issue titled `Release Milestone <m> · Release <n>`. A Release is named, not numbered; the next Release in the same Milestone raises `<n>`, and a new Milestone starts again at `<n>` = 1. Releases up to 0.25.0 were numbered (`release-X.Y.Z`, titled `Release X.Y.Z`).
- **Whole-Release check**: on the changelog pull request's branch, run `bash scripts/check-plugin.sh`, `python3 scripts/test-check-plugin.py` and `claude plugin validate .`, then a clean-up pass: search the repo for sentences that wait on an issue this Release closed (such as "until #<n>") and for text its merges left stale. Fix such text outside `plugins/dev-skills/skills/` in the changelog pull request; file stale skill text as an issue for the next Release planning, so the changelog pull request changes no version.

Releases here cover the `dev-skills` plugin only. `dai-portal-data` has no release doc of its own yet, so its version is left as it is.

## The bump commit

The merging thread adds it as the pull request's last commit, just before merge, with the number the coordinator handed out:

- Update both manifests to the same version; leave their other fields unchanged. The `codex-packaging` check rejects drift.
- Before pushing, run `bash scripts/check-plugin.sh` and `claude plugin validate .`.
