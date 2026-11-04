# Review brief script tests

`test_review_briefs.py` tests `plugins/dev-skills/skills/review-rounds/review_briefs.py` as a command. Each test builds a scratch git repo with a planted change, writes the spec, standards list, earlier Findings and design answers to files, runs `review_briefs.py round1` and reads the briefs back. No agent runs.

Run: `python3 evals/review-briefs/test_review_briefs.py` (Python 3 and git only). Run it after changing the script or the brief files it cuts from (`FINDERS.md`, `DEEP.md`, `SKILL.md` of `review-rounds`, `review-record`, `docs-index`).

A test checks what a brief holds against the skill files read the same way (a section present or absent, an Always check line included or left out, the Finders the table names for each level), never a sentence of a skill's wording, so rewording a skill does not fail it. Cases: who runs at each level, with and without a spec; each Finder's sections and the ones it must not get; Always check lines by kind of file; the smell baseline only for code; the docs index check only with an index; defaults without `REVIEW.md`, a Boundary record or an index; the angle by name and an unknown angle; a missing section stopping with exit 3 and its name; usage errors (exit 2); an output directory inside the work tree refused; only `git` called; nothing written outside the output directory.
