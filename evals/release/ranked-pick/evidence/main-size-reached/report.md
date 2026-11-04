# Release thread report (2026-11-04)

## Cut

There was no current Release to cut. Release 2 (#2) is already cut and closed, its changelog entry is on main, and no open issue has a `Release <n>` title or carries a release label. I cut nothing and went straight to Release planning.

## Release 3 planned (inside Milestone #1)

I planned it from Milestone #1's feature order without waiting for you. The proposed tracker writes are in `.scratch/proposed-actions.md`: create label `release-3`, put it on #20, #21 and #22, and open release issue #31 `Release 3`.

- **Goal:** The greeter gains its quiet, shout and read-names-from-a-file options.
- **Scope (3 of 3):** #20 Quiet flag, #21 Shout flag, #22 Read names from a file. These are the first three planned features in the Milestone's order. All are open, unblocked and not parked.
- **Cap:** I used 3. `docs/dev-skills/release.md` sets a Release size of 3, which is lower than the skill's default cap of 5, so I kept to the repo's limit.
- **Maintenance fixes:** none.
- **Left out:**
  - #23 Repeat flag: it is fourth in the Milestone's order and does not fit the cap, so it waits for Release 4.
  - #30 Typo in usage text: see the question below.

## What was not read

I could not read the maintenance-fix sources for Release 2 (#2), so Release 3 may be missing some maintenance fixes:

- **Triage batch:** #2 has no `## Triage batch` comment. It only has an old `<!-- release end-of-Release pass -->` note saying triage ran.
- **Release-end Retro planning:** there is no closed `retro-planning` record created after #2. Again there is only the old note.

The next planning will not look at these again.

## Question for you

**#30 Typo in usage text** is an open `ready-for-agent` bug that Milestone #1 does not list, so I labelled nothing for it. Do you want it planned, for example as a maintenance fix in Release 3 or as a lone fix outside the Milestone?

## Notes

- `docs/dev-skills/release.md` names no bump mode and the repo keeps no version, so I followed its Release name line: name `Release 3`, label `release-3`, title `Release 3`. The plan has no version.
- Issues filed from now on wait for the next Release planning. The exception is Tickets split from a Spec in Release 3, which `to-tickets` gives the label.
- Nothing waits on a reply.
