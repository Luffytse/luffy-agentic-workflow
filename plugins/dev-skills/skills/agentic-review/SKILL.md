---
name: agentic-review
description: "Review a pull request, or the changes since a fixed point (commit, branch, tag, or merge-base). Round 0 sizes the review from the changed files: at level None the project's checks are the whole review; at Quick, Standard or Deep, review-rounds runs Finders, a Verifier and at most 3 Rounds. Use when the user wants to review a PR, a branch or work-in-progress changes, run a ticket check, or asks to \"review since X\"."
---

**Round 0** sizes the review before any agent starts. You run it yourself, in the top-level session, with no subagent. It picks a **level** (None, Quick, Standard or Deep), records it, and hands over to `review-rounds` when a Round will run.

## 1. Pin the diff

- **Pull request:** `git diff <base>...HEAD` (three-dot, against the merge-base), `git diff --stat <base>...HEAD` and `git log <base>..HEAD --oneline`.
- **Ticket check:** the same, with the Ticket branch as `HEAD` and the Spec branch as `<base>`.
- **Fixed point** (no pull request: "review since X"): whatever the user named (a SHA, branch, tag, `main`, `HEAD~5`); ask if they named none. `git diff --merge-base <fixed-point>` (the working tree counts), `git diff --stat --merge-base <fixed-point>`, every untracked new file from `git ls-files --others --exclude-standard`, read whole, and `git log <fixed-point>..HEAD --oneline`.

Record `git rev-parse HEAD` as the head. Confirm every ref resolves and the diff is not empty, so a bad ref fails here.

**Continuing.** Read the pull request's comments first. One that already has a Round 1 or later comment is past Round 0: load `review-rounds` by name and continue as its "Resuming" section says, at the level of the latest Round comment.

## 2. Read what sizes it

Read the changed files' hunks, the `--stat` and, when the repo has them, the Boundary record (`docs/dev-skills/boundaries.md`) and `REVIEW.md` at the repo root. A "Review levels" section in `REVIEW.md` names the project's own paths per level, and it overrides the defaults below.

## 3. Pick the level

Defaults, read from the top, first match wins:

- **Deep:** the change touches what the Boundary record or `REVIEW.md` marks risky (security, money, deleting data, migrations).
- **None:** every changed line is a version field, a changelog entry, a lock file or generated output.
- **Quick:** every change is text that leaves what each rule or line of code does as it was: a typo, wording, a link, a comment.
- **Standard:** everything else, a change to what a rule or code does included.

When two levels both seem to fit, take the higher one. A level the user or the caller names wins. A Ticket check is always Quick. Write the reason as one line naming the files that decided it.

## 4. Record and hand over

- **None:** run the project's automated checks; they must pass. On a pull request, post this one line as the whole review comment: `<!-- code-review kind=round round=0 level=None head=<full sha> --> Code review: Round 0, level None (<reason>). The project's checks are the review.` Report the level and the checks' result. Load nothing more.
- **Quick, Standard or Deep:** load `review-rounds` by name and run Round 1 at this level. The level and reason go on the Round 1 comment's `Level:` line.
- **Fixed point:** run Round 0, then Round 1 only, and report it to the user. No comment is posted.
