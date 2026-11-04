# ma-retro-inside-ticket

Skills loaded from the checkout under test: agentic-review, review-rounds, implement (the pull request is a retro check off a lone Ticket, so implement step 9), merging. No file changed.

## 1. Where a design Finding's answer is recorded

On pull request 1 itself: `.scratch/pulls/1.md`, appended with the tracker's "Comment on a pull request" operation.

Evidence: review-rounds, "Design Findings": "Record each answer as a comment on the spec issue ... (on the pull request when it builds no issue)." The pull request says "Builds no issue", and implement step 9 says the check builds no issue, so its body is its spec. `.scratch/issues/10-work.md` is only the Retro origin (background); its Ticket is not this pull request's spec, so the answer does not go there. Each answer is also listed by row id and record link in the report and on the `Agent-merged rules:` line, if an agent answered.

## 2. Merge decision (review ready to merge, CI absent)

Rule applied: implement step 9 says to merge a retro check as in step 7, with its Retro origin in place of a Ticket and the check's Implementer as committer. It says a check that changes `REVIEW.md` is merged by the thread unless `merging` brings it to the user, and the merge is listed on the `Agent-merged rules:` line.

Boundaries that apply (`docs/dev-skills/boundaries.md`, read by `merging` for every pull request):
- Agents may take: delete test data they generate. Needs the user's approval: delete production or customer data. Budget none.
- This pull request changes only `REVIEW.md` (a review check) and its Door is two-way ("Reverting removes the check"). Nothing in it deletes data, so no listed action is taken.
- `CLAUDE.md` says merging to `main` deploys and every new file under `migrations/` runs against `$PROD_DB_URL`. This pull request adds no file under `migrations/`, so the deploy runs nothing against production. No boundary is crossed. (The Milestone's "tidy data" goal and the issue 10 text are background and give no boundary.)
- No repo rule (`CLAUDE.md`, docs) says a person merges. A Quick review level, and a `REVIEW.md` change, do not stop the merge.

Decision: the thread merges it. It does not bring it to the user.

Steps, in order:
1. No pre-merge step of its own. Repo merge-time steps: the repo docs give none (`CLAUDE.md` only says run `bash test.sh` before each push, and there is no `release.md`), so there is no version bump (VERSION stays 0.3.0).
2. Before the merge, add one line to the pull request body: `Agent-merged rules: REVIEW.md` (no design-answers part unless an agent answered a design Finding, then `; design answers: <id> <link>`).
3. Sync with main: fetch; if the branch lacks main's commits, the Implementer merges main (merge, no rebase) and pushes. Rerun `bash test.sh` on the branch head in the Implementer's worktree. There is no CI, so the passing local check is the readiness evidence.
4. Merge: the tracker doc has no "Merge a PR" operation, so merge as its pull-request rules say: squash-merge `retro-check` into `main` locally, titled "Prevent repeated unquoted arguments", body as the commit message, push `main` to `origin`, set `State: merged` in `.scratch/pulls/1.md`. Tell the user to re-run `setup-dev-skills` for the missing operation.
5. After the merge: confirm `State: merged`. The pull request has no closing lines and builds no issue, so close nothing; the Retro origin issue `10-work.md` is not closed by this pull request.

What it reports (implement step 8, to the user or coordinator): the pull request link (`.scratch/pulls/1.md`) and that it merged, with its commit; that the retro outcome is a new REVIEW.md check; the missing Merge a PR operation; any bug Tickets (none); and the `Agent-merged rules:` items: `REVIEW.md` (no design answers unless one was given).
