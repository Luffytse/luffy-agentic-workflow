# Repeated Bug classes

A **Bug class** that comes up more than once in a pull request becomes a check, so later Reviews need not catch it again. The record is the Round and Ticket-check comments interpreted by `review-record`.

## Procedure

1. **Load the `review-record` skill by name**, then read every comment on the pull request, all pages (the tracker doc's **Read an issue** operation gives a pull request's comments, to the last page). Select the Round and Ticket-check comments that carry a Finding table by that contract (a Round 0 line at level None has none). None kept: say so, end this procedure, and go on to the next step of `retro`.
2. **Build the historical view** using `review-record`'s successive-comment interpretation and retrospective inclusion rules.
3. **Group the rows by Bug class.** Finders name classes in their own words: merge names that mean the same kind of problem, and say which you merged. A class's **instances** are its distinct locations across all its Findings. It is **repeated** when it has more than one instance, in one Finding or across Findings and Rounds.
4. **Look for a guardrail first**, for each repeated class: lint config, check or validate scripts, pre-commit hooks, CI workflows, `REVIEW.md`. A lint rule, check script, hook or CI job that covers the class and still missed it is the finding: repair, wire it up or clarify it instead of adding a second one. The same holds for an Always-check line in `REVIEW.md` that covers the class and still missed it: clarify that line rather than adding a near-duplicate in step 5. A prose rule (a `REVIEW.md` line) is no guardrail for a mechanical class, which always ends with a deterministic check (step 5).
5. **Otherwise classify** as the "Coding standards" category in [SKILL.md](SKILL.md) does:
   - **Mechanical**: a deterministic check, whichever of a rule in the repo's linter, a line in its check script, a pre-commit hook or a CI job is cheapest next to the existing guardrail.
   - **Judgement**: one line under "Always check" in `REVIEW.md` at the repo root, naming the Bug class, what to look for and the kinds of file it applies to (for example `src/**/*.ts`), in one sentence; name the kinds the class was found in, and none only when it fits every file. With no `REVIEW.md`, create it with three short sections (what Important means here, Skip, Always check): the Always-check line, and a sentence that the default meaning of Important applies, unless the user says otherwise.
6. **Run the new check on the current default branch.** If it fails anywhere on the default branch (Pre-existing places, or instances the reviewed pull request left unfixed), do not wire a failing check. Add those places to the open issue tracking that Bug class, or file one (as `review-rounds` files Pre-existing Findings), note there that the check lands with that fix, and use a `REVIEW.md` line meanwhile.
7. **Make the changes on a new branch off the default branch**, as one pull request for this retro (the reviewed pull request is done; leave it as it is). When adding or editing `REVIEW.md` or any doc, load `docs-index` and apply its contract. In a build thread, record its originating Ticket or Spec as `Retro origin: <issue link>` in the body, as the build skill instructs: its merge follows the build skill's one merge rule, and the check builds no issue, so its body is its spec. The pull request is reviewed like any other. One that adds or changes `REVIEW.md` changes the review rules, so in a build thread the thread merges it unless the build skill's merge rule stops it, listing it on the `Agent-merged rules:` line; a retro that runs outside a build thread leaves the merge to a person.
8. **Report a table**, one row per Bug class. Classes with one instance read "not repeated" and need no change.

| Bug class | Instances | Finding ids | What was done |
| --- | --- | --- | --- |
| Unchecked null from the API client (merged with "missing null guard") | 3 | R1-2, R2-1 | New lint rule in `eslint.config.js` |
| Error messages leak internals | 2 | R1-4 | `REVIEW.md` Always-check line |
| Unused exports | 4 | R1-5, R2-3 | Existing `knip` job fixed: it skipped `src/lib` |
| Hardcoded timezone | 2 | R2-2 | `REVIEW.md` line now; check lands with Pre-existing issue #<n> |
| Wrong default in config loader | 1 | R1-1 | Not repeated |
