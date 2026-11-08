# setup-project results

One entry per run of a `setup-project` case.

## Coordinator that cannot load the plugin (`no-plugin.txt`, `no-plugin-outside.txt`)

Change: Ticket #31 (`setup-project` asks the coordinator about its skill access and copies `team-lead/DELIVERY-LOOP.md`'s loop into the draft when it cannot load the plugin). Behaviour change; decision-level, regular tier.

- Case check (premium, fresh subagent, before any run): PENDING: verdict keep, fix or drop for each case.
- Branch run (setup-project and siblings from this branch): PENDING: both cases, draft kept locally, scored against the README's pass list.
- Baseline run (main's skills from a `git archive`): PENDING: both cases. Expected to fail: main has no loop file and the draft only points at `milestone` and `team-lead`.
- Regression runs of `milestone-rerun.txt` and `no-milestone.txt` on the branch: PENDING: the drafts must not gain the loop.
