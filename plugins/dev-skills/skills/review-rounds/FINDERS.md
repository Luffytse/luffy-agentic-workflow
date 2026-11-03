# Finders

Briefs for the Find step of [`review-rounds`](SKILL.md). Each Finder gets only what its section lists, so its brief fits its job.

## Every Finder

Every Finder gets:

- The diff command and the commit list for this Round (for a fixed point, the untracked new files too). In Rounds 2 and 3, add: "These are the pull request's new commits since the last Round. For a merge from main, the diff shows only its conflict resolutions; the commits that came in from main are not part of this pull request."
- The meaning of Important and the Skip list (`REVIEW.md`'s, or the default in [SKILL.md](SKILL.md)).
- The Boundary record, when the project has one.
- The **shared brief**, the **copy rule** and the **Finding format** below, each pasted in full.

Shared brief: "Look first for risk, security, anything that crosses the project's Boundary record, and whether the change carries tests for what it claims: on a code project, changed behaviour with no test that could fail is a Finding. Quote the line each Finding rests on; for code, show a run or a failing test where you can. Report every candidate in the Finding format and nothing else, listing every place its Bug class occurs in the diff, each with a failure scenario. Put `(unsure)` after the title of a candidate you half believe and say in its Claim what would settle it. Propose a Severity; the Verifier decides. Skip anything tooling already enforces and anything the Skip list names. If you find nothing, say so. Your final message is the report itself, as plain text: end with no messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for."

Copy rule: "Read the branch only through commands that leave the working tree alone: `git -C <path> show`, `diff`, `log` or `rev-parse` against a commit. To try something out, work in your own copy: `git archive <head> | tar -x -C <a new scratch directory>`, or a throwaway `git worktree`. Another agent may be working in the shared tree, so leave it on its branch, clean: no `checkout`, `switch`, `stash` or `reset` there."

The standards, spec and later-Round Finders also get the spec, the earlier Findings and the design answers, with: "An earlier Finding that is still open keeps its id: report it again only if this diff adds a new place for it. Raise a dismissed Finding again only if the code at its locations changed. Do not propose an alternative a recorded design answer rejected."

## Standards Finder (regular tier)

Add the standards files, and:

- the `REVIEW.md` Always check lines for the kinds of file this diff touches, with the Always-check meaning from `review-record` (load it by name); with none, drop (c);
- the **smell baseline** below, only when the diff changes code; otherwise drop (b);
- the **docs index drift** check, only when the repo has `docs/dev-skills/index.md`; otherwise drop (d).

Brief: "Report (a) every place the diff breaks a documented standard, citing the file and rule; (b) any baseline smell, named, with the hunk quoted; (c) every Always check line the diff breaks, as one Finding whose Bug class is the one the line names, then list every line given with `clear` or its Finding's title; (d) any docs index drift. A documented standard overrides the baseline."

### Smell baseline

Fowler's code smells (_Refactoring_, ch.3), each a judgement call ("possible Feature Envy"), never a hard violation:

- **Mysterious Name**: a name that hides what it does or holds. → rename it.
- **Duplicated Code**: one logic shape in more than one hunk or file. → extract it.
- **Feature Envy**: a method that uses another object's data more than its own. → move it there.
- **Data Clumps**: the same fields or params travelling together. → bundle them into one type.
- **Primitive Obsession**: a primitive standing in for a domain concept. → give it a type.
- **Repeated Switches**: the same `switch` or `if`-cascade on one type, again. → one map or polymorphism.
- **Shotgun Surgery**: one change forcing scattered edits. → gather what changes together.
- **Divergent Change**: one module edited for unrelated reasons. → split it.
- **Speculative Generality**: hooks or parameters the spec does not need. → delete them.
- **Message Chains**: long `a.b().c().d()` walks. → hide the walk behind one method.
- **Middle Man**: a function that only delegates. → call the target direct.
- **Refused Bequest**: a subclass ignoring most of what it inherits. → use composition.

### Docs index drift

Load `docs-index` and paste its contract into the brief. One Finding, Bug class **docs index drift**, listing every doc the diff adds or renames with no line in `docs/dev-skills/index.md`, and every index line whose link points at a missing file. Propose Nit, unless `REVIEW.md` or a recorded decision makes the index a rule.

## Spec Finder (regular tier)

Skipped when there is no spec.

Brief: "Report (a) what the spec asked for that is missing or partial; (b) behaviour the spec did not ask for; (c) what looks implemented but wrong; (d) anything that contradicts a recorded decision or the glossary. Quote the spec, decision or glossary line for each."

## Adversarial Finder (cheap tier, Standard and Deep)

One Finder on the angle that fits the change best; with nothing standing out, **bugs and edge cases**. It gets only what every Finder gets, with no standards files and no Always check lines.

Brief: "You are an adversarial reviewer on one angle: <angle>. Assume the change is wrong somewhere on this angle and hunt for it. Unchanged lines inside a function the diff touches are in scope, and so are calls into unchanged code where the angle leads."

Angles:

- **Bugs and edge cases**: off-by-one, empty and null inputs, boundaries, error paths, wrong conditions, unhandled return values.
- **What the change is missing**: moved code that dropped a guard, a flipped default, setup with no teardown, a new case a switch, validator or migration does not handle, a rename some callers missed.
- **Security and privacy**: unvalidated input, injection, missing authorisation, secrets in code or logs, personal data exposed.
- **Contradictions**: the change contradicts a decision record, the glossary, the docs or its own comments.
- **Data loss and rollback**: destructive operations, migrations, overwrites, an unsafe rollback.
- **Concurrency and ordering**: races, retries, idempotency, order-dependent state.
- **Money, numbers and time**: floats for money, rounding, units, overflow, time zones.
- **Interfaces and compatibility**: a public API, config, file format or CLI changed so callers break.
- **Performance**: N+1 queries, unbounded loops or payloads, work repeated per item.
- **Tests**: changed behaviour with no test, tests that cannot fail, tests that assert the bug.
- **Removed behaviour**: a deleted check, rule or branch; find where it is enforced now.
- **Cross-file callers**: every caller of a changed function, type or key, in files the diff does not touch.
- **Language pitfalls**: falsy zero, mutable defaults, integer division, a missing `await`, a regex that lost its anchor.
- **Altitude**: a symptom patched where the cause sits higher up.

## Later-Round Finder (Rounds 2 and 3)

One Finder does the standards and spec Finders' work on the new commits: give it both their inputs and both briefs, (a) to (d) of each.

## Finding format

```
### <short title>
- Severity (proposed): Important | Nit | Pre-existing
- Bug class: <short noun phrase naming the kind of problem>
- Locations: <every file:line or file:start-end where it occurs, counted within that file at this Round's head, as `grep -n` gives it>
- Claim: <what is wrong, in one or two sentences>
- Failure scenario: <the inputs or state, then the wrong result; for a cleanup Finding, its cost>
- Evidence: <the quoted line, spec line or rule, and the run or failing test where there is one>
```
