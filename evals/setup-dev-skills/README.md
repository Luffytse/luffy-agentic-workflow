# setup-dev-skills eval

A fixture run that checks `setup-dev-skills` asks for the Boundary record's values and writes the record from its seed, and that every file it writes lands in `docs/dev-skills/` with only `REVIEW.md` and the `CLAUDE.md` block at the root. Rerun when the skill's Section B, E or F, its `boundaries.md` seed, the paths it writes or its re-run diff changes.

## Fixture

A scratch git repo outside this one, with a made-up GitHub remote (`https://github.com/example-org/scratch-app.git`), a `README.md`, a `package.json` and one commit. No `CLAUDE.md`, `AGENTS.md`, `docs/` or `REVIEW.md`. The remote cannot be reached, so the run skips the reachability call, label creation and the GitHub settings check and says "not checked: fixture".

## Scripted conversation

The user answers in section order, the way the skill asks:

- Section A: accept GitHub.
- Section B: keep the default labels; no agent-only labels.
- Section C: single-context.
- Section D: no rules of its own.
- Section E (Releases): no.
- Section F (Boundaries): irreversible actions agents may take, "delete test data that agents generate while implementing"; actions needing approval, "delete production or customer data"; budget, "at most 20 dollars of API usage a month"; check-in interval and Milestone label form, accept the recommended answers.
- Approve every draft; create `CLAUDE.md`.

## Pass

- Section F asks one question per value, each leading with a recommended answer.
- `docs/dev-skills/boundaries.md` holds the five values and the Milestone-issue rule; the three values the user gave replace the seed's placeholders, and the check-in interval and label form stay at the recommended answers.
- The `## Agent skills` block has a `### Boundaries` part, and `docs/dev-skills/index.md` lists the record with a "read when" line.
- Every file written lands under `docs/dev-skills/` (the issue-tracker, triage-label and domain docs, the Boundary record and `index.md`), except the starter `REVIEW.md` at the repo root and the `CLAUDE.md` block; the block points at `docs/dev-skills/index.md`, and nothing else is written under `docs/` or at the root.
- A re-run shows no change to the three values the user gave, asks again only for a value the record lacks, and reports "no change" for every file.

## Case 2: Releases (Section E)

The same fixture and conversation as above, except Section E is answered yes and a run per versioning policy. Rerun when Section E, the `release.md` seed or the `next-release` label step changes.

Scripted Section E answers, the same for the three runs unless noted: uses Releases, yes; versioning policy, **none** (run a, the fixture has no version file), **pull requests bump** (run b) or **Releases bump** (run c; b and c add the version file `package.json`, its `"version"` field and, for b, the files `src/`, the number "given by the person who merges"); Release name form, accept the recommended `Release <n>`; Release size, accept the recommended 5; changelog path, accept; cut steps, none; whole-Release check, `npm test`.

Score the written `docs/dev-skills/release.md` with `python3 score_release_doc.py <release doc> <none|pull-requests-bump|releases-bump>`; it checks the fields, never the wording, and `fixtures/` holds a passing doc for each policy.

### Pass

- Section E asks, in order and one answer each with a recommended answer: uses Releases, the versioning policy, the name form (default `Release <n>`), the size (default 5), the changelog path and label prefix, the cut steps, the whole-Release check.
- Run a writes a release doc with policy none, a name form, a size and no version fields (no version file, bump, sizes or `Versions:` line). Run b keeps the version file, the bump commit and the `Versions:` cut step, and no semver sizes or bump pull request. Run c keeps the version file, the semver sizes, the bump pull request's steps and the `Versions:` line. Each deletes the other policies' sections and every seed note.
- The `## Agent skills` block has a `### Releases` part whenever a release doc was written, including run a.
- `docs/dev-skills/triage-labels.md` defines the `next-release` role, and step 4 creates the `next-release` label with the other labels (a fixture run with no reachable remote says "not checked: fixture"; a real run lists it among the labels created).
- A re-run over a doc that has a "Bump mode" line and no policy takes the mode as the policy and asks for every field the doc lacks (usually the size and the cut steps, and the name form when it has none).

