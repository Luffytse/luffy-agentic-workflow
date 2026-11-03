# Round 0: expected results

One fresh top-level session per branch, given its `PROMPT-<branch>.md`. Keep this file away from it.

| Branch | Level | Why | Comment written | Skills loaded |
|--------|-------|-----|-----------------|---------------|
| `version-only` | None | every changed line is the manifest's `version` field or a changelog entry | one line, the Round 0 record `agentic-review` gives (`kind=round round=0 level=None`, the full head of `version-only`) | `agentic-review` only |
| `typo` | Quick | one misspelled word in `skills/greet/SKILL.md`; what the rule says is unchanged | none: a Round would run, and its comment carries the level | `agentic-review`; `review-rounds` not loaded (the prompt stops there) |
| `rule-change` | Standard | `skills/greet/SKILL.md` now says to greet by full name: what a rule does changed | none, as for `typo` | as for `typo` |

A run passes when, for each branch:

- the level is the one above, with a reason that names the file or the kind of change that decided it;
- for `version-only`, the session ran the project's checks (`bash check.sh`) and they passed, the comment file holds exactly one line in the Round 0 shape, and no subagent was started;
- for `typo` and `rule-change`, it says it would hand over to `review-rounds` at that level, and started no subagent;
- nothing in the run asked the user anything.

Fails to watch for: `typo` sized Standard because it touches a skill file (the defaults size by what the change does, not the path); `rule-change` sized Quick because the diff is small; `version-only` sized Quick, or a Round started for it.

Record each run in [`../RESULTS.md`](../RESULTS.md): the plugin version, the runtime and tier, the three levels and reasons, the files read and skills loaded (from the session's tool calls), and the pass or fail of each row.
