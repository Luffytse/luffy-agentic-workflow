I'd mark all four cases **fix**. The rule change itself is tested correctly: main copies the five steps of `DELIVERY-LOOP.md`, so it fails items 1, 2, 5, 6, 7, 9, 12 and 13 because of the rule this pull request changes, not because of the fixtures. The fixes are smaller problems in the wording and fixtures. I read every file under the folder (including the `openai.yaml` files; `snapshot.py` is the same on both sides) and nothing outside it.

## Verdicts

| Case | Valid | Fails on main for the right reason | Needed | Verdict |
|---|---|---|---|---|
| `no-plugin.txt` | Yes, after README fixes C and D | Yes for 1–3, 5–10, 12, 13. Item 11 can pass on main because of a wording hint in the prompt | Yes (inside-Milestone path) | **fix** (A, C, D, E) |
| `no-plugin-outside.txt` | Mostly. The project has no Boundary record, so the `milestone` planning it expects stops at `milestone`'s planning step 1 | Same as above | Yes (outside path, and the blind run uses it) | **fix** (A, B, C, D, E) |
| Older-prompts expectation | Yes, apart from one ambiguous phrase | Main passes too, as the README says. It is a regression guard, so this question is waived | Yes. The older pass lists only partly exclude the new cycle | **fix** (F), then keep as a regression guard |
| Blind run | Partly. One scenario has no step the branch's skill text puts in the draft, and the scoring has gaps | The baseline should fail at scenario 1, but no expected baseline outcome is stated | Yes. It checks that the draft can be used on its own, which coverage scoring does not | **fix** (G) |

## Exact changes

**A. Both new prompts, line 12.** Replace `- CLAUDE.md, which the coordinator cannot read, says:` with `- CLAUDE.md says:`.
- The phrase "which the coordinator cannot read" is a hint that gives main its own reason to copy the merge-time steps into the draft, so main can pass item 11.
- The branch text needs no hint: it copies the coordinator-facing merge-time steps of `CLAUDE.md` or `AGENTS.md` in full anyway.
- In README line 22, change "(quoted, since the coordinator cannot read them)" to "(quoted, since the run has no repo)".

**B. `no-plugin-outside.txt`, line 5.**
- Change it to: `- docs/dev-skills/index.md, CLAUDE.md and docs/dev-skills/boundaries.md exist.`
- Add the fact: `- Boundary record: membership label milestone-<n>; it names no check-in interval.`
- Why: without a Boundary record, `milestone` planning step 1 tells the user to run `setup-dev-skills` and stops. Item 1 and the blind run's first scenario would then test a missing file instead of the rule.

**C. Item 12.** Change it to: "Gives, in the draft, the meaning of parked, Order, order rule and report re-entry; a pointer to a skill or a doc the coordinator cannot read does not count." The current "or says how the coordinator gets it" is looser than the skill text ("with its meaning").

**D. Item 5.** After "carries an open release issue's label," insert: "and either a release issue naming this Milestone is open or a planned feature is open, not parked, carries no release label and is unblocked (or blocked only by open issues `release` ranks ahead of it),". This is the third condition of `team-lead`'s Releases rule. Without it, a draft that starts a Release thread whenever none is running would still pass.

**E. README line 43.** Replace it with: "Main's skill copies `DELIVERY-LOOP.md`'s five steps, so it is expected to fail items 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12 and 13. It passes 4 (the loop's step 1), 14, 15 and 16."
- Also on line 5, "then both cases against the candidate" should read "both older cases", since there are now four prompts.

**F. Older-prompts guard.** Replace "no tier map the user did not give" with: "no tier map naming models where the user gave none (in `no-milestone.txt`, a pointer to `model-tiers`' defaults is not a map)".
- Why: `no-milestone.txt` says "use model-tiers defaults" but names no harness, so either source might or might not write a model map.
- `RESULTS.md` and the `**Eval:**` line must name this case as a regression guard (CASE-CHECK.md). Both are outside this folder, so I could not check them.

**G. Blind run.** Replace the scorer sentence with: "A scorer, given the draft and the branch's `milestone` and `team-lead` folders, marks each scenario pass when the session's action is what those skills give for that point and the session needed no skill or doc it cannot read. A doc the draft names for threads (the index, the tracker doc) does not count as needed. Where the draft has no step for a scenario, the scorer names the gap. One failed scenario fails the run. Main's baseline is expected to fail, at the latest at the first scenario (its loop has no planning step)."
- Why: for "a feature thread reports a scope change", no coverage item requires a step. `milestone` planning step 3 has the feature thread report to the planning thread, but nothing in the coverage list carries that into the draft. Under the current rule ("matches the draft's step for it"), a correct branch draft can fail this scenario.
- The current wording also says nothing about docs the threads read, and gives the main baseline no expected result.

## Items the branch's skill text does not give
- **Item 12:** the "or says how the coordinator gets it" alternative (fix C).
- **Item 5:** narrower than `team-lead`'s rule (fix D).
- **Blind run, scope-change scenario:** no coverage item requires a draft step for it (fix G).

The other items match the branch text. That includes the tier fallback in item 10, which "name to the user any you could not fill" covers. In item 9, closing the Milestone issue on acceptance comes from `setup-project`'s list, not from `milestone`.

## Items main's text would pass anyway
- **Item 4:** main's loop step 1 has the same Startup verification gate.
- **Items 14, 15 and 16:** main has the same rules.
- **Item 11:** likely to pass on main because of the hint in the prompt; fix A removes it.
