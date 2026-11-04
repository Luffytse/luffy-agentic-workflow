# Release thread report (2026-11-04 09:00 UTC)

## Where this run started

Main at `a09d5f0` (`docs(release): Release 1 (#6)`). Release 1 is cut (its changelog entry is on main). Open release
issue #2 (Release 2) lists an Order, but #21 Shout flag in that Order does not carry `release-2`: a planning that
stopped part way ("Find where you are", case 1). This run finished it through step 5's "Rerun first"; the Order
stands and nothing was ranked again.

## What this run did (proposed in `.scratch/proposed-actions.md`, dry run)

1. Checked against main the open issues with no release label (#21, #31; #20 already carries `release-2`; the
   Milestone issue #1 and release issue #2 are records, not checked). Both are **still valid**:
   - #21 Shout flag: `src/greet.sh` has no `-s` handling; `greet.sh hello -s Ada` prints `Hello, -s!`.
   - #31 Empty name: `greet.sh hello ''` still prints `Hello, !` (`${2-world}` keeps an empty argument).
2. Wrote the missing `## Checked against main` and `## Proposed to the user` (None.) sections into #2's body,
   keeping the rest of it word for word.
3. Applied `release-2` to #21.

No issue carries `next-release`, so no mark was removed. No unplanned feature was found, no issue is parked and
no question was raised by the check against main.

## Release 2 as planned

Size 5, used 3 (as the issue records). Order:
1. #20 Quiet flag: next in the Milestone's order (carries `release-2`).
2. #21 Shout flag: next in the Milestone's order (now gets `release-2`).
3. #31 Empty name prints `Hello, !`: listed in the Order, but see below.

Left out: none.

## Needs your attention

- **#31 is both in the Order and under `## Carried over` in #2**, with the line "the user chose to carry it over;
  its fix is not done". A carried-over issue is unlabelled on purpose, so this run did **not** apply `release-2`
  to #31, even though the Order lists it: re-labelling it would undo your carry-over. Because #31 is in the Order
  without the label, #2 will keep reading as a part-way planning on every rerun. Please say which you want:
  (a) #31 is in Release 2 (remove the Carried over line and label it), or (b) #31 is out (drop it from the Order,
  Used becomes 2, and it waits for the next planning as a carried-over candidate).
- **The Goal does not fit the Order.** #2's Goal is "Say goodbye and keep quiet", but no issue in the Order or the
  Milestone adds a goodbye; the Milestone's features are #20 Quiet and #21 Shout. The rerun leaves a stopped
  planning's text as it is, so the Goal is unchanged; consider "Add the quiet and shout flags."
- #31's Order reason says "next in the Milestone's order", but #31 is a `ready-for-agent` bug that Milestone #1
  does not list (group 3, oldest bug, filed 2026-09-15), not a planned feature.
