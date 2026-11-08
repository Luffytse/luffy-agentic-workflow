# Review rules

## Important

The default meaning of Important in `review-rounds` applies.

## Skip

Nothing yet.

## Always check

Each line has the form `- **<Bug class>** (files: `glob`, `glob`; from <where it came from>): what to look for`, the form the review's parser reads. The bold name is the Bug class; `files:` lists the globs of the files it applies to, and `(files: all)` says it applies to every diff. A line with neither globs nor `all` still applies to every diff, and the brief run warns about it. The line below is an example to replace with your own; it is quoted so it is not a live rule:

> - **unchecked null from the API client** (files: `src/*.ts`; from <origin>): a value from `client.get` is used without a null check.
