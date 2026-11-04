# Release thread report (2026-11-04T09:00:00Z, dry run)

All writes are proposed in `.scratch/proposed-actions.md`; nothing in the tracker or git was changed.

## Release 2: cut and closed

- Current Release: #2 (Release 2). Its two issues, #10 Farewell command and #31 Empty name prints `Hello, !`, were already carried over (listed under `## Carried over`, `release-2` removed). Shipped: none. Dropped: none.
- Changelog PR 32, `docs(release): Release 2`, commits `fe4a120..e84452d`: the entry says nothing shipped and lists "Also merged: README usage (#9)". Release 1's changelog merge (#6) rides along unlisted. Whole-Release check `bash test.sh`: OK. Merged by this thread (the Boundary record lets agents merge it), squash.
- #2 gets the entry as its notes and is closed.
- End-of-Release pass: `triage` (Triage batch) and `retro-planning` (Release-end) both ran for Release 2; records posted on #2.

## Release 3: planned (proposed issue #33, label `release-3`)

Goal: The greeter says goodbye, shouts on request, and no longer prints `Hello, !` for an empty name.

Size: 5. Used: 3.

Order:
1. #10 Farewell command: no dependency between the planned features, so the Milestone's order puts it first; carried over from Release 2.
2. #21 Shout flag: the Milestone's second feature; with #10 it completes the goal.
3. #31 Empty name prints `Hello, !`: carried over from Release 2; a `ready-for-agent` bug open since 2026-09-15.

Left out: none. Check against main (`e84452d`): #10, #21, #31 all still valid; no questions. Proposed to you: none. Nothing parked.

Notes: PR 32 and issue 33 take the next numbers free across issues and pull requests. Step 3 reads the entry from the merge proposed in action 4, since nothing merges in this dry run.
