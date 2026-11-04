# Proposed actions (Release thread, 2026-11-04 09:00 UTC)

Where I am: release issue #02 (Release 2) is open, its issues carry `release-2`, and CHANGELOG.md on main has no `## Release 2` entry, so the run starts at step 1. Step 1: #10 shipped (PR 7, merged into main, `Closes #10`); #20 shipped (PR 8, merged into main, `Fixes #20`). Nothing dropped, nothing blocks the cut.

### 1. Run a command
Issue: new (PR 10)
Command: `bash test.sh` on branch `release-2-changelog` (made from main at 1c6fe96, with the entry below added). Result: OK.

### 2. Open a pull request
Issue: new (PR 10)
Branch: release-2-changelog
Title: docs(release): Release 2
Body:
~~~
## Summary

Adds the Release 2 entry to `CHANGELOG.md`, for release issue #2 (it stays open; the Release is closed with its notes after this merges).

```diff
 # Changelog

+## Release 2 (2026-11-04)
+
+Say goodbye and keep quiet.
+
+Commits: 9a18f55..1c6fe96.
+
+- Farewell command (#10)
+- Quiet flag (#20)
+
+Also merged: README usage (#9).
+
 ## Release 1 (2026-10-16)
```

- Start commit: 9a18f55 (end of Release 1's `Commits:` line). End commit: 1c6fe96 (main's tip).
- Shipped: #10 (PR 7), #20 (PR 8). Also merged: PR 9 (no issue). Release 1's changelog merge (PR 6) rides along unlisted.
- Dropped issues: none.
- Versions: none; the release doc's versioning policy is none. Cut steps: none.

## Evidence

- **Tests:** docs-only change; the whole-Release check `bash test.sh` on this branch: OK.
- **Checks:** `bash test.sh`: OK.
- **Screenshots:** not visual.

## Merge Danger

**Door:** two-way

**Blast Radius:** docs

🤖 Generated with [Claude Code](https://claude.com/claude-code)

~~~
File: CHANGELOG.md
~~~
# Changelog

## Release 2 (2026-11-04)

Say goodbye and keep quiet.

Commits: 9a18f55..1c6fe96.

- Farewell command (#10)
- Quiet flag (#20)

Also merged: README usage (#9).

## Release 1 (2026-10-16)

Hello greets by name.

Commits: d8757cb..9a18f55.

- Hello command (#3)
~~~

### 3. Run a command
Issue: PR 10
Command: Pre-merge (merging, "Before the merge"): fetch main; main is still at 1c6fe96, the end commit, so the branch needs no update. Repo merge-time steps: none (release doc and CLAUDE.md give none). Rerun `bash test.sh` on the branch head. Result: OK. The Boundary record lets agents merge it; no `Agent-merged rules:` line (it changes only CHANGELOG.md).

### 4. Merge a pull request
Issue: PR 10
Pull: 10
Method: squash, commit title `docs(release): Release 2`, commit message the pull request's body. Committer: this Release thread. It builds no issue, so the merge closes none.

### 5. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
## Release 2 (2026-11-04)

Say goodbye and keep quiet.

Commits: 9a18f55..1c6fe96.

- Farewell command (#10)
- Quiet flag (#20)

Also merged: README usage (#9).
~~~

### 6. Close
Issue: 02-release-2.md
Outcome: completed
Reason: Release 2 is cut: its changelog entry merged in PR 10 and is posted above as its notes.

### 7. Run a skill
Issue: 02-release-2.md
Skill: triage
Brief:
~~~
Run the Triage batch for Release 2, release issue #2 (closed), Milestone #1. Agents decide; ask the user nothing except as "Goes to the user" says. Read the release issue, Milestone #1 and docs/dev-skills/boundaries.md, fetch main, then triage the open needs-triage issues, sweep the backlog, and post the `## Triage batch` summary comment on #2. Skip retro issues.
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
Run the Release-end Retro planning for Release 2, release issue #2 (closed), Milestone #1.
~~~

### 10. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
<!-- release end-of-Release pass -->
retro-planning ran for this Release.
~~~

### 11. Create an issue
Issue: new (22-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter can shout, which completes the Milestone's commands.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 1.

## Order

1. #21 Shout flag: the only planned feature of Milestone #1 still open; nothing depends on it and it has no open blockers, and it completes the Milestone's goal.

## Left out

None.

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
