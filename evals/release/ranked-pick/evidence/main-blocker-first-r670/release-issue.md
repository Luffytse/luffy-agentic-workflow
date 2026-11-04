Title: Release 3

**Goal:** The greeter gains its farewell command and its quiet flag, with the flag parser fixed underneath it, completing Milestone 1's features.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 4.

## Order

1. #10 Farewell command: no other feature depends on it and #20 does not depend on it either; both move the goal equally, so the Milestone issue's order (feature 1) puts it first. A Spec, one item, standing for its Tickets #11 and #12.
2. #40 Flags after the name are dropped: a `ready-for-agent` bug placed in group 2 because it is the open blocker of the planned feature #20, which cannot work until the parser reads flags after the name.
3. #20 Quiet flag: feature 2 in the Milestone issue's order; it comes after its blocker #40.
4. #30 Typo in usage text: a `ready-for-agent` bug (group 3), filed 2026-09-01, the oldest open bug; the usage line says `helo` instead of `hello`.

## Left out

None.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
