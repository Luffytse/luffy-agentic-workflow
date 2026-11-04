# Decision: pull request 1 (retro check, REVIEW.md)

Loaded from the checkout under test: agentic-review, review-rounds, implement-spec. The work issue `.scratch/issues/10-work.md` is `Type: spec`, so the build skill is implement-spec. Its step 10 ("Run the retro") is the retro merge rule. Nothing was launched and no file was changed.

## Facts read

- PR 1 (`.scratch/pulls/1.md`, head `retro-check`, base `main`) changes only `REVIEW.md` (adds "Check shell arguments remain quoted") and the PR file. It says "Builds no issue", "Retro origin: .scratch/issues/10-work.md", Door two-way, Review level Quick.
- Boundary record (`docs/dev-skills/boundaries.md`): agents may delete test data they generate; the user's approval is needed to delete production or customer data. Budget none.
- `CLAUDE.md`: merging to `main` deploys, and every new file under `migrations/` runs once against `$PROD_DB_URL`. It does not say a person merges. It asks for `bash test.sh` before each push.
- There is no CI and no release doc. `VERSION` is 0.3.0 and nothing says pull requests bump it.
- Issue 10 is the Spec (Review level Deep, "the user asked for it"). Issue 00 is the Milestone and holds no boundaries of its own. The PR does not carry the `milestone-1` label.

## 1. Where an agent's answer to a design Finding is recorded

On the pull request itself: append it as a comment to `.scratch/pulls/1.md`, using the tracker's "Comment on a pull request" operation.

Authority: review-rounds, "Design Findings": "Record each answer as a comment on the spec issue ... (on the pull request when it builds no issue)". The sources rule says a pull request that references no issue "is its own spec: its body".

PR 1 builds no issue, so it is its own spec. `.scratch/issues/10-work.md` is only the Retro origin, which is background context. The answer is not recorded there, and the Spec's Deep level does not carry over to this PR. The row's note would read `design kept: <link to that PR comment>`. A change answered in or after Round 3 becomes a bug Ticket.

## 2. Retro merge rule, assuming the review ready to merge and CI absent

Rule (implement-spec step 10, applying step 8): a check that changes `REVIEW.md` is merged by the thread (squash-merge, as a lone pull request off main) unless step 8 stops it, and is listed on its `Agent-merged rules:` line.

### Boundaries that apply (step 8 and the Boundary record)

Step 8 stops the merge only if one of these holds:

1. **It crosses a boundary.** No.
   - Evidence: the diff against `main` touches only `REVIEW.md` and `.scratch/pulls/1.md`. It adds nothing under `migrations/`, so the deploy-on-merge in `CLAUDE.md` runs no migration against production.
   - The PR deletes no production or customer data and takes no irreversible action.
   - The PR's Door is two-way: reverting the commit removes the check, and nothing outside git changed. So the one-way test does not apply, and no irreversible action needs allowing.
2. **The repo's own rules say a person merges it.** No. `CLAUDE.md`, the docs and the Boundary record say nothing of the kind.

Not stoppers, by step 8's text:
- A change to `REVIEW.md`.
- A Deep review. The Spec is Deep, but this PR is its own spec at Quick, and a Deep review would not stop it anyway.
- The Milestone: it holds no boundaries, and the Boundary record applies exactly as written.

The Boundary record's only approval-gated action is deleting production or customer data. This PR does not do it, so no boundary applies to this merge and the empty set of crossings is the evidence. The `CLAUDE.md` migrations deploy is the one thing that could have made it a boundary case, and it is not triggered.

### Does the thread merge it? Yes

Preconditions, all met:
- The review is ready to merge, as assumed.
- CI is absent, which step 8 treats as "or the repo has no CI". The checks still apply: `bash test.sh` must pass on the branch head.
- Before merging, re-read the PR body and fetch main. There is no release doc and no version-bump step, so `VERSION` stays as it is. If main moved, merge it in (never a rebase) and rerun `bash test.sh`.

Steps:
1. Before the merge, add the line `Agent-merged rules: REVIEW.md` to the PR body. Add `; design answers: <id> <link>` only if an agent answered a design Finding. None is assumed, so the design-answers part is left out.
2. Squash-merge into `main` as a lone PR. In this local tracker that means merging the branch into `main` locally and pushing `main` to `origin`. The PR file then reads `State: merged`.

### What it reports (step 9, and the retro's outcome to the user or coordinator)

- The PR link (`.scratch/pulls/1.md`) and the outcome: merged by the thread, squash-merged, with no boundary crossed and no person needed.
- The `Agent-merged rules:` item: `REVIEW.md`. No ADR, glossary, `CLAUDE.md` or `AGENTS.md` file changed, and there are no agent design answers.
- Any bug Tickets from the review: none are assumed.
- The retro's outcome: the repeated Bug class (unquoted shell arguments) now has an Always-check line in `REVIEW.md`.

Note: the Round 0 level was not re-sized here, as this is decision-only. The PR's own "Quick" label would be confirmed or raised (to Standard, since a new rule changes what a rule does) by Round 0. Neither level changes the merge decision.
