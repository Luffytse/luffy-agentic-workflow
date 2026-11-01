# Results

One entry per run, newest first. Rerun when `agentic-review` changes, and record the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`. An entry written inside an open pull request names the commit and plugin version it ran on as its base; anything that happens after the entry's last commit (later Rounds, merges, the merge itself) is recorded on the pull request, not in the file.

## Template

```
### <date>, dev-skills <version>, <depth>

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | | | n/a | |
| P2 | | | | |
| P3 | | | n/a | |
| P4 | | | n/a | |
| P5 | | | | |
| P6 | | | n/a | |
| F1 | dropped? | | | |
| F2 | dropped? | | | |
| K1 | | | n/a | known extra: reported? at an accepted Severity? |
| K2 | | | n/a | known extra: reported? at an accepted Severity? |

Extras: <each other Finding, real or false>
Pass: yes | no. <one line on what to change in agentic-review, if anything>
```

For the Verify-only check (scored by the Verify-only section of `EXPECTED.md`):

```
### <date>, dev-skills <version>, Verify-only, <Standard | Deep>

| id | Kept or dropped | Severity given | Caused by this change? | Locations given | Notes |
|----|-----------------|----------------|------------------------|-----------------|-------|
| V-a | | | | | |
| V-b | | | | | |
| V-c | | | | | |
| V-d | | | | | |

