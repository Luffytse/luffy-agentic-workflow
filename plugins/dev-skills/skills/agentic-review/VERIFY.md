# Verify

The Verify stage of [`agentic-review`](SKILL.md). Verifiers are brand-new subagents on the regular tier, save the premium-tier rebuttal Verifier ([Rebuttals](#rebuttals)).

- **Quick and Standard:** one Verifier checks every candidate Finding of the Review.
- **Deep:** three Verifiers each check every candidate Finding, each with one stance (below), and their votes are combined by the rules at the end.

Every Verifier gets: all candidate Findings in the fixed format, each tagged with its Finder; the open Importants from earlier Rounds and Ticket checks, with their ids, claims and locations, each location first brought to this Review's head as [ROUNDS.md](ROUNDS.md#rank) says (one in a file deleted since is given as recorded and marked deleted); the diff commands; the spec, the settled designs ([SKILL.md step 2](SKILL.md#2-find-the-spec-and-standards-sources)), the standards list and `REVIEW.md` (with its Always check lines); and the meaning of Important (`REVIEW.md`'s, or the default in [SKILL.md](SKILL.md#2-find-the-spec-and-standards-sources)).

## Verifier brief

"For each candidate Finding, open every cited file and line at the current head and check the claim against the code itself, not against names, comments or the Finder's wording. Follow the code path as far as it takes to be sure. Then make four calls, each with one line of reasoning:

1. **Real?** keep or drop. Drop it when the code does not do what the claim says, the problem cannot happen, or it is something `REVIEW.md` says to skip. Judge it against the settled designs you were given: drop a Finding that proposes an alternative a settled decision rejected. A Finding that the chosen design is imperfect is real only if the text overclaims (it says the design does something it does not) or contradicts itself or the repo, or if the Finding shows the decision breaks what the user agreed (inside a Milestone, the goal, an acceptance criterion or an exclusion); such a Finding is a design Finding. When the problem is real but its stated failure scenario is wrong, correct the scenario instead of dropping. Keep a realistic rare path (an error handler, a race, a falsy zero, a regex that lost its anchor): rare is no reason to drop. A cleanup Finding is real when the cost it states holds. Judge an `(unsure)` candidate like any other. A Finding raised from a `REVIEW.md` Always check line is real when the code breaks that line as written. Fix the Locations list when the Finder missed or misplaced instances of the Bug class. Every location is `file:line` (or `file:start-end`) counted within that file at this Review's head, as `grep -n` on the file gives it, never a line counted in the diff output or in a listing of several files you read; change a Location only when the Finder's line is wrong in the file itself.
2. **Caused by this change?** yes, or Pre-existing when the same problem is in the code before the change (check `git show <base>:<file>`) and the change neither adds nor widens it.
3. **Important or Nit?** confirm or change the Finder's proposal, using the meaning of Important you were given. Not asked for Pre-existing Findings.
4. **For a Nit: fix or skip?** fix when it is cheap and clearly makes the code better; skip when it is taste, churn, or out of proportion to the change.

When a call drops a Finding, or marks a Nit skip, name in its line the `file:line` the reason rests on (a guard elsewhere, say), if any: the dismissal is recorded with them.

Then, for each open Important from earlier Rounds or Ticket checks, find its code at the current head by its claim, not by line number alone: the locations given are already brought to this head, but a fix may have moved the code, and a location marked deleted means the file is gone, so look for where its code went. Check that code and say **fixed** (cite the line that fixes it), **partly fixed** (name each fixed location, citing the line that fixes it, and the locations still open), **still open** (cite the line that still has the problem), or **dismissed** (it was never real; say why, naming the `file:line` the reason rests on, if any).

Read the branch only through commands that do not touch the working tree: `git -C <path> show`, `diff`, `log` or `rev-parse` against a commit, or a `git archive <head>` copy. To try something out (plant a line, run a check, test a commit), work in your own copy: `git archive <head> | tar -x -C <a new scratch directory>`, or a throwaway `git worktree`. Never run `git checkout` (a branch or `<sha>`), `git switch` (`--detach` too), `stash` or `reset` in the shared tree, because an Implementer is working in it and each of them moves it; leave it on its branch, clean.

Answer per Finding: its title, the four calls with their reasons, and the corrected Locations, plus the corrected failure scenario when you corrected one. Under 600 words in all. Your final message is the report itself, as plain text. Do not end with any messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for."

## Deep: three stances

Add one stance to the brief for each of the three Verifiers:

- **Tracer:** "Follow the code path from an entry point to the cited line and show, with a concrete input or sequence, that the Finding's failure scenario happens. If you cannot construct one, vote drop unless you can say why the problem is real anyway."
- **Skeptic:** "Argue that each Finding is a false positive: look for the guard, caller contract, type or test that makes it impossible. Say keep only when your argument fails."
- **Spec checker:** "Judge each Finding against the spec, the ADRs, the glossary and the tests: is the behaviour actually wrong by what this project says it should do?"

## Combining Deep votes

Treat each call separately:

1. A Finding is **kept** only when at least 2 of the 3 Verifiers say it is real. This holds for every Finder, the security Finder included.
2. The Verifiers who said it is real decide the other calls by majority.
3. When those voters tie, the more cautious value wins: caused by this change over Pre-existing, Important over Nit, "fix" over "skip".

An open Important from an earlier Round or Ticket check is closed as fixed, or dismissed, only when at least 2 of the 3 say so, and loses a location as fixed only when 2 of the 3 call that location fixed; otherwise it stays open.

## Gap sweep

On Deep, the gap sweep's Findings get a second Verify: three more brand-new Verifiers with the same brief, stances and vote rules, given only those Findings and the Findings the first Verify kept, to check none repeats one. There are no open Importants to re-check; the first Verify did that.

## Rebuttals

Inside a Milestone, the owner of the code may rebut an open Important instead of fixing it ([ROUNDS.md](ROUNDS.md#rebuttals-inside-a-milestone)). Each rebuttal goes to one brand-new **rebuttal Verifier** on the **premium** tier, at every depth, never to a Verifier that judged the Finding before. It gets: the head to judge at (the head of the Review whose report the rebuttal answers, whose comment records the decision), the Finding (its id, Severity, Bug class, locations brought to that head as [ROUNDS.md](ROUNDS.md#rank) says, claim, failure scenario and evidence, and the Verifier's still-open line when it has one), the rebuttal, the diff commands, the spec, the settled designs ([SKILL.md step 2](SKILL.md#2-find-the-spec-and-standards-sources)), the standards list and `REVIEW.md`, and the meaning of Important. Its call is final.

### Rebuttal Verifier brief

"You decide one rebuttal. A review kept the Finding below as Important, and the owner of the code says it is wrong and has not fixed it. If you dismiss it, it is not fixed before merge, so dismiss it only on evidence you checked yourself. Open every file and line the Finding and the rebuttal cite at the head given, and check the claim and the rebuttal against the code itself, not against names, comments or either side's wording. Rerun any command or test the rebuttal quotes in your own copy, and judge what its output shows, not what the rebuttal says it shows: a passing test proves only the case it runs. Follow the code path as far as it takes to be sure. Then make one call. **Dismiss** when the rebuttal shows the claim does not hold: the code does not do what the claim says, or the failure scenario cannot happen at this head (a guard, a caller contract, a type, or a run that shows the right result on the Finding's own input). **Uphold** when the claim still holds at any one of its locations, when the rebuttal argues only that the problem is rare, small, out of scope or tested elsewhere, when it disputes only the failure scenario while the problem stays real, or when you are unsure. Answer: the Finding's id; Dismiss or Uphold; one line of reasoning; for Dismiss, every `file:line` your reason rests on; for Uphold, every `file:line` that still has the problem, and a corrected failure scenario if the Finding's was wrong. Every location is `file:line` (or `file:start-end`) counted within that file at the head given, as `grep -n` on the file gives it. Under 300 words. Read the branch only through commands that do not touch the working tree (`git -C <path> show`, `diff`, `log` or `rev-parse` against a commit), and try things out only in your own copy (`git archive <head> | tar -x -C <a new scratch directory>`, or a throwaway `git worktree`); never run `git checkout`, `switch`, `stash` or `reset` in the shared tree. Your final message is the report itself, as plain text. Do not end with any messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for."
