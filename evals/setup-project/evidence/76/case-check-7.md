**Verdict: no-plugin.txt keep, no-plugin-outside.txt fix (one line in item 2), older-prompts expectation keep, blind run keep.** The only real problem is how the new wording in item 2 handles the project's own planning skills.

**`no-plugin.txt` — keep.**
- **Valid:** the new clause in item 2 changes nothing here, because this prompt names no planning skills of the project's own. The item stays tied to `milestone`'s Planning step 3.
- **Item 3:** "planned with the user first, then joins through a thread running `milestone`" is what `milestone`'s "Adding a feature mid-Milestone" step 1 says ("Plan it with the user first, as planning step 3 says"). It also fits the coverage list ("planned first, then added as `milestone` says") and its "starts a thread for each step that needs a skill" rule.
- **Release and triage folders:** these make item 10 checkable. `release` names premium for its thread. `triage` names no tier, so the item's fallback (`model-tiers`' "Use for" column, or named to the user as unfilled) applies. Item 5's ranking clause is `team-lead`'s Releases rule as written.
- **Fails on main for the right reason:** main's delivery loop has no feature planning briefs and no mid-Milestone step, so items 2 and 3 still fail because of the rule this pull request changes.
- **Needed:** yes.

**`no-plugin-outside.txt` — fix item 2.**
- **Problem:** item 2 now reads "from `milestone`'s Planning step 3 (…) **or** from the project's own planning skills where the case gives them". `setup-project`'s coverage list says "the skills a feature thread runs for each kind of feature, as `milestone`'s Planning gives them, **beside** any the project adds". That is additive. With "or", a draft that lists only wayfinder, to-spec and to-tickets and drops `grill-with-docs`/`grilling` would pass, although the skill text doesn't give that result.
- **Exact change to README item 2:** replace
  `from \`milestone\`'s Planning step 3 (\`grill-with-docs\` or \`grilling\`, then \`to-spec\` and \`to-tickets\` for a multi-session feature, or one lone Ticket) or from the project's own planning skills where the case gives them,`
  with
  `from \`milestone\`'s Planning step 3 (\`grill-with-docs\` or \`grilling\`, then \`to-spec\` and \`to-tickets\` for a multi-session feature, or one lone Ticket), with the project's own planning skills beside them where the case gives them,`
- **Fails on main:** yes, for the right reason. Main's outside draft keeps "planning threads with wayfinder, to-spec and to-tickets", but it has no Milestone number, no planning-thread link, no ending issue with acceptance criteria and no scope-change report. So item 2 still fails on main.
- **Needed:** yes.
- **Rest of the case:** items 3 and 10 and the two added folders are fine, for the same reasons as above.

**Older-prompts expectation (`milestone-rerun.txt`, `no-milestone.txt`) — keep.** None of this round's changes touch it. Those runs still get only `milestone` alongside `setup-project`, and the branch's "add none of this" rule for a coordinator that can load the skills gives this expectation. Main passes it too, so it stays a regression guard as the README records.

**Blind run — keep.** "The project's own planning skills count where the case gives them" is a scoring allowance for which skills the session uses. Once item 2 requires the draft to carry both sets, a session that picks the project's planning skills is following both its draft and the coverage list's "beside". No change is needed beyond item 2's fix.

**README pass items the branch's skill text doesn't give:** only item 2's "or", fixed above.

**Items main's text would pass anyway:** none beyond what the README already states (4, 14, 15, 16, and possibly 11).
