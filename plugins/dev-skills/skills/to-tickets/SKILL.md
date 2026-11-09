---
name: to-tickets
description: "Split a plan, spec or conversation into tracer-bullet tickets that declare their blockers, and publish them. Use when the user says \"break this into tickets\" or \"split into issues\", or asks for vertical slices of a spec."
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

Read the configured project issue-tracker and triage-label docs before publication. Use the triage-label doc's role-to-label mapping whenever applying a triage role. If either doc was not provided, tell the user to run `setup-dev-skills`.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

When another workflow calls this skill, retain its intended outcome, source roles (absorbed reports versus a parent), scope, constraints, failed-fix context, dependencies and publication budget. A problem approval permits investigation; step 4 still obtains approval of the concrete work. Load `issue-absorption` now when sources will be absorbed, so their bodies and comments inform the draft.

For a resumed publication, first reconcile existing identifiers and source mappings with tracker state, including Tickets whose labels or links were never completed. Retain the prior solution decision and repair only incomplete actions. An existing Ticket is not a new publication slot.

When the Spec says a note is on another issue ("a note is on #24") or that another issue must change, that note is posted: check it is there, and post it if missing.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Start at `docs/dev-skills/index.md` and open only the docs that fit (with no index, fall back to `docs/dev-skills/glossary.md` and `docs/dev-skills/adr/`). When the source Spec was filed in an earlier session, do this even if you explored before, and also open every ADR or glossary entry newer than the Spec: other threads may have decided since, and the slices follow the newer entry where it differs from the Spec (say so in the breakdown). Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

**Scope edges.** When a drafted ticket names a part it does not change ("step 5 is not changed here"), check that exclusion against every one of its acceptance criteria and against any step, template or shared piece that reuses the excluded part. Where a criterion needs the excluded part, the ticket says the smallest edit it may make there, in a "Scope edges" paragraph (for example "step 5 only for the Release's name and label"), so its Implementer edits no more and a reviewer does not flag that edit as scope creep. This check applies to every split, in or outside a Milestone.

**Shared doc lines.** When more than one drafted ticket would edit the same doc lines that describe a rule (a glossary entry, an index line, a README line), put those doc edits in one ticket, or block the later ticket on the earlier one, so tickets that can build in parallel never edit the same doc lines. Check every pair with no blocker path between them, not only the pairs you expect to run together; a pair where one already blocks the other needs nothing more. On a resumed publication, count the tickets already filed too: a new ticket that would edit the same lines as a filed one is blocked by it.

**Runs the Implementer cannot make.** When a criterion needs a run that takes tools an Implementer subagent does not hold (scheduling a check-in, stopping a worker, a recorded run only the top-level session can make), end that criterion with `(evidence from the build thread)` and say in the ticket what the run shows, so the build thread produces it and the Implementer drafts the entry with pending markers.

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

Give each ticket a **model tier**, the tier its Implementer runs on: **regular** by default, **premium** for heavy or tricky work (a subtle design call, wide-reaching changes, concurrency, security or money logic). Name the tier, never a vendor's model. Load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

For a caller requesting one complete Ticket, return before publication if the work needs several: explain the required slices and why one would be oversized, and let the caller settle the larger scope. Respect its available budget; a cap is not permission to expand the requested scope.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **Model tier**: regular or premium, and for premium one line on why
- **What it delivers**: the end-to-end behaviour this ticket makes work
- **Agent label**: only for a ticket whose runtime need sets one (step 5): the label and the criterion that requires that agent's runtime

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?
- Does each ticket's model tier fit its difficulty?

