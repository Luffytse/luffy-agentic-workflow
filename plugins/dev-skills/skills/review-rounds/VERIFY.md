# Verify

The Verify step of [`review-rounds`](SKILL.md). One brand-new Verifier, on the regular tier (premium at Deep), checks every candidate of the Round.

The Verifier gets: every candidate in the Finding format, tagged with its Finder; every open Finding from earlier Rounds and Ticket checks (id, claim, locations as recorded) and any dispute of it; the diff command and commit list; the spec and the design answers; the meaning of Important and the Skip list; and an Always check line only for a candidate raised from it. Paste in the brief and the copy rule from [FINDERS.md](FINDERS.md). On a Round that is the Verifier alone, give it only the disputed Findings and their disputes.

Brief: "You decide which Findings are real. For each candidate, open every cited line at the current head and check the claim against the code itself, not against names, comments or the Finder's wording. Keep only what you have confirmed yourself: the line says what the claim says, and for a claim about behaviour, a run or a failing test shows it where one can be made. Then make four calls, each with one line of reasoning:

1. **Real?** keep or drop. Drop it when the code does not do what the claim says, the problem cannot happen, the Skip list names it, or it proposes an alternative a design answer rejected. When the problem is real but its failure scenario is wrong, correct the scenario. A realistic rare path (an error handler, a race, a falsy zero) is no reason to drop. A Finding raised from an Always check line is real when the code breaks that line as written. Fix the Locations when the Finder missed or misplaced one: each is `file:line` counted within that file at this head, as `grep -n` gives it.
2. **Caused by this change?** yes, or Pre-existing when the same problem is in the code before the change (`git show <base>:<file>`) and the change neither adds nor widens it.
3. **Important or Nit?** by the meaning of Important you were given. Not asked for Pre-existing.
4. **For a Nit: fix or skip?** fix when cheap and clearly better; skip when it is taste or churn.

When you drop a Finding or skip a Nit, name the `file:line` your reason rests on, if any.

For each earlier open Finding, find its code at this head by its file and claim, not by its old line number, and say **fixed** (cite the line that fixes it), **still open** (cite the line that still has it) or **dismissed** (it was never real; say why, with the `file:line` it rests on). When the owner disputed it, judge the dispute on evidence you checked yourself: rerun its command in your own copy and judge what the output shows. Dismiss only when that evidence shows the claim does not hold; when the dispute argues only that the problem is rare, small or out of scope, or you are unsure, it stays open.

Answer per Finding: its title or id, the calls with their reasons, and the corrected Locations and failure scenario where you changed them. Under 600 words in all. Your final message is the report itself, as plain text: end with no messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for."
