---
name: grilling
description: "Grill the user relentlessly about a plan, decision, or idea. Use when there is no working directory to record in, or the user wants only the interview with nothing written down; in a repo, grill-with-docs is the default."
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet.

Ask a **big** frontier question alone: one that changes the plan, is hard to undo, or turns on what only the user knows. Give two to four options at the same depth (what changes, the gain, the cost) and recommend one. The options are material: the user may combine them or bring another.

**Small** frontier questions, with an obvious default and nothing hanging off them, go together, at most three, each with its default, worded so "yes" accepts it. Any answer but yes makes it big. In doubt, it is big.

Use the tool's choice card where it has one, each card under its own question. Then wait for the user's answers before the next round.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent with a fresh context window to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
