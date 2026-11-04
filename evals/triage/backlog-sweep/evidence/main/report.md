# Triage batch, Release 3 (#4): report for the user

Ran 2026-11-04 09:00 UTC, inside Milestone 1 (#1). The tracker is in dry-run mode: every write is a proposed block in `.scratch/proposed-actions.md` (blocks 1 to 7), and nothing under `.scratch/issues/` changed.

## Decided

| Issue | Category | State | Disposition |
| --- | --- | --- | --- |
| #41 greet.sh writes every name to a world-readable log | bug | ready-for-agent | joins the next Release (severe: security and privacy) |
| #50 Add a --json output mode | enhancement | ready-for-agent | stays open (outside Milestone 1's features; build after #40) |

Nothing went to you for a decision, and no issue was handled at once since the last summary.

## Needs you

- **#41, data already exposed.** I reproduced it: a run appends the name to `/tmp/greet.log` and makes that file mode 0666. The fix stops new writes, but every machine that ran the greeter still has a world-readable log holding past names, email addresses among them. Deleting those files, and deciding whether anyone needs telling, is yours to do; the brief leaves it out of scope.
- I applied no `next-release` or release label to #41. The triage skill leaves release labels to Release planning, and the release doc lets a severe issue join past the Release size of 1.

## Seen but outside the batch (not acted on)

The batch covers only `needs-triage` issues. These already-`ready-for-agent` issues look worth a look at the next Release planning or triage:

- #30 and #31 report the same `helo` typo in the usage line. One is probably a duplicate of the other.
- #32 (hello with no name prints `Hello, !`) looks fixed by PR #8: the name now defaults to `world`.
- #36 (usage line does not mention bye) is still true: the usage line printed on stderr names only `helo`.
- My checks ran the greeter, and `bash test.sh` runs it too, so this machine's `/tmp/greet.log` gained a few test lines (`Ada`). I removed the `probe@example.com` line I added.
