# Release thread report (2026-11-04 09:00 UTC, dry run)

Every tracker and pull-request write is listed in order in `.scratch/proposed-actions.md` (12 blocks). Main is at `1c6fe96`.

## Release 2: cut and closed

- Where the run started: #2 (Release 2) is an open release issue in the older shape, with a `## Scope` list and no `## Order`. #10 and #20 carry its label, so it counts as the current Release rather than as a planning that stopped part way. The changelog on main had no `## Release 2` entry, so the run began by checking the Release was done.
- Shipped: #10 Farewell command (PR 7, `Closes #10`) and #20 Quiet flag (PR 8, `Fixes #20`). Nothing was dropped, nothing blocked the cut and nothing was carried over.
- Changelog pull request (proposed as PR 22, `docs(release): Release 2`): it covers commits `9a18f55..1c6fe96`, lists #10 and #20, and adds "Also merged: README usage (#9)". It has no "What to do" section, and the release doc has no cut steps or versioning. The whole-Release check, `bash test.sh`, gave OK. Under the Boundary record an agent merges it as a squash.
- After the merge, the entry is posted on #2 as its notes and #2 is closed.
- End-of-Release pass: `triage` (Triage batch) and `retro-planning` (Release-end Retro planning) each run, and each gets its `<!-- release end-of-Release pass -->` record on #2. In this dry run both skills ran but changed nothing.

## Release 3: planned

- Order: 1. #21 Shout flag. It is the Milestone's last planned feature that is still open. It has no blockers and nothing depends on it.
- Size: 5. Used: 1.
- Left out: none.
- Checked against main (`1c6fe96`): #21 is still valid, because `src/greet.sh` has no `-s` handling.
- Proposed to you: no unplanned features.
- Writes: open release issue #23 "Release 3", create the label `release-3` and apply it to #21. No issue carried `next-release`.

## Something to look at (does not block anything)

- On main, `src/greet.sh` has no `bye` command and no `-q` flag. It has only the comment lines `# bye` and `# quiet`, and `test.sh` tests only `hello`. #10 and #20 count as shipped under the shipped test (each was closed by a merged pull request with a closing keyword), but the features they describe do not seem to be on main. You may want to reopen them, or file bugs for them. This report does not do either.
- Numbering: pull requests and issues seem to share one number sequence, so the new pull request is numbered 22 and the new release issue 23.
- Because this is a dry run, the later steps assumed the proposed merge of PR 22 had happened: closing #2 and posting the entry as its notes came from the entry in that PR, not from main.
