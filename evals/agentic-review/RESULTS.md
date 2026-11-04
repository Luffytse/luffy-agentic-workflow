# Results

One entry per run, newest first. Rerun when a pull request changes how `agentic-review` or `review-rounds` behave, as the [evals guide](../../docs/dev-skills/evals.md) says, and record the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`. An entry written inside an open pull request names the commit and plugin version it ran on as its base; anything that happens after the entry's last commit (later Rounds, merges, the merge itself) is recorded on the pull request, not in the file.

Entries before the review was rebuilt around Round 0 and `review-rounds` ran the earlier review (up to 5 Rounds, rebuttals, the convergence check, Milestone design answers, merge-only Rounds). They are kept as history: the checks they name for those rules were removed with the rules, and a `<depth>` there is the old Review depth.

### 2026-11-04, dev-skills 0.71.0, Verify-only, Standard

Run level: decision-level in a subagent, as the README says: one fresh regular-tier subagent per run, given its `verifier.md` and no other input. Branch run: `38bbea8` (the Verifier-alone brief carries the meaning of Important and the Skip list), plugin 0.71.0. Baseline run: main `7dc6244` (0.71.0, from a `git archive`). Both on the Standard fixture from `setup.sh`, brief from `briefs.sh --verify-only <fixture> standard`. Driven by the thread, which scored with `EXPECTED.md`.

| id | main's skill | branch's skill |
|----|--------------|----------------|
| V-a | dropped: `amount_cents` is always an `int` from `parse_amount` (`money.py:6`), `format_cents` emits only digits, sign and dot, a non-number raises; not dropped as a repeat of V-d | same |
| V-b | dropped: the loop walks the `list(pending)` copy (`split.py:29`); the run gave `[(Ben, Ana, 1000), (Caro, Ana, 1000)]`, Dan unpaid only because of `:27` | same |
| V-c | kept, Important, caused by this change, `splitter/split.py:27` (`settle` gave `[]`) | same |
| V-d | kept, Important, caused by this change, Locations exactly `splitter/report.py:11` and `splitter/report.py:16` (`:12` removed) | same |

Locations counted within their own file: yes, in both runs.
Pass: yes, both runs, 4/4.

Extras, both runs, outside the check: spare cents given to the last people (`split.py:11`) and the docs-index entry for `docs/splitting.md` missing; the branch run also noted `index.md:5` still pointing to `currency.md`.

What it shows: no regression. The change affects only the Verifier-alone `disputes` brief and the sentence of `VERIFY.md` about it, and the Verify-only check builds neither; `briefs.sh --verify-only` output is byte-identical on this branch and on main once the scratch directory name is normalised (10468 and 10466 bytes before that, the gap being `fx-branch` against `fx-main`) so the check's input did not move. The Verifier-alone `disputes` brief is out of scope of this check (it uses `verify`); `evals/review-briefs/test_review_briefs.py` (`DisputesRound`) covers it.

### 2026-11-04, Script briefs, second run, dev-skills 0.69.0

Run level: decision-level in a subagent that can run shell commands (regular tier); it starts no agent. Two fresh regular-tier subagents, each told to read the case's `PROMPT.md` and do exactly it (one hop: the prompt came from the file, not pasted). Rerun because the branch's skill text changed after the first run below: SKILL.md "Briefing the agents" now names `<finder>.md` and says `verify` takes the same `--level` and `--spec` as the Round's briefs.

Case: `script-briefs/`. Branch run: `plugins/` of the Spec branch at `b229874` (dev-skills 0.69.0). Baseline run: `plugins/` of main at `098821e` (0.69.0). Scored with `python3 evals/agentic-review/script-briefs/score.py <out-dir>`.

| check | main's skill | branch's skill |
|-------|--------------|----------------|
| F1 files | FAIL (left: adversarial-finder.md, spec-finder.md, standards-finder.md, verifier.md) | PASS |
| B1 standards brief | FAIL (finder-standards.md missing) | PASS |
| B2 spec brief | FAIL (finder-spec.md missing) | PASS |
| B3 adversarial brief | FAIL (finder-adversarial.md missing) | PASS |
| B4 Verifier brief | FAIL (verifier.md differs from the script's) | PASS |
| L1 work tree | PASS | PASS |
| H1 command named (by hand) | no script exists | named, see below |

Score: main 1/6, branch 6/6.

Branch's run (H1): the agent read SKILL.md, ran `--help`, wrote `round1 --level standard --base main --head planted ... --spec ... --angle "Bugs and edge cases"`, copied the three messages as `standards.md`, `spec.md` and `adversarial.md` into a reports directory outside the repository and the briefs directory, then ran `verify --level standard ... --reports <dir>`. There was no retry this time: the first run's retry is gone with the file-naming wording.

Main's run: the agent again hand-built the briefs with a heredoc-based shell generator; tiers standards and spec regular, adversarial cheap, Verifier regular. Same caveat as the first run: F1 and B1-B3 fail partly on file names, not only on content.

The premium-tier re-check of the case said keep (valid, needed); it fails on main mostly for the right reason, named above (hand-built briefs differ from the script's).

### 2026-11-04, Script briefs, dev-skills 0.67.0 plus Ticket #649

Run level: decision-level in a subagent that can run shell commands (regular tier); it starts no agent. Two fresh regular-tier subagents, each given `PROMPT.md`'s text only.

Case: `script-briefs/` (Round 1 at Standard on the planted fixture, then the Verifier's brief from three canned Finder messages). Branch run: `plugins/` of `ticket-649` at `5931d20` (0.67.0, as on the Spec branch). Baseline run: `plugins/` of main at `b7f9873` (0.67.0, no brief script). Scored with `python3 evals/agentic-review/script-briefs/score.py <out-dir>`.

| check | main's skill | branch's skill |
|-------|--------------|----------------|
| F1 files | FAIL (left: adversarial-finder.md, spec-finder.md, standards-finder.md, verifier.md) | PASS (finder-adversarial.md, finder-spec.md, finder-standards.md, verifier.md) |
| B1 standards brief | FAIL (finder-standards.md missing) | PASS (identical to the script's) |
| B2 spec brief | FAIL (finder-spec.md missing) | PASS (identical) |
| B3 adversarial brief | FAIL (finder-adversarial.md missing) | PASS (identical) |
| B4 Verifier brief | FAIL (verifier.md differs from the script's) | PASS (identical) |
| L1 work tree | PASS | PASS |
| H1 command named (by hand) | no script exists; see below | named, see below |

Score: main 1/6, branch 6/6.

Main's run: the agent read SKILL.md, FINDERS.md, VERIFY.md and the docs-index and review-record skills, read the repo with git status, log, diff, merge-base, rev-parse and cat, wrote a generator shell script (heredocs) and ran it to produce all four briefs. Tiers it gave: standards regular, spec regular, adversarial cheap, Verifier regular. It noted gaps in the canned Finder reports and added nothing to the candidate list. Main's F1 and B1-B3 failures come partly from file names (the agent named files `<role>-finder.md`), not only from unmatched content; the case does not show content divergence for B1-B3 on main, only B4 differs in content.

Branch's run: the reply named `review_briefs.py round1 --level standard --base main --head planted --repo <repo> --out <briefs dir> --spec <repo>/.scratch/SPEC.md --angle "bugs and edge cases"`, then `verify ... --level standard --for round1 --reports <dir> --spec ...`. The first `verify`, pointed at the messages directory (files named `<role>-finder.txt`), wrote nothing; the agent copied them as `standards.md`, `spec.md` and `adversarial.md` into a reports directory outside the repository and the briefs directory, reran, and wrote `verifier.md`. Finding: at `5931d20` the skill text said to save each message "to a file named for that Finder" and did not give the name `<finder>.md`, so the agent learned it from the script's failure. The commit that records this entry adds the name to SKILL.md ("Briefing the agents"); that wording was run in the second run above, where the retry did not recur.

What it shows: with the Ticket's skill text the agent used the script and its output is byte-identical to the script's; on main the agent hand-built briefs with a generator script. It does not show that the added file-naming phrase removes the retry.

### 2026-11-02, base dev-skills 0.44.0, merge-only depth summary

Base: main `0c35d65`; green used that base with the working-tree Round-comment Depth summary changed to point to its existing Merge-only Rounds owner. The coordinator drove two fresh regular-tier Codex agents (`red_probe` and `green_probe`) with the bounded decision prompt (`evals/agentic-review/merge-depth/README.md` at `25708c4`, removed since); scoring expectations were withheld. The summary entry point was isolated: agents followed its pointers rather than repairing contradictions from unreferenced text; the owner section was supplied for pointer lookup and the following-Round continuation.

Each cell records the returned run depth / marker `depth=` / heading depth; every heading had the shape `## Code review: Round <n> of at most 5 (<depth>)`.

