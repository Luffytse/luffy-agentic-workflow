# Release thread report (2026-11-04 09:00 UTC)

## No Release to cut

No Release is open: Release 2 (#2) is closed with its notes, no open issue is titled `Release <n>`, and no open issue carries a release label (`release-1`, `release-2`). There was nothing to cut, so the run went straight to Release planning.

Bump mode: the release doc names none, but it gives Release name, label and title forms (`Release <n>`, `release-<n>`), says the repo keeps no version, and names a whole-Release check, so the run used the named-Release (no version) forms. Please add an explicit bump mode line to `docs/dev-skills/release.md` if that is not what you mean.

## Release 3 planned (inside Milestone 1, #1)

Planned without waiting for you, from the Milestone issue's order (proposed actions 1 to 3 in `.scratch/proposed-actions.md`):

- Label `release-3` created; release issue `Release 3` opened (new #27).
- Goal: the greeter reads its output format and colour from a config file, the base the Milestone's colour and JSON output build on.
- Scope (cap 5, used 1): **#26 Config file loader**, third in the Milestone's order and the only planned feature that is unblocked.
- Left out: **#24 Colour output** and **#25 JSON output for scripts**, first and second in the Milestone's order, both blocked by #26, which is still open. A blocker counts as cleared only when it is closed or is a feature taken earlier in the same scope, and #26 comes after both in the Milestone's order, so neither qualified. The Milestone's order was not changed. Once #26 merges, both are unblocked for Release 4. If you would rather build all three in one Release, put #26 first in the Milestone issue's feature list; the next planning would then take #26, #24 and #25 together.
- Maintenance fixes: none. **Sources not read**: the Triage batch for Release 2 (#2 has no `## Triage batch` comment, only a note saying triage ran) and the Release-end Retro planning for Release 2 (no closed `retro-planning` issue created after #2). Release 2's maintenance fixes may therefore be missing; the next planning will not look again.
- No candidate outside the Milestone's list and nothing crossing a boundary, so nothing waits on you.

Issues filed from now on wait for the next Release planning, apart from Tickets split from a Spec in this Release.
