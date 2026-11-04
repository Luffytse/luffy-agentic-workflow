# Release thread report (2026-11-04 09:00 UTC)

## Cut: nothing to cut

No release issue is open (Release 2, #2, is closed with its notes) and no open issue carries a release label, so there was no current Release to cut. The thread went straight to Release planning, inside Milestone #1.

Bump mode: `docs/dev-skills/release.md` names no bump mode line, but it says the repo keeps no version and gives a Release name line (`Release <n>`, `release-<n>`) and a whole-Release check, so it was read as the named-Release ("pull requests bump") shape, with no versions. Consider adding an explicit bump-mode line to the release doc.

## Planned: Release 3 (label `release-3`, release issue to be opened as #41)

- **Goal:** The greeter says goodbye: `greet.sh bye <name>` prints a farewell and the usage line lists it.
- **Scope (cap 5, used 1):**
  - Farewell command: #10 (Spec), with its Tickets #11 and #12. First in Milestone #1's order, unblocked.
- **Maintenance fixes:** none, because neither source could be read (see below).
- **Left out:**
  - #20 Quiet flag: the Milestone's second feature, blocked by #40 (open). It was not taken, and no later feature was taken in its place.
  - #40 Flags after the name are dropped: not a planned feature (Milestone #1 does not list it).
  - #30 Typo in usage text: not listed in Milestone #1. Note: `src/greet.sh` already says `greet.sh hello`, so this issue may be stale; a matter for `triage`.

The proposed writes are in `.scratch/proposed-actions.md` (create label `release-3`, label #10, #11 and #12, open release issue `Release 3`).

## Sources not read

- Triage batch: release issue #2 (the last Release cut) has no `## Triage batch` comment, only an end-of-Release pass marker saying triage ran.
- Release-end Retro planning: no closed `retro-planning` issue created after #2 exists.

So Release 3's maintenance fixes may be missing. The next planning will not look again.

## Question for you (one)

Milestone #1 does not list #40 "Flags after the name are dropped". It blocks the Milestone's second feature, #20 Quiet flag, so until it is built #20 cannot join any Release. Do you want to add #40 to Milestone #1 as a planned feature, ahead of #20? Nothing is labelled for it until you decide.

## From now on

Issues filed from now on wait for the next Release planning, apart from Tickets split from the Farewell Spec (#10), which `to-tickets` gives the `release-3` label.
