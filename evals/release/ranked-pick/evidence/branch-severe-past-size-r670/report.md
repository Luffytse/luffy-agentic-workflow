# Release thread report (2026-11-04 09:00 UTC)

**Where I started.** No open release issue; Release 2 (#2) is closed, cut, and holds both end-of-Release records (triage, retro-planning). No open issue carries an unnamed release label. So this run went straight to step 5: plan the next Release, **Release 3** (label `release-3`, release issue #38), for Milestone 1 (#1).

## Order (size 2, used 2, plus 1 severe past the size)

1. #36 test.sh fails on main, so no pull request can pass: severe (delivery stopped); oldest severe issue.
2. #31 `--save` overwrites ~/.profile: severe (lost data).
3. #37 test.sh prints the registry token in CI logs: severe (security hole); joins past the size because it is severe.

## Left out (size reached)

- #35 test.sh takes 10 s (`next-release`; keeps its mark for the next planning).
- #10 Farewell command (Spec, with Tickets #11, #12): first planned feature.
- #20 Quiet flag: second planned feature.

Note: three severe issues fill this Release, so neither Milestone feature, nor the `next-release` issue #35, gets into it.

## Check against main (main at `788e2cf`)

All 8 issues in scope are still valid: #10, #11, #12, #20, #31, #35, #36, #37. I confirmed on main: `src/greet.sh` has no `bye` or `-q` and writes over `$HOME/.profile` on `--save`; `test.sh` has `sleep 10`, echoes `$REGISTRY_TOKEN`, and fails (`bash test.sh` exits 1, since greet prints `Hello, Ada!` but the test expects `Hello, Ada.`).

The skill says that with more than 5 issues, read-only premium-tier subagents should do the checking. This thread has no tool for starting subagents, so I read all 8 myself.

## Questions raised

None.

## Features proposed

None. Every open enhancement is listed in the Milestone issue.

## Writes (dry run, see `.scratch/proposed-actions.md`)

1. Open release issue #38 "Release 3".
2. Create label `release-3`.
3–5. Apply `release-3` to #36, #31, #37. None of them carried `next-release`, so no mark was removed.
