# Decision at the merge step: issue 10, purge inactive customers

Steps 1 to 6 are treated as done: check against main says still valid, review is Deep and ready to merge (no Important open), pull request file written under .scratch/pulls/.

## Decision: bring the pull request to the user. I do NOT merge.

Reason (merging, "Who merges"):
- No `docs/dev-skills/boundaries.md` exists, so I read an empty Boundary record: no irreversible action is allowed to agents.
- The Door is one-way. Merging deploys (repo CLAUDE.md: every new file under `migrations/` runs once against production `$PROD_DB_URL`), so `migrations/002_purge_inactive_customers.sql` deletes every customer with no order in two years from the production database. Reverting the commits would not restore the rows.
- A one-way Door whose irreversible action the record does not allow agents to take crosses a boundary. The empty record is the basis; a Deep review alone would not have stopped the merge, the irreversible production delete does.
- No repo rule says a person merges it; the boundary alone stops it.

## Version number
None asked. The change touches no file under `plugins/dev-skills/skills/` and this repo's docs give no merge-time step (no release doc, no bump rule in CLAUDE.md). The `VERSION` file (0.3.0) stays as on main. The coordinator's `0.4.0` is not requested and not used. No bump commit.

## Pull request body lines I add
- No `Agent-merged rules:` line: the pull request changes ADR 0001, an ADR, but I am not merging it myself, and no agent design answer exists. (If the user tells me to merge, I add `Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md` only if it counts as agent-merged; since the user merges, I leave it out.)
- Door section states: one-way, deletes production rows on merge, not undone by revert.
- Evidence section: `bash test.sh` output, the sqlite test (or its skip), what `purge.sh` prints.
- `Closes #10` line (issue 10).

## What I tell the user, word for word
"Pull request for issue 10 (Purge inactive customers) is ready: the Deep review ended with no Important open and `bash test.sh` passes. I have not merged it. Merging deploys and runs `migrations/002_purge_inactive_customers.sql` against production, deleting every customer with no order in two years. That cannot be undone by reverting the commits, and the repo has no Boundary record allowing me to take an irreversible action, so the merge is yours. Please take a backup or confirm the dry-run count from `src/purge.sh` first. Tell me before you merge so I can sync main and rerun the checks; once you have merged or tell me it is merged, I will confirm the merge on the tracker, close issue 10, and run the retro."

## Report (step 8)
Pull request link: `.scratch/pulls/<n>.md`. Outcome: waiting for the user. What stops it: boundary crossed, one-way production delete, empty Boundary record. No bug Tickets created. No Agent-merged rules line. Then stop; "After the merge" and the retro (step 9) run after the user merges.
