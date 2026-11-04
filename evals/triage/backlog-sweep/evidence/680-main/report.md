# Triage batch, Release 3 (#4): report for the user

Run 2026-11-04 09:00 UTC by the Release thread's end-of-Release pass. The tracker is in dry-run mode, so every write is proposed in `.scratch/proposed-actions.md` (16 blocks) and not applied.

## Needs your attention (no reply needed for the batch to finish)

- **#41 is a security hole and gets `next-release`.** `src/greet.sh` appends every name it is given (some callers pass email addresses) to `/tmp/greet.log` and makes that file mode 0666, readable and writable by every user. This has been on main since the first commit. Any machine that ran the greeter may already hold such a log; the fix cannot delete it there.
- **Two agent-found enhancements wait for you at `ready-for-human`:** #50 (`--json` output, from an architecture audit) and #51 (`--colour`, from a retro, moved off `ready-for-agent`). Only you can accept these (move them to `ready-for-agent`) or close them.

## Decisions

| Issue | Outcome |
| --- | --- |
| #41 name log | bug, ready-for-agent, `next-release` (severe) |
| #50 --json | enhancement, ready-for-human (agent-found) |
| #31 usage typo | closed as duplicate of #30 |
| #32 empty name | closed as obsolete (fixed by PR #8, 6ab449a) |
| #33 upper case | expired (left out of Releases 1, 2, 3); reopen to bring it back |
| #40 flag parse | `next-release` (blocks planned feature #20) |
| #51 colour | moved to ready-for-human (agent-found) |

Unchanged: #20, #30, #34, #36. Nothing went to you as a question under "Goes to the user".
