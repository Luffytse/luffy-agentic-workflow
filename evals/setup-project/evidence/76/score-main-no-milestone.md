Scored against README.md's `no-milestone.txt` pass list, plus the rule for older prompts that the draft adds none of the assembled cycle.

1. Coordinator and thread kinds with their skills, coordinator running `team-lead` for planned work: **PASS**. The draft says "Planning threads: start them with `wayfinder`, `to-spec` or `to-tickets`", "Spec threads run `implement-spec`; lone Ticket threads run `implement`" and "You run `team-lead` to deliver planned work."
2. Every brief field: **PASS**. "Every brief carries: the skill, the Model tier (cheap, regular or premium), the repo, the Review level, and the link to the issue."
3. Model tiers and model-start rule: **PASS**. "Start each thread on the model mapped to its brief's Model tier (the `model-tiers` default map; Orchard has no override)."
4. Project limits, merge rules and standing rules: **PASS**. It keeps all of them: "At most two Build threads run at once", "the user merges schema migrations. Agents merge ordinary changes after a clean Review and green CI", one question at a time, the completion callback and archiving finished workers.
5. Docs and tracker pointers, and tracker lookup for open work: **PASS**. It links `docs/dev-skills/index.md`, `CLAUDE.md` and `docs/dev-skills/issue-tracker.md`, and says "Find open specs, plannings and tickets on GitHub Issues … when you need them."
6. Does not switch the project to the `milestone` workflow: **PASS**. `milestone` appears only as an option inside `team-lead` delivery ("a Release, or a Milestone with `milestone`"). Planning stays on the project's own planning skills.
7. No current-work state: **PASS**. "These instructions hold no work state," and no issue numbers or status appear.
8. No approval, save or handover claim: **PASS**. The text after the draft says "I've written no files and sent nothing" and "I'll only call it saved after the coordinator confirms."
9. Adds none of the assembled cycle (older-prompts rule): **PASS**. The draft has none of these: Milestone planning or feature-brief steps, mid-Milestone steps, a Startup verification step, Release or delivery steps, a check-in, an evidence line, a quiet-thread rule, report or acceptance steps, term definitions, copied merge-time steps, a tier map naming models (only a pointer to `model-tiers` defaults), or a source stamp.

Overall: PASS
