# Convergence check: expected results

How a decision-level run of the convergence check is scored. Keep this file away from every session under test: it works in the fixture repo and reads only its prompt and the skills.

Each run is a fresh top-level session given the text between the lines of a fixture's `PROMPT.md` (`make-fixture.sh <out-dir> <returned|flip> <inside|outside>`). It carries on from Rank with Verify's results given, writes the Round comment under `.scratch/pulls/<n>/`, and does every step after it through the end of the Round, committing nothing and starting no subagents. Score the Round comment, the issue file (`.scratch/issues/20-backup.md` or `30-count.md`), any new issue or filing receipt, and the final report.

## The fixtures

- **returned** (pull request 1, branch `backup`, Round 3): R1-1 (unquoted path) was confirmed fixed in Round 2 at `src/backup.sh:6, :8` (Round 2's head). The fix commit since Round 2 adds a line above and rewrites the `cp` line without the quotes, so that line is now 9. Verify kept R3-1 (the same claim at `src/backup.sh:9`, under the Bug class "unquoted variable"), R3-2 (a different claim, file permissions, at lines 7 and 9, which overlap both fixed rows), and R3-3 (Pre-existing, the same Bug class name as R1-1, in `src/add.sh`), and confirmed R2-1 fixed. The issue holds no attempt record.
- **flip** (pull request 2, branch `count`, Round 2): R1-1 (a missing list file read as an empty list) is confirmed fixed by the commit that makes `src/count.sh:5` exit 1. Verify kept R2-1 (a first run before any item is added should print 0 and exit 0, which would undo that fix) and R2-2 (an unreadable file passes `[ -f ]`, a different claim at lines 5 and 6 whose fix keeps the exit 1). Pull request 1 is a closed first attempt; case `inside` has its attempt record on the issue (attempt 1, restart, a different problem: comment lines counted).

## Case `inside`

Both fixtures pass when all of these hold:

1. **Membership.** It decides the pull request is inside a Milestone from the Boundary record's label form and the issue's `milestone-1` label.
2. **Detection.** returned: R3-1 counts as returned, matched to R1-1 (its line brought from 8 to 9, the Bug class name ignored). flip: R2-1 counts as flipped, matched to R1-1.
3. **No false match.** returned: neither R3-2 (same lines, other claim) nor R3-3 (Pre-existing, other file) counts. flip: R2-2 (same line, keeps the fix) does not count. Earlier attempt (flip): R2-1 and R2-2 are not counted as returning attempt 1's row (another claim).
4. **The Round comment.** Its Result is the attempt-ended form `review-record` lists, with the right outcome and cause: returned `attempt ended: restart (a Finding returned)`, flip `attempt ended: park (a fix flipped back)`. The matched row's Note says "returned: R1-1" or "flipped: R1-1". The earlier Importants confirmed fixed are `fixed` with their commit; the kept Findings are `open`.
5. **Stops patching.** No fix is planned for a next Round and no next Round is announced; the session says the attempt ended.
6. **The attempt record.** A comment added to the issue with the tracker doc's "Comment on an issue" operation (returned: Comment 1; flip: Comment 2), in the `review-record` attempt-record shape: marker `kind=attempt` with `attempt=1` (returned) or `attempt=2` (flip) and the pull request number; the Rounds run (1 to 3, or 1 to 2); Ended by and Outcome matching the Result; Earlier attempts none (returned) or the link to Comment 1 (flip); a row for the returned or flipped Finding with How `returned R1-1` or `flipped R1-1`, and a row for the other open Important (R3-2 or R2-2) with How `open`; no row for R3-3; Tried naming the fix commits; a Lesson (returned: the R2-1 fix rewrote the `cp` line and lost R1-1's quoting; flip: the missing-file versus empty-list question has to be settled first); Untouched listing the diff's files no open row names (returned: `README.md` and `tests/backup.sh`; flip: `tests/count.sh`).
7. **Filing.** returned: R3-3 is filed now, as an issue made with the tracker doc's "Create an issue" operation (title naming the Bug class and pull request 1, label `needs-triage`), and a filing receipt is posted under `.scratch/pulls/1/`. flip: nothing to file, no receipt.
8. **The outcome.** The report to the caller says `restart` (returned) or `park` (flip), with the attempt record's link.

## Case `outside`

Both fixtures pass when all of these hold:

1. It decides the pull request is outside a Milestone (no label in the Boundary record's form).
2. No convergence check changes anything: the Round comment's Result is `not clean, 2 Important open`, and no row's Note says returned or flipped as an ending. (Saying in the report that R3-1 is R1-1's problem back is fine; ending on it is not.)
3. Nothing is written to the issue file; no attempt record anywhere.
4. The Importants go to the owner to fix and the next Round (returned: Round 4; flip: Round 3) is named as following.
5. No outcome (`restart` or `park`) is reported. returned: R3-3 is not filed yet (the pull request's last Round has not run).

## Scoring

- Inside, a missed detection (condition 2) fails: the review runs on toward Round 5. A false match (condition 3) fails and is the more serious failure: it ends a healthy review.
- Outside, any attempt record, attempt-ended Result or reported outcome fails: the change leaked out of the Milestone.
- Record each condition as yes or no, with what the session wrote where it differs.
