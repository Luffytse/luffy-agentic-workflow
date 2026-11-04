# Proposed actions

### 1. Create an issue
Issue: new (38-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** Main's test check passes again, and the greeter no longer overwrites `~/.profile` or prints the registry token in CI logs, so Milestone 1's commands can be built and shipped safely.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 2. Used: 2, plus 1 severe past the size.

## Order

1. #36 test.sh fails on main, so no pull request can pass: severe (delivery stopped): `bash test.sh` fails on main since #9, so no pull request's check can pass and nothing can merge; oldest severe issue (2026-10-05).
2. #31 `--save` overwrites ~/.profile: severe (lost data): `greet.sh hello <name> --save` writes over the user's `~/.profile`; second-oldest severe issue (2026-10-20).
3. #37 test.sh prints the registry token in CI logs: severe (security hole): the token is echoed into every public CI log; joins past the size, as every severe issue does (2026-10-25).

## Left out

- #35 test.sh takes 10 s: the size was reached (group 1, marked `next-release` by Release 2's retro planning; it keeps its mark).
- #10 Farewell command: the size was reached (group 2, first planned feature: no feature depends on another, so the Milestone's order stands; a Spec with Tickets #11 and #12).
- #20 Quiet flag: the size was reached (group 2, second planned feature, by the Milestone's order).

## Checked against main

Main at `08a1007`.

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
