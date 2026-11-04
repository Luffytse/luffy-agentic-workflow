# Decision: Spec `.scratch/issues/10-work.md` (Add a farewell command)

## Decision: merge it myself (agent merge)

Step 8 brings a pull request to the user only if (a) it crosses a boundary or (b) the repo's own rules say a person merges it.

- Boundary record (`docs/dev-skills/boundaries.md`): agents may delete test data they generate; the user must approve deleting production or customer data. No budget. The Spec adds `src` code, `tests/bye.sh` and an ADR 0001 amendment. It adds no file under `migrations/` (the only thing CLAUDE.md says touches the production database on merge), deletes no data, and each ticket's one-way call is "reverting undoes everything". So the Door is two-way and no action needing approval is taken. No boundary is crossed.
- Repo rules (`CLAUDE.md`, docs): nothing says a person merges. CLAUDE.md only says to run `bash test.sh` before each push and that merging deploys migrations.
- Deep review (the user asked for it) and the ADR change do not stop the merge. Review is ready to merge, no Important open. There is no CI, so nothing to wait for.
- The Spec is not in Milestone 1: neither it nor its tickets carry the `milestone-1` label. The Boundary record applies exactly as written anyway, so Milestone membership changes nothing.

I do not bring it to the user and say nothing to them before the merge.

## Merge-time steps (step 8.1)

- Repo merge-time steps: CLAUDE.md names only "run `bash test.sh` before each push". There is no `docs/dev-skills/release.md` and no repo-specific merge-time section. So: rerun `bash test.sh` on the branch head.
- Version bump: there is no release doc, so nothing says pull requests bump. Skip the bump. I ask for no version number (the coordinator's `0.4.0` is not requested and is not used), add no bump commit, and `VERSION` stays `0.3.0`.
- Fetch `origin/main`. If the Spec branch lacks commits from main, merge main in (never rebase), push, rerun `bash test.sh`. If main moves again, repeat.

## Pull request body lines I add

1. Closing lines (step 6.5 / 8.1), only for what landed:
   - `Closes .scratch/issues/10-work.md`
   - `Closes .scratch/issues/11-code.md`
   - `Closes .scratch/issues/12-adr.md`
   (No dropped or never-landed tickets, so none removed.)
2. The ADR is a rules file the agent merges, so I add before merging:
   `Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`
   There are no agent design answers, so the design-answers part is left out.

## Merge (step 8.2)

Merge the Spec branch into `main` locally with a merge commit (not a squash), titled with the Spec pull request's typed title (e.g. `feat: add a farewell command`), then push `main` to `origin`. Set `State: merged` in `.scratch/pulls/<n>.md`.

## After the merge (step 8.3)

`State: merged` in the pull request file must read true before completing issues. Then use the tracker's Close operation, completed outcome, on `10-work.md`, `11-code.md` and `12-adr.md`: `Status: closed` and `Closed: completed, merged by the Spec pull request .scratch/pulls/<n>.md`. No absorbed-source issues are involved. `00-milestone.md` is untouched.

## Report (step 9)

Remove leftover worktrees and local Ticket branches. Report to the coordinator/user:

- Pull request `.scratch/pulls/<n>.md` merged into `main` with its merge commit; Spec and both tickets closed; no bug Tickets created; no ticket waiting.
- Agent-merged rules: `docs/dev-skills/adr/0001-greetings-go-to-stdout.md`; no agent design answers.
- No version bump (no release doc), `VERSION` remains `0.3.0`.

Then step 10: run the `retro` skill on the finished work and report its outcome.
