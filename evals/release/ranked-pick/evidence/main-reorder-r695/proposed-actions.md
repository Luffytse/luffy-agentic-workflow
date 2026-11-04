### 1. Create an issue
Issue: new (27-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** Scripts can read the greeter's output as JSON, with output format and colour set from a config file.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #26 Config file loader: the other two planned features (#24, #25) are blocked by it and need the config file it reads, so it comes first, ahead of its place (3) in the Milestone's order.
2. #25 JSON output for scripts: moves the Milestone's goal (usable from scripts) furthest, since it gives scripts output they can parse; its blocker #26 is placed above it.
3. #24 Colour output: helps scripts the least of the three; its blocker #26 is placed above it. Despite being first in the Milestone's order, it comes after #25 because the goal ranks above that order.

## Left out

None.

## Checked against main

Main at `d7170d7`.

- #24 Colour output: still valid
- #25 JSON output for scripts: still valid
- #26 Config file loader: still valid

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 2. Create a label
Issue: none
Label: release-3

### 3. Apply / remove labels
Issue: 26-config.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 25-json.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 24-colour.md
Add: release-3
Remove: none
