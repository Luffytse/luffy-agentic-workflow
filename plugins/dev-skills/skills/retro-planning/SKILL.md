---
name: retro-planning
description: Work through this repo's Retro backlog: snapshot the open Retro issues, group them by root cause, walk the user through each group one at a time and act on each call at once (a Ticket, a close, or a spin-off to its own planning), keeping an open record that is closed at the end; inside a Milestone, agents decide every group at Release end. Use when the user asks for Retro planning, when a Release ends inside a Milestone, or to resume one whose record is still open.
---

A **Retro planning** works through one repo's **Retro backlog** (its open issues labelled `retro`): it merges duplicates, closes one-offs, and turns repeated problems into Tickets. Run this thread at the **premium** tier: the snapshot, verdict, cap, order, spin-off and expiry rules below interact, and each must be applied exactly. Load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it.

Plan only the current repo. Its tracker is named in `docs/dev-skills/issue-tracker.md`; with no such file, use the GitHub repo of the checkout's `origin` remote. Read and write only that repo's issues, using the commands that file gives.

**The cap: at most 3 Tickets per planning.** Every Ticket this planning files counts toward it: repeated groups, severe one-offs and failed fixes alike. A spun-off group does not count. Only the user may raise the cap, and only for this planning: when more groups qualify than fit, say so, and keep the cap unless the user raises it. The record notes the cap used and the user's reason. Inside a Milestone there is no cap (see "Inside a Milestone").

Load `issue-absorption` before reconciling absorption records, classifying the snapshot or carrying out an absorption or close-with-Ticket verdict. Apply its agreement and lifecycle as reference while continuing this planning.

This file describes a planning that runs with the user. Inside a Milestone (the agreement test in "Inside a Milestone" at the end), follow that section instead of walking the user through each group.

If the brief says this thread owns a spun-off group, skip steps 0 to 7 and go straight to "Running a spun-off planning".

## 0. Resume or start

Look for an open issue labelled `retro-planning`. If there is one, this is a resumed planning, and its creation time stays the snapshot time:

1. If its Snapshot section is still "None", continue at step 1.
2. Otherwise read its snapshot table and cap, then reconcile the record with each snapshot issue's current state: closed, an `Absorbed by` comment made since the snapshot, a `Spun off to` comment, or a Ticket labelled `ready-for-agent` filed since the snapshot that links it and is not named in a spin-off's `Filed #<ticket> (from spin-off` comment. Any call carried out on the issues but missing from the record goes into the record now, so no group is walked twice and no Ticket filed twice. An issue with a `Spun off to` comment belongs to its spin-off: record only the spin-off itself, if the record lacks it, and leave its later closes and Tickets to the spin-off's comments.
3. Reconcile any unfinished handoff before walking another group: search for already-created Tickets even if labels or absorption comments are missing, using the recorded identifiers, source links and approved work. Count each real Ticket once toward the cap, and resume `to-tickets` with its existing identifiers, mappings, solution approval and incomplete actions to repair publication rather than create it again. Preserve a declined solution and the user's problem verdict; resume the pending decision, not a fresh proposal.
4. Redo steps 2 to 4 on the snapshot issues that still have no verdict, counting the record's "Tickets filed" toward the cap, then continue at step 5.

Otherwise file the record now as an **open** issue (format in "The record", with Cap `3 (default)` and every other section "None" for now), creating the `retro` and `retro-planning` labels if the repo lacks them. Its creation time is the **snapshot** time.

Done when there is exactly one open record and you know whether this planning is resumed.

## 1. Read the snapshot and the earlier records

The snapshot is everything filed or commented before the record's creation time, and it is all this planning plans. An issue filed, or a `Seen again` comment made, after that time **arrived during this planning**: leave it for the next planning, and list it in the record at step 7. Other threads keep running meanwhile; nothing is held.

