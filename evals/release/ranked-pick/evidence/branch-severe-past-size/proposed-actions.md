### 1. Create an issue
Issue: new (38-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** Main is safe and mergeable again: `test.sh` passes on main, no longer leaks the registry token, and `--save` no longer overwrites `~/.profile`.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 2. Used: 2, plus 1 severe past the size.

## Order

1. #36 test.sh fails on main, so no pull request can pass: severe (delivery stopped: every pull request's check is red and nothing can merge); oldest severe issue (2026-10-05), and every other fix needs it to merge.
2. #31 `--save` overwrites ~/.profile: severe (lost data: the user's settings are overwritten); second-oldest severe issue (2026-10-20).
3. #37 test.sh prints the registry token in CI logs: severe (security hole: the token is in every public CI log); third-oldest severe issue (2026-10-25), joins past the size.

## Left out

- #35 test.sh takes 10 s: marked `next-release` by Release 2's Retro planning (a 10 s sleep for nothing); the size was reached. It keeps its mark.
- #10 Farewell command: planned feature, first after re-ordering (no feature depends on the other; it adds a whole command, moving the Milestone's goal furthest, and is first in the Milestone's order); the size was reached.
- #20 Quiet flag: planned feature, second after re-ordering (a flag on an existing command; second in the Milestone's order); the size was reached.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 2. Create a label
Issue: none
Label: release-3

### 3. Apply / remove labels
Issue: 36-ci-red.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 31-profile.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 37-token-log.md
Add: release-3
Remove: none
