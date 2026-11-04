# Release thread report (2026-11-04)

Where I was: the last release issue (#2, Release 2) is closed and holds both end-of-Release records, so I went to step 5 (plan the next Release). Steps 1-4 did not apply.

Planned Release 3 (Milestone #1), size 5, used 5. No severe or next-release issues.
Order: #20 Quiet flag, #21 Shout flag, #30 Typo in usage text, #31 Names with spaces, #32 --version prints 0.0.0.
Left out: #33 (size reached), #34 (size reached; also no repro steps).
Proposed to you: #45 Colour output is an unplanned feature (the Milestone excludes it); plan it with `milestone` if wanted.

Things you should know:
- Merged since Release 2 with no changelog entry yet (#7, #8, #9, #10); they ride into Release 3's changelog.
- #21 looks already built by PR #8, #30 already fixed by PR #7 (neither PR closes its issue), and #32 is probably obsolete after PR #10 dropped --version. They are ranked as the rules say; the builders should verify on main and close them (as completed, or not planned for #32). Their items still count toward the size.
- #31 is only half fixed (bye still cuts names).
- Release 1 label exists but no release issue for it; ignored.
- Release issue file number 46 is my guess at "next free".
