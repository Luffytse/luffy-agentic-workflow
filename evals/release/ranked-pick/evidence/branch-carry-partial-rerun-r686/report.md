# Release thread report (2026-11-04)

## Release 2: cut and closed (proposed, dry run)

- **Where the run started:** release issue #2 was open. #10 carries `release-2`. #31 is listed under `## Carried over` and has already lost the label, so the earlier carry-over finished both of its writes and #31 is accounted for. The changelog had no Release 2 entry, so the run started at step 1.
- **Shipped:** #10 Farewell command, closed by merged PR #7 (`Closes #10`).
- **Dropped:** none.
- **Carried over:** #31, already recorded. This run did not relabel it.
- **Changelog:** PR 8 `docs(release): Release 2` adds the entry `Commits: fe4a120..176cdf9.`. The whole-Release check `bash test.sh` passes (`OK`). The Boundary record lets agents merge it, so it is squash-merged. Its notes are posted on #2 and #2 is closed.
- **End-of-Release pass:** triage (Triage batch) and retro-planning (Release-end) both ran in dry run, and each has a record on #2.

## Please look: #10 may not really be done

#10 passes the shipped test (a merged PR closed it with `Closes #10`), so it is listed as shipped. But PR #7 only added a `# bye` comment line to `src/greet.sh`. On main, `bash src/greet.sh bye Ada` prints the usage text and exits 2. If you agree it is not done, reopen #10 or file a bug for it. Release 2's notes say the farewell command shipped. The triage brief names this too.

## Release 3: planned

- **Goal:** The greeter shouts on request and greets an empty name sensibly.
- **Label:** `release-3` (new). **Size:** 5, used 2.
- **Order:**
  1. #21 Shout flag: the Milestone's only open feature now that #10 has shipped; nothing blocks it.
  2. #31 Empty name prints `Hello, !`: carried over from Release 2; a `ready-for-agent` bug open since 2026-09-15 (group 3).
- **Left out:** none.
- **Check against main** (main at `176cdf9`): #21 is still valid (`greet.sh hello -s Ada` prints `Hello, -s!`). #31 is still valid (`greet.sh hello ''` prints `Hello, !`). No questions came up.
- **Proposed to you (unplanned features):** none.

Nothing waits on a reply. Every write is in `.scratch/proposed-actions.md`, blocks 1 to 14.
