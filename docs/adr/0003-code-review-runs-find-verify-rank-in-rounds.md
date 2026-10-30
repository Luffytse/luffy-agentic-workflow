# agentic-review runs Find, Verify and Rank, in rounds of 2 to 5

Our `agentic-review` skill follows the shape of Claude Code's own Code Review (several Finders, then a verify step that drops false positives, then ranking by Severity), adapted to agents that review their own pull requests in a session. We kept Upstream's two Finders (standards and spec) and added cheap adversarial Finders, a regular-tier Verifier, and Rounds that stop early once nothing Important remains.

## How a Review runs

1. **Find.** The standards Finder and spec Finder (regular tier) run in parallel with 2 adversarial Finders (cheap tier). When there is no spec or ticket, the spec Finder is skipped and the Review says so. Each adversarial Finder takes one angle chosen to fit the pull request, such as bugs and edge cases, security and privacy, or contradictions with the ADRs and glossary. Every Finding proposes a Severity, names its Bug class, and lists every place in the pull request where that class occurs (in commit Rounds too, not only in the new commits).
2. **Verify.** For each candidate Finding, a Verifier (regular tier) opens the cited file and line and checks the claim against the code itself, not against names. It makes the final call on four things, with one line of reasoning each: whether the Finding is real (keep or drop); whether this pull request caused it (if not, its Severity is Pre-existing); whether it is Important or a Nit, confirming or changing the Finder's proposal; and, for a Nit, whether to "fix" or "skip" it. On Quick and Standard, one Verifier agent checks all the Findings of a Review. On Deep, three Verifiers each check every Finding: a Finding is kept only when at least two say it is real, and the Verifiers who said it is real decide the other calls by majority. If they tie, or Severity splits three ways, the more cautious value wins (Important over Nit, caused-by-this-pull-request over Pre-existing, "fix" over "skip").
3. **Rank.** The kept Findings are deduplicated, Findings already dismissed in an earlier Round (dropped by Verify, or Nits marked "skip") are dropped, and Findings already raised are not reported again but stay open until fixed (an unfixed Important still blocks the stop). The rest are sorted by Severity. At most 5 Nits are reported, "fix" Nits first.

Without a `REVIEW.md` saying otherwise, **Important** means the change would break behaviour, lose or leak data, contradict the spec or an ADR, or make a rollback unsafe; anything else real is a **Nit**.

Each Review keeps a record of every Finding raised or dismissed in its pull request, so later Rounds can drop repeats and `retro` can see which Bug classes came up more than once. Each Round posts one comment on the pull request listing the Findings it raised and dismissed, and that is the record; `retro` reads all of them.

Every Round starts brand-new Finder and Verifier agents; none is reused from an earlier Round, so each Round reads the code with fresh eyes.

## Review depth

- **Quick:** the standards and spec Finders only, one Verifier.
- **Standard (default):** all four Finders, one Verifier.
- **Deep:** the Finders above plus a **security Finder** on the premium tier, and three Verifiers that each take a different stance: a **tracer** that follows the code path to show the bug happens, a **skeptic** that argues it is a false positive, and a **spec checker** that judges it against the spec, ADRs and tests. Every Finding, the security Finder's included, is kept only when at least two of the three agree.

Deep is for risky pull requests (security, money, deleting data, or anything the user marks), Quick for docs-only or trivial ones, and Standard for the rest. The depth is chosen once per pull request and stays the same across its Rounds unless the user changes it.

A repo can add a short `REVIEW.md` at its root saying what Important means there, what to skip, and what to always check.

## Rounds

Rounds 1 and 2 review the whole pull request. Rounds 3 to 5 review only the commits added since the previous Round. In every Round, the Verifier also re-checks each **open Important** (one raised in an earlier Round and not yet confirmed fixed) against the current code, and closes it once the fix is there.

A Round is **clean** when, after its Verify, no Important is open: it found no new Important, and every earlier one is confirmed fixed.

- **Round 1** always leads to Round 2. Its fixes and its "fix" Nits are committed, and Round 2 reviews them.
- **Round 2 to Round 4**, if not clean: the fixes and "fix" Nits are committed, and the next Round reviews them.
- **Round 2 to Round 5**, if clean: its "fix" Nits go into one last commit that no further Round reviews, and the pull request is ready to merge.
- **Round 5**, if not clean: the agent stops and tells the user what kept coming up, since the plan may need discussing.

Once the pull request's last Round is done, each Pre-existing Bug class becomes one GitHub issue labelled `needs-triage`, so it is tracked without blocking the pull request. When a Bug class had more than one instance in a pull request (in one Finding or across Rounds), `retro` turns it into a deterministic check or a `REVIEW.md` line, so later Reviews do not have to catch it again.

## Considered options

- **Cheap Verifiers.** Cheaper, but verifying is a judgement task, and cheap Verifiers checking cheap Finders tend to share their blind spots. A Verifier reads one Finding and the files it cites, so the regular tier costs little extra.
- **Two Verifiers that must both agree on Deep.** One wrong Verifier would drop a real bug. Three with a majority, each with a different stance, gives votes that are more independent than three copies of the same prompt.
- **A separate premium whole-design review.** The Claude Code team's process (blog post "How the Claude Code team does code review", 2026-10-15) has no such reviewer: people keep direction and architecture. Design questions come to the user during grilling, the spec Finder and adversarial angles check ADRs, and Deep covers risky pull requests.
- **Claude Code's cap of 3 Rounds** (after three Rounds their reviewer asks the author to reconsider the approach, per the same post). Their review prompts and project history let most pull requests pass in one Round. We keep two full-PR Rounds and a cap of 5, with the later Rounds limited to new commits.
