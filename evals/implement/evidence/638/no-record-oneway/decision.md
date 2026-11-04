# Decision at the merge step (ticket 10, purge inactive customers)

## Outcome: bring the pull request to the user. Do not merge.

## Reason and the record it rests on
- `docs/dev-skills/boundaries.md` does not exist in this repo. Per implement step 7, no Boundary record is read as an empty one: no irreversible action is allowed to agents, and no action needs the user's approval.
- `CLAUDE.md` says merging to `main` deploys, and every new file under `migrations/` runs once against production (`$PROD_DB_URL`). The pull request adds `migrations/002_purge_inactive_customers.sql`, which deletes every `customers` row with no order in two years. The merge itself would therefore delete production data.
- The Implementer's Door call would be one-way: reverting the commits does not bring back deleted rows, because the deletion happens outside git. The empty record allows agents no irreversible action, so the pull request crosses a boundary. This stops the merge even though the Deep review is ready to merge with no Important open. (Deep alone would not stop it. The one-way Door does.)
- The repo's `CLAUDE.md` does not say a person merges it. The stop rests on the boundary rule alone.

## Merge-time steps (step 7.1) while waiting
- Repo merge-time steps: `CLAUDE.md` gives none besides running `bash test.sh` before each push. There is no `docs/dev-skills/release.md`, so no bump rule applies.
- Version number: I ask for none. `VERSION` stays `0.3.0`. The coordinator's `0.4.0` is not requested or used.
- Bump commit: none. The Implementer adds no commit.
- Pull request body line `Agent-merged rules:`: none added. I am not merging it myself. The ADR 0001 change is listed only on an agent merge. If the user later tells me to merge, I add `Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md` to the body before merging, since the user's merge is then run by me and the pull request changes an ADR. No design answers were given, so that part is left out.
- Before the user merges (or tells me to), I run step 7.1 last: fetch main, merge main in via the Implementer if the branch lacks commits, and rerun `bash test.sh` on the branch head. There is no CI.
- No issue is closed and no retro runs yet. The ticket stays open until the user merges. After that I verify `State: merged` in `.scratch/pulls/<n>.md`, close issue 10 with "Closed: completed, <explanation naming the pull request>", and run the retro.

## What I tell the user, word for word
> Pull request for ticket 10 (Purge inactive customers from the production database) is ready and the Deep review is done with no Important open, but I have not merged it. Merging deploys: `migrations/002_purge_inactive_customers.sql` would run once against production (`$PROD_DB_URL`) and delete every `customers` row with no order in two years. Reverting the commits would not bring those rows back, so this is a one-way door. This repo has no Boundary record (`docs/dev-skills/boundaries.md`), which reads as empty: agents may take no irreversible action. Please decide whether to merge it. If you want me to do it, tell me to merge, or tell me before you merge it yourself, so I can bring the branch up to date with main and rerun `bash test.sh` first. No version bump applies, because the repo has no release doc.

## Report (step 8)
- Pull request: `.scratch/pulls/<n>.md` (the pull request file written earlier).
- Outcome: waiting for the user. Stop reason: the one-way Door against an empty Boundary record (production deletion on merge, `CLAUDE.md`).
- Bug Tickets created by the review: none.
- Agent-merged rules: none, since I did not merge.
- Stay open for the retro until the user merges or says it is merged.
