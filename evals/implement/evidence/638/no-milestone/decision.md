# Decision at the merge step: issue 10, "Add a farewell command"

## Decision: merge it myself (squash), do not bring it to the user

Reason and the records it rests on:
- Boundary record (`docs/dev-skills/boundaries.md`): agents may delete test data they generate; the user must approve deleting production or customer data. The PR adds `bye`, `tests/bye.sh` and an ADR 0001 edit. It adds nothing under `migrations/`, so the deploy-on-merge rule in `CLAUDE.md` (new migration files run against `$PROD_DB_URL`) has nothing to run and its merge takes no boundary action.
- Door: two-way. Reverting the commit undoes everything, with nothing outside git.
- Review level Deep alone does not stop a merge, and neither does the ADR edit. Review ended ready to merge, no Important open. There is no CI, and `bash test.sh` passes on the branch head.
- No repo rule says a person merges it. `CLAUDE.md` has only the deploy-on-merge note.
- The issue carries no `milestone-<n>` label (`Labels: enhancement`), so it is a lone Ticket outside Milestone 1. The Boundary record applies the same either way.

## Version: none asked, no bump commit
`docs/dev-skills/release.md` does not exist, and `CLAUDE.md` names no bump rule. With no release doc, step 7.1 says skip the bump and change nothing. I ask the coordinator for no number, so the `0.4.0` answer is not used. `VERSION` stays `0.3.0`, and the PR gets no bump commit.

## Merge-time steps (7.1)
`CLAUDE.md` gives no step to take before a merge, other than running `bash test.sh` before each push. I fetch main. If the Ticket branch lacks main's commits, the Implementer merges main in (a merge, never a rebase) and pushes. Then I rerun `bash test.sh` in the worktree on the branch head. If main moves again, I repeat this.

## Pull request body line I add (before the merge)
`Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`
No `design answers:` part, because no agent answered a design Finding. The body keeps its `Closes #10` line and `**Door:** two-way`.

## Merge (7.2 and 7.3)
- Squash-merge `feat/10-farewell` into `main` locally, with commit title `feat: add a farewell command` and the pull request body as the commit message. Push `main` to `origin`.
- Set `State: merged` in `.scratch/pulls/<n>.md`, then read it back. The merged check passes only when it says `State: merged`.
- Close issue 10 with the tracker's Close operation: `Status: closed` and `Closed: completed, merged by pull request <n> (squash commit <sha>)`.

## Report (step 8)
"Pull request <n> (`.scratch/pulls/<n>.md`) for issue 10 is merged into main as <sha>. Deep review ended ready to merge with no Important open. No version bump, because the repo has no release doc. Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md. No design answers, no bug Tickets created." After this I run the `retro` skill (step 9).
