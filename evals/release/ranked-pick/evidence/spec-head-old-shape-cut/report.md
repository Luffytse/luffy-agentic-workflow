# Release thread report (2026-11-04)

## Where I started

Open release issue #2 "Release 2" (label `release-2`, Milestone #1). It is written in an older format (`**Cap:**` and a `## Scope` section instead of `**Size:**` and `## Order`). I read its Scope as its Order: it lists #10 and #20, both carrying `release-2` and neither carrying `next-release`, so its planning finished and Release 2 is the current Release, not a planning that stopped part way. CHANGELOG.md on main had no `## Release 2` entry, so I started at step 1.

## Release 2: cut and closed

- Shipped: #10 Farewell command (PR #7, `Closes #10`), #20 Quiet flag (PR #8, `Fixes #20`), both merged into main. Dropped: none. Nothing blocked the cut.
- Changelog entry `## Release 2 (2026-11-04)`, Commits `9a18f55..1c6fe96`; also merged: README usage (#9), which no issue covers. The Release 1 changelog merge (#6) rides along unlisted. No "What to do" section: nothing here makes a user of the greeter act.
- Cut steps: none (release doc). Whole-Release check `bash test.sh`: passed.
- Changelog pull request (PR 10, `docs(release): Release 2`) opened and merged by the agent, as the Boundary record allows; main had not moved past 1c6fe96.
- Entry posted on #2 as its notes; #2 closed as completed.

## End-of-Release pass

`triage` (Triage batch) and `retro-planning` (Release-end) both ran for Release 2; each has its record on #2. In this dry run they changed nothing.

## Release 3: planned

Release issue #22 "Release 3", label `release-3` (label created), Milestone #1. Goal: the greeter shouts on request, the last command the Milestone plans.

- Order: 1. #21 Shout flag: the only planned feature still open, no blockers; it completes every feature the Milestone lists.
- Size: 5. Used: 1.
- Left out: none.
- Proposed to you: none (no unplanned features open).
- `release-3` applied to #21; no issue carried `next-release`.

Nothing waits on your reply. All writes are recorded as dry-run blocks in `.scratch/proposed-actions.md`.
