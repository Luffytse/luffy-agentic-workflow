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

## 2026-11-04 — #637 Release-end mark

Case `release-end`: inputs in `release-end/fixture/` (the baseline's `src/`, `docs/`, #12 and open record #20, plus a `next-release` mapping in `triage-labels.md`, closed release issue #30, Milestone issue #31 with feature #33, #33 blocked by #12, closed #32; no boundaries doc), prompt in `release-end/prompt.txt`. Candidate: commit `a380992`. Base: main at `c29d3b1`. Each run was a fresh regular-tier subagent that loaded only an archived copy of the skills. These are subagent runs, not the app-server install the other cases use, so they show the skill text's behavior, not installed discovery. Dialogue and events were not preserved; `release-end/output/` holds the branch run's resulting fixture, and `release-end/question-main.txt` the question main's run stopped on.

| Run | Observed result |
| --- | --- |
| Main's skill | Red: found no boundaries doc, treated the run as not a Milestone run (cap 3), resumed #20, and stopped at step 5 to ask the user for #12's verdict (Act proposed, 1 of 3 slots). It wrote no files and no issue carries `next-release`. |
| This branch's skill | Green: asked no question. Created issues/34.md "Summary report handles empty input" with labels `bug, ready-for-agent, next-release`, "Part of #31", Model tier regular, acceptance criteria including `Closes #12`, no release label. Commented "Absorbed by #34; closes when it is completed." on #12. In #20 set Cap to `none (Release end)`, wrote a Verdicts row "joins the next Release" (#34; blocks Milestone feature #33) and closed the record. #33 untouched. |

Not exercised: the app-server install, tracker transport beyond the local files, and the resume path that gives a missing mark to an existing Ticket.

## 2026-11-04 — #629 first-sighting check

Case `first-sighting` (see the README): built by `first_sighting.py`, self-tested by `test_first_sighting.py` (18 tests: the rendered input says what the case means, #41 names no severe wording, the check really fails on the kept past mistake and no CI step runs it, a reference run passes, and planted runs fail, among them main's both-`wontfix` run). Base: main `5edb3e2`, its skills from a `git archive` of `origin/main`. Candidate: branch `ticket-629` at `635649f` (skill text unchanged since), on the fixture rebuilt from the latest fixture commit. The case asks for a top-level premium-tier session that can start subagents, given only the checkout's skills. A run that could not start a necessity subagent and wrote `necessity check: not run` is reported separately, not as red: it shows the not-run path works and says nothing on whether a confirmed check is acted on.

| Check | Result |
| --- | --- |
| Premium case check (fresh premium-tier subagent, whole skill and workflow, before the runs) | FIX, with two fixes: runs need a top-level session because subagents have no Agent tool, and the prompt said "the one Ticket". Both applied (commits `c69746b`, `355173c`). A later run on the first fixture also showed #41 could be judged severe; the later reword of #41 fixed that. No separate link: the verdict is recorded here. |
| Main's skill (premium subagent, rebuilt fixture) | Red for the right reason: #41 and #42 both closed as `wontfix`, no Ticket, record closed. The scorer is red on the #41 lines (acted on, Absorbed by, necessity row, Ticket filed) and green on #42. An earlier main run on the first fixture judged #41 severe and filed a Ticket (only the necessity-confirmed line failed), which is why #41 was reworded. |
| This branch's skill (premium subagent, rebuilt fixture) | Not the run the case requires. The subagent had no Agent tool and started 0 subagents, so it took the skill's cannot-start-a-subagent path: #41 kept open, record row `necessity check: not run`, #42 closed as `wontfix`, record closed. The scorer is red on the Ticket lines, by design. This shows the not-run path works; it is not a pass. |

Necessity subagent started: main no (not needed), branch no (no Agent tool). The scorer reads only tracker files and cannot see whether a subagent was started, so this line is the run's own report.

The confirmed-path run (a Ticket for #41 with `necessity check: confirmed`) is therefore not recorded: it needs a top-level session that can start subagents, which the building thread could not make (a nested `claude -p` run was refused by the permission classifier). It is not claimed passed.

Not exercised: the confirmed path above, the app-server install, `to-tickets` itself (the prompt has the run file the Ticket), a necessity check that does not confirm, and a group held back by the cap or decided at a Release end.

## 2026-11-08 — #32 Retro scope

Case `scope` (see the README): built by `scope.py`, self-tested by `test_scope.py` (20 tests: the rendered input says what the case means, a reference run passes, and planted wrong runs fail, among them main's behaviour). Regular tier, subagent runs, no dialogue or events kept; the branch's and main's skills are taken from checkouts.

| Check | Result |
| --- | --- |
| Premium case check (fresh premium-tier subagent, whole skill folder and case files, before the runs) | PENDING: case check verdict (keep, fix or drop) |
| Main's skill | PENDING: main run (expected red: no Scope in the record, #54 decided here, no refiling) |
| This branch's skill | PENDING: branch run (expected green on every scorer line) |

PENDING: Not exercised (to be filled after the runs; candidates: a Retro that mixes scopes, a re-run that finds a Scope already assigned in an earlier record).
