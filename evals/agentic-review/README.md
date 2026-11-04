# agentic-review eval

Behaviour checks for the review: `agentic-review` (Round 0) and `review-rounds` (the Rounds). They test what a review does on a fixture, never the skills' wording. Rerun the cases whose rules a change touches.

- **Planted fixture:** a small pull request with planted problems of known Bug classes (one breaks the fixture's `REVIEW.md` Always check line for its Python files) and two plausible false alarms. Does Round 1 report the right Findings at the right Severity and drop the false ones? Rerun at Standard and at Deep when the Finder or Verifier briefs change.
- **Verify-only check:** the Verifier alone, handed the two false alarms and two real controls, so its drop call is tested even when no Finder raises them. Rerun when `VERIFY.md` changes.
- **Round 0:** does Round 0 pick None for a version-only diff, Quick for a typo and Standard for a skill-rule change, and load nothing more at None?
- **Loop, `merge`:** does Round 2 after a merge of main review only the pull request's commits and the merge's conflict resolution, with one Finder and one Verifier?
- **Loop, `empty-round`:** does a Round 2 in which the Finder returns no candidate and no Finding is open start no Verifier, go to Rank, and say in its comment that no candidates went to a Verifier?
- **Loop, `after-round3`:** after a Round 3 that is not clean, does the open Important become a bug Ticket, the Nit get dropped, and the pull request become ready to merge, with no Round 4 and no question to the user?
- **Loop, `after-round3-labels`:** the same sort in a repo whose triage-labels doc has a Repo labels table (`backend` for the server code under `app/`, `frontend` for the UI under `ui/`): does the bug Ticket carry `backend` and not `frontend`? The plain `after-round3` case, which has no table, also checks that the bug Ticket carries no label beyond `bug` and `ready-for-agent`.
- **Script briefs:** does a fresh top-level-style session, following `review-rounds`, write a Round's Finder and Verifier briefs by running the plugin's brief script, so the files are the script's own? Rerun when `review-rounds` or `review_briefs.py` changes how a Round is briefed.

Every case's builder has a test that builds it and checks it holds what the case needs; run them after changing a builder or a skill file they read. None of them starts an agent:

```
bash evals/agentic-review/test-briefs.sh
python3 evals/agentic-review/script-briefs/test_score.py
bash evals/agentic-review/round0/test-fixture.sh
bash evals/agentic-review/loop/test-fixture.sh
```

## Run level

**Run level** means what the runner can show from where it runs. *Decision-level in a subagent*: a fresh subagent (which cannot start subagents of its own) is given the skill and the fixture and says what it would do; steps that start or watch real workers are listed as not exercised. *Full build-flow in a top-level session*: a session that can start subagents, schedule a check-in and archive a worker runs the skill end to end.

| Case | Run level |
| --- | --- |
| Planted fixture, step 3 (Finders and Verifier started by hand or by the coordinator) and the whole-review run | full build-flow in a top-level session: Finders and the Verifier are subagents, which a subagent cannot start |
| Verify-only check | decision-level in a subagent: one Verifier, given its brief, starts nothing |
| Round 0 | full build-flow in a top-level session, as its steps say (the score reads whether a subagent was started); the level pick itself could be shown decision-level (guess, not yet tried) |
| Script briefs | decision-level in a subagent that can run shell commands: it writes briefs and starts no agent (regular tier) |
| Loop, `merge` | full build-flow in a top-level session: Round 2 starts a Finder and a Verifier |
| Loop, `empty-round` | full build-flow in a top-level session: Round 2 starts a Finder; the score reads the comment's `Verifier: none` line, and that no Verifier was started is checked by hand. No model run is recorded yet (the builder, scorer and reference outcomes are tested; no agent has run it) |
| Loop, `after-round3` | steps say a top-level session that can start subagents; the sort needs no Finder, so decision-level in a subagent may show it (guess, not yet tried) |
| Loop, `after-round3-labels` | as `after-round3`; no model run is recorded: the sort starts a premium-tier subagent, which a decision-level subagent cannot do, so the run needs a top-level session (the stated gap of Ticket #692). The builder, scorer and reference outcomes are tested; no agent has run it |
| the builders' tests | no model session |

## Files

- `base/`, `after/`, `SPEC.md`, `setup.sh`: the planted fixture. `base/` is the repo before the change (a tiny Python cost splitter with its own `docs/dev-skills/index.md` and a `REVIEW.md` with two Always check lines, one for `splitter/*.py`, which the change breaks once, and one for shell scripts, which the change does not touch); `after/` holds the files the change adds or edits; `setup.sh` builds it as a scratch repo (branch `main` holds `base/`, branch `planted` adds one commit with the change, and the spec sits untracked at `.scratch/SPEC.md`). The fixture's files are test data.
- `EXPECTED.md`: the planted Findings, the false alarms, the known extras, how a run is scored, and the scoring of the Verify-only check.
- `VERIFY-ONLY.md`: the candidates for the Verify-only check, in the Finding format, each tagged with its Finder.
- `briefs.sh`: builds the Round 1 Finder briefs for the planted fixture by calling `plugins/dev-skills/skills/review-rounds/review_briefs.py` (`round1`), the one builder; with `--verify-only` it splits `VERIFY-ONLY.md` into one report per Finder and calls `review_briefs.py verify`. It holds no brief text. `test-briefs.sh` checks what it builds (the files, and that the fixture's spec and Always check line reach the right brief); what each brief holds from the skill files is tested in `evals/review-briefs/`.
- `script-briefs/`: the Script briefs case: `make-case.sh`, `PROMPT.md`, `messages/` (the Finders' canned final messages), `score.py`, `test_score.py`.
- `round0/`: `make-fixture.sh`, `test-fixture.sh`, `EXPECTED.md`.
- `loop/`: `make-fixture.sh` (cases `merge`, `after-round3`, `after-round3-labels` and `empty-round`), `score.py` (scores a run from the files it left), `reference.sh` (hand-made right and wrong outcomes for the scorer's self-test), `test-fixture.sh`, `EXPECTED.md`.
- `RESULTS.md`: one entry per run.

Keep `EXPECTED.md`, `VERIFY-ONLY.md`, `score.py` and `RESULTS.md` away from the reviewing agents: they work in the scratch repo, not in this one.

## Planted fixture

1. Build it outside this repo: `evals/agentic-review/setup.sh <new-empty-dir>`.
2. Build the Finder briefs: `evals/agentic-review/briefs.sh <scratch-repo> standard` (or `quick`, `deep`). They go to `<scratch-repo>.briefs/<level>/`, outside the scratch repo: `finder-standards.md`, `finder-spec.md`, `finder-adversarial.md` (Standard and Deep; the angle defaults to bugs and edge cases, or name another from `FINDERS.md` as the third argument) and `finder-security.md` (Deep).
3. Start each Finder as a brand-new subagent on its tier from `review-rounds` (standards and spec regular, adversarial cheap, security premium), given one brief file and told to read only that and the scratch repo. Each brief names the report file its Finder writes (`<scratch-repo>.briefs/<level>/reports/<finder>.md`, `<finder>` one of `standards`, `spec`, `adversarial`, `security`; a Finder that cannot write it says so, and you save its final message there). Run `python3 plugins/dev-skills/skills/review-rounds/review_briefs.py verify --level <level> --base main --head planted --repo <scratch-repo> --spec <scratch-repo>/.scratch/SPEC.md --out <scratch-repo>.briefs/<level>` (`--reports` defaults to that `reports` directory) and start the Verifier on the `verifier.md` it writes (regular; premium at Deep). Rank by `review-rounds`' Rank step.
4. Score with `EXPECTED.md` and add an entry to `RESULTS.md`.

A fresh top-level session can run it whole instead: "Run agentic-review on branch planted since main, spec at .scratch/SPEC.md, at Standard". That is a review since a fixed point: Round 0 and Round 1, and no comment.

## Verify-only check

1. Build the fixture with `setup.sh`.
2. `evals/agentic-review/briefs.sh --verify-only <scratch-repo> standard` writes `<scratch-repo>.briefs/standard-verify-only/verifier.md`: the Verifier brief with `VERIFY-ONLY.md`'s candidates in it as the script's `verify` carries them (never its path or name). The script prints the Deep tier whatever the level: run it on the tier of the level you test.
3. In a fresh session, start one brand-new Verifier subagent on the regular tier, given that file and nothing else; for Deep, run the same file on the premium tier.
4. Score with the Verify-only section of `EXPECTED.md` and record it in `RESULTS.md`.

The fixture's own tests pass (`python3 -m unittest` in the scratch repo): the planted bugs are the kind tests miss.

## Script briefs

A Round whose briefs come from the plugin's brief script. Scoring: [`script-briefs/score.py`](script-briefs/score.py) and `EXPECTED.md`. A fresh subagent that can run shell commands gets the skill text under test and the fixture, and is asked to write Round 1 (Standard) briefs for the Finders and then, given the Finders' canned final messages, the Verifier's brief. It starts no agent.

1. `bash evals/agentic-review/script-briefs/make-case.sh <new-out-dir> <plugins-copy>` builds `<out-dir>/repo` (the planted fixture), `<out-dir>/messages/` and `<out-dir>/PROMPT.md`. `<plugins-copy>` is a copy of the `plugins/` folder under test, outside this checkout: the branch's, or main's (`git archive main plugins | tar -x -C <dir>`). One case per skill version.
2. Give a fresh regular-tier subagent the text of `PROMPT.md`, nothing else, and keep this checkout away from it.
3. `python3 evals/agentic-review/script-briefs/score.py <out-dir>`, then score H1 by hand from its reply and record both runs in `RESULTS.md`.

## Round 0

[`round0/make-fixture.sh`](round0/make-fixture.sh) builds a small repo that writes skills (a manifest, a changelog, one skill, a Boundary record, a `REVIEW.md` without a "Review levels" section, and `check.sh` as its checks) with three one-commit branches: `version-only`, `typo` and `rule-change`. Scoring: [`round0/EXPECTED.md`](round0/EXPECTED.md).

1. `bash evals/agentic-review/round0/make-fixture.sh <out-dir>` makes `<out-dir>/repo` and `<out-dir>/PROMPT-<branch>.md` for each branch.
2. Copy this checkout's `plugins/` folder to a directory of its own, so the session reads the skills but not `evals/`.
3. For each branch, give a fresh top-level session the text between the lines of its `PROMPT-<branch>.md`, its working directory `<out-dir>/repo`, `<checkout>` replaced by that copy's path. Three runs.
4. Score with `round0/EXPECTED.md`, from each answer, the comment file it wrote and its tool calls (which files it read, which skills it loaded, whether it started a subagent). Record the runs in `RESULTS.md`.

## Loop cases

[`loop/make-fixture.sh`](loop/make-fixture.sh) builds a small Python repo with a local Markdown tracker (issues under `.scratch/issues/`, pull request 1 and its comments under `.scratch/pulls/`), a Boundary record that needs the user for nothing, and pull request 1 part way through its review. Scoring: [`loop/EXPECTED.md`](loop/EXPECTED.md) and [`loop/score.py`](loop/score.py).

- `merge`: Round 1 is posted (R1-1 open); since then a fix commit and a merge of `main` whose conflict resolution swaps two operands. `main` also brought in a bug of its own. Round 2 is next.
- `after-round3`: three Rounds are posted; Round 3 is not clean, with one real open Important and one "fix" Nit.
- `after-round3-labels`: `after-round3` in a repo whose triage-labels doc has a Repo labels table (`backend`, `frontend`).

1. `bash evals/agentic-review/loop/make-fixture.sh <out-dir> <merge|after-round3|after-round3-labels|empty-round>` makes `<out-dir>/repo` and `<out-dir>/PROMPT.md`.
2. Copy this checkout's `plugins/` folder to a directory of its own, as for Round 0.
3. Give a fresh top-level session that can start subagents the text between the lines of `PROMPT.md`, its working directory `<out-dir>/repo`, `<checkout>` replaced by that copy's path. One run per case.
4. Run `python3 evals/agentic-review/loop/score.py <case> <out-dir>`, score the hand-scored points in `loop/EXPECTED.md` from the session's report and tool calls, and record the run in `RESULTS.md`.

## Measuring the Finders

Each Round comment's Note names the Finder that raised a Finding, and its Status says whether it was fixed. To see how often each Finder's Findings get fixed, count, over the merged pull requests' Round comments, the rows per Finder named in the Note and how many of them end `fixed`. Record the counts in `RESULTS.md` when a later cut to the roster is weighed.
