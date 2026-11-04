### 1. Create an issue
Issue: new (27-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter reads its config file and prints JSON and coloured output from it, so scripts can use it.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #26 Config file loader: moved up from third in the Milestone's order, because #24 and #25 are both blocked by it.
2. #25 JSON output for scripts: moves the Milestone's goal (usable from scripts) furthest, since it gives scripts output they can parse; its blocker #26 is placed above.
3. #24 Colour output: the last planned feature; it does less for script use than #25; its blocker #26 is placed above.

## Left out

None.

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
