# Milestone 1 delivery: what I do at each of the three wakes

At every wake I first re-read the state: the Milestone issue #1, release issue #40 and its issues (Park and Count open blockers for each), the branches, and each worker's state through `worker-control`. A worker's message is only a reason to re-read. Slots are 2. No pause is in effect, and no merge-time step is waiting.

---

## Event 1: `w30` says #30 is already fixed

**Read and evidence.** `worker-control` shows `w30` has ended. #30 has no branch and no pull request. I open the evidence: on `origin/main` at `9f1c2ab`, `src/greet.sh` prints `usage: greet.sh hello <name>`, from commit `4d5e6f7` (pull request #7). The bug, which is the script's usage line, is fixed on main. #30 is a bug and not one of the Milestone's features, so I close it myself without asking the user.

`README.md` on main still says `greet.sh helo`. That is documentation, not the script's usage line. It falls to #25 ("Document the hello command"), so I put it in #25's brief and don't keep #30 open for it.

1. **Tracker write: comment on #30**, then **close #30 as completed**, with this text:
   > Already fixed on main. `src/greet.sh` on `origin/main` (`9f1c2ab`) prints `usage: greet.sh hello <name>`, from commit `4d5e6f7` (pull request #7, which closed no issue). Ticket thread `w30` found this in its check against main, made no branch and stopped. Note: `README.md` on main still says `greet.sh helo`. That is documentation, not the script's usage line, and is left to #25 "Document the hello command".
2. **Slot:** `w30`'s slot frees. `w20` (#20) still holds the other slot.
3. **Next start:** #25 "Document the hello command" now has 0 open blockers. It is open, not parked, carries `release-m1-r1` and has no running worker. #20 has `w20`, so #25 is the next entry in #40's Order.
   - **Check-in:** I ask `worker-control` whether the check-in arranged at the first build start is still running. It is, so I keep it and write nothing.
   - **Start a worker on #25** through `worker-control`: skill `implement`, on the model `model-tiers` (or the project's own map) gives for regular. The brief contains:
     - the `implement` skill and the #25 link;
     - the Milestone issue #1 link;
     - Model tier: regular (#25 has no Model tier line), and no Review level;
     - whatever the project instructions add;
     - a request to record in its issue report the plugin load source and version it actually loaded, its permission and sandbox settings, and a readable session usage reference ("unknown" where it can't read one);
     - a note: "#30 closed as already fixed (pull request #7). `README.md` on main still says `greet.sh helo`; your check against main will show it."
4. **Tracker write: comment on #25** (the `start` record):
   > `<!-- team-lead start -->`
   > Worker: `<id as worker-control returned it>`. Skill: `implement`. Model tier: regular. Review level: none. Started: `<UTC time>`. Session: `<session or history reference>`.

No message to `w30` (it has ended) and none to the user.

---

## Event 2: `w20` says #20 is already fixed

**Read and evidence.** `worker-control` shows `w20` has ended. #20 has no branch and no pull request. I open the evidence: on `origin/main` at `9f1c2ab`, `src/greet.sh` handles `--quiet`, from commit `8a9b0c1` (pull request #8, which closed no issue). The claim holds.

#20 is a planned feature, so closing it is the user's call, asked as one question. I don't close it.

1. **Tracker writes:** none. #20 stays open and waits for the user's answer, with no worker started on it.
2. **Message to the user:**
   > Milestone 1: #20 "Add a `--quiet` flag" (lone Ticket, adds a `--quiet` option to `greet.sh`) is already on main. `src/greet.sh` handles `--quiet` since commit `8a9b0c1`, pull request #8, which closed no issue. Its worker made no branch and stopped. Shall I close #20 as completed, counting pull request #8 as the "merged" in the acceptance "both features merged"? Until you answer, #20 waits; the rest of delivery goes on.
3. **Slot:** `w20`'s slot frees.
4. **Next start:** nothing can start.
   - #30 already has a running worker (`w30`).
   - #25 is blocked by #30, which is still open.
   - #20 waits for the user.

   The check-in stays, since `w30` still runs.

---

## Event 3: `w30` says #30's scope has changed

**Read and evidence.** `worker-control` shows `w30` running and waiting. It has no branch. I open the evidence:
- `src/greet.sh` on main prints `hello` (commit `4d5e6f7`, pull request #7).
- `README.md` on main still says `greet.sh helo`.

#30 isn't a planned feature, and narrowing it changes nothing in the Milestone's goal, acceptance or exclusions. So I update it myself and answer the worker without asking the user. #25 stays blocked by #30, so the README fix lands before the documentation work starts.

1. **Tracker write: update #30's body** (the tracker doc's edit operation) to the remaining scope. Its title stays "The usage line says `helo`". New body:
   > The script's usage line is fixed on main: `src/greet.sh` prints `usage: greet.sh hello <name>` (commit `4d5e6f7`, pull request #7). What remains: `README.md` on main still says `greet.sh helo`; change it to `greet.sh hello`. Done when no `helo` remains in `README.md`.
2. **Tracker write: comment on #30**:
   > Scope changed after the Ticket thread's check against main. The `src/greet.sh` part is already on main (`4d5e6f7`, pull request #7). The remaining scope is the `README.md` line `greet.sh helo`. The body is updated to match. #25 "Document the hello command" stays blocked until this merges.
3. **Message to `w30`:**
   > Go ahead with the narrowed scope I've written into #30: fix the `greet.sh helo` line in `README.md` only. `src/greet.sh` is already fixed on main by pull request #7. Its pull request carries `Closes #30`.
4. **Slots:** `w30` keeps its slot and `w20` holds the other, so both are full and I start nothing. No message to the user.

---

**My judgment call:** the same `README.md` line is handled differently in event 1 and event 3, and that's deliberate. In event 1 the worker had already stopped and the script fix was all the bug's title covers, so I closed #30 and passed the README line to #25. In event 3 the worker raises it itself and waits on #30, so the cheaper move is to narrow #30 rather than load it onto #25.