- Every open issue labelled `retro` in the snapshot, with its body, comments and creation date.
- Every **closed** issue labelled `retro-planning` (the earlier records, format below), newest first. From them take: the groups the newest record held back by the cap, every Ticket in its "Tickets filed" and every Ticket in its `Filed #<ticket> (from spin-off ...)` comments, each with the Retro issues it absorbed, and each open issue's "plannings without a new vote" count from the newest record.

Count each issue's **votes by distinct thread**: the thread its body names as the source, plus the thread of each `Seen again in <thread link>` comment in the snapshot. A thread counts once, however many comments it left. An issue has a **new vote** when it was filed, or got a `Seen again` comment, after the newest closed record was created; with no record yet, every issue has one.

Give each issue a status:

- **Waiting on an open Ticket**: the absorption contract says waiting. List it, and leave it out of steps 2 to 5.
- **Spun off, waiting**: it has a `Spun off to <thread link>` comment and no later `Absorbed by` comment. Its owning planning has not decided it yet. List it, and leave it out of steps 2 to 5.
- **Failed-fix candidate**: the absorption contract says completed, with a new vote since the Ticket closed. It goes to step 2.
- **Closing with its Ticket**: the contract says completed, with no new vote since. Its verdict is **Close with its Ticket**.
- **In the backlog**: every other issue, including the contract's not-fixed sources. Keep its votes and new-vote answer, and group and judge it in steps 2 to 5 like any other.

Write the snapshot table into the record.

Done when every open `retro` issue in the snapshot has its distinct-thread count, its new-vote yes or no, and its status, and the record holds them.

## 2. Recheck earlier fixes

For each Ticket named in an earlier record that closed as completed, check whether its problem has come back: an absorbed issue with a new vote after the Ticket closed, or a Retro issue in the snapshot filed or voted on after it closed that matches the Ticket's problem. Each match makes a **failed-fix group**: the fix did not work. This runs before the cap is filled, and a failed-fix group counts toward it.

Apply the absorption contract to mark the other closed Tickets "not fixed".

Done when every closed Ticket in the earlier records is marked "holding", "came back" or "not fixed", with the matching issues.

## 3. Group and propose verdicts

Group the remaining backlog issues by root cause and merge duplicates. A group's vote count is the number of distinct threads across all its issues, so one thread that filed two duplicates counts once.

Give each group the first verdict that fits:

1. **Act, failed fix**: a failed-fix group from step 2.
2. **Expire**: the group has had no new vote across 2 plannings. That is: every issue in it has a count of 1 or more under "plannings without a new vote" in the newest record, and none has a new vote. Close it with "reopen if seen again". A group the newest record held back by the cap never expires (inside a Milestone, nor one it listed as proposed to the user).
3. **Act**: seen in 2 or more distinct threads.
4. **Act, severe**: seen in one thread, but severe: lost data, a security problem, or a large waste of time or money.
5. **Close as `wontfix`**: seen in one thread and not severe. Write the reason.

Done when every group, and every issue closing with its Ticket, has a verdict, and every `wontfix` a reason.

## 4. Order the walk

Order the acting groups:

1. Failed fixes.
2. Groups the newest record held back by the cap.
3. The rest, by distinct-thread count, highest first; on a tie, the group with the oldest issue first.

After them come the `wontfix` groups, oldest issue first. Expiries and issues closing with their completed Ticket are the **mechanical closes**: they leave no judgment to make and wait for the end of step 5.

Done when every group has its place in one ordered walk.

## 5. Walk the user through each group, one at a time

Inside a Milestone this step is replaced by "Deciding the groups" below.

Take the groups in the step 4 order. While this planning has filed fewer Tickets than the cap allows (spin-off Tickets live only in comments on the record and do not count), the next acting group is proposed as a Ticket; once the cap is full, each later acting group is shown as **held back by the cap**. So when the user closes or spins off a proposed Ticket, its slot stays free and the next acting group moves up into it.

Show one group, with full details:

