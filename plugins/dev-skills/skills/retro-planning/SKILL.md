---
name: retro-planning
description: Work through this repo's Retro backlog: snapshot the open Retro issues, group them by root cause, walk the user through each group one at a time and act on each call at once (a Ticket, a close, or a spin-off to its own planning), keeping an open record that is closed at the end. Use when Retro planning is due, or to resume one whose record is still open.
---

A **Retro planning** works through one repo's **Retro backlog** (its open issues labelled `retro`): it merges duplicates, closes one-offs, and turns repeated problems into Tickets. Run this thread at the **premium** tier: the snapshot, verdict, cap, order, spin-off and expiry rules below interact, and each must be applied exactly.

Plan only the current repo. Its tracker is named in `docs/agents/issue-tracker.md`; with no such file, use the GitHub repo of the checkout's `origin` remote. Read and write only that repo's issues, using the commands that file gives.

**The cap: at most 3 Tickets per planning.** Every Ticket this planning files counts toward it: repeated groups, severe one-offs and failed fixes alike. A spun-off group does not count. Only the user may raise the cap, and only for this planning: when more groups qualify than fit, say so, and keep the cap unless the user raises it. The record notes the cap used and the user's reason.

If the brief says this thread owns a spun-off group, skip steps 0 to 7 and go straight to "Running a spun-off planning".

## 0. Resume or start

Look for an open issue labelled `retro-planning`. If there is one, this is a resumed planning, and its creation time stays the snapshot time:

1. If its Snapshot section is still "None", continue at step 1.
2. Otherwise read its snapshot table and cap, then reconcile the record with each snapshot issue's current state: closed, an `Absorbed by` comment made since the snapshot, a `Spun off to` comment, or a Ticket labelled `ready-for-agent` filed since the snapshot that links it and is not named in a spin-off's `Filed #<ticket> (from spin-off` comment. Any call carried out on the issues but missing from the record goes into the record now, so no group is walked twice and no Ticket filed twice. An issue with a `Spun off to` comment belongs to its spin-off: record only the spin-off itself, if the record lacks it, and leave its later closes and Tickets to the spin-off's comments.
3. Redo steps 2 to 4 on the snapshot issues that still have no verdict, counting the record's "Tickets filed" toward the cap, then continue at step 5.

Otherwise file the record now as an **open** issue (format in "The record", with Cap `3 (default)` and every other section "None" for now), creating the `retro` and `retro-planning` labels if the repo lacks them. Its creation time is the **snapshot** time.

Done when there is exactly one open record and you know whether this planning is resumed.

## 1. Read the snapshot and the earlier records

The snapshot is everything filed or commented before the record's creation time, and it is all this planning plans. An issue filed, or a `Seen again` comment made, after that time **arrived during this planning**: leave it for the next planning, and list it in the record at step 7. Other threads keep running meanwhile; nothing is held.

- Every open issue labelled `retro` in the snapshot, with its body, comments and creation date.
- Every **closed** issue labelled `retro-planning` (the earlier records, format below), newest first. From them take: the groups the newest record held back by the cap, every Ticket in its "Tickets filed" and every Ticket in its `Filed #<ticket> (from spin-off ...)` comments, each with the Retro issues it absorbed, and each open issue's "plannings without a new vote" count from the newest record.

Count each issue's **votes by distinct thread**: the thread its body names as the source, plus the thread of each `Seen again in <thread link>` comment in the snapshot. A thread counts once, however many comments it left. An issue has a **new vote** when it was filed, or got a `Seen again` comment, after the newest closed record was created; with no record yet, every issue has one.

Give each issue a status:

