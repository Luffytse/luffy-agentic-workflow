# Releases

How this repo versions `dev-skills` and cuts a Release with the `release` skill: where the version lives, how a pull request bumps it, where the changelog goes, how Releases and their labels are named, and the whole-Release check (see [ADR 0008](../adr/0008-each-skill-change-bumps-the-plugin-version.md)).

- **Bump mode**: pull requests bump. Every pull request that changes a file under `plugins/dev-skills/skills/` bumps the version as its last commit, with the number the coordinator hands out just before merge (see "Version hand-out" and "The bump commit" below; `CLAUDE.md` "Merge-time steps" states the rules). A Release opens no bump pull request: the `release` skill writes the changelog entry in a changelog pull request, runs the whole-Release check and closes the release issue with its notes.
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

## Version hand-out

This repo's rule, not a skill's: the skills only say to follow the merge-time steps the repo's docs give. The coordinator gives the number (the user, when no coordinator runs).

- **Who asks, when.** The thread about to merge a pull request that changes a file under `plugins/dev-skills/skills/` asks just before merging. A pull request that changes no such file gets no number and merges with no bump.
- **The number.** The `version` of `plugins/dev-skills/.claude-plugin/plugin.json` on main, freshly fetched, raised minor for a new or changed skill and patch for a fix or a revert; below 1.0.0 a breaking change bumps minor (ADR 0008).
- **The record.** Before telling the thread, comment on the issue the pull request builds (a Spec pull request: the Spec; a pull request that builds no issue: the pull request itself). First line `<!-- version hand-out -->`, second `Version <number> for <pull request>: merge it next, with the bump as its last commit, as the release doc says.` Then tell the thread its number.
- **Older records.** A record under the earlier marker `<!-- milestone version hand-out -->` counts as a hand-out record too, for "out", void and waiting alike.
- **One at a time.** A number is **out** while main's version has not reached it, its pull request is open and the thread it was given to is running. Read main's version and the hand-out records on the open skill-changing pull requests' issues: a record is out when all three hold. A record whose pull request closed unmerged, or whose issue or pull request is parked, is void, and so is one whose thread has ended. While one is out, give none: comment on the same issue with first line `<!-- version hand-out -->` and second line `Waiting: <pull request> asked while <number> was out.`, and tell the thread to wait. At the first wake when no number is out and a waiting request has no number after it, give numbers to the waiting requests one at a time, in the order they asked. So skill-changing pull requests merge one at a time, each on top of the one before.
- **Waiting requests are served at any wake**, a scheduled check-in included, not only when a merge is reported: a number goes void with no report when its pull request closes unmerged, is parked, or its thread ends.
- **During a pause** (the user's word to pause delivery) give no number: record the request as waiting, as above, and tell the thread to wait. A number already out stays out and its merge may finish. Waiting requests are served after the resume.
- **A repeat.** A thread that asks again because main's version moved under it gets a new number from the new main, recorded the same way; its earlier record is void.
- **After the merge.** Read the version on main. It should read the number. If it reads anything else, give no further number and tell the merging thread to put main right first.

## Ticket re-read after a skill merge

This repo's rule, not a skill's. The coordinator (or a `triage` thread it briefs with the merge, the changed skill, main's version and the issues, which then holds every further start until it reports) follows it.

- **When.** Right after a pull request that changed a file under `plugins/dev-skills/skills/` merges, before any further thread starts.
- **Which issues.** The open issues that no running thread is building and whose body names the changed skill or a file the merge changed; inside a Milestone, only those carrying its membership label. A running thread keeps the skill version it started with until its Ticket or Spec is done.
- **Read each against main's new text of the skill, then one of three outcomes:**
  - the change makes it wrong or incomplete: update it. Read the whole body, write it whole back with only that change and a one-line note naming the merge, and read it back. A change that would alter a Milestone's agreement (goal, acceptance or exclusions) goes to the user as one question, and that feature waits for the answer;
  - the change makes it obsolete: close it, with a note naming the merge;
  - otherwise: comment that it was re-read after the merge and still fits.
- **Then** read the blockers again and take the next start from what they now say.
