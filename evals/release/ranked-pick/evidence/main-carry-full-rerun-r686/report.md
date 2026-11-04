# Release thread report (2026-11-04, 09:00 UTC, dry run)

All tracker and pull request writes are in `.scratch/proposed-actions.md` (14 blocks). Nothing waits on a reply.

## Where the run started, and a reading you may want to check

#2 (Release 2) is open. None of its issues carries `release-2`: both issues in its Order, #10 and #31, are listed
under its `## Carried over` section and have lost the label. Read literally, the skill's case 1 ("an Order that
lists an issue that does not carry its label" is a planning that stopped part way) would send the run to "Rerun
first", which would put `release-2` back on #10 and #31 and undo the carry-over you chose. I read #2 instead as the
current Release with every item carried over: step 1 says a carried-over entry that has lost its label "counts as
carried, not as lost". So the run cut Release 2 and planned Release 3. Tell me if you meant otherwise. The skill
text could say this case outright (an Order entry listed under `## Carried over` is not a missing label).

## Release 2: cut (shipped nothing labelled)

- Shipped: none. Dropped: none. Carried over: #10 Farewell command, #31 Empty name prints `Hello, !`.
- Changelog entry `## Release 2 (2026-11-04)`, `Commits: fe4a120..e84452d.`, with `Also merged: README usage (#9).`
  The goal line is #2's, "Say goodbye and keep quiet.", as the skill takes it; note that Release 2 did not deliver it.
- Changelog PR 32 (`docs(release): Release 2`); whole-Release check `bash test.sh` passes (run on main locally: OK).
  Agent merge per the Boundary record. #2 is closed with the entry as its notes.
- End-of-Release pass: `triage` and `retro-planning` runs proposed with their records on #2 (in this dry run they
  change nothing).

## Release 3: planned (new release issue #33, label `release-3`)

Size 5, used 3. Order:

1. #10 Farewell command: planned feature, first in the Milestone's order; carried over from Release 2.
2. #21 Shout flag: planned feature, second; no dependency, so the Milestone's order breaks the tie.
3. #31 Empty name prints `Hello, !`: `ready-for-agent` bug, oldest open (2026-09-15); carried over from Release 2.

- Left out: none.
- Check against main (`e84452d`): #10, #21, #31 all still valid (no `bye` command, no `-s` flag; `greet.sh hello ''`
  still prints `Hello, !`). No questions raised; nothing unchecked.
- Proposed unplanned features: none. No `next-release` marks to remove; no parked issues.
