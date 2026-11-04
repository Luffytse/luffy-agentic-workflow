# ma-retro-outside-spec answer

Skills read from the checkout under test: agentic-review, review-rounds, implement-spec (the work issue 10 is a Spec; step 10 holds the retro merge rule, implement step 9 is the lone-Ticket twin), and merging.

## 1. Where a design Finding's answer is recorded

On pull request 1 itself: append the comment to `.scratch/pulls/1.md`, using the tracker doc's "Comment on a pull request" operation.

Evidence: review-rounds "Design Findings" says to record each answer "on the spec issue ... (on the pull request when it builds no issue)". The pull request body says "Builds no issue", and review-rounds "Sources" says a pull request that references no issue is its own spec: its body. The `Retro origin: .scratch/issues/10-work.md` line only records where the retro came from. It is background, not a built issue, so the answer does not go on `10-work.md`. The agent lists the answer, by row id and link, in its report to its caller.

## 2. Retro merge rule (implement-spec step 10 / implement step 9, then merging)

The rule: the retro check is a lone branch off main with its own pull request, body recording `Retro origin: <issue>`, and it builds no issue, so its body is its spec. It is reviewed as in the build skill's review step and merged by loading `merging` (squash; the check's own Implementer as committer; the Retro origin issue in place of a Ticket, and it closes no issue). The rule adds: a check that changes `REVIEW.md` "is merged by you unless `merging` brings it to the user, and listed on its `Agent-merged rules:` line."

Which boundaries apply (merging "Who merges"): the Boundary record applies exactly as written to every pull request. It is the only source of boundaries. The pull request body's own "Door: two-way" is a claim, so I checked the diff.

- Approval-needed action: "delete production or customer data". The repo's CLAUDE.md says merging to main deploys every new file under `migrations/` against `$PROD_DB_URL`. `git diff --stat main...retro-check` shows only `.scratch/pulls/1.md` and `REVIEW.md`. There is no `migrations/` file and no `migrations/` directory on main (`git ls-files | grep -i migr` is empty). So the merge takes no production-data action.
- One-way Door with an irreversible action not allowed to agents: the Door is two-way (a new 5-line `REVIEW.md`; reverting removes it), and the diff confirms nothing outside git changes. Not crossed.
- Budget or limit: Budget is none; the 1 hour check-in interval is not a merge limit. Not crossed.
- Repo rule that a person merges: CLAUDE.md, the docs and the index state none. A change to `REVIEW.md`, and a Deep review (the Spec's, not this PR's), do not stop an agent merge by themselves (merging: "neither does a change to ... a REVIEW.md").

Result: no boundary is crossed, so the thread (the Spec thread, not the user) merges.

Steps once the review is ready and CI is absent (no CI exists; the checks are the readiness):
1. Pre-merge: sync with main, rerun `bash test.sh` on the head (no CI to wait for). The repo gives no other merge-time steps: no `release.md`, and no bump rule in CLAUDE.md, so `VERSION` (0.3.0) is left alone.
2. Before the merge, add this line to the pull request body: `Agent-merged rules: REVIEW.md` (no design-answers part unless an agent answered a design Finding on it; then append `; design answers: <id> <link>`).
3. Squash-merge with the check's Implementer as committer, using the typed title (e.g. `chore: ...` as `pr` writes it). The commit message is the body as it then stands.
4. After the merge: confirm `State: merged` on the tracker (`.scratch/pulls/1.md`), then close nothing, since it builds no issue and `10-work.md` is only the Retro origin and was already closed by the Spec merge.

What it reports (to the user or coordinator): the retro's outcome, the pull request link, that it merged (merge commit), and `Agent-merged rules: REVIEW.md` (plus any design answers by row id and record link). Note: the PR body says Review level: Quick; default sizing of agentic-review would call a rule change Standard, but a level the caller names wins, so this is a note and not a blocker.
