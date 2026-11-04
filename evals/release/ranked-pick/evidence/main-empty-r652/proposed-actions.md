# Proposed actions (dry run)

Release thread, 2026-11-04T09:00:00Z. "Find where you are": no open release issue; no open issue carries a release label; the last release issue, 02-release-2.md (Release 2), is closed and holds both end-of-Release records (triage, retro-planning). So steps 1-4 have nothing to do and this run is step 5: plan the next Release, for Milestone #1 (01-milestone-1.md, open). Main at `b5280c564fda29dc51c2c88d30ac9750ac9f97c5`.

### 1. Create an issue
Issue: new (51-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** Hello takes the quiet flag `-q`, once flags after the name are parsed, so the greeter's commands are rounded out.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 0.

## Order

None.

## Left out

- #20 Quiet flag: the Milestone's only planned feature, left out because its blocker #40 (Flags after the name are dropped) is at `ready-for-human`, not `ready-for-agent`, so an agent cannot take it; it waits on the user's decision on the flag syntax.

## Checked against main

Main at `b5280c5`.

- #20 Quiet flag: still valid
- #34 Names with accents come out mangled: cannot tell: the issue gives no name, input, locale or mangled output to reproduce; on main `src/greet.sh` echoes `$2` unchanged, and `greet.sh hello José` printed `Hello, José!` with its UTF-8 bytes intact, but without the reported case that does not show the report is fixed. Unchecked, not ranked.
- #40 Flags after the name are dropped: still valid
- #50 Colour output: still valid

## Proposed to the user

- #50 Colour output: an unplanned feature; the Milestone issue does not list it.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 2. Create a label
Issue: none
Label: release-3
