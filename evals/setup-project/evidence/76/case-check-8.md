**Verdict: keep** for both `no-plugin.txt` and `no-plugin-outside.txt`. Item 2 now matches the skill text.

**Item 2 against the branch's skill text.** The coverage list in `branch/setup-project/SKILL.md:47` says the feature planning briefs name "the skills a feature thread runs for each kind of feature (the project's own, or `milestone`'s Planning's where it names none)". Item 2 now asks for `milestone`'s Planning step 3 skills (`grill-with-docs` or `grilling`, then `to-spec` and `to-tickets`, or one lone Ticket) "or the project's own planning skills where the case gives them (the coverage list prefers those)". The two now say the same thing: the project's own skills win, and `milestone`'s apply where the project names none. Step 3 is quoted correctly (`branch/milestone/SKILL.md:29`). The other parts of item 2 also come from line 47 and from step 3's last sentences:
- the Milestone number and the planning thread's link;
- ending with an issue that holds acceptance criteria;
- reporting a scope change to the planning thread.

**How each case uses it:**
- **`no-plugin.txt`** names no planning skills of the project's own, so `milestone`'s step 3 skills apply. The item gives exactly that.
- **`no-plugin-outside.txt`** says planning threads run `wayfinder`, `to-spec` and `to-tickets`, so those win for a multi-session feature. The project names nothing for a lone Ticket, so `milestone`'s "one lone Ticket" applies there. Because the item says "or", a draft that mixes the two sources this way passes, which is what the skill text gives.

**One soft spot, not a validity problem.** "Prefers" and the "or" are a little weaker than "win". Read loosely, a scorer could pass a no-plugin-outside draft that swaps the project's `wayfinder` for `grilling`. Item 15 still catches that draft, because it requires keeping the project's thread kinds and their skills. So the item cannot pass a draft the skill text would not give. If you want it tighter, change "(the coverage list prefers those)" to "(those win where given)". This is optional and does not make it a fix.

**Fails on main for the right reason.** Main's `setup-project` has no coverage list and no assembled cycle for a coordinator that cannot load the plugin. Its only planning text is the general "Skill per thread kind" line (`main/setup-project/SKILL.md:29`). So main's text does not give the feature planning brief content, and main does not pass item 2 anyway.

**Needed.** Neither older case covers feature planning briefs, so item 2 is still needed.
