"""Cases for the to-tickets Milestone-signal check. Shared by make_fixture.py, score.py and test_cases.py."""

READY = "ready-for-agent"
UNFILED = "Hub login"  # a feature of the Milestone that is planned but has no issue yet

CHILDREN = {
    "01": {"slug": "format-greeting", "title": "Format a greeting", "criteria": ["format_greeting('Ada') returns 'Hello Ada'"]},
    "02": {"slug": "greet-after-login", "title": "Greet a logged-in user", "criteria": ["A logged-in user is greeted by name"]},
}

# `planning`: the Spec carries no label, the caller (the prompt) says it is planning a feature of Milestone 2 whose issue is not written yet,
# and nobody has approved the breakdown: the run publishes without asking. Ticket 02 needs the unfiled Hub login feature.
# `plain`: the same Spec with no Milestone signal and no approval: the run publishes nothing and asks.
CASES = {
    "planning": {
        "milestone_statement": True, "unfiled_blocker": True,
        "expect": {"01": [READY, "milestone-2"], "02": ["milestone-2"]},
        "report": {"02": ["hub login"]},
        "meaning": "caller names Milestone 2 (no issue yet): split published unasked, Tickets get milestone-2; 02 waits on an unfiled blocker so it is not ready-for-agent and the report names that blocker",
    },
    "plain": {
        "milestone_statement": False, "unfiled_blocker": False,
        "expect": {}, "ask": True,
        "report": {},
        "meaning": "no Milestone label and no caller statement: nothing is published and the run asks the user to approve the breakdown",
    },
}