Locations counted within their own file: yes | no. <any line counted across a listing>
Pass: yes | no. <one line on what to change in VERIFY.md, if anything>
```

## Runs

### 2026-10-31, dev-skills 0.24.1, Spec #348 candidate, Deep

Source: `9b98dfec4cf92df1e354d542a4961d4216b45054`. Candidate-generated briefs; fresh regular standards/spec, cheap bugs/money and premium security Finders; three regular Verifiers, then premium gap Finder and three new regular gap Verifiers. Agents ran in available slots, not all concurrently. Expected/scoring files were withheld from reviewing agents. Six fixture unit tests passed. Rank: 6 Important, 1 Nit (fix), 1 Pre-existing.

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | 3/3 keep |
| P2 | yes | Important | yes | 3/3; report.py:11,16 combined |
| P3 | yes | Important | n/a | 3/3 keep |
| P4 | yes | Pre-existing | n/a | real 3/3; attribution 2/3 Pre-existing (skeptic/spec), tracer voted new CLI Important; majority wins; money.py:6 and cli.py:9 |
| P5 | yes | Important | yes | 3/3, explicit every-doc-index spec sentence; splitting.md:1-5, money.md:1-3, index.md:6 |
| P6 | yes | Nit (fix) | n/a | 3/3; cli.py:7-11, Bug class public function without a docstring; Always-check broken |
| F1 | never raised | | | no verified-drop claim |
| F2 | never raised | | | no verified-drop claim |
| K1 | yes | Important | n/a | gap: omitted payer, split.py:17-19; 3/3 keep, caused |
| K2 | yes | Important | n/a | gap: duplicate participants, split.py:8-11; 3/3 keep, caused |

Extras: only the known K1/K2 cases. No groups dropped; no synthetic fixture issues filed. Pass: yes, all six planted cases at accepted severities/locations. This does not convert Standard's failure below into a pass.

### 2026-10-31, dev-skills 0.24.1, Spec #348 candidate, Standard

Same source and candidate brief generation as Deep. Fresh regular standards/spec and cheap bugs/security Finders, followed by one fresh regular Verifier; run serially because Implementers occupied slots. All reports received; expected files withheld. Six fixture unit tests passed. Rank: 4 Important, 1 Nit (fix), 0 Pre-existing.

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | split.py:11 |
| P2 | yes | Important | yes | report.py:11,16 combined |
| P3 | yes | Important | n/a | split.py:27 |
| P4 | no | | n/a | pre-existing money.py:6 never raised |
| P5 | yes | Important | yes | explicit spec requirement; splitting.md:1, money.md:1, index.md:6 |
| P6 | yes | Nit (fix) | n/a | cli.py:7-8; Bug class public function without a docstring; Always-check broken |
| F1 | never raised | | | no verified-drop claim |
| F2 | never raised | | | no verified-drop claim |
| K1 | no | | n/a | allowed known extra absent |
| K2 | no | | n/a | allowed known extra absent |

Extras: none. All five candidate groups kept, zero dropped by Verify. Pass: no, P4 missed, the known discovery miss tracked in #376. No discovery fix or synthetic tracker issue is included here. VERIFY.md is unchanged, so no required Verify-only rerun. These fixed-point evaluations do not prove every Round lifecycle branch or the final remote installation.

### 2026-10-31, dev-skills 0.24.1, Deep

Base: implementation commit `6339a7ca79bd5b249cd68c5d90d4793bee54ee5a` for #329/#330, plugin version 0.24.1. The Ticket thread used the fixture and generated Deep briefs from the same unchanged `SKILL.md`, `FINDERS.md` and `VERIFY.md` inputs as the Standard run below. Five fresh Finders completed reports, then three fresh Verifiers voted; a fresh premium Gap sweep Finder reported K2, and three more fresh Verifiers voted on it. Agents ran in bounded batches because the session allowed at most 3 active child agents. Rank left 5 Important, 1 Nit (fix), and 0 Pre-existing Findings. As in Standard, this fixed-point fixture does not exercise design-answer Round completion; the scenario walkthroughs below cover that change.

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | 3 of 3 keep and Important; Verifiers corrected the Finder example: 1001/3 gives 333, 334, 334, not 333, 333, 335 |
| P2 | yes | Important | yes | 3 of 3 keep and Important; payer and creditor locations |
| P3 | yes | Important | n/a | 3 of 3 keep and Important; Verifiers corrected the example: balances Ana 1, Ben 1, Caro -2 pay Ben and leave Ana unpaid |
| P4 | no | | n/a | pre-existing float parser bug missed |
| P5 | yes | Important | yes | 3 of 3 keep and Important, citing the explicit every-doc-index spec requirement |
| P6 | yes | Nit (fix) | n/a | 3 of 3 keep and Nit (fix); Bug class "public function without a docstring"; Always check line recorded as broken |
| F1 | never raised | | | |
| F2 | never raised | | | |
| K1 | no | | n/a | known extra not raised |
| K2 | yes | Important | n/a | Gap sweep: `splitter/split.py:8-11`; second vote 3 of 3 keep, Important and caused by this change; duplicate names lose part of the total, violating the exact-total guarantee |

Extras: none beyond K2. Dropped by Verify: none. The corrected P1 and P3 examples retained their claims; K2 is distinct from P1's remainder assignment.
Pass: no. P4 was not found, the same discovery miss as Standard. No change to discovery/Verify instructions or scoring expectations is included in this review-completion Ticket.

### 2026-10-31, dev-skills 0.24.1, Standard

Base: implementation commit `6339a7ca79bd5b249cd68c5d90d4793bee54ee5a` for #329/#330, plugin version 0.24.1. The Ticket thread built the fixture with `setup.sh` and generated the Standard briefs before that commit; `SKILL.md`, `FINDERS.md` and `VERIFY.md`, the brief inputs, are unchanged from its main base. Four fresh Finders and one fresh Verifier completed their reports, followed by Rank (4 Important, 1 Nit (fix), 0 Pre-existing). Agents ran in bounded batches because the session allowed at most 3 active child agents, rather than all Finders simultaneously. This fixed-point fixture checks Finding discovery and verification; it does not exercise the changed design-answer Round lifecycle. That lifecycle was checked separately by before/after scenario walkthroughs: Round 1 keep-all becomes clean but proceeds to Round 2; Rounds 2–5 commit and check text "fix" Nits before editing to clean; partial Nit locations stay open; agreed design changes require another Round within the cap, with Round 5 changes handed to the user unreviewed. No Verify-only run was required because `VERIFY.md` is unchanged.

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | spare cents assigned to the last people |
| P2 | yes | Important | yes | both unescaped payer and creditor locations |
| P3 | yes | Important | n/a | last creditor skipped |
| P4 | no | | n/a | pre-existing float parser bug missed |
| P5 | yes | Important | yes | both drift locations; Verifier cited the explicit every-doc-index spec requirement |
| P6 | yes | Nit (fix) | n/a | Bug class "public function without a docstring"; Always check line recorded as broken |
| F1 | never raised | | | |
| F2 | never raised | | | |
| K1 | no | | n/a | known extra not raised |
| K2 | no | | n/a | known extra not raised |

Extras: none. Dropped by Verify: none.
Pass: no. P4 was not found. Discovery and Verify instructions are unchanged by this Ticket; the miss is recorded without changing those instructions or the expected results as part of the review-completion fix.

All runs on 2026-10-31, dev-skills 0.22.13 (`agentic-review` text as on main f27a5c8), driven by the Ticket thread of #148, the same way as the 0.12.1 runs below: the thread built the fixture with `setup.sh` (head a0a951d, main af4d866), started the agents, passed the briefs from `FINDERS.md` and `VERIFY.md` word for word (written to brief files outside the repo, each agent told to read only its own brief and the scratch repo), merged duplicate candidates before Verify, and applied the Rank rules; it read `EXPECTED.md` only to score. Every Finder and Verifier was a fresh subagent; tiers were mapped to models by the Model tiers table in `plugins/dev-skills/README.md`. The thread had read `EXPECTED.md`, so it did not use a fresh session; the agents never saw `EXPECTED.md` or the Verify-only mapping, and the Verify-only Verifiers got the contents of `VERIFY-ONLY.md` pasted into their brief, never its path. Angles: bugs and edge cases plus security and privacy, as in every earlier Standard run. The fixed-point diff was `git diff --merge-base main`, with no untracked files. A slip in the run: the thread's first batch of Finder briefs lost the Finding format (the script that cut it out of `FINDERS.md` stopped at the `### <short title>` line inside the code block), so those Finders gave no line numbers. The thread discarded that batch and reran all four Finders, fresh, on fixed briefs. One Finder (security, first batch) ended without a report and was asked again, as `SKILL.md` says. Line numbers (#98): these are the first runs since `VERIFY.md`'s Location rule (#147), and every Location a Verifier gave was counted within its own file; in the full run the Verifier corrected two wrong Finder lines to the file's own lines. These are also the first runs with the Verify-only check and the known extras K1 and K2. No full Deep run was made this time, because the ticket asks for one run; the Verify-only Deep run is the Deep coverage. Through 0.22.17, `agentic-review` differs from 0.22.13 only in `ROUNDS.md`'s Rank step 2 (how a dismissed Finding is matched, #138), which a fixed-point Review and the Verify-only check do not use; no Find or Verify text changed.

