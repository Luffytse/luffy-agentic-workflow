# Proposed actions (dry run)

### 1. Open a pull request
Issue: new (PR 10)
Branch: release/release-2
Title: docs(release): Release 2
Body:
~~~
## Summary

Cuts Release 2 (release issue #2): adds its changelog entry.

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
- Shipped: #10 (closed by PR #7), #20 (closed by PR #8). Also merged: PR #9 (no issue). The Release 1 changelog merge (PR #6) rides along unlisted.
- Dropped issues: none.

## Evidence

- **Tests:** docs-only change; no test covers it. Checked each listed issue's closing pull request: #7 `Closes #10`, #8 `Fixes #20`, both merged into main.
- **Checks:** whole-Release check `bash test.sh` on this branch: passed (`OK`).
- **Screenshots:** not visual.

## Merge Danger

**Door:** two-way

**Blast Radius:** changelog-only

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
Issue: PR 10
Command: bash test.sh

### 3. Merge a pull request
Issue: PR 10
Pull: 10

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
Reason: Release 2 is cut: its changelog entry merged to main (PR 10) and is posted above as its notes.

### 6. Run a skill
Issue: 02-release-2.md
Skill: triage
Brief:
~~~
Run the Triage batch for Release 2, which just closed. Release issue: #2 (.scratch/issues/02-release-2.md). Its Milestone is #1 (Milestone 1: Round out the greeter's commands). Read the release issue, the Milestone issue and docs/dev-skills/boundaries.md, fetch main, then triage every open needs-triage issue and sweep the ready-for-agent backlog. Post the `## Triage batch` summary on #2.
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
Run the Release-end Retro planning ("At a Release end") for Release 2, which just closed. Release issue: #2 (.scratch/issues/02-release-2.md); the Triage batch for it has already run. Its Milestone is #1. Agents decide every group; no cap applies; mark the Ticket of each group that joins the next Release with next-release.
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
**Goal:** The greeter shouts on request, the last command the Milestone plans.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 1.

## Order

1. #21 Shout flag: planned feature (group 2), the only feature the Milestone lists that is still open; no feature depends on another and it has no open blockers, and building it completes every feature the Milestone lists.

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
