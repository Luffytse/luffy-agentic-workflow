# Triage batch

The Release thread runs the batch from `triage` at a Release end, naming the Release just closed or its release issue. Agents decide: the user is asked nothing per issue, except as "Goes to the user" says. Before the first issue, read the release issue, the Milestone issue it names (goal, features, acceptance criteria, exclusions) and the Boundary record (`docs/dev-skills/boundaries.md`), and fetch main. Every comment triage posts here starts with the disclaimer in [SKILL.md](SKILL.md), and each one on an issue names the Release, so a rerun can tell what this batch already did. Skip `retro` issues throughout.

### 1. Triage the new issues

For every open `needs-triage` issue:

1. Gather context and verify the claim (steps 1 and 3 of "Triage a specific issue or PR" in [SKILL.md](SKILL.md)). Where the issue needs fleshing out (step 4), settle it by reading the code, docs, ADRs, the Milestone issue and the issue's comments; ask nobody.
2. Decide the category and the state, with the agent-found enhancement rule in Roles, the `next-release` rule in part 2, and the triage-labels doc's rule for repo labels. When "Goes to the user" applies to the issue, apply nothing (no brief, no label change) and leave it `needs-triage`. Otherwise apply the outcome as step 5 of "Triage a specific issue or PR" says: an agent brief for `ready-for-agent`, a brief for `ready-for-human`, triage notes for `needs-info`, a close as completed for an already-implemented one, a reasoned close for `wontfix`.
3. Record the decision on the issue in a comment: category, state, any mark, any repo label added or removed and the reason (a removed repo label's one-line reason can be this comment).

Done when no open issue but those waiting on the user is at `needs-triage`.

### 2. Sweep the backlog

The **sweep** keeps the `ready-for-agent` backlog true, since Release planning ranks all of it.

The **`next-release` mark** goes on a `ready-for-agent` issue that is **severe** (a security hole, lost data, or delivery stopped: nothing can merge or ship) or that blocks a **planned feature** (one the Milestone issue lists: the open issue carrying a label in the Boundary record's Milestone label form, or for a batch the one its release issue names). Only the batch sets it by this rule.

For every open `ready-for-agent` issue (those part 1 just moved there included), take the first test that fits:

1. **Agent-found enhancement**: move it to `ready-for-human`, with a comment saying why. Nothing else in the sweep touches it.
2. **Duplicate**: it reports the same problem or asks for the same change as another open issue. Keep the one with the fuller brief (the older when they are even), close the other as a duplicate (as not planned where the tracker has no duplicate outcome) with a comment linking the kept issue, and comment on the kept issue anything only the closed one said.
3. **Obsolete**: main's current code no longer has the problem or already does what the issue asks; reproduce it or read the code to confirm. Close it as completed, since main already has the work and nothing is left to do, with the reason: where on main it is fixed or done, and the commit or pull request when you find it. A planned feature it blocks is then unblocked, as a close as completed counts as done.
4. **Needs the mark**: it is severe or blocks a planned feature and lacks `next-release`: set it, with a comment giving the reason.
5. **Expired**: it is listed under "Left out" in the release issues of each of the last 3 Releases cut (the one just closed and the two before it). Find the two earlier release issues by the name, label and title forms the repo's release doc (`docs/dev-skills/release.md`) gives (the Releases whose names come just before the closed one's), and read only each one's "Left out" section. Close it as not planned, with a comment naming those Releases and saying "reopen to bring it back". With fewer than 3 Releases cut, nothing expires. A planned feature, a Ticket of a planned Spec, a parked issue and one already marked `next-release` never expire.

A planned feature, or a Ticket of a planned Spec, that reads as a duplicate or obsolete is not closed: closing it would change the Milestone's agreement, so it goes to the user. Any other issue stays as it is.

Done when every open `ready-for-agent` issue has been through the tests.

### Goes to the user

Ask one question per decision, saying which kind it is, for a decision that:

- **crosses a boundary** in the Boundary record,
- **changes the Milestone's agreement** (goal, acceptance criteria, exclusions), for example a person's request for a feature the Milestone issue does not list, or closing a planned feature, or
- needs the issue's **conflicting state roles** settled.

The issue keeps its labels until the user answers, and the summary lists it as waiting on the user. Every other decision is the agent's.

### The summary

At the end, post one comment on the release issue. It starts with the disclaimer and then the heading `## Triage batch`, and lists every issue the run decided or changed in the sweep since the last summary, one row each: issue, category, state, reason, and one outcome of `next-release`, `stays open`, `ready-for-human`, `closed` (duplicate, obsolete, already implemented or `wontfix`), `expired` or `waiting on the user`. An issue the sweep left as it was gets no row. A rerun for the same release issue posts a new comment under the same heading, covering only what it decided; an issue whose comment from this batch is already on it is not decided again.

Any merge-time step the repo's own docs give is not part of the batch; it stays at or after the merge it belongs to.
