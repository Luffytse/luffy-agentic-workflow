Warning: no stdin data received in 3s, proceeding without it. If piping from a slow command, redirect stdin explicitly: < /dev/null to skip, or wait longer.
# Case check: setup-project, for a coordinator that cannot load the plugin

I read every file under the folder and nothing outside it. In `branch/`, `setup-project` changed, and so did `team-lead` (its Releases rule, the build Order and the `wait` record) and `milestone` (two pointers). `team-lead/DELIVERY-LOOP.md` was removed. `model-tiers`, `to-tickets` and `milestone/reporting.md` are the same on both sides.

**No case needs a drop. All four need a fix**, and three of the four fixes are wording changes in the README. The fourth (blind run) also adds scenarios and a main baseline run. Once fixed, each needs checking again.

| Case | Valid | Fails on main for the right reason | Needed | Verdict |
|---|---|---|---|---|
| `no-plugin.txt` | Mostly; items 15, 10, 9 and 6 need changes | Yes | Yes | **fix** |
| `no-plugin-outside.txt` | Mostly; items 10, 9 and 6 need changes | Yes | Yes | **fix** |
| Older-prompts expectation | No: as written it contradicts the older cases' own pass lists | No; main passes it | Yes | **fix**, then keep as a regression guard |
| Blind run | Partly | Not shown | Yes | **fix** |

## `no-plugin.txt`: fix

**Valid.** The prompt gives every fact the coverage list needs: the coordinator's built-ins-only answer, the harness, the quoted `CLAUDE.md` rule and merge-time steps, the stamp, and that the plugin is at main's version. It also gives the project's own choices. Items 1–8 and 11–14 are what the branch's text gives. Four items are not:

- **Item 15, "points to the Boundary record": the branch text doesn't give this for a coordinator that cannot load the skills.** `setup-project/SKILL.md:62` ties the Boundary-record pointer and "keep only the project-specific choices" to a coordinator that *can* load them. Line 44 only says to write the cycle "from them and the project's facts". The prompt also says this coordinator cannot read `CLAUDE.md`, so a bare pointer to `boundaries.md` may be useless to it.
  - Change item 15's first half to: "For `no-plugin.txt`, keeps the project choices (two-thread limit, backend before dashboard, migration merge gate), and gives the Boundary record's check-in interval and production-deploy approval, either quoted or as the file a thread reads."
  - Or fix line 62 so it covers both coordinators.
- **Item 10: the run folder can't supply every tier.** "Thread kinds and tiers, chore threads included" needs tiers for the Release, triage and report threads. `team-lead` says the Release worker runs "at the tier that skill names", and `release` and `triage` aren't in the run folder. A drafter therefore has to guess, which `model-tiers` forbids, or name the gap to the user (line 44 asks for that).
  - Change item 10 to: "Names thread kinds and tiers, chore threads included (a tier the folder's skills don't give is either taken from `model-tiers`' 'Use for' column or named to the user as unfilled), and writes a tier map with a model for each tier."
  - Or add the `release` and `triage` folders to the run folder.
- **Item 9, "a feature sent back resumes through `milestone`": the branch skills disagree with each other here.** The README follows `setup-project:54`. But `milestone/reporting.md` (re-entry paragraph) resumes sent-back work "through the `team-lead` skill (which arranges the check-in again)", then posts a new report linking the old one.
  - Change item 9's end to: "a feature sent back resumes through the delivery steps, with the check-in arranged again and a new report linking the earlier one."
  - Separately, line 54 of the skill should be fixed to match.
- **Item 6, "ends it when the report is written": `team-lead` says when, but not in those words.** Its End of delivery, and `milestone`'s Milestone review, end the check-in *before* the report is written. `setup-project:51` says "off when the report is written".
  - Change to: "ends it as the report starts (before the report thread writes it)".

**Fails on main for the right reason: yes.** Main copies `DELIVERY-LOOP.md`'s five steps word for word, which is exactly the rule this PR replaces. That loop has:
- no planning step, no feature briefs, no check-in, no evidence line, no definitions of terms and no stamp;
- separate plan and cut triggers keyed on a "current Release";
- a report that runs on "merged or parked", with no wait for the last cut and no acceptance step.

So items 1, 2, 5, 6, 7, 9, 12 and 13 fail on main because of the changed rule, not because of the fixture. Two notes:
- Item 5 fails on main partly because main's `team-lead` also still had the old Releases rule. That's within this PR, since the PR changes both files.
- Main's folder includes `DELIVERY-LOOP.md`, so `../team-lead/DELIVERY-LOOP.md` resolves and the baseline isn't broken.

**Needed: yes.** This is the only case for a coordinator inside a Milestone that cannot load the skills.

## `no-plugin-outside.txt`: fix

