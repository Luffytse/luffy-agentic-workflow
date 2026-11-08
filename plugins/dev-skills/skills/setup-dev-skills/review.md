# Review rules

## Important

The default meaning of Important in `review-rounds` applies.

## Skip

Nothing yet.

## Always check

Each line has the form `- **<Bug class>** (files: `glob`, `glob`; from <where it came from>): what to look for`, the form the review's parser reads. The bold name is the Bug class; `files:` lists the globs of the files it applies to, and `(files: all)` says it applies to every diff. A line with neither globs nor `all` still applies to every diff, and the brief run warns about it. For example:

- **unchecked null from the API client** (files: `src/**/*.ts`; from #12): a value from `client.get` is used without a null check.
