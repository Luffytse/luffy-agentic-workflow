---
name: retro-planning
description: Work through this repo's Retro backlog in one batch: group the open Retro issues by root cause, propose a verdict per group, and after the user approves, turn the top groups into Tickets, close the rest by the rules, and file a closed record. Use when Retro planning is due.
---

A **Retro planning** works through one repo's **Retro backlog** (its open issues labelled `retro`) in a batch: it merges duplicates, closes one-offs, and turns repeated problems into Tickets. Run this thread at the **premium** tier: the verdict, cap, order and expiry rules below interact, and each must be applied exactly.

Plan only the current repo. Its tracker is named in `docs/agents/issue-tracker.md`; with no such file, use the GitHub repo of the checkout's `origin` remote. Read and write only that repo's issues, using the commands that file gives.

**The cap: act on at most 3 groups per planning.** Every group that acts counts toward it: repeated groups, severe one-offs and failed fixes alike.

## 1. Read the backlog and the earlier records

- Every open issue labelled `retro`, with its body, comments and creation date.
- Every closed issue labelled `retro-planning` (the earlier records, format below), newest first. From them take: the groups the newest record held back by the cap, every Ticket filed and the Retro issues it absorbed, and each open issue's "plannings without a new vote" count from the newest record.

Count each issue's **votes by distinct thread**: the thread its body names as the source, plus the thread of each `Seen again in <thread link>` comment. A thread counts once, however many comments it left. An issue has a **new vote** when it was filed, or got a `Seen again` comment, after the newest record was created; with no record yet, every issue has one.

An open issue absorbed by a Ticket that is still open is waiting on that Ticket: list it, and leave it out of steps 2 to 4. An open issue absorbed by a closed Ticket goes to step 2 if it has a new vote since the Ticket closed; otherwise it gets the verdict **Close with its Ticket** in step 3.

Done when every open `retro` issue has its distinct-thread count, its new-vote yes or no, and its status (waiting, failed-fix candidate, closing with its Ticket, or in the backlog).

## 2. Recheck earlier fixes

For each closed Ticket named in an earlier record, check whether its problem has come back: an absorbed issue with a new vote after the Ticket closed, or a Retro issue filed or voted on after it closed that matches the Ticket's problem. Each match makes a **failed-fix group**: the fix did not work. This runs before the cap is filled, and a failed-fix group counts toward it.

Done when every closed Ticket in the earlier records is marked "holding" or "came back", with the matching issues.

## 3. Group and propose verdicts

Group the remaining backlog issues by root cause and merge duplicates. A group's vote count is the number of distinct threads across all its issues, so one thread that filed two duplicates counts once.

Give each group the first verdict that fits:

1. **Act, failed fix**: a failed-fix group from step 2.
2. **Expire**: the group has had no new vote across 2 plannings. That is: every issue in it has a count of 1 or more under "plannings without a new vote" in the newest record, and none has a new vote. Close it with "reopen if seen again". A group the newest record held back by the cap never expires.
3. **Act**: seen in 2 or more distinct threads.
4. **Act, severe**: seen in one thread, but severe: lost data, a security problem, or a large waste of time or money.
5. **Close as `wontfix`**: seen in one thread and not severe. Write the reason.

Each issue from step 1 absorbed by a closed Ticket, with no new vote since, gets its own verdict outside the groups: **Close with its Ticket**, naming that Ticket.

Done when every group, and every issue closing with its Ticket, has a verdict, and every `wontfix` a reason.

## 4. Fill the cap

Order the acting groups:

1. Failed fixes.
2. Groups the newest record held back by the cap.
3. The rest, by distinct-thread count, highest first; on a tie, the group with the oldest issue first.

The first groups up to the cap become Tickets. Every acting group after them is **held back by the cap**: it stays open, is exempt from expiry, and comes second at the next planning.

For each Ticket, draft its title, its done condition, and a proposed Model tier (`regular` or `premium`; for `premium`, one line on why). Prefer a check or a hook that catches the problem mechanically over a new prose rule in a skill or steering file; propose a prose rule only when no check can see the problem, and say why.

Done when every acting group is either a drafted Ticket with a tier or held back by the cap.

## 5. Get the user's approval

Show the user one list: every group with its issues, distinct-thread count, verdict and reason; every issue closing with its Ticket, with the Ticket that absorbed it; and each Ticket's draft and tier. Ask up to three questions at a time, about what you are least sure of (a grouping, a severity call, a Ticket's shape); ask the next ones once those are answered.

Approval is the user's own message saying so. Close nothing and file nothing before it. A verdict the user declines leaves its group or issue open with no action. If the user changes a verdict, redo step 4 with the change and show the changed list again.

Done when the user has approved the list, or declined every verdict.

## 6. Act on the approved verdicts

Create the `retro` and `retro-planning` labels if the repo lacks them.

- **Each Ticket**: file it with `to-tickets`' issue template, including its `**Model tier:**` line. Label it `ready-for-agent` (the string `docs/agents/triage-labels.md` maps it to, if the repo has that file). Its done condition goes in the acceptance criteria. Link each Retro issue it absorbs, and add a criterion that those issues close with the Ticket (list them as `Closes #<n>` in the pull request that closes the Ticket). On each absorbed issue, comment `Absorbed by #<ticket>; closes when it closes.`
- **`wontfix`**: comment the reason, add the `wontfix` label (the string `docs/agents/triage-labels.md` maps it to, if the repo has that file), and close.
- **Expire**: comment `No new vote across 2 plannings. Reopen if seen again.` and close.
- **Close with its Ticket**: comment `Closed with #<ticket>.` and close.
- **Held back by the cap**, or declined: leave open.

Done when every approved verdict is carried out and each issue's state matches its verdict.

## 7. File the record

End every planning by filing the record, also when the user declined every verdict: it starts `retro`'s clock again and advances the expiry counts. File it in the format below, then close it at once. Give the user its link.

Done when the record is filed and closed, and the user has its link.

## The record

A **closed** issue titled `Retro planning <yyyy-mm-dd>` (today's date), labelled `retro-planning`. The next planning reads only these records, so each section below is required, with "None" when empty:

```markdown
## Verdicts

| Group | Retro issues | Distinct threads | Verdict | Reason or Ticket |
|-------|--------------|------------------|---------|------------------|
| <root cause> | #12, #15 | 3 | Ticket | #40 |
| <root cause> | #13 | 1 | wontfix | <reason> |
| <root cause> | #14 | 2 | held back by the cap | |
| <root cause> | #16 | 1 | declined, kept open | |
| absorbed by a closed Ticket | #11 | 2 | closed with its Ticket | #31 |

## Held back by the cap

- <root cause>: #14

## Tickets filed

- #40 (<root cause>), absorbs #12, #15

## Earlier fixes rechecked

- #31: holding / came back (#17)

## Open issues: plannings without a new vote

- #14: 0
- #16: 1

## Waiting on open Tickets

- #18: #35
```

Every verdict appears, declined ones included. "Plannings without a new vote" covers every issue left open and not waiting on a Ticket: 0 if it had a new vote since the previous record or is held back by the cap, otherwise the previous record's count plus 1.
