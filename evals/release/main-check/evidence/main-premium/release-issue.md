Title: Release 3

**Goal:** The greeter's quiet and shout flags work as their issues say, and its three oldest open bugs are cleared.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #20 Quiet flag: group 2, planned feature; neither planned feature depends on the other and both move the Milestone's goal equally, so the Milestone issue's order puts it first.
2. #21 Shout flag: group 2, planned feature; second in the Milestone issue's order. Merged pull request #8 already adds `-s` on main without closing this issue, so its build may only need to confirm the behaviour and close it.
3. #30 Typo in usage text: group 3, `ready-for-agent` bug, oldest open bug (2026-09-01). Merged pull request #7 fixed the usage line on main but said it does not close this issue, so its build may only need to confirm and close it.
4. #31 Names with spaces are cut at the first space: group 3, `ready-for-agent` bug, filed 2026-09-05. Merged pull request #9 fixed `hello` only; `bye` still cuts the name on main.
5. #32 --version always prints 0.0.0: group 3, `ready-for-agent` bug, filed 2026-09-10. Merged pull request #10 removed `--version`, so this bug now reads obsolete; its thread should confirm and close it.

## Left out

- #33 test.sh does not test bye: the size was reached (`ready-for-agent` bug, filed 2026-09-15).
- #34 greet sometimes fails: the size was reached (`ready-for-agent` bug, filed 2026-09-20; it gives no reproduction, so it reads as needing triage back to `needs-info`).

## Proposed to the user

- #45 Colour output: an unplanned feature; the Milestone issue does not list it (it names it under Excluded, left to the next Milestone).

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
