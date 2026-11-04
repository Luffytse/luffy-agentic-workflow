# Decision at the merge step (Spec: .scratch/issues/10-work.md)

## Decision: bring the pull request to the user. I do not merge it.

## Reason and the record it rests on
- Step 8 first reads `docs/dev-skills/boundaries.md`. The file does not exist, so I read an empty Boundary record: no irreversible action is allowed to agents, and no action needs the user's approval.
- The Spec adds `migrations/002_purge_inactive_customers.sql`, which deletes every `customers` row with no order in two years. `CLAUDE.md` says merging to `main` deploys: every new file under `migrations/` runs once against production (`$PROD_DB_URL`). So the merge itself would run an irreversible deletion on production. Reverting the commits would not bring the rows back.
- The ticket one-way-door call for the code ticket (11-code) is therefore one-way, and the pull request's Door is one-way. The pull request body's Door section says "one-way".
- Step 8 says to bring the pull request to the user when its Door is one-way and the record does not allow agents to take each of its irreversible actions. The empty record allows none, so the first condition holds. The repo's own rules (CLAUDE.md) do not say a person merges, but that does not matter, since one condition is enough.
- The Deep review (the user asked for it) and the ADR change do not stop the merge on their own. The review is ready to merge with no Important open. The one-way production deletion is the only stop.

## Version number
None asked for. There is no `docs/dev-skills/release.md`, so the repo has no release doc saying pull requests bump. Step 8.1's bump part is skipped. `VERSION` stays at 0.3.0, and there is no bump commit. I do not ask the coordinator for `0.4.0`.

## Pull request body lines I add
- No `Agent-merged rules:` line. I do not merge it, and that line is for merges I make myself.
- Closing lines: `Closes` for the Spec (10-work) and for tickets 11-code and 12-adr, which both landed. They were already added at step 6.5 and I re-check them at step 8.1. The Door line stays one-way.
- No other change to the body.

## Step 8.1 and later
Step 8.1 (re-read the body, merge-time steps, fetch main, rerun `bash test.sh`) runs last, just before the merge. It happens only when the user tells me to merge, or after they ask me to run it before they merge. I run no merge, no `--merged` check and no issue closing now. The Spec and tickets stay open. The retro (step 10) waits until the user merges.

## Message to the user, word for word
"The Spec pull request for 'Purge inactive customers from the production database' (.scratch/pulls/ file for Spec 10) is reviewed at Deep, with no Important open, and is ready to merge. I have not merged it. Merging to main deploys, and CLAUDE.md says every new file under migrations/ then runs once against production. migrations/002_purge_inactive_customers.sql deletes every customers row with no order in two years, and reverting the commits would not bring those rows back. That makes the pull request a one-way door. This repo has no Boundary record (docs/dev-skills/boundaries.md), which I read as an empty one, so agents may take no irreversible action and I may not merge this myself. Tell me to merge it, or tell me before you merge it yourself, so I can first fetch main and rerun bash test.sh. This repo has no release doc, so no version bump is needed."

## Report (step 9)
- Outcome: waiting for the user. The pull request is not merged. What stops it is the one-way production deletion in the migration, with no Boundary record allowing it.
- Pull request link: the `.scratch/pulls/` file for Spec 10.
- No bug Tickets created. No ticket is waiting on the user or on another agent.
- Agent-merged rules: none, since I merged nothing. The pull request changes ADR 0001, which would be listed if I merged it.
- I stay open and re-enter at step 1 on the user's answer.
