**Blind run score**

The draft in INSTRUCTIONS.md is main's five-step-loop draft. It has no stamp, no planning steps and no defined terms, so this run works as the baseline, not a branch draft.

1. **FAIL.** The user asks for Milestone 4. The draft has no step for planning a Milestone: no planning thread running `milestone`, and no "offer the set-aside work first" (the session asked for both with NEED). Gap: no planning start.
2. **FAIL.** Two features planned in parallel. The draft's planning threads run `wayfinder`/`to-spec`/`to-tickets`. It has no `grill-with-docs`/`grilling` first, no skill for a lone Ticket (NEED), no Milestone number or planning-thread link in the brief, and no "end with an issue holding acceptance criteria". Gap: feature planning briefs.
3. **FAIL.** A feature thread reports a scope change. `milestone` sends it to the planning thread, which keeps the draft. The session sent it to the user instead and asked for the Boundary record. Gap: scope change reported to the planning thread.
4. **PASS.** Planning settles. Loop step 1 starts the Startup verification thread, as `milestone` gives. The NEED about which agent runs `worker-control`'s check belongs to the thread that runs `milestone`, so it did not block the action. The NEED about "Review level" is a draft gap, not a coverage item: `team-lead` puts one in only when the issue or user names one.
5. **FAIL.** Startup verification. The draft carries no stamp and no compare step, so with the stamp moved (9ab0c3d) the session cannot tell the user once to re-run `setup-project`. It treated both hashes the same. Gap: coverage item 13.
6. **PASS.** First Release. The session started a Release thread with `release` to plan one, which is what `team-lead`'s Releases rule gives for this state. Its brief left out the release doc and the last cut release issue, a minor gap.
7. **FAIL.** The Release thread reports #125. The session needed the meaning of "order rule" (NEED), which coverage item 12 says the draft must carry.
8. **FAIL.** Build threads start. The thread kinds were right (`implement-spec`, `implement`), but the session arranged no check-in before the first build start, the briefs lack `team-lead`'s evidence line and the main's-copy rule, and the slot count depended on the undefined order rule. Gaps: coverage items 6, 7 and 12.
9. **FAIL.** Mid-Milestone feature and bug. The draft has no step for either (NEED). The skills give: plan the feature with the user, then a thread running `milestone` adds it; a `triage` thread files the bug. Gap: coverage item 3.
10. **FAIL.** Version request while another is out. The session needed `CLAUDE.md`'s hand-out steps (NEED). The draft points to them but does not copy them. Gap: coverage item 11.
11. **FAIL.** The merge and the re-read. Same gap: the re-read and the next number are unknown without `CLAUDE.md`.
12. **FAIL.** Quiet thread. `team-lead`'s rule is to nudge once, then stop it, read the stop back and replace it, with the slot held while it runs. The session messaged the thread, then only told the user. Gap: coverage item 8.
13. **FAIL.** Blocked cut. `team-lead`'s rule is to tell the user once, post a `wait` record and start no Release thread again until the state changes or the user writes. The session guessed at building #130 or needed `release` (NEED). Gap: blocked-cut handling in coverage item 5.
14. **FAIL.** Last Release's issues all closed. The session started the cut and the report together. The skills give the cut first, then the end of the check-in, then the report only after the cut has ended. Gaps: coverage items 6 and 9.
15. **PASS.** Report posted. The session stops for the user's review, tells the user with the link and starts nothing, as `milestone` gives.
16. **FAIL.** The user sends a feature back. The draft has no step, and "report written" blocks step 5 from running again (NEED). The skills give: back into delivery, arrange the check-in again, write a new report that links the earlier one. Gap: report re-entry.
17. **FAIL.** The user accepts. The session asked whether to close #120. Coverage item 9 says a thread closes the Milestone issue. Gap: acceptance step.

Fixture and skill gaps, not draft failures: the case gives no tier-to-model map, and no Review level values (scenarios 2, 4 and 6).

Overall: FAIL (scenarios 1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17)

The README expects the baseline to fail at the latest at Startup verification with the stamp moved. It failed earlier, from scenario 1.
