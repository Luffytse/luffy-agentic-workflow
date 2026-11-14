# Review rules

## Important

The default meaning of Important in `agentic-review` applies, with one sentence added: a change is also Important when an agent following the text gets a wrong result or stalls.

## Skip

- **wording edge case that needs a new clause**: in skill or doc text, an edge case whose fix adds a clause is a Nit (skip) unless an agent following the text literally would produce a wrong result. When the Ticket asks for a minimal change, weigh the clause's length against that.
- **summary shorter than the rule it summarises**: a glossary entry, index line or README line that gives less detail than the rule's owner text but states nothing different is not a contradiction; one that omits a condition and so gives a different result is.
- **rare compound-failure path**: a path that needs two or more unlikely failures at once, and whose fix needs a new clause, is a Nit.

## Always check

Each line names where it came from and the files it applies to, in the form `(files: ...; from ...)` the review's parser reads. At Release end the coordinator (the user, when none runs) lists the last ~30 merged pull requests that touched a line's files (`gh pr list --state merged --limit 200 --json number,files`, filtered by the line's globs; take fewer if the list is short), reads their Round comments (`gh pr view <n> --json comments`, the ones starting `<!-- code-review kind=round`), and reviews the line for removal if no kept Finding (one left open or fixed, not dropped or dismissed) has a Bug class and `file:line` that the line covers.

- **related text updated when a rule changes** (files: `plugins/*`, `docs/*`, `scripts/*`, `CLAUDE.md`, `AGENTS.md`, `README.md`, `REVIEW.md`, `.claude-plugin/*`, `.agents/*`; from #79, #122, #256): every consumer, record shape, glossary entry, ADR, README, checker message and quoted count or name that uses or describes the changed rule, or the changed layout or packaging, is updated, and parallel sentences in the edited file do not contradict it. Independent rules may differ; a Shared rule changes with its owner and its unmigrated shared copies. When a decision recorded in an ADR or glossary entry replaces a rule still stated elsewhere until a later change lands, the new text says the old rule governs until then, in every place it states the new one.
- **every field and condition a step uses has a source in the text** (files: `plugins/*`, `docs/*`, `CLAUDE.md`; from #79, #209): a completeness check of the text, read against the text, not a prediction of what an agent will do. Every field a step writes has an input in the text that carries it, and every condition a step tests (merged, approved, owned by, closed by) names the command, field or route that reads it, in every parallel recipe in the file; a negative marker alone is not the test of a positive condition.
- **every state a rerun can find has a step in the text** (files: `plugins/*`, `docs/*`, `CLAUDE.md`; from #282, #307, #607, d42ca69): a completeness check of the text, read against the text, not a prediction of what an agent will do. A step that can be stopped before and re-entered re-reads state that may have changed (main's version, whether a pull request merged) and says what a rerun does. A rerun can find a record that it or another agent wrote earlier (a handoff, a request, a claim); the text has a step for each state it can be in (worker running, ended without its result, never started), so no state leaves the request repeated or waiting on a result that will not come. Where two agents write one branch or record, the text has a step for each one's rejected or conflicting write. Each test still holds once a later change has moved the state past it (an equality test on a version fails once a newer version is on main), in the first run and in every resume path. No exit fires at the first of several writes, no state is left that nothing ends, and a thread has one end point in every sentence that states it.
- **skill descriptions do not collide** (files: `plugins/dev-skills/skills/*/SKILL.md`; from #94): when a description or `ask-matt`'s routing changes, no realistic user phrase matches two descriptions, and none contradicts what `ask-matt` says about its skill.
- **plugin text names nothing only this repo has** (files: `plugins/dev-skills/*`; from #179): no path, file, ADR, issue, person, project or merge rule that exists only here, because every project that loads the plugin reads it. `repo-free-skill-text` in `scripts/check-plugin.sh` catches this repo's own names; this line covers the rest.
- **a command that decides a step was run on a real example** (files: `plugins/*`, `docs/*`, `scripts/*`, `CLAUDE.md`; from #307): a `gh`, `git` or `jq` command or regex whose output decides a step (shipped, merged, found) has its output shown on a real example of each outcome from this repo's history (the Finder or Verifier runs it if the pull request does not), because it can parse and still read an often-empty field or match inside another word.

## Review levels

- Standard: plugin skill text, under `plugins/dev-skills/skills/`.
- Quick: `plugins/dev-skills/CHANGELOG.md`, and a change under `docs/` alone that edits no rule and no code (prose, links, typos).
- Standard: a change under `docs/` that edits a rule (the glossary, an ADR, the Boundary record, the release, tracker or label docs) and alters what the rule says, not only its wording.
- None: the `version` lines of `plugins/*/.claude-plugin/plugin.json` and `plugins/*/.codex-plugin/plugin.json`.
- Any other path, and a diff that mixes levels, follows the defaults in `agentic-review` (the higher level wins).
