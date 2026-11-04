# Decision: ma-no-record-twoway-spec

## Steps 1-7 (treated as done)
Spec 10 owned and checked against main (still valid). Tickets 11 (code + tests/bye.sh) and 12 (ADR 0001 amendment) landed on the Spec branch as squash commits. Spec PR `.scratch/pulls/<n>.md` is ready, Deep review ended ready to merge, no Important open.

## Step 8: I MERGE. I do not bring it to the user.

Reason, from `merging` "Who merges":
- Boundary record: `docs/dev-skills/boundaries.md` does not exist. With no record I read an empty one: no action needs the user's approval, no budget or limit, and no irreversible action is allowed to agents.
- Crossing a boundary needs (a) an action the record says needs approval (none listed), (b) a one-way Door whose irreversible actions the record does not allow, or (c) a budget breach (none). Only (b) could apply, so I checked the Door.
- Door is two-way. `CLAUDE.md` says merging to main deploys, but the only deploy effect is that new files under `migrations/` run once against `$PROD_DB_URL`. This PR adds no file under `migrations/` (it adds a `bye` command in `src/greet.sh`, `tests/bye.sh` and an ADR 0001 edit). Reverting the merge commit undoes everything the change did, nothing outside git included. Both tickets' one-way calls are "no", so the Spec PR Door is two-way. The deploy line is a warning for migration PRs, not a boundary here.
- Repo rules do not say a person merges it (`CLAUDE.md` has no such rule).
- A Deep review and an ADR change do not stop an agent merge (`merging`).
Therefore I merge.

## Version number
None asked. The repo has a `VERSION` file (0.3.0), but no repo doc gives a bump or any merge-time step: no `docs/dev-skills/release.md`, and `CLAUDE.md` names none. `merging` says "where they give none, there is none". So no request to the coordinator, no bump commit, and `VERSION` stays 0.3.0.

## Pre-merge ("Before the merge")
1. Closing-line reconcile (implement-spec's own pre-merge step), run first: body keeps `Closes` lines for the Spec (`.scratch/issues/10-work.md`) and the landed tickets 11 and 12; no other lines.
2. Repo merge-time steps: none.
3. Fetch main; merge it in via the Spec-branch Implementer if the branch lacks commits (I write no code), and push.
4. Rerun `bash test.sh` on the branch head in the Implementer's worktree (no CI exists). It must print OK.
5. If main moves again, repeat from 1.

## Pull request body line I add (before the merge)
`Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`
(No design answers on this PR, so no `design answers:` part. If the review did record an agent design answer, it is added as `; design answers: <id> <link>`.)
The body's final attribution lines from the system reminder also stay at the end:
`🤖 Generated with [Claude Code](https://claude.com/claude-code)` and the session link.

## The merge
Local merge commit, not a squash, into main, titled with the Spec PR's typed title (for example `feat: add a farewell command`), with `bye`'s tickets kept as their own commits. The Spec-branch Implementer makes any commit needed. Then push main to `origin`, and set `State: merged` in `.scratch/pulls/<n>.md`.

## After the merge
1. Confirm the merge: read `.scratch/pulls/<n>.md` shows `State: merged` and `origin/main` holds the merge commit.
2. Close with the tracker's Close operation (`Status: closed` plus `Closed: completed, merged by .scratch/pulls/<n>.md`): `10-work.md`, `11-code.md`, `12-adr.md`. No absorbed sources.
3. Step 9: remove worktrees and local ticket branches (all landed). Step 10: run `retro`.

## Report to the user/coordinator
"Spec 10 (Add a farewell command) is merged: merge commit `<sha>` on main, pushed to origin, from `.scratch/pulls/<n>.md`. Review was Deep and ended ready to merge with no open Important. No Boundary record exists (read as empty) and the change adds no migration, so the merge crosses no boundary and I merged it. Closed: 10, 11, 12. No version bump (the repo's docs give none; VERSION stays 0.3.0). Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md. No bug Tickets were created."
