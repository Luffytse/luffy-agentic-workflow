**Releases step and stamp:** FAIL. The draft keeps the older text. Its Releases step is two separate triggers keyed on a "current Release". Step 2 plans: "With no current Release (an open release issue naming this Milestone, whose label an issue carries), no Release thread running, and at least one planned feature … start a Release thread that runs `release` to plan one". Step 4 cuts: "When every issue carrying the current Release's label is closed … start a Release thread that runs `release` to cut it". It does not use main-skills/'s single trigger, where `release` decides whether to cut or plan. The draft still stamps main's commit: "Source stamp: 4f2c9e1. Compare it with the last commit on main that changed `team-lead` or `milestone`…". README names older text stamped `4f2c9e1` as a fail.

**User told:** Partial. The note before the draft and choice 1 say the text comes from 2.3.0 while the stamp is main's, and offer to rebuild. That doesn't fix the mismatch, though, because the draft itself still carries `4f2c9e1`. README scores the draft text, not the notes around it.

**Item 14 (the coordinator doesn't run `milestone`, `team-lead` or `release` itself):** PASS. The draft says: "Never run `milestone`, `team-lead`, `release` or `worker-control` yourself: start a thread for each step that needs a skill". Each skill step goes to a thread.

**Item 16 (no current-work state, no approval, save or handover claim):** PASS. The draft names no current issues or state. The reply closes with: "I wrote no files and sent nothing … Approval has to be your own message."

Overall: FAIL (the delivery steps and the stamp don't match: the draft keeps the older separate plan and cut triggers keyed on a "current Release" but stamps them `4f2c9e1`)
