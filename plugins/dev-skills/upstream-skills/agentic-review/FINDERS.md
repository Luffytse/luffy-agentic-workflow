# Finders

Briefs for the Find stage of [`agentic-review`](SKILL.md). Every Finder is a brand-new subagent on the tier given here, and every brief includes:

- The diff command for this Review and, in Rounds 3 to 5, the whole-pull-request diff command too, plus the commit list.
- The spec (path or fetched contents), the standards-source files, and `REVIEW.md` if the repo has one.
- The **Finding format** at the end of this file, pasted in full, with: "Report every candidate Finding in this format and nothing else. List every place in the pull request where the Bug class occurs, not only the first, and in Rounds 3 to 5 not only in the new commits. Propose a Severity; the Verifier makes the final call. Skip anything tooling already enforces and anything `REVIEW.md` says to skip. If you find nothing, say so."

## Standards Finder (regular tier)

Paste in the standards-source files and the **smell baseline** below in full (the subagent has no other access to it), plus the **docs index drift** check when the repo has `docs/index.md`, and the **`REVIEW.md` Always check** section below when the repo's `REVIEW.md` has at least one Always check line; without one, drop (d) from the brief.

Brief: "Report (a) every place the diff violates a documented standard: cite the standard (file and rule); (b) any baseline smell you spot: name it and quote the hunk; (c) any docs index drift; (d) every `REVIEW.md` Always check line the diff breaks, reported once under (d) and not again under (a). Documented-standard breaches can be hard; baseline smells are always judgement calls, and a documented repo standard overrides the baseline."

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

Only when the repo has `docs/index.md`. A doc is anything the index is meant to list (the list in [`domain-modeling/DOCS-INDEX.md`](../domain-modeling/DOCS-INDEX.md#what-is-listed)): glossary pages, ADRs, `docs/agents/` files, `.out-of-scope/` notes, `REVIEW.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, README files and research notes; never `CLAUDE.md` or `AGENTS.md` files, `SKILL.md` files, code, or test fixtures. Report as Bug class **docs index drift**, one Finding listing every instance:

- a doc added or renamed in the diff with no line in `docs/index.md`;
- a line in `docs/index.md` whose link points at a file that does not exist at this Review's head.

Propose Nit, unless `REVIEW.md` or an ADR makes the index a rule, then Important.

### `REVIEW.md` Always check

Only when the repo's `REVIEW.md` has at least one Always check line. Each line there names a Bug class that earlier Reviews had to catch more than once, and what to look for (`retro` adds them: [BUG-CLASSES.md](../retro/BUG-CLASSES.md)). The other Finders get `REVIEW.md` too, but this check is the standards Finder's job, so every depth runs it, a Ticket check included.

- Check every Always check line against the whole diff you were given (in Rounds 3 to 5, the whole-pull-request diff, not only the new commits), one line at a time, even when the change looks unrelated to it.
- For each line the diff breaks, report one Finding whose Bug class is the one the line names, listing every instance. Propose its Severity by the meaning of Important like any other Finding.
- After the Findings, list every Always check line with `clear` or the title of its Finding, so the Review shows each line was checked. This list is the one addition to "this format and nothing else".

## Spec Finder (regular tier)

Skipped when there is no spec; the Review says so.

Brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong; (d) anything that contradicts an ADR or the glossary. Quote the spec line, or the ADR or glossary line, as the evidence for each Finding."

## Adversarial Finders (cheap tier, Standard and Deep)

Two Finders, each on one angle. Pick the 2 angles from the list that fit this change best, two different ones; when nothing stands out, take **bugs and edge cases** plus the best fit. Name the angle in the brief.

Brief: "You are an adversarial reviewer on one angle: <angle>. Assume the change is wrong somewhere on this angle and hunt for it. Open the code around each hunk and follow calls into unchanged code where the angle leads there. Cite the input, path or sequence of events that makes each problem happen."

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

## Security Finder (premium tier, Deep only)

Brief: "Review this change for security and privacy only, in depth. Trace every input an outside party controls from where it enters to where it is used (HTML, SQL, shell, file paths, URLs, logs, other services), and check authentication, authorisation, secrets, personal data, and new dependencies. Cite the source-to-sink path for each Finding."

Its Findings go through Verify like every other Finding.

## Finding format

```
### <short title>
- Severity (proposed): Important | Nit | Pre-existing
- Bug class: <short noun phrase naming the kind of problem, e.g. "unescaped user input">
- Locations: <every file:line or file:start-end in the pull request where this Bug class occurs>
- Claim: <what is wrong and what happens because of it, in one or two sentences>
- Evidence: <the quoted code, spec line, standard or ADR rule, or the input that triggers it>
```

Severity: **Important** must be fixed before merge (see the meaning in [SKILL.md](SKILL.md#2-find-the-spec-and-standards-sources) or `REVIEW.md`); **Nit** is real but small and optional; **Pre-existing** is real but not caused by this change.
