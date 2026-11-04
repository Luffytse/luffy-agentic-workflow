# Release thread report (2026-11-04)

**Where I started:** no open release issue, and no open issue carries a release label. The last release issue, #2 (Release 2), is closed with its notes and both end-of-Release records (triage, retro-planning), so this run went straight to step 5: plan the next Release. Nothing was cut this run.

## Release 3 planned (release issue #38, label `release-3`, Milestone #1)

**Goal:** No pull request is blocked by a red check and the greeter no longer destroys the user's settings or leaks the registry token.

**Size:** 2. Used: 2, plus 1 severe past the size.

### Order

1. #36 test.sh fails on main, so no pull request can pass: severe (delivery stopped), oldest severe issue.
2. #31 `--save` overwrites ~/.profile: severe (lost data).
3. #37 test.sh prints the registry token in CI logs: severe (security hole). Joins past the size, because the size was full after #31 and a severe issue always joins.

### Left out (all because the size was reached)

- #35 test.sh takes 10 s: marked `next-release`; ranked after the severe issues. It keeps its `next-release` mark and will lead the next planning, after any severe issue.
- #10 Farewell command (Spec, Tickets #11, #12): first planned feature (a new command moves the Milestone's goal furthest; first in the Milestone's order).
- #20 Quiet flag: second planned feature.

### Proposed to you

None: no open unplanned feature.

### Note

Three severe bugs fill this Release, so the Milestone's features do not start until Release 4 at the earliest. If you want a feature in sooner, raise the Release size in `docs/dev-skills/release.md` or carry a bug out. Nothing waits on your reply.

Dry run: the tracker writes (create #38, create label `release-3`, label #36, #31, #37) are in `.scratch/proposed-actions.md`.
