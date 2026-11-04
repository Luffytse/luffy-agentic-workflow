# Release thread report (2026-11-04 09:00 UTC)

## No Release to cut

No Release is open: no open `Release <n>` issue, and no open issue carries a release label. Release 2 (#2) was cut and closed on 2026-10-16, and main has nothing new since its changelog entry apart from that entry's own changelog pull request. Nothing was cut in this run. The run went straight to Release planning.

## Release 3 planned (inside Milestone 1)

I planned it from the Milestone issue (#1) without waiting for you. The proposed writes are in `.scratch/proposed-actions.md`.

- **Name / label / issue:** Release 3, `release-3` (a new label), release issue `52-release-3.md`.
- **Goal:** The greeter can say goodbye and greet quietly, finishing the commands Milestone 1 plans.
- **Scope (cap 5, used 2):**
  1. Farewell command: Spec #10 with its Tickets #11 and #12. First in the Milestone's order, unblocked.
  2. Quiet flag: #20. Second in the order, unblocked.
- **Maintenance fixes:** none. Neither source could be read:
  - The Release 2 issue (#2) has no `## Triage batch` comment with rows. It has only a marker saying triage ran.
  - No closed `retro-planning` record created after #2 exists. #2 has only a marker saying retro-planning ran.

  So Release 2's maintenance fixes may be missing. The next planning will not look for them again.
- **Left out:**
  - #50 Colour output: the Milestone issue does not list it, and it is not a command. If you want it, add it to the Milestone with `milestone`.
  - #51 Run shellcheck in test.sh: it is `ready-for-human`, so it is not a candidate.
  - #30 Typo in usage text: see the question below.

Issues filed from now on wait for the next Release planning. The exception is Tickets split from a Spec in this Release, which `to-tickets` gives the label.

## One question for you

1. **#30 Typo in usage text** (a bug, `ready-for-agent`): should it be planned? The Milestone issue does not list it, and no Triage batch chose it as a maintenance fix. It is a one-word fix in the usage line, which #12 also edits. Nothing is labelled for it until you decide.

## Notes on the repo's docs

- The release doc names no bump mode, but its policy says the repo keeps no version, and its Release name line gives named forms (`Release <n>`, `release-<n>`). So I treated it as the "pull requests bump" mode with no versions: named Releases, a changelog pull request, and no `Versions:` line.
- Release 2's issue used `**Size:**` and `## Order` lines. The new release issue follows the skill's template (`**Cap:**` and `## Scope`).