### 2026-10-31, dev-skills 0.22.13, Standard

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | spec and bugs Finders; standards passed it on |
| P2 | yes | Important | yes | `report.py:11` and `:16`; security, spec and bugs Finders |
| P3 | yes | Important | n/a | bugs Finder cited `split.py:27`, spec Finder `:29`; the Verifier kept `:27` ("line 29 is only the inner loop") |
| P4 | yes | Pre-existing | n/a | bugs Finder; the Verifier kept `money.py:6` and dropped the `cli.py:9` call site from the Locations |
| P5 | yes | Important | yes | `docs/index.md:6`, `docs/splitting.md:1`, `docs/money.md:1`; standards proposed Nit, spec and bugs Important; the Verifier kept Important on the spec line "Every doc gets a line" |
| P6 | yes | Nit (fix) | n/a | `splitter/cli.py:7-8`. Raised by standards under its Always check step (proposed Important), and its Always check list named the Finding; spec and bugs Finders raised it too. Verifier: Nit, "breaks the Always check line as written, but nothing behaves wrongly" |
| F1 | never raised | | | the security Finder checked the amount column and did not raise it |
| F2 | never raised | | | |
| K1 | yes | Important | n/a | security and bugs Finders; the Verifier kept `split.py:18-19` ("money silently disappears") and dropped `:17` and an `(unsure)` `expenses.py:15` (file unchanged). Accepted Severity |
| K2 | yes | Important | n/a | bugs Finder; Verifier: shares no longer add up to the total, `split.py:10-11`. Accepted Severity |

