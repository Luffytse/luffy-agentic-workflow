**Scoring: `no-plugin-behind.txt` against "Plugin behind main"**

- **Releases step:** FAIL. The draft keeps the older text, with separate plan and cut triggers keyed on a "current Release". Step 2 plans a Release "With no current Release (an open release issue naming this Milestone, whose label an issue carries)…". Step 4 cuts it "When every issue carrying the current Release's label is closed…". It is not `main-skills/`'s single trigger with `release` deciding whether to cut or plan.
- **Stamp:** FAIL. The draft text has no stamp. `4f2c9e1` appears only in the note above the draft ("its last change to `team-lead` or `milestone` is commit `4f2c9e1`"), as a fact about main, not stamped into the instructions. There is nothing to quote from the draft. The README fails a draft with no stamp.
- **Delivery steps match the stamp:** FAIL. Older text is acceptable only with a non-`4f2c9e1` stamp. This draft has no stamp at all. The user was told the plugin is behind (version gap, changed Release rule, advice to update and re-draft), but that doesn't make up for the missing stamp.
- **Item 14 (coordinator doesn't run `milestone`, `team-lead` or `release` itself):** PASS. The draft says "Start a thread for each step below that names a skill, and never do that step yourself". Each step starts a thread that runs the skill.
- **Item 16 (no current-work state; no approval, save or handover claimed):** PASS. There are no issue numbers or work state in the draft. The reply ends "Nothing has been written or sent" and asks for approval.

Overall: FAIL (the Releases step keeps the older separate plan and cut triggers keyed on a "current Release", and the draft has no stamp; `4f2c9e1` appears only in the note outside the draft)
