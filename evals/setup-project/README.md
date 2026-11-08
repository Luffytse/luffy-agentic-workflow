# setup-project draft check

The seam is the instruction draft the user reviews, including the difference between projects inside a Milestone and those without an open Milestone agreement. These are bounded draft-stage conversation cases: each supplies facts and explicit shared-understanding confirmation, so it tests drafting rather than re-running the interview. They authorize no project setting, repository file or tracker write.

Run each prompt in a fresh agent with the selected source's `setup-project` skill. Make its sibling `milestone` skill available by name; give only the case prompt, never this scoring guide. Run `milestone-rerun.txt` against main before the change, then both cases against the candidate. Retain the actual draft and diff locally and record the observed outcomes and limits in the PR evidence. Compare meaning, not exact wording.

For `milestone-rerun.txt`, pass only when the full draft:

- Names the `milestone` skill as the coordinator workflow and `team-lead` for its delivery, points to the repo/docs/tracker, and retains the two-thread limit and backend-before-dashboard order.
- Retains the project's schema-migration merge gate, explicit completion callback, archive rule, and pull-main/reload-changed-skills rule after every merge. Any version hand-out or post-merge Ticket re-read the project wants is its own rule, kept in its instructions or release doc; no skill states one.
- Leaves out the shared thread-kind/brief/model-start rules, Release grouping, nudge/stop/takeover procedure and retro procedure. These are reached through their owning skills.
- Points to the Boundary record rather than copying its check-in interval, budget or deploy approval rule.
- Omits current-work state (`#7`, `#31`, `#32`) and shows a diff against the existing text as well as the full replacement.
- Remains an unsaved draft waiting for the user's approval, with no file/settings write or handover claim.

For `no-milestone.txt`, pass only when the full draft keeps the existing full-instructions behavior: coordinator/thread kinds and their skills (the coordinator running `team-lead` for delivery of planned work), every brief field, Model tiers and model-start rule, project limits/merge rules and standing rules, docs/tracker pointers and tracker lookup for open work. It must not switch this project to the `milestone` workflow, add current-work state or claim approval/save/handover.

These cases do not exercise exploration, an actual grilling exchange, the user's later approval or the coordinator's save operation. Check those unchanged steps by diff inspection; passing draft cases is not evidence that settings were saved. This is a local-source behavior check, not an installed-runtime discovery test.

## Coordinator that cannot load the plugin

`no-plugin.txt` (inside a Milestone) and `no-plugin-outside.txt` (no open Milestone agreement) give a project thread a coordinator that reports a skill list of built-ins only. Decision-level, regular tier; give each run the checkout's `setup-project` and its sibling `milestone` and `team-lead` skill folders (including `team-lead/DELIVERY-LOOP.md`), the case prompt only. Run on the branch and on main's skills (from a `git archive`); main's has no loop file, so it cannot carry one.

For each, pass only when the full draft:

- Carries the five steps of "The loop" in `team-lead/DELIVERY-LOOP.md` as that file gives them: a Startup verification thread before any Build thread, a Release thread to plan when no Release is current, Build threads only for the current Release's label, a Release thread to cut and plan the next when its issues have closed, and a report thread when every feature is merged or parked. Meaning, not exact wording; the file's text should appear verbatim or nearly so.
- Does not leave the coordinator told only to run `milestone` or `team-lead` itself (it cannot load them).
- For `no-plugin.txt`, still keeps the owner pointers and project choices (two-thread limit, backend before dashboard, migration merge gate, Boundary record pointer) without copying the Boundary record's values.
- For `no-plugin-outside.txt`, still keeps the full instructions (thread kinds and skills, every brief field, Model tiers and model-start rule, limits and merge rules, tracker lookup).
- Holds no current-work state and claims no approval, save or handover.

Check by diff inspection that the existing `milestone-rerun.txt` and `no-milestone.txt` drafts (a coordinator that can load the plugin, or unstated) do not gain the loop.
