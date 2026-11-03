"""Cases for the to-tickets runtime-derived agent-label check. Shared by make_fixture.py, score.py and test_cases.py."""

# Two imaginary agents, "alpha" and "beta", so the fixture names no real agent. A repo maps the agent-only role to one label each.
MAPPING = {"alpha": "alpha-only", "beta": "beta-only"}
READY = "ready-for-agent"

# Child slices of the fixture Spec. `needs` is the agent whose native runtime the acceptance criteria demand, or None.
CHILDREN = {
    "01": {"slug": "format-greeting", "title": "Format a greeting", "needs": None,
           "criteria": ["format_greeting('Ada') returns 'Hello Ada'"]},
    "02": {"slug": "beta-runtime-run", "title": "Run the formatter in beta", "needs": "beta",
           "criteria": ["The formatter's tests pass when run inside beta's own runtime, and the run output is recorded"]},
    "03": {"slug": "record-beta-result", "title": "Record the beta run in the docs", "needs": None, "blocked_by": ["02"],
           "criteria": ["The docs list the recorded beta run from ticket 02"]},
}

# Per case: mapping present, labels on the source Spec, tickets that must exist after publication and their labels,
# tickets that must NOT exist (held), and what the report must name.
CASES = {
    "unrestricted": {
        "mapping": True, "source_labels": [], "children": ["01", "02"],
        "expect": {"01": [READY], "02": [READY, "beta-only"]},
        "report": {"02": ["beta-only"]},
        "meaning": "source has no agent label: 02 needs beta's runtime and gets beta-only with its reason reported; 01 stays unlabelled",
    },
    "inherited": {
        "mapping": True, "source_labels": ["alpha-only"], "children": ["01", "02"], "child_overrides": {"02": {"slug": "alpha-runtime-run", "title": "Run the formatter in alpha", "needs": "alpha",
                                   "criteria": ["The formatter's tests pass when run inside alpha's own runtime, and the run output is recorded"]}},
        "expect": {"01": [READY, "alpha-only"], "02": [READY, "alpha-only"]},
        "report": {},
        "meaning": "source is alpha-only and 02 needs alpha's runtime: both inherit alpha-only, no conflict",
    },
    "conflict": {
        "mapping": True, "source_labels": ["alpha-only"], "children": ["01", "02", "03"],
        "expect": {"01": [READY, "alpha-only"]}, "held": ["02", "03"],
        "report": {"02": ["alpha-only", "conflict"], "03": ["02"]},
        "meaning": "source is alpha-only but 02 needs beta's runtime: 02 is surfaced and not published, 03 (blocked by 02) waits, 01 inherits alpha-only; no label changed or removed",
    },
    "no-mapping": {
        "mapping": False, "source_labels": [], "children": ["01", "02"],
        "expect": {"01": [READY], "02": [READY]},
        "report": {"02": ["mapping"]},
        "meaning": "triage-labels doc has no agent-only role: no label is guessed; the report names 02 as needing beta's runtime",
    },
    "milestone": {
        "mapping": True, "source_labels": ["milestone-1", "release-m1-r1"], "children": ["01", "02"],
        "expect": {"01": [READY, "milestone-1", "release-m1-r1"], "02": [READY, "beta-only", "milestone-1", "release-m1-r1"]},
        "report": {"02": ["beta-only"]},
        "meaning": "same rule inside a Milestone: 02 gets beta-only on top of the unchanged Milestone and release labels",
    },
    "resume": {
        "mapping": True, "source_labels": [], "children": ["01", "02"], "preexisting": {"01": [READY], "02": [READY]},
        "expect": {"01": [READY], "02": [READY, "beta-only"]}, "no_new_tickets": True,
        "report": {"02": ["beta-only"]},
        "meaning": "publication resumed with 01 and 02 already filed and 02 never labelled: 02 gets beta-only, no new ticket is created",
    },
}
