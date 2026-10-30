# Review rules

## Important

The default meaning of Important in `agentic-review` applies.

## Skip

Nothing yet.

## Always check

- **related text not updated when a shared rule changes**: when a change edits a shared rule (the Finding format, a diff command, a stage's output or a record's shape), check every skill, record shape, glossary entry and ADR that uses or describes it, and its parallel sentences in the same file, and the counts, versions and numbers that `PATCHES.md` quotes about the change.
- **a step asks for data its input does not carry**: every field a step writes (an issue body, a report line, a comment row) comes from an output or record that carries it.
- **skill description collides with another skill or with the router's routing**: when a change edits a skill's description or `ask-matt`'s routing, check the description's "Use when" branches against every other `plugins/dev-skills/*/*/SKILL.md` description and against `ask-matt/SKILL.md`; no realistic user phrase may match two descriptions (two claiming the same trigger) and none may contradict what `ask-matt` says about that skill.
- **shared record written by more than one thread**: when a skill has more than one thread or agent write the same issue body, file or record, check that one writer owns it and the others only append (comments, new files), or that the text gives a mechanism that stops a stale write (a lock, a version check, a single merge step), not only a re-read; a "re-read before editing" rule does not stop a write from a stale copy dropping another thread's lines.
- **results entry out of date with its own PR**: when a change adds or edits an eval `RESULTS.md` entry, check that every number, SHA, Round and "not exercised" claim in it agrees with the rest of the entry and with the repo as of the entry's own commit and the pull request's final state; values the entry labels as its base are not stale.
- **skill text that only fits this repo**: when a change edits anything under `plugins/dev-skills/` that agents load (skills, their reference files, seeds and templates), check that it names no path, file, ADR, issue, person, project or rule that exists only in this repo (for example `PATCHES.md`, `check-plugin.sh`, an ADR number, or a merge rule only this repo has), because every project that loads the plugin reads that text. Such a rule goes in this repo's `CLAUDE.md` or `REVIEW.md`, and the skill gives only the general case. The check `repo-free-skill-text` in `check-plugin.sh` catches this repo's ADR numbers and "Upstream"; this line covers the rest.
