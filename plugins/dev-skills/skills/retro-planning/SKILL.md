---
name: retro-planning
description: "Sort this repo's Retro backlog unattended: group open Retro issues by root cause, close one-offs, hand repeated or severe ones to triage, and record the run. Use for Retro planning, at a Release end before the Triage batch, or to finish a run whose record is still open."
---

A **Retro planning** sorts one repo's **Retro backlog** (its open issues labelled `retro`): it closes what was seen once and hands what repeated or is severe to `triage`, whose Triage batch writes the brief. It runs one way, whoever starts it: the Release thread runs it at a Release end, before the Triage batch, and anyone may ask for one at any other time. It asks the user nothing and waits for nothing.

Sort only the current repo. Its tracker is named in `docs/dev-skills/issue-tracker.md`; with no such file, use the GitHub repo of the checkout's `origin` remote. Read and write only that repo's issues, with the commands that file gives; the one exception is refiling a misplaced Retro (step 2). Role names map to label strings through `docs/dev-skills/triage-labels.md`.

## 1. Open the record

An open issue labelled `retro-planning` is a run that stopped part way: continue in it. A group with a row is done. Each `retro` issue closed, or given `needs-triage`, since the record was created and still without a row gets its row now, from its comments. An open record with no `## Groups` heading is in an older format: close it with a comment that this run replaces it, and file a new one.

Otherwise file the record: an **open** issue titled `Retro planning <yyyy-mm-dd>`, labelled `retro-planning`, with the format in "The record" and no rows yet. Create the `retro` and `retro-planning` labels if the repo lacks them.

Done when exactly one open record exists.

## 2. Read the backlog

Read every open issue labelled `retro`, with its body and comments. Load `issue-absorption` and leave out, untouched, each issue that:

- carries a state role: it was handed over already. An open issue with `wontfix` is the exception: `retro` reopened an old close, so remove that label and sort it.
- has a latest `Absorbed by #<ticket>` comment naming a Ticket that is open, as `issue-absorption` reads it. It is neither closed, merged nor handed over; it closes with that Ticket.

List them in the record under "Left as it is". These are the only places this skill reads an absorption comment; it writes none.

Give each remaining issue its **Scope** (`skill`, `environment` or `this repo`) from its `Scope:` line; with none, decide it by `retro`'s question (would this happen in a fresh repo using the skills, in the same environment?). A Retro whose Scope does not belong in this tracker (a `this repo` Retro of another repo, or a `skill` or `environment` Retro outside the plugin's repo) is refiled: for `skill` or `environment`, in the repo the plugin manifest's `repository` field names, as `retro`'s filing step does; for `this repo`, in the tracker of the project its source thread names. File it there with the label `retro` and no state role, then close it here with the link. If you cannot write there, leave it open and record it as `misplaced, not refiled`.

Count each issue's **threads**: the source thread its body names, plus the thread of each `Seen again in <thread link>` comment. A thread counts once, however many comments it left.

Done when every open `retro` issue is left out, refiled or has its Scope and thread count.

## 3. Group and decide

Group the issues by Scope, then by root cause; a group never mixes Scopes. Within a group, keep the fullest issue: close each other one as a duplicate (as not planned where the tracker has no duplicate outcome), with a comment linking the kept issue, and comment on the kept issue anything only the closed one said. The group's count is its distinct threads across all its issues.

**Hand a group to triage** when it:

- was seen in 2 or more distinct threads,
- is **severe**: lost data, a security problem, or a large waste of time or money, or
- holds an issue reopened after its fix merged: its latest `Absorbed by #<ticket>` comment names a Ticket closed as completed, and the issue is open again.

Hand it over by applying the `needs-triage` role to the kept issue, keeping the `retro` label, with a comment giving the threads and the reason. The Triage batch decides it from there; write no brief, file no Ticket and set no `next-release` mark.

**Close** every other group (one thread, not severe): comment the reason and `A new sighting reopens it.` on the kept issue, then close it as not planned, with no label added.

Carry out each group at once and add its row to the record before the next. The Outcome is `handed to triage`, `closed`, `refiled` or `misplaced, not refiled`.

Done when every group has its row.

## 4. Close the record

Close the record and give its link to the caller (the Release thread links it from the release issue) or to the user who asked.

Done when the record is closed and its link given.

## The record

```markdown
Run: <date and time>; Release: <name, or "none">

## Groups

| Retro issues (kept first) | Scope | Threads | Outcome | Reason |
|---------------------------|-------|---------|---------|--------|
| #12, #15 | skill | 3 | handed to triage | <root cause> |
| #13 | this repo | 1 | closed | <root cause; why one sighting is enough to close> |
| #21 | skill | 1 | refiled | <link> |

## Left as it is

- #18: absorbed by open #35
- #19: carries `ready-for-agent`
```

A run with nothing to sort writes "None" under each heading. Records written before this format are not read.
