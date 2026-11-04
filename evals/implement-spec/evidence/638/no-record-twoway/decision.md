# Decision at the merge step (implement-spec step 8)

Decision: MERGE it myself. Do not bring it to the user.

## Reason and the record it rests on
- Boundary record: `docs/dev-skills/boundaries.md` does not exist, so I read an empty one: no irreversible action is allowed to agents, and no action needs the user's approval.
- Boundary test 1: the pull request takes no action that needs approval, because the empty record lists none. Its Door is two-way: the change is `greet.sh bye`, `tests/bye.sh` and an ADR 0001 amendment, and both tickets' one-way calls are "no" (reverting the commits undoes everything). It adds no file under `migrations/`, so the deploy-on-merge rule in `CLAUDE.md` (new migrations run once against `$PROD_DB_URL`) has nothing to run. If it had added one, the Door would be one-way and, with an empty record, I would bring it to the user.
- Boundary test 2: `CLAUDE.md` and the docs do not say a person merges. They only say merging to `main` deploys.
- Deep review (which the user asked for) and the ADR change do not stop a merge. The review is ready to merge with no Important open. There is no CI, so there is nothing to wait for. I rerun `bash test.sh` on the branch head before merging.

## Step 8.1, merge-time steps
- Pull request body: the Spec's own `Closes` line (`.scratch/issues/10-work.md`) and the lines for tickets 11 and 12 stay, because both landed. No other ticket lines, and no absorbed-source lines.
- Repo merge-time steps: `CLAUDE.md` gives only "run `bash test.sh` before each push", and I do that. There is no `docs/dev-skills/release.md`, so no bump applies.
- Version: no release doc says pull requests bump, so I ask nobody for a version number (the coordinator's `0.4.0` is not requested and not used). No bump commit is made, and `VERSION` stays `0.3.0`.
- Fetch `origin/main`. If it moved, merge it into the Spec branch (a merge, never a rebase) and push. Then rerun `bash test.sh`.
- Pull request body line I add before merging, because the pull request changes an ADR:
  `Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`
  There is no design-answers part, because no agent answered a design Finding.

## Step 8.2, merge
Merge locally into `main` with a merge commit (not a squash), with the Spec pull request's typed title as the commit subject, `feat: add a farewell command`. Push `main` to `origin`. Set `State: merged` in `.scratch/pulls/<n>.md`.

## Step 8.3, completion
Require the pull request file to read `State: merged` (the `--jq .merged` equivalent). Then close `.scratch/issues/10-work.md`, `11-code.md` and `12-adr.md`, each with `Status: closed` and `Closed: completed, merged by pull request .scratch/pulls/<n>.md`. Nothing was dropped or absorbed.

## Report (step 9)
"Spec 'Add a farewell command' (`.scratch/pulls/<n>.md`) is merged into main with a merge commit and pushed to origin. The review was Deep, with no Important open. No boundary stopped it: there is no Boundary record, so it is empty, the Door is two-way, and no migration is added. No version bump was needed, because there is no release doc. Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md. There are no design answers, no bug Tickets and no tickets waiting. Spec and tickets 11 and 12 are closed."

Then clean up worktrees and local Ticket branches, and run the `retro` skill (step 10).
