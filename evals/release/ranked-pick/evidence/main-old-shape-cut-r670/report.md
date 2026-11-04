# Release thread report, 2026-11-04

**Release 2 cut** (dry run: every write is in `.scratch/proposed-actions.md`).

- Release issue #2 was in the old shape (`## Scope`, no `## Order`); its label was on #10 and #20, so it was treated as the current Release with those two as its scope.
- Shipped: #10 Farewell command (PR #7), #20 Quiet flag (PR #8). Dropped: none. Also merged: README usage (#9, no issue).
- Changelog PR 10 `docs(release): Release 2`, commits 9a18f55..1c6fe96, whole-Release check `bash test.sh` passed; agent-merged under the Boundary record.
- #2 closed with the entry as its notes. End-of-Release pass: triage and retro-planning both ran (records on #2).

**Release 3 planned** (new release issue #22, label `release-3`, Milestone #1):

- Order: 1. #21 Shout flag: the last planned feature of Milestone #1, no blockers; it completes the Milestone's commands.
- Size: 5, used 1.
- Left out: none. Proposed to you (unplanned features): none.
- No issue carried `next-release`, so none was removed.

Nothing waits on a reply.
