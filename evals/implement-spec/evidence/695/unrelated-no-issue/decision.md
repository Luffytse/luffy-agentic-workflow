# Decision: pull request 1 (retro check, REVIEW.md), builds no issue

Skills read from the checkout under test: agentic-review, review-rounds, implement (step 9 is the retro merge rule; implement-spec step 10 says the same), merging.

## 1. Where an agent's answer to a design Finding is recorded

On the pull request itself, as a comment on `.scratch/pulls/1.md`, made with the tracker doc's "Comment on a pull request" operation (append the comment to that file).

Evidence:
- review-rounds, "Design Findings": "Record each answer as a comment on the spec issue ... (on the pull request when it builds no issue)."
- `.scratch/pulls/1.md` says "Builds no issue." Its pull request body is its own spec (review-rounds, "Sources": "A pull request that references no issue is its own spec").
- `.scratch/issues/10-work.md` (the farewell Spec) is only an "Incidental issue reference ... background reading only". It is unrelated to this change, so the answer is not recorded there, and the "Review level: Deep" line in it does not apply to this pull request.

The answer is listed in the report to the caller by its row id and the link to that record. It is also named on the `Agent-merged rules:` line as `design answers: <id> <link>`.

## 2. Retro merge rule, review ready to merge, no CI

Rule applied: implement step 9 says the retro check's pull request is "merged by you unless `merging` brings it to the user, and listed on its `Agent-merged rules:` line". It is merged as in step 7. That means squash, the check's own Implementer as committer, and the Retro origin issue in place of a Ticket (it closes none).

Boundaries that apply, from `docs/dev-skills/boundaries.md` read through `merging` "Who merges":
- Action that needs the user's approval: "delete production or customer data". The pull request changes only `REVIEW.md` (plus its pull-request file). No file is added under `migrations/`, so the deploy-on-merge in `CLAUDE.md` (new files under `migrations/` run against `$PROD_DB_URL`) runs nothing. The merge does not delete production or customer data.
- Irreversible actions agents may take: delete test data agents generate. This pull request takes no irreversible action, so this is not needed.
- Door: the pull request declares two-way ("Reverting removes the check"), which is right. Reverting the commit undoes everything, and nothing lies outside git.
- Budget: none. Check-in interval: 1 hour. Neither is crossed or relevant.
- Repo rule that a person merges: none. `CLAUDE.md` says only to run `bash test.sh` before each push. No `AGENTS.md` and no release doc add a merge-time step.
- Result: it crosses no boundary. A `REVIEW.md` change does not stop the merge ("neither does a change to an ADR, the glossary, a CLAUDE.md, an AGENTS.md or a REVIEW.md"), and neither does a Deep review.
- Review level on the pull request is Quick, but Quick/Standard/Deep does not matter to this decision.

CI: the repo has none (the tracker doc says "There is no CI"). `merging` merges "once it is ready and CI is green (or the repo has no CI)". With no CI, the checks to rerun are the local ones: `bash test.sh` on the branch's head in the Implementer's worktree. That is the "Before the merge" step 4 check.

Before the merge: no pre-merge step of the caller's own. The repo has no merge-time steps (no version-bump or release doc rule; `VERSION` stays 0.3.0, since no version is handed out). Sync with main, merging main in (a merge, never a rebase) if the branch lacks commits, then rerun `bash test.sh`.

Decision: YES, the thread merges this REVIEW.md change itself and does not bring it to the user.

Steps, in order:
1. Before the merge, add this line to the pull request body: `Agent-merged rules: REVIEW.md; design answers: <id> <link>, ...`. Leave out the design-answers part if no agent answered a design Finding.
2. Squash-merge into main with the pull request's typed title (the repo has no other title convention) and the body as the commit message.
3. After the merge, read the pull request's merged state (`State: merged` in `.scratch/pulls/1.md`) before treating it as merged. It closes no issue: it has no closing lines and the Retro origin is not closed by it.

What it reports (implement step 8, and step 9's "Tell the user (or the coordinator) the retro's outcome"):
- The pull request link and outcome: merged, with its commit.
- The `Agent-merged rules:` items: `REVIEW.md` (the added Always-check line), and each agent design answer by row id and link, or none.
- No bug Tickets from the review, if the review ended clean.
- The retro's outcome for the repeated Bug class (unquoted shell arguments) that this check addresses.
