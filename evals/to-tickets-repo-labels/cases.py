"""Cases for the to-tickets repo-labels check. Shared by make_fixture.py, score.py and test_cases.py."""

READY = "ready-for-agent"

# The repo labels the fixture's triage-labels doc records (cases with a table).
TABLE = {
    "frontend": "Work on the web UI under `ui/`: layout, styling, what the page shows.",
    "backend": "Work on the server code under `api/`: endpoints, queries, exports.",
}

# Child slices of the fixture Spec "order totals", an end-to-end Spec: its Tickets cut through the API, the UI and the docs.
CHILDREN = {
    "01": {"slug": "orders-total-endpoint", "title": "Add an order total to the orders endpoint",
           "criteria": ["`GET /orders/<id>` in `api/orders.py` returns the order's total, summed from its lines",
                        "A test in `api/test_orders.py` covers an order with two lines"]},
    "02": {"slug": "cart-shows-total", "title": "Show the order total on the cart page", "blocked_by": ["01"],
           "criteria": ["`ui/cart.html` shows the total from the orders endpoint under the lines",
                        "The total is right-aligned and readable on a phone"]},
    "03": {"slug": "document-total", "title": "Note the total in the changelog",
           "blocked_by": ["01", "02"],
           "criteria": ["`CHANGELOG.md` has a line saying orders now show a total"]},
}

# Per case: whether the triage-labels doc has the Repo labels table, the repo labels on the source Spec, whether the
# prompt says the user named them, and the labels each published ticket must end with.
CASES = {
    "split": {
        "table": True, "source_labels": [], "user_named": False,
        "expect": {"01": [READY, "backend"], "02": [READY, "frontend"], "03": [READY]},
        "meaning": "an end-to-end Spec with no repo label: the API Ticket gets backend, the UI Ticket frontend, the changelog Ticket neither",
    },
    "named": {
        "table": True, "source_labels": ["backend"], "user_named": True,
        "expect": {"01": [READY, "backend"], "02": [READY, "backend", "frontend"], "03": [READY, "backend"]},
        "meaning": "the user named backend for the Spec: it goes on every Ticket, and the UI Ticket still gets frontend by its own work",
    },
    "no-table": {
        "table": False, "source_labels": [], "user_named": False,
        "expect": {"01": [READY], "02": [READY], "03": [READY]},
        "meaning": "no Repo labels rows: no repo label is applied; the Tickets carry only what they carried before",
    },
}
