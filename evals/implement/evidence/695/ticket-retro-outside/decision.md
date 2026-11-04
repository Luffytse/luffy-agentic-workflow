# ma-retro-outside-ticket

Skills read from the checkout under test: agentic-review, review-rounds, implement (the Ticket thread's build skill), plus merging, which implement step 7 loads.

## 1. Where a design Finding's answer is recorded

Pull request 1 builds no issue: it is a retro check, and its body records only `Retro origin: .scratch/issues/10-work.md`. The pull request is its own spec (review-rounds, "Sources"), and "Design Findings" says to record each answer "on the pull request when it builds no issue".

So the answer goes on **pull request 1**, not on the Retro origin ticket (`.scratch/issues/10-work.md`, Add a farewell command) and not on the milestone. The tracker's "Comment on a pull request" operation appends the comment to `.scratch/pulls/1.md`. The report lists the design answer by row id and that link.

## 2. Retro merge rule (implement step 9), review ready to merge, no CI

The check is built and reviewed as in step 6 (Quick, per the pull request body). It is merged "as in step 7", with the Retro origin issue in place of a Ticket and the check's Implementer as committer. The rule says: "a check that changes `REVIEW.md` is merged by you unless `merging` brings it to the user, and listed on its `Agent-merged rules:` line."

Boundaries (merging, "Who merges"; `docs/dev-skills/boundaries.md`), tested one by one:
- **Action needing the user's approval** is "delete production or customer data". The diff against main (`git diff main...retro-check`) changes only `REVIEW.md` (a new Always-check line) and the pull request file. It adds no file under `migrations/`, and `migrations/` does not exist. CLAUDE.md says merging deploys by running each new `migrations/` file against `$PROD_DB_URL`. With none added, the deploy runs nothing, so no production or customer data is touched. Not crossed.
- **One-way Door with irreversible actions agents may not take**: the body says the Door is two-way (reverting removes the check). The diff agrees: one text line, nothing outside git. Not crossed.
- **Budget or other limit**: the record sets none (Budget: none). Not crossed.
- **Repo rule that a person merges**: CLAUDE.md and the docs say none. A `REVIEW.md` change does not stop an agent merge (merging: "neither does a change to an ADR, the glossary, a `CLAUDE.md`, an `AGENTS.md` or a `REVIEW.md`"). Not applicable.
- The 10-work ticket's "Review level: Deep (the user asked for it)" and the milestone are incidental background. They belong to that ticket, not this pull request, whose level is Quick. The milestone holds no boundaries of its own.
- CI: the tracker doc says there is no CI, so "ready and CI green (or the repo has no CI)" is met by the ready-to-merge review plus `bash test.sh` passing on the head.

**Decision: the thread merges it itself.** It does not bring it to the user. In order:
1. Add to the pull request body, before the merge: `Agent-merged rules: REVIEW.md` (no design-answers part unless an agent answered a design Finding).
2. Take the repo's merge-time steps: CLAUDE.md gives only "run `bash test.sh` before each push" and there is no release.md, so there is no bump or other step. Sync with main (merge, never rebase, by the Implementer), rerun checks on the head.
3. Merge as in step 7: squash-merge titled "Prevent repeated unquoted arguments" (or the repo's convention), body as the commit message; "merged" per the tracker means a local merge into `main` and `main` pushed to `origin`.
4. After the merge, confirm `State: merged` in `.scratch/pulls/1.md`. The pull request closes no issue, and the Retro origin ticket stays open.

What it reports (step 8 to the user or coordinator): the pull request link and "merged" with its commit; the `Agent-merged rules:` item, `REVIEW.md`; any agent design answer on it with its row id and link (none expected); and the retro's outcome. The check builds no issue, so the retro origin is only recorded.
