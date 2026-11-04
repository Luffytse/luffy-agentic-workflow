# Decision: Spec .scratch/issues/10-work.md (purge inactive customers)

## Outcome: bring the pull request to the user. Do not merge.

### Reason
Step 8 of implement-spec stops the merge when the pull request crosses a boundary. It does here.

- `docs/dev-skills/boundaries.md` lists the actions that need the user's approval: "delete production or customer data". The only irreversible action agents may take is "delete test data that agents generate while implementing".
- `CLAUDE.md` says merging to `main` deploys, and that every new file under `migrations/` runs once against production (`$PROD_DB_URL`).
- `migrations/002_purge_inactive_customers.sql` deletes every `customers` row with no order in two years. Merging it would delete production customer data. That is a boundary action, not the agent-allowed test-data deletion.
- Its Door is one-way (a revert of the commits cannot restore deleted rows), and the record does not let agents take that action.
- The Deep review level is not a reason to stop. The ADR 0001 change is not one either. The boundary is the only reason.

The review state is "waiting on a boundary", not "ready to merge". No Finding is open.

### Version number
None asked. There is no `docs/dev-skills/release.md`, and `CLAUDE.md` has no bump rule. The skill's "bump where pull requests bump" part is skipped. `VERSION` stays `0.3.0` and there is no bump commit. I would not ask the coordinator for `0.4.0`.

### Merge-time steps
Step 8.1 runs last, just before the merge, and only once the user says to merge. At that point:
- Re-read the pull request body and keep the `Closes` lines for the spec and the landed tickets (11 and 12) only.
- There are no repo merge-time steps and no bump.
- Fetch main and merge it in if it moved.
- Rerun `bash test.sh`. There is no CI.
- Merge with a merge commit titled with the pull request's typed title.
- Check that the merge landed, then close 10, 11 and 12 as completed, naming the pull request.

### Pull request body lines I add now
- No `Agent-merged rules:` line. I am not merging, and no agent answered a design Finding. The ADR change would be listed there only if I merged it myself.
- `Door: one-way` (the migration deletes production data on deploy).
- `Closes` lines for the spec (`.scratch/issues/10-work.md`) and tickets 11 and 12.
- Each ticket's evidence in its Evidence section.

### Exact words to the user
> The Spec pull request for "Purge inactive customers from the production database" (`.scratch/pulls/` file for issue 10) has finished its Deep review with no Important Finding open. I have not merged it. It crosses a boundary in `docs/dev-skills/boundaries.md`: "delete production or customer data" needs your approval. `CLAUDE.md` says merging to `main` runs every new file under `migrations/` against production, so merging runs `migrations/002_purge_inactive_customers.sql`. That deletes every `customers` row with no order in two years, and the change cannot be undone by reverting the commits (one-way Door). Please merge it yourself or tell me to merge. If you will merge it yourself, tell me first so I can fetch main, rerun `bash test.sh` and check the body's `Closes` lines before you do. After the merge I will close the spec and its tickets.

### Report (step 9)
- Pull request: the Spec pull request file under `.scratch/pulls/`.
- Outcome: waiting on a boundary (production data deletion by `migrations/002_purge_inactive_customers.sql`, deployed on merge).
- Bug Tickets created: none. Tickets still waiting: none.
- Agent-merged rules: none, since nothing is merged by me.
- I stay open and re-enter at step 1 when the user answers. The retro (step 10) runs after the merge.
