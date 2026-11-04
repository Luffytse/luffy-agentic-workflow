# Proposed actions (dry run): Release 2 cut and Release 3 planning

### 1. Run a command
Issue: new (PR 22)
Command: `bash test.sh` on branch `docs/release-2` (the release doc's whole-Release check; also the repo's pre-push check). Result: `OK` (run locally on main's tree plus this entry, which changes only CHANGELOG.md).

### 2. Open a pull request
Issue: new (PR 22)
Branch: docs/release-2
Title: docs(release): Release 2
Body:
~~~
## Summary

Changelog entry for Release 2 (release issue #2), covering everything merged since Release 1.

```diff
 # Changelog
+
+## Release 2 (2026-11-04)
+...
 ## Release 1 (2026-10-16)
```

- Release issue: #2
- Start commit: 9a18f55. End commit: 1c6fe96.
- Versions delivered: none; this repo keeps no version (release doc, "Policy: none").
- Shipped: #10 Farewell command (PR #7), #20 Quiet flag (PR #8).
- Also merged: #9 docs: README usage.
- Dropped issues: none.

## Evidence

- **Tests:** docs-only change; no test covers it.
- **Checks:** whole-Release check `bash test.sh` on this branch: `OK`.
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

Commits: 9a18f55..1c6fe96.

- Farewell command (#10)
- Quiet flag (#20)

Also merged: docs: README usage (#9).

## Release 1 (2026-10-16)

Hello greets by name.

Commits: d8757cb..9a18f55.

- Hello command (#3)
~~~

### 3. Merge a pull request
Issue: PR 22
Pull: 22
(Just before merging, main was re-read: still at the end commit 1c6fe96, so the entry stands. The Boundary record lets agents merge docs-only changelog pull requests whose checks pass.)

### 4. Comment on an issue
Issue: 02-release-2.md
Body:
~~~
## Release 2 (2026-11-04)

Say goodbye and keep quiet.

Commits: 9a18f55..1c6fe96.

- Farewell command (#10)
- Quiet flag (#20)

Also merged: docs: README usage (#9).
~~~

### 5. Close
Issue: 02-release-2.md
Outcome: completed
Reason: Release 2 cut; changelog pull request #22 merged and its entry posted as the notes.

### 6. Run a skill
Issue: 02-release-2.md
Skill: triage
Brief:
~~~
Triage batch for Release 2 (release issue #2, just cut), inside Milestone 1 (#1). Look at incoming issues and mark each that must join the next Release as `joins the next Release`, recording the batch as a `## Triage batch` comment on #2.
~~~

### 7. Run a skill
Issue: 02-release-2.md
Skill: retro-planning
Brief:
~~~
Release-end Retro planning for Release 2 (release issue #2, just cut), inside Milestone 1 (#1). Agents decide every group; record verdicts in a closed retro-planning issue.
~~~

### 8. Create a label
Issue: none
Label: release-3

### 9. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none

### 10. Create an issue
Issue: new (23-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter can shout, completing Milestone 1's planned commands.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Cap:** 5 features. Used: 1. Maintenance fixes: 0, outside the cap.

## Scope

- **Shout flag**: third and last planned feature in Milestone 1's order (after #10 and #20, both shipped in Release 2); it completes the Milestone's command set.
  - #21 Shout flag

Maintenance fixes: none. The Triage batch and Release-end Retro planning for Release 2 left no record (no `## Triage batch` comment on #2, no closed retro-planning record), so maintenance fixes were not read for this Release.

## Left out

None. #21 was the only candidate.

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.

Planned by the Release thread from the Milestone issue's order, without waiting for the user.
~~~