| Case | Expected | Red: original summary | Green: owner pointer |
| --- | --- | --- | --- |
| A: spelling and cross-reference | Quick | Quick / Quick / Quick | Quick / Quick / Quick |
| B: shell check exit-code behavior | Deep | Quick / Quick / Quick — fail | Deep / Deep / Deep |
| C: Markdown rule changes merge authority | Deep | Quick / Quick / Quick — fail | Deep / Deep / Deep |
| Following ordinary Round 4 | Deep, from ordinary Round 2 | Deep / Deep / Deep, from Round 2 | Deep / Deep / Deep, from Round 2 |

Red failed B/C before the fix. Green passed every row after the pointer fix; the existing owner rule supplies the logic exception without changing its semantics. `bash scripts/check-plugin.sh`, `claude plugin validate .` and `git diff --check` passed on the changed worktree. Not visual; Door: two-way, since the changes are git-only text and a revert undoes them.

Limits: these were decisions over supplied scenarios and passages, not live merges or Review execution. No actual conflict resolutions, posted Round comments, Find/Verify, installed-runtime loading, mixed merge/fix ranges or late-design budget paths were exercised. The full planted Standard/Deep fixture suites were not rerun for this bounded summary fix. Later Rounds and final version allocation belong to the pull request record, not this base-version entry.

