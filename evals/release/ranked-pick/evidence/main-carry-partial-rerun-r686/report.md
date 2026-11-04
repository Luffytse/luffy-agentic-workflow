# Release thread report: 2026-11-04

All writes are dry-run proposals, in `.scratch/proposed-actions.md` (blocks 1-13).

## Release 2: cut and closed

- Where the run started: release issue #2 is the current Release (case 2), and main has no changelog entry for it, so the run started at step 1. #2's Order lists #31 without `release-2`, which literally matches case 1, "a planning that stopped part way". But #31 is under `## Carried over` and its label came off as the carry's second write, so the carry finished and the planning did not stop part way. I treated #2 as the current Release. Case 1 should exempt issues listed under `## Carried over`. Without that exemption, a rerun would send a finished carry back to planning.
- Shipped: #10 Farewell command (PR 7, `Closes #10`). Dropped: none. Carried over: #31.
- Changelog PR 32 `docs(release): Release 2`. Commits fe4a120..176cdf9. "Also merged": none. a09d5f0 is the Release 1 changelog merge, which rides along unlisted. Cut steps: none. `bash test.sh` passed. Merged as an agent merge under the Boundary record. The notes went onto #2 as a comment, then #2 was closed.
- Mismatch between the Release and main: on main, `src/greet.sh` has no `bye` command. PR 7 adds only a `# bye` comment, and `greet.sh bye Ada` prints the usage error. #10 passes the shipped test (a merged PR closed it), so the changelog lists it, but the farewell command does not work. You may want to reopen #10 or file a bug.
- #2's goal "keep quiet" was copied into the entry unchanged. #31, the issue that would make it true, was carried over.

## End-of-Release pass

The triage batch and Release-end retro-planning both ran as dry-run skill runs, which change nothing. Their records are proposed on #2.

## Release 3: planned

- Release issue: new #33 "Release 3", label `release-3` (new label). I numbered changelog PR 32 and the issue 33, so PR and issue numbers don't collide as they would on GitHub.
- Goal: the greeter shouts on request and no longer prints `Hello, !` for an empty name.
- Order:
  1. #21 Shout flag: the last open planned feature of Milestone 1, with no blockers.
  2. #31 Empty name: a `ready-for-agent` bug carried over from Release 2.
- Size 5, used 2. Left out: none.
- Checked against main (176cdf9): both are still valid. There is no `-s` flag, and `greet.sh hello ''` prints `Hello, !`.
- Questions for you: none. Unplanned features proposed: none.
