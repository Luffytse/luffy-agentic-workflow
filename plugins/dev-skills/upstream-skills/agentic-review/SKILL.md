---
name: agentic-review
description: "Review a pull request, or the changes since a fixed point (commit, branch, tag, or merge-base): parallel Finders look for problems on the standards, spec and adversarial angles, a Verifier checks each candidate against the code, and the survivors are ranked by Severity. A pull request is reviewed in Rounds (2 to 5), each posting one comment. Use when the user wants to review a PR, a branch, work-in-progress changes, run a ticket check, or asks to \"review since X\"."
---

A **Review** runs three stages over one diff: **Find** (fresh Finder subagents in parallel), **Verify** (a fresh Verifier checks every candidate Finding against the code), and **Rank** (you dedupe, drop repeats and sort). There are two entry points:

- **Pull request.** Review it in **Rounds**: each Round is one Review plus the fix commits after it, and posts one comment on the pull request. Rounds 1 and 2 review the whole pull request; Rounds 3 to 5 review only the commits added since the last Round (for a merge from main, only what it changed in the pull request). Follow [ROUNDS.md](ROUNDS.md).
- **A diff since a fixed point** (no pull request, or a **Ticket check**, which is one Quick Review over a Ticket branch's diff against its Spec branch). One Review, not a Round. Report it; for a Ticket check, also record it as described in [ROUNDS.md](ROUNDS.md#ticket-checks).

Every Finder and Verifier is a **brand-new subagent** each Review: never reuse one from an earlier Round or check, so each Review reads the code with fresh eyes.

Run the Review (Find, Verify, Rank and the Round loop) in the **top-level session**, the one that can start subagents. A subagent cannot start subagents of its own, so never hand the whole Review to one subagent: it stops at Find. If subagents cannot be started at all, stop and tell the user; do not do the Finders' or Verifier's work yourself.

The issue tracker should have been provided to you. If not, tell the user to run `setup-dev-skills`.

## Depth and tiers

The **Review depth** sets which agents run. Agents name a **model tier**, never a model.

| Depth | Finders | Verify |
|-------|---------|--------|
| Quick | standards + spec (regular) | 1 Verifier (regular) |
| Standard (default) | standards + spec (regular), 2 adversarial (cheap) | 1 Verifier (regular) |
| Deep | Standard's four, plus a security Finder (premium); after Verify, a gap sweep Finder (premium) | 3 Verifiers (regular): tracer, skeptic, spec checker; a second 3 for the gap sweep's Findings |

Pick Deep for risky changes (security, money, deleting data, or anything the user marks), Quick for docs-only or trivial ones, Standard for the rest. A depth the user or the brief names wins. For a pull request the depth is chosen once, in Round 1, and carried in each Round comment; later Rounds reuse it unless the user changes it. One exception: a **merge-only Round** (a Round 3 to 5 whose new commits are only a merge from main, plus any commit that takes the numbers after it, with conflicts only in numbers or text) runs at Quick unless the resolutions touch logic, and the Round after it goes back to the carried depth ([ROUNDS.md](ROUNDS.md#merge-only-rounds)). A Ticket check is always Quick.

## Process

### 1. Pin the diff

- **Pull request, Round 1 or 2:** the whole pull request, `git diff <base>...HEAD` (three-dot, against the merge-base), plus `git log <base>..HEAD --oneline`.
- **Pull request, Round 3 to 5:** the commits since the last Round, `git diff <last-head>..HEAD`, where `<last-head>` is the `head` recorded in the last Round comment. When those commits include a merge from main (`git log --merges --oneline <last-head>..HEAD` lists it), use `git log -p --first-parent --remerge-diff <last-head>..HEAD` instead: it shows each new commit of the pull request, and for the merge only what it changed in the pull request (its conflict resolutions), not the commits that came in from main. Tell the Finders so ([FINDERS.md](FINDERS.md)). Keep the whole-pull-request diff command too: Findings list every place their Bug class occurs in the pull request, not only in the new commits.
- **Fixed point:** whatever the user said (a SHA, branch, tag, `main`, `HEAD~5`); ask if they gave none. `git diff --merge-base <fixed-point>` (the working tree, so staged and unstaged work counts), plus every untracked new file from `git ls-files --others --exclude-standard`, read whole, and `git log <fixed-point>..HEAD --oneline`. Pull-request Rounds review commits only.

Record `git rev-parse HEAD` as this Review's head. Confirm every ref resolves (`git rev-parse`) and the diff (with the untracked files) is non-empty: a bad ref or empty diff fails here, not inside parallel subagents.

For a pull request, read every earlier comment by this skill on it (the `<!-- code-review` marker lines in [ROUNDS.md](ROUNDS.md#the-round-comment)): they give the Round number, the depth (the carried depth is the one in the latest comment that is not a merge-only Round's), the last head, and every Finding already raised, dismissed or open. Ticket-check comments count as already raised: their open Importants stay open until a Verifier confirms them fixed, or until they are dismissed because the user kept the design. For a Ticket check, read the earlier checks of the same Ticket the same way.

### 2. Find the spec and standards sources

Start at `docs/index.md` and open only the docs whose line fits the change (with no index, fall back to `GLOSSARY.md` or `GLOSSARY-MAP.md`, and `docs/adr/`).

**Spec**, in this order:

1. Issue references in the pull request body and commit messages (`#123`, `Closes #45`, GitLab `!67`), fetched via the workflow in the tracker doc.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If there isn't one, the spec Finder is skipped and the Review says "no spec available".

**Standards:** search the repo for every file that documents how code should be written, including `CLAUDE.md`/`AGENTS.md`, which the index does not list. `CODING_STANDARDS.md` and `CONTRIBUTING.md` must be on the list when they exist. The standards Finder also carries the smell baseline in [FINDERS.md](FINDERS.md).

**`REVIEW.md`** at the repo root, when present, overrides the default meaning of Important and adds a skip list and an Always check list. Pass it to every Finder and Verifier; the standards Finder checks each Always check line against the diff ([FINDERS.md](FINDERS.md#reviewmd-always-check)). Without it, **Important** means the change would break behaviour, lose or leak data, contradict the spec or an ADR, or make a rollback unsafe; anything else real is a **Nit**.

### 3. Find

Brief and start the Finders for the depth, all in one parallel batch in the foreground, each a brand-new subagent on its tier. The briefs, the adversarial angle list (pick 2 angles that fit this change) and the one fixed Finding format are in [FINDERS.md](FINDERS.md). Every Finder gets the diff commands, the commit list, the sources from step 2 and `REVIEW.md`. Before Verify starts, count the reports: you need one report from each Finder you started, a report that says "nothing found" included. A Finder that ended without returning its report is asked again for it; if it cannot be reached, start a new Finder on the same brief. Do not go on to Verify with a Finder missing. Tag each returned Finding with the Finder that raised it.

### 4. Verify

Start the Verifier(s) as brand-new subagents with every candidate Finding, every **open Important** from earlier Rounds and Ticket checks (to re-check against the current code), the spec, the standards list and `REVIEW.md`. Brief and voting rules: [VERIFY.md](VERIFY.md). The Verifier's calls are final: keep or drop, caused by this change or Pre-existing, Important or Nit, and "fix" or "skip" for a Nit. A failure scenario the Verifier corrected replaces the Finder's.

Before the next step starts (Rank, or on Deep the gap sweep, whose input is the Findings they kept), count the Verifier reports: you need one report from each Verifier you started. A Verifier that ended without returning its report is asked again for it; if it cannot be reached, start a new Verifier on the same brief. Do not go on with a Verifier missing.

On Deep, then run the **gap sweep**: one brand-new Finder gets the kept Findings and looks only for what the change is missing ([FINDERS.md](FINDERS.md#gap-sweep-premium-tier-deep-only)), and its Findings go through a second Deep Verify ([VERIFY.md](VERIFY.md#gap-sweep)). Count these reports the same way: you need one report from the gap sweep Finder before the second Verify starts, and one report from each second Verifier before Rank. A gap sweep Finder or second Verifier that ended without returning its report is asked again for it; if it cannot be reached, start a new Finder or Verifier on the same brief. Do not go on with one missing.

### 5. Rank and report

Rank the kept Findings yourself, by the rules in [ROUNDS.md](ROUNDS.md#rank). Report to the user under `## Important`, `## Nits` and `## Pre-existing`, each Finding with its Bug class, every location, the claim, its failure scenario and which Finder raised it; then one line with the number dropped by Verify.

For a pull request, post the Round comment and carry on with the Round loop and the stop rule in [ROUNDS.md](ROUNDS.md). For a fixed point, the report is the end; Pre-existing Findings are filed only if the user asks.

## Why the Finders stay separate

A change can pass one axis and fail another:

- Code that follows every standard but implements the wrong thing: **standards pass, spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions: **spec pass, standards fail.**

Each Finder works in its own context so one axis cannot mask another. Their Findings meet only after Verify, which judges each on its own evidence, and every reported Finding keeps the name of the Finder that raised it.
