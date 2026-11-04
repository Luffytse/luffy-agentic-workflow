Title: Release 3

**Goal:** The greeter reads a config file and prints JSON output that scripts can parse, with colour on top.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #26 Config file loader: planned feature that #24 and #25 both depend on (their `Blocked by:` names it), so it lands first; it has no blockers of its own.
2. #25 JSON output for scripts: planned feature that moves the Milestone's goal ("usable from scripts") furthest, so it comes before #24 although the Milestone issue lists #24 first; its only blocker, #26, is placed above.
3. #24 Colour output: planned feature that adds least to script use; its only blocker, #26, is placed above.

## Left out

None.

## Checked against main

Main at `b5280c5`.

- #26 Config file loader: still valid
- #25 JSON output for scripts: still valid
- #24 Colour output: still valid

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
