### 1. Create an issue
Issue: new (38-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** Main's check passes again, and the greeter stops overwriting users' `~/.profile` and leaking the registry token, so Milestone 1's commands can be built and merged safely.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 2. Used: 2, plus 1 severe past the size.

## Order

1. #36 test.sh fails on main, so no pull request can pass: severe, delivery stopped (every pull request's check is red, nothing can merge); oldest severe issue (2026-10-05).
2. #31 `--save` overwrites ~/.profile: severe, lost data (the user's shell settings are overwritten); severe, created 2026-10-20.
3. #37 test.sh prints the registry token in CI logs: severe, a security hole (the token is in every public CI log); newest severe issue (2026-10-25), joins past the size because it is severe.

## Left out

- #35 test.sh takes 10 s: the size was reached (group 1, marked `next-release` by Retro planning for Release 2: `test.sh` sleeps 10 s for nothing); keeps its `next-release` mark.
- #10 Farewell command: the size was reached (group 2, first planned feature: no feature depends on another, both move the Milestone's goal equally, so the Milestone issue's order puts it first; its Tickets #11 and #12 stay with it).
- #20 Quiet flag: the size was reached (group 2, second planned feature, by the Milestone issue's order).

## Checked against main

Main at `788e2cf`.

- #10 Farewell command: still valid
- #11 bye: the command: still valid
- #12 bye: usage text: still valid
- #20 Quiet flag: still valid
- #31 `--save` overwrites ~/.profile: still valid
- #35 test.sh takes 10 s: still valid
- #36 test.sh fails on main, so no pull request can pass: still valid
- #37 test.sh prints the registry token in CI logs: still valid

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
