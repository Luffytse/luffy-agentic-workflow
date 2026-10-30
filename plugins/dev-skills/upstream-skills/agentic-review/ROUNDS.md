# Rank, Rounds and the record

The Rank stage of [`agentic-review`](SKILL.md), the Round comment that records each Review, the Round loop with its stop rule, and filing Pre-existing Findings.

## Rank

You rank; no subagent. Over the Findings Verify kept:

1. **Dedupe.** Findings with the same Bug class and overlapping locations are one Finding: merge their locations and keep every Finder's name.
2. **Drop the dismissed.** A Finding already dismissed in an earlier Round or Ticket check (dropped by Verify, or a Nit marked "skip") is dropped, even if this Review's Verifier kept it.
3. **Hold the already raised.** A Finding already raised earlier (same Bug class, overlapping locations) is not reported again. It keeps its earlier id and stays open until fixed; an unfixed Important still blocks the stop. If this Review found new instances of its Bug class, add them to its locations in this Round's comment.
4. **Sort** by Severity: Important, then Nit, then Pre-existing.
5. **Cap the Nits** at 5, "fix" Nits first. The Nits cut by the cap are not reported and not recorded.

## The Round comment

Each Round posts exactly one comment on the pull request (`gh pr comment <number> --body-file <file>`, or the GitHub tool you have). It is the only record of the Round: a fresh session reads all of them to continue the Rounds, and `retro` reads all of them to find Bug classes that came up more than once. Keep the shape exact:

```
<!-- code-review kind=round round=2 depth=Standard head=<full sha> base=<sha reviewed from> -->
## Code review: Round 2 of at most 5 (Standard)

Reviewed: the whole pull request | the commits <base>..<head>
Result: clean | not clean, <n> Important open | 5-Round cap reached
Finders: standards, spec, adversarial (bugs and edge cases), adversarial (security and privacy)

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
| R2-1 | Important | unescaped user input | src/page.ts:42, src/list.ts:17 | open | spec Finder: name shown raw in HTML |
| R2-2 | Nit (fix) | mysterious name | src/split.ts:8 | open | standards Finder: `tmp` holds the shares |
| R2-3 | Nit (skip) | duplicated code | src/a.ts:3, src/b.ts:9 | dismissed | Verifier: two lines, extracting adds churn |
| R2-4 | Important | null dereference | src/load.ts:30 | dismissed | Verifier: dropped, the guard at src/load.ts:22 covers it |
| R2-5 | Pre-existing | float money math | src/money.ts:4 | open | to be filed after the last Round |
| R1-1 | Important | off-by-one | src/settle.ts:12 | fixed | fixed in <sha>, confirmed by Verifier |
```

- **Ids** are `R<round>-<n>` and never change; a Ticket check uses `T<ticket number>.<check>-<n>`, so the 3 checks of one Ticket never reuse an id. A Finding keeps its first id in every later comment.
- **Rows:** every Finding this Round raised or dismissed (a dropped Finding shows the Finder's proposed Severity), plus every earlier Finding whose status or locations changed in this Round.
- **Status** is `open`, `fixed` or `dismissed`. The latest comment that names an id holds its current status. `fixed` needs the fixing commit in the Note.
- **Note** names the Finder and gives the one-line reason (the Verifier's, for a dismissal).
- **Nit status.** Every Round posts its "skip" Nits as `dismissed` and its "fix" Nits as `open`. A "fix" Nit becomes `fixed` in the next Round's comment once its fix commit lands (that Round's Verifier may confirm it; otherwise you mark it with the commit). On a clean Round 2 to 5, make the final "fix" Nits commit before posting, and post those Nits as `fixed` with that commit in the Note. Round 1 always leads to Round 2, so its "fix" Nits stay `open` until Round 2's comment.

## The Round loop

A Round is **clean** when, after its Verify, no Important is open: it found no new Important, and every earlier one is confirmed fixed.

After each Round's report, the Important Findings and "fix" Nits are fixed and committed by whoever owns the code (in a build thread, its Implementer); "skip" Nits are left alone. Then:

- **Round 1** always leads to Round 2. Its fixes and its "fix" Nits are committed, and Round 2 reviews them.
- **Round 2 to Round 4**, if not clean: the fixes and "fix" Nits are committed, and the next Round reviews them.
- **Round 2 to Round 5**, if clean: its "fix" Nits go into one last commit that no further Round reviews, and the pull request is ready to merge.
- **Round 5**, if not clean: stop. No sixth Round. Tell the user which Bug classes and Findings kept coming up across the Rounds and why the fixes did not hold, and say the plan may need discussing before more fixes.

Each new Round starts at step 1 of [SKILL.md](SKILL.md#process) with brand-new Finders and Verifiers.

## Filing Pre-existing Findings

Once the pull request's last Round is done (clean, or the cap reached), gather every open Pre-existing Finding from all the Round and Ticket-check comments and group them by Bug class. For each Bug class:

1. Look for an open issue already tracking it; if there is one, comment there with the new locations instead.
2. Otherwise file one issue with the tracker workflow: title `<Bug class> (found in review of #<pr>)`, a body listing every location with its claim, failure scenario and evidence and linking the pull request, and the label the repo uses for `needs-triage` (from `docs/agents/triage-labels.md`; `needs-triage` if that file is missing).

Then post one short comment on the pull request, starting `<!-- code-review kind=pre-existing -->`, listing each Finding id with the issue it went to.

## Ticket checks

A Ticket check is one Quick Review over a Ticket branch's diff, not a Round. Record its Findings as one comment on the Spec's pull request, in the Round comment shape with marker `<!-- code-review kind=ticket-check ticket=<number> check=<1-3> depth=Quick head=<sha> -->` and ids `T<ticket>.<check>-<n>`. If the Spec's pull request is not open yet, post it once it opens. Each later check of the same Ticket, and each of the Spec pull request's Rounds, treats these Findings as already raised: their open Importants go to Verify to be re-checked, and stay open until confirmed fixed. Pre-existing Findings from Ticket checks wait and are filed with the Spec pull request's, after its last Round.
