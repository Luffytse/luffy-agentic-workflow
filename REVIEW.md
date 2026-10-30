# Review rules

## Important

The default meaning of Important in `agentic-review` applies.

## Skip

Nothing yet.

## Always check

- **related text not updated when a shared rule changes**: when a change edits a shared rule (the Finding format, a diff command, a stage's output or a record's shape), check every skill, record shape, glossary entry and ADR that uses or describes it.
- **a step asks for data its input does not carry**: every field a step writes (an issue body, a report line, a comment row) comes from an output or record that carries it.
- **skill description collides with another skill or with the router's routing**: when a change edits a skill's description or `ask-matt`'s routing, check the description's "Use when" branches against every other `plugins/dev-skills/*/*/SKILL.md` description and against `ask-matt/SKILL.md`; no realistic user phrase may match two descriptions (two claiming the same trigger) and none may contradict what `ask-matt` says about that skill.
- **shared record written by more than one thread**: when a skill has more than one thread or agent write the same issue body, file or record, check that one writer owns it and the others only append (comments, new files), or that the text gives a mechanism that stops a stale write (a lock, a version check, a single merge step), not only a re-read; a "re-read before editing" rule does not stop a write from a stale copy dropping another thread's lines.
