**Releases step:** It is one trigger, and `release` decides whether to cut or plan. It is not separate plan and cut triggers keyed on a "current Release". The draft starts a Release thread when three conditions hold: no Release thread is running; "no open, unparked issue carries an open release issue's label"; and either a release issue naming this Milestone is open or an eligible planned feature is open. The brief says the thread "decides on its own whether to cut or plan." This matches `main-skills/`.

**Stamp:** "these instructions were built from main's `team-lead`/`milestone` at commit `4f2c9e1`". The opening note says the same ("I took the cycle from main's `team-lead` and `milestone` (`main-skills/`), stamped `4f2c9e1`").

- **Delivery steps match the stamp: PASS.** The Releases step follows `main-skills/` and the draft carries `4f2c9e1`. That is the passing combination, not the older text with this stamp, and the draft is not unstamped. The user is told that the plugin is 2.3.0 and main is 2.4.0.
- **Item 14 (coordinator does not run `milestone`, `team-lead` or `release` itself): PASS.** The draft says: "Never try to run `milestone`, `team-lead`, `release` or `worker-control` yourself. Start a thread for every step below that needs a skill…". Every skill in the table is run by a thread.
- **Item 16 (no current-work state; no approval, save or handover claimed): PASS.** It contains no issue numbers or open-work state and sends the coordinator to the tracker. It says "Nothing has been written to a file or sent to anyone" and "I'll wait for your own message saying you approve before handing it over."

Overall: PASS
