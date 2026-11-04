# Release thread report (2026-11-04)

## Release 2: cut

- Bump mode: the release doc names none (which the `release` skill reads as "Releases bump"), but this repo keeps no version ("Policy: none"), names Releases `Release <n>` and names a whole-Release check on a "changelog pull request". The Releases-bump path cannot run here (no version file; the names are not versions; its title pattern would not even find `Release 2`), so I cut it the way Release 1 was cut: one changelog pull request that changes no version. Please add a bump-mode line to `docs/dev-skills/release.md` (this repo fits "pull requests bump" with no versions) so the next Release does not depend on this reading; the skill itself has no explicit no-version mode.
- Shipped: #10 Farewell command (PR #7), #20 Quiet flag (PR #8). Both pass the shipped test. Dropped: none. Also merged: #9 (README usage).
- Commits: 9a18f55..1c6fe96. Versions delivered: none (no version kept), so the entry has only a `Commits:` line, like Release 1's.
- Whole-Release check `bash test.sh`: OK.
- Changelog pull request #22 `docs(release): Release 2` opened and merged by me (the Boundary record lets agents merge docs-only changelog pull requests); entry posted on #2 as its notes and #2 closed.

## Release 3: planned (inside Milestone 1, no reply needed)

- Scope: 1 of 5 features: #21 Shout flag, the last planned feature in Milestone 1's order. Label `release-3` created and applied to #21; release issue `Release 3` opened (#23).
- Maintenance fixes: none taken. The Triage batch (`triage`) and the Release-end Retro planning (`retro-planning`) were started for Release 2, but in this dry run they wrote nothing: there is no `## Triage batch` comment on #2 and no closed retro-planning record, so neither source was read and **Release 3's maintenance fixes may be missing**. The next planning will not look again.
- Left-out candidates: none.
- Issues filed from now on wait for the next Release planning, apart from Tickets split from a Spec in this Release.
- After Release 3 ships, every planned feature of Milestone 1 is done, so the Milestone review follows.

All writes are proposed in `.scratch/proposed-actions.md` (dry run); nothing was committed or branched.
