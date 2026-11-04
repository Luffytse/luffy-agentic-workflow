### 1. Create an issue
Issue: new (27-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** Scripts can configure the greeter from a config file and parse its output as JSON, with colour output from the same config.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #26 Config file loader: moved up from third in the Milestone's order, because #24 and #25 both depend on it (their open blocker), so it must land first.
2. #25 JSON output for scripts: moves the Milestone's goal (usable from scripts) furthest, since it gives scripts parseable output; moved ahead of #24 for that reason.
3. #24 Colour output: depends on #26 like #25 but does less for scripts; last of the planned features.

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
