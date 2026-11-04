# Decision at the merge step: ticket 10 (farewell command)

Steps 1 to 6 are treated as done. The Deep review is ready to merge with no Important open, and the pull request file is under `.scratch/pulls/`. The diff holds `src/greet.sh` (the new `bye` command), `tests/bye.sh`, and the ADR 0001 amendment. It adds no file under `migrations/`.

## Decision: I merge it myself

I load `merging` and follow it. The reason and the record it rests on:

- **Boundary record** (`docs/dev-skills/boundaries.md`):
  - The only action that needs the user's approval is "delete production or customer data".
  - The pull request deletes nothing.
  - `CLAUDE.md` says that merging deploys and that every new file under `migrations/` runs once against `$PROD_DB_URL`. This pull request adds no migration, and `migrations/` does not exist. Merging it therefore runs nothing against production, and the Door is two-way: reverting the commit undoes everything.
  - Budget is none, so no limit is passed.
  - So it crosses no boundary.
- **Repo rules**: `CLAUDE.md` and the other docs say nothing about a person merging.
- **Deep review**: a Deep review alone does not stop the merge. Neither does an ADR change (`merging`, "Who merges").
- **Readiness**: the review is ready to merge, and there is no CI.

I do not bring it to the user, and I tell them nothing before the merge. If I had added a file under `migrations/`, I would stop and bring it to them, naming the boundary "delete production or customer data" and the deploy rule in `CLAUDE.md`. That does not apply here.

## Merge-time steps ("Before the merge")

1. **No pre-merge step of the Ticket thread's own.**
2. **Repo merge-time steps** (`docs/dev-skills/release.md`, "pull requests bump"):
   - The pull request changes `src/greet.sh`, so it gets a bump.
   - I ask the coordinator for the version number just before the merge, and wait. (A coordinator, not a user, because the doc says "the coordinator gives".)
   - The coordinator answers `0.4.0`.
   - I message the same Implementer, in its worktree, to commit the bump as the pull request's last commit. I write no code.
     - It changes only the value in `VERSION`, from `0.3.0` to `0.4.0`.
     - It commits as `chore(release): 0.4.0` and pushes.
     - It reports `git rev-parse origin/<branch>` equal to `HEAD`.
   - `CHANGELOG.md` is not touched: a Release writes it, and the doc asks for nothing else in a bump.
3. **Sync with main.** I fetch main.
   - If the branch lacks main's commits, the Implementer merges main in (a merge, never a rebase) and pushes.
   - If main's version is unchanged, I keep the bump and its number.
   - If it changed, I ask for a new number and the Implementer redoes the bump as a new commit after the merge, taking main's `VERSION`.
4. **Rerun `bash test.sh`** on the branch's head in the Implementer's worktree. It must print `OK`. There is no CI.
5. If main moves again, I repeat from step 1.

## Pull request body

I add one line before the merge:

`Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`

There are no design answers, so I leave out the design-answers part. The body already has `Closes #10`, in this tracker the `10-work.md` issue, and the Evidence and Door sections from `pr`.

## The merge

- I squash-merge locally into `main`, titled with the pull request's typed title (for example `feat: add a farewell command`).
- The commit message is the pull request body as it then stands.
- I push `main` to `origin`.
- I set the pull request file to `State: merged`.

## After the merge

1. I confirm the merge by reading `State: merged` in the pull request file, and that the commit is on `origin/main`.
2. I read the body's closing lines. For `.scratch/issues/10-work.md` I set `Status: closed` and add `Closed: completed, merged by pull request <n>`.
3. The Milestone issue stays open. Other issues may remain in it.
4. I check that `VERSION` on main reads `0.4.0`. If not, I tell the coordinator, who gives no further number until main is put right.

## Report (step 8)

I tell the coordinator, or the user when none runs:

- The pull request link (`.scratch/pulls/<n>.md`).
- Outcome: merged, with its commit, version 0.4.0.
- `Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`
- Bug Tickets created by the review: none.

Then I run the `retro` skill (step 9).
