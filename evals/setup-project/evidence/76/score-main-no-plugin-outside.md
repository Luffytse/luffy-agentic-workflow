1. FAIL: There is no planning-thread step in the draft. The only mention is a session note under "Gaps": "no confirmed thread kind runs `milestone`'s planning". Nothing offers the set-aside work first or writes the Milestone issue last.
2. FAIL: There are no feature planning briefs. Nothing names the skills a feature thread runs, carries the Milestone number and planning-thread link, ends with an issue holding acceptance criteria, or reports a scope change.
3. FAIL: Nothing covers a feature the user plans mid-Milestone or a bug the user raises then; there is no `triage` thread for bugs.
4. PASS: Step 1 starts a Startup verification thread and says "Start no Build thread until the result on the Milestone issue reads `Verdict: ready`, or the user says to go on."
5. FAIL: Steps 2 and 4 are separate plan and cut triggers keyed on a "current Release" ("With no current Release … start a Release thread that runs `release` to plan one" / "… to cut it"). The guide fails exactly that form. The draft also has no "tell the user once" rule for a blocked cut.
6. FAIL: The draft has no check-in step. It appears only in a note: "No check-in timing. The loop has no check-in step."
7. FAIL: Build briefs carry no evidence line (load source and version, permission and sandbox settings, session usage reference). They also don't carry the `CLAUDE.md` rule to follow main's copy of each skill.
8. FAIL: Nothing says what to do with a thread that goes quiet, or that it still holds its slot.
9. FAIL: The report starts "When every feature is merged or parked", not once the last Release cut has ended. Nothing covers acceptance closing the Milestone issue, or a feature sent back re-entering delivery with the check-in arranged again and a new report linking the earlier one.
10. FAIL: There is no tier map; the draft falls back to "the worker tool's default model" when no map is given. Chore threads and their tiers are not named.
11. FAIL: The merge-time steps are not copied. The draft says only "take the coordinator's steps in [CLAUDE.md](CLAUDE.md) (the version hand-out and the re-read after a skill merge) exactly as it says". That leaves out who gives the number, how it is raised, one out at a time, and the re-read before the next start.
12. FAIL: The draft uses "parked", "Order" and "the Milestone's order rule" without defining them, and gives no meaning for report re-entry.
13. FAIL: `4f2c9e1` appears only in the closing note ("Where the loop came from"), not in the draft. Startup verification has no compare-with-main step and no "re-run `setup-project`" message to the user.
14. PASS: The draft says "Start a thread for each step below that names a skill, and never do that step yourself." It never tells the coordinator to run `milestone`, `team-lead` or `release`.
15. PASS: The full instructions are kept: thread kinds and their skills, "Every brief carries the skill, the Model tier …, the repo …, the Review level and the issue link", the model-start rule, "At most two Build threads", the migration and ordinary merge rules, and "look that up on the tracker each time you need it".
16. PASS: The draft says "They hold no state of the work". The session's reply ends "I've written no files and sent nothing" and waits for approval.

Overall: FAIL (items 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13)
