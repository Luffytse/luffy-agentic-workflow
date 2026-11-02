# Mixed final-range Git histories

Seam: given a clean Round's pinned head and actual Git history, classify the final range, pin all review patches, choose depth and apply the existing Round budget. This is a bounded manual workflow check; the builder tests Git plumbing, not skill prose or agent decisions.

Run `python3 evals/agentic-review/final-range/make-fixture.py <new-directory>` outside this repo. Each case creates its own repository on `ticket`, a `last-reviewed` tag, and `.git/scenario.json` with exact SHAs. `.git/round.md` pins the clean Deep Round 5 and any checked R5-1 fixing commit; `.git/release.md` supplies version-only authority. `.git/review-range.patch` is the actual output of `git log -p --first-parent --remerge-diff <last-reviewed>..HEAD`. The builder checks that own patches, including a superseding bump after the merge, are present and an imported main patch is absent.

For each case read that output, the preceding clean Round record (assume Deep, R5, `head=last-reviewed`, and R5-1 fixed by the named spelling commit when present), and a release doc requiring only the `version.json` value to change. Apply `agentic-review`'s Merge-only Rounds owner. Report each commit's category and authority, the entire Reviewed range, depth/marker/heading, and outcome. Repeat at R2 to check ordinary budget remains available. Keep the expected table below away from an agent under test.

| Case | Expected decision after clean R5 |
| --- | --- |
| bump-text | bump plus text resolution, one late R6 at Quick; both patches reviewed |
| nit-text | R5-1 spelling fix plus text resolution, one late R6 at Quick; marker still pins pre-Nit head, both patches reviewed |
| both-logic | Nit, bump, rule-meaning resolution and superseding bump after merge, one late R6 at Deep; all four patches reviewed |
| disguised-logic | alleged bump includes `check.sh`, ineligible; no R6, end attempt |
| unrelated-clean | unrelated logic plus conflict-free merge, ineligible; no R6, end attempt |

For each qualifying case, a non-clean late Round ends the attempt; a further conflicting merge after its clean late Round also ends it with no R7. `restart` when the built issue has no earlier attempt, `park` when it has one or the pull request builds no issue. At R2, the two ineligible cases instead take ordinary R3 at Deep over the full range. Following a Quick merge-only R3, ordinary R4 restores Deep from R2. After a late design R6, a qualifying range uses the sole late merge-only R7; no R8 is available. These are manual continuation decisions, not histories built by the script.

Record observed traces and limits in [../RESULTS.md](../RESULTS.md). This check does not run fresh Finders/Verifiers, post tracker records, exercise live CI, prove installed-runtime loading or replace the full Standard/Deep planted-Finding eval.
