# Decision: PR 1 (retro-check, REVIEW.md change)

Skills read from the checkout under test: agentic-review, review-rounds, implement (this is a lone retro check built by a Ticket thread, and the merge rule is implement step 7, with step 9 for the retro check).

## 1. Where an agent's answer to a design Finding is recorded

On pull request 1 itself, as a comment appended to `.scratch/pulls/1.md` (tracker doc: "Comment on a pull request: append the comment to its file").

Why: review-rounds, "Design Findings", says to record each answer "as a comment on the spec issue ... (on the pull request when it builds no issue)". PR 1 says "Builds no issue", and review-rounds "Sources" says a pull request that references no issue is its own spec: its body. `.scratch/issues/10-work.md` is only named as "background reading only" (an incidental reference), so it is not the spec and the answer does not go there. The milestone issue 00 is not the spec either. The answer's link (`design kept: <link>`) points at that comment in `.scratch/pulls/1.md`.

## 2. Retro merge rule, review ready to merge, CI absent

Rule: implement step 7 (applied to the retro check by step 9). Read the Boundary record first; it applies exactly as written, inside a Milestone or not. Issue 00's `milestone-1` label and issue 10 add no boundaries.

Boundaries that apply (`docs/dev-skills/boundaries.md`):
- Agents may take irreversible action: delete test data that agents generate while implementing.
- Needs the user's approval: delete production or customer data.
- Budget none; check-in 1 hour (not merge conditions).

Do they stop this merge? No.
- Crosses a boundary? No. Evidence: `git diff --stat main...retro-check` changes only `REVIEW.md` (adds one Always-check line, "Check shell arguments remain quoted.") and `.scratch/pulls/1.md`. `CLAUDE.md` says merging to main deploys only new files under `migrations/` to `$PROD_DB_URL`; there is no `migrations/` directory and the PR adds no file under it, so the merge deploys nothing and deletes no production or customer data. The PR's Door is two-way ("Reverting removes the check"), so no irreversible action is taken, and none beyond what the record lets agents do is needed.
- Repo rule that a person merges? No. `CLAUDE.md`, `docs/dev-skills/*` and `REVIEW.md` say nothing of the kind.
- Deep review, or a change to `REVIEW.md`, does not stop the merge (step 7 says so). PR 1 is Quick anyway (the Deep request belongs to issue 10, not this PR).
- The merge-time steps in step 7: no `docs/dev-skills/release.md` exists and `CLAUDE.md` names none, so there is no version bump (the `VERSION` file at 0.3.0 stays) and no number to ask for. CI is absent (tracker doc: "There is no CI"), which step 7 allows ("CI is green (or the repo has no CI)").

Result: the thread merges this REVIEW.md change itself and does not bring it to the user.

How:
1. Fetch main; merge main into the branch if it lags (via the Implementer, a merge not a rebase); rerun `bash test.sh` on the branch head.
2. Before the merge, add one line to the PR body: `Agent-merged rules: REVIEW.md` (no design-answers part unless an agent answered a design Finding, then `; design answers: <id> <link>`).
3. Squash-merge with the PR title "Prevent repeated unquoted arguments" (typed as `pr` says) and the PR body as message. In this local tracker, "merged" means main was updated locally and pushed to origin, then `State: merged` is set in `.scratch/pulls/1.md`; confirm that the file reads `State: merged` (the `--jq .merged` equivalent) before completing any issue. PR 1 closes no issue (it builds none), and issue 10 is not touched or closed.
4. Step 9: run the `retro` skill after the merge.

What it reports (step 8): the PR link (`.scratch/pulls/1.md`), outcome "merged" with its commit, no bug Tickets (unless the review made some), and the list of rule files it changed and merged itself: `REVIEW.md`, plus any agent design answers on it (by row id and link; none if none).
