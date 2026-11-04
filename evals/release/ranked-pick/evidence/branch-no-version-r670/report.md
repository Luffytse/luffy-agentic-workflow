# Release thread report (2026-11-04)

## Release 2 cut

- Release 2 (#2) was the current Release: both its issues shipped. #10 Farewell command closed by PR #7 (`Closes #10`), #20 Quiet flag closed by PR #8 (`Fixes #20`), both merged into main. Nothing dropped, nothing carried over.
- Changelog pull request #22, `docs(release): Release 2`, covers `9a18f55..1c6fe96`. It lists #10 and #20, and adds "Also merged: README usage (#9)". The Release 1 changelog merge (#6) rides along unlisted. It has no version line, because the release doc's versioning policy is none and there are no cut steps.
- Whole-Release check `bash test.sh`: passes. Agent-merged as a squash (the Boundary record lets agents merge it). Its entry was posted on #2 as the notes and #2 was closed.
- End-of-Release pass: triage (Triage batch) and retro-planning (Release-end Retro planning) both ran, and each has its record on #2.

## Release 3 planned (#23, label `release-3`)

- Goal: The greeter can shout, completing the Milestone's last planned command.
- Size 5, used 1.
- Order: 1. #21 Shout flag. It is the only planned feature of Milestone #1 still open and it has no blockers.
- Left out: none. Proposed unplanned features: none.
- Checked against main (`1c6fe96`): #21 is still valid, because `src/greet.sh` has no `-s` handling. No questions were raised.
- The `release-3` label was created and applied to #21.

## Worth a look

- On main, `src/greet.sh` handles only `hello`. PRs #7 and #8 each added just a comment line (`# bye`, `# quiet`), and `test.sh` covers only `hello`. So #10 and #20 count as shipped by the closing-keyword test, but `greet.sh bye <name>` and `-q` do not seem to work on main. Milestone #1 accepts each feature "when it works as its issue says". If you agree they are not done, reopen #10 and #20 so a later planning ranks them.
- Numbering: in this dry run I took the next number after every existing issue and pull request. That gives PR 22 for the changelog pull request and #23 for the release issue.
