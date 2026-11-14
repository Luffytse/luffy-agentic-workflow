# Milestone report

The coordinator owns the report comment on the Milestone issue. Build it against the latest agreement, not the initial plan. Read the feature issues, their acceptance criteria and pull requests, each release issue's Triage batch summary and the `team-lead` audit trail. A closed issue alone does not prove a feature merged: read its pull request's merged state and account for every issue in a Spec or related-issue feature. An abandoned or obsolete feature is a gap unless the user agreed to its disposition. A feature with a parked Ticket is reported as parked, with that Ticket's blocker.

## Gather the evidence

Link each fact's source; name unknowns where a history or session record cannot be read. Collect these as they become readable during delivery, so an archived thread's lost history stays a named gap.

- **User messages.** Read them only to find the **unplanned step-ins**: the user noticing a problem or pushing a thread. Feature planning, the Milestone review, answering a parked feature's blocker and an action the Boundary record requires of the user are planned and get no row. An unreadable history makes the count a lower bound, and the report says so.
- **Time and tokens.** One line: wall time from delivery start to the report, the number of threads, and total tokens where the session records can be read (unknown otherwise, said plainly).
- **Versions.** One line: the Plugin version check's reading, any go-on the user gave after a mismatch, and an Environment check result where the repo's own docs give one.
- **Agent decisions.** Only merges to rules files (ADRs, the glossary, `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`), from the `Agent-merged rules:` line on merged pull request bodies, with file and merge link.

## Post and stop

Post one comment with the tracker doc's **Comment on an issue** operation. First line `<!-- milestone report -->`, then `## Milestone report — ready for user review`, the agreement source and report time. Then:

1. **Key points**, about one screen (about 200 words), so a reader of only this knows the outcome, what is asked of them and what is proposed next:
   - features merged and features parked, as counts;
   - what needs the user: the acceptance checks the Milestone issue names, and each parked issue with why and the user's choices for it (fix it now, move it to the next Milestone, or split it);
   - the unplanned step-ins as a count with causes;
   - the proposals for the next Milestone, one line each; proposals, not scope.
2. **Outcomes:** each feature and acceptance criterion with its outcome and evidence links; satisfied, unmet and unverified kept apart. Include regression or end-of-Milestone checks actually run and their limits. Invent no pass or acceptance.
3. **Parked and maintenance:** each parked feature or Ticket with its blocker; each maintenance issue left open, with its recorded reason.
4. **Unplanned step-ins:** each with time, source link and cause.
5. **Time and tokens, Versions, Agent decisions:** the lines above.

End with `Ready for the user's Milestone review; acceptance pending.`, leaving the Milestone open. Read the comment back before telling the user its link and stopping delivery. If the write or read-back fails, report it and retry at the next wake.

On re-entry, read existing report comments and compare the latest agreement and outcomes with their sources. Reuse the report for an unchanged review state: no duplicate comment or notification; a check-in while it waits has nothing to do. If the user sends a feature back or lifts a park, re-read the agreement and tracker, resume only the authorized work through `team-lead` (which arranges the check-in again), and post a new report when the gate holds again, linking the prior report and naming what changed. The user alone accepts the Milestone. When they accept it in words after the report, close the Milestone issue, with the tracker doc's **Close** operation and a comment naming where and when they accepted.