## Case 3: Repo labels (Section B's third question)

Does `setup-dev-skills` ask whether the repo has labels of its own (recommended no), offer the tracker's unmapped labels as candidates, record the picked ones as rows of the Repo labels table with drafted lines, create a new label, and delete nothing; and does a re-run that drops a row leave the tracker label? Rerun when Section B's third question, the Repo labels seed section, the candidate rule or the label-creation step changes (Ticket #691, Spec #690).

Run level: a fresh subagent on the **regular** tier (decision-level, not a top-level session) that is given the skill folder to test (`plugins/dev-skills/skills/setup-dev-skills/` of the branch, or of main's archive for the baseline) and the case's `PROMPT.md`, nothing else. Keep this README, `repo_labels_cases.py` and `score_repo_labels.py` away from it. The prompt carries the scripted answers up front, so the run logs its questions instead of holding a conversation, and puts a stub `gh` first on PATH.

### Files

- [`repo_labels_cases.py`](repo_labels_cases.py): the three cases, the made-up tracker's labels and issues, and what each case must leave behind.
- [`make_repo_labels_fixture.py`](make_repo_labels_fixture.py): `python3 make_repo_labels_fixture.py <out-dir> <fresh|rerun-drop|none>` builds `<out-dir>/repo` (git repo, made-up remote; for `rerun-drop` it already holds a triage-labels doc with `frontend` and `backend` rows), `bin/gh`, `gh-state.json`, `gh.log` and `PROMPT.md`.
- [`repo_labels_gh_stub.py`](repo_labels_gh_stub.py): the logging `gh` stand-in, which serves the labels and issues from `gh-state.json`, applies a label creation or deletion to it and logs every call. It never reaches the network.
- [`score_repo_labels.py`](score_repo_labels.py): `python3 score_repo_labels.py <out-dir> <case>` scores the outcomes. Save the run's final reply to `<out-dir>/REPORT.txt` first.
- [`test_repo_labels.py`](test_repo_labels.py): the self-test (the rendered prompt and repo say what each case means, the stub works, a reference run per case passes, planted wrong runs fail). It reads no skill text; `python3 evals/setup-dev-skills/test_repo_labels.py` prints `ok`, and `scripts/run-tests.sh` runs it.

### Cases

The tracker has every label the skills use, so a correct run creates none of its own. Labels in use that nothing covers: `frontend`, `backend`, `docs-only`.

| Case | Answer to "labels of its own" | Expected rows | Candidates offered | Created | Deleted |
| --- | --- | --- | --- | --- | --- |
| `fresh` | yes: pick `frontend` and `backend`, accept the drafted lines, add `security` with the user's line | `frontend`, `backend`, `security` | `frontend`, `backend`, `docs-only` | `security` only | none |
| `rerun-drop` | yes: drop `backend`, keep `frontend` | `frontend`, its line unchanged | optional; only a label no row covers | none | none; `backend` stays in the tracker |
| `none` | no | none | none | none | none |

### Pass

The scorer reads outcomes only: the rows under `## Repo labels` in `docs/dev-skills/triage-labels.md` (each with a filled-in line, the role tables intact), the labels the stub saw created and deleted, the tracker's final labels, `CANDIDATES.txt` (the names the run offered) and the `Q: ... | recommended: ...` lines of the reply (a question about labels of the repo's own recommends no, or yes in `rerun-drop` where rows exist). It never reads the wording of a drafted line. On main's skill `fresh` fails (no candidates, rows or `security` label) and `none` fails on the missing `## Repo labels` section (main ignores that seed section; its question check can pass). `rerun-drop` passes on main (run 2026-11-04): it is a regression guard for the never-delete rule, not a branch-versus-main discriminator. Its prompt says only that `backend` is no longer used, so a skill without the never-delete rule may delete the label.
