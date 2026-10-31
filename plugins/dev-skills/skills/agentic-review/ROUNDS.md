# Rank, Rounds and the record

The Rank stage of [`agentic-review`](SKILL.md), the Round comment that records each Review, the Round loop with its stop rule, and filing Pre-existing Findings.

## Rank

You rank; no subagent. Two locations **match** when they are in the same file with overlapping lines and their Findings make the same claim, whatever Bug class each Finder gave: wording the same problem as another Bug class does not make it new, and the same Bug class alone is not enough. Compare lines at this Review's head. An earlier row's lines, a partly fixed row's fixed locations in its Note included, are counted at the head of the latest comment naming its id, so first bring each to this head with `git diff -U0 <that head>..HEAD` on its file: shift it by the lines added minus removed in the hunks above it (a hunk that only adds lines is above it when it lands before that line); a line inside a hunk becomes that hunk's lines at this head (for a hunk that only removes, the line above, or line 1 at the start of the file). Over the Findings Verify kept, match location by location:

1. **Dedupe.** Findings with matching locations are one Finding: merge their locations and keep every Finder's name. Two different claims on one line stay two Findings.
2. **Drop the dismissed.** A location matching a Finding already dismissed in an earlier Round or Ticket check (dropped by Verify, an earlier open Important a Verifier dismissed as never real, a Nit marked "skip", or a design Finding the user settled by keeping the design) is dropped, even if this Review's Verifier kept it, but only while neither the code at the dismissed Finding's locations nor the code its reason rests on (the lines its Note cites) has changed since the head of the comment that dismissed it. Test it with `git diff -U0 <that head>..HEAD` on those files: any hunk touching those lines, counted at that head, counts, and so does a hunk that only adds lines between two of them or inside a cited range; this change test shifts no lines. If a line changed, or a dismissed "skip" Nit now reads as Important, judge the location afresh (it stays as a new Finding with a new id, not dropped). A dismissal's Note cites the lines its reason rests on, as row R2-4 below does; when a Verifier's dismissal cites none, any change to a file named in its locations since that head means judge afresh; a design Finding the user kept rests on its locations alone and binds while they are unchanged. The Finding's other locations stay, so a new instance of a dismissed claim is reported; a Finding left with no location is dropped.
3. **Hold the already raised.** A Finding with a location matching an earlier `open` row is held under that row: it keeps the earlier id and stays open until fixed, and is reported again only when raised; an unfixed Important still blocks the stop. Add its other locations to the row in this Round's comment, except one that a partly fixed row dropped (a regression, below). When this Review's Verifier gives it a Severity that step 4 sorts before the row's (Nit to Important, or Pre-existing to caused by this change), raise the row to it in this Round's comment and report it; a raised Important counts toward the stop rule. A lower Severity leaves the row as it is. A `fixed` row holds nothing, nor does a location a partly fixed row dropped: the same claim there again is a regression, a new Finding with a new id.
4. **Sort** by Severity: Important, then Nit, then Pre-existing.
5. **Cap the Nits** at 5, "fix" Nits first. The Nits cut by the cap are not reported and not recorded.

## The Round comment

Each Round posts exactly one comment on the pull request (`gh pr comment <number> --body-file <file>`, or the GitHub tool you have). It is the only record of the Round: a fresh session reads all of them to continue the Rounds, and `retro` reads all of them to find Bug classes that came up more than once. Keep the shape exact:

