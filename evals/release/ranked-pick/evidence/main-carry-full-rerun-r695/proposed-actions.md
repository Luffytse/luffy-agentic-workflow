### 1. Open a pull request
Issue: new (PR 32)
Branch: docs/release-2
Title: docs(release): Release 2
Body:
~~~
## Summary

Adds the Release 2 entry to `CHANGELOG.md`, for release issue #2 (this pull request does not close it; the Release thread closes it with its notes after the merge).

```diff
 # Changelog

+## Release 2 (2026-11-04)
+
+Say goodbye and keep quiet.
+
+Commits: bcfabd7..7be173c.
+
+- Nothing shipped: every issue in this Release (#10, #31) was carried over.
+
+Also merged: README usage (#9).
+
 ## Release 1 (2026-10-16)
```

Start commit: `bcfabd7` (end of Release 1). End commit: `7be173c` (main's tip). The Release 1 changelog merge (`c12bde9`, #6) rides along unlisted.

Dropped issues: none. Carried over (listed on #2, not in the entry): #10, #31.

## Evidence

- **Tests:** docs-only change; the whole-Release check, `bash test.sh` on this branch, passes (`OK`).
- **Checks:** `bash test.sh`: OK. Cut steps: none (versioning policy: none).
- **Screenshots:** not visual.

## Merge Danger

**Door:** two-way

**Blast Radius:** changelog
~~~
File: CHANGELOG.md
~~~
# Changelog

## Release 2 (2026-11-04)

Say goodbye and keep quiet.

Commits: bcfabd7..7be173c.

- Nothing shipped: every issue in this Release (#10, #31) was carried over.

Also merged: README usage (#9).

## Release 1 (2026-10-16)

Hello greets by name.

Commits: e92f988..bcfabd7.

- Hello command (#3)
~~~

### 2. Run a command
Issue: PR 32
Command: bash test.sh

### 3. Merge a pull request
Issue: PR 32
Pull: 32

### 4. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
## Release 2 (2026-11-04)

Say goodbye and keep quiet.

Commits: bcfabd7..7be173c.

- Nothing shipped: every issue in this Release (#10, #31) was carried over.

Also merged: README usage (#9).
~~~

### 5. Close
Issue: 02-release-2.md
Outcome: completed
Reason: Release 2 cut; its changelog entry (PR #32) is on main and posted above as its notes.

### 6. Run a skill
Issue: 02-release-2.md
Skill: triage
Brief:
~~~
Run the Triage batch for Release 2, just closed. Release issue: #2 (.scratch/issues/02-release-2.md).
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
Run the Release-end Retro planning for Release 2, just closed. Release issue: #2 (.scratch/issues/02-release-2.md).
~~~

### 9. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
<!-- release end-of-Release pass -->
retro-planning ran for this Release.
~~~

### 10. Create an issue
Issue: new (33-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter says goodbye and shouts on request, and an empty name no longer prints `Hello, !`.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #10 Farewell command: first in the Milestone's order; no feature depends on another, so the order breaks the tie; carried over from Release 2.
2. #21 Shout flag: second in the Milestone's order; completes the Milestone's planned features.
3. #31 Empty name prints `Hello, !`: a `ready-for-agent` bug carried over from Release 2, which the user chose to keep going (oldest open bug, filed 2026-09-15).

## Left out

None.

## Checked against main

Main at the squash merge of #32 (parent `7be173c`).

- #10 Farewell command: still valid
- #21 Shout flag: still valid
- #31 Empty name prints `Hello, !`: still valid

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 11. Create a label
Issue: none
Label: release-3

### 12. Apply / remove labels
Issue: 10-farewell.md
Add: release-3
Remove: none

### 13. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none

### 14. Apply / remove labels
Issue: 31-empty-name.md
Add: release-3
Remove: none
