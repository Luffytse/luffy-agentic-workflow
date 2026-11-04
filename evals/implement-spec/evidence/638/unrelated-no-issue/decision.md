# Decision: pull request 1 (retro check, REVIEW.md)

Skills read from the checkout under test: agentic-review, review-rounds, implement-spec (step 8 and step 10) and, for the lone-pull-request parts, implement (steps 7 and 9). The spec issue is `.scratch/issues/10-work.md` (Type: spec), so implement-spec is the build skill.

## 1. Where a design Finding's answer is recorded

On pull request 1 itself: appended to `.scratch/pulls/1.md`, using the tracker's "Comment on a pull request" operation.

Evidence: review-rounds, "Design Findings": "Record each answer as a comment on the spec issue with the tracker's 'Comment on an issue' operation (on the pull request when it builds no issue)." Pull request 1 says "Builds no issue." Its `Context: .scratch/issues/10-work.md` line is labelled "background reading only". It is not a Spec the pull request builds, so the answer is not recorded on `10-work.md`, `11-code.md` or `12-adr.md`. The Spec (the "Sources" section) is the pull request's own body, because it references no issue as something it builds. The answer is also listed in the report by row id and link, and on the `Agent-merged rules:` line if the agent answered it and merges.

## 2. Retro merge rule

Rule used: implement-spec step 10 (and implement step 9). A check that changes `REVIEW.md` "is merged by you (squash-merge, as a lone pull request off main) unless step 8 stops it, and listed on its `Agent-merged rules:` line." Step 8 and implement step 7 say a Deep review, or a change to an ADR, glossary, CLAUDE.md, AGENTS.md or REVIEW.md, does not by itself stop the merge.

Step 8 stops the merge only if (a) it crosses a boundary, or (b) the repo's own rules say a person merges it.

Boundaries that apply (`docs/dev-skills/boundaries.md`, applied exactly as written, Milestone or not):
- Irreversible actions agents may take: delete test data agents generate while implementing.
- Needs the user's approval: delete production or customer data.
- Budget none, check-in 1 hour, Milestone label `milestone-<n>`. These do not gate this merge.

Evidence on whether any boundary is crossed:
- `CLAUDE.md` says merging to `main` deploys, and every new file under `migrations/` runs once against production (`$PROD_DB_URL`). So the merge could take a production action. `git diff --stat main...retro-check` shows the pull request adds only `REVIEW.md` (+5 lines, one Always-check line) and `.scratch/pulls/1.md` (the pull request record). It adds no file under `migrations/`, and the repo has no `migrations/` directory. Nothing runs against production, and no production or customer data is deleted. The "needs approval" action is not taken.
- The Door is two-way ("Reverting removes the check"), which matches the diff: a text-only rules file. A two-way Door cannot trigger the one-way clause.
- (b): `CLAUDE.md`, the docs, and the tracker doc do not say a person merges pull requests.
- The Milestone's goal and the Spec's Deep level ("the user asked for it") belong to the Spec's own work, not to this pull request, which is Quick. The Spec's review level does not carry over.

CI is absent: the repo has no CI (tracker doc: "There is no CI"), which step 8 treats as met. The review is assumed ready to merge.

Merge-time steps just before the merge: neither `CLAUDE.md` nor a release doc (`docs/dev-skills/release.md` does not exist) sets any, and there is no version bump. Run `bash test.sh` on the branch head after fetching main, and merge main in if it moved.

## 3. Does the thread merge it, and what does it report

Yes. The thread merges pull request 1 itself, as a squash-merge (retro check, lone pull request off main) with the pull request's title ("Prevent repeated unquoted arguments") as the commit title and its body as the message, with no user approval needed.

Before the merge, add one line to the pull request body: `Agent-merged rules: REVIEW.md` (no design-answers part unless an agent answered a design Finding, in which case `; design answers: <id> <link>`).

The pull request should also record `Retro origin: <Spec issue link>` per step 10. It says only "Context ... background reading only", so note that gap, but it is not a reason to stop. The origin is background and the pull request builds no issue, so no issue is closed on merge, and the Spec and tickets are not touched by it.

Report to the user (or coordinator): the pull request link (`.scratch/pulls/1.md`, "merged" meaning branch `retro-check` merged into local `main` and `main` pushed to `origin`); outcome merged, with its commit; no boundary crossed (no `migrations/` file, so no production run); no bug Tickets created; and the Agent-merged rules list: `REVIEW.md`, plus any agent design answers on it. The retro's outcome is also reported.