- **Background**: how the skill or workflow works today, at the point the issues touch.
- **What went wrong**: the concrete incident in each thread that filed or voted on it.
- **Root cause** the issues share, and the distinct-thread count.
- **Proposed verdict** with its reason.
- For an acting group: the intended outcome and whether to address this problem. Ticket preparation follows that call.

When the call is to address the problem, before the `to-tickets` workflow shows its proposed Ticket (step 6), fetch the default branch and re-read the current state of every issue, pull request and path its draft names, and correct the draft; the votes stay as of the snapshot.

Then ask for the user's call and wait for it: address the problem, spin off, close, or the user's own change (a different verdict, a reshaped problem, keep it open). Approval to address a problem authorizes preparation, not its concrete solution. Record the call, carry it out at once with step 6, and reconcile the result in the record before showing the next group. A call that changes the grouping regroups only the groups not yet walked.

When every group is walked, show the mechanical closes in one short list (each issue, and the completed Ticket that absorbed it, or "expired"), and carry them out once the user agrees. One the user holds back stays open.

Done when every group in the walk and every mechanical close has the user's call, carried out and in the record.

## 6. Carry out a call

- **Address the problem**: invoke the complete `to-tickets` workflow. Pass the intended outcome; source reports explicitly marked as issues to absorb; agreed constraints, failed-fix context and known dependencies; this one group's scope; and the remaining actual-ticket budget. Request one complete Ticket, with a return before publication if investigation requires several. Prefer a mechanical check or hook over a prose rule; pass that preference as a constraint, with a reason required when only prose can address the problem. Do this re-read (step 5) before each time the proposed Ticket is shown, a resumed handoff included. `to-tickets` owns context gathering, investigation, drafting, tier/dependency discussion, concrete-solution approval and verified publication. Include any existing publication identifiers, source mappings, approval and incomplete actions on resume.
  - Reconcile its returned identifiers, source-to-ticket mappings and incomplete actions into the record. A real Ticket counts immediately even when a later label, link, comment or verification failed. Keep the handoff pending and resume its unfinished actions before showing another group; never recreate an existing Ticket.
  - If several Tickets are necessary, return to the user's spin-off decision before any publication. Keep the cap unchanged unless the user explicitly changes it; a larger budget alone does not turn this one-Ticket handoff into permission to publish several.
  - If the solution is declined, preserve both the problem approval and solution rejection, with the user's next call (revise, spin off, close or keep open). A decline creates no Ticket and consumes no slot. Once a solution has been approved and published, update the record without asking for solution approval again.
- **`wontfix`** or another close: comment the reason, add the `wontfix` label (the string `docs/dev-skills/triage-labels.md` maps it to, if the repo has that file) when the verdict is `wontfix`, and close.
- **Spin off**: the group needs more discussion, so this planning does not decide it. Ask for a separate planning thread for its issues: in a project with a coordinator, ask the coordinator; otherwise tell the user to start one, and give them the brief. The brief names the issues, this record, and "Running a spun-off planning" below. On each issue, comment `Spun off to <thread link>; that planning decides it.` (with no link yet, name the thread as the user or coordinator named it). A spun-off group stays open, does not count toward the cap, and cannot expire.
- **Expire**: comment `No new vote across 2 plannings. Reopen if seen again.` and close.
- **Close with its Ticket**: recheck eligibility under `issue-absorption`; when eligible, comment `Closed with #<ticket>.` and close, otherwise apply its current lifecycle state.
- **Held back by the cap**, or kept open: leave open.

Then update the record straight away: the group's row in "Verdicts", its line in "Tickets filed", "Held back by the cap" or "Spun off", and "Cap" when the user raised the cap. Keep pending handoffs in "Incomplete actions", including the problem verdict, solution approval or rejection, published identifiers, source mappings and remaining work; clear that entry only after reconciliation.

Done when the issue's state matches the call and the record shows it.

## 7. Close the record

