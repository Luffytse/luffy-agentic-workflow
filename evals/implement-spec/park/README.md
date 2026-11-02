# implement-spec park check

Does the Spec thread, at step 5 (the third Ticket check still has an Important open), park the Ticket inside a Milestone and bring it to the user outside one? Each run gets an entry in [RESULTS.md](../RESULTS.md).

## Fixture

[`make-fixture.sh`](make-fixture.sh) builds one scratch repo outside this repo: `bash evals/implement-spec/park/make-fixture.sh <out-dir> <inside|outside>`. It starts from the merge-authority fixture's `spec` flow ([its README](../../implement/README.md#merge-authority-check)) and then:

- plants Ticket 11, whose first two acceptance criteria contradict each other (the farewell goes to standard output; the farewell goes nowhere but a log file), so no code passes its Ticket checks;
- keeps Ticket 12 blocked by 11, and adds Ticket 13, with no blockers;
- gives the local Markdown tracker doc the **Comment on an issue**, **Apply / remove labels** and **Park** operations (the `parked` label on the issue's `Labels:` line);
- labels the Spec `milestone-1` for `inside`, not for `outside`, and drops the Deep Review request.

It also makes `<out-dir>/PROMPT.md`. [`test-fixture.sh`](test-fixture.sh) builds both and checks each holds what its case needs; run it after changing the builder.

| Case | Spec labels | Expected |
| --- | --- | --- |
| `inside` | `enhancement, milestone-1` | Ticket 11 parked: `parked` on its `Labels:` line, an attempt record comment on it (`kind=attempt attempt=1`, `Outcome: park`, `Ended by: third Ticket check not clean`), the user told once in one message; 12 not started; 13 still lands; the Spec pull request stays a draft with no Rounds. |
| `outside` | `enhancement` | Ticket 11 brought to the user as today: no `parked` label, no attempt record; 12 not started; 13 still lands; the Spec pull request stays a draft with no Rounds. |

## Running it

1. Build the case into a scratch directory outside this repo.
2. Start a **fresh** session (a premium-tier agent), working directory `<out-dir>/repo`, and give it only the text between the lines of `<out-dir>/PROMPT.md`, with `<checkout>` replaced by this checkout's path. Keep `PROMPT.md` itself, and this README, away from it: the Expected line is the answer. The check is a **decision-level run** of step 5: the prompt hands the session the three Ticket checks' results, since it cannot start the Implementer and reviewers, and it edits the scratch repo's issue files where the tracker doc defines the operations.
3. Score against the Expected line: the membership decision, park or hand-over, the attempt record's fields, the number of messages to the user, and what happens to Tickets 12 and 13 and the Spec pull request. Check the issue files in `<out-dir>/repo/.scratch/issues/` for the label and the record.
4. Record the run in [RESULTS.md](../RESULTS.md) with its template, saying how it was driven, and the commit and plugin version of the checkout under test.
