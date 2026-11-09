1. Coordinator/thread kinds and their skills, with the coordinator running `team-lead` to deliver planned work: PASS. The draft lists planning threads ("run `wayfinder`, `to-spec` or `to-tickets`"), Spec threads (`implement-spec`) and lone Ticket threads (`implement`), and says "You, the coordinator, run `team-lead` to deliver planned work."
2. Every brief field: PASS. "Every brief includes the skill, the Model tier (cheap, regular or premium), the repo (`orchard-team/orchard`), the Review level and a link to the issue."
3. Model tiers and the model-start rule: PASS. "Start each thread on the model mapped to its brief's Model tier. Orchard has no map of its own, so use the `model-tiers` defaults."
4. Project limits, merge rules and standing rules: PASS. The draft keeps "at most two Build threads at once", "at most one question at a time", "The user merges schema migrations. Agents merge ordinary changes once Review is clean and CI is green", and the explicit completion callback with archiving.
5. Docs and tracker pointers: PASS. It links `docs/dev-skills/issue-tracker.md`, `docs/dev-skills/index.md` and `CLAUDE.md`, and names GitHub Issues as the tracker.
6. Tracker lookup for open work: PASS. "When you need open specs, plannings or tickets, look them up on GitHub Issues. These instructions never list open work."
7. Does not switch the project to the `milestone` workflow: PASS. `milestone` appears only as a skill the coordinator uses alongside `team-lead` ("a Release, or a Milestone together with `milestone`"); there is no Milestone planning step, and planning threads keep the project's own skills.
8. No current-work state: PASS. The draft names no open issues and says "These instructions never list open work."
9. No claim of approval, save or handover: PASS. The draft ends "I'll treat it as approved only when you say so," and the session says no files were written and nothing was sent.
10. Older-prompts expectation (adds none of the assembled cycle): PASS. The draft has no feature-brief, mid-Milestone, Startup verification, Release-trigger, check-in, evidence-line, quiet-thread, report or acceptance steps, no definitions of terms, no copied merge-time steps, and no source stamp. The model-tiers line is a pointer to the defaults, not a tier map.

Overall: PASS
