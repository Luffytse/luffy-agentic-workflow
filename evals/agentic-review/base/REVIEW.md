# Review rules

## Important

The default meaning of Important applies.

## Skip

Nothing yet.

## Always check

Each line names the files it applies to.

- **public function without a docstring** (files: `splitter/*.py`): every public function in `splitter/` (a name without a leading underscore) has a docstring saying what it returns or does; the rest of the package reads its contract from them.
- **unquoted variable** (files: `*.sh`): every variable in a shell script is quoted, so a path with a space stays one argument.
