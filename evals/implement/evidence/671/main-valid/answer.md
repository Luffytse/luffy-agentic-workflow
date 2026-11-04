Driven by: the Ticket thread, a fresh regular-tier subagent, decision-level, given PROMPT.md and main's skill folder from a git archive of origin/main 91a35d3; scored with score.py.

Title: The usage line says "helo"
Branch: git fetch origin && git worktree add ../wt-40-usage-typo -b ticket-40-usage-typo origin/main && git -C ../wt-40-usage-typo push -u origin ticket-40-usage-typo
Brief: Build ticket 40, "The usage line says "helo"" (.scratch/issues/40-usage-typo.md), in the worktree ../wt-40-usage-typo (absolute path of the sibling of the repo checkout) on branch ticket-40-usage-typo; commit only there and run every git command as `git -C <path> ...`. The worktree is a fresh checkout; start at docs/dev-skills/index.md (absent here, so see CLAUDE.md: run `bash test.sh` before each push); build test-first with tdd so the usage line in src/greet.sh reads `usage: greet.sh hello <name>`, with a test in test.sh; check `git status -sb` shows the branch before each push and report `git rev-parse origin/ticket-40-usage-typo` equals HEAD after; regular tier; report the failing-then-passing test, `bash test.sh` output, "not visual", and your one-way-door call.
Message: none
Thread: building
