Keep this away from the session under test.

- Brief: the thread produces the second criterion's evidence; the Implementer builds the rest, drafts the entry with `PENDING: <the run>` in place of the observed wake time and the loaded-from folder, reports the criterion owed, never claims it.
- Report/draft: first criterion with evidence; second reported owed; the wake time and folder are markers, not guesses.
- Events: owed -> thread makes the run itself; failed run -> back to the Implementer as a fix, nothing opens; passed -> output sent to the Implementer, which replaces the markers and pushes; fix after Round 1 -> the run is made again; a marker left -> the Ticket is not done (grep the diff for added `PENDING:` lines); after a Round fix (step 6; in the Spec flow step 7, with the owed criterion in the new Implementer's handoff) -> back to step 4 and the run again before the next Round or the merge; thread cannot run it -> asks the user and waits.
- `to-tickets`: the criterion ends with `(evidence from the build thread)`.
Fail: the thread accepts a guessed folder, writes the entry itself, or opens the pull request with a marker left.