End every planning by closing the record, also when the user declined every verdict: once closed, it is the newest record, so the expiry counts advance. Before closing, fill "Arrived during this planning" (each open `retro` issue filed, and each `Seen again` comment made, after the snapshot time), "Open issues: plannings without a new vote", and the waiting lists. Then close it, and give the user its link.

A planning that pauses before the end leaves its record open; the next run of this skill resumes it at step 0.

Done when the record is complete and closed, and the user has its link.

## Running a spun-off planning

When the brief says this thread owns a spun-off group, plan only its issues with the user. Discuss them as long as the user needs, then give each issue a verdict, carried out as in step 6: absorbed by Tickets prepared and published through the complete `to-tickets` workflow, or closed with a reason. Pass this spun-off scope and its agreed budget instead of the ordinary one-Ticket limit; the originating planning's cap does not apply here. File no `retro-planning` record of your own, and never edit the body of the record that spun it off: its planning is the body's only writer. Instead, comment on that record, open or closed: right after filing each Ticket, one comment for it, `Filed #<ticket> (from spin-off <this thread's link>), absorbs #<n>, ...`, so later plannings recheck it in step 2, and one more listing each issue you closed with its reason. The thread's work is done when no issue it owns is left open without an `Absorbed by` comment, and every Ticket it filed has its `Filed` comment on that record. On resuming this thread, first check that every Ticket it filed has its `Filed` comment, and post any that is missing.

## Inside a Milestone

