You are the coordinator running Milestone 1's delivery with `team-lead` (its whole folder is given to you). `STATE.md` is the state at this wake, as you would read it; take it as read through the tracker, the branches and `worker-control`. Do not run anything. Three events reach you, one at a time, each at its own wake, each starting from `STATE.md` with only the change the event names (not from the event before):

1. The hourly check-in fires at 11:00. No other change.
2. The user writes at 10:30: "Carried #20 and #25 over. Go on." One change to `STATE.md`: #20 and #25 are each also blocked by #35 "Pick a docs tool" (open, `needs-triage`, an enhancement the Milestone issue does not list).
3. The hourly check-in fires at 11:00. One change to `STATE.md`: only #25 was carried over. #20 still carries `release-m1-r1` (the `## Carried over` section lists only #25), and its build worker `w20` was never stopped: it is running, and its branch `t20` is pushed, with a commit at 10:50.

For each event, write what you do, in order: each tracker write (which issue, the action, and the text of any comment), each message to a worker or to the user, and each worker you start, with its skill, model tier and the full text of its brief.
