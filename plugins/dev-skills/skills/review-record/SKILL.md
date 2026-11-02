---
name: review-record
description: Interpret review records. Use when writing or reading Round or Ticket-check comments or attempt records, or supplying Bug class and Always-check meaning to reviewers.
user-invocable: false
---

The shared contract for review comment writers and readers. Review orchestration, ranking, fix timing and filing belong to `agentic-review`; grouping recurring problems and choosing preventive checks belong to `retro`. Loading this reference starts neither workflow.

## Terminology

A **Finding** is one reported problem, with a Severity, Bug class, Locations and Failure scenario. A **Bug class** names the kind of problem (for example “unescaped user input”), so every place it occurs can be fixed together. A **Failure scenario** gives the inputs or state and wrong result; a cleanup Finding states its cost instead.

A **Severity** is Important, Nit or Pre-existing. Important must be fixed before merge or acceptance, Nit is real but small and optional, and Pre-existing is real but not caused by the change. The review workflow applies the project's meaning of Important and decides a Nit’s fix/skip disposition.

An **Always-check line** in the repo's `REVIEW.md` names a Bug class earlier Reviews caught more than once and what to look for. Reviewers need this meaning and the project's actual lines; the review workflow owns checking them, and retro owns adding or repairing preventive checks.

## Comment shape

Record comments start with the marker on their first line. A Round uses this exact shape; the workflow chooses Result, depth, Reviewed scope and Finders:

```
<!-- code-review kind=round round=2 depth=Standard head=<full sha> base=<sha reviewed from> -->
## Code review: Round 2 of at most 5 (Standard)

Reviewed: the whole pull request | the commits <base>..<head> | the merge from main <base>..<head> (merge-only Round)
Result: clean | not clean, <n> Important open | 5-Round cap reached | attempt ended: <restart | park> (<cause>)
Finders: standards, spec, adversarial (bugs and edge cases), adversarial (security and privacy)

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
| R2-1 | Important | unescaped user input | src/page.ts:42, src/list.ts:17 | open | spec Finder: name shown raw in HTML |
| R2-2 | Nit (fix) | mysterious name | src/split.ts:8 | open | standards Finder: `tmp` holds the shares |
| R2-3 | Nit (skip) | duplicated code | src/a.ts:3, src/b.ts:9 | dismissed | Verifier: two lines, extracting adds churn |
| R2-4 | Important | null dereference | src/load.ts:30 | dismissed | Verifier: dropped, the guard at src/load.ts:22 covers it |
| R2-5 | Pre-existing | float money math | src/money.ts:4 | open | adversarial Finder: shares summed as floats; a 0.10 bill split three ways loses a cent |
| R1-1 | Important | off-by-one | src/settle.ts:12 | fixed | fixed in <sha>, confirmed by Verifier |
```

