"""Cases for the to-tickets shared-doc-lines check. Shared by make_fixture.py, score.py and test_cases.py."""

# The fixture Spec's two work items. They touch different files and functions (`code`), so the only thing they can collide on is a glossary entry.
# Each names the glossary entry its docs update rewrites; a case may override an item's `entry` and `doc`.
SHOUT = {"slug": "shout-option", "title": "Add a shout option", "key": "format_greeting",
         "code": "greet.py, function format_greeting",
         "criteria": ["format_greeting('Ada', shout=True) returns 'HELLO ADA'"],
         "entry": "Greeting", "doc": "a Greeting can be shouted"}
HISTORY = {"slug": "greeting-history", "title": "Record greetings in a history", "key": "record_greeting",
           "code": "history.py, function record_greeting",
           "criteria": ["record_greeting('Ada') appends the line 'Hello Ada' to history.txt"],
           "entry": "Greeting", "doc": "each Greeting is recorded in the history"}
# Needs item 01's shout option in code (it logs shouted greetings), but rewrites a different glossary entry.
LOUD = {"slug": "loud-log", "title": "Log shouted greetings", "key": "record_shout",
        "code": "loudlog.py, function record_shout", "needs": "01",
        "criteria": ["record_shout('Ada') appends the line 'HELLO ADA' to loud.log"],
        "entry": "Loud log", "doc": "the Loud log lists every shouted Greeting"}
ITEMS = {"01": SHOUT, "02": HISTORY, "03": HISTORY}

# Per case: items present, per-item overrides, tickets already filed, and the expected shape of the published set.
#   "shape": "grouped" = one Ticket carrying both items, or two Tickets with exactly one blocked by the other;
#            "unblocked" = two Tickets, neither blocked; "chain_to_filed" = 01 filed and unblocked, 02 new, carrying the history item, and blocked by 01;
#            "pairs" = three items where 02 needs 01 in code and `pair` shares a glossary entry: that pair is in one Ticket or has a blocker path (direct or through another Ticket), and 02 follows 01.
CASES = {
    "shared": {
        "items": ["01", "02"], "overrides": {}, "shape": "grouped",
        "meaning": "both items rewrite the glossary entry Greeting and have no code dependency: publish one Ticket, or block one on the other",
    },
    "separate": {
        "items": ["01", "02"],
        "overrides": {"02": {"entry": "History", "doc": "the History lists every Greeting recorded"}}, "shape": "unblocked",
        "meaning": "the items rewrite different glossary entries and have no code dependency: two Tickets, neither blocked (control)",
    },
    "hidden": {
        "items": ["01", "02", "03"], "overrides": {"02": LOUD}, "shape": "pairs", "pair": ["01", "03"],
        "meaning": "01 and 02 depend on each other in code (02 needs 01), 01 and 03 share only the glossary entry Greeting, 02 and 03 share nothing: the 01/03 pair needs one Ticket or a blocker path, and 02 must follow 01",
    },
    "resume": {
        "items": ["01", "02"], "overrides": {}, "preexisting": ["01"], "shape": "chain_to_filed",
        "meaning": "publication resumed with 01 already filed and unblocked; 02 rewrites the same entry: 02 is published blocked by 01, no other new Ticket",
    },
}
