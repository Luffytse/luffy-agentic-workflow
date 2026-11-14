# agentic-review sizes a review in Round 0, then runs Find, Verify and Rank in at most 3 Rounds

Our review follows the shape of Claude Code's own Code Review (Finders, then a Verifier that drops false positives, then ranking by Severity), adapted to agents that review their own pull requests in a session. It is split into small skills that load only when needed: `agentic-review` holds only **Round 0**, the hidden `review-rounds` skill holds the Rounds and the loop, and `review-record` holds the comment shape.

Amended 2026-11-03 (Spec #555, replacing #352 and #137): this ADR described Rounds 2 to 5 at a chosen Review depth, with a convergence check, attempt records, `restart` and `park` outcomes, late design and late merge-only Rounds, rebuttals decided by a premium Verifier, and three Deep Verifiers voting. That text had grown to about 12,500 words of skill, most of it rules that never ran (no attempt ever ended), every pull request paid at least two full Rounds, and the review could stop for the user for reasons the Boundary record does not list. Peer reviews do the job in about 1,100 words, and the published evidence says the first pass gives most of the value and later passes should look only at new commits. All of that is removed; what follows is the review now.

## Round 0

The top-level session, with no subagent, pins the diff, reads the changed files, `git diff --stat`, the Boundary record and `REVIEW.md`, and picks a **level**: None, Quick, Standard or Deep. The defaults, which a "Review levels" section in `REVIEW.md` overrides:

- **Deep:** the change touches what the Boundary record or `REVIEW.md` marks risky (security, money, deleting data, migrations), or the user asks.
- **None:** every changed line is a version field, a changelog entry, a lock file or generated output.
- **Quick:** text that leaves what each rule or line of code does as it was. *Amended 2026-11-14, Spec #183:* a change that touches only prose docs is Quick; skills, `CLAUDE.md`, `AGENTS.md`, `REVIEW.md` and decision records stay Standard.
- **Standard:** everything else.

When unsure it takes the higher level. It records the level with a one-line reason. At None that line is the whole review comment, and the project's automated checks must pass. Above None the session loads `review-rounds` and runs Round 1. A review since a fixed point (no pull request) runs Round 0, then Round 1 only, and reports.

## A Round

Find, Verify, Rank, one comment. Sources (spec, standards, `REVIEW.md`, Boundary record) are gathered once in Round 1 and passed on.

- **Quick:** the standards and spec Finders (regular tier), then one Verifier (regular).
- **Standard:** those two plus one adversarial Finder (cheap) on the angle that fits the change best, then one Verifier.
- **Deep:** Standard plus a security Finder (premium), then one premium Verifier. "What the change is missing" is one of the adversarial angles.
- **Rounds 2 and 3:** at any level, one Finder (standards and spec in one) and one Verifier.
- **Nothing to verify:** a Round in which no Finder returned a candidate and no earlier Finding is open starts no Verifier and goes to Rank; its comment says no candidates went to a Verifier. Otherwise the Verifier stays a separate agent each Round (#583). *Amended 2026-11-14, Spec #183:* a Finder report off the Report format no longer stops the Round: the Brief script passes it to the Verifier as written with a note, and stops only for a missing or empty report.

Adversarial Finders get no Always check lines; the standards Finder gets only the lines for the files the diff touches, and the smell baseline only when code changed. The review looks for risk, security, boundary crossings and whether the change carries tests for what it claims. A Finding quotes its line, and for code shows a run or failing test where it can; the Verifier keeps only what it confirmed. Every Finder and Verifier is a brand-new subagent each Round, given a brief, never the skill.

## The loop

- **Round 1** reviews the whole pull request. Clean (no Important open after Verify) means ready to merge.
- **Rounds 2 and 3** review only the pull request's new commits (`git log -p --first-parent --remerge-diff`), so a merge from main shows only its conflict resolutions. Earlier Findings are matched by file and claim; a dismissed one is not raised again unless its code changed. The level only goes up, when a new commit touches a risky path.
- **Disputes.** An owner who thinks a Finding is wrong writes why, with evidence, and the next Verifier decides. When nothing was committed, the next Round is the Verifier alone, on the disputes.
- **After Round 3**, a premium agent turns each open Important into a bug Ticket or dismisses it with a reason. Nits are dropped and the pull request merges. *Amended 2026-11-14, Spec #183:* the thread reports each bug Ticket to its caller and builds none (the first wording had it worked straight away as its own Ticket), and each Ticket carries a `Joins the running Release:` line saying whether and why it joins the running Release.
- **Design Findings** go to a premium agent that answers within what the spec agreed (the pull request body when it builds no issue), recorded as a comment on the spec issue, or on the pull request when it builds no issue. An answer that changes the pull request is fixed in the next Round; one in or after Round 3 becomes a bug Ticket. The answers are listed on the pull request body's `Agent-merged rules:` line and in the build thread's report, and the Milestone report reads only its rules-file part.
- **Merges from main:** conflict resolutions go to the next Round; after Round 3, at most one Quick check of only the resolutions runs, and its open Importants become bug Tickets. A version-only last commit needs no review. *Amended 2026-11-14, Spec #183:* that sentence left the skill, because the version is bumped at the Release cut (ADR 0016), not in a pull request; a resolutions check's open Importants also carry the `Joins the running Release:` line.
- **Resuming:** a fresh session continues from the latest Round comment. After Round 3 there is no next Round, only the sort, which records each bug Ticket on its row as it is filed, so a rerun files none twice.
- **Ticket checks:** one Quick Round on a Ticket branch against its Spec branch, recorded on the Spec pull request; its open Findings carry into the Spec pull request's Round 1.

## Stopping for a person

The review stops for a person only when a fix, a design answer, a bug Ticket or the merge would cross a boundary as the `merging` skill defines it (an action the project's **Boundary record** says needs the user's approval, a one-way door it does not allow agents, or a limit or budget it sets). The Round comment's Result then reads `waiting on a boundary: <what would be crossed>` until the user's answer clears it; a resumed session asks for that answer if none is on the pull request, then continues the step that was waiting. Nothing else in the review stops for the user; the build skills' own merge lists (ADR 0004) still decide who merges.

## Records

One comment per Round, each Finding with an id, Severity, Bug class, `file:line`, claim and status (open, fixed or dismissed), so a fresh session can continue a review and `retro` can find recurring Bug classes. *Amended 2026-11-14, Spec #157:* a retro no longer adds a check or a `REVIEW.md` line itself; it files a Retro issue that proposes it. After the last Round, Pre-existing Findings are filed as issues, grouped by Bug class.

## Considered options

- **Keep Rounds 2 to 5 with a convergence check, attempts, restart and park.** Bounded a stuck review, but none of it ever ran, and its text was most of what every review read. Three Rounds and the after-Round-3 sort bound it more simply: a stuck Important becomes a bug Ticket instead of an attempt.
- **Rebuttals decided by a premium Verifier.** Replaced by the plain dispute: the owner writes why, the next Verifier decides.
- **Three Deep Verifiers voting, and a second gap-sweep Verify.** Costly for little gain; one premium Verifier and a security Finder keep Deep's extra depth.
- **Every pull request at a fixed depth.** A version bump or a typo paid two full Rounds. Round 0 sizes the review from the changed files, and at None the checks are the review.
- **Every design Finding to the user.** The pull request waits for questions the spec already answers. An agent answers within the spec; the user is asked only when the answer would cross the Boundary record.
- **Claude Code's cap of 3 Rounds** (after three Rounds their reviewer asks the author to reconsider). We take the same cap, with the sort into bug Tickets instead of asking the author.
