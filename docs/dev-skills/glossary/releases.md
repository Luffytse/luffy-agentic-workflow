# Building: Releases

The words of cutting a Release and planning the next. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Release**:
A named step of a Milestone (for example "Milestone 1 · Release 1"; a small Release is a Milestone with one Release), and the items it delivers, at most the **Release size** of them, picked from the top of the **Ranked list**. Every issue in it carries its release label (here `release-m<milestone>-r<n>`), and one release issue holds its plan, its **Main check** verdicts, what it carried over and, once cut, its notes. Its name is never a version: `release` is version-free, and what a repo does with a version is its release doc's (ADR 0012, ADR 0016). Not a Milestone, which is the product goal its Releases work toward.
_Avoid_: sprint, version bump

**Release size**:
The most items a Release takes, set per repo in the release doc (setup's default 5; this repo 10), counted of any kind (a Spec with its Tickets is 1). Only a severe issue joins once it is full. Owned by `release` and the release doc.
_Avoid_: cap, feature cap

**Main check**:
The first part of **Release planning**: `release` reads each open candidate issue against freshly fetched main and gives it one verdict (still valid, already fixed, changed scope, obsolete, or cannot tell), with evidence on main, recorded in the release issue. Which issues it reads, what each verdict does and what goes to the user are `release`'s. A build thread makes the same check on its own issue as the **Build check**.
_Avoid_: validity check, re-triage

**Ranked list**:
The one list `release` sorts every candidate for the next Release into once the **Main check** has run, in three priority groups: severe and `next-release` issues; the Milestone's planned features, each after its open blockers; then carried-over issues and other `ready-for-agent` bugs. A feature the Milestone issue does not list is never ranked. The ordering rules are `release`'s.

**Release planning**:
The last step of `release`: the **Main check**, the **Ranked list**, then taking from the top up to the **Release size**, opening the release issue and labelling what it takes; when nothing qualifies it opens none and says why. It runs with no approval; the user's part is planning the Milestone with `milestone`.
_Avoid_: release triage

**Cut steps**:
What a repo's release doc says the cut runs once the changelog entry is written, in order: what its versioning policy adds, anything else the repo must change or run, and optionally a step between Releases for a fix that cannot wait. A cut step wins over `release`'s own text where they differ, so the skill names no version policy.

**Triage batch**:
The run of `triage` that the Release thread makes at each Release end, naming the release issue just closed: agents decide every open `needs-triage` issue against the Milestone without asking the user per issue, make the **Backlog sweep** and post one `## Triage batch` summary on the release issue. A severe issue or a blocker of a feature being built is triaged at once instead. Owned by `triage`.

**Backlog sweep**:
The second part of the **Triage batch**: a pass over every open `ready-for-agent` issue at a Release end, so that the **Ranked list** ranks a true backlog. It moves, closes, marks or **expires** each issue as `triage` says.

**Release thread**:
A project thread that runs `release`: it cuts the current Release (the changelog entry, the **Cut steps**, the merge, the **Triage batch** and the Release-end Retro planning), then plans the next. One started with nothing before it to cut only plans. When one starts is the **Team lead**'s; whether it cuts or plans is `release`'s "Find where you are".
