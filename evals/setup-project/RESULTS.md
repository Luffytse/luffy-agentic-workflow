# setup-project results

One entry per run of a `setup-project` case.

## Coordinator that cannot load the plugin (`no-plugin.txt`, `no-plugin-outside.txt`)

Change: Ticket #31 (`setup-project` asks the coordinator about its skill access and copies `team-lead/DELIVERY-LOOP.md`'s loop into the draft when it cannot load the plugin). Behaviour change. Commit fabdf36; main at 9e8bc1d (skills from a `git archive` of each); decision-level, regular tier; runs made by the coordinator, drafts kept in its scratchpad. Plugin version not bumped yet (merge-time step).

- Case check (premium, fresh subagent, before any run): both new cases keep (valid, fail on main for the right reason, needed). It found that the older prompts left the coordinator's skill access unstated, so "unanswered counts as cannot" was ambiguous; fixed by a fact line added to `milestone-rerun.txt` and `no-milestone.txt`.
- Branch, `no-plugin.txt`: PASS. The draft copies the five-step loop verbatim, has no instruction to run `milestone` or `team-lead` itself, keeps the two-thread limit, backend first and the migration gate, points at the Boundary record without its values, and claims no state, approval or handover.
- Branch, `no-plugin-outside.txt`: PASS. The loop verbatim plus thread kinds, brief fields, the model-start rule, limits and merge rules, and tracker lookup.
- Main, `no-plugin.txt`: FAIL as expected. A short Milestone form telling the coordinator to run `milestone` and `team-lead`; it adds only an improvised "tell the user which skill is missing and wait"; none of the five loop steps.
- Main, `no-plugin-outside.txt`: FAIL as expected. Full instructions plus an improvised "name the skill in each brief, don't load plugin skills"; no loop steps and no delivery path.
- Regression, branch, `milestone-rerun.txt` and `no-milestone.txt`: PASS. Neither draft gains the loop.

No regression guard is needed: main fails both new cases. Not exercised: exploration, a real grilling exchange, approval or save.
