# Release thread report (2026-11-04)

## Nothing to cut

No release issue is open and no open issue carries a release label (`release-1`, `release-2` exist; `release-2` is only on #3, closed and shipped by PR #5). Release 2 was already cut and closed with its notes; the only commit since its end commit (9a18f55) is its own changelog pull request (b5280c5, #6). So there is no current Release to cut, and this run went straight to Release planning.

Note on the release doc: `docs/dev-skills/release.md` names no bump mode, but it keeps no version (Policy: none) and gives the Release name, label and title forms (`Release <n>`, `release-<n>`), so I used those named forms, as the existing Release 2 did.

## Release 3 planned (inside Milestone 1, without waiting for you)

- **Goal:** the greeter gains its quiet and shout flags, the two commands left in Milestone 1.
- **Name / label / release issue:** Release 3, `release-3` (new label), release issue #35 (proposed).
- **Scope (cap 5, used 2):**
  1. #20 Quiet flag: first in the Milestone's order.
  2. #21 Shout flag: second in the Milestone's order.
  Both are open, unblocked and not parked. These are all the planned features the Milestone issue lists, so the cap is not filled.
- **Maintenance fixes: none, and these sources were not read.** Release 2's release issue (#2) has only marker comments saying triage and retro-planning ran; it has no `## Triage batch` comment, and there is no closed `retro-planning` record created after #2. So the Triage batch and the Release-end Retro planning results for Release 2 were not readable, and Release 2's maintenance fixes may be missing. The next planning will not look again.
- **Left out:**
  - #30, #31, #32, #33 (ready-for-agent bugs): the Milestone issue does not list them and no Triage batch or Retro planning chose them as maintenance fixes, so nothing was labelled for them. See the questions below.
  - #34 (needs-triage): belongs to `triage`.

Issues filed from now on wait for the next Release planning, apart from Tickets split from a Spec in this Release.

## Questions for you (nothing waits on a reply)

Each of these is not listed in the Milestone issue. Say whether to plan it (into Milestone 1 / a Release) or not:

1. #30 Typo in usage text: plan it?
2. #31 Empty name prints a double space: plan it?
3. #32 Unknown command exits 0 from a pipe: plan it?
4. #33 Trailing space after the greeting: plan it?

The proposed tracker writes are in `.scratch/proposed-actions.md`.
