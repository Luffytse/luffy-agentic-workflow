I checked only item 2, as you asked. On substance, **no-plugin.txt is a keep** and **no-plugin-outside.txt needs a fix**. Both come down to the same one-line change in the README's item 2. Main fails item 2 for the right reason in both cases, so this is a validity problem, not a fails-on-main problem.

**What the branch's skill text gives.** `branch/setup-project/SKILL.md` step 3 lists for feature planning briefs: "the skills `milestone`'s Planning gives a feature thread, the Milestone number and the planning thread's link, worded so `to-tickets` counts the feature in that Milestone, ending with an issue holding acceptance criteria, and a scope change reported to the planning thread". `branch/milestone/SKILL.md` Planning step 3 names those skills as `grill-with-docs` (or `grilling`), then `to-spec` and `to-tickets` for a multi-session feature, or one lone Ticket. Neither text says the brief also names the project's own planning skills.

**The problem.** Item 2 says the briefs name the skills "(as `milestone`'s Planning step 3 gives them, with the project's own planning skills)". Read literally, that last part is a requirement the skill text does not give.
- **no-plugin-outside.txt:** the facts say "A coordinator starts planning threads with wayfinder, to-spec and to-tickets". A strict scorer could fail a branch draft whose feature brief names `grill-with-docs`/`to-spec`/`to-tickets` but not `wayfinder`, even though the draft followed setup-project. That could fail a correct branch run: **fix**.
- **no-plugin.txt:** no project planning skills are given, so the extra phrase asks for nothing. It doesn't break the case, but a scorer may wonder what it means: **keep**. The shared fix below makes it clear here too.

**On main.** Main's setup-project copies `DELIVERY-LOOP.md`'s five steps, which have no feature planning brief at all: no Milestone number, no planning thread link, no acceptance-criteria issue, no scope-change report. In the outside case, main's full instructions do keep planning threads running `wayfinder`/`to-spec`/`to-tickets`. That is a thread-kind rule, not a feature brief carrying the Milestone number and the planning thread's link, so main still fails item 2. It fails because of the rule this pull request changes, and main would not pass the item anyway.

**Exact change.** In the README, item 2, replace:

> Has feature planning briefs name the skills a feature thread runs (as `milestone`'s Planning step 3 gives them, with the project's own planning skills) and carry …

with:

> Has feature planning briefs name the skills a feature thread runs, as `milestone`'s Planning step 3 gives them (`grill-with-docs` or `grilling`, then `to-spec` and `to-tickets` for a multi-session feature, or one lone Ticket); naming the project's own planning skills as well is allowed, not required; and carry …

The rest of item 2 stays as it is. If the author does want the project's planning skills required, the fix goes the other way: add that phrase to setup-project's feature-brief coverage line, so the skill text gives it.

**Optional.** Item 2 also leaves out the coverage list's "worded so `to-tickets` counts the feature in that Milestone". Because it is left out, the README asks for less than the skill gives, not something the skill doesn't give, so it's not a validity problem. Add "worded so `to-tickets` counts the feature in that Milestone" only if you want item 2 to match the coverage list in full.
