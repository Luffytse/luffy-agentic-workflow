Title: Release 3

**Goal:** No pull request is blocked by a red check and the greeter no longer destroys the user's settings or leaks the registry token.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 2. Used: 2, plus 1 severe past the size

## Order

1. #36 test.sh fails on main, so no pull request can pass: severe, delivery stopped (every check is red and nothing can merge); oldest severe issue (2026-10-05).
2. #31 `--save` overwrites ~/.profile: severe, lost data (the user's settings are overwritten); second-oldest severe issue (2026-10-20).
3. #37 test.sh prints the registry token in CI logs: severe, a security hole (the token is in every public CI log); youngest severe issue (2026-10-25), joins past the size because it is severe.

## Left out

- #35 test.sh takes 10 s: marked `next-release` by Retro planning for Release 2 (test.sh sleeps 10 s for nothing), ranked after the severe issues; the size was reached. It keeps its `next-release` mark.
- #10 Farewell command: planned feature, ranked first of the features (a new command moves the Milestone's goal, rounding out the greeter's commands, furthest; neither feature depends on the other, and it is first in the Milestone's order); the size was reached.
- #20 Quiet flag: planned feature, ranked after #10 (a flag on an existing command moves the goal less; second in the Milestone's order); the size was reached.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