**A source Spec in a Milestone.** Read the Boundary record (`docs/dev-skills/boundaries.md`) for its Milestone label form. The source Spec is in a Milestone when it carries a label in that form, or when the caller says it is planning a feature of a named Milestone whose Milestone issue is not written yet (`milestone` planning, which labels that feature's issues when it writes the Milestone issue); otherwise, including with no Boundary record, this paragraph does not apply and the questions above go to the user as written. The user already planned that feature, so do not wait for them to approve its split: publish the breakdown (step 5) and report it to the user as the numbered list above, with its tiers and blocking edges, as long as the Tickets keep the Spec's scope. A Ticket that adds scope the Spec did not name, or drops scope it did (an absorbed issue counts as added scope), or whose runtime need conflicts with the Spec's agent label (step 5), goes to the user as one question about that Ticket; only that Ticket waits, and the rest are published. A Ticket blocked by a waiting Ticket waits with it (publish blockers first, step 5; never publish a dependent with a missing or dangling blocker), and the report names the Tickets held. When the Spec or its Milestone issue names a Ticket count and the split needs more Tickets of the same scope, the scope wins: publish the Tickets the scope needs and say in the report that the count gave way and why. This paragraph is for a Spec split, read from the source's own label or the caller's statement that it is planning a Milestone feature; a caller that says it is deciding at a Release end, or inside a Milestone (below), is the other case, and its rule governs there.

Iterate until the user approves the concrete breakdown, except for a source Spec in a Milestone (the paragraph above). When the caller says it is deciding at a Release end, or inside a Milestone, judge whether the breakdown is a feature (a Spec with its Tickets, not a lone Ticket): if so, publish nothing and return it to the caller as needs larger scope; if not, the caller's approval of the concrete breakdown stands in for the user's, so settle these questions with the caller and publish without asking the user. If the user declines, publish nothing; return the rejection and any next decision to the caller. On resume, retain an existing solution approval unless the proposed work changes.

### 5. Publish the tickets to the configured tracker

Publish the tickets with the tracker doc's operations (the tracker `setup-dev-skills` configured): one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the tracker's native blocking relationship where it has one; otherwise write each ticket's blockers in the form the tracker doc reads (for GitHub without native dependencies, a `Blocked by: #<n>, #<n>` line as the first line of the ticket body, above everything else including a `Part of #<parent>` line, and no `## Blocked by` section). The tracker doc's form wins over the issue template's `## Blocked by` section. If a native write fails at run time (for example a server without the dependencies API), write the tracker doc's fallback form for that ticket instead, using the tracker doc's way of adding a line to an issue body (the ticket already exists, and rewriting its body without reading it first loses its text), listing every blocker of that ticket, not only the failed one. Then check with the tracker doc's way of counting open blockers (it reads both the native edge and the body line) that every blocker of the ticket is in place in one form or the other; do not report the ticket published until they are. When blockers are written as the tracker doc's `Blocked by:` line or set as native edges, omit the `## Blocked by` section, including for a ticket with no blockers; write "None (can start immediately)" only where the issue template's `## Blocked by` section is kept. If the source was an existing issue that the tickets split (a parent, not one a Ticket absorbs, see below), make each ticket its sub-issue (tracker doc's operation). If that write fails at run time (for example a repo without sub-issues enabled), write the tracker doc's fallback form for that ticket instead, again with the tracker doc's way of adding a line to an issue body (a `Part of #<parent>` line on the line after the `Blocked by:` line, or as the first line if the ticket has none); then check with the tracker doc's way of checking a sub-issue link (it reads both the sub-issue edge and the body line) that the ticket is linked in one form or the other, and do not report the ticket published until it is. Apply the label mapped to the `ready-for-agent` role unless instructed otherwise; the tickets are agent-grabbable by construction. A ticket with a blocker that is planned but not yet filed (a feature of a Milestone still being planned) is published without that label, names the blocker in its body, and is reported (step 7); the caller labels it once the blocker is filed and linked. This is the one case where a ticket is published with a blocker that is not an issue yet (a held ticket's dependents still wait, above). If the repo has a release doc (`docs/dev-skills/release.md`) that defines a label prefix, and the source issue carries a label with that prefix (its Release's label), give each ticket that label too, so a Spec's Tickets ship in its Release. If the repo's triage-labels doc (`docs/dev-skills/triage-labels.md`) maps an agent-only role to labels, and the source issue carries one, give each ticket that same label too, so the agent that the Spec is for builds its Tickets. A ticket whose acceptance criteria demonstrably require one agent's native runtime (a run only that agent's own environment can make) also takes that agent's label from the mapping, even when the source carries none, so an agent without that runtime does not take it; every other ticket keeps the rule above (the source's label, else none), and on a resumed publication an existing ticket missing a derived label gets it, with no new ticket. Never guess a label: when the doc has no agent-only role or no label for that agent, give the ticket none and name it in the report as needing that agent's runtime. When the source carries a label for a different agent than a ticket's runtime need, neither the source's label nor the ticket's is changed or removed: that ticket is not published and goes to the user as one question about that ticket (to the caller, when it is deciding at a Release end or inside a Milestone), the other tickets are published, and a ticket it blocks waits with it (blockers first, above). The rule is the same in or outside a Milestone. When the source is in a Milestone (step 4), give each ticket that Milestone's label too, so the Tickets are in the same Milestone as the Spec: the source's own label, or for a Milestone the caller names that has no issue yet, the Boundary record's label form with the named number (creating the label if the tracker lacks it, as `milestone` planning does); when the source carries none and the caller names no Milestone or the form is unknown, give no ticket one. Give no other ticket a release label: an issue filed during a Release waits for the next Release planning. Apply the repo labels by the rule in `triage`'s Roles section (load `triage` by name), judging each ticket on its own work and not copying the source's repo labels; a repo label the user named for the source goes on every ticket, and on a resumed publication an existing ticket missing a repo label that fits gets it, with no new ticket.

If the source is **one or more existing issues** that a Ticket absorbs, load `issue-absorption` and apply its writing agreement while drafting and publishing. Right before publishing, also re-read every blocker's state and drop or note any already closed.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Do NOT close or modify any parent issue.

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue that the tickets split, otherwise omit this section; an issue the Ticket absorbs goes in What to build, not here).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation. When the Ticket absorbs existing issues (step 5), name them here with links to their briefs, not copies.

**Model tier:** this ticket's tier as set in the breakdown: `regular` or `premium`.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] `Closes #<n>`, one line per absorbed issue (only when the Ticket absorbs existing issues, step 5)

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)". Omit this section when blockers were set as native edges or as a `Blocked by:` line (step 5), including for a ticket with no blockers; write "None (can start immediately)" only where the section is kept.
</issue-template>

Avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

### 6. Offer `setup-project`

Once the tickets are published, decide whether they changed what the project's threads need: a new repo, a new kind of thread, or a new standing rule. If so, offer the user `setup-project` in one line naming what changed. Only offer: call the Skill tool with "setup-project" only after the user says yes. If nothing changed, say nothing about it.

### 7. Return to the caller

Return the outcome (published, needs larger scope, declined or incomplete), every created Ticket identifier, source-to-ticket mappings, each runtime-derived agent label with its reason, each Ticket held for a conflicting source label or left unlabelled for want of a mapping, each Ticket published without `ready-for-agent` with the blocker it waits for, and all unfinished actions. Preserve identifiers even if creation succeeded but a later operation failed; report those as incomplete rather than fully published. The caller reconciles its record and cap before continuing. Do not ask again for an unchanged solution's approval on return.
