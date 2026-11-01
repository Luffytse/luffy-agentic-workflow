# Results

## 2026-10-31 — #369 local candidate

Source baseline: `168084d9c32c3bbeb8a138cb46c91da845043d99`. Candidate: the same worktree plus this Ticket's skill changes before commit; installed file hashes in each `provenance.json` identify the exact tested content. This was a local checkout install, not a GitHub install. Model `regular Codex tier from plugins/dev-skills/README.md at 168084d9c32c3bbeb8a138cb46c91da845043d99`, provider default `openai`, fallback disabled; CLI identity is recorded per case. Every fresh runtime discovered all 27 installed plugin skills, enabled, with no discovery errors. No plugin version changed.

| Case | Observed result |
| --- | --- |
| Baseline | Red: caller drafted title, done condition and tier, then asked to file before invoking the complete preparation workflow. |
| Single | Problem-only decision first; actual installed `to-tickets` read after approval; separate concrete solution approval; exactly #21 created with source-body/comment requirements, `Closes #12`, ready label, absorption comment and verification. Record closed, 1/3 used, source open waiting. |
| Multi | Actual `to-tickets` read; investigation found expand/migrate/contract needed many Tickets; returned to spin-off decision with zero Tickets. Named spin-off recorded, cap stayed 3, source remained open, brief retained constraints. Detailed solution/budget left to spun-off planning. |
| Decline | Concrete solution rejected after problem approval. No Ticket or absorption comment, record open with both decisions and remaining budget 3. |
| Decline resume | Fresh runtime retained the rejection and problem approval and asked the pending alternative-result question. No writes or new Ticket; expected decision boundary reached. |
| Partial resume | Loaded `to-tickets`, repaired existing #21's label and absorption comment, verified and reconciled record, counted one actual Ticket. No duplicate or repeat approval. |
| Order | Repaired the partial #21, verified source agreement and updated #20 before presenting #13. Record counted 1/3. Stopped at the next verdict question with record open. |

Every captured candidate turn completed successfully. `issue-absorption` was observably loaded in all cases; `to-tickets` was observably loaded for preparation and publication repair. The decline-resume case stayed at its pending user decision without drafting or publishing. Source reports were linked absorbed issues, not parents. The fixture has no blockers; nonempty dependencies and real tracker transport remain outside this evaluation.

The first baseline attempt could discover skills but failed before inference with `workspace routing discovery failed` because the host lacked network access. It was stopped and rerun with host network permission. This is transport setup, not a behavioral result. The baseline transcript retains that initial user input followed by the successful runtime; completed events are from the successful attempt. Authentication and raw runtime files are excluded from these artifacts.

Visual status: not applicable to this text/protocol change; menu visibility unmeasured. These fixture results do not replace the final clean remote Spec install gate.

After implementation commit `2754ae8`, merged Spec `9b98dfec4cf92df1e354d542a4961d4216b45054` without rebasing (merge `a235545`). The three runtime-relevant bodies (`retro-planning`, `to-tickets`, `issue-absorption`) still match the evaluated installed hashes exactly. `check-plugin.sh`, all five packaging tests, `claude plugin validate .` passed after the merge; the initial whitespace check covered only the working-tree diff, not the committed Ticket diff. The initial checks correctly rejected literal vendor model names in new provenance; those records now identify the same model through the immutable README tier mapping, following existing eval convention. Isolated runtime processes finished and temporary homes, credentials and raw runtime material were removed.

Review verification caught renderer-added trailing blank separators in seven transcript files. They were normalized to one final newline, preserving every message byte before the final separators. The corrected whitespace validation checks the complete committed Ticket diff with `git diff --check codex/spec-348-shared-base...HEAD`, rather than only uncommitted changes. No behavioral rerun was needed for this output-formatting correction.