Extras (all real): unrequested rename `currency.md` to `money.md` (Nit, fix); thin tests (Nit, fix, raised `(unsure)`); `settle` parameter shadowing `balances()` (Nit, skip; the spec Finder cited `split.py:26`, the Verifier corrected it to `:22`); CLI tracebacks on missing or malformed arguments (Nit, skip). Dropped by Verify: negative amounts accepted (raised `(unsure)`; the spec does not make them invalid and puts parsing out of scope). Five Nits, exactly Rank's cap, so all would be reported.
Line numbers (#98): every Location the Verifier gave was counted within its own file, and it corrected the two wrong Finder lines (`split.py:29` to `:27`, `:26` to `:22`) to the file's own lines. The one cross-listing number in the run came from the standards Finder's pass-on notes, not a Finding (`report.py:12` and `:17` for `:11` and `:16`); no Verifier saw it.
Pass: yes.

### 2026-10-31, dev-skills 0.22.13, Verify-only, Standard

| id | Kept or dropped | Severity given | Caused by this change? | Locations given | Notes |
|----|-----------------|----------------|------------------------|-----------------|-------|
| V-a | dropped | | | `money.py:6`, `:9-13` cited as reasons | `amount_cents` is always an int; `format_cents` raises `TypeError` on a string |
| V-b | dropped | | | | walks `list(pending)`, a copy; the loss in the scenario is the `:27` bound |
| V-c | kept | Important | yes | `split.py:27` | ran the scenario: `[]` |
| V-d | kept | Important | yes | `report.py:11`, `:16` | removed `:12` |

Locations counted within their own file: yes. The Verifier said it did not read `cli.py`, so it did not check the Always check line; no candidate was on it.
Pass: yes.

### 2026-10-31, dev-skills 0.22.13, Verify-only, Deep

Votes are tracer, skeptic and spec checker.

| id | Kept or dropped | Severity given | Caused by this change? | Locations given | Notes |
|----|-----------------|----------------|------------------------|-----------------|-------|
| V-a | dropped 0 to 3 | | | | all three: `format_cents` emits only digits, `-` and `.` |
| V-b | dropped 0 to 3 | | | | all three ran or traced the scenario: Caro is paid |
| V-c | kept 3 of 3 | Important 3 of 3 | yes 3 of 3 | `split.py:27` | |
| V-d | kept 3 of 3 | Important 3 of 3 | yes 3 of 3 | `report.py:11`, `:16` (all three removed `:12`) | the skeptic also corrected the scenario: line 11 alone fires; line 16 only when `settle` names that payer |

Locations counted within their own file: yes.
Pass: yes.

Does a broken `VERIFY.md` fail the check? Two more Verify-only runs at Standard, each with only call 1 ("Real?") of the Verifier brief changed:

1. Drop rule weakened to "When a claim does not hold as stated, correct its failure scenario instead of dropping it; drop only what `REVIEW.md` says to skip." The Verifier still dropped V-a and V-b and the check passed: it went against the weakened rule because the claims plainly do not hold. So the check catches a change that actually stops Verify dropping, not every weaker wording.
2. Rewritten to "keep. Finders raise only what they have checked, so keep every candidate; when its stated failure scenario does not hold, correct the scenario." The Verifier kept V-a (Nit, skip, `report.py:12`, `:16`) and V-b (Nit, skip, "no scenario exists"), still with V-c and V-d right. The check fails on V-a and V-b, as it should.

Both runs on 2026-10-30, dev-skills 0.12.1, driven by the Ticket thread of #27, the same way as the 0.10.0 runs below: the thread started the agents, passed the briefs from `FINDERS.md` and `VERIFY.md` word for word (written to brief files outside the repo, each agent told to read only its own brief and the scratch repo), merged duplicate candidates before Verify, and applied the Rank rules; it read `EXPECTED.md` only to score. Every Finder and Verifier was a fresh subagent; tiers were mapped to models by the README table. Angles as before: bugs and edge cases plus security and privacy (Standard), bugs and edge cases plus money, numbers and time (Deep). The fixed-point diff was `git diff --merge-base main`, with no untracked files (`.scratch/` is excluded). These are the first runs with the fixture's `REVIEW.md` (P6), and the first since `VERIFY.md`'s corrected-scenario rule: one gap-sweep Verifier gave a corrected failure scenario (G1). The Standard Verifier and one Deep Verifier (the skeptic) "corrected" Locations to line numbers counted across their own concatenated file listing (for example `report.py:50` and `:55` for `:11` and `:16`, `split.py:79` and `:95` for `:11` and `:27`), not the file's own lines; the thread kept the file lines when ranking. Filed as #98. Through 0.15.1, `agentic-review` differs from 0.12.1 only in its setup hint (`setup-dev-skills`, #84); no Find, Verify or Rank text changed.

### 2026-10-30, dev-skills 0.12.1, Standard

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | spec, bugs and standards Finders (standards passed it on as `(unsure)`) |
| P2 | yes | Important | yes | `report.py:11` and `:16`, raised by all four; the Verifier cited them as `:50` and `:55` (see above) |
| P3 | yes | Important | n/a | spec, bugs, standards `(unsure)` |
| P4 | yes | Pre-existing | n/a | bugs Finder; Verifier checked `main` |
| P5 | yes | Important | yes | standards and spec proposed Important citing the spec line, bugs Nit; Verifier kept Important on the spec line |
| P6 | yes | Nit (fix) | n/a | standards Finder under (d), and its Always check list named the Finding. The bugs Finder noticed the comment but judged `main` exempt as a CLI entry point and did not report it, so only the Always check step caught it |
| F1 | never raised | | | |
| F2 | never raised | | | |

Extras (all real): unrequested rename `currency.md` to `money.md` (Nit, fix); payer outside the people list (Nit, fix; raised `(unsure)` as Important); thin tests (Nit, fix); CLI tracebacks on missing arguments and `inf`/`nan` (Nit, skip). Dropped by Verify: none. With P6 there are five Nits, all reported under Rank's cap.
Pass: yes.

### 2026-10-30, dev-skills 0.12.1, Deep

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | 3 of 3; raised by standards, spec, bugs and money Finders |
| P2 | yes | Important | yes | 3 of 3; the premium security Finder traced `load_expenses` to both sinks |
| P3 | yes | Important | n/a | 3 of 3 |
| P4 | yes | Pre-existing | n/a | 3 of 3; bugs and money Finders |
| P5 | yes | Important | yes | 3 of 3, spec line cited (standards Finder proposed Nit) |
| P6 | yes | Nit (fix) | n/a | 3 of 3 fix; raised by standards (under (d), with the Always check list), spec and bugs Finders |
| F1 | never raised | | | |
| F2 | never raised | | | |

Extras (all real): unrequested rename (Nit, fix, 3 of 3); payer outside the people list (Nit 3 of 3, fix 2 to 1; bugs and money Finders proposed Important `(unsure)`); tests (Nit, fix); CLI tracebacks (Nit, skip). Gap sweep (premium, after Verify): duplicate names collapse shares (Important 2 to 1, 3 of 3 keep; earlier runs kept it as a Nit) and `settle`'s parameter shadowing `balances()` (Nit, skip, 3 of 3). Neither repeated a kept Finding. Six Nits before Rank's 5-Nit cap: the four "fix" Nits and one "skip" Nit would be reported.
Pass: yes. F1 and F2 still tempted no Finder, so Verify dropping them is still untested.

Both runs on 2026-10-30, dev-skills 0.10.0, driven by the Ticket thread of #51, in the same way as the 0.2.0 runs below: the thread started the agents, passed the briefs from `FINDERS.md` and `VERIFY.md` word for word, merged duplicate candidates before Verify, and applied the Rank rules; it read `EXPECTED.md` only to score. Every Finder and Verifier was a fresh subagent. Tiers were mapped to models by the README table. Angles picked as in the 0.2.0 runs, so the two can be compared: bugs and edge cases plus security and privacy (Standard), bugs and edge cases plus money, numbers and time (Deep). The fixed-point diff was `git diff --merge-base main` with the untracked `.scratch/SPEC.md` listed as an untracked new file (it is also the spec); no Finder mistook it for part of the change. `VERIFY.md`'s rule to correct a wrong failure scenario instead of dropping (call 1) and the corrected-scenario answer field were added after these runs (commits 7628986 and 854f488), so the runs did not exercise them.

### 2026-10-30, dev-skills 0.10.0, Standard

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | standards, spec and bugs Finders |
| P2 | yes | Important | yes | `report.py:11` and `:16`, raised by all four |
| P3 | yes | Important | n/a | spec and bugs; the standards Finder passed it on as `(unsure)` |
| P4 | yes | Pre-existing | n/a | bugs Finder; Verifier checked `main` |
| P5 | yes | Important | yes | Verifier cited the spec line "Every doc gets a line" |
| F1 | never raised | | | |
| F2 | never raised | | | |

Extras (all real): unrequested rename `currency.md` to `money.md` (Nit, fix); thin tests (Nit, fix); `settle` parameter shadowing `balances()` (Nit, skip); bare transfer tuples (Nit, skip; the spec fixes the shape); payer not in the people list (Nit, skip, raised `(unsure)`); duplicate names collapse shares (Nit, skip, raised `(unsure)` as Important); CLI tracebacks (Nit, skip). This lists every kept extra before Rank's 5-Nit cap; the two "fix" Nits and three "skip" Nits would be reported. Dropped by Verify: none. Every Finding carried a failure scenario, and the cleanup ones stated a cost.
Pass: yes.

### 2026-10-30, dev-skills 0.10.0, Deep

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | 3 of 3 keep |
| P2 | yes | Important | yes | 3 of 3; the premium security Finder traced `load_expenses` to both sinks and ran it |
| P3 | yes | Important | n/a | 3 of 3 |
| P4 | yes | Pre-existing | n/a | 3 of 3 Pre-existing |
| P5 | yes | Important | yes | 3 of 3, spec line cited |
| F1 | never raised | | | |
| F2 | never raised | | | |

Extras (all real): payer outside the people list loses money (`split.py:17-19`; Important 3 of 3, kept as a realistic rare path, raised Important by the money and bugs Finders); unrequested rename (Nit, fix); tests (Nit, fix); CLI tracebacks including `inf` (Nit, skip); duplicate names collapse shares (Nit 2 to 1, skip); shadowing and bare tuples (Nit, skip). Gap sweep (premium, after Verify): README's index line not updated for the new CLI section (Nit, fix, 3 of 3) and a missing charset on the HTML fragment, raised `(unsure)` and dropped 3 to 0 because nothing serves the page. Neither repeated a kept Finding. These extras list every kept one before Rank's 5-Nit cap: with the gap sweep's Nit there are seven, so the three "fix" Nits and two "skip" Nits would be reported.
Pass: yes. Same planted Findings as the 0.2.0 runs, no false extra reported. F1 and F2 still tempted no Finder, so Verify dropping them is still untested; the gap sweep's one false candidate was dropped by its second Verify. The new adversarial angles were not picked, to keep the runs comparable.

Both runs on 2026-10-29, dev-skills 0.2.0, driven by the build thread of ticket #6. The thread had read `EXPECTED.md`, so it only started agents, passed the briefs from `FINDERS.md` and `VERIFY.md` word for word, and applied the Rank rules; every Finder and Verifier was a fresh subagent that never saw `EXPECTED.md`. Tiers were mapped to models by the README table. Angles picked: bugs and edge cases plus security and privacy (Standard), bugs and edge cases plus money, numbers and time (Deep).

### 2026-10-29, dev-skills 0.2.0, Standard

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | raised by all four Finders |
| P2 | yes | Important | yes | `report.py:11` and `:16`, raised by all four |
| P3 | yes | Important | n/a | spec and bugs Finders |
| P4 | yes | Pre-existing | n/a | bugs Finder; Verifier checked `main` |
| P5 | yes | Important | yes | Verifier cited the spec line "Every doc gets a line"; the spec Finder also called the rename scope creep |
| F1 | never raised | | | |
| F2 | never raised | | | |

Extras (all real): payer not in the people list breaks the zero sum (Nit, skip); CLI tracebacks on missing arguments (Nit, skip); tests check only the sum (Nit, fix). Dropped by Verify: transfers as bare tuples, `settle` parameter shadowing `balances()`, duplicated render loops, the README example.
Pass: yes. F1 and F2 tempted no Finder, so this run did not test Verify dropping them.

### 2026-10-29, dev-skills 0.2.0, Deep

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | 3 of 3 keep |
| P2 | yes | Important | yes | 3 of 3; the premium security Finder traced payer to creditor to `report.py:16` |
| P3 | yes | Important | n/a | 3 of 3 |
| P4 | yes | Pre-existing | n/a | 3 of 3 Pre-existing |
| P5 | yes | Important | yes | 3 of 3, spec line cited |
| F1 | never raised | | | |
| F2 | never raised | | | |

Extras (all real): duplicate names collapse shares, so they no longer add up to the total (`split.py:9-11`; Important 2 to 1, not planted but a fair reading of the spec's "add up to exactly the total"); payer not in the people list (Nit, skip 2 to 1); CLI tracebacks (Nit, skip); tests (Nit, fix); `settle` parameter shadowing and bare tuples (kept 2 to 1 over the skeptic, Nit, skip). Duplicated render loops dropped 3 to 0. Five Nits reported, the "fix" one first.
Pass: yes. Same gap on F1 and F2.

What these runs changed in `agentic-review`: the first attempt ran the Review inside a subagent, which cannot start subagents of its own and stopped, so `SKILL.md` now says the Review runs in the top-level session. Cheap Finders quoted wrong line numbers (from a concatenated listing); the Verifier corrected them, as its brief asks.
