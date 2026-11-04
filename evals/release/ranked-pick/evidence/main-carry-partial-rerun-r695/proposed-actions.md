### 1. Open a pull request
Issue: new (PR 8)
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

Start commit: bcfabd7. End commit: b24a688.

Dropped issues: none.

Carried over (in #2's `## Carried over`, not listed): #31.

## Evidence

- **Tests:** docs only; whole-Release check `bash test.sh` on this branch: passes (OK).
- **Checks:** `bash test.sh`: OK.
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

Commits: bcfabd7..b24a688.

- Farewell command (#10)

## Release 1 (2026-10-16)

Hello greets by name.

Commits: e92f988..bcfabd7.

- Hello command (#3)
~~~

### 2. Run a command
Issue: PR 8
Command: bash test.sh

### 3. Merge a pull request
Issue: PR 8
Pull: 8

### 4. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
## Release 2 (2026-11-04)

Say goodbye and keep quiet.

Commits: bcfabd7..b24a688.

- Farewell command (#10)
~~~

### 5. Close
Issue: 02-release-2.md
Outcome: completed
Reason: Release 2 cut; changelog merged in PR 8, notes posted.

### 6. Run a skill
Issue: 02-release-2.md
Skill: triage
Brief:
~~~
Run the Triage batch for Release 2, just closed. Release issue: #2 (02-release-2.md).
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
Run the Release-end Retro planning for Release 2, just closed. Release issue: #2 (02-release-2.md).
~~~

### 9. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
<!-- release end-of-Release pass -->
retro-planning ran for this Release.
~~~

### 10. Create a label
Issue: none
Label: release-3

### 11. Create an issue
Issue: new (32-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter shouts on request and greets an empty name sensibly.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 2.

## Order

1. #21 Shout flag: planned feature, the last one the Milestone lists after #10; no blockers, and it completes the Milestone's commands.
2. #31 Empty name prints `Hello, !`: group 3, carried over from Release 2 (the user chose to keep it going); a `ready-for-agent` bug, open since 2026-09-15.

## Left out

None.

## Checked against main

Main at the merge of PR 8 (Release 2 changelog, on b24a688).

- #21 Shout flag: still valid
- #31 Empty name prints `Hello, !`: still valid

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 12. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none

### 13. Apply / remove labels
Issue: 31-empty-name.md
Add: release-3
Remove: none
