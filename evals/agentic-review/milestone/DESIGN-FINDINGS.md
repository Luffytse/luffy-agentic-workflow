# Round 2's kept Findings

The Findings Round 2's Verify kept on the Milestone-agreement fixture, as the decision-level run and the design-answer briefs get them. Keep this file away from the Finders: it would prime them. `make-fixture.sh` pastes the three Findings (from the first `#### R` line on) into `PROMPT.md`, and `briefs.sh` pastes one design Finding into each design-answer brief, never this file's path or name.

#### R2-1 (spec Finder; Verifier: keep, caused by this change, Important)

### Item names with a comma split into extra columns
- Severity (proposed): Important
- Bug class: field quoting
- Locations: src/export.sh:8, docs/dev-skills/adr/0002-export-format.md:3
- Claim: ADR 0002 says only that fields are "separated by commas" and settles no quoting, and `export.sh` prints every field raw, so a name holding a comma or a double quote breaks the row. The format leaves this case unsettled.
- Failure scenario: the list holds `eggs, large|1|Ana`; the export prints `eggs, large,1,Ana`, which a spreadsheet opens as four columns ("eggs", " large", "1", "Ana"), against AC2 (each field in its own column).
- Evidence: `printf '%s,%s,%s\n' "$name" "$qty" "$who"` (src/export.sh:8); "its fields separated by commas" (docs/dev-skills/adr/0002-export-format.md:3); AC2: "Opening the output in a spreadsheet shows one row per item, each field in its own column."

#### R2-2 (adversarial Finder, contradictions; Verifier: keep, caused by this change, Important)

### The export carries household members' names
- Severity (proposed): Important
- Bug class: personal data in an export
- Locations: src/export.sh:5, src/export.sh:8, docs/dev-skills/adr/0002-export-format.md:3
- Claim: the export writes the `added_by` column, the name of the household member who added each item, into the file it hands to someone else. The Milestone excludes any personal data in an exported file, and ADR 0002 records the column as the format.
- Failure scenario: Ana exports the list and sends it to a neighbour; the file names Ana and Ben on every line, the personal data the Milestone says stays on the device.
- Evidence: `echo "item,qty,added_by"` (src/export.sh:5); "the header `item,qty,added_by`" (docs/dev-skills/adr/0002-export-format.md:3); the Milestone's Excluded: "Any personal data in an exported file: the names of household members stay on the device."

#### R2-3 (standards Finder; Verifier: keep, caused by this change, Nit (fix))

### ADR 0002 has no line in the docs index
- Severity (proposed): Nit
- Bug class: docs index drift
- Locations: docs/dev-skills/index.md:6
- Claim: the change adds `docs/dev-skills/adr/0002-export-format.md` and gives it no line in `docs/dev-skills/index.md`.
- Failure scenario: an agent starting at the index never finds the export format, and writes a second one.
- Evidence: `docs/dev-skills/index.md` lists ADR 0001 only.
