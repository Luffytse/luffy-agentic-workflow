# Decision: Ticket 10 "Add a farewell command" (Deep review, ready to merge)

## Merge or bring to the user: MERGE it myself

Step 7 of `implement` brings a pull request to the user only if it crosses a boundary or the repo's rules say a person merges it. Neither holds.

- Boundary record (`docs/dev-skills/boundaries.md`): the only action needing approval is "delete production or customer data". The pull request adds `greet.sh bye`, `tests/bye.sh`, and an ADR 0001 amendment. It adds no file under `migrations/`, so its merge deploys nothing that touches `$PROD_DB_URL`. (`CLAUDE.md` says merging to `main` runs new `migrations/` files against production; this pull request has none, and I would check the diff with `git diff --stat origin/main...HEAD` to confirm.)
- Door: reverting the commits undoes everything, with nothing outside git. It is a two-way door, so no irreversible action is in play.
- Repo rules: `CLAUDE.md` and the docs say no person must merge it.
- Deep review alone does not stop the merge, and neither does the ADR change. The review is ready to merge (no Important open), and the repo has no CI.

Record it rests on: `docs/dev-skills/boundaries.md` (empty of any matching approval action), `CLAUDE.md`, and the review's "ready to merge" end.

## Merge-time steps (step 7.1), in order

1. **Version number.** `docs/dev-skills/release.md` says pull requests bump and every pull request that changes a file under `src/` bumps. This one changes `src/greet.sh`, so it bumps. I ask the coordinator for the next version number just before the merge and wait. The coordinator answers `0.4.0` (main's `VERSION` is `0.3.0`, new feature, minor).
2. **Bump commit.** I have the same Implementer add it as the pull request's last commit: change `VERSION` to `0.4.0` (its only line, nothing else), commit as `chore(release): 0.4.0`, and push.
3. Fetch main. If the Ticket branch lacks commits from main, the Implementer merges main in (a merge, never a rebase) and pushes. If main's `VERSION` is still `0.3.0`, keep the bump commit and ask for no new number. If main's version changed, ask again, merge main in, take main's `VERSION`, and redo the bump as a new commit.
4. Rerun `bash test.sh` in the worktree on the branch head. There is no CI to wait for.

## Pull request body line to add (before the merge)

`Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`

(No design answers were given by an agent, so no `design answers:` part.) The pull request body also keeps `Closes` for the Ticket (`.scratch/issues/10-work.md`), its Evidence section, and its Door (two-way).

## The merge (step 7.2)

No forge, so locally: squash-merge the Ticket branch into `main` (`git merge --squash`), with the pull request's typed title (`feat: add a farewell command`) as the commit title and the pull request body, `Agent-merged rules:` line included, as the commit message. Push `main` to `origin`. Set `State: merged` in `.scratch/pulls/<n>.md`.

## After the merge (step 7.3)

Check the pull request file reads `State: merged` (the local form of `--jq .merged` printing `true`). Read the body's closing lines, then close `.scratch/issues/10-work.md` with the tracker's Close operation: `Status: closed` and `Closed: completed, merged by pull request <n>`. No absorbed sources are listed, so no `issue-absorption` recheck changes anything.

## Report (step 8)

To the coordinator or user: the pull request link (`.scratch/pulls/<n>.md`) and "merged, commit <sha>, version 0.4.0, Ticket 10 closed". Because I merged a rules change myself, I also list: ADR file changed `docs/dev-skills/adr/0001-greetings-go-to-stdout.md`; no glossary, `CLAUDE.md`, `AGENTS.md` or `REVIEW.md` change; no agent design answers; no bug Tickets created.

## Then (step 9)

Run the `retro` skill on this thread now that the pull request is merged and the issue is closed, and report its outcome.
