"""Score retained runtime artifacts, not skill prose. Rerun runtimes per README first."""
import json
from pathlib import Path
r = Path(__file__).resolve().parent
expected = [
    ('#11', 'Waiting on an open Ticket', '#31', 2, False),
    ('#12', 'Closing with its Ticket', '#32', 2, True),
    ('#13', 'In the backlog', '#33', 2, False),
    ('#14', 'In the backlog', '#34', 2, False),
    ('#15', 'Waiting on an open Ticket', '#31', 2, False),
    ('#16', 'Failed-fix candidate', '#32', 3, False),
    ('#17', 'Closing with its Ticket', '#32', 2, True),
    ('#18', 'In the backlog', None, 2, False),
]
keys = ('source', 'status', 'authoritative_ticket', 'votes_retained', 'eligible_for_mechanical_close')
for case in ('baseline', 'candidate'):
    result = json.loads((r / case / 'result.json').read_text())
    assert [tuple(row[k] for k in keys) for row in result['sources']] == expected, case
lines = [line for line in (r / 'pr/closes.md').read_text().splitlines() if line.startswith('Closes ')]
assert len(lines) == 7
assert set(lines) == {
    'Closes #100', 'Closes #31', 'Closes #32', 'Closes #11', 'Closes #12', 'Closes #15', 'Closes #17'
}
assert json.loads((r / 'writer/comments.json').read_text()) == [
    {'issue': 21, 'body': 'Absorbed by #41; closes when it is completed.'},
    {'issue': 22, 'body': 'Absorbed by #41; closes when it is completed.'},
]
# Requirement meaning in ticket-41.md is manually scored in RESULTS.md.
print('PASS: baseline and candidate lifecycle decisions, PR closure set, publication records')