- **Waiting on an open Ticket**: absorbed by a Ticket that is still open. List it, and leave it out of steps 2 to 5.
- **Spun off, waiting**: it has a `Spun off to <thread link>` comment and no later `Absorbed by` comment. Its owning planning has not decided it yet. List it, and leave it out of steps 2 to 5.
- **Failed-fix candidate**: absorbed by a Ticket closed as completed (read the close reason with `gh issue view <n> --json state,stateReason`, or `state_reason` on the REST route, or the tracker doc's equivalent), with a new vote since the Ticket closed. It goes to step 2.
- **Closing with its Ticket**: absorbed by a Ticket closed as completed, with no new vote since. Its verdict is **Close with its Ticket**.
- **In the backlog**: every other issue, including one absorbed by a Ticket closed any other way than completed (not planned, duplicate, abandoned). Nothing fixed it, so it is not closing, not a failed-fix candidate and not waiting: it keeps its votes and new-vote answer, and is grouped and judged in steps 2 to 5 like any other.

An issue's latest `Absorbed by` comment decides which Ticket it waits on or closes with.

Write the snapshot table into the record.

Done when every open `retro` issue in the snapshot has its distinct-thread count, its new-vote yes or no, and its status, and the record holds them.

## 2. Recheck earlier fixes

For each Ticket named in an earlier record that closed as completed, check whether its problem has come back: an absorbed issue with a new vote after the Ticket closed, or a Retro issue in the snapshot filed or voted on after it closed that matches the Ticket's problem. Each match makes a **failed-fix group**: the fix did not work. This runs before the cap is filled, and a failed-fix group counts toward it.

A Ticket closed any way other than completed (not planned, duplicate, abandoned) fixed nothing: mark it "not fixed", and its issues stay in the backlog.

Done when every closed Ticket in the earlier records is marked "holding", "came back" or "not fixed", with the matching issues.

## 3. Group and propose verdicts

Group the remaining backlog issues by root cause and merge duplicates. A group's vote count is the number of distinct threads across all its issues, so one thread that filed two duplicates counts once.

Give each group the first verdict that fits:

1. **Act, failed fix**: a failed-fix group from step 2.
2. **Expire**: the group has had no new vote across 2 plannings. That is: every issue in it has a count of 1 or more under "plannings without a new vote" in the newest record, and none has a new vote. Close it with "reopen if seen again". A group the newest record held back by the cap never expires.
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

Take the groups in the step 4 order. While this planning has filed fewer Tickets than the cap allows (spin-off Tickets live only in comments on the record and do not count), the next acting group is proposed as a Ticket; once the cap is full, each later acting group is shown as **held back by the cap**. So when the user closes or spins off a proposed Ticket, its slot stays free and the next acting group moves up into it.

Show one group, with full details:

- **Background**: how the skill or workflow works today, at the point the issues touch.
- **What went wrong**: the concrete incident in each thread that filed or voted on it.
- **Root cause** the issues share, and the distinct-thread count.
- **Proposed verdict** with its reason.
- For a proposed Ticket: its draft (title, done condition) and a Model tier (`regular` or `premium`; for `premium`, one line on why). Prefer a check or a hook that catches the problem mechanically over a new prose rule in a skill or steering file; propose a prose rule only when no check can see the problem, and say why.

Then ask for the user's call and wait for it: act as a Ticket, spin off, close, or the user's own change (a different verdict, a reshaped Ticket, keep it open). The user's call is that group's approval: carry it out at once with step 6, update the record, then show the next group. A call that changes the grouping regroups only the groups not yet walked.

When every group is walked, show the mechanical closes in one short list (each issue, and the completed Ticket that absorbed it, or "expired"), and carry them out once the user agrees. One the user holds back stays open.

Done when every group in the walk and every mechanical close has the user's call, carried out and in the record.

## 6. Carry out a call

- **Ticket**: file it with `to-tickets`' issue template, including its `**Model tier:**` line. Label it `ready-for-agent` (the string `docs/agents/triage-labels.md` maps it to, if the repo has that file). Its done condition goes in the acceptance criteria. Link each Retro issue it absorbs, and add a criterion that those issues close with the Ticket (list them as `Closes #<n>` in the pull request that closes the Ticket), and only when the Ticket is completed: if it is closed as not planned, they stay open. On each absorbed issue, comment `Absorbed by #<ticket>; closes when it is completed.`
- **`wontfix`** or another close: comment the reason, add the `wontfix` label (the string `docs/agents/triage-labels.md` maps it to, if the repo has that file) when the verdict is `wontfix`, and close.
- **Spin off**: the group needs more discussion, so this planning does not decide it. Ask for a separate planning thread for its issues: in a project with a coordinator, ask the coordinator; otherwise tell the user to start one, and give them the brief. The brief names the issues, this record, and "Running a spun-off planning" below. On each issue, comment `Spun off to <thread link>; that planning decides it.` (with no link yet, name the thread as the user or coordinator named it). A spun-off group stays open, does not count toward the cap, and cannot expire.
- **Expire**: comment `No new vote across 2 plannings. Reopen if seen again.` and close.
- **Close with its Ticket**: first check the Ticket's close reason is `completed`; if not, leave the issue open in the backlog. Comment `Closed with #<ticket>.` and close.
- **Held back by the cap**, or kept open: leave open.

Then update the record straight away: the group's row in "Verdicts", its line in "Tickets filed", "Held back by the cap" or "Spun off", and "Cap" when the user raised the cap.

Done when the issue's state matches the call and the record shows it.

## 7. Close the record

End every planning by closing the record, also when the user declined every verdict: once closed, it is the newest record, so `retro`'s clock runs from its creation (the snapshot time) and the expiry counts advance. Before closing, fill "Arrived during this planning" (each open `retro` issue filed, and each `Seen again` comment made, after the snapshot time), "Open issues: plannings without a new vote", and the waiting lists. Then close it, and give the user its link.

A planning that pauses before the end leaves its record open; the next run of this skill resumes it at step 0.

Done when the record is complete and closed, and the user has its link.

## Running a spun-off planning

When the brief says this thread owns a spun-off group, plan only its issues with the user. Discuss them as long as the user needs, then give each issue a verdict, carried out as in step 6: absorbed by a Ticket this thread files, or closed with a reason. File no `retro-planning` record of your own, and never edit the body of the record that spun it off: its planning is the body's only writer. Instead, comment on that record, open or closed: right after filing each Ticket, one comment for it, `Filed #<ticket> (from spin-off <this thread's link>), absorbs #<n>, ...`, so later plannings recheck it in step 2, and one more listing each issue you closed with its reason. The thread's work is done when no issue it owns is left open without an `Absorbed by` comment, and every Ticket it filed has its `Filed` comment on that record. On resuming this thread, first check that every Ticket it filed has its `Filed` comment, and post any that is missing.

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

Every verdict appears, kept-open ones included. "Plannings without a new vote" covers every snapshot issue left open that is not waiting on a Ticket or spun off: 0 if it had a new vote since the previous record or is held back by the cap, otherwise the previous record's count plus 1 (a missing count is 0). "Spun off, waiting" lists issues spun off by an earlier planning and still undecided; this planning's own spin-offs are under "Spun off".
