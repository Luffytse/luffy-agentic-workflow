### 1. Create a label
Issue: none
Label: release-3

### 2. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 3. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 22-name-file.md
Add: release-3
Remove: none

### 5. Create an issue
Issue: new (31-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet, shout and read-names-from-a-file options.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Cap:** 3 features (the release doc's Release size). Used: 3. Maintenance fixes: 0, outside the cap.

## Scope

- **Quiet flag**: first in the Milestone's order; adds the first of the commands the Milestone rounds out.
  - #20 Quiet flag
- **Shout flag**: second in the Milestone's order; adds the next greeting option toward the Milestone's goal.
  - #21 Shout flag
- **Read names from a file**: third in the Milestone's order; lets the greeter take its names from a file.
  - #22 Read names from a file

## Maintenance fixes

None listed: the Triage batch and Release-end Retro planning records for Release 2 (#2) were not found (no `## Triage batch` comment on #2, no closed Retro planning record created after #2), so maintenance fixes were not read for this planning.

## Left out

- #23 Repeat flag: fourth in the Milestone's order; does not fit the cap of 3 and waits for the next Release.
- #30 Typo in usage text: not a planned feature of Milestone #1 and not a maintenance fix chosen by a Triage batch or Retro planning; proposed to the user.

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.

Planned by the Release thread from the Milestone issue's order, without waiting for the user.
~~~
