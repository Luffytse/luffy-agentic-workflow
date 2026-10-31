# Review rules

## Important

The default meaning of Important in `agentic-review` applies.

## Skip

Nothing yet.

## Always check

- **public function without a docstring**: every public function in `splitter/` (a name without a leading underscore) has a docstring saying what it returns or does; the rest of the package reads its contract from them.
