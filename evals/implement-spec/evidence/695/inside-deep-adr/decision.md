# Decision at the merge step (Spec thread, 10-work.md)

Steps 1-7 treated as done: tickets 11 and 12 landed on the Spec branch, the Deep review ended ready to merge with no Important open, and the draft was marked ready as `.scratch/pulls/<n>.md` (Base main, Head the Spec branch, State open).

## Decision: I merge it. It does not go to the user.

Reason, from `merging` "Who merges", read against the Boundary record (`docs/dev-skills/boundaries.md`) and the repo rules (`CLAUDE.md`):
- The Boundary record says only "delete production or customer data" needs the user's approval. The change touches no file under `migrations/`, so the deploy-on-merge warning in `CLAUDE.md` (new migrations run against `$PROD_DB_URL`) is not triggered. It deletes no data. No budget is set, so no limit is passed.
- Door: two-way. Reverting the commits undoes everything, because nothing sits outside git. The record's one irreversible allowance (test data) is not used either, so no one-way action is left unallowed.
- No repo rule says a person merges it.
- Deep review and the ADR amendment do not stop an agent merge (`merging`: "A Deep review alone does not stop the merge, and neither does a change to an ADR").
- The repo has no CI, and the review ended ready to merge.

The record it rests on is `docs/dev-skills/boundaries.md`, with `CLAUDE.md` and `docs/dev-skills/release.md` checked.

## Before the merge (`merging` "Before the merge")

0. Spec thread's own pre-merge step (implement-spec step 8): re-read the PR body and reconcile the `Closes` lines. Keep the Spec line and the lines of the landed tickets 11 and 12 (both landed). Remove any other ticket's line. There are no absorbed sources. Lines: `Closes .scratch/issues/10-work.md`, `Closes .scratch/issues/11-code.md`, `Closes .scratch/issues/12-adr.md`.
1. Repo merge-time step, from `docs/dev-skills/release.md` ("pull requests bump"): the PR changes `src/greet.sh`, a file under `src/`, so it gets a version number and a bump.
   - I ask the coordinator for the next version number just before the merge and wait. The coordinator answers `0.4.0` (main is 0.3.0).
   - The Implementer on the Spec branch (I write no code) edits `VERSION` to `0.4.0`, changing only that value, and commits it as `chore(release): 0.4.0` as the PR's last commit. Before the push, `git status -sb` shows the Spec branch. It pushes and reports that `git rev-parse origin/<spec-branch>` equals `HEAD`.
   - `CHANGELOG.md` is not touched. A Release writes it, and the bump changes only the version value.
2. Sync with main: fetch `origin main`. If main has moved, the Implementer merges main in (a merge, never a rebase) and pushes. If main's version is unchanged, the bump commit and `0.4.0` stay, with no second bump. If main's version changed, I ask for a new number, the Implementer takes main's `VERSION` in the merge and redoes the bump as a new commit. A merge with conflicts is reviewed in the next Round. A merge without conflicts needs only the checks.
3. Rerun `bash test.sh` on the Spec branch head (in the Implementer's worktree). It must print `OK`, which includes `tests/bye.sh`. There is no CI to wait for.
4. If main moves again, repeat from the closing-line reconcile.

## Pull request body line added, before the merge

`Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`

There are no agent design answers, so there is no design-answers part. The PR changes no glossary, `CLAUDE.md`, `AGENTS.md` or `REVIEW.md` file.

## The merge

Local merge commit, not a squash, so main keeps each ticket as its own commit. The title is the PR's typed title: `feat: add a farewell command`. Run `git merge --no-ff` of the Spec branch into `origin/main` with that title, then push main to `origin`. Set `State: merged` in the `.scratch/pulls/<n>.md` file.

## After the merge (`merging`)

1. Confirm `State: merged` in the pull request file, and that main on `origin` holds the merge commit. If it does not read merged, close nothing and tell the user what the tracker shows.
2. Close the issues the body's closing lines list, each with the tracker's Close operation (set `Status: closed`, add `Closed: completed, merged by .scratch/pulls/<n>.md`): `10-work.md`, `11-code.md`, `12-adr.md`. The milestone issue `00-milestone.md` is not closed, since the PR does not close it.
3. Check that main's `VERSION` reads `0.4.0`. If it does not, tell the merging side to put it right.

Then step 9 (clean up the worktrees and local Ticket branches; the tickets landed, so none are kept) and step 10 (run `retro`).

## Report (step 9)

"Spec 10 'Add a farewell command' is merged: pull request `.scratch/pulls/<n>.md`, merge commit `feat: add a farewell command` on main, pushed to `origin`. VERSION is 0.4.0 (bump commit `chore(release): 0.4.0`). Issues 10, 11 and 12 are closed. The Deep review ended ready to merge with no Important open. No bug Tickets were created, and no ticket is waiting. Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md; no design answers."

## What I would tell the user

Nothing. The merge crosses no boundary, so no message goes to the user.