## Template

Every new entry records its run level (see [Run level](README.md#run-level)); earlier entries have no such line and are not rewritten.

```
### <date>, dev-skills <version>, <level>

Run level: decision-level in a subagent | full build-flow in a top-level session

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

For the Round 0 case (scored by `round0/EXPECTED.md`):

```
### <date>, dev-skills <version>, Round 0

| Branch | Expected | Got | Reason given | Skills loaded | Pass? |
|--------|----------|-----|--------------|---------------|-------|
| version-only | None, one-line record, checks run | | | | |
| typo | Quick, hands over | | | | |
| rule-change | Standard, hands over | | | | |

Runtime and tier: <how the sessions ran>
Pass: yes | no. <one line on what to change in agentic-review, if anything>
```

For the loop cases (scored by `loop/score.py` and `loop/EXPECTED.md`):

```
### <date>, dev-skills <version>, Loop: <merge | after-round3>

score.py: <its output, PASS or the failed checks>
Hand-scored: <the diff command used; the subagents started, with their tiers; the report to the caller; any question to the user>
Pass: yes | no. <one line on what to change in review-rounds, if anything>
```

## Runs

### 2026-11-02, dev-skills 0.29.0, Spec #400 pull request #444, Deep

Base: `301d551d28ef4915efeb5ec3521ea7b0aa68c10b` (branch `claude/project-thread-ksqrgp`, pull request #444, after its Round 1 fixes; version left at 0.29.0 as on main). The skill text read is that commit's `plugins/dev-skills/skills/agentic-review/` (main's plus this pull request). The commit that adds this entry, and any later docs-only commits, change no file the briefs are cut from. Driven by the pull request's Implementer, which had read `EXPECTED.md`, so not a fresh session; it had no subagent tool, so every agent was a brand-new headless `claude -p` session on its tier from the `model-tiers` map (cheap, regular, premium, as `FINDERS.md` and `VERIFY.md` give them), working directory the scratch repo, Write and Edit tools disallowed, given one brief file from `briefs.sh` and told to read only it and the scratch repo. A fresh fixture from `setup.sh`; six fixture unit tests passed; the scratch repo was clean after the run. Five Finders ran in parallel; their reports were pasted into the three stance briefs whole, each tagged with its Finder, and the Verifiers merged the duplicates. The premium gap sweep got the kept Findings; its two Findings went to three more brand-new regular Verifiers with the kept Findings for the repeat check. Votes combined by `VERIFY.md`'s rules. Rank: 5 Important, 5 Nits shown (2 fix, 3 skip; the cap cut one skip Nit, `balances` shadowing the function name, kept 2 of 3), 1 Pre-existing.

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | 3 of 3 keep and Important; `split.py:11` |
| P2 | yes | Important | yes | 3 of 3; `report.py:11` and `:16` in one Finding (spec, both adversarial and security Finders merged) |
| P3 | yes | Important | n/a | 3 of 3; `split.py:27` |
| P4 | yes | Pre-existing | n/a | raised by both adversarial Finders; 3 of 3 real and Pre-existing; `money.py:6` |
| P5 | yes | Important | yes | 3 of 3 Important, each citing the spec's every-doc-index line; `index.md:6`, `splitting.md:1`, `money.md:1` (tracer gave the missing lines as `index.md:7`, outvoted on location) |
| P6 | yes | Nit (fix) | n/a | 3 of 3 Nit (fix), lowering the standards Finder's Important; `cli.py:7`, Bug class "public function without a docstring"; the standards Finder's Always check section lists the line as broken by it |
| F1 | never raised | | | |
| F2 | never raised | | | |
| K1 | yes | Nit (skip) | n/a | raised by both adversarial Finders; 3 of 3 keep, Nit (skip); `split.py:17-19` |
| K2 | yes | Important | n/a | gap sweep; second Verify 3 of 3 keep, 2 of 3 Important (tracer, skeptic: shares no longer add up to the total, as the spec asks; spec checker Nit (fix)); `split.py:8-12`, `split.py:19`, `cli.py:10` |

Extras: unrequested rename of `currency.md` to `money.md` (spec Finder), Nit (skip) by 2 of 3, real; missing tests for spare-cent order, `balances`, `settle` and the report, Nit (fix) 3 of 3, real; `balances` parameter shadows the function (standards smell), kept 2 of 3 as Nit (skip), real but harmless, cut by the Nit cap; CLI gives a traceback with missing arguments (gap sweep), Nit (skip) 3 of 3, real, `cli.py:9-10` (the skeptic's `cli.py:8-9` was off by one, outvoted). Dropped by Verify: duplicated loops in `report.py` and bare-tuple transfers (standards smells), 3 of 3 drop. No false extra kept.
Pass: yes. All six planted cases at accepted Severities and locations, P4 included, and both known extras at accepted Severities. Locations counted within their own file, apart from the two outvoted lines noted.

### 2026-11-02, dev-skills 0.29.0, Spec #400 pull request #444, Standard

Base, skill text and driver as the Deep run above, on the same scratch repo: four Finders (regular standards and spec, cheap bugs and edge cases and cheap security and privacy) in parallel, then one brand-new regular Verifier with their reports pasted whole, each tagged with its Finder; the Verifier merged the duplicates. Rank: 4 Important, 5 Nits (3 fix, 2 skip; under the cap), 1 Pre-existing.

| id | Reported? | Severity given | All locations? | Notes |
|----|-----------|----------------|----------------|-------|
| P1 | yes | Important | n/a | `split.py:11` |
| P2 | yes | Important | yes | `report.py:11` and `:16` in one Finding |
| P3 | yes | Important | n/a | `split.py:27` |
| P4 | yes | Pre-existing | n/a | raised by the bugs-and-edge-cases Finder, which ran `parse_amount("0.29")` and got 28; `money.py:6` |
| P5 | yes | Important | yes | Verifier cited the spec's every-doc-index line, overruling an adversarial Finder's Nit; `index.md:6`, `money.md:1`, `splitting.md:1` |
| P6 | yes | Nit (fix) | n/a | lowered from the standards Finder's Important; `cli.py:7`, Bug class "public function without a docstring"; the standards Finder's Always check list shows the line broken by it |
| F1 | never raised | | | |
| F2 | never raised | | | |
| K1 | yes | Nit (skip) | n/a | raised by the spec Finder (Nit, unsure) and the bugs Finder (Important, unsure); `split.py:18-19` |
| K2 | no | | n/a | known extra not raised |

Extras: unrequested rename of `currency.md` to `money.md`, Nit (fix), real; missing tests, Nit (fix), real; CLI traceback with missing arguments, Nit (skip), real. Dropped by Verify: terminal escape sequences in CLI output from member-typed names (security Finder, unsure), correctly. No false extra kept.
Pass: yes. All six planted cases at accepted Severities and locations; P4 found at Standard, which the 0.24.1 Standard runs missed (#376).

### 2026-11-02, dev-skills 0.29.0, Convergence check

Base: `3817c93e3ef06f1e0b59b3f943142577b2d9af54` (branch `ticket-440`, version left at 0.29.0 as on main; later changes to `ROUNDS.md`, including the resumed-record rule and rebuttal counting, are not in the copy the runs read). Driven by the Ticket's Implementer: each fixture built with `convergence/make-fixture.sh`, the text between the lines of its `PROMPT.md` given to a fresh headless top-level session on the premium tier (`claude -p`, edits allowed, working directory the fixture repo), with `<checkout>` set to a copy of `plugins/` alone, so `EXPECTED.md` and the Expected line stayed out of reach. No subagents (Find and Verify given).

| run | Expected | Got | Pass? | Notes |
|-----|----------|-----|-------|-------|
| returned, inside | R3-1 returned R1-1; restart; record; R3-3 filed | as expected | yes | all 8 conditions. Matched R1-1's line 8 at Round 2's head to line 9 and named commit 6ba2c84 as the one that dropped the quotes; Result `attempt ended: restart (a Finding returned)`; record Comment 1 (attempt 1, R3-1 returned R1-1, R3-2 open, Tried, a Lesson naming the lost quoting, Untouched `README.md, tests/backup.sh`); R3-3 filed as `21-unquoted-path.md` (`needs-triage`) with a receipt |
| flip, inside | R2-1 flipped R1-1; park (attempt 2); record | as expected | yes | all 8 conditions. Result `attempt ended: park (a fix flipped back)`; record Comment 2 (attempt 2, earlier attempt linked, R2-1 flipped R1-1, R2-2 open, a Lesson that the Ticket must settle missing file versus empty list, Untouched `tests/count.sh`); said neither Finding returns attempt 1's row; no filing |
| returned, outside | not clean, 2 Important open; Round 4; no record | as expected | yes | said the convergence check does not run outside a Milestone; noted the quoting came back and suggested a test, without ending on it; R3-3 left for the last Round |
| flip, outside | not clean, 2 Important open; Round 3; no record | as expected | yes | warned the owner that R2-1's fix as asked would undo R1-1's, and went on to Round 3 |

False matches: none (R3-2, R3-3 and R2-2 not counted).

Baseline: the two inside runs on the unchanged skill (main's `agentic-review` at 0.29.0), driven the same way, both failed: returned noted that R3-1 is R1-1 back but planned Round 4; flip did not hold R2-1 under R1-1 and went on to Round 3. No attempt record in either.

Not exercised: the late design Round, an attempt ended at Round 5, the resumed-record rule, and a Finding that returns from an earlier attempt record (the flip run checked only that a different claim does not).

Pass: yes.

### 2026-11-02, dev-skills 0.29.0, Rebuttal

Base: `3f6b381` (branch `ticket-441`, version left at 0.29.0 as on the Spec branch). The rebuttal brief and `REBUTTALS.md` are as in that commit; the run itself was made on the working tree just before it, whose later edits touched only `ROUNDS.md`, `review-record` and ADR 0003, not the brief. Driven by the Ticket #441 Implementer, which had read `EXPECTED.md`: a fresh fixture from `setup.sh`, briefs from `briefs.sh --rebuttal`, and each brief given whole to a brand-new headless session on the premium tier (a `claude -p` session on the premium model of the `model-tiers` map, read-only tools), told to read only it and the scratch repo. None saw this README, `EXPECTED.md`, `VERIFY-ONLY.md`, `REBUTTALS.md` or `RESULTS.md`.

| Id | Expected | Got | Lines cited | Reran the evidence? | Pass? |
|----|----------|-----|-------------|---------------------|-------|
| R1-1 | Uphold | Uphold | `split.py:27`, plus `split.py:39` (returns with debts left in `pending`) | yes: the 6 tests pass but `grep` finds no test calling `settle`; the one-creditor input returns `[]`; a two-creditor input leaves Dan unpaid | yes |
| R1-2 | Dismiss | Dismiss | `money.py:6`, `:11`, `:13`, `expenses.py:15`, `report.py:12`, `:16` | yes: `format_cents("<b>")` raises `TypeError`; also tried a float and `load_expenses` with typed text | yes |
| R1-3 | Uphold | Uphold | `report.py:11`, `report.py:16`; dropped `:12` as not a problem | yes: rendered a page with a markup payer in its own copy | yes |
| R1-4 | Dismiss | Dismiss | `split.py:25`, `:29`, `:34`, `:36` | yes: the Finding's input prints `[('Ben', 'Ana', 1000), ('Caro', 'Ana', 1000)]` | yes |

Locations counted within their own file: yes.
Pass: yes. The Verifiers rejected both unsound rebuttals on a run of their own, not on doubt: R1-1's passing tests never call `settle`, and R1-3's command-line path never reaches the page. R1-3 also corrected the Finding's scenario (one creditor gets no transfer, so the creditor cell needs two or more creditors). R1-2 and R1-4 each named, in one line, the real Findings in the same lines (the unescaped payer, the loop bound) without counting them against the call.

### 2026-11-02, dev-skills 0.29.0, Verify-only, Standard

Base and driver as the Rebuttal run above. `VERIFY.md` changed only by the new "Rebuttals" section and one intro sentence, outside the brief that `--verify-only` cuts, so the Verifier brief `briefs.sh --verify-only` cuts is unchanged; rerun as the README asks for any `VERIFY.md` change. One brand-new headless session on the regular tier (a `claude -p` session on the regular model of the `model-tiers` map).

| id | Kept or dropped | Severity given | Caused by this change? | Locations given | Notes |
|----|-----------------|----------------|------------------------|-----------------|-------|
| V-a | dropped | n/a | n/a | n/a | `parse_amount` returns an `int`, `format_cents` formats only digits, `.` and `-`; the only `Expense(` is `expenses.py:15` |
| V-b | dropped | n/a | n/a | n/a | the loop walks `list(pending)`, a copy |
| V-c | kept | Important | yes | `splitter/split.py:27` | |
| V-d | kept | Important | yes | `splitter/report.py:11`, `splitter/report.py:16` | dropped `:12`, pointing at V-a |

Locations counted within their own file: yes.
Pass: yes.

### 2026-11-02, dev-skills 0.27.0, Milestone agreement (rerun after the brief fix)

Base: `a4e9576104999d678c2819363e26952980919e0c` (branch `ticket-399-design-answers`, version left at 0.27.0 as on main), whose design-answer brief tells the agent to sort only its own Finding. Driven by the coordinator thread as in the first run: a fresh `inside` fixture, briefs from `milestone/briefs.sh` and `--control`; each agent a brand-new subagent given one brief file. Two premium-tier design-answer agents, and the four control Finders on the blind copy `repo-control/` (no spec Decisions, comments or sorting exclusion, no Round 1 comment). The four Finders with settled designs were not rerun: the change touched only the design-answer brief, so their rows carry over from the first run. `EXPECTED.md` and `DESIGN-FINDINGS.md` were withheld from the agents.

| id | Expected | Got | Pass? | Notes |
|----|----------|-----|-------|-------|
| R2-1 | (a), quote fields, lasting | (a) | yes | change: RFC 4180 quoting for a field holding a comma or a double quote (a `csv()` helper in `export.sh`; `qty` unquoted, digits only; no line breaks, per ADR 0001), a sentence in ADR 0002, tests for `eggs, large` and `12" pizza`; reason AC2; lasting, ADR 0002. It mentioned the `added_by` conflict in one line as outside its Finding. |
| R2-2 | (b), names AC1 or the personal-data exclusion | (b) | yes | quoted the Milestone exclusion and the glossary against AC1; every answer (keep, drop, initials or ids) changes one; recommended keeping the exclusion and amending AC1 to the header `item,qty`; lasting, ADR 0002 |
| S1 | sort not re-raised | carried over: not raised | yes, with the limit below | blind control: not raised |
| S2 | fractions not re-raised | carried over: not raised | yes, with the limit below | blind control: not raised |
| inside | decision-level, 6 conditions | not run | not exercised | needs a fresh top-level session |
| outside | decision-level, 4 conditions | not run | not exercised | needs a fresh top-level session |

The Verifier (`briefs/verifier.md`) was not run: no re-raise to judge. Not exercised.

Re-raise limit: even on the blind copy, no control Finder proposed sorting or accepting fractional quantities. The fixture does not provoke the re-raise, so S1 and S2 show only that the Finders were quiet; this run gives no evidence that the settled designs stopped a re-raise.

Extras (the 4 blind control Finders): R2-1 (unquoted CSV fields) raised by 3 of 4, all but the standards Finder; R2-2 (personal data) by 2 of 4, the contradictions and spec Finders; R2-3 (docs index drift) by 3 of 4, all but the bugs Finder. The contradictions Finder raised a Nit (unsure), "the order added is not guaranteed by the list file" (`docs/adr/0002-export-format.md:3`, `src/export.sh:6`): an overclaim-style Finding that does not propose sorting, so not a re-raise. Also raised, real but not planted: the read loop drops a last line with no trailing newline (bugs and spec Finders), plus Nits on unchecked field counts, partial output, malformed lines, CRLF and thin tests.

Pass: yes for the design sort (R2-1 and R2-2). Not shown: that settled designs stop a re-raise (the fixture cannot provoke one), the Verifier's handling of a re-raise, and the decision-level runs (membership, recording on the spec issue, the row Notes, the Milestone review list).

### 2026-11-02, dev-skills 0.27.0, Milestone agreement

Base: `a3c09262991c146fb894978c3230f7aba2bc8165` (branch `ticket-399-design-answers`, version left at 0.27.0 as on main). Driven by the coordinator thread: fixtures built with `milestone/make-fixture.sh` (`inside`), briefs with `milestone/briefs.sh` and `--control`; each agent a brand-new subagent given one brief file. Two premium-tier design-answer agents; four Finders with settled designs (standards and spec regular, adversarial bugs and edge cases and contradictions cheap); the same four from `briefs-control/`. `EXPECTED.md` and `DESIGN-FINDINGS.md` were withheld from the agents.

| id | Expected | Got | Pass? | Notes |
|----|----------|-----|-------|-------|
| R2-1 | (a), quote fields, lasting | (b) | no | over-cautious: it called the quoting fix alone safe and lasting (an RFC 4180 rule in ADR 0002, `export.sh:8`, a test), then ruled (b) because fixing the format "means settling the `added_by` column", the conflict between AC1 and the Milestone exclusion that R2-2 raises. It pulled another Finding's conflict into its own sort. |
| R2-2 | (b), names AC1 or the personal-data exclusion | (b) | yes | named AC1 and the Milestone exclusion (and the glossary entry); recommended keeping the exclusion and dropping `added_by` (AC1's header becomes `item,qty`), lasting, recorded in ADR 0002 |
| S1 | sort not re-raised | not raised by any of the 4 Finders | yes, with the caveat below | control: not raised either |
| S2 | fractions not re-raised | not raised by any of the 4 Finders | yes, with the caveat below | control: not raised either |
| inside | decision-level, 6 conditions | not run | not exercised | needs a fresh top-level session |
| outside | decision-level, 4 conditions | not run | not exercised | needs a fresh top-level session |

The Verifier (`briefs/verifier.md`) was not run: no Finder re-raised S1 or S2, so it had no re-raise to judge. Not exercised.

Control caveat: the control is not blind. The fixture repo itself holds the spec's Decisions and the Round 1 comment under `.scratch/`, and the control Finders read them (the control contradictions and spec Finders said the R1-2 and R1-3 dismissals rest on the spec's Decisions). So the S1 and S2 passes show only that the Finders were quiet; this fixture cannot provoke the re-raise, and the run does not show that the settled designs stopped one.

Extras (8 Finder reports, 4 with settled designs and 4 control):
- R2-1 (unquoted CSV fields) raised by 7 of 8, all but the control standards Finder.
- R2-2 (personal data in the export) raised by 6 of 8, all but the adversarial contradictions Finder with settled designs and the control adversarial bugs Finder.
- R2-3 (docs index drift, ADR 0002) raised by 6 of 8, all but the two adversarial bugs Finders.
- Not planted, real: the read loop drops a last line with no trailing newline (`src/export.sh:6-9`), raised by 6 of 8, all but the control contradictions and control standards Finders; `tests/export.sh:5`'s `! bash src/export.sh` cannot fail under `set -e` (spec Finder with settled designs); partial output before a validation error, blank lines and CRLF (Nits, several Finders).

Pass: no. R2-1 was sorted (b) because of a conflict another Finding raises; the design-answer brief must tell the agent to sort only its own Finding. The re-raise check needs a blind control before it can show #217 fixed.

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


## 2026-11-02 — Ticket #480 mixed final-range histories

Source baseline: main `e77e84b`, dev-skills `0.45.0`. Version remains unchanged during review. Confirmed seam: actual Git-history classification, full pinned diff and depth/budget decisions, under the Ticket's worker brief. This is a manual before/after workflow trace, independently checked by the coordinating agent, plus executed fixture plumbing controls. No wording assertions were added.

Built five disposable repositories with `python3 evals/agentic-review/final-range/make-fixture.py /tmp/ticket480-after`. All five passed: each non-merge patch and each conflict resolution appears in `git log -p --first-parent --remerge-diff <last-reviewed>..HEAD`; the imported `upstream.txt` patch does not. The script's assertions check those actual Git outputs, not classification decisions or skill text. `.git/round.md` supplies the prior clean Deep Round 5, `.git/release.md` authorizes changing only `version.json`'s version value, and `.git/scenario.json` records exact SHAs.

**Before:** main's literal “only a merge from main” eligibility is false for both `bump-text` and `nit-text` (two own first-parent commits each). The callers nevertheless request a merge-only Round. The existing remerge-diff command already includes both patches, but the owner supplies no explicit depth/late eligibility for that mixed range. This is the red workflow trace; no fresh-runtime baseline was run. The fixture was prepared after drafting the rule, then traced against the untouched main source; this is not a claim of an automated red/green TDD run.

**After, observed manual decisions:** the Implementer read every patch, then the coordinator independently inspected all five histories and their source records and applied the drafted owner rule. Both reached:

| History | Commits accounted for | Decision after clean Round 5 |
| --- | --- | --- |
| bump-text | `5ac5ddf` version value only; `732e27b` main merge, wording resolution | late Round 6, Quick, entire two-commit range |
| nit-text | `7a38438` checked R5-1 spelling fix; `066cf70` main merge, wording resolution | late Round 6, Quick, entire two-commit range |
| both-logic | `7a38438` checked Nit; `b2850b0` bump; `93921b8` main merge, authority-changing rule resolution; `a51dacb` superseding bump after merge | late Round 6, Deep, entire four-commit range |
| disguised-logic | `a8d193b` alleged bump also adds unconditional-success check; `e93e69c` main merge | ineligible; no extra Round, end attempt |
| unrelated-clean | `f5d9c6a` unrelated logic; `da4c78c` conflict-free main merge | ineligible despite no conflicts; no extra Round, end attempt |

The first three share pinned prior head `231c92a0c4ee980afdeebe243fc00774cc50e5d9`. In `nit-text`, it stays in the Round 5 marker even though the `fixed` R5-1 Note names `7a38438`; `note.md:1` is counted at the pinned head. Thus neither posting the clean comment after the Nit nor bumping after the merge truncates the next range. Quick cases use `depth=Quick` and heading `## Code review: Round 6, late merge-only Round (Quick)`; the logic case uses matching Deep marker and heading. Every own patch is sent to Find/Verify, with the whole-PR diff retained for Bug class coverage.

Manual continuation trace (not additional built histories): the two ineligible ranges after Round 2 instead use ordinary Round 3 at carried Deep. Following a Quick merge-only Round 3, ordinary Round 4 takes Deep from Round 2. A qualifying range after late design Round 6 uses the sole late merge-only Round 7, never Round 8. A non-clean late merge-only Round, or another conflicting main merge after its clean completion, ends the attempt; an ineligible post-cap range does so without a Round. Outcomes remain `restart` with no earlier attempt and `park` with an earlier attempt or no built issue. No exhausted design-answer policy was changed.

Required packaging checks passed: `claude plugin validate .`, `bash scripts/check-plugin.sh`; `git diff --check` passed. Not visual. Limits: no fresh installed runtime, actual Find/Verify reviews, tracker posting, live CI, full Standard/Deep planted-Finding reruns or live final merge were exercised here. The bounded Git evidence and manual decisions cover the changed eligibility/diff/depth boundary only.

## 2026-11-02 — Ticket #481 exhausted design-answer decisions

Baseline: main `4ec7279`, dev-skills `0.46.0`. The version stays unchanged during review. Seam: the owner/caller decision after a clean late Round has closed. The coordinator dispatched one fresh regular-tier baseline agent against immutable baseline sources, and a separate fresh regular-tier after agent against the working draft. Both read the actual owner, callers and record contract, ran no Find/Verify and posted nothing. The Implementer authored this evidence from their returned decisions. The repeatable prompt and scoring (`evals/agentic-review/exhausted-design/README.md` at `25708c4`, removed since) isolate these workflow states; there is no string assertion presented as behavior.

**Red, before implementation:** baseline case A, a Ticket inside a Milestone receives an agreed rule-meaning change after clean late design Round 6; no earlier attempt and late merge-only allowance unused. The fresh agent returned “Baseline leaves this case unresolved.” It found no further Round authorized: the unused merge-only allowance requires a main merge and permitted companions. It found no explicit post-closure outcome or no-Round record/cause; first-attempt restart would apply *if* an ending were established, but that trigger was missing. Its next action was to surface the gap before committing or merging. It distinguished a later answer after clean closure from an answer of Round 6 itself and did not relabel the clean Round. This is an observed decision failure of the source contract, not a full executed review.

**Green, after implementation:** a separate fresh agent read the working draft and returned these decisions (condensed without changing their meaning):

| Case | Observed next action |
| --- | --- |
| A: inside Ticket, clean late design 6, unused merge allowance, no history | No Round 7; record first attempt on Ticket, `restart`; unused merge allowance cannot review design work. |
| B: exhausted late design with earlier failed attempt, other allowance used | No Round; next attempt number, `park` on Ticket. |
| C: inside Spec, clean late merge-only 6, unused design allowance | No design Round 7; Spec `restart` with no history, `park` with history. |
| D: inside Ticket, clean late merge-only 7 | No Round 8; Ticket restart/park by its history. |
| E: inside corrective check with Retro origin | Conditional on late closure, attempt 1 `park` on corrective PR; origin attempts do not count; origin answer is linked in Lesson. |
| F: inside Ticket, clean ordinary 4 | Commit the agreed change; ordinary Round 5 at carried depth; no attempt ending for this cause. |
| G/H: outside, clean late design 6 or late merge-only 6 with design allowance unused | Bring explicitly unreviewed answer to user under outside merge list; no new Round or inside-only attempt record/restart/park. |
| I: late answer keeps a design Nit but needs ADR | Same special ending, retaining Nit id/Severity and required ADR; ordinary Round 4 would instead lead to 5, Round 5 to late design 6. |

The after probe's E/I prompt was less explicit than the final repeatable prompt about exact last Round/history; the agent correctly made those responses conditional. The final README makes E a clean late design Round 6 and I the A history; these clarified inputs were not a separate fresh-agent run. The Implementer's manual trace under those explicit assumptions gives E immediate corrective-PR park and I first Ticket restart.

The after agent also returned the shared record contract: cause `agreed design change after last Round`; current PR head at receipt versus unchanged last Round's pinned Find/Verify head; only Rounds actually run; existing Finding id/Severity with locations brought to current head, How `agreed design answer`; Tried already committed answer work or none; Lesson preserves answer/source/required ADR/affected files and need for review on next attempt; Untouched none; resume reuses PR/head record. None of A–E/I gets an unreviewed merge or routine user merge decision.

Executed checks: `claude plugin validate .`, `bash scripts/check-plugin.sh`, `python3 scripts/test-check-plugin.py` (15 tests), Milestone-agreement and merge-authority fixture tests passed. Convergence, lone-Ticket restart and Spec park fixture tests initially failed on macOS because their existing GNU-style `sed -i` calls are incompatible with BSD sed; all three passed with a temporary uncommitted wrapper translating `sed -i` to `/usr/bin/sed -i ''`. No repository fixture was changed for this platform issue. `git diff --check` passed. Consistency searches covered owner, both build callers, record shape, glossary, ADRs and index; existing full pinned-range eligibility, depth and record-head rules are retained.

Not visual. Two-way Door: workflow text and evidence can be reverted. Limits: decision probes and fixture plumbing do not prove full Standard/Deep planted-Finding runtime, installed dependency loading, actual Find/Verify, tracker writes, CI, restart/park execution or a live merge. Those full runtimes were not run here.
