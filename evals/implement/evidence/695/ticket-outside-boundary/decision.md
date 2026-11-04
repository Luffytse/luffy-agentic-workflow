# Decision at the merge step: issue 10, purge inactive customers

## Decision: bring the pull request to the user. I do not merge it.

Step 7 loads `merging`. Its "Who merges" section reads the Boundary record in `docs/dev-skills/boundaries.md`.

- The record's only approval line is: "Actions that need the user's approval: delete production or customer data."
- The only irreversible action it allows agents is: "delete test data that agents generate while implementing."
- `CLAUDE.md` says "Merging to `main` deploys: every new file under `migrations/` runs once against the production database (`$PROD_DB_URL`)."
- The pull request adds `migrations/002_purge_inactive_customers.sql`, which deletes every `customers` row with no order in two years.
- So the merge itself would delete customer data in production. That is the action the record reserves for the user, and it crosses a boundary.
- The Door is one-way for the same reason: reverting the commits would not bring the deleted rows back, and no allowed irreversible action covers that deletion.
- The test against a throwaway SQLite file and the "Deep" review level do not change this. Deep alone never stops a merge, and the review being ready to merge (no Important open) is only the readiness input.
- The merge is the stop. I could not make the migration safe by editing the pull request. The migration is the thing the ticket asks for.

## Record it rests on

- `docs/dev-skills/boundaries.md`, the line "Actions that need the user's approval: delete production or customer data."
- `CLAUDE.md`, the deploy rule for `migrations/`.

## Version number: none asked for

- No version hand-out applies here. `CLAUDE.md` gives no merge-time steps, and there is no `docs/dev-skills/release.md`. `merging` says "Take only the steps those docs give: where they give none, there is none."
- I do not ask the coordinator for `0.4.0`.
- There is no bump commit. `VERSION` stays `0.3.0`.

## Pull request body lines I add

- I add no `Agent-merged rules:` line, because I am not merging it. The line is for changes I merge myself. When the user merges it, ADR 0001 is the one ADR file the change touches, and I will report it then.
- The body keeps `Closes #10` (the `Closes` line for the ticket), the Evidence section, and the Door. The Door states that the change is one-way, because the deploy deletes production customer rows, and that a revert would not restore them.
- I append a pull request comment (the tracker's "Comment on a pull request" operation) naming the stop: "Waiting on a boundary: merging deploys `migrations/002_purge_inactive_customers.sql`, which deletes production customer data. The Boundary record reserves that for the user."
- I do not set `State: merged`, run no local merge and push nothing to `origin/main`. I close no issue.

## What I tell the user, word for word

> Pull request for ticket 10 (Purge inactive customers) is ready: Deep review ended with no Important open, `bash test.sh` passes, and ADR 0001 records what `src/purge.sh` prints. I have not merged it. Merging deploys `migrations/002_purge_inactive_customers.sql` to production, and it deletes every row in `customers` with no order in two years. Your Boundary record says deleting production or customer data needs your approval, and a revert would not bring those rows back. Please decide: merge it yourself, or tell me to merge it. Either way, tell me first, so I can fetch main, merge it in if it has moved, and rerun the checks before the merge. After it is merged I will confirm it on the tracker, close ticket 10 and run the retro.

## Report (step 8)

- Pull request: `.scratch/pulls/<n>.md`, the file written before this step.
- Outcome: waiting for the user, because the merge crosses the Boundary record's "delete production or customer data". No commit, no bump and no bug Tickets.
- Ticket 10 stays open.
- Step 9 (the retro) waits. After the user merges or tells me to merge, I run "Before the merge", merge if told to, then run "After the merge" (confirm `State: merged`, close ticket 10), then the retro.
