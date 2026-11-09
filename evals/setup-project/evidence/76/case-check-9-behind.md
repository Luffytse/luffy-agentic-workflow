**Verdict: keep.** I read every file in the run folder: CASE-CHECK.md, the case README and all five prompts, and every file under branch/ and main/. All three questions pass.

**1. Valid: yes.**
- **Prompt:** It is `no-plugin.txt` word for word except the last fact. That fact gives the plugin as 2.3.0 with `team-lead` and `milestone` under `skills/`, main as 2.4.0 under `main-skills/` ("read from the remote"), and `4f2c9e1` as main's last commit to those two skills. The only new variable is the plugin being behind main.
- **Fixture:** `skills/team-lead` is main's copy, and its step 2 has the separate plan and cut triggers keyed on "current Release", as the README says. `main-skills/team-lead` is the branch's copy, with the single trigger: "when none runs, no open, unparked issue carries the label of an open release issue, and either…". `release` is identical on both sides, and its "Find where you are" (line 20) exists. So the branch's brief line handing cut or plan to `release` is backed by text the run can read.
- **Expected result:** The branch's `setup-project` (line 44) says to read `team-lead` and `milestone` "from that main" when the plugin is behind, "so the text matches the stamp below". Its stamp item (line 58) gives main's last commit. That produces exactly the README's first pass path: `main-skills/`'s Releases step stamped `4f2c9e1`.
- The milestone files differ between the two sides only in their pointers to DELIVERY-LOOP.md. So scoring only the Releases step plus the stamp is the right test.
- Items 14 and 16 are rightly carried over. Item 14 is never telling the coordinator to run `milestone`, `team-lead` or `release` itself; item 16 is no current-work state and no approval, save or handover claim.

**2. Fails on main for the right reason: yes.**
- Main's `setup-project` copies "The loop" word for word from `../team-lead/DELIVERY-LOOP.md`, which resolves to `skills/team-lead`. Only the older copy has that file; `main-skills/team-lead` does not. Main's text also says "never writing your own version". So the baseline draft gets the older plan and cut triggers.
- Main's skill has no stamp rule. Its draft therefore either has no stamp or copies `4f2c9e1` from the prompt onto the older text, and the pass rule fails both.
- Both failures come from rules this pull request adds: reading from main when the plugin is behind, and the source stamp. Nothing in the fixture causes them.

**3. Needed: yes.** `no-plugin.txt` and `no-plugin-outside.txt` both say the plugin "is at main's version". No other case tests the plugin being behind main, or whether the stamp matches the text it was read from.

**Two optional notes (no change required):**
- The second pass path ("keeps the older text and its stamp is not `4f2c9e1`, with the user told") accepts a result the branch text doesn't directly give, since that text says to read from main. It can only come up if the model can't read `main-skills/`, and that is always provided here. You could narrow "with the user told" to: "with the user told that the text is the plugin's older copy and that it doesn't match main's stamp."
- The baseline run should put main's `setup-project` and the other skills under `skills/`, so that main's `../team-lead/DELIVERY-LOOP.md` link resolves to the older copy. The README's "run like the no-plugin cases" already implies this layout.
