# Repeated Bug classes

A **Bug class** that comes up more than once in a pull request becomes a check, so later Reviews need not catch it again. The record is the Round comments that `agentic-review` posts ([ROUNDS.md](../agentic-review/ROUNDS.md)).

## Procedure

1. **Read every comment** on the pull request, all pages (`gh api --paginate repos/<owner>/<repo>/issues/<n>/comments`, or the GitHub tool, to the last page). Keep those whose body starts `<!-- code-review kind=round` or `<!-- code-review kind=ticket-check`; a Spec's pull request counts its Ticket-check comments too. None kept: say so, end this procedure, and go on to the next step of `retro`.
2. **One row per Finding id**, across all kept comments. Severity and status come from the latest comment naming the id; Locations are the union of every location any comment listed for it. Leave out Findings the Verifier dropped (status `dismissed` with a Severity other than `Nit (skip)`, and a Note that does not say "user keeps the design"), because they were not real. Keep open, fixed, `Nit (skip)` and Pre-existing ones, and `dismissed` ones whose Note says "user keeps the design": those were real design questions.
3. **Group the rows by Bug class.** Finders name classes in their own words: merge names that mean the same kind of problem, and say which you merged. A class's **instances** are its distinct locations across all its Findings. It is **repeated** when it has more than one instance, in one Finding or across Findings and Rounds.
4. **Look for a guardrail first**, for each repeated class: lint config, check or validate scripts, pre-commit hooks, CI workflows, `REVIEW.md`, `CODING_STANDARDS.md`. A lint rule, check script, hook or CI job that covers the class and still missed it is the finding: repair, wire it up or clarify it instead of adding a second one. The same holds for an Always-check line in `REVIEW.md` that covers the class and still missed it: clarify that line rather than adding a near-duplicate in step 5. A prose rule (`CODING_STANDARDS.md`, `REVIEW.md`) is no guardrail for a mechanical class, which always ends with a deterministic check (step 5).
5. **Otherwise classify** as the "Coding standards" category in [SKILL.md](SKILL.md) does:
   - **Mechanical**: a deterministic check, whichever of a rule in the repo's linter, a line in its check script, a pre-commit hook or a CI job is cheapest next to the existing guardrail.
   - **Judgement**: one line under "Always check" in `REVIEW.md` at the repo root, naming the Bug class and what to look for, in one sentence. With no `REVIEW.md`, create it with three short sections (what Important means here, Skip, Always check): the Always-check line, and a sentence that the default meaning of Important applies, unless the user says otherwise.
6. **Run the new check on the current default branch.** If it fails anywhere on the default branch (Pre-existing places, or instances the reviewed pull request left unfixed), do not wire a failing check. Add those places to the open issue tracking that Bug class, or file one ([ROUNDS.md](../agentic-review/ROUNDS.md) "Filing Pre-existing Findings"), note there that the check lands with that fix, and use a `REVIEW.md` line meanwhile.
7. **Make the changes on a new branch off the default branch**, as one pull request for this retro (the reviewed pull request is done; leave it as it is). Adding or editing `REVIEW.md`, `CODING_STANDARDS.md` or any doc updates `docs/index.md` in the same commit ([DOCS-INDEX.md](../domain-modeling/DOCS-INDEX.md)). The pull request is reviewed like any other. One that adds or changes `REVIEW.md` changes the review rules, so a person merges it, not the agent.
8. **Report a table**, one row per Bug class. Classes with one instance read "not repeated" and need no change.

| Bug class | Instances | Finding ids | What was done |
| --- | --- | --- | --- |
| Unchecked null from the API client (merged with "missing null guard") | 3 | R1-2, R2-1 | New lint rule in `eslint.config.js` |
| Error messages leak internals | 2 | R1-4 | `REVIEW.md` Always-check line |
| Unused exports | 4 | R1-5, R2-3 | Existing `knip` job fixed: it skipped `src/lib` |
| Hardcoded timezone | 2 | R2-2 | `REVIEW.md` line now; check lands with Pre-existing issue #<n> |
| Wrong default in config loader | 1 | R1-1 | Not repeated |
