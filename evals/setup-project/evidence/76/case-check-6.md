**Verdict on item 2: keep for both `no-plugin.txt` and `no-plugin-outside.txt`.** No validity problem remains. Main fails the item because of the rule this pull request changes.

**Valid: the branch's text gives item 2.**
- The branch's `setup-project` coverage list has its own line for feature planning briefs: "the skills `milestone`'s Planning gives a feature thread, the Milestone number and the planning thread's link, worded so `to-tickets` counts the feature in that Milestone, ending with an issue holding acceptance criteria, and a scope change reported to the planning thread".
- The skills in item 2 match `milestone` Planning step 3 word for word: "`grill-with-docs` (or `grilling`), then `to-spec` and `to-tickets` for a multi-session feature, or one lone Ticket".
- "Report a scope change to the planning thread" is a fair short form of step 3's "reports any change to the goal, acceptance, exclusions, order or Release split to the planning thread".
- The ending matches too. Step 3 is done when each feature "has its own issue holding its acceptance criteria", which is item 2's "end with an issue holding acceptance criteria".
- Item 2 does not score the clause "worded so `to-tickets` counts the feature in that Milestone". Leaving it out only makes the check looser; it does not expect anything the skill doesn't give. The Milestone number in the brief is also what `to-tickets` reads ("the caller says it is planning a feature of a named Milestone").
- In `no-plugin-outside.txt`, the project's own planning skills (`wayfinder`, `to-spec`, `to-tickets`) are "allowed, not required". So a draft that also names them is not failed wrongly, and the skills from `milestone` must still be there.

**Fails on main for the right reason.**
- Main's `setup-project` tells the drafter to copy the five steps of `team-lead/DELIVERY-LOOP.md` word for word. None of those steps covers feature planning briefs. The loop's general brief line ("the skill, the issue link, the Milestone issue link and the Model tier") names no planning skills and no planning-thread link. It also has no ending with an issue holding acceptance criteria and no scope-change report.
- The README already counts item 2 among main's expected failures.
- In `no-plugin-outside.txt`, main could pick up `wayfinder`, `to-spec` and `to-tickets` from the project facts. Even then it lacks `grill-with-docs` or `grilling`, the planning thread's link, the acceptance-criteria ending and the scope-change report, so it still fails.

**Needed.** No other item, and neither older prompt, checks feature planning briefs.

Item 2 is not an expected result the branch's text fails to give, and main's text does not pass it.
