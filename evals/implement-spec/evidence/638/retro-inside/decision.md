# Decision: pull request 1 (retro check, REVIEW.md)

Skills read from the checkout under test: agentic-review, review-rounds, implement-spec (the retro origin, `.scratch/issues/10-work.md`, is a Spec, so implement-spec's step 10 is the build skill; implement's step 9 reads the same).

## 1. Where a design Finding's answer is recorded

review-rounds, "Design Findings": record each answer as a comment on the spec issue, "on the pull request when it builds no issue". Pull request 1 states "Builds no issue", and its body is its own spec (review-rounds "Sources": a pull request that references no issue is its own spec). The `Retro origin: .scratch/issues/10-work.md` line is provenance, not a built issue, so it does not make 10-work.md the spec.

Answer: it goes in a comment on pull request 1, appended to `.scratch/pulls/1.md` (issue-tracker.md: "Comment on a pull request: append the comment to its file"). Not on `10-work.md`, `11-code.md` or `12-adr.md`. The row is dismissed as `design kept: <link to that comment>`, or the change is fixed in the next Round. The link goes in the report to the caller.

## 2. Retro merge rule (implement-spec step 10, applying step 8)

Step 10: a check that changes `REVIEW.md` is merged by the thread itself (squash-merge, as a lone pull request off main) unless step 8 stops it, and it is listed on the `Agent-merged rules:` line.

Step 8 stops the merge only for these two causes. Neither applies.

1. Crosses a boundary. Boundary record (`docs/dev-skills/boundaries.md`):
   - Agents may take: delete test data that agents generate. Needs the user's approval: delete production or customer data. No budget. Check-in 1 hour.
   - Evidence: the diff `main...retro-check` adds only `REVIEW.md` and the pull request file `.scratch/pulls/1.md`.
   - It deletes no data, production or customer.
   - It adds no file under `migrations/`. CLAUDE.md says a merge to `main` deploys and runs each new `migrations/` file against `$PROD_DB_URL`. Nothing here triggers that, so the deploy hook does nothing.
   - Door is two-way ("Reverting removes the check"), so the one-way test, which needs an irreversible action the record does not allow, does not fire.
   - The Boundary record applies as written, Milestone or not. Milestone 1 holds no boundaries of its own.
2. Repo rule that a person merges. `CLAUDE.md`, `docs/dev-skills/` and `REVIEW.md` have no such rule. A `REVIEW.md` change does not by itself stop the merge, and neither does a Deep review. The pull request is Quick anyway.

The Spec's "Deep (the user asked for it)" is the Spec's own level. It does not carry to this separate check and would not stop a merge if it did.

Other preconditions:
- Review ready to merge, by assumption.
- CI absent: the tracker doc says "There is no CI", and step 8 allows merging when the repo has no CI.
- Merge-time steps: CLAUDE.md only says to run `bash test.sh` before each push. There is no `docs/dev-skills/release.md`, so no version bump (`VERSION` stays 0.3.0). The pull request changes nothing a bump covers.
- Fetch main. If it moved, merge it in. Rerun `bash test.sh`.

## Result

Yes, the thread merges this REVIEW.md change itself, with no user approval.

Steps:
1. Before the merge, add one line to the pull request body: `Agent-merged rules: REVIEW.md` (no design-answers part, unless a design Finding was answered, in which case add `; design answers: <id> <link>`).
2. Squash-merge `retro-check` into `main` locally, push `main` to origin, and set `State: merged` in `.scratch/pulls/1.md` (tracker doc: that is what "merged" means here).

Report to the user or coordinator:
- the pull request link (`.scratch/pulls/1.md`) and the outcome: merged by squash;
- `REVIEW.md` is the agent-merged rules file (the `Agent-merged rules:` item), and there were no ADR, glossary, `CLAUDE.md` or `AGENTS.md` changes;
- any design answers with their row ids and links (none unless made);
- the retro's outcome, namely this check built from the repeated unquoted-argument Bug class.
