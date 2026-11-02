# Finders

Briefs for the Find stage of [`agentic-review`](SKILL.md). Every Finder is a brand-new subagent on the tier given here, and every brief includes:

- The diff command for this Review and, in Rounds 3 to 5, the whole-pull-request diff command too, plus the commit list and, for a fixed point, the untracked new files. When a Round's new commits include a merge from main, add: "The new commits include a merge from main. Review every new commit as the diff command shows it, and for the merge only what it changed in the pull request; the commits that came in from main are not part of this pull request."
- The spec (path or fetched contents), the standards-source files, and `REVIEW.md` if the repo has one.
- The **settled designs** ([SKILL.md step 2](SKILL.md#2-find-the-spec-and-standards-sources)), when there are any, with: "These designs are settled: the user, or an agent within what the user agreed, already decided them. Do not propose an alternative a settled decision rejected. A Finding that the chosen design is imperfect is real only if the text overclaims (it says the design does something it does not) or contradicts itself or the repo, or if the Finding shows the decision breaks what the user agreed (inside a Milestone, the goal, an acceptance criterion or an exclusion); such a Finding is a design Finding."
- The **Finding format** at the end of this file, pasted in full, with: "Report every candidate Finding in this format and nothing else. List every place in the pull request where the Bug class occurs, not only the first, and in Rounds 3 to 5 not only in the new commits. Give each Finding a failure scenario. Report a candidate you only half believe too: put `(unsure)` after its title and say in the Claim what would settle it; the Verifier judges it. Propose a Severity; the Verifier makes the final call. Skip anything tooling already enforces and anything `REVIEW.md` says to skip. If you find nothing, say so."
- The **copy rule**, pasted in full: "Read the branch only through commands that do not touch the working tree: `git -C <path> show`, `diff`, `log` or `rev-parse` against a commit, or a `git archive <head>` copy. To try something out (plant a line, run a check, test a commit), work in your own copy: `git archive <head> | tar -x -C <a new scratch directory>`, or a throwaway `git worktree`. Never run `git checkout` (a branch or `<sha>`), `git switch` (`--detach` too), `stash` or `reset` in the shared tree, because an Implementer is working in it and each of them moves it; leave it on its branch, clean."

## Standards Finder (regular tier)

Paste in the standards-source files and the **smell baseline** below in full (the subagent has no other access to it), plus the **docs index drift** check when the repo has `docs/index.md`, and the **`REVIEW.md` Always check** section below when the repo's `REVIEW.md` has at least one Always check line; without one, drop (d) from the brief.

Brief: "Report (a) every place the diff violates a documented standard: cite the standard (file and rule); (b) any baseline smell you spot: name it and quote the hunk; (c) any docs index drift; (d) every `REVIEW.md` Always check line the diff breaks, reported once under (d) and not again under (a). Documented-standard breaches can be hard; baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Your final message is the report itself, as plain text. Do not end with any messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for."

### Smell baseline

On top of whatever the repo documents, the standards Finder always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### Docs index drift

Only when the repo has `docs/index.md`, load `docs-index` and paste its contract into the standards Finder brief so the Finder uses its listed-doc scope and exceptions. Report as Bug class **docs index drift**, one Finding listing every instance:

- a doc added or renamed in the diff with no line in `docs/index.md`;
- a line in `docs/index.md` whose link points at a file that does not exist at this Review's head.

Propose Nit, unless `REVIEW.md` or an ADR makes the index a rule, then Important.

### `REVIEW.md` Always check

Only when the repo's `REVIEW.md` has at least one Always check line. Use the Bug class and Always-check meaning from `review-record` (load it by name and include that meaning with this brief). The other Finders get `REVIEW.md` too, but this check is the standards Finder's job, so every depth runs it, a Ticket check included.

- Check every Always check line against the whole diff you were given (in Rounds 3 to 5, the whole-pull-request diff, not only the new commits), one line at a time, even when the change looks unrelated to it.
- For each line the diff breaks, report one Finding whose Bug class is the one the line names, listing every instance. Propose its Severity by the meaning of Important like any other Finding.
- After the Findings, list every Always check line with `clear` or the title of its Finding, so the Review shows each line was checked. This list is the one addition to "this format and nothing else".

## Spec Finder (regular tier)

Skipped when there is no spec; the Review says so.

Brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong; (d) anything that contradicts an ADR or the glossary. Quote the spec line, or the ADR or glossary line, as the evidence for each Finding. Your final message is the report itself, as plain text. Do not end with any messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for."

## Adversarial Finders (cheap tier, Standard and Deep)

Two Finders, each on one angle. Pick the 2 angles from the list that fit this change best, two different ones; when nothing stands out, take **bugs and edge cases** plus the best fit. Name the angle in the brief.

Brief: "You are an adversarial reviewer on one angle: <angle>. Assume the change is wrong somewhere on this angle and hunt for it. Open the code around each hunk: unchanged lines inside a function the diff touches are in scope. Follow calls into unchanged code where the angle leads there. Your final message is the report itself, as plain text. Do not end with any messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for."

Angles:

- **Bugs and edge cases**: off-by-one, empty and null inputs, boundaries, error paths, wrong conditions, unhandled return values.
- **Security and privacy**: unescaped or unvalidated user input, injection, missing authorisation, secrets in code or logs, personal data exposed.
- **Contradictions**: the change contradicts an ADR, the glossary, the docs or its own comments and docstrings.
- **Data loss and rollback**: destructive operations, migrations, overwrites, anything that makes a rollback unsafe.
- **Concurrency and ordering**: races, retries, idempotency, order-dependent state.
- **Money, numbers and time**: floats for money, rounding, units, overflow, time zones and dates.
- **Interfaces and compatibility**: a public API, config, file format or CLI changed in a way callers break on.
- **Performance**: N+1 queries, unbounded loops or payloads, work repeated per item.
- **Tests**: changed behaviour with no test, tests that cannot fail, tests that assert the bug.
- **Removed behaviour**: a deleted check, rule or branch. Find where it is enforced now, if anywhere.
- **Cross-file callers**: every caller of a changed function, type or config key, in files the diff does not touch, still gets what it expects.
- **Language pitfalls**: falsy zero or empty string, mutable defaults, integer division, a missing `await`, shadowing, a regex that lost its anchor.
- **Wrappers and proxies**: a call routed through a wrapper, proxy, decorator or middleware that drops, reorders or swallows arguments, options or errors.
- **Altitude**: the change patches a symptom where the cause sits higher up, so other paths to the same cause still fail.

## Security Finder (premium tier, Deep only)

Brief: "Review this change for security and privacy only, in depth. Trace every input an outside party controls from where it enters to where it is used (HTML, SQL, shell, file paths, URLs, logs, other services), and check authentication, authorisation, secrets, personal data, and new dependencies. Cite the source-to-sink path for each Finding. Your final message is the report itself, as plain text. Do not end with any messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for."

Its Findings go through Verify like every other Finding.

## Gap sweep (premium tier, Deep only)

Runs after Verify, as one brand-new Finder. Premium, because spotting what is absent is harder than checking what is there. Give it the shared brief above and the Findings Verify kept.

Brief: "The Findings given are already known; report none of them again. Look only for what the change is missing: moved code that dropped a guard, a flipped default, setup with no matching teardown, a new case that a switch, validator or migration does not handle, a rename that some callers missed. Your final message is the report itself, as plain text. Do not end with any messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for."

Its Findings go through a second Verify ([VERIFY.md](VERIFY.md#gap-sweep)).

## Finding format

```
### <short title>
- Severity (proposed): Important | Nit | Pre-existing
- Bug class: <short noun phrase naming the kind of problem, e.g. "unescaped user input">
- Locations: <every file:line or file:start-end in the pull request where this Bug class occurs, each line counted within that file at this Review's head (as `grep -n` on the file gives it), never a position in the diff output or in a listing of several files>
- Claim: <what is wrong, in one or two sentences>
- Failure scenario: <the inputs or state, then the wrong result; for a cleanup Finding (a smell, or a Nit with no wrong result), its cost instead>
- Evidence: <the quoted code, spec line, standard or ADR rule, or the input that triggers it>
```

Severity: **Important** must be fixed before merge (see the meaning in [SKILL.md](SKILL.md#2-find-the-spec-and-standards-sources) or `REVIEW.md`); **Nit** is real but small and optional; **Pre-existing** is real but not caused by this change.
