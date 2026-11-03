---
name: agentic-review
description: "Review a pull request, or the changes since a fixed point (commit, branch, tag, or merge-base): parallel Finders look for problems on the standards, spec and adversarial angles, a Verifier checks each candidate against the code, and the survivors are ranked by Severity. A pull request is reviewed in Rounds (2 to 5), each posting one comment; a review that will not settle ends with restart or park. Use when the user wants to review a PR, a branch, work-in-progress changes, run a ticket check, or asks to \"review since X\"."
---

A **Review** runs three stages over one diff: **Find** (fresh Finder subagents in parallel), **Verify** (a fresh Verifier checks every candidate Finding against the code), and **Rank** (you dedupe, drop repeats and sort). There are two entry points:

- **Pull request.** Review it in **Rounds**: each Round is one Review plus the fix commits after it, and posts one comment on the pull request. Rounds 1 and 2 review the whole pull request; Rounds 3 to 5, a late design Round and a late merge-only Round review only the commits added since the last Round (for a merge from main, only what it changed in the pull request). Follow [ROUNDS.md](ROUNDS.md).
- **A diff since a fixed point** (no pull request, or a **Ticket check**, which is one Quick Review over a Ticket branch's diff against its Spec branch). One Review, not a Round. Report it; for a Ticket check, also record it as described in [ROUNDS.md](ROUNDS.md#ticket-checks).

Every Finder and Verifier is a **brand-new subagent** each Review: never reuse one from an earlier Round or check, so each Review reads the code with fresh eyes.

Run the Review (Find, Verify, Rank and the Round loop) in the **top-level session**, the one that can start subagents. A subagent cannot start subagents of its own, so never hand the whole Review to one subagent: it stops at Find. If subagents cannot be started at all, stop and tell the user; do not do the Finders' or Verifier's work yourself.

The issue tracker should have been provided to you. If not, tell the user to run `setup-dev-skills`.

## Depth and tiers

The **Review depth** sets which agents run. Agents name a **model tier**, never a model. Load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it.

| Depth | Finders | Verify |
|-------|---------|--------|
| Quick | standards + spec (regular) | 1 Verifier (regular) |
| Standard (default) | standards + spec (regular), 2 adversarial (cheap) | 1 Verifier (regular) |
| Deep | Standard's four, plus a security Finder (premium); after Verify, a gap sweep Finder (premium) | 3 Verifiers (regular): tracer, skeptic, spec checker; a second 3 for the gap sweep's Findings |

Pick Deep for risky changes (security, money, deleting data, or anything the user marks), Quick for docs-only or trivial ones, Standard for the rest. A depth the user or the brief names wins. For a pull request the depth is chosen once, in Round 1, and carried in each Round comment; later Rounds reuse it unless the user changes it. One exception: a **merge-only Round** runs at the depth [ROUNDS.md](ROUNDS.md#merge-only-rounds) gives after accounting for its main merges and permitted final text-Nit and version-only bump commits; logic resolutions retain the carried depth, and the following ordinary Round restores it. A Ticket check is always Quick.

## Process

### 1. Pin the diff

- **Pull request, Round 1 or 2:** the whole pull request, `git diff <base>...HEAD` (three-dot, against the merge-base), plus `git log <base>..HEAD --oneline`.
- **Pull request, Round 3 to 5, a late design Round or a late merge-only Round:** the commits since the last Round, `git diff <last-head>..HEAD`, where `<last-head>` is the `head` recorded in the last Round comment. When those commits include a merge from main (`git log --merges --oneline <last-head>..HEAD` lists it), use `git log -p --first-parent --remerge-diff <last-head>..HEAD` instead: it shows each new commit of the pull request, and for the merge only what it changed in the pull request (its conflict resolutions), not the commits that came in from main. Tell the Finders so ([FINDERS.md](FINDERS.md)). Keep the whole-pull-request diff command too: Findings list every place their Bug class occurs in the pull request, not only in the new commits.
- **Fixed point:** whatever the user said (a SHA, branch, tag, `main`, `HEAD~5`); ask if they gave none. `git diff --merge-base <fixed-point>` (the working tree, so staged and unstaged work counts), plus every untracked new file from `git ls-files --others --exclude-standard`, read whole, and `git log <fixed-point>..HEAD --oneline`. Pull-request Rounds review commits only.

Record `git rev-parse HEAD` as this Review's head. Confirm every ref resolves (`git rev-parse`) and the diff (with the untracked files) is non-empty: a bad ref or empty diff fails here, not inside parallel subagents.

Load the `review-record` skill by name before reading or writing review comments and before briefing Finders. For a pull request, read every earlier record comment: they give the Round number, the depth (the carried depth is the one in the latest Round comment that is not a merge-only Round's), the last head, and every Finding already raised, dismissed or open. Ticket-check comments count as already raised: their open Importants stay open until a Verifier confirms them fixed or dismisses them as never real, or until they are dismissed because the user or an agent kept the design ([ROUNDS.md](ROUNDS.md#design-findings)) or merged into another row ([ROUNDS.md](ROUNDS.md#rank) step 3). For a Ticket check, read the earlier checks of the same Ticket the same way.

### 2. Find the spec and standards sources

Start at `docs/dev-skills/index.md` and open only the docs whose line fits the change (with no index, fall back to `docs/dev-skills/glossary.md` and `docs/dev-skills/adr/`).

**Spec**, in this order:

1. Issue references in the pull request body and commit messages (`#123`, `Closes #45`, GitLab `!67`), fetched via the workflow in the tracker doc.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If there isn't one, the spec Finder is skipped and the Review says "no spec available".

**Retro origin.** A build thread's corrective check pull request builds no issue. Before Review, its caller records exactly one `Retro origin: <originating Ticket or Spec issue link>` line in the pull request body. Read that issue through the configured tracker. This line supplies only the membership and design-answer source: it does not make the check build or close that issue, or import its attempt history. Other issue references alone supply no inherited membership to a no-issue pull request. For this check, “spec issue” in the design-answer and settled-design rules means this origin issue; the corrective check's scope remains its own pull request. An unreadable or ambiguous origin must be resolved with the caller before Review proceeds.

**Milestone.** For a pull request or a Ticket check, decide whether it is **inside a Milestone**, as the build skills decide it: read the Boundary record (`docs/dev-skills/boundaries.md`) for its Milestone label form. Use the issue it builds (a lone Ticket, or the Spec of a Spec pull request or a Ticket check), or, only for a no-issue corrective check, its recorded Retro origin. It is inside a Milestone when this source issue carries a label in that form; then fetch the Milestone issue (the issue that carries the same label and holds the Milestone's goal) and the source issue's comments. With no Boundary record, no source issue, or no label in its form, it is outside a Milestone. Report `Milestone: <label or outside>; source: <issue link or none>` in each Round or Ticket check, including outside membership. Membership decides who answers design Findings ([ROUNDS.md](ROUNDS.md#design-findings)) and whether an Important can be rebutted ([ROUNDS.md](ROUNDS.md#rebuttals-inside-a-milestone)); it does not change the convergence check or what ends an attempt ([ROUNDS.md](ROUNDS.md#when-a-review-will-not-settle)). For a pull request, inside a Milestone or outside one, also read every attempt record on the issue it builds (the `review-record` attempt-record shape; on the pull request itself when it builds no issue): earlier attempts of the same problem, whose returned and flipped Findings count in the convergence check.

**Settled designs**, which every Finder and Verifier gets: the decisions the spec records; every row of an earlier Round or Ticket-check comment dismissed because the user or an agent kept the design whose locations have not changed since the head of the comment that dismissed it (by the change test of [ROUNDS.md](ROUNDS.md#rank) step 2; a row whose lines changed is not settled), with its claim, its Note and its locations brought to this head as [ROUNDS.md](ROUNDS.md#rank) says; and, inside a Milestone, the design answers recorded as comments on the spec issue.

**Standards:** search the repo for every file that documents how code should be written, including `CLAUDE.md`/`AGENTS.md`, which the index does not list, and any team style guide the repo keeps. `CONTRIBUTING.md`, wherever the repo keeps it (the root, `docs/` or `.github/`), must be on the list when it exists. The standards Finder also carries the smell baseline in [FINDERS.md](FINDERS.md).

**`REVIEW.md`** at the repo root, when present, overrides the default meaning of Important and adds a skip list and an Always check list. Pass it to every Finder and Verifier; the standards Finder checks each Always check line against the diff ([FINDERS.md](FINDERS.md#reviewmd-always-check)). Without it, **Important** means the change would break behaviour, lose or leak data, contradict the spec or an ADR, or make a rollback unsafe; anything else real is a **Nit**.

### 3. Find

Brief and start the Finders for the depth, all in one parallel batch in the foreground, each a brand-new subagent on its tier. The briefs, the adversarial angle list (pick 2 angles that fit this change) and the one fixed Finding format are in [FINDERS.md](FINDERS.md). Every Finder gets the diff commands, the commit list, the sources from step 2 (the settled designs included) and `REVIEW.md`. Before Verify starts, count the reports: you need one report from each Finder you started, a report that says "nothing found" included. A Finder that ended without returning its report is asked again for it; if it cannot be reached, start a new Finder on the same brief. Do not go on to Verify with a Finder missing. Tag each returned Finding with the Finder that raised it.

### 4. Verify

Start the Verifier(s) as brand-new subagents with every candidate Finding, every **open Important** from earlier Rounds and Ticket checks (to re-check against the current code, its locations first brought to this head as [ROUNDS.md](ROUNDS.md#rank) says), the spec, the settled designs (step 2), the standards list and `REVIEW.md`. Brief and voting rules: [VERIFY.md](VERIFY.md). The Verifier's calls are final: keep or drop, caused by this change or Pre-existing, Important or Nit, and "fix" or "skip" for a Nit. A failure scenario the Verifier corrected replaces the Finder's. Inside a Milestone, after the report, the owner of the code may rebut an open Important that is not a design Finding, with evidence, instead of fixing it, and a brand-new premium-tier rebuttal Verifier makes the final call ([VERIFY.md](VERIFY.md#rebuttals), [ROUNDS.md](ROUNDS.md#rebuttals-inside-a-milestone)).

Before the next step starts (Rank, or on Deep the gap sweep, whose input is the Findings they kept), count the Verifier reports: you need one report from each Verifier you started. A Verifier that ended without returning its report is asked again for it; if it cannot be reached, start a new Verifier on the same brief. Do not go on with a Verifier missing.

On Deep, then run the **gap sweep**: one brand-new Finder gets the kept Findings and looks only for what the change is missing ([FINDERS.md](FINDERS.md#gap-sweep-premium-tier-deep-only)), and its Findings go through a second Deep Verify ([VERIFY.md](VERIFY.md#gap-sweep)). Count these reports the same way: you need one report from the gap sweep Finder before the second Verify starts, and one report from each second Verifier before Rank. A gap sweep Finder or second Verifier that ended without returning its report is asked again for it; if it cannot be reached, start a new Finder or Verifier on the same brief. Do not go on with one missing.

### 5. Rank and report

Rank the kept Findings yourself, by the rules in [ROUNDS.md](ROUNDS.md#rank). Report to the user under `## Important`, `## Nits` and `## Pre-existing`, each Finding with its Bug class, every location, the claim, its failure scenario and which Finder raised it, an earlier Important still open and a partly fixed "fix" Nit included under their ids ([ROUNDS.md](ROUNDS.md#rank) step 3), each with its live locations, the Verifier's still-open line when it has one and, when no Finding of this Review is held under it, the claim from its row's Note; then one line with the number dropped by Verify.

For a pull request, post the Round comment and carry on with the Round loop and the stop rule in [ROUNDS.md](ROUNDS.md); inside a Milestone, this report and your report to your caller when the Rounds end list the agents' design answers ([ROUNDS.md](ROUNDS.md#an-agent-answers-inside-a-milestone)); and when the convergence check, Round 5, the late design Round or the late merge-only Round ends the attempt (a second conflicting merge after the late merge-only Round and an inside-Milestone agreed design change after either clean late Round included, which run no Round), inside a Milestone or outside one, your report to your caller gives its outcome, `restart` or `park`, with the attempt record's link ([ROUNDS.md](ROUNDS.md#ending-an-attempt)). For a fixed point, the report is the end; Pre-existing Findings are filed only if the user asks.

## Why the Finders stay separate

A change can pass one axis and fail another:

- Code that follows every standard but implements the wrong thing: **standards pass, spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions: **spec pass, standards fail.**

Each Finder works in its own context so one axis cannot mask another. Their Findings meet only after Verify, which judges each on its own evidence, and every reported Finding keeps the name of the Finder that raised it.