- **Result** values: `clean`; `not clean, <n> Important open`; `5-Round cap reached`; and, inside a Milestone, for the Round that ends an attempt, `attempt ended: restart (<cause>)` or `attempt ended: park (<cause>)`, the cause being `a Finding returned`, `a fix flipped back`, `5-Round cap reached` or `late design Round did not settle`. A returned or flipped row's Note says "returned: <earlier id>" or "flipped: <earlier id>".
- **Late design Round.** Inside a Milestone, the one Round after Round 5 is Round 6, with `round=6` in the marker and the heading `## Code review: Round 6, late design Round (<depth>)`.
- **Ids** are `R<round>-<n>` and never change; a Ticket check uses `T<ticket number>.<check>-<n>`, so the 3 checks of one Ticket never reuse an id. A Finding keeps its first id in every later comment.
- **Rows:** every Finding the Review raised or dismissed (a dropped Finding shows the Finder's proposed Severity), plus every earlier Finding whose status, Severity or locations changed in this Review.
- **Status** is `open`, `fixed` or `dismissed`. The latest Round or Ticket-check comment that names an id holds its current status and Severity. An `open` row closes only as `fixed` (a Verifier confirms the fix, or for a "fix" Nit under the review workflow’s Nit-status rules) or as `dismissed` (a Verifier dismisses it as never real, a rebuttal Verifier inside a Milestone included, the user keeps the design or, inside a Milestone, an agent keeps it within what the user agreed, or the review workflow’s Rank step 3 merges it into another row), save a row whose rebuttal was rejected, which closes only as `fixed` or merged (see Note). `fixed` needs the fixing commit in the Note. A row found partly fixed (by the Verifier, or for a "fix" Nit under the review workflow’s Nit-status rules) stays `open` with only its live locations in Locations (the same Finding, not a regression) and its Note names each fixed one as `file:line` with its commit; it becomes `fixed` when none is left. A Pre-existing row stays `open` once it is **filed** as an issue: the problem is still in the code, and a later Finding with its claim is still held under it (the review workflow’s Rank step 3). Filing writes no status; the `kind=pre-existing` comment the Filing step posts records which Findings are filed (the filing receipt below).
- **Note** names the Finder and gives the one-line reason (the Verifier's, for a dismissal, with the lines it rests on as `file:line`). A design row says who answered it: “user keeps the design”, or inside a Milestone “user answers: <change>”, “agent keeps the design: <reason>, <link to the record>” or “agent answers: <change>, <link to the record>”, the record being the answer's comment on the spec issue. Inside a Milestone, a row whose rebuttal a premium-tier Verifier decided says so: “rebuttal upheld: <reason>, rests on <file:line>, ...” on a `dismissed` row (the Verifier's reason and the lines it rests on), or “rebuttal rejected: <reason>” on a row that stays `open`. Once any comment's row for an id notes “rebuttal rejected”, that Finding cannot be rebutted again, whatever later Notes say, nor can a row it is merged into, and it closes only as `fixed` or merged, never as dismissed by a later Verifier. A Pre-existing row's Note gives its claim and Failure scenario in short, because filing it may fall to a fresh session that has only the comments (the filing receipt below).

A Ticket-check comment uses the same fields and table with marker `<!-- code-review kind=ticket-check ticket=<number> check=<1-3> depth=Quick head=<sha> -->`. It records a check, not a Round.

An **attempt record** is a comment on the issue the pull request builds (the lone Ticket, or the Spec of a Spec pull request), not on the pull request, written when a review inside a Milestone ends an attempt. It uses this shape:

```
<!-- code-review kind=attempt attempt=1 pr=<number> head=<full sha> -->
## Review attempt 1: restart

Pull request: <link>
Rounds: 1 to 3 (Standard)
Ended by: a Finding returned
Outcome: restart
Earlier attempts: none

| id | Severity | Bug class | Locations | How | Claim |
|----|----------|-----------|-----------|-----|-------|
| R3-1 | Important | unquoted variable | src/backup.sh:9 | returned R1-1 | a list path with a space splits into two arguments |
| R3-2 | Important | file permissions | src/backup.sh:7, src/backup.sh:9 | open | backups are readable by every user on the machine |

Tried: R1-1 fixed in <sha> by quoting both paths; the R2-1 fix in <sha> rewrote the cp line without them.
Lesson: <why the fixes did not hold, and what the next attempt should do differently>
Untouched: README.md, tests/backup.sh
```

- **attempt** is one more than the number of attempt records already on the issue, not counting a record whose marker names this pull request and head (a resumed session reuses that record); **Outcome** is `restart` for attempt 1 and `park` for any later one, the same outcome the ending Round's Result names. **Ended by** is that Result's cause. **Earlier attempts** links each earlier record, or says none.
- **Rows** are the Findings the attempt ended on: each returned or flipped Finding, its How `returned <earlier id>` or `flipped <earlier id>`, and every other Important still open, its How `open`. Locations are counted at the record's `head`. Claim is one line.
- **Tried** names the fix commits for those Findings and the rows they matched; **Lesson** says why those fixes did not hold; **Untouched** lists the files of the pull request's diff that no open Important or "fix" Nit names (candidates to split off and keep), or none.

A filing receipt starts `<!-- code-review kind=pre-existing -->` and has one line per Finding filed or given new locations: its id, the issue it went to, and the locations sent there this time. A receipt changes no Finding status and is not a Finding table.

## Reading successive comments

Read all pages of comments in chronological order. Attempt records are read from the issue's comments, not the pull request's: read every one, as one history of the problem, whatever pull request, Ticket or agent wrote it; their count gives the next attempt number, and their returned and flipped rows are what a later attempt's Finding can return to (the review workflow's convergence check). Finding tables come from bodies starting `<!-- code-review kind=round` or `<!-- code-review kind=ticket-check`; a Spec pull request includes its Ticket checks. Keep one row per id. The latest comment naming that id supplies current Severity, Status, Note and Locations. An omitted id retains its prior row. Locations are counted within their file at the head recorded in that comment; the review workflow brings them to the current head before matching code. A merged row's Note names its holding id, whose live Locations carry the problem forward.

For a retrospective's historical view, use that latest Severity and Status but union every location listed for the id across all kept comments. Keep open and fixed Findings, `Nit (skip)` Findings and Pre-existing Findings. Exclude a `dismissed` row with Severity other than `Nit (skip)` unless its Note says “user keeps the design” or “agent keeps the design”: these design questions remain real for retrospection. This also excludes a merged-away row; its locations survive under the holding Finding. Historical locations include fixed instances, whereas a partly fixed current row lists only live locations. The retro workflow groups the retained rows and selects guardrails.
