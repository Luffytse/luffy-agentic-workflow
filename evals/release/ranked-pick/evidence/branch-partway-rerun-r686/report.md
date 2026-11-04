# Release thread report, 2026-11-04 09:00 UTC

**Where it stood.** Release 2 (#2) is open. Its Order lists #20, #21 and #31, but #21 Shout flag did not carry `release-2`. #31 counts as accounted for because the issue's `## Carried over` section lists it. So this was a planning that stopped part way (case 1). This run finished it under "Rerun first": the Order stays as written and nothing was ranked again.

**Check against main** (main at `a09d5f0`). This covered the open issues with no release label, #21 and #31. Both are still valid:
- #21: `src/greet.sh` has no `-s` flag. `greet.sh hello -s Ada` prints `Hello, -s!`.
- #31: `greet.sh hello ''` still prints `Hello, !`.

No issue was closed or edited, and no question was raised.

**Writes proposed** (dry run, in `.scratch/proposed-actions.md`):
1. Add the missing `## Checked against main` and `## Proposed to the user` sections to the Release 2 issue.
2. Apply `release-2` to #21.

**Release 2 now:**
- Order: #20 Quiet flag and #21 Shout flag, both Milestone 1 features in the Milestone's order, plus #31.
- Size: 5. Used: 3 (as recorded).
- Left out: none.
- Proposed to you: none.
- `next-release`: no issue carries it, so none was removed.

**Notes for you:**
- **#31 stays unlabelled.** It is in the Order and also under the Release's own `## Carried over`. The skill says an issue listed there stays carried over, so it is not labelled. The Release cut does not wait on it. The next planning will see it again as a carried-over `ready-for-agent` bug (group 3). If you meant #31 to be built in Release 2, remove its Carried over line and label it `release-2`.
- **The Goal does not match the Order.** It reads "Say goodbye and keep quiet", but no issue in the Order is about saying goodbye. I left the Goal as written, since a rerun does not re-plan. You may want to correct it.
