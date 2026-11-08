---
name: review-record
description: Interpret review records. Use when writing or reading Round or Ticket-check comments, or supplying Bug class and Always-check meaning to reviewers.
user-invocable: false
---

The shape of the comments a review posts, and how to read them back. Running the review belongs to `agentic-review` and `review-rounds`; grouping recurring problems belongs to `retro`. Loading this reference starts neither.

## Terminology

A **Finding** is one reported problem, with a Severity, Bug class, Locations, a claim and a failure scenario. A **Bug class** names the kind of problem (for example "unescaped user input"), so every place it occurs can be fixed together. A **failure scenario** gives the inputs or state and the wrong result; a cleanup Finding states its cost instead.

A **Severity** is Important, Nit or Pre-existing. Important must be fixed before merge, Nit is real but small and optional, and Pre-existing is real but not caused by the change. A Nit is `Nit (fix)` or `Nit (skip)`.

An **Always-check line** in the repo's `REVIEW.md` has the form `- **<Bug class>** (files: `glob`, `glob`; from ...): what to look for`: it names a Bug class earlier reviews caught more than once, the globs of the files it applies to, and what to look for; `(files: all)` applies it to every diff.

## Round comment

One comment per Round on the pull request. Its first line is the marker:

```
<!-- code-review kind=round round=2 level=Standard head=<full sha> base=<sha reviewed from> -->
## Code review: Round 2 of at most 3 (Standard)

Level: Standard (changes what the export rule does)
Reviewed: the whole pull request | the new commits <base>..<head>
Result: clean | not clean, <n> Important open
Finders: standards and spec
Verifier: ran

| id | Severity | Bug class | Locations | Claim | Status | Note |
|----|----------|-----------|-----------|-------|--------|------|
| R2-1 | Important | unescaped user input | src/page.ts:42, src/list.ts:17 | a name is shown raw in HTML | open | spec Finder |
| R2-2 | Nit (fix) | mysterious name | src/split.ts:8 | `tmp` holds the shares | fixed | standards Finder; fixed in <sha> |
| R2-3 | Nit (skip) | duplicated code | src/a.ts:3, src/b.ts:9 | two copies of one check | dismissed | Verifier: two lines, extracting adds churn |
| R2-4 | Important | null dereference | src/load.ts:30 | a missing file crashes the load | dismissed | Verifier: the guard at src/load.ts:22 covers it |
| R2-5 | Pre-existing | float money math | src/money.ts:4 | a 0.10 bill split three ways loses a cent | open | adversarial Finder |
| R1-1 | Important | off-by-one | src/settle.ts:12 | the last creditor is never paid | fixed | fixed in <sha>, confirmed by Verifier |
```

- **Round 0 at None** posts one line, `agentic-review`'s, and it is the whole review: its marker reads `kind=round round=0 level=None` and it has no table.
- **Level** is None, Quick, Standard or Deep, with Round 0's one-line reason. Older comments say `depth=` in the marker; read it as the level.
- **Ids** are `R<round>-<n>`; a Ticket check uses `T<ticket number>.<check>-<n>`. A Finding keeps its first id in every later comment.
- **Locations** are `file:line` or `file:start-end`, counted within the file at the comment's head.
- **Verifier** is `ran`, or `none (no candidates, no open Finding)` when no Finder returned a candidate and no earlier Finding was open, so no candidates went to a Verifier; the table then has no rows. A Round comment without the line ran its Verifier.
- **Rows:** every Finding this Round raised or dismissed, plus every earlier Finding whose status changed.
- **Status** is `open`, `fixed` or `dismissed`. `fixed` names the fixing commit in the Note. A dismissal's Note says who and why: `Verifier: <reason>, rests on <file:line>`; `design kept: <link to the answer>`; or `dismissed after Round 3: <reason>`. An Important that became a bug Ticket after Round 3 stays `open` with `bug Ticket: <link>` in its Note.
- **Note** starts with the Finder that raised the Finding, or with who closed it; keep it short.
- **Result** after Round 3 is edited to `sorted after Round 3: <n> bug Tickets, <m> dismissed`. A review stopped for a person reads `waiting on a boundary: <what would be crossed>` until the user's answer, on the pull request after it, clears it.

## Ticket-check comment

The same table and fields, with the marker `<!-- code-review kind=ticket-check ticket=<number> check=<n> level=Quick head=<sha> -->` and the heading `## Ticket check: Ticket <number>`. It is posted on the Spec's pull request.

## Resolutions check

The one Quick check of a merge's conflict resolutions after Round 3 uses the same table and fields, the marker `<!-- code-review kind=resolutions level=Quick head=<sha> base=<sha> -->`, and ids `M-<n>`.

## Reading successive comments

Read every page of comments in order. Records are the bodies that start `<!-- code-review kind=`; a Spec pull request's include its Ticket checks. Keep one row per id: the latest comment naming the id gives its Severity, Status, Note and Locations, and an id a later comment leaves out keeps its row.

For a retrospective, keep every id with its latest Severity and Status and the union of every location listed for it across the comments. Leave out a `dismissed` row unless its Severity is `Nit (skip)` or its Note says `design kept` or `dismissed after Round 3` (a kept Important the sort dismissed): the others were never real, or were not judged.
