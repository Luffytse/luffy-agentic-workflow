# Building: Releases

The words of cutting a Release and planning the next. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Release**:
A named step of a Milestone (for example "Milestone 1 · Release 1"; a small Release is a Milestone with one Release), and the items it delivers, at most the **Release size** of them: the next **Slice** of the Milestone's features and the waiting issues. Every issue in it carries its release label (here `release-m<milestone>-r<n>`), and one release issue holds its plan, its **Main check** verdicts, the issues that **left the Release** at the cut (a **Parked** issue and what **waits with** it) and, once cut, its notes. A cut asks the user nothing unless an open issue of the Release is neither parked nor waits with a parked issue, and carries no issue over. Its name is never a version: `release` is version-free, and what a repo does with a version is its release doc's (ADR 0012, ADR 0016). Not a Milestone, which is the product goal its Releases work toward.
_Avoid_: sprint, version bump

**Release size**:
The most items a Release takes, set per repo in the release doc (setup's default 5; this repo 10), counted of any kind (a Spec with its Tickets is 1). Only a severe issue joins once it is full. Owned by `release` and the release doc.
_Avoid_: cap, feature cap

**Main check**:
The check **Release planning** makes before taking an issue: `release` reads each feature of the **Slice** and each waiting issue it is about to take, and nothing else, against freshly fetched main and gives it one verdict (still valid, already fixed, changed scope, obsolete, or cannot tell), with evidence on main, recorded in the release issue. Which issues it reads, what each verdict does and what goes to the user are `release`'s. A build thread makes the same check on its own issue as the **Build check**.
_Avoid_: validity check, re-triage

**Slice**:
The features `release` takes for the next Release: the open, unlabelled, unparked features of the Milestone issue's table, in its order and never re-ordered, up to the **Release size**. A feature whose blocker is parked, **waits with** a parked issue or cannot be taken by an agent is left out naming it (a Spec with a parked Ticket names that Ticket), with what depends on it; an unparked setup Ticket for the person leaves none out. The **bug dependency pass** places a waiting issue (one at `ready-for-agent` or marked `next-release`, a bug, chore or `retro` issue alike) that blocks a feature just before it, recording the blocker link; the other waiting issues follow the features (severe, `next-release`, the rest, oldest first), and a severe one joins past the size. Each Order entry ends with its `After:` blockers. A feature the table does not list is neither taken nor proposed. The rules are `release`'s.
_Avoid_: ranked list, re-ordering

**Release planning**:
The last step of `release`: the **Slice** and the waiting issues, each passing the **Main check** before it is taken, then opening the release issue and labelling what it takes; when nothing is taken it opens none and tells the user why. It runs with no approval; the user's part is planning the Milestone with `milestone`.
_Avoid_: release triage

**Cut steps**:
What a repo's release doc says the cut runs once the changelog entry is written, in order: what its versioning policy adds, anything else the repo must change or run, and optionally a step between Releases for a fix that cannot wait. A cut step wins over `release`'s own text where they differ, so the skill names no version policy.

**Triage batch**:
The run of `triage` that the Release thread makes at each Release end, naming the release issue just closed: agents decide every open `needs-triage` issue, a **Handed-over Retro issue** included, against the Milestone without asking the user per issue, make the **Backlog sweep** and post one `## Triage batch` summary on the release issue. Its procedure lives in its own file in the `triage` folder, `TRIAGE-BATCH.md`, which a session triaging with the user does not read; only the batch sets `next-release` by rule. Owned by `triage`.

**Backlog sweep**:
The second part of the **Triage batch**: a pass over every open `ready-for-agent` issue at a Release end, so that the waiting issues Release planning takes are a true backlog. It moves, closes, marks or **expires** each issue as `triage` says.

**Release thread**:
A project thread that runs `release`: it cuts the current Release (the changelog entry, the **Cut steps**, the merge, Retro planning and then the **Triage batch**), then plans the next. One started with nothing before it to cut only plans. When one starts is the **Team lead**'s; whether it cuts or plans is `release`'s "Find where you are".
