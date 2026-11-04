# ma-retro-inside-spec

## 1. Where a design-Finding answer is recorded

On pull request 1 itself: append the comment to `.scratch/pulls/1.md`. That is the tracker's "Comment on a pull request" operation.

Source: review-rounds, "Design Findings": "Record each answer as a comment on the spec issue ... (on the pull request when it builds no issue)."

PR 1 builds no issue. Its body says "Builds no issue", and its only issue reference is `Retro origin: .scratch/issues/10-work.md`. That line is an origin, not something the PR builds, so the Spec is not the record. `.scratch/issues/10-work.md`, its Tickets 11 and 12, and the Milestone are background. The PR is its own spec (review-rounds "Sources": a PR that references no issue is its own spec).

The answer is also listed in the Spec thread's report, by row id and link to that PR comment. It is a keep-the-design answer (row dismissed, `design kept: <link>`) or a change the owner makes in the next Round.

## 2. Retro merge rule (implement-spec step 10, plus `merging`)

Rule: a check that changes `REVIEW.md` is merged by the Spec thread unless `merging` brings it to the user. It is listed on the `Agent-merged rules:` line. The merge is a squash, with the check's own Implementer as committer, and the Retro origin issue stands in for a Ticket. It closes no issue.

Boundaries that apply: only the Boundary record `docs/dev-skills/boundaries.md`, read exactly as written. The Milestone issue holds none of its own. PR 1 carries no `milestone-1` label, and in any case the record applies the same inside or outside a Milestone.

Evidence that nothing is crossed:
- The record lists one irreversible action agents may take: delete test data that agents generate. It lists one action needing approval: delete production or customer data. The budget is none, and the check-in interval is 1 hour.
- PR 1 changes only `REVIEW.md` (a new Always-check line) and `.scratch/pulls/1.md`. Checked with `git diff main...retro-check --stat`: 2 files, 15 insertions. It adds nothing under `migrations/`. CLAUDE.md says merging deploys and runs new `migrations/` files on `$PROD_DB_URL`, so nothing runs against production.
- The PR states Door two-way ("Reverting removes the check"). `merging` only stops a one-way Door when the record does not allow its irreversible actions.
- No repo rule says a person merges it. CLAUDE.md and the docs say nothing of the kind. Under `merging`, a `REVIEW.md` change and a Deep review (the Spec's level, not this PR's) do not stop the merge.

Merge-time steps: the repo's docs give none. CLAUDE.md only asks to run `bash test.sh` before a push, and there is no `release.md`. So there is no version hand-out or bump. VERSION stays 0.3.0.

Ready: the review is assumed ready to merge, and CI is absent (no CI in this tracker). Before the merge: fetch main, sync it in if behind (a merge, not a rebase), and rerun `bash test.sh` on the head. The PR's own Review level is Quick. By agentic-review's defaults, adding an Always-check line changes what a rule does, so Standard would arguably fit. That does not change who merges.

Decision: yes, the Spec thread merges this REVIEW.md change itself and does not bring it to the user.

Steps:
1. Add the line `Agent-merged rules: REVIEW.md` to the PR body. There are no design answers unless a design Finding was answered, in which case add `; design answers: <id> <link>`.
2. Squash-merge into main. The committer is the check's Implementer. The title is the PR's typed title.
3. After the merge, confirm `State: merged` on the tracker. Close nothing, since the PR builds no issue and the Retro origin issue is not closed by it.

What it reports (to the user or coordinator, as implement-spec step 9 and 10 say):
- Merged: PR 1 ("Prevent repeated unquoted arguments"), with its merge commit.
- Changed files listed under `Agent-merged rules:` are `REVIEW.md`, plus any agent design answers on it.
- Bug Tickets from the review: none, unless any were created.
- The retro's outcome.
- Spec 10's tickets 11 and 12 and the Spec are unaffected by this PR.
