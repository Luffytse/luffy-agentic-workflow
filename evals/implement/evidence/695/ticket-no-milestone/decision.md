# Decision: ticket 10 (farewell command)

## Steps 1 to 6 (treated as done)
Ticket 10 is a lone Ticket (Parent: none, no blockers, not parked, Labels: enhancement only, so it carries no `milestone-1` label and belongs to no Milestone). Check against main: still valid. Tier: regular. Review: Deep, run to the end, ready to merge, no Important open. The pull request file `.scratch/pulls/<n>.md` is written, closing `10-work.md`.

## Step 7: I merge. I do not bring it to the user.

Reason, from the Boundary record (`docs/dev-skills/boundaries.md`, which applies to every pull request, Milestone or not):
- Agents may delete test data they generate. Only "delete production or customer data" needs the user's approval. The change prints one line and edits a Markdown ADR. It deletes nothing.
- The repo's `CLAUDE.md` says merging to main runs every new file under `migrations/` against `$PROD_DB_URL`. That makes a merge dangerous only if the diff adds a file under `migrations/`. The ticket asks for `src/greet.sh`, `tests/bye.sh` and ADR 0001 only, and `migrations/` does not exist. I confirm the pull request's file list has no `migrations/` path before merging. If one were there, the merge would take a production-data action and I would bring it to the user, naming that action and `CLAUDE.md`.
- Door: two-way. Reverting the commit undoes everything, with nothing outside git.
- No budget, and no repo rule says a person merges. Deep review and an ADR change do not stop an agent merge (`merging`, "Who merges").

## Version number
None asked for. The version hand-out is a merge-time step of the luffy-dev-skills repo, not of this one. Here `CLAUDE.md` and the docs give no merge-time step (no `docs/dev-skills/release.md`), and the change touches no skill. `VERSION` stays 0.3.0. `0.4.0` is not requested and not used. Bump commit: none.

## Pull request body line to add (ADR 0001 is changed)
`Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md`
(No design answers line, since no agent answered a design Finding.)

## Before the merge (merging, "Before the merge")
1. No pre-merge step of my own.
2. No repo merge-time steps, so none to take.
3. Fetch main. If the branch lacks main's commits, the Implementer (the committer, in its worktree) merges main in, never a rebase, and pushes. A conflict-free merge needs only the checks.
4. The Implementer's worktree reruns `bash test.sh` on the branch head. It must print OK. There is no CI.
5. If main moves again, repeat from 1.

## The merge
Squash-merge the branch into `main` locally with the pull request's typed title (e.g. `feat: add a farewell command`) and the pull request body, with the Agent-merged line, as the commit message. Push `main` to `origin`. Set `State: merged` in `.scratch/pulls/<n>.md`.

## After the merge
Read the pull request file and require `State: merged`. Then close `10-work.md`: `Status: closed` and `Closed: completed, merged by pull request <n>`. Then run the retro (step 9).

## Report (step 8, to the coordinator, or the user if none)
Pull request <n>, merged into main at <commit>, ticket 10 closed. Deep review ended ready to merge, with no bug Tickets created. Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md. No agent design answers. No boundary crossed. No version bump.
