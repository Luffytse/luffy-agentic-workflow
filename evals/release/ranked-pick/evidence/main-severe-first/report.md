# Release thread report (2026-11-04 09:00 UTC)

## No Release to cut

No release issue is open and no open issue carries a release label (`release-2` is only on closed #3; Release 2 was cut and closed on 2026-10-16). Nothing has merged to main since Release 2's changelog pull request (`b5280c5`). So nothing was cut, and the thread went straight to Release planning.

Bump mode: the release doc names none, but it says the repo keeps no version and gives name, label and title forms (`Release <n>`, `release-<n>`) and a whole-Release check. I read it as named Releases with no version (the "pull requests bump" forms, with no version file).

## Release 3, planned inside Milestone #1 (proposed, dry run)

Release issue `Release 3` (new #36), label `release-3` (a new label). Goal: close the name-leaking log hole, then round out the greeter with the farewell command and the quiet flag.

- Cap 5 features, 2 used:
  1. Farewell command: Spec #10 and its Tickets #11, #12. First in the Milestone's order.
  2. Quiet flag: #20. Second in the Milestone's order.
- Maintenance fixes, outside the cap:
  - **#31, the world-readable name log (security). Severe: build it first.** The release doc's rule is that a severe issue joins past the Release size. One thing to check: the current `src/greet.sh` has no log write, so the build thread should first confirm the bug reproduces.
  - #35, the 10 s test.sh. Retro planning for Release 2 marked it with `next-release`.
- Left out: #30, the usage typo. It is not a planned feature and nothing marked it. `src/greet.sh` already reads `hello`, so it looks stale; send it back to `triage` to close.

## Records in the wrong form

The `release` skill reads maintenance fixes from `## Triage batch` comments on the release issue that was just cut, and from a closed `retro-planning` record with a Verdicts table. Release 2 has neither. It has only `<!-- release end-of-Release pass -->` notes saying triage and retro-planning ran. I took #35 from its `next-release` label, which the repo's triage-labels doc defines as "must join the next Release". If those passes chose any other fix for Release 2 and recorded it only in a form I could not read, that fix may be missing from Release 3.

From now on, new issues wait for the next Release planning. The exception is Tickets split from a Spec in Release 3. Nothing here waits on your reply. All writes are listed in `.scratch/proposed-actions.md`.
