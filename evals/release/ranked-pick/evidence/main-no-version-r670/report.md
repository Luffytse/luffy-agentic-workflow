# Release thread report (2026-11-04 09:00 UTC)

All writes are dry-run proposals, listed in order in `.scratch/proposed-actions.md`.

## Release 2: cut and closed

- Done check: #10 Farewell command shipped (PR 7, `Closes #10`) and #20 Quiet flag shipped (PR 8, `Fixes #20`). Nothing was dropped and nothing blocked the cut.
- Changelog PR 10, `docs(release): Release 2`: commits 9a18f55..1c6fe96. It lists #10 and #20, plus "Also merged: README usage (#9)". It lists no versions, because the release doc's versioning policy is none. There were no cut steps.
- The whole-Release check, `bash test.sh`, passed. The Boundary record lets agents merge, so the thread merged it as a squash. That merge closes no issue.
- Release issue #2 gets the entry as its notes and is closed as completed.
- In the dry run, main does not actually change. I treated the proposed merge of PR 10 as done when I read main's changelog for the notes (step 3) and checked the merge ("After the merge").

## End-of-Release pass

The thread ran `triage` (Triage batch) and `retro-planning` (Release-end) for Release 2, and recorded each one on #2. Both ran. In this dry run they change nothing.

## Release 3: planned

- **Order:** 1. #21 Shout flag. It is the last planned feature of Milestone #1, it has no blockers, and it completes the Milestone's goal.
- **Size used:** 1 of 5. There are no severe issues, `next-release` issues or `ready-for-agent` bugs to fill the rest.
- **Left out:** none.
- **Proposed to the user:** none. There are no unplanned features.
- Label `release-3` is created and applied to #21. Release issue #22 is opened.

## Observation, not blocking

`src/greet.sh` on main has only `# bye` and `# quiet` comment lines for #10 and #20. Its `case` has no `bye` branch and no `-q` handling, and `test.sh` tests only `hello`. Both issues pass the shipped test (merged PRs with closing keywords), so the cut goes ahead. The features may still be missing, though, and you may want a bug filed for each.
