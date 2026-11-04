# Proposed actions: Release thread, 2026-11-04 09:00 UTC

Where I started: release issue #2 (Release 2) is open, both issues in its Order (#10, #20) carry `release-2`, and `CHANGELOG.md` on main has no `## Release 2` heading. That is case 2 of "Find where you are", so I went to step 1.
Step 1: #10 was closed as completed by merged PR 7 into main (`Closes #10`). #20 was closed as completed by merged PR 8 into main (`Fixes #20`). Both shipped. Nothing was dropped, nothing blocks the cut and nothing was carried over.
Step 2: the last Release ended at e79583d (top entry `Commits: 5a545b2..e79583d`) and main's tip is 30bb03d. The commits in between are d42d9ed (the Release 1 changelog, PR 6, which rides along unlisted), 7a95533 (PR 7 -> #10), 2f668f6 (PR 8 -> #20) and 30bb03d (PR 9, which covers no issue). No open pull request names #2. Cut steps: none. Versioning policy: none, so no version line.
PR number: issue and pull request numbers share one space (issues #10, #20 and #21 exist), so the new pull request takes 22 and the new release issue takes 23.

### 1. Run a command
Issue: new (PR 22), branch `release/release-2`
Command: bash test.sh
Result: passes (`OK`). This is the whole-Release check on the changelog branch.

### 2. Open a pull request
Issue: new (PR 22)
Branch: release/release-2
Title: docs(release): Release 2
Body:
~~~
## Summary

```diff
 # Changelog

+## Release 2 (2026-11-04)
+
+Say goodbye and keep quiet.
+
+Commits: e79583d..30bb03d.
+
+- Farewell command (#10)
+- Quiet flag (#20)
+
+Also merged: README usage (#9).
+
 ## Release 1 (2026-10-16)
```

Changelog entry for Release 2. Release issue: #2 (this pull request does not close it).

- **Start commit:** e79583d
- **End commit:** 30bb03d
- **Dropped issues:** none.

## Evidence

- **Tests:** docs-only change. The whole-Release check, `bash test.sh`, passes on this branch (`OK`).
- **Checks:** `bash test.sh`: OK.
- **Screenshots:** not visual.

## Merge Danger

**Door:** two-way

**Blast Radius:** changelog

🤖 Generated with [Claude Code](https://claude.com/claude-code)

~~~
File: CHANGELOG.md
~~~
# Changelog

## Release 2 (2026-11-04)

Say goodbye and keep quiet.

Commits: e79583d..30bb03d.

- Farewell command (#10)
- Quiet flag (#20)

Also merged: README usage (#9).

## Release 1 (2026-10-16)

Hello greets by name.

Commits: 5a545b2..e79583d.

- Hello command (#3)
~~~

Merging: the Boundary record says agents merge every pull request whose checks pass, changelog pull requests included. No action here needs the user's approval, the Door is two-way, and no repo rule says a person merges, so the agent merges. No `Agent-merged rules:` line is needed (no ADR, glossary, CLAUDE.md, AGENTS.md or REVIEW.md changes). Pre-merge step: I fetched main, and it is still at 30bb03d, so the end commit stands. Merge-time steps: none (CLAUDE.md and the release doc give none). Sync: the branch is cut from main's tip, so no merge from main is needed.

### 3. Run a command
Issue: PR 22, branch `release/release-2`, at its head
Command: bash test.sh
Result: passes. This is the rerun of checks before the merge. The repo has no CI.

### 4. Merge a pull request
Issue: PR 22
Pull: 22
Method: squash, titled `docs(release): Release 2`, with the pull request's body as the commit message.

After the merge: PR 22 reads merged. It has no closing lines and builds no issue, so nothing is closed. Step 3 then reads `## Release 2 (2026-11-04)` from CHANGELOG.md on main.

### 5. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
## Release 2 (2026-11-04)

Say goodbye and keep quiet.

Commits: e79583d..30bb03d.

- Farewell command (#10)
- Quiet flag (#20)

Also merged: README usage (#9).
~~~

### 6. Close
Issue: 02-release-2.md
Outcome: completed
Reason: Release 2 is cut. Its changelog entry merged in PR 22, and its notes are posted above.

### 7. Run a skill
Issue: 02-release-2.md
Skill: triage
Brief:
~~~
Run the Triage batch at the end of Release 2, naming release issue #2 (closed, notes posted). Milestone #1. Boundary record: docs/dev-skills/boundaries.md. Main is at the squash merge of PR 22, on top of 30bb03d.
~~~

### 8. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
<!-- release end-of-Release pass -->
triage ran for this Release.
~~~

### 9. Run a skill
Issue: 02-release-2.md
Skill: retro-planning
Brief:
~~~
Run the Release-end Retro planning ("At a Release end") for Release 2, naming release issue #2. Milestone #1. Boundary record: docs/dev-skills/boundaries.md. Cap: none (Release end).
~~~

### 10. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
<!-- release end-of-Release pass -->
retro-planning ran for this Release.
~~~

Step 5: Milestone #1 is open. In the dry run, triage and retro-planning changed nothing.
Check against main: the only issue in scope is #21 Shout flag (open, no release label, not parked, in Milestone 1). The Milestone issue and the release issues are records, so they are not checked. #21 is **still valid**: main's src/greet.sh handles only `hello` and has no `-s` flag. That needs no write.
Candidates: #21, a planned feature (Milestone feature 3), at ready-for-agent, with no blockers (`Blocked by: none`). There are no severe issues, no `next-release` issues, no ready-for-agent bugs, nothing carried over from Release 2 and no unplanned features.
Ranked list: group 2: #21. Taken: 1 of 5.
Name: Release 3 / `release-3`. No closed issue carries `release-3`, and the label does not exist yet.

### 11. Create an issue
Issue: new (23-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter can shout, so Milestone 1's last planned command is built.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 1.

## Order

1. #21 Shout flag: the only planned feature of Milestone 1 still open. It has no blockers and nothing depends on it, and it is the last thing the Milestone's goal needs.

## Left out

None.

## Checked against main

Main at the squash merge of PR 22 (`docs(release): Release 2`), on top of `30bb03d`.

- #21 Shout flag: still valid

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 12. Create a label
Issue: none
Label: release-3

### 13. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none