**Valid.** It's the same as above, plus the full instructions for a project outside a Milestone. Item 15's second half matches `setup-project:64`, including dropping the line that has the coordinator run `team-lead` (item 14). Item 15 needs no change here. The same fixes to items 10, 9 and 6 apply. The project choice "every brief includes … Review level" overrides `team-lead`'s "Review level only when named", and "every brief field" scores that correctly.

**Fails on main: yes, for the same reasons.** Main's outside-a-Milestone path also writes no tier map when the user has none ("draft the rule without the map"), so main also fails item 10. That's the right reason: the branch now always writes the map for this coordinator.

**Needed: yes.** This path is separate: full instructions plus the cycle, minus the run-`team-lead` line.

## Older-prompts expectation (`milestone-rerun.txt`, `no-milestone.txt`): fix, then keep as a regression guard

**Valid?** The intent matches `setup-project:60` ("Where the coordinator can load them, add none of this"). Both prompts do give the coordinator's "can load `team-lead`, `milestone`, `release` and `worker-control`" answer.

But "gain none of the coverage list's text" can't be met as written:
- `no-milestone.txt`'s own pass list requires thread kinds and skills, Model tiers and the model-start rule, which is the same ground as items 10 and 15.
- `milestone-rerun.txt` allows the project's own version hand-out and re-read rule, which overlaps item 11, and keeps the two-thread limit.

Replace the sentence with:

> "…their drafts add none of the assembled cycle: no planning, feature-brief or mid-Milestone steps, no Startup verification step, no delivery or Releases steps, no check-in, no evidence line, no quiet-thread rule, no report or acceptance steps, no definitions of terms, no copied merge-time steps beyond what the project's existing text or facts carry, no tier map the user did not give, and no source stamp. What each older case's own pass list requires is not counted against it."

**Fails on main: no.** Main's text says the same thing ("add nothing for it"), so main passes. Under CASE-CHECK this is a changed expectation that guards a rule a capable model already follows. Record it as a **regression guard** in `RESULTS.md` and name it on the `**Eval:**` line. It doesn't need checking again after the wording fix.

**Needed: yes.** No other case stops the new list leaking into drafts for a coordinator that can load the skills. `milestone-rerun`'s "leaves out" list covers part of it; `no-milestone` has no such check.

## Blind run: fix

**Valid in purpose** (can a coordinator with no skills act from the draft alone?), but it needs four changes:

1. **Say which draft it reads.** "One assembled draft" doesn't say which. Make it: "the `no-plugin-outside.txt` draft, since its first scenario (the user asks for a Milestone) starts with no Milestone open; optionally the `no-plugin.txt` draft too."
2. **Have a scorer judge it, not the blind session.** Add: "A scorer, not the blind session, marks each scenario pass when the action matches the draft's step for it and the session needed no skill and no doc it cannot read. One scenario needing either fails the run."
3. **Add the scenarios the item list covers but the run doesn't:**
   - the user plans a feature mid-Milestone;
   - the user raises a bug mid-Milestone (item 3);
   - a Release thread reports it planned nothing, or that the cut is blocked (`team-lead`'s `wait` rule).
4. **Show it fails on main.** Add: "Run the same scenarios once on main's draft (the copied loop) and record which ones fail." If the run is only evidence that the draft can be used, say that instead and record it as such.

**Needed: yes.** Items 1–16 check what the draft covers, not whether a coordinator can act on it. Running a coordinator with no skills against the draft is what found the gaps the last time project instructions were drafted for this coordinator.

## Extra flags

**README items the branch's skill text doesn't give, or gives differently:**
- **Item 15:** the Boundary-record pointer is only for a coordinator that can load the skills.
- **Item 9:** the "resumes through `milestone`" route conflicts with `reporting.md`.
- **Item 6:** the timing of ending the check-in differs from `team-lead`.
- **Item 10:** the fixture can't supply the Release and triage tiers.
- **Item 5 omits part of `team-lead`'s Releases rule.** The branch has `setup-project` cover "each delivery step of `team-lead` as it now reads, its Releases rule included", but item 5 leaves out two parts of it:
  - the "or a release issue naming this Milestone is open" start condition;
  - the `wait` record and back-off.

  Without the back-off, a coordinator could restart Release threads at every wake. Add to item 5: "…and, when a Release thread reports a blocked cut or nothing planned, tells the user once and starts no Release thread again until that changes or the user writes."
- **Item 13 omits part of the skill's rule.** It leaves out "tells the user *once*, and goes on unless the user says to wait". Add those words.

**Items main's text would pass anyway.** These aren't defects, because each case still fails on the changed rule:
- **Item 4:** main's loop step 1 gives the Startup verification gate almost word for word.
- **Item 14:** main says the same.
- **Items 15 and 16:** unchanged rules.
- **Item 11 (likely):** the prompt's "which the coordinator cannot read" pushes even main's drafter to copy the quote.

Don't add item 4, 11, 14, 15 or 16 to the expected main failures.