```
<!-- code-review kind=round round=2 depth=Standard head=<full sha> base=<sha reviewed from> -->
## Code review: Round 2 of at most 5 (Standard)

Reviewed: the whole pull request | the commits <base>..<head> | the merge from main <base>..<head> (merge-only Round)
Result: clean | not clean, <n> Important open | 5-Round cap reached
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

- **Depth** in the marker and the heading is the depth this Round ran at: the carried depth, or Quick for a merge-only Round.
- **Ids** are `R<round>-<n>` and never change; a Ticket check uses `T<ticket number>.<check>-<n>`, so the 3 checks of one Ticket never reuse an id. A Finding keeps its first id in every later comment.
- **Rows:** every Finding this Round raised or dismissed (a dropped Finding shows the Finder's proposed Severity), plus every earlier Finding whose status, Severity or locations changed in this Round.
- **Status** is `open`, `fixed` or `dismissed`. The latest comment that names an id holds its current status and Severity. `fixed` needs the fixing commit in the Note. A row the Verifier calls partly fixed stays `open` with only its live locations in Locations (the same Finding, not a regression) and its Note names each fixed one as `file:line` with its commit; it becomes `fixed` when none is left.
- **Note** names the Finder and gives the one-line reason (the Verifier's, for a dismissal, with the lines it rests on as `file:line`). A Pre-existing row's Note gives its claim and failure scenario in short, because filing it may fall to a fresh session that has only the comments ([Filing Pre-existing Findings](#filing-pre-existing-findings)).
- **Nit status.** Every Round posts its "skip" Nits as `dismissed` and its "fix" Nits as `open`. A "fix" Nit becomes `fixed` in the next Round's comment once its fix commit lands (that Round's Verifier may confirm it; otherwise you mark it with the commit). On a clean Round 2 to 5, make the final "fix" Nits commit before posting, and post those Nits as `fixed` with that commit in the Note. Round 1 always leads to Round 2, so its "fix" Nits stay `open` until Round 2's comment. A design "fix" Nit is `dismissed` once the user keeps the design, not `fixed` ([Design Findings go to the user](#design-findings-go-to-the-user)).

## The Round loop

A Round is **clean** when, after its Verify, no Important is open: it found no new Important (a design Finding it raised that the user then kept counts as none), and every earlier one is confirmed fixed, or dismissed by a Verifier as never real or because the user kept the design.

After each Round's report, the Important Findings and "fix" Nits are fixed and committed by whoever owns the code (in a build thread, its Implementer); "skip" Nits are left alone. On a pull request that changes design, the Findings that question the design go to the user first ([Design Findings go to the user](#design-findings-go-to-the-user)). Then:

- **Round 1** always leads to Round 2, even when the user keeps the design on every design Finding. Its fixes and its "fix" Nits are committed, and Round 2 reviews them.
- **Round 2 to Round 4**, if not clean: the fixes and "fix" Nits are committed, and the next Round reviews them.
- **Round 2 to Round 5**, if clean: its "fix" Nits go into one last commit that no further Round reviews, and the pull request is ready to merge. An agreed change to the design gets one more Round instead ([Design Findings go to the user](#design-findings-go-to-the-user)).
- **Round 5**, if not clean: stop. No sixth Round. Tell the user which Bug classes and Findings kept coming up across the Rounds and why the fixes did not hold, and say the plan may need discussing before more fixes.

Each new Round starts at step 1 of [SKILL.md](SKILL.md#process) with brand-new Finders and Verifiers.

## Design Findings go to the user

A pull request changes design when it adds or edits an ADR, the glossary, a spec or a design doc, a lone Ticket's pull request that edits one included. On such a pull request, sort each Important and "fix" Nit after Rank:

- **Design:** a Finding that questions the design itself, such as a gap in the agreed behaviour, two rules that conflict, or a case the design leaves unsettled. Its fix would record a decision, and the decisions are the user's. When unsure, treat the Finding as design.
- **Text:** every other Finding, wording, citations and index lines included. These are fixed as usual.

Put the design Findings to the user as the `grilling` skill puts a round: each one a numbered grilling question with your recommended answer, at most 3 at a time. Ask the next ones once the user answers, with any new questions the answers raise, and go on until the user says nothing more is worth settling. Then the owner of the code commits only the agreed answer for each, with the text Findings' fixes, and the next Round reviews them. Once the user answers, edit that Round's own comment, which stays its one comment (`gh api -X PATCH repos/<owner>/<repo>/issues/comments/<id> -f body=...`, or the GitHub tool you have); a Ticket check's comment is edited the same way, and one not posted yet is posted with these rows already settled. Each row the user settled by keeping the design becomes `dismissed`, with "user keeps the design" in the Note. Then recount the `<n> Important open` in its `Result:`; from Round 2 on, if none is left, `Result:` becomes `clean`.

Waiting on the user's answers is not a Round. An agreed answer that changes the pull request always gets one more Round, within the 5-Round cap, even after a clean Round: a "fix" Nit that questions the design goes to the user, not into the unreviewed last commit. When no Round is left (the answer comes at Round 5), commit it and bring the pull request to the user, saying plainly that the change is unreviewed. Extra Rounds for this are expected; what matters is that the user agrees at the end. When the user keeps the design on every open design Finding and no other Important is open, nothing is committed for them: they become `dismissed` ("user keeps the design"), and from Round 2 on the Round counts as clean and the pull request is ready to merge (Round 1 still leads to Round 2). A Ticket check of a Ticket that changes design follows the same rule before the next check.

## Merge-only Rounds

A **merge-only Round** is a Round 3 to 5 whose new commits since the last Round are only a merge from main. When that merge's conflicts were only in text (wording, cross-references, entries that both sides added), it runs at **Quick** depth (standards and spec Finders, one Verifier), not the carried depth: it reviews only what the merge changed in the pull request (its conflict resolutions), with the diff command in [SKILL.md step 1](SKILL.md#1-pin-the-diff). If any resolution touches logic (code behaviour, a check, or what a rule means), it runs at the carried depth instead. Its comment's marker and heading say the depth it ran at; its `Reviewed:` line says merge-only Round, and the Round after it takes the carried depth from the latest comment that is not a merge-only Round's. A merge-only Round is a Round like any other: it counts toward the 5-Round cap and follows the Round loop above.

## Filing Pre-existing Findings

Once the pull request's last Round is done (clean, or the cap reached), gather every Finding whose latest row in the Round and Ticket-check comments is an open Pre-existing one and group them by Bug class. For each Finding, take its claim, failure scenario and evidence from the Review's own Findings when this session still has them; otherwise take the claim and failure scenario from its Note, and the evidence by quoting the code at its locations. For each Bug class:

1. Look for an open issue already tracking it; if there is one, comment there with the new locations instead.
2. Otherwise file one issue with the tracker workflow: title `<Bug class> (found in review of #<pr>)`, a body listing every location with its claim, failure scenario and evidence and linking the pull request, and the label the repo uses for `needs-triage` (from `docs/agents/triage-labels.md`; `needs-triage` if that file is missing).

Then post one short comment on the pull request, starting `<!-- code-review kind=pre-existing -->`, listing each Finding id with the issue it went to.

## Ticket checks

A Ticket check is one Quick Review over a Ticket branch's diff, not a Round. Record its Findings as one comment on the Spec's pull request, in the Round comment shape with marker `<!-- code-review kind=ticket-check ticket=<number> check=<1-3> depth=Quick head=<sha> -->` and ids `T<ticket>.<check>-<n>`. If the Spec's pull request is not open yet, post it once it opens. Each later check of the same Ticket, and each of the Spec pull request's Rounds, treats these Findings as already raised: their open Importants go to Verify to be re-checked, and stay open until confirmed fixed, or dismissed by a Verifier as never real or because the user kept the design. Pre-existing Findings from Ticket checks wait and are filed with the Spec pull request's, after its last Round.
