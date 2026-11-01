---
name: issue-absorption
description: Record and interpret issues absorbed by a Ticket. Use when publishing an absorbing Ticket, reading absorption records, or selecting absorbed issues for closing lines or closure.
user-invocable: false
---

# Issue absorption

This is a reference contract. Load it for the absorption decision, then continue the caller's workflow. Tracker reads, comments and closes use the project's configured tracker doc; this contract owns their meaning, not their commands.

## Write the agreement

- Read each source issue's body **and comments**. Put every requirement that must land with the fix into the Ticket's acceptance criteria, or into the Ticket that owns the file it touches.
- Name the issues the Ticket absorbs and link their briefs instead of copying them. Absorbed issues are linked sources, not parents: do not make the Ticket their sub-issue.
- For each source, put a separate `Closes #<n>` criterion in the Ticket's acceptance criteria. Once the Ticket exists, comment on each source: `Absorbed by #<ticket>; closes when it is completed.`
- Immediately before publication, re-read each absorbed issue's state and drop or note any already closed.

## Read the agreement

Read the source's comments and the absorbing Ticket's current state and close reason. The **latest** `Absorbed by` comment is authoritative: older records or criteria do not override it.

| Authoritative Ticket | Meaning for its source issues |
| --- | --- |
| Open | Waiting on this Ticket; keep the sources open. |
| Closed as completed | The fix completed; the sources may close with this Ticket. |
| Closed any other way (not planned, duplicate, abandoned) | Not fixed; the sources stay available to planning with their votes. They are neither waiting on the Ticket nor evidence of a failed completed fix. |

A later absorption record transfers this agreement to its named Ticket. Unrelated issues have no absorption agreement. Callers still own recurrence checks, planning verdicts, user approval and when to perform a close.

## Closing lines and closure

The pull request completing a Ticket carries a separate `Closes #<n>` line for each source it authoritatively absorbs. Include only sources of Tickets that the pull request actually completes; recheck the latest records when maintaining those lines. A dropped or never-landed Ticket cannot authorize closing its sources. Retain a source's line only when a Ticket the pull request completes is its authoritative absorber.

Before closing a source with a Ticket, recheck that the authoritative Ticket is closed as completed. Otherwise leave the source open and apply the state table. A source becoming eligible for closure does not bypass the caller's approval or recurrence policy.
