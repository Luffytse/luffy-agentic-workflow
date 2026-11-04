# ma-no-milestone-spec: merge-step decision

## Decision: I merge it myself. Nothing is brought to the user.

Reason, from `merging` ("Who merges") and the repo's records:
- Boundary record (`docs/dev-skills/boundaries.md`): the only action needing the user's approval is deleting production or customer data. Agents may delete test data they generate. Budget none.
- The repo's CLAUDE.md says merging to main deploys, and every NEW file under `migrations/` runs once against `$PROD_DB_URL`. This Spec's diff (`src/greet.sh` bye command, `tests/bye.sh`, the ADR 0001 amendment) adds no file under `migrations/` (the directory does not exist), so the deploy touches no production data. I would confirm that with `git diff --name-only origin/main...HEAD` just before the merge; if a `migrations/` file ever appeared in the diff, that would cross the boundary and I would bring it to the user instead.
- Door: two-way. Reverting the commits undoes everything the change did, with nothing outside git (the tickets' one-way calls are "no").
- No repo rule says a person merges it. The Deep review level (the user asked for it) does not stop the merge, and neither does the ADR change. Review is ready to merge (no Important open). No CI in this repo.
- The Spec has Parent: none and no `milestone-<n>` label, so no Milestone rules apply. The Boundary record applies the same way to a pull request outside a Milestone.

## Version number: none asked
CLAUDE.md and the docs give no merge-time step and no release doc exists. The `VERSION` file (0.3.0) is not named by any rule, so there is no hand-out, no request to the coordinator, and no bump commit. I take only the steps the repo's docs give; they give none. (I do not ask for 0.4.0.)

## Before the merge (in order)
1. Closing-line reconcile (implement-spec's pre-merge step): re-read the PR body in `.scratch/pulls/<n>.md`. Keep `Closes` lines for the Spec (`.scratch/issues/10-work.md`) and the landed tickets `11-code.md` and `12-adr.md`; remove any line for a ticket that did not land. No absorbed sources.
2. Add this line to the PR body, since the PR changes an ADR:
   `Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`
   (no design answers, so no "design answers:" part).
3. Fetch main (`git fetch origin main`). If the Spec branch lacks main's commits, the Spec-branch Implementer merges main in (a merge, never a rebase) and pushes. I write no code.
4. Rerun `bash test.sh` on the branch head, expecting OK. If main moves again, repeat from step 1.

## The merge
Local merge into main as a merge commit (not a squash), titled with the PR's typed title (for example `feat: add a farewell command`), then push main to `origin`. Set the PR file to `State: merged`.

## After the merge
1. Confirm `State: merged` in the PR file and that main was pushed to origin.
2. Close the Spec `10-work.md` and tickets `11-code.md`, `12-adr.md` with `Status: closed` and `Closed: completed, <explanation naming the pull request>`.
3. Clean up worktrees and local Ticket branches, then run the `retro` skill.

## Report (to the user, since no coordinator runs)
Spec "Add a farewell command": merged to main as a merge commit; pull request `.scratch/pulls/<n>.md`; Spec and tickets 11 and 12 closed. No version bump (this repo's docs give none). Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md. No agent design answers, no bug Tickets.
