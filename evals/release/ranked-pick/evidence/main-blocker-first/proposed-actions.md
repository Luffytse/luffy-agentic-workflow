# Proposed actions (dry run): Release thread, 2026-11-04 09:00 UTC

### 1. Create a label
Issue: none
Label: release-3

### 2. Apply / remove labels
Issue: 10-farewell.md
Add: release-3
Remove: none

### 3. Apply / remove labels
Issue: 11-bye-code.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 12-bye-usage.md
Add: release-3
Remove: none

### 5. Create an issue
Issue: new (41-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter says goodbye: `greet.sh bye <name>` prints a farewell and the usage line lists it.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Cap:** 5 features. Used: 1. Maintenance fixes: 0, outside the cap.

## Scope

- **Farewell command**: first in Milestone #1's order and unblocked; it adds the `bye` command, rounding out the greeter's commands.
  - #10 Farewell command
  - #11 bye: the command
  - #12 bye: usage text

## Maintenance fixes

None. The Triage batch and the Release-end Retro planning results for Release 2 could not be read (no `## Triage batch` comment on #2, no closed Retro planning record created after #2), so maintenance fixes were left out of this planning.

## Left out

- #20 Quiet flag: second in Milestone #1's order, blocked by #40 (open).
- #40 Flags after the name are dropped: not listed in Milestone #1; proposed to the user as a planned feature, since it blocks #20.
- #30 Typo in usage text: not listed in Milestone #1 and not chosen as a maintenance fix.

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.

Planned by the Release thread from the Milestone issue's order, without waiting for the user.
~~~