A planning runs **inside a Milestone** when both hold: the Boundary record (`docs/dev-skills/boundaries.md`) names a Milestone label form, and an open Milestone issue exists (the issue carrying a label in that form that holds the Milestone's goal; for a Release-end run, the one the release issue links or names). The caller, the Release thread, runs it at the end of a named Release, naming the Release or its release issue, together with or after the Triage batch (see `triage`). With no such agreement, everything above runs as written, cap included, and everything below is skipped.

Inside a Milestone agents decide: the user is asked nothing per group, except as "Goes to the user" says. Read the Milestone issue (goal, features, acceptance criteria, exclusions, its own boundaries) and the Boundary record before the first group. Steps 0 to 4 run as written, except that the record's Cap section reads `none (inside a Milestone)`. No cap applies: no Ticket counts toward one, no group is held back by one, and the cap wording in steps 0 to 4, step 5's held-back logic, "Held back by the cap" and "raised by the user" apply to nothing here.

### Deciding the groups

Take the groups in step 4 order and decide each one yourself, without waiting. Step 3's verdict says whether a group deserves action; the call sets its **disposition**:

- **joins the next Release**: an acting group whose fix touches a feature of this Milestone (it blocks it, or fixes something the feature relies on) or is severe (a security flaw, lost data, a large waste of time or money). Carry it out through step 6's "Address the problem", as changed below. This is the proposal for Release planning, which owns the release labels: apply no release label. The fix does not count toward the Release's feature cap.
- **stays open**: any other acting group, including one an open Ticket or a planned piece of the Milestone already covers. Write the reason down; leave its issues open.
- **closed**: a `wontfix` group, an expiry, or an issue closing with its Ticket, carried out as step 6 says. Mechanical closes need no asking.
- **proposed to the user**: see "Goes to the user".
- **spun off**: only as step 6 says, for a group that needs discussion with the user; prefer a disposition above.

Carry each call out at once with step 6, then update the record's "Verdicts" row: the disposition in the Verdict column, and in the last column the reason and any Ticket. The user sees every call and reason at the Milestone review.

Step 6's "Address the problem" changes here. No budget limit is passed; request the group's Tickets, each separately sized, and tell `to-tickets` that this planning is deciding inside a Milestone. `to-tickets` drafts the breakdown and judges whether the fix is a **feature** (a Spec with its Tickets, not a lone Ticket). If it is, `to-tickets` publishes nothing and returns the breakdown as "needs larger scope"; if not, this planning's approval of the concrete breakdown stands in for the user's (`to-tickets` step 4) and `to-tickets` publishes. The "return to the user's spin-off decision" and "solution is declined" bullets apply to nothing here. A returned feature-sized breakdown makes the group "Goes to the user": proposed, nothing filed.

### Goes to the user

Ask one question per decision, saying which kind it is, for a group that:

- **crosses a boundary** in the Boundary record or in the Milestone issue's own boundaries,
- **changes the Milestone's agreement** (goal, acceptance criteria, exclusions), or
- would join the next Release but needs a **feature-sized** fix: the user plans every feature, agents only propose. (A group that would stay open anyway is not proposed.)

Propose it and file nothing: the group stays open and its disposition is `proposed to the user`. The record lists it under "Proposed to the user" (group, issues, kind, question), with its issues' "plannings without a new vote" at 0. A group the newest record listed there and still open is listed again as waiting, not asked again, unless it has a new vote.

### Dry run

When the caller asks for a dry run (proposals only), run steps 0 to 4 read-only, with no record issue filed and the snapshot read at the current time, then decide each group as above. Write nothing to the tracker: no record, comment, label, close or Ticket, and ask the user nothing. Return each group with its disposition, reason, and for a group that joins the next Release the Ticket it would file, in your reply.

## The record

An issue titled `Retro planning <yyyy-mm-dd>` (the snapshot's date), labelled `retro-planning`. It is open while the planning runs and closed at its end; the next planning reads only closed records, so each section below is required, with "None" when empty:

```markdown
Snapshot time: <the record's creation time>

## Cap

3 (default) / <n>, raised by the user: <reason>

## Snapshot

| Retro issue | Distinct threads | New vote | Status |
|-------------|------------------|----------|--------|
| #12 | 2 | yes | in the backlog |
| #18 | 1 | no | waiting on #35 |
| #19 | 1 | no | spun off, waiting |

## Verdicts

| Group | Retro issues | Distinct threads | Verdict | Reason or Ticket |
|-------|--------------|------------------|---------|------------------|
| <root cause> | #12, #15 | 3 | Ticket | #40 |
| <root cause> | #13 | 1 | wontfix | <reason> |
| <root cause> | #14 | 2 | held back by the cap | |
| <root cause> | #20 | 2 | spun off | <thread link> |
| <root cause> | #16 | 1 | kept open by the user | |
| absorbed by a Ticket closed as completed | #11 | 2 | closed with its Ticket | #31 |

## Incomplete actions

None / <group: problem verdict; solution decision; existing Ticket identifiers and source mappings; remaining actions>

## Held back by the cap

- <root cause>: #14

## Tickets filed

- #40 (<root cause>), absorbs #12, #15

## Spun off

- <root cause>: #20, owned by <thread link>

## Earlier fixes rechecked

- #31: holding / came back (#17) / not fixed

## Arrived during this planning

- #22 filed
- #14 seen again in <thread link>

## Open issues: plannings without a new vote

- #14: 0
- #16: 1

## Waiting on open Tickets

- #18: #35

## Spun off, waiting

- #19: <thread link>
```

Every verdict appears, kept-open ones included. "Plannings without a new vote" covers every snapshot issue left open that is not waiting on a Ticket or spun off: 0 if it had a new vote since the previous record, is held back by the cap or (inside a Milestone) is proposed to the user, otherwise the previous record's count plus 1 (a missing count is 0). "Spun off, waiting" lists issues spun off by an earlier planning and still undecided; this planning's own spin-offs are under "Spun off".

Inside a Milestone the record differs in four places: Cap reads `none (inside a Milestone)`; the Verdict column of "Verdicts" holds the disposition (`joins the next Release`, `stays open`, `closed`, `proposed to the user`, `spun off`) and its last column the reason and any Ticket; the zero case of "Open issues: plannings without a new vote" also covers a group proposed to the user; and a required section follows "Held back by the cap" (which reads "None"):

```markdown
## Proposed to the user

- <root cause>: #14, <kind: crosses a boundary / changes the agreement / feature-sized>, <question>
```
