Driven by: the Ticket thread, a fresh regular-tier subagent, decision-level, given PROMPT.md and the branch's skill folder at dde4766; scored with score.py.

Title: The usage line says "helo"
Branch: git -C <runs>/impl-valid-branch/repo fetch origin && git -C <runs>/impl-valid-branch/repo worktree add <runs>/impl-valid-branch/wt-40-usage-typo -b ticket-40-usage-typo origin/main && git -C <runs>/impl-valid-branch/wt-40-usage-typo push -u origin ticket-40-usage-typo
Brief: Ticket 40, "The usage line says \"helo\"" (.scratch/issues/40-usage-typo.md), regular tier. Work only in the worktree <runs>/impl-valid-branch/wt-40-usage-typo on branch ticket-40-usage-typo, committing there and running every git command as `git -C <runs>/impl-valid-branch/wt-40-usage-typo ...`; the worktree is a fresh checkout. Fix src/greet.sh so no-argument usage prints `usage: greet.sh hello <name>`, test-first with the tdd skill (add the test to test.sh, see it fail, then pass); run `bash test.sh` before each push. Check `git status -sb` shows the branch before each push and report `git rev-parse origin/ticket-40-usage-typo` equals HEAD after it. Leave the version/any bump alone. Report evidence: test failing before and passing after, checks, "not visual", and your one-way-door call.
Message: none
Thread: building
