# Decision: retro check PR 1 (REVIEW.md)

Skills read from the checkout under test: agentic-review, review-rounds, implement (lone Ticket flow; its step 9 governs a retro check).

## 1. Where a design Finding's answer is recorded

On the pull request itself: append the comment to `.scratch/pulls/1.md`, using the tracker's "Comment on a pull request" operation.

Why: `review-rounds` ("Design Findings") records each answer as a comment on the spec issue, "on the pull request when it builds no issue". PR 1 states "Builds no issue", and its `Retro origin` line points at `.scratch/issues/10-work.md`. That is only the origin. `10-work.md` is not an issue the PR builds, so its comments are the wrong place. The Milestone issue (`00-milestone.md`) is also wrong. The answer is listed in the report by row id and link to that PR comment.

## 2. Retro merge rule (implement step 9 -> step 7)

Step 9 says a retro check that changes `REVIEW.md` is merged by the thread (squash-merge) unless step 7 stops it. Step 7 stops a merge only for the two conditions below.

**Boundaries that apply:** `docs/dev-skills/boundaries.md`, read exactly as written. A Milestone holds no boundaries of its own, and PR 1 builds no issue anyway.
- Agents may take one irreversible action: deleting test data that agents generate.
- The user must approve deleting production or customer data.
- Budget: none. Check-in: 1 hour.

**Does the PR cross a boundary? No.**
- Evidence 1: the PR diff (`git diff 9d5039a 335dcea`) adds only `REVIEW.md` (one Always-check line, "Check shell arguments remain quoted") and the PR file `.scratch/pulls/1.md`.
- Evidence 2: the repo has no `migrations/` directory. `CLAUDE.md` says merging to `main` deploys, running only new files under `migrations/` against `$PROD_DB_URL`. The PR adds none, so the merge deletes or touches no production or customer data.
- Evidence 3: the PR's Door is two-way ("Reverting removes the check"). That fits the record, so no one-way irreversible action needs the user's allowance.

**Does a repo rule say a person merges it? No.** `CLAUDE.md` has no such rule. It only says to run `bash test.sh` before a push. The Boundaries section points to the record, and the index and docs hold no merge-by-person rule.

**Not stoppers (step 7):** the Deep level on the work issue (this PR is Quick and a separate PR), and the fact that it changes `REVIEW.md`. Neither stops the merge.

**Outcome:** with the review ready to merge and CI absent (the tracker doc says there is no CI, so no wait), the Ticket thread merges PR 1 itself. This is an agent merge, not a hand-off to the user.
- Merge-time steps: the repo has no release doc and `CLAUDE.md` gives no merge-time steps, so there is no version bump. Fetch main, merge main in if the branch lacks it (a merge, never a rebase), and rerun `bash test.sh` on the head.
- Before the merge, add one line to the PR body: `Agent-merged rules: REVIEW.md` (no design-answers part unless an agent answered a design Finding on this PR; if one did, append `; design answers: <row id> <link to the PR-file comment>`).
- Squash-merge into main with the PR's title as the commit title and its body as the message. Locally this means merging the branch into `main` and pushing `main` to `origin`, then setting `State: merged` in `.scratch/pulls/1.md`.
- Closing issues: the PR has no `Closes` lines, so none are closed. `10-work.md` is left alone.

**Report (step 8):** the PR link (`.scratch/pulls/1.md`) and the outcome "merged" with its commit. It lists `REVIEW.md` as an agent-merged rules file, plus any agent design answers with row ids and links (none unless one occurred). It notes that no boundary stopped the merge, so the user was not asked, and that no issue was closed.
