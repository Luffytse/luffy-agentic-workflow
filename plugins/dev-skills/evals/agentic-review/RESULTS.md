# Results

One entry per run, newest first. Rerun when `agentic-review` changes, and record the plugin version from `.claude-plugin/plugin.json`.

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
| F1 | dropped? | | | |
| F2 | dropped? | | | |

Extras: <each other Finding, real or false>
Pass: yes | no. <one line on what to change in agentic-review, if anything>
```

## Runs

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
