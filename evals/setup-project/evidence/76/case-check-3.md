I read every file in the folder. My verdicts: **keep** `no-plugin.txt`, `no-plugin-outside.txt` and the older-prompts expectation, and **fix** the Blind run. One pass item may also pass on main; it doesn't change any verdict.

## Verdicts

### `no-plugin.txt` (inside a Milestone): keep
- **Valid:** The prompt gives every fact the coverage list needs: a coordinator with built-ins only, Claude Code, no custom tier map, the quoted `CLAUDE.md` steps, the stamp `4f2c9e1`, and the plugin at main's version. Items 1–16 match what the branch's `setup-project` coverage list gives, read with the branch's `team-lead` (the Releases rule, Slots, Build order, Kind, evidence line, check-in and End of delivery), `milestone` (Planning step 3, Adding a feature mid-Milestone, Startup verification) and `reporting.md` (re-entry). Item 10's escape ("named to the user as unfilled") covers the `release` and `triage` thread tiers, which the given folders don't state.
- **Fails on main for the right reason:** Main's `setup-project` copies `DELIVERY-LOOP.md` verbatim and adds nothing of its own. The loop has no planning, check-in, evidence line, quiet-thread rule, acceptance or send-back steps, term definitions or stamp. Inside a Milestone, main writes a tier map only when the user overrides the default. Its separate plan and cut triggers are the form item 5 names as failing. All of these come from the rule the PR changes.
- **Needed:** No other case has a coordinator that cannot load the skills inside a Milestone. Item 15 and the inside-a-Milestone tier-map rule are tested only here.

### `no-plugin-outside.txt` (no open Milestone agreement): keep
- **Valid:** Same as above. Item 15's "full instructions" matches the branch's "Outside a Milestone, keep the full instructions… without the line that has it run `team-lead`". With no custom map, item 10's tier map follows the coverage item's "always written (`model-tiers`' map for its harness…)".
- **Fails on main for the right reason:** Main's "If the user has no map yet… draft the rule without the map" fails item 10, and the verbatim loop fails the rest as above.
- **Needed:** It is the only case for this setup outside a Milestone.

### Older-prompts expectation (`milestone-rerun.txt`, `no-milestone.txt`): keep, as a regression guard
- **Valid:** Both prompts say the coordinator can load the skills. The branch's "Where the coordinator can load them, add none of this" gives exactly the "adds nothing" list.
- **No conflict with the older pass lists:**
  - The carve-out ("What each older case's own pass list requires is not counted against it") covers the existing text's version and re-read lines, `no-milestone.txt`'s planning-thread kinds, and the `team-lead` pointer.
  - The tier-map clause matches both skill versions' "draft the rule without the map".
- **Fails on main:** The fail-on-main question is waived. Main's "add nothing for it" passes too, so this is correctly recorded as a regression guard. The expectation changed because the rule changed (the delivery loop became the assembled cycle).
- **Needed:** No other case guards that line.

### Blind run: fix
**Validity problem:** The scorer gets only the branch's `milestone` and `team-lead` folders. It is told to pass a scenario when the action is "what those skills give". But three scenarios have expected actions that only the branch's `setup-project` coverage list gives:
- **Startup verification, stamp moved:** comparing the stamp and telling the user once to re-run `setup-project`. `milestone`'s Startup verification has no stamp.
- **The user raises a bug:** a `triage` thread files it. Neither skill mentions this.
- **The user accepts:** a thread closes the Milestone issue. `milestone` says only that acceptance is the user's and the report leaves the issue open.

So a correct session can be failed, or a wrong one passed, depending on how the scorer reads the gap.

**Exact change.** Replace

> A scorer, given the draft and the branch's `milestone` and `team-lead` folders, marks each scenario pass when the session's action is what those skills give for that point

with

> A scorer, given the draft and the branch's `setup-project`, `milestone` and `team-lead` folders, marks each scenario pass when the session's action is what those skills give for that point (for the stamp moving at Startup verification, a bug the user raises and the user's acceptance, what `setup-project`'s coverage list gives)

**Same section, baseline sentence.** The prediction "expected to fail at the latest at the first scenario (its loop has no planning step)" could be wrong. Main's loop does say "Once Milestone planning has settled", so a session could guess "start a thread running `milestone`" and pass scenario 1. Replace it with:

> expected to fail at the latest at Startup verification with the stamp moved (main's draft has no stamp)

That failure is certain.

## Pass items the branch's skill text does not give
None. Items 1–16 each trace to the branch's coverage list or to the `team-lead`, `milestone` and `reporting.md` text it points to. Item 9's "on acceptance a thread closes the Milestone issue" comes only from `setup-project`, not from `milestone`. That is acceptable for the draft cases, which are scored against `setup-project`. It matters only for the Blind run, which the fix above covers.

## Items main's text might pass anyway
- **Item 11 (copying the merge-time steps), possible:**
  - Main doesn't forbid it.
  - Both prompts quote the steps as being for the coordinator.
  - Main's "extra merge gates" counts as a project-specific choice, so a capable model could copy them in full.
  
  The README lists 11 among main's expected failures. Each case fails on main whatever happens here (items 1, 5, 6, 9, 12 and 13 fail for certain). This doesn't affect any verdict, but if the main baseline passes 11, record that rather than treat it as a surprise.
- **Item 7, only one half:** Main might keep the `CLAUDE.md` rule to follow main's copy of each skill, but its loop has no evidence line, so item 7 still fails.
- All other items of main's expected result (pass 4, 14, 15, 16; fail the rest) hold.
