# Release thread report (2026-11-04)

## Release mode
`docs/dev-skills/release.md` has no bump-mode line. The `release` skill on main takes that to mean "Releases bump", which needs a version file. This repo keeps no version, though ("Policy: none"), and its Release name line gives name, label and title forms (`Release <n>`, `release-<n>`, `Release <n>`). So I ran the Release the way the skill runs one when pull requests bump: Releases are named, not numbered, there is no bump pull request, and the changelog entry lists no versions, as the release doc asks. If that is wrong, please add a bump-mode line to the release doc.

## Cut
There is no Release to cut. Release 2 (#2) is closed and already has its notes, no open issue is titled `Release <n>`, and no open issue carries a `release-*` label. So nothing was cut, and no changelog pull request was opened.

## Release 3 planned (inside Milestone 1, #1)
- **Goal:** The greeter can say goodbye and greet quietly, finishing Milestone 1's planned commands.
- **Name and label:** Release 3, `release-3` (a new label).
- **Scope:** 2 features, taken in the Milestone's order. The cap is 5, and the release doc's "Release size: 2" is also met.
  1. Farewell command: #10 (the Spec), with its Tickets #11 and #12.
  2. Quiet flag: #20.
- **Maintenance fixes:** none planned. See below.
- **Release issue:** new, `Release 3` (proposed as 38-release-3.md). Every proposed write is in `.scratch/proposed-actions.md`.

Issues filed from now on wait for the next Release planning, apart from Tickets split from a Spec in this Release.

## Sources not read: maintenance fixes may be missing
The skill reads maintenance fixes from two records about Release 2 (#2):
- a `## Triage batch` comment on #2;
- a closed `retro-planning` issue created after #2.

Neither exists. Instead, #2 has two `<!-- release end-of-Release pass -->` comments that say triage and retro-planning ran, but they hold no rows. The skill reads only those two records, so I planned the feature scope alone. As a result, Release 3 may be missing Release 2's maintenance fixes. #35 (`test.sh` takes 10 s) carries `next-release`, and its body says Retro planning for Release 2 marked it to join the next Release. That is not a form the skill reads, so #35 was left out. Tell me if it should join.

## Questions for you (one per candidate; nothing was labelled for these)
Milestone 1 does not list any of these, so only you can add them to a Release:
1. **#36 test.sh fails on main, so no pull request can pass** (bug). If this is true, nothing in Release 3 can merge, so it would block the whole Release. Should it join Release 3? Note: in this checkout `bash test.sh` passes on main, and the #9 it names is not in the git history, so it may need triage first.
2. **#37 test.sh prints the registry token in CI logs** (bug, security). Should it join Release 3? Note: the current `test.sh` does not echo `$REGISTRY_TOKEN`.
3. **#31 `--save` overwrites ~/.profile** (bug, user data lost). Should it join Release 3? Note: the current `src/greet.sh` has no `--save` option.
4. **#35 test.sh takes 10 s** (bug, marked `next-release`). Should it join Release 3 as a maintenance fix?

The release doc says "A severe issue joins past it" (past the Release size). The `release` skill on main has no such rule, so I added none of these myself. If #31, #36 or #37 is severe, it is your call to add it.
