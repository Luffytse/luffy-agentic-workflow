### 1. Create an issue
Issue: new (46-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet and shout flags, and its known usage, name and test bugs are cleared.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #20 Quiet flag: planned feature 1 in the Milestone's order; nothing depends on either flag, so the Milestone's order breaks the tie.
2. #21 Shout flag: planned feature 2 in the Milestone's order. Note: merged pull request #8 (`-s` shouts the greeting) already appears to implement it without closing it; the builder checks main and closes it with evidence rather than rebuilding.
3. #30 Typo in usage text: ready-for-agent bug, oldest (2026-09-01). Note: merged pull request #7 fixed the usage line but does not close it; the builder checks main and closes it.
4. #31 Names with spaces are cut at the first space: ready-for-agent bug, second oldest (2026-09-05). Pull request #9 fixed `hello` only; `bye` still cuts the name.
5. #32 --version always prints 0.0.0: ready-for-agent bug, third oldest (2026-09-10). Note: merged pull request #10 dropped `--version`, so this is probably obsolete; the builder checks and closes it as not planned if so.

## Left out

- #33 test.sh does not test bye: the size (5) was reached; ready-for-agent bug, 2026-09-15.
- #34 greet sometimes fails: the size (5) was reached; ready-for-agent bug, 2026-09-20, and its report gives no steps to reproduce.

## Proposed to the user

- #45 Colour output: an unplanned feature; the Milestone issue does not list it (it is excluded as left to the next Milestone).

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 2. Create a label
Issue: n/a
Label: release-3

### 3. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 30-usage-typo.md
Add: release-3
Remove: none

### 6. Apply / remove labels
Issue: 31-name-spaces.md
Add: release-3
Remove: none

### 7. Apply / remove labels
Issue: 32-version-zero.md
Add: release-3
Remove: none
