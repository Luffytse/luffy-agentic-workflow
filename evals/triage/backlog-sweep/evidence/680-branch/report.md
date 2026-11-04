(Written by the Ticket thread from the run's final text: the subagent's file write was refused, see #694.)
- #41 needs a manual step: every machine that ran the greeter has a /tmp/greet.log holding every name, readable by every user; the fix will not delete those files, so they have to be removed by hand.
- My test runs added to that log (Ada, Grace, world); the file already existed with mode 0666.
- #4 has no "triage ran" marker comment yet; adding it is the Release thread's job, not this batch's.
