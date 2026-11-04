# Release planning: Release 3 (2026-11-04)

Release 2 was already cut and closed, with both end-of-Release records (triage and retro-planning), so this run went straight to planning the next Release. Nothing below waits on a reply.

Release issue: new #38 "Release 3", label `release-3` (label to be created), Milestone #1.

**Goal:** Main is safe and mergeable again: `test.sh` passes on main, no longer leaks the registry token, and `--save` no longer overwrites `~/.profile`.

**Size:** 2. Used: 2, plus 1 severe past the size.

## Order

1. #36 test.sh fails on main, so no pull request can pass: severe (delivery stopped); oldest severe issue.
2. #31 `--save` overwrites ~/.profile: severe (lost data); second-oldest severe issue.
3. #37 test.sh prints the registry token in CI logs: severe (security hole); joins past the size, as every severe issue does.

## Left out

- #35 test.sh takes 10 s (`next-release`): the size was reached; it keeps its `next-release` mark for the next planning.
- #10 Farewell command (Spec, Tickets #11, #12): planned feature; the size was reached.
- #20 Quiet flag: planned feature; the size was reached.

## Proposed to the user

None: no unplanned feature is open.

Dry run: the writes are in `.scratch/proposed-actions.md` (create #38, create label `release-3`, apply it to #36, #31, #37). No issue taken carried `next-release`, so none was removed.
