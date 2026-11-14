# Splitting the glossary

Read this only when a split happens: you are adding a term to a single-context repo whose `docs/dev-skills/glossary.md` holds the terms and is over about 10 KB (check with `wc -c docs/dev-skills/glossary.md`; do not split before then).

A repo starts with one glossary, `docs/dev-skills/glossary.md`. The split makes one page per Area at `docs/dev-skills/glossary/<area>.md` and turns `docs/dev-skills/glossary.md` into the map listing the pages. The entry point keeps its path, so skills that read it find the pages from it; only its content changes, from terms to the map. A page uses the structure in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md), with the Area as its title.

1. Group the terms by Area (the same Areas the docs index uses).
2. `git mv docs/dev-skills/glossary.md` to the first Area's page so history follows, then move the other groups into their own pages.
3. Write a new `docs/dev-skills/glossary.md` as the map, one line per Area page (map format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)).
4. Change the glossary's line in the docs index to say it is now the map, add a line for each Area page, and fix any other doc that links a term's old place (`docs-index` has the format, including creation when absent).

If `docs/dev-skills/glossary.md` is already a map (split per Area, or a multi-context layout), add the term to the page the map points to for its Area or context; never put terms back into the map or split again just because a map exists. A page that grows past about 10 KB splits again by sub-area, and the map gets the new page.
