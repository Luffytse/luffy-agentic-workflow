**Shared steps at each wake.** Before acting I re-read the state: the Milestone issue #1, release issue #40 and its Order, and **Park** and **Count open blockers** for #30, #20 and #25. I also read the branches and each worker's state through `worker-control`. The worker's message is only a reason to read. Each wake below starts from `STATE.md`. There is no pause, no merge-time step and the end-of-delivery gate does not hold, so none of those steps apply. The check-in already exists because build workers were started earlier, so nothing about it changes.

---

## Event 1: `w30` says #30 is already fixed

1. **Read and check the evidence.** #30 has no branch or pull request. `worker-control` shows `w30` as ended. On main at `9f1c2ab`, `src/greet.sh` prints `usage: greet.sh hello <name>` from commit `4d5e6f7` (pull request #7), so the usage line is fixed. `README.md` still says `greet.sh helo`, but that is documentation, which is #25's job ("Document the hello command"), not the usage line. The verdict stands.
2. **Close #30 (not a planned feature, so this is mine to do).**
   - Action: close as completed.
   - Close reason: `Checked against main: already fixed. src/greet.sh on main prints "usage: greet.sh hello <name>" (commit 4d5e6f7, pull request #7, which closed no issue). Nothing is left to do here. README.md's "greet.sh helo" is documentation and is left to #25.`
3. **Slot.** `w30`'s slot is free. No message to `w30` is needed, since it has stopped.
4. **Start #25.** Closing #30 as completed clears #25's only blocker, so **Count open blockers** for #25 is 0. In #40's Order, #20 has a running worker and #25 is open, not parked and unblocked. With `w20` holding 1 of the 2 slots, one slot is free.
   - Start worker `w25` through `worker-control` on the model `model-tiers` (or the project's own map) gives for **regular**, since #25 has no Model tier line.
   - Brief: skill `implement`; issue #25 link; Milestone issue #1 link; tier regular; no Review level; what the project's instructions add. It must record the plugin load source and version it loaded, its permission and sandbox settings, and a session usage reference ("unknown" where it can't read one). It must also preserve the evidence `milestone`'s report gathers. Optional extra: "main's README.md still says `greet.sh helo`".
5. **Tracker write.** Comment on #25:
   ```
   <!-- team-lead start -->
   Worker: w25 (id as worker-control returned it). Skill: implement. Model tier: regular. Review level: none. Started: <UTC time>. Session: <reference>.
   ```

No message to the user.

---

## Event 2: `w20` says #20 is already fixed

1. **Read and check the evidence.** #20 has no branch or pull request. `w20` reads as ended. On main, `src/greet.sh` handles `--quiet` from commit `8a9b0c1` (pull request #8). The verdict holds.
2. **#20 is a planned feature, so I don't close it.** Closing it would change what the Milestone agreed, so it goes to the user as one question and #20 waits for the answer, with no worker started on it.
   - Tracker write: comment on #20:
     `Checked against main: already fixed? src/greet.sh on main handles --quiet (commit 8a9b0c1, pull request #8, which closed no issue). This is a planned feature of Milestone 1 (#1), so it is the user's call: may I close #20 as completed, naming 8a9b0c1 / PR #8, and count it as merged for the acceptance "both features merged"? #20 waits for your answer, and no worker starts on it.`
3. **Message to the user (one question):** "#20 'Add a `--quiet` flag' (Milestone 1 feature): worker `w20` found that main already handles `--quiet` (commit `8a9b0c1`, PR #8, which closed no issue). May I close #20 as completed and count PR #8 toward 'both features merged'? Link: #20. Nothing else waits on this."
4. **Slot.** `w20`'s slot is free. Nothing starts:
   - #30 still has `w30` running.
   - #20 waits for the user.
   - #25 is still blocked by #30.

No other writes, and no message to `w20` because it has stopped.

---

## Event 3: `w30` reports changed scope on #30 and waits

1. **Read and check the evidence.** `w30` reads as running and waiting, with no branch. On main, `src/greet.sh` prints `hello` (`4d5e6f7`, PR #7), and `README.md` still says `greet.sh helo`. The verdict holds.
2. **This is mine to decide.** #30 is a bug, not a planned feature. Narrowing it to the README changes neither the Milestone's goal ("a quieter greeter"), its acceptance ("both features merged") nor its exclusions. So I don't ask the user. I update the issue, then answer the worker.
   - Tracker write: edit #30's body. I read the whole body and write it back with only the scope changed: what remains is `README.md` saying `greet.sh helo`, which should say `greet.sh hello`. `src/greet.sh` is out of scope. At the end I add the line `Checked against main: the usage line in src/greet.sh already prints "hello" (commit 4d5e6f7, pull request #7); what remains is README.md, which still says "greet.sh helo".` Then I read the body back.
3. **Message to `w30`:** "#30 is updated to the narrowed scope: fix `greet.sh helo` → `greet.sh hello` in `README.md` only, and leave `src/greet.sh` alone (main already has it, `4d5e6f7` / PR #7). Go ahead and build that as `implement` says; your Closes line still names #30."
4. **Slots.** `w30` keeps its slot and goes on building. `w20` holds the other one. Nothing new starts, and #25 stays blocked by #30.

No message to the user.

