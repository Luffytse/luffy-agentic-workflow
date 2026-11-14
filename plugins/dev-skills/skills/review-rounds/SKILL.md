---
name: review-rounds
description: "Run a review's Rounds (Finders, Verifier, Rank, one comment, at most 3) once agentic-review's Round 0 has picked a level. Use when Round 0 hands over a Round or a Ticket check."
user-invocable: false
---

A **Round** is one Review of a pull request (Find, Verify, Rank; Verify is skipped when there is nothing to verify), its one comment, and the fix commits after it. A pull request gets at most **3 Rounds**. Load `review-record` by name for the comment shape and for reading earlier comments.

Run every Round in the **top-level session**, the one that can start subagents: a subagent cannot start its own, so never hand a Round to one. Every Finder and Verifier is a **brand-new subagent** each Round, given a brief, never this skill. If subagents cannot be started, stop and tell the user. Agents name a **model tier**; load `model-tiers` by name for the model each tier is in your coding agent (the project's own tier map wins). The issue tracker should have been provided to you; if not, tell the user to run `setup-dev-skills`.

## Who runs

| Round | Finders | Verifier |
|-------|---------|----------|
| Round 1, Quick | standards, spec (regular) | 1 (regular) |
| Round 1, Standard | standards, spec (regular); 1 adversarial on the best-fitting angle (cheap) | 1 (regular) |
| Round 1, Deep | Standard's three, plus a security Finder (premium) | 1 (premium) |
| Rounds 2 and 3, any level | 1 later-Round Finder: standards and spec in one (regular; premium at Deep) | 1 (regular; premium at Deep) |

A Verifier column entry is the Verifier that runs when step 3 starts one; step 3 says when none runs.

The brief text is in [FINDERS.md](FINDERS.md), [VERIFY.md](VERIFY.md) and, at Deep, [DEEP.md](DEEP.md); they are its only source.

## Briefing the agents

Run `python3 <this skill's folder>/review_briefs.py <kind> ...` (Python 3 and git only; `--help` gives the options) to write one complete brief file per agent into a directory you name outside the work tree. Give each file's path to one brand-new subagent, at the tier the script prints beside it, and tell it: "read it whole; it is your only instruction". Paste the file whole only into an agent that cannot read files. The kind is the Round: `round1` (Round 1), `later` (Round 2 or 3), `ticket` (a Ticket check), `fixed` (a diff since a fixed point), `verify` (the Verifier, after the Finders), `disputes` (the Verifier alone on disputes). You still decide what needs judgement and pass it in as files: the spec, the standards files, the adversarial angle, the earlier open Findings with their disputes, the design answers.

Each Finder brief names the file its Finder writes its report to (`<out>/reports/<finder>.md`) and the Report format ([FINDERS.md](FINDERS.md)), and the Finder also returns the report as its final message (the Verifier's brief names `<out>/reports/verifier.md` the same way); a Finder that says it could not write the file has its message saved there by you. Run `verify` over those files, with the same `--level` and `--spec` (and `--round`, `--for`) as the Round's briefs and no retyping: it checks that each Finder reported in the Report format (Findings, or a line saying nothing found, with any notes under one `## Notes` heading), names any that did not (ask that Finder again, as step 2 says), and carries the reports into the Verifier's brief as written. It writes no brief when there is nothing to verify.

If the script cannot run or stops on a section it cannot find, build each brief by hand from the brief files: each Finder gets only what its section lists, the Verifier what VERIFY.md lists.

## Sources, gathered once

In Round 1, gather these and pass them on to Rounds 2 and 3; re-read only a source a new commit changed.

- **Spec:** the issues the pull request body and commit messages reference, fetched through the tracker; a path the user passed; a spec file under `docs/` or `specs/` matching the branch. A pull request that references no issue is its own spec: its body. With none, the spec Finder is skipped and the Review says "no spec available".
- **Standards:** the files that say how code or text is written here (`CLAUDE.md`, `AGENTS.md`, a style guide, `CONTRIBUTING.md`). Start at `docs/dev-skills/index.md` when the repo has one.
- **`REVIEW.md`**, at the repo root when present: the meaning of Important, the Skip list and the Always check lines, each as `- **<Bug class>** (files: `glob`, `glob`; from ...): what to look for` (`(files: all)` applies to every diff). Without it, **Important** means the change would break behaviour, lose or leak data, contradict the spec or a recorded decision, or make a rollback unsafe; anything else real is a Nit.
- **Boundary record**, `docs/dev-skills/boundaries.md` when present: what the project marks risky and what needs a person.
- **Earlier records:** every Round and Ticket-check comment on the pull request, and the design answers recorded on the spec issue.

## A Round

1. **Pin.** Round 1 reviews the whole pull request, with Round 0's diff. Rounds 2 and 3 review only its new commits: `git log -p --first-parent --remerge-diff <last-head>..HEAD`, where `<last-head>` is the head in the last Round comment. This shows each commit of the pull request, and for a merge from main only its conflict resolutions. Record `git rev-parse HEAD` as the head.
2. **Find.** Start the Finders for this Round in one parallel batch. Before Verify, count one report from each Finder, a "nothing found" included; ask again for a missing one, or start a new Finder on the same brief.
3. **Verify.** Start the Verifier with every candidate, tagged with its Finder, and every open Finding from earlier Rounds and Ticket checks, with any dispute of it. Its calls are final. Its brief names the file it writes its report to (`<out>/reports/verifier.md`); wait for that file the same way as for the Finders' (a Verifier that says it could not write it has its message saved there by you), and read the verdicts from it. When no Finder returned a candidate and no earlier Finding is open, start no Verifier: go to Rank, and the Round comment says no candidates went to a Verifier. Otherwise the Verifier is a separate agent each Round.
4. **Rank** yourself. Two Findings match when they are in the same file and make the same claim. Merge matching Findings into one, keeping every location and Finder. A Finding matching an earlier open one keeps that id. Drop one matching an earlier dismissed Finding, unless the code at its locations changed since. Sort Important, then Nit, then Pre-existing; report at most 5 Nits, "fix" ones first.
5. **Post** the Round comment and report to your caller under `## Important`, `## Nits` and `## Pre-existing`, each Finding with its id, Bug class, locations, claim and failure scenario.

## Resuming

A session that finds Round comments already posted continues from the latest one:

- **Its Result reads `waiting on a boundary: …`:** the user's answer clears it. Look for that answer on the pull request after the comment; with none, ask the user and wait. Then continue the step that was waiting, as the answer says, and record a spoken answer as a pull request comment.
- **Round 1 or 2:** not clean, run the next Round; clean, the review is over (ready to merge), unless a merge with conflicts since then needs its Round (see Merges from main).
- **Round 3:** there is no next Round. If it is not clean and its Result does not yet read `sorted after Round 3`, do the sort below; otherwise the review is over: ready to merge, with any bug Tickets as the remaining work.

## The loop

A Round is **clean** when no Important is open after its Verify.

- **Clean:** the owner commits the "fix" Nits in one last commit that the project's checks pass, and the Round comment, posted after it, marks them fixed. The pull request is ready to merge.
- **Not clean:** the owner of the code (in a build thread, its Implementer) fixes every open Important and "fix" Nit and leaves the "skip" Nits. An owner who thinks a Finding is wrong writes why, with evidence (`file:line`, a command and its output), in the commit message or a pull request comment, and the next Verifier decides. Each open Important is fixed or disputed before the next Round. When nothing was committed since the last head, the next Round is the Verifier alone, on the disputes (an open dispute is an open Finding, so that Verifier runs).
- **The level only goes up.** When a new commit touches what Round 0 would call Deep, the next Round runs at Deep.
- **After Round 1 or 2**, if not clean, the next Round follows. **After Round 3**, if not clean, sort what is open (below).

A last commit that changes only a version field and its changelog entry needs no review.

## After Round 3

Start one brand-new premium-tier agent with the open Importants whose Note names no bug Ticket yet, the spec and the Boundary record. For each it chooses one, and you carry it out, one row at a time, editing that row's Note on the Round 3 comment as soon as it is done, so a rerun files no Ticket twice:

- **Bug Ticket:** create an issue with the tracker's "Create an issue" operation, holding the Finding's claim, `file:line`, failure scenario and a link to the pull request, with the `bug` category and `ready-for-agent` state labels the repo's triage-labels doc maps, and the repo labels that fit the Finding, as the triage-labels doc says; the row's Note becomes `bug Ticket: <link>`. Your caller works it straight away, as its own Ticket.
- **Dismiss:** with a one-line reason; the row becomes `dismissed`, `dismissed after Round 3: <reason>`.

Open Nits are dropped. Last, edit the Round 3 comment's Result to the sorted one. The pull request is then ready to merge.

## Design Findings

A design Finding questions the design itself: a gap in the agreed behaviour, two rules that conflict, a case the design leaves open. Its fix would record a decision. For each, start one brand-new premium-tier agent with the Finding, the spec with its comments, and the decision records and glossary lines it touches. It answers within what the spec agreed: **keep the design** (the row is dismissed, `design kept: <link>`), or **a change** the owner makes, fixed in the next Round. Record each answer as a comment on the spec issue with the tracker's "Comment on an issue" operation (on the pull request when it builds no issue). A change answered in or after Round 3 becomes a bug Ticket. List the design answers in your report to your caller, each by its row id and the link to its record.

## Merges from main

A merge's conflict resolutions are new commits, and the next Round reviews them, after a clean Round 1 or 2 too. Only after Round 3 does a merge with conflicts get one Quick check of only its resolutions (`git show --remerge-diff <merge>`), recorded as a resolutions check; its open Importants become bug Tickets as after Round 3. At most one such check runs per pull request, over every resolution since the last reviewed head, so run it just before the merge. A merge without conflicts needs no review; the project's checks must pass.

## When a person is needed

Only when a fix, a design answer, a bug Ticket or the merge would cross a boundary, as the `merging` skill defines a crossing (load it by name and read only its "Who merges" part, not the merge flow). Then set the Round comment's Result to `waiting on a boundary: <what would be crossed>`, and tell your caller which Finding and which boundary. The user's answer clears it (see Resuming). Nothing else stops the review for a person.

## Pre-existing Findings

After the last Round, file the open Pre-existing Findings, grouped by Bug class. For each class, comment the new locations on an open issue that already tracks it, or file one issue titled `<Bug class> (found in review of #<pr>)`, listing each location with its claim, failure scenario and evidence, linking the pull request, with the `needs-triage` label the triage-labels doc maps. Then post one comment on the pull request starting `Filed Pre-existing Findings:`, one line per id with its issue link; a later filing skips the ids it lists. For a fixed point, file only if the user asks.

## Ticket checks

A Ticket check is one Quick Round on a Ticket branch against its Spec branch, and is not one of the Spec pull request's Rounds. Post it on the Spec pull request as a Ticket-check comment; if that pull request is not open yet, post it once it opens. A later check of the same Ticket, and the Spec pull request's Round 1, carry its open Findings as earlier Findings. Its Pre-existing Findings are filed with the Spec pull request's.

## Fixed point

A diff since a fixed point runs Round 1 only, posts no comment, and its report to the user is the end.
