# Release thread report (2026-11-04 09:00 UTC, dry run)

This was a dry run, so nothing changed in git or the tracker. Every write I would make is recorded in `.scratch/proposed-actions.md`.

## Release 2: cut and closed
- **Shipped:** #10 Farewell command (PR 7) and #20 Quiet flag (PR 8). Both were closed by a closing keyword in a merged pull request into main.
- **Dropped, blocking or carried over:** none.
- **Changelog:** I would open PR 22, `docs(release): Release 2`, adding the entry `## Release 2 (2026-11-04)`.
  - It covers `Commits: e79583d..30bb03d.`.
  - It lists #10 and #20, and gives `Also merged: README usage (#9).`.
  - It names no versions, because the repo's versioning policy is "none" and the release doc lists no cut steps.
- **Check:** the whole-Release check, `bash test.sh`, passes.
- **Merge:** under the Boundary record, the agent merges PR 22 as a squash.
- **Close:** the entry is posted as the notes on release issue #2, and #2 is closed as completed.
- **End-of-Release pass:** I ran triage's Triage batch, then retro-planning's Release-end planning. Each has its record comment on #2.

## Release 3: planned
- **Release issue:** #23, label `release-3` (I would create the label).
- **Goal:** the greeter can shout, so Milestone 1's last planned command is built.
- **Size:** 5. Used: 1.
- **Order:**
  1. #21 Shout flag. It is the only planned feature of Milestone 1 still open, it has no blockers, and it completes the Milestone's goal.
- **Left out:** none.
- **Check against main:** #21 is still valid. `src/greet.sh` on main has no `-s` flag.
- **Questions for you:** none.
- **Unplanned features proposed:** none.

## Worth a look (no action taken)
- **#10 and #20 may not really be built.** They count as shipped by the release rule: each was closed by a merged pull request with a closing keyword. But `src/greet.sh` on main has no `bye` command and no `-q` flag, only `# bye` and `# quiet` comment lines, and `test.sh` tests only `hello`. Please check whether they were really built. If they were not, reopen them or file bugs so the next planning picks them up.
- **Numbering:** issues and pull requests share one number space here, so I gave the new pull request 22 and the new release issue 23.
