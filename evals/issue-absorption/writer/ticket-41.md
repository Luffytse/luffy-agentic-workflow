## What to build

Preserve export formatting through a verified export roundtrip. This Ticket absorbs the source briefs [#21](fixture://issue/21) and [#22](fixture://issue/22).

**Model tier:** regular

**Status:** ready-for-agent

## Acceptance criteria

- [ ] An export roundtrip preserves decimal formatting and blank cells.
- [ ] An export roundtrip preserves date timezones and UTC offsets, including during DST transitions.
- [ ] Completion is demonstrated by a verified export roundtrip covering these cases.
- [ ] Closes #21
- [ ] Closes #22
