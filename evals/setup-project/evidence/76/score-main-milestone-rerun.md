**Scoring: OUTPUT.md against README.md's pass list for milestone-rerun.txt**

1. **Skills, pointers, limits:** PASS. The draft says "Run `milestone` for the Milestone and `team-lead` for its delivery" and links docs/dev-skills/index.md, CLAUDE.md and the tracker doc. It keeps "at most two Build threads at once" and "start the backend one first".
2. **Project rules kept:** PASS. It keeps all four rules: "The user merges schema migrations.", "send an explicit completion callback", "Archive each worker once it has finished." and "After every merge, pull main and reload any changed skills." The draft has no version hand-out or re-read rule, and no draft line says a skill states one. That is consistent with the user's confirmed additions list.
3. **Shared rules left out:** PASS. The diff removes the thread-kind/skill line, the brief fields, the model-start rule, Release grouping, the check-in/nudge/stop/takeover line and the retro line. None of them come back in the new text.
4. **Boundary record:** PASS. The draft says "Boundaries, the check-in interval and the budget are in the Boundary record" and links boundaries.md. It does not copy the 45 minutes, the 100 credits or the deploy approval rule.
5. **No work state; diff and full text:** PASS. The full text has no #7, #31 or #32; "-Current Milestone is #7; build #31 next; #32 is blocked." shows up only as a removed line in the diff. The reply gives both the full replacement and the diff.
6. **Unsaved draft:** PASS. The reply ends "Please approve the full text above… Once you approve, I'll send exactly that text to the coordinator to save." It claims no write, save or handover.
7. **Older-prompts expectation (none of the assembled cycle added):** PASS. The draft has none of the assembled cycle: no planning, feature-brief or mid-Milestone steps, no Startup verification, no delivery or Release steps, no check-in, no evidence line, no quiet-thread rule, no report or acceptance steps, no definitions, no copied merge-time steps, no tier map and no stamp. The reply says so: "No delivery loop is included, because the coordinator reported that it can load the skills."

Overall: PASS
