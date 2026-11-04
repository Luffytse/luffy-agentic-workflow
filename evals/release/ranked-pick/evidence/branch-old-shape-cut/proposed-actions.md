# Proposed actions (dry run)

Release thread, 2026-11-04T09:00Z. "Find where you are": release issue #2 (Release 2) is open, written before the Order list (a `## Scope` list, no `## Order`), and its label `release-2` is carried by #10 and #20, so it is the current Release (case 2). `CHANGELOG.md` on main has no `## Release 2` heading, so the run starts at step 1.

Step 1: #10 (closed completed, `Closes #10` in merged PR #7 into main) and #20 (closed completed, `Fixes #20` in merged PR #8 into main) both shipped. Nothing dropped, nothing blocks the cut.

Step 2: start commit 9a18f55 (end commit of Release 1's `Commits:` line), end commit 1c6fe96 (main's tip). Commits between: dfc536d (#6, Release 1's changelog merge, rides along unlisted), e2f6abd (#7, closes #10), a5dd9f8 (#8, closes #20), 1c6fe96 (#9, no issue: "Also merged"). No open pull request names #2. Cut steps: none. PR number 22 is the next number free across issues and pull requests (issue numbers run to #21).

### 1. Open a pull request
Issue: new (PR 22)
Branch: release-2-changelog
Title: docs(release): Release 2
Body:
~~~
## Summary

Changelog entry for Release 2 (release issue #2).

```diff
 # Changelog
 
+## Release 2 (2026-11-04)
+...
 ## Release 1 (2026-10-16)
```

- **Release issue:** #2
- **Commits:** 9a18f55..1c6fe96 (start: Release 1's end commit; end: main's tip)
- **Shipped:** #10 Farewell command, #20 Quiet flag
- **Also merged:** #9 (README usage, no issue)
- **Dropped:** none

## Evidence

- **Tests:** docs-only change; whole-Release check `bash test.sh` on this branch: OK.
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

### 2. Run a command
Issue: PR 22
Command: bash test.sh (whole-Release check, on branch release-2-changelog)

### 3. Run a command
Issue: PR 22
Command: git fetch origin main (just before merging: main is still at 1c6fe96, the end commit, so nothing is redone)

### 4. Merge a pull request
Issue: PR 22
Pull: 22

Step 3: the entry below is taken from `CHANGELOG.md` on main after the merge (heading `## Release 2 (2026-11-04)` through the line before `## Release 1`).

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
Reason: Release 2 cut: changelog PR #22 merged; notes posted above.

Step 4: end-of-Release pass.

### 7. Run a skill
Issue: 02-release-2.md
Skill: triage
Brief:
~~~
Run the Triage batch at a Release end for Release 2, release issue #2 (closed, Milestone #1). Agents decide; ask the user nothing per issue except as "Goes to the user" says. Post the `## Triage batch` summary comment on #2.
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
Run Retro planning at a Release end for Release 2, release issue #2 (closed, Milestone #1), after the Triage batch. Agents decide every group; no cap applies.
~~~

### 10. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
<!-- release end-of-Release pass -->
retro-planning ran for this Release.
~~~

Step 5: plan Release 3. Milestone #1 is open. Candidates (open, no release label, not parked): #21 Shout flag only (a planned feature, Milestone row 3, `ready-for-agent`, no blockers). No severe, `next-release` or `ready-for-agent` bug issues; nothing carried over; no unplanned features. Name: `Release 3`, label `release-3` (no closed issue carries it). Release issue number 23 (22 is the changelog PR).

### 11. Create an issue
Issue: new (23-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter can shout, completing the Milestone's planned commands.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 1.

## Order

1. #21 Shout flag: the only planned feature still open (Milestone row 3, after Farewell and Quiet, both shipped in Release 2); no feature depends on it and it has no blockers, and it completes the Milestone's goal.

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
