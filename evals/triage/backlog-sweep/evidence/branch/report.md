# Triage batch for Release 3 (release issue #4): report to the user

Run 2026-11-04 09:00 UTC by the Release thread's end-of-Release pass, against main 5f89fa4. Every write is proposed in `.scratch/proposed-actions.md` (dry-run tracker). Nothing needed your decision; nothing waits on you.

## New issues (part 1)
- **#41 world-readable name log**: bug, ready-for-agent, `next-release`. Reproduced: every run appends the name to `/tmp/greet.log` and chmods it 0666; some callers pass email addresses. Severe (security/personal data), so it must join the next Release.
- **#50 --json output**: enhancement, ready-for-human. An audit agent filed it; you decide whether the greeter gets this feature.

## Backlog sweep (part 2)
- **#51 Colour the greeting**: moved to ready-for-human (retro-agent finding; your call).
- **#31** closed as a duplicate of **#30** (usage line says `helo`).
- **#32** closed as obsolete: fixed by 6ab449a / PR #8.
- **#40 Flags after the name are dropped**: marked `next-release`, since it blocks the Milestone's Quiet flag (#20).
- **#33 HELLO in upper case**: expired (left out of Releases 1, 2 and 3). Reopen to bring it back.
- Unchanged: #20 (planned feature, never expires), #30, #34, #36, #41.

## For your attention
- #50 and #51 wait at ready-for-human for you to accept, shape or close.
- Release size is 1, but two issues now carry `next-release` (#41 severe, #40 blocking #20). A severe issue joins past the size, so the next Release planning should take both.
