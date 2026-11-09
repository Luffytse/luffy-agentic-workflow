1. FAIL. The draft has no step for planning a Milestone. Its loop starts at "Once Milestone planning has settled". So there is no planning thread running `milestone`, no offer of set-aside work first, and no rule that the Milestone issue is written last.
2. FAIL. There are no feature planning briefs. Nothing names the planning skills (`grill-with-docs`/`grilling`, `to-spec`, `to-tickets`), the Milestone number, the planning thread's link, the acceptance-criteria issue or how a scope change is reported.
3. FAIL. Nothing covers a feature the user plans mid-Milestone or a bug the user raises then; no `triage` thread is mentioned.
4. PASS. Step 1 starts a Startup verification thread and says: "Start no Build thread until the result on the Milestone issue reads `Verdict: ready`, or the user says to go on."
5. FAIL. It uses separate plan and cut triggers keyed on a current Release: step 2 says "With no current Release … start a Release thread that runs `release` to plan one" and step 4 starts one "to cut it". The guide fails this pattern by name. The draft also has no rule for a Release thread that reports a blocked cut or nothing planned (tell the user once, don't start another).
6. FAIL. The draft never arranges the check-in or ends it before the report. The gap appears only in the session's note: "says nothing about setting one up".
7. FAIL. Build briefs carry "the skill, the issue link, the Milestone issue link and the Model tier". There is no evidence line (load source and version, permission and sandbox settings, session usage) and no rule to follow main's copy of each skill per `CLAUDE.md`.
8. FAIL. There is no rule for a thread that goes quiet or for it keeping its slot.
9. FAIL. Step 5 starts the report "When every feature is merged or parked", not once the last Release cut has ended. It then just says "stop for the user's Milestone review", with nothing on acceptance closing the Milestone issue or on a feature sent back (re-entering delivery, check-in arranged again, new report linking the earlier one).
10. FAIL. There is no tier map, only "the worker tool's default model when they give none". Tiers are not named per thread kind, chores included. The map appears only in the note ("cheap = <model>, regular = <model>, premium = <model>").
11. FAIL. The draft only points to the steps: "follow CLAUDE.md's 'Version hand-out' and 'Re-read after a skill merge'". It doesn't copy who gives the number, how it is raised, the one-out-at-a-time rule or what the re-read covers, and the coordinator cannot be assumed to read `CLAUDE.md`. Only "Start no further thread until the re-read is done" is carried.
12. FAIL. "parked", "Order", "order rule" and report re-entry are used but never defined.
13. FAIL. The draft carries `4f2c9e1`, but only as a provenance note. The Startup verification step never compares it with main's or tells the user once to re-run `setup-project` when it has moved.
14. PASS. The draft never tells the coordinator to run `milestone`, `team-lead` or `release` itself: "Start a thread for each step below that names a skill, and never do that step yourself."
15. PASS. It keeps "at most two Build threads at once", "start the backend one first" and "the user merges any pull request that contains a schema migration", and it points to the Boundary record at `docs/dev-skills/boundaries.md`.
16. PASS. It holds no current-work state and claims no save: "Once you approve the full text in your own message, I'll send exactly that text…"

Overall: FAIL (items 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13)
