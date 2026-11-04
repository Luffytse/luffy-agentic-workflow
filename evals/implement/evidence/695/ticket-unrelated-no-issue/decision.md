# Decision: PR 1 "Prevent repeated unquoted arguments" (retro check, changes REVIEW.md)

Skills read from the checkout under test: implement (step 6, 7, 9), merging, review-rounds, agentic-review. Fixture read: tracker doc, boundaries.md, CLAUDE.md, REVIEW.md, 00-milestone.md, 10-work.md, .scratch/pulls/1.md, and `git diff 55dd723 0ab9917 --stat`.

## 1. Where an agent's answer to a design Finding is recorded

On the pull request itself: review-rounds "Design Findings" says to record each answer "on the spec issue ... (on the pull request when it builds no issue)". PR 1 says "Builds no issue", so there is no spec issue. With this tracker, "Comment on a pull request" means appending the comment to `.scratch/pulls/1.md`. The answer's link in the report and in the `Agent-merged rules:` line points to that comment.

`.scratch/issues/10-work.md` (Add a farewell command, Review level Deep) is only background: the PR does not close or build it, so nothing is recorded there. Its Deep level and its ADR 0001 amendment do not carry to PR 1.

## 2. Retro merge rule, assuming review ready to merge and CI absent

Rule: implement step 9, a retro check "is merged as in step 7, with its Retro origin issue in place of a Ticket (it closes none) ... a check that changes `REVIEW.md` is merged by you unless `merging` brings it to the user, and listed on its `Agent-merged rules:` line." The decision is then `merging`'s "Who merges".

Boundaries that apply, with evidence:
- boundaries.md, needs user approval: "delete production or customer data". CLAUDE.md says merging to main deploys, and every NEW file under `migrations/` runs once against `$PROD_DB_URL`. PR 1's diff (`git diff 55dd723 0ab9917 --stat`) is only `.scratch/pulls/1.md` and `REVIEW.md` (+5 lines, one Always-check line about quoted shell arguments). It adds no file under `migrations/`, so the merge deploys nothing that touches production data. That boundary exists in this repo but is not crossed.
- Irreversible actions agents may take: only "delete test data that agents generate", not used. The PR's Door is "two-way. Reverting removes the check", so the one-way-door clause does not trigger.
- Budget: none. Check-in interval of 1 hour is not a limit on this merge. No Milestone label: the PR carries no `milestone-1` and builds no Milestone issue (the Milestone has no boundaries of its own anyway).
- Repo rules saying a person merges: none in CLAUDE.md or docs. A REVIEW.md change explicitly does not stop an agent merge (merging "Who merges").
- Readiness: review ended ready to merge (assumed); no CI, which merging accepts ("or the repo has no CI").

## 3. Does the thread merge, and what it reports

Yes, the thread merges it itself; it does not bring it to the user.

Before the merge (merging "Before the merge"):
1. No caller pre-merge step.
2. Merge-time steps from the repo's own docs: CLAUDE.md gives only "run `bash test.sh` before each push"; there is no `docs/dev-skills/release.md`. No version bump (VERSION stays 0.3.0, as nothing asks for one). No hand-out.
3. Fetch main and, if it moved, have the Implementer (committer, in its worktree) merge main in, never rebase.
4. Rerun `bash test.sh` on the branch head in the Implementer's worktree. No CI to wait for.
5. Add to the PR body the line: `Agent-merged rules: REVIEW.md` (no design-answers part unless a design Finding was answered, in which case `; design answers: <row id> <link to the PR comment>`).

Merge: squash into main, titled "Prevent repeated unquoted arguments" (the PR's title; the repo sets no title convention), body as commit message, committed by the Implementer's worktree path. The tracker doc has no "Merge a PR" operation, so per merging it merges as the tracker's docs say (local merge of the branch into main, push main to origin, set `State: merged` in `.scratch/pulls/1.md`) and tells the user to re-run `setup-dev-skills`.

After the merge: confirm `State: merged` in `.scratch/pulls/1.md`. The PR has no closing lines and records no Retro origin line, so origin is none and no issue is closed. The Milestone and the Add a farewell command ticket stay open and untouched.

Report (implement step 8/9 to user or coordinator): the PR link (`.scratch/pulls/1.md`), merged with its commit, `Agent-merged rules: REVIEW.md`, any design answers with row id and link (none unless a design Finding was answered), no bug Tickets, and the retro outcome. Note for the record that the PR header says Review level Quick; Round 0 picks its own level (a changed Always-check rule is arguably Standard) and the report should state the level actually run.
