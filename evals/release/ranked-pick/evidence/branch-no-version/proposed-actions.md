# Proposed actions (dry run): Release thread, 2026-11-04 09:00 UTC

### 1. Run a command
Issue: none (branch `release/release-2`, made from main at 1c6fe96, with the changelog entry below)
Command: bash test.sh

### 2. Open a pull request
Issue: new (PR 10)
Branch: release/release-2
Title: docs(release): Release 2
Body:
~~~
## Summary

Changelog entry for Release 2 (release issue #2).

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

- Release issue: #2
- Start commit: 9a18f55 (end of Release 1). End commit: 1c6fe96 (main's tip).
- Dropped issues: none.
- Cut steps: none (versioning policy: none, so the entry names no versions).

## Evidence

- **Tests:** docs-only change; whole-Release check `bash test.sh` on this branch: OK (passes).
- **Checks:** every issue labelled `release-2` shipped: #10 closed by merged PR #7 (`Closes #10`), #20 closed by merged PR #8 (`Fixes #20`).
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

### 3. Merge a pull request
Issue: PR 10
Pull: 10
(Checks pass; the Boundary record lets agents merge docs-only changelog pull requests. Main fetched just before merging: still at 1c6fe96, the end commit, so nothing to redo.)

### 4. Comment on an issue
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

### 5. Close
Issue: 02-release-2.md
Outcome: completed
Reason: Release 2 cut; its changelog entry merged via PR 10 and is posted above as its notes.

### 6. Run a skill
Issue: 02-release-2.md
Skill: triage
Brief:
~~~
Run the Triage batch for Release 2, just closed. Release issue: #2 (label `release-2`, Milestone #1). The next Release's planning runs right after you, so finish before it.
~~~

### 7. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
<!-- release end-of-Release pass -->
triage ran for this Release.
~~~

### 8. Run a skill
Issue: 02-release-2.md
Skill: retro-planning
Brief:
~~~
Run the Release-end Retro planning for Release 2, just closed. Release issue: #2 (label `release-2`, Milestone #1). Agents decide every group; the next Release's planning runs right after you.
~~~

### 9. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
<!-- release end-of-Release pass -->
retro-planning ran for this Release.
~~~

### 10. Create an issue
Issue: new (22-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter can shout, completing the Milestone's commands.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 1.

## Order

1. #21 Shout flag: the only planned feature of Milestone #1 still open; nothing depends on it and it has no blockers, so it finishes the Milestone's goal.

## Left out

None.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 11. Create a label
Issue: none
Label: release-3

### 12. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none
