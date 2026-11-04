# Release thread report (2026-11-04)

**Where it started:** no open release issue and no stray release label; the last release issue, #2 (Release 2), is closed with its notes and both end-of-Release records (triage, retro-planning). So this run went straight to step 5 and planned the next Release. Main at `cdcf698`.

## Release 3 planned (dry run: see `.scratch/proposed-actions.md`)

Release issue `51-release-3.md`, label `release-3` (new). Size 5, used 4. Goal: the greeter gains its quiet flag, and its usage text, empty-name greeting and unknown-command exit code are fixed.

Order:
1. #20 Quiet flag: the Milestone's only planned feature, no blockers.
2. #30 Typo in usage text: `ready-for-agent` bug, oldest (2026-09-01).
3. #31 Empty name prints `Hello, !`: carried over from Release 2; bug from 2026-09-15.
4. #33 Unknown command exits 0 from a pipe: `ready-for-agent` bug, carried over from Release 2.

Left out: none. No issue carried `next-release`; no severe issue; nothing parked.

## Check against main

Six open issues checked against `cdcf698` (#20, #30, #31, #32, #33, #50). All six are still valid; nothing closed or edited. I ran the check myself rather than in premium subagents (the skill wants subagents above 5 issues), because this thread has no tool to start them; with six one-file issues, each verdict was checked directly against `src/greet.sh` (and #31 and #33 by running the script).

## Proposed to you

- #50 Colour output: an unplanned feature. You removed it from Milestone 1's features on 2026-10-18, so it is not ranked even though Release 2's `## Carried over` lists it. Plan it with `milestone` if you want it back.

## Things to know

- **#31 still needs your decision**: greet `world`, or refuse an empty name? It is in Release 3 because Release 2 carried it over, but its builder will hit that open question. The skill makes a carried-over issue a candidate but gives no ranked group to one that is not `ready-for-agent`; I placed it with the bugs by age. If you would rather it wait, take its `release-3` label off, or mark it `ready-for-human`.
- **#32 Trailing space** is not in Release 3. Release 2's Notes say it was "carried to the next Release", but it is not under that issue's `## Carried over` section (the only place the skill reads carry-overs from), and it is a plain `bug` with no `ready-for-agent`, so it is not a candidate. Triage it to `ready-for-agent` or mark it `next-release` if it should ship next.
- **#34 Names with accents** is listed under Release 2's `## Carried over` but is closed as completed with no merged pull request closing it. Since it is closed, it is not a candidate.
