# Model evals are retired: a skill change merges on CI, the review and its acceptance lines

This repo runs no model evals. The eval folder and the evals guide are deleted, and a pull request that changes skill text merges when it shows three things: **CI is green** (the plugin checker, the plugin validation and the script tests), **the review is done** as `REVIEW.md` says, and **each acceptance line of the issue it builds is shown as met** in the pull request body, one line of evidence each (a word count, a word diff against the inherited text, a search that finds nothing, a script test). A gap a real project finds in a skill comes back as a Retro issue. This replaces [ADR 0013](0013-skill-changes-are-tested-by-ci-evals-and-review.md). Settled with the user on 2026-11-13 in the planning of Milestone 4 (Spec #147, answering #141; #5 and #7 closed as not planned).

## Why

The eval rules were built on 2026-11-03 because the skills were not stable then: a behaviour change ran the skill's eval cases on its own text and on main's, and each new case had a premium-tier check. Since then the eval folder grew to 25 suites and about 420,000 words, and of its 37 test files only 5 tested a script the plugin ships; the other 32 tested the evals' own fixtures and scorers. In the skill-by-skill walk of 2026-11-11 to 2026-11-13, every call on a skill rested on real pull requests, review comments and Retro issues from three repos, and none on an eval result. A search for a rule returned the stale cases with it, and about 33 open issues ended their acceptance with an eval line that only one stated rule could replace.

## Decisions

- **Three things before a merge**, stated once in this repo's `CLAUDE.md` in place of the `**Eval:**` line rule. No eval is run here, even while `tdd`, `implement` and `implement-spec` still carry their sentence that instructions for an agent are tested by an eval (those sentences leave under #135, #132 and #134).
- **Two layers remain, CI and review.** If a script can catch it, it is CI; otherwise it is review, and real use shows the rest through Retro issues (the path #140 builds).
- **The shipped scripts keep their tests.** The tests of `review_briefs.py` and `snapshot.py` moved to `scripts/`, and `scripts/run-tests.sh` looks in `scripts/` only. A test that mixed script coverage with an eval scorer or dry-run cases kept only what no other test covered.
- **Docs and skill text are built without `tdd`**; a script change is built with `tdd` and a script test. `codebase-design`, `improve-codebase-architecture`, `prototype`, `diagnosing-bugs` and `wizard` run only when the user asks.
- Git history keeps the eval folder and the guide; no archive copy stays in the tree.

## Considered options

- **Keep a small core of cases** (the review fixture, the delivery dry runs). Each kept case still needs a run rule, a baseline and a case check, so the rule and its cost stay for a few cases no decision rested on.
- **Keep the folder with no rule.** It would go stale at once, and every search for a rule would still return it.

## Consequences

- Other ADRs and the changelog that name an eval path are history and are not edited.
- A Retro issue, not an eval case, is how a skill's gap reaches this repo, and it waits for the next Milestone's planning.
