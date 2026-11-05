# `dev-skills` moved to its own public repo with a rewritten history

On 2026-11-05 `dev-skills` moved out of the private repo `Luffytse/luffy-dev-skills` into a new repo, `Luffytse/luffy-agentic-workflow`, which is meant to be public. The new repo holds `dev-skills` alone, its marketplace is named `luffy-agentic-workflow`, and its history is the old history rewritten. The old repo stays as a private archive. Making the old repo public was rejected.

## Why

`dev-skills` is used in all of the user's projects and reached 1.0.0, so others can use it, read it and report bugs only if it is public. The old repo could not simply be made public:

- **A private product's plugin is in the first commits.** `dai-portal-data` (a database cookbook for a private product) is in the root commits. GitHub keeps a hidden ref for every pull request, pointing at its commits, so rewriting the branches and deleting the folder would still leave it readable through those refs. Only a new repo has no such refs.
- **The history carried personal traces:** personal email addresses in commits and files, about 300 session links in commit messages and issue text, and local home-folder paths.
- **GitHub cannot transfer issues from a private repo to a public one.** The old issues, Specs and pull requests could not move along; they stay in the archive.

## Decisions

- **A new repo, not a public old one.** The old repo is archived private and stays the record of the issues and pull requests it holds.
- **A rewritten history, not a fresh start.** `scripts/rewrite-public-history.py` rewrites a full clone: it removes the `dai-portal-data` folder from every commit (commits left empty are dropped), replaces author and committer emails with the GitHub no-reply address, deletes session trailers and links, and replaces home paths and private names with neutral ones. Authors' names stay. `scripts/check-public-history.py` walks every commit of the result and fails naming the commit, so the rewritten history is checked before it is pushed, and again before the repo goes public.
- **Renames.** The marketplace is `luffy-agentic-workflow` (it was `luffy-dev`), so the plugin id is `dev-skills@luffy-agentic-workflow`. The repo checker keeps the old names on its repo-only names list, so skill text names none of them.
- **Numbers keep their archive meaning.** The new repo's issues start again at 1 (the moved issues first). Bare issue and pull request numbers in text written before the move on 2026-11-05 (ADRs 0001 to 0013, changelog entries before the move entry, eval results and evidence, and the issues moved from the archive, which link their original) refer to the private archive `Luffytse/luffy-dev-skills`; from the move on, a bare number means this repo's issue, and a reference to an archive issue is written in full as `Luffytse/luffy-dev-skills#<n>`. The commit IDs recorded for past Releases are the archive's; the rewrite changed every ID, so they do not resolve here.
- **Eval results and evidence stay as history.** They record runs made against the old name and are not edited. Eval instructions that name the live install source are updated.
- **License.** The repo carries an MIT `LICENSE` for our own work at the root, beside `plugins/dev-skills/LICENSE-mattpocock-skills`, the notice for the skills that began as Matt Pocock's.
- **No version bump.** No file under `plugins/dev-skills/skills/` changed, so the move bumps nothing (ADR 0008).

## Consequences

- Install, update and local-development lines in the READMEs, the issue tracker doc and the settings that turn off the installed copy name the new repo and marketplace. A project that installed `dev-skills@luffy-dev` must add the new marketplace and install `dev-skills@luffy-agentic-workflow`.
- `dai-portal-data` is no longer in this repo's catalogs, docs or checker; it lives on only in the private archive.
- The rewrite and check scripts stay in the repo as the record of how the history was made.
- Reading an old issue number needs the archive; the docs index and changelog say so.
