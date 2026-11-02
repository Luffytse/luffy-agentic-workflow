# Merge-only depth decision probe

Confirmed seam: application of the Round-comment Depth summary to resolution depth and record metadata. This isolates the summary entry point; it does not exercise actual merges, diff pinning, Find/Verify, external posting or installed-runtime loading.

Give a fresh agent the current `ROUNDS.md` Depth summary bullet, its Merge-only Rounds section available for pointer lookup and the continuation, and the Round heading shape in `review-record`. Give it the prompt below, keeping the scoring table away from it. Run before and after editing the summary; record the actual returned decisions in `../RESULTS.md`. A run that repairs the contradiction itself may pass before the fix; report that honestly.

## Prompt

Apply the Round-comment Depth summary as entry point, following any pointer it contains; do not repair contradictions from unreferenced text. Round 2 was an ordinary Round at Deep; no user changed depth. In each independent case Round 3 contains only a merge from main with conflicts:

- A: a spelling correction and cross-reference; no rule meaning changes.
- B: a shell check resolution changes which exit codes count as failure.
- C: a Markdown rule resolution changes who may merge a pull request.

For each give the run depth, marker `depth=` field and full heading. Then use the Merge-only Rounds section for a continuation: after A, Round 4 contains an ordinary fix commit, with no merge. Give its depth, marker depth and heading, and which earlier comment supplies its carried depth. Run no Find/Verify and post nothing externally.

## Scoring

All four rows must pass, including agreement of run depth, marker and heading:

| Case | Run depth | Marker | Heading |
| --- | --- | --- | --- |
| A | Quick | `depth=Quick` | `## Code review: Round 3 of at most 5 (Quick)` |
| B | Deep | `depth=Deep` | `## Code review: Round 3 of at most 5 (Deep)` |
| C | Deep | `depth=Deep` | `## Code review: Round 3 of at most 5 (Deep)` |
| Following ordinary Round | Deep from Round 2 | `depth=Deep` | `## Code review: Round 4 of at most 5 (Deep)` |

The unconditional summary can produce Quick for B/C: this is the red failure, even though the owner section already states the right exception.
