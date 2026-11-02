# Exhausted design-answer decision probe

Confirmed seam: a build caller receives an agreed design answer after the clean late Round has closed. This is a bounded workflow decision check, not a full Review, an installed-runtime dependency test, a merge or a tracker-write test. Use fresh agents, with this scoring section withheld, to apply the actual owner, callers and record contract. Keep the baseline immutable so later edits cannot leak into it. Record actual responses and limits in `../RESULTS.md`.

## Prompt

Read `agentic-review/ROUNDS.md`, `review-record/SKILL.md`, and the merge/restart steps in `implement/SKILL.md` and `implement-spec/SKILL.md` from the supplied source revision. Find/Verify are complete; run none and post nothing. A new agreed answer keeps the Milestone agreement and changes rule meaning after the last clean Round was already closed. It is not a final text Nit or a version bump; no main merge is present. For each independent case, state next action, whether any Round runs, attempt outcome and record destination/cause/head/answer linkage, and whether merge or a routine user merge decision is allowed:

- A: inside a Milestone, Ticket, clean late design Round 6; unused late merge-only allowance; no earlier attempt.
- B: A with an earlier failed attempt and the other late allowance already used.
- C: inside, Spec, clean late merge-only Round 6 after clean ordinary Round 5; late design allowance unused; no earlier attempt.
- D: inside, Ticket, clean late merge-only Round 7 after late design Round 6; no earlier attempt.
- E: inside, no-issue corrective check with recorded Retro origin; clean late design Round 6; earlier attempts exist only on the origin issue.
- F: inside, Ticket, clean ordinary Round 4; no earlier attempt.
- G: outside, Ticket, clean late design Round 6.
- H: outside, Ticket, clean late merge-only Round 6; late design allowance unused.
- I: A, except the answer keeps a design “fix” Nit and needs a lasting ADR record.

The baseline red probe can use A alone. Distinguish an answer received after a clean Round closed from an answer to an open Finding of that Round. Do not invent a policy when the source leaves a branch undefined.

## Scoring

A, C and D end the first issue attempt as `restart` with cause `agreed design change after last Round`; B is `park`. No new Round, unreviewed merge or routine user merge decision. An unused late allowance cannot cover the answer. The record goes on the built Ticket/Spec, preserves existing Finding ids/Severity and answer source/affected files/required ADR work, records only Rounds run and the current PR head, and conservatively has `Untouched: none`. Last clean Round Result and Find/Verify head remain unchanged. Resume reuses the same PR/head record.

E parks immediately on the corrective PR, with its Retro origin used only for membership/design-answer source, never as attempt history. I follows A, with the design Nit and needed ADR work recorded. F runs ordinary Round 5 at carried depth to review the change; it does not end an attempt for this cause. G and H retain the outside merge-list handoff to the user with the change explicitly unreviewed, without a new Round.

The baseline must expose the missing inside-Milestone trigger; an agent that infers a safe stop has not proved that the source supplied a restart/park record rule. Fixture plumbing is separate evidence from this decision check. No text-matching assertion is a behavioral substitute for the returned decisions.
