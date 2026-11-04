"""Shared data for the Repo labels cases of the setup-dev-skills eval (Ticket #691): the made-up tracker's labels and
issues, the three cases and what each must leave behind. Used by make_repo_labels_fixture.py and score_repo_labels.py."""

REPO = "example-org/scratch-app"

# Every label the skill itself uses already exists in the made-up tracker, so a correct run creates no label of its own
# and the only label a run may create is one the user asks for.
ROLE_LABELS = ["needs-triage", "needs-info", "ready-for-agent", "ready-for-human", "wontfix", "bug", "enhancement",
               "next-release"]
OTHER_COVERED = ["wayfinder:map", "wayfinder:research", "wayfinder:prototype", "wayfinder:grilling", "wayfinder:task",
                 "parked", "retro", "retro-planning", "release-m1-r1", "milestone-1"]
# Labels in use that no role or row covers: the candidates.
UNMAPPED = {
    "frontend": "Work on screens, components and styling",
    "backend": "Work on the API and the data layer",
    "docs-only": "Changes to documentation only",
}
ISSUES = [
    {"number": 11, "title": "Fix button alignment on the settings page", "body": "The save button overlaps the footer on narrow screens.", "labels": ["bug", "frontend"]},
    {"number": 12, "title": "Restyle the empty state of the orders list", "body": "Use the new card component.", "labels": ["enhancement", "frontend"]},
    {"number": 13, "title": "Add pagination to the orders endpoint", "body": "The endpoint returns every row.", "labels": ["enhancement", "backend"]},
    {"number": 14, "title": "Index the orders table by customer", "body": "Slow query on the customer page.", "labels": ["bug", "backend"]},
    {"number": 15, "title": "Fix typo in the install guide", "body": "README says 'instal'.", "labels": ["docs-only"]},
]
FRONTEND_LINE = "User interface work: screens, components and styling"
BACKEND_LINE = "API endpoints and the data layer"
NEW_LABEL = "security"
NEW_LINE = "Changes to authentication, secrets or permissions"

ALL_LABELS = ROLE_LABELS + OTHER_COVERED + list(UNMAPPED)

CASES = {
    "fresh": {
        "meaning": "first run, the user has labels of their own: candidates are the unmapped labels in use, two are picked "
                   "with drafted lines, one new label is added and created, nothing is deleted",
        "rows": {"frontend", "backend", NEW_LABEL},
        "candidates": {"frontend", "backend", "docs-only"},
        "created": {NEW_LABEL},
        "existing_rows": {},
        "recommend": "no",
    },
    "rerun-drop": {
        "meaning": "re-run over a doc with two rows: the user drops one row; the row goes, the kept row's line is untouched, "
                   "and the tracker label is not deleted",
        "rows": {"frontend"},
        "candidates": None,  # optional on a re-run; may hold only labels no row covers
        "created": set(),
        "existing_rows": {"frontend": FRONTEND_LINE, "backend": BACKEND_LINE},
        "recommend": "yes",  # rows exist
    },
    "none": {
        "meaning": "first run, the user answers no to labels of their own: the table stays empty, no candidates are offered, "
                   "nothing is created or deleted",
        "rows": set(),
        "candidates": set(),
        "created": set(),
        "existing_rows": {},
        "recommend": "no",
    },
}
