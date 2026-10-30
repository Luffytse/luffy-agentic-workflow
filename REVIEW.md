# Review rules

## Important

The default meaning of Important in `agentic-review` applies.

## Skip

Nothing yet.

## Always check

- **related text not updated when a shared rule changes**: when a change edits a shared rule (the Finding format, a diff command, a stage's output or a record's shape), check every skill, record shape, glossary entry and ADR that uses or describes it.
- **a step asks for data its input does not carry**: every field a step writes (an issue body, a report line, a comment row) comes from an output or record that carries it.
