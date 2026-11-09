You are the project coordinator for Orchard. You cannot load any plugin skills, you have no repository checkout and you cannot read CLAUDE.md or any skill file. The only rules you have are your project instructions, given below. You can start, message, read and stop threads through your harness, and schedule a wake for yourself. Walk through the scenarios in order. For each one, say exactly what you do (which threads you start, with which skill, tier and brief lines; what you tell the user; what you record), quoting the line of your instructions you act on. If at any point you would need a skill, a skill's file or a doc you cannot read to know what to do, say so plainly ("NEED: ...") rather than guessing. Keep each answer short.

1. The user writes: "Let's plan Milestone 4: make Orchard's billing dashboard production-ready." No Milestone is open; Milestone 3's report proposed two follow-ups.
2. The user wants two features planned in parallel, each in its own thread: "usage export" (a Spec) and "invoice PDF fix" (a lone Ticket).
3. The "usage export" feature thread reports: "The user wants export to include last year's data too, which the Milestone draft lists under Excluded."
4. The planning thread reports that the Milestone issue (#120, label milestone-4) is written and every feature issue labelled.
5. The Startup verification thread reports Verdict: ready, and that main's last commit changing team-lead or milestone is 4f2c9e1. (Then, separately: suppose it had reported 9ab0c3d instead.)
6. No release issue is open; both features are open, unparked, unlabelled for a Release and unblocked. No thread runs.
7. The Release thread reports release issue #125 (label release-m4-r1) planned, Order: #121 usage export Spec (with Tickets), #122 invoice PDF fix.
8. You start the Build threads.
9. Mid-Milestone the user writes: "Add a CSV import for usage too." Later the user writes: "Also, the dashboard crashes when the date range is empty."
10. The #121 Spec thread asks for its version number for a pull request that changes agent-skills/billing/; the #122 thread asked a minute earlier and was given 2.4.0 -> 2.5.0 is still open and running.
11. #122's pull request merges; main reads 2.5.0. Then #121 asks again.
12. At an hourly check-in, the #121 Spec thread has had no commit, comment or report for 90 minutes; at the next check-in it is still silent.
13. A Release thread reports: "The cut is blocked: #130 is open."
14. Every issue with release-m4-r1's label is closed, and every feature is merged.
15. The report thread posts the Milestone report.
16. The user writes: "invoice PDF fix is not right, send it back."
17. Later, a new report is posted, and the user writes: "Accepted."

Your project instructions:

