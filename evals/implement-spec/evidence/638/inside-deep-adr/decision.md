# Decision: merge it myself (step 8 of implement-spec)

## Boundary and repo-rule check
- Boundary record (`docs/dev-skills/boundaries.md`): agents may delete self-generated test data; the user's approval is needed only to delete production or customer data. Nothing else is listed.
- CLAUDE.md says merging to main runs every new file under `migrations/` against production. This Spec adds `src/greet.sh` (bye command), `tests/bye.sh` and an ADR 0001 amendment. It adds no file under `migrations/`, so its merge takes no production action.
- Door is two-way: reverting the commits undoes everything, and neither ticket reported a one-way call.
- No repo rule says a person merges it. Deep review alone does not stop a merge, and neither does an ADR change.
- Review is ready to merge (no Important open), the repo has no CI, and `bash test.sh` is the check.

Decision: merge, do not bring it to the user. It rests on the Boundary record plus the pull request's file list (no `migrations/`, no one-way call), and on the absence of any person-merges rule in CLAUDE.md or docs.

## Merge steps, in order
1. Re-read the pull request body. Keep the Spec's own `Closes` line and the lines for tickets 11 and 12, which both landed. Remove any other line. No absorbed sources.
2. Merge-time steps in the repo docs (CLAUDE.md, `release.md`): bump mode is "pull requests bump", and the pull request changes `src/greet.sh`, so it bumps. No version number is known, so just before merging I ask the coordinator for it. The coordinator answers `0.4.0` (main is 0.3.0, a new command is a minor bump). I wait for the answer.
3. A new Implementer on the Spec branch (regular tier, briefed with the push check: `git status -sb` shows the Spec branch, then `git rev-parse origin/<branch>` equals `HEAD`) adds the bump as the pull request's last commit. It changes only the value in `VERSION` from `0.3.0` to `0.4.0` and commits `chore(release): 0.4.0`. I write no code myself.
4. Fetch main. If the Spec branch lacks main's commits, merge main in (never a rebase) and push. Rerun `bash test.sh` on the head. There is no CI. If main moves again, repeat; keep the bump commit and number if main's VERSION is still 0.3.0, otherwise ask for a new number and redo the bump as a new commit.
5. Add one line to the pull request body, before merging: `Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md` (no design-answers part unless the review had an agent design answer; if it did, append `; design answers: <id> <link>`).
6. Merge into main with a merge commit (not a squash), titled with the Spec pull request's typed title, e.g. `feat: add a farewell command`. Per the tracker doc, this is a local merge with `--no-ff`, then push main to `origin`, and set `State: merged` in the `.scratch/pulls/` file.
7. Require `State: merged` in the pull request file (the `--jq .merged` equivalent) to read true. Then use Close on the Spec (10) and tickets 11 and 12: `Status: closed` plus `Closed: completed, merged by pull request <n>`. Read each back. If any read or close fails, stop and tell the user.

## Report (step 9)
Remove leftover worktrees and local ticket branches. Tell the coordinator/user: pull request link, merged with its merge commit, version 0.4.0 bump commit `chore(release): 0.4.0`, Spec 10 and tickets 11, 12 closed, no bug Tickets, nothing waiting. Also list the ADR file changed: `docs/dev-skills/adr/0001-greetings-go-to-stdout.md` (no glossary, CLAUDE.md, AGENTS.md or REVIEW.md changes; no agent design answers unless the review had any). Then run the `retro` skill (step 10).
