from html import escape

from .money import format_cents


def render_summary_html(title, expenses, transfers):
    """The trip summary page, shared with the group as a link."""
    rows = []
    for expense in expenses:
        rows.append(
            f"<tr><td>{expense.payer}</td><td>{escape(expense.description)}</td>"
            f"<td>{format_cents(expense.amount_cents)}</td></tr>"
        )
    moves = []
    for debtor, creditor, cents in transfers:
        moves.append(f"<li>{escape(debtor)} pays {creditor} {format_cents(cents)}</li>")
    return f"<h1>{escape(title)}</h1><table>{''.join(rows)}</table><ul>{''.join(moves)}</ul>"
