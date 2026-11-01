# Shared-rules final reconciliation

## 2026-10-31 — #370, Spec #348

Integrated baseline: `ee8e342fea6400eb437b754dfb534a7580b2524f`. ADR 0009's owner/consumer matrix records the completed #364/#365/#368/#369/#366 migrations. Each named Base has one contract body; consumers load it at the relevant write/read/check branch. Workflow procedures remain with their complete workflow; project operations/mappings remain with configured project documents. The authoring gate remains reusable guidance for future migrations, rather than a claim that this migration is pending.

Remaining references were classified by responsibility: owner-local reference/procedure, complete workflow invocation, direct interview composition, deferred retro follow-up build, independent caller policy, project configuration, and unrelated absorption word sense. None were deleted to meet a link-count target. `retro/BUG-CLASSES.md` retains preventive-check work; direct `grilling` plus `domain-modeling` remains. Unmigrated shared copies still require consistency checks. Same-file contradictions and stale repository descriptions remain covered by CLAUDE.md, REVIEW.md and writing-for-agents even for independent rules. The latter wording makes that continuing scope explicit; no agentic-review skill body, Finding/Verify semantics, fixture expectation or workflow behavior changes in this Ticket, so the completed fixture evaluations are not invalidated.

Evidence audit:

| Scope | Retained evidence and limits |
| --- | --- |
| Required loading gate #360 | `evals/skill-loading/RESULTS.md`: fresh actual GitHub candidate discovery/loading/application passed for small complete-workflow and reference cases; full production fact-finding branch unverified. Menu visibility optional and unmeasured. |
| Index #364 | Same results: writer and standards-checker read owner, preserve throwaway/test-input exceptions; narrowed-description writer recheck passed. Branch probes, not full review. |
| Review record #365 | `evals/review-record/README.md`: baseline/candidate answers and body-read evidence agree on identifiers, statuses, history, dismissal and filing receipt; full orchestration outside seam. |
| Absorption #368 | `evals/issue-absorption/RESULTS.md`: lifecycle, later authoritative record, recurrence, source body/comments and closing-line decisions; builder load points inspected, full builds not executed. |
| Retro handoff #369 | `evals/retro-handoff/RESULTS.md`: baseline red, single/multi, rejection/resume, partial publication and ordered record reconciliation; no real tracker transport/nonempty blockers. |
| Caller/configuration #366 | `evals/caller-cleanup/RESULTS.md`: six installed caller probes, custom tracker/roles and final local completion; restored positive merged-state gate checked on real merged/unmerged history. No full reviewer dispatch or merge lifecycle claim. |
| Full review fixture | `evals/agentic-review/RESULTS.md`: source 9b98dfe, Standard FAIL (known P4 discovery miss #376), Deep PASS including 2/3 Pre-existing attribution vote for P4. False alarms never raised, so no verified-drop coverage claimed. VERIFY unchanged, no required Verify-only. |

No new behavioral gap was introduced by this documentation reconciliation. Existing bounded evidence is retained with its limits, not relabeled as end-to-end proof; unchanged passing probes were not rerun. The coordinator's final clean remote-install evaluation is still pending against the published actual final Spec candidate. This record does not claim it happened.

The full `origin/main...HEAD` whitespace check exposed eight renderer-added final blank separators in absorption and skill-loading transcripts that working-tree-only checks had missed. Only those EOF separator runs were normalized to one newline; message bytes and internal separators were preserved. This corrects check scope and artifact formatting, requiring no behavioral rerun.

Visual check: not applicable to text/protocol artifacts. Door: two-way, reversible documentation and evidence changes; no external writes, issue closure, push or version change.

Validation: merged latest local Spec tip `ee8e342fea6400eb437b754dfb534a7580b2524f` (already up to date). Repository checker, all five disposable packaging tests, Claude marketplace/plugin validation, review-record baseline/candidate semantic scorer and absorption evidence scorer pass. Full committed `git diff --check origin/main...HEAD` is the required final whitespace scope. Same-file and repository restatement searches covered shared ownership, independent policies, migration status, contradictions, stale descriptions and visibility before committing.

### Ticket check 1 correction — T370.1-1

The first check found a missed parallel status sentence in the Base skill glossary entry: it still described ADR 0009 as planning the skills. It now names the three implemented Base skills and preserves protections for unmigrated shared copies. A fresh same-file and repository search checked planned-state/migration wording against the implemented inventory. This is status reconciliation only; no contract or workflow semantics changed, so no behavioral rerun is needed.
