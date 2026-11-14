# Code review

How a change to skill text is tested, and the words of a Review: its Rounds, its agents and what a Finding is. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Testing skill changes

A change to skill text is tested in two layers, **CI** and **Review**: if a script can catch it, it is CI; otherwise it is review, and real use shows the rest through Retro issues. No model eval is run in this repo: a skill change merges on CI green, the review and its issue's acceptance lines shown as met (ADR 0015, `CLAUDE.md`).

**CI**:
The layer for questions with one right answer from the files: a script with no model, on every pull request (the plugin checker, `claude plugin validate` and `scripts/run-tests.sh`). It tests structure, banned names and what a script does, never that a skill holds a given sentence.

## Language

**Review**:
One review of a change by the `agentic-review` skill: **Round 0** sizes it, and above level None the hidden `review-rounds` skill runs its Rounds. It reviews a pull request in up to 3 Rounds, or the diff since a fixed point (a commit, branch, tag or merge-base) in Round 0 and Round 1 only, with no comment.

**Round 0**:
The step, run by the top-level session itself before any agent starts, that sizes a Review: it picks the **Review level** with a one-line reason and records it. At None that line is the whole review comment. Owned by `agentic-review`.

**Review level**:
How much review a change gets, picked by Round 0: **None** (the project's checks only), **Quick** (text that does not change what a rule or code does, and a change that touches only prose docs; skills, `CLAUDE.md`, `AGENTS.md`, `REVIEW.md` and decision records stay Standard), **Standard** (everything else, the default) or **Deep** (what the Boundary record or `REVIEW.md` marks risky, or the user asks). `REVIEW.md` may name a project's own paths per level; what each level covers is `agentic-review`'s. Older records call it the Review depth.
_Avoid_: depth, mode

**Round**:
One pass of Find, Verify and Rank over a pull request, its one comment, and the fix commits after it; a pull request gets at most 3. **Round 1** reviews the whole pull request; **Rounds 2 and 3** review only its new commits. A Round is **clean** when no Important is open after its Verify step, which means ready to merge. Owned by `review-rounds` (ADR 0003).
_Avoid_: pass, iteration

**After-Round-3 sort**:
What happens when Round 3 is not clean: a premium-tier agent turns each open Important into a bug Ticket or dismisses it with a reason, open Nits are dropped, and the pull request is ready to merge. Each bug Ticket carries a `Joins the running Release:` line (`severe`, `blocks #<n>`, `breaks an acceptance criterion of #<n>` or `no`); the thread reports each Ticket to its caller and builds none. Owned by `review-rounds`.

**Dispute**:
An owner's written case, with evidence (`file:line`, a command and its output), that a Finding is wrong, in place of a fix. The next Round's Verifier decides it (`review-rounds`).
_Avoid_: rebuttal (the earlier, removed rule)

**Design Finding**:
A Finding that questions the design itself (a gap in the agreed behaviour, two rules in conflict, a case left open). A premium-tier agent answers it within what the spec agreed, and the answer is listed on the pull request body's `Agent-merged rules:` line. Owned by `review-rounds`.

**Waiting on a boundary**:
The one way a Review stops for a person: a fix, a design answer, a bug Ticket or the merge would cross a boundary as the `merging` skill defines it. The user's answer clears it. Owned by `review-rounds`.

**Question round**:
One batch of questions a skill (`grilling`, `triage`) puts to the user at once. Not a Round, and not a Review: the skills' "round" without a capital R means this.
_Avoid_: Round (for a batch of questions)

**REVIEW.md**:
A short file at a repo's root telling reviewers what Important means there, what to skip, what to always check (the **Always check** lines, each a Bug class earlier reviews caught) and optionally its own Review levels. The line form is `review-record`'s.

**Finder**:
A reviewer agent that looks for problems and reports candidate Findings, as a Markdown report in the **Report format** (Findings, then any notes under one `## Notes` heading), written to the file its brief names. Its kinds are the **standards Finder** and **spec Finder** (from Upstream), the **adversarial Finder**, the premium **security Finder** and the **later-Round Finder**; which run at each level and Round is `review-rounds`'.
_Avoid_: reviewer (too broad), scanner

**Brief script**:
`review_briefs.py`, in the `review-rounds` folder: it writes each Round's Finder and Verifier briefs, one complete Markdown file per agent, cut from the skill's brief files, and its `verify` checks each Finder's report against the **Report format**. How the briefs are handed out, or built by hand when it cannot run, is `review-rounds`'.
_Avoid_: brief builder

**Verifier**:
The one agent per Round that checks each candidate Finding, and each open Finding with any dispute of it, against the code, keeps only what it confirmed and makes the final call on it. When it is skipped and its tier are `review-rounds`'.
_Avoid_: judge, triage agent

**Finding**:
One problem a Review reports, with a file and line, a Severity, a Bug class, and a Failure scenario.
_Avoid_: issue (that word means a GitHub issue), comment

**Severity**:
How much a Finding matters. **Important** must be fixed before the change is merged or accepted. **Nit** is small and optional. **Pre-existing** is real but not caused by the change under review.
_Avoid_: priority, blocker

**Bug class**:
The kind of problem a Finding is (for example "unescaped user input"), so every place it occurs is fixed together.
_Avoid_: category, type

**Failure scenario**:
The part of a Finding that shows the problem happens: the inputs or state, then the wrong result. A cleanup Finding (a smell, or a Nit with no wrong result) states its cost instead.
_Avoid_: repro, example
