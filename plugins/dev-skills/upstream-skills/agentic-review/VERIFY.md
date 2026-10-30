# Verify

The Verify stage of [`agentic-review`](SKILL.md). Verifiers are brand-new subagents on the regular tier.

- **Quick and Standard:** one Verifier checks every candidate Finding of the Review.
- **Deep:** three Verifiers each check every candidate Finding, each with one stance (below), and their votes are combined by the rules at the end.

Every Verifier gets: all candidate Findings in the fixed format, each tagged with its Finder; the open Importants from earlier Rounds and Ticket checks, with their ids; the diff commands; the spec, the standards list and `REVIEW.md` (with its Always check lines); and the meaning of Important (`REVIEW.md`'s, or the default in [SKILL.md](SKILL.md#2-find-the-spec-and-standards-sources)).

## Verifier brief

"For each candidate Finding, open every cited file and line at the current head and check the claim against the code itself, not against names, comments or the Finder's wording. Follow the code path as far as it takes to be sure. Then make four calls, each with one line of reasoning:

1. **Real?** keep or drop. Drop it when the code does not do what the claim says, the problem cannot happen, or it is something `REVIEW.md` says to skip. When the problem is real but its stated failure scenario is wrong, correct the scenario instead of dropping. Keep a realistic rare path (an error handler, a race, a falsy zero, a regex that lost its anchor): rare is no reason to drop. A cleanup Finding is real when the cost it states holds. Judge an `(unsure)` candidate like any other. A Finding raised from a `REVIEW.md` Always check line is real when the code breaks that line as written. Fix the Locations list when the Finder missed or misplaced instances of the Bug class.
2. **Caused by this change?** yes, or Pre-existing when the same problem is in the code before the change (check `git show <base>:<file>`) and the change neither adds nor widens it.
3. **Important or Nit?** confirm or change the Finder's proposal, using the meaning of Important you were given. Not asked for Pre-existing Findings.
4. **For a Nit: fix or skip?** fix when it is cheap and clearly makes the code better; skip when it is taste, churn, or out of proportion to the change.

Then, for each open Important from earlier Rounds or Ticket checks, check the current code and say **fixed** (cite the line that fixes it), **still open** (cite the line that still has the problem), or **dismissed** (it was never real; say why).

To try something out (plant a line, run a check, test a commit), work in your own copy: `git archive <head> | tar -x -C <a new scratch directory>`, or a throwaway `git worktree`. Never run `git checkout`, `switch`, `stash` or `reset` in the shared tree, because an Implementer is working in it; leave it on its branch, clean.

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

An open Important from an earlier Round or Ticket check is closed as fixed, or dismissed, only when at least 2 of the 3 say so; otherwise it stays open.

## Gap sweep

On Deep, the gap sweep's Findings get a second Verify: three more brand-new Verifiers with the same brief, stances and vote rules, given only those Findings and the Findings the first Verify kept, to check none repeats one. There are no open Importants to re-check; the first Verify did that.
