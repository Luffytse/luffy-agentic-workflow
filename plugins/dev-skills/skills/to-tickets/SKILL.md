---
name: to-tickets
description: "Split a plan, spec or conversation into tracer-bullet tickets that declare their blockers, and publish them. Use when the user says \"break this into tickets\" or \"split into issues\", or asks for vertical slices of a spec."
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

Read the configured project issue-tracker and triage-label docs before publication. Use the triage-label doc's role-to-label mapping whenever applying a triage role. If either doc was not provided, tell the user to run `setup-dev-skills`.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments. When the source is one or more existing issues that a Ticket absorbs, load `issue-absorption` and follow its writing agreement while drafting and publishing.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching, including any recorded after the Spec was filed.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

Give each ticket a **model tier**, the tier its Implementer runs on: **regular** by default, **premium** for heavy or tricky work (a subtle design call, wide-reaching changes, concurrency, security or money logic), never top. Name the tier, never a vendor's model.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **Model tier**: regular or premium, and for premium one line on why
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown. Publish nothing before they do, whether or not the source is in a Milestone; if the user declines, publish nothing.

### 5. Publish the tickets to the configured tracker

Publish the approved tickets with the tracker doc's operations (the tracker `setup-dev-skills` configured): one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the tracker's native blocking relationship where it has one; otherwise write each ticket's blockers in the form the tracker doc reads (on GitHub, a `Blocked by: #<n>, #<n>` first line), which wins over the template's `## Blocked by` section. If the source was an existing issue that the tickets split (a parent, not an issue a Ticket absorbs), make each ticket its sub-issue. When a link write fails, follow the tracker doc's **Blocking**, **Make an issue a sub-issue of a parent**, **Add a line to an issue body**, **Count open blockers** and **Check a sub-issue link**; do not report a ticket published until its links are checked. Apply the label mapped to the `ready-for-agent` role unless instructed otherwise; the tickets are agent-grabbable by construction.

Each ticket also takes the source issue's Release label (the release doc's label prefix) and Milestone label (the Boundary record's form), where the source carries one, so the Tickets ship in the Spec's Release and count in its Milestone. A ticket gets neither any other way; when the source has no Milestone label yet, `milestone` labels the feature's issues when it writes the Milestone issue. Apply the repo labels as the triage-labels doc says, judging each ticket on its own work and not copying the source's repo labels; a repo label the user named for the source goes on every ticket.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Do NOT close or modify any parent issue.

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue that the tickets split, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

**Model tier:** this ticket's tier as set in the breakdown: `regular` or `premium`.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] `Closes #<n>`, one line per absorbed issue (only when the Ticket absorbs existing issues)

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)". Omit this section when blockers were set as native edges or as the tracker doc's `Blocked by:` line.

</issue-template>

Avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.
