You are the Spec thread for the Spec in `SPEC.md`, following `implement-spec` (and, where it sends you, `implement` and `team-lead`). Do not run anything. For each scenario below, write out what you do, step by step, and what you never do:

1. **Mixed-agent siblings.** First entry: nothing is built yet; a coordinator runs.
2. **Closed parent, open child.** The Spec pull request merged with only 41 landed; the Spec issue is closed; 42 and 43 are open, with no squash commit on main.
3. **Same-agent Spec.** As scenario 1, but 42 carries no agent label.
4. **Repeated entry after a child landed.** You re-enter mid-build: the pushed Spec branch holds 41's squash commit and a commit Codex pushed for 42, and the draft Spec pull request has a Ticket-check comment on 42 from Codex. Variant 4b: 42 has not landed and your Continuation handoff is already on it; say what you do when the coordinator reads its worker as running, and when it reads it as ended without landing. Variant 4c: you re-enter after scenario 5 left an incomplete handoff on 42.
7. **Waiting and waking.** In scenario 1, 41 has landed and you have nothing left to build until 42 lands: say where you end, what wakes you and how. Your push of 41's squash commit is rejected because Codex pushed first: say what you do.
5. **No authorized dispatch.** As scenario 1, but the coordinator replies that it cannot start Codex and no one has confirmed who else may own 42.

Then answer as the Codex worker: (6) you are a Codex thread handed 42 alone through `implement`: say where step 1 sends you, what you build and land, the comment you leave on 42 (and what it carries), whom you report to, and where you stop.
