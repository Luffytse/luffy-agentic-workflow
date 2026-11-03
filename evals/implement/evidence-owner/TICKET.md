# 31: Probe a scheduled check-in

**What to build:** a `check-in` note in the repo's `docs/probes.md` saying how a scheduled check-in is armed and where the skill that arms it loads from.

**Model tier:** regular

## Acceptance criteria

- [ ] `docs/probes.md` has a "Check-in" section describing the arming steps.
- [ ] A recorded run schedules a check-in one minute ahead and sees it fire; `docs/probes.md` records the observed wake time and the folder the skill loaded from. (evidence from the build thread)
