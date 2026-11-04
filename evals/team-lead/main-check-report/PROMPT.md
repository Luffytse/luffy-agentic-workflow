You are the coordinator running Milestone 1's delivery with `team-lead` (its whole folder is given to you). `STATE.md` is the state at this wake, as you would read it; take it as read through the tracker, the branches and `worker-control`. Do not run anything. Three events reach you, one at a time, each at its own wake, each starting from `STATE.md` (not from the event before):

1. Worker `w30` reports on #30: "Check against main: already fixed. `src/greet.sh` on main prints `hello`, commit `4d5e6f7` (pull request #7). I made no branch and stopped."
2. Worker `w20` reports on #20: "Check against main: already fixed. `src/greet.sh` on main handles `--quiet`, commit `8a9b0c1` (pull request #8). I made no branch and stopped."
3. Worker `w30` reports on #30: "Check against main: changed scope. `src/greet.sh` on main prints `hello` (commit `4d5e6f7`, pull request #7), but `README.md` on main still says `greet.sh helo`. I am waiting for your answer before building."

For each event, write what you do, in order: each tracker write (which issue, the action, and the text of any comment or close reason), each message to a worker or to the user, and each worker you start or that frees its slot.
