# Boundary record

What the user has agreed agents may do on their own in this repo, which actions are the user's to decide, and the limits agents work within. The `merging` skill, which the build skills and `release` load at their merge step, reads this record for every merge, instead of a fixed list, to decide whether a pull request crosses a boundary and so goes to the user.

- **Irreversible actions agents may take**: `<actions the user allowed, for example "delete test data generated during implementation">`. _(Write "none" if the user allowed none.)_
- **Actions that need the user's approval**: `<actions the user wants to decide, for example "delete production or customer data">`. _(An empty list is valid: write "none".)_
- **Budget**: `<the paid or limited resources agents may use and how much of each>`. _(Write "none" if no paid or limited resource is used.)_
- **Check-in interval**: 1 hour (how often a Milestone's scheduled check-ins wake the coordinator during delivery).
- **Milestone label form**: `milestone-<n>`. An issue belongs to a Milestone when it carries that Milestone's label, and the Milestone issue carries the same label. Skills read the form from here and never hard-code it.

## Milestone issues

A Milestone issue holds no boundaries of its own: this record applies to every issue, inside a Milestone or not. To allow or reserve an action for a Milestone, change this record.
