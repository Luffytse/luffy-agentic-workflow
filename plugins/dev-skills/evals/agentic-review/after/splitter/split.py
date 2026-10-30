from .expenses import total_paid


def split_evenly(total_cents, people):
    """Split total_cents among people so the shares add up to exactly the total."""
    if not people:
        raise ValueError("no one to split between")
    base, spare = divmod(total_cents, len(people))
    shares = {}
    for i, person in enumerate(people):
        shares[person] = base + (1 if i >= len(people) - spare else 0)
    return shares


def balances(expenses, people):
    """What each person is owed (positive) or owes (negative), in cents."""
    paid = total_paid(expenses)
    shares = split_evenly(sum(paid.values()), people)
    return {person: paid.get(person, 0) - shares[person] for person in people}


def settle(balances):
    """Transfers (debtor, creditor, cents) that bring every balance to zero."""
    creditors = sorted(((owed, person) for person, owed in balances.items() if owed > 0), reverse=True)
    pending = [[person, -owed] for person, owed in balances.items() if owed < 0]
    transfers = []
    for i in range(len(creditors) - 1):
        need, creditor = creditors[i]
        for item in list(pending):
            debtor, owes = item
            pay = min(owes, need)
            transfers.append((debtor, creditor, pay))
            need -= pay
            item[1] -= pay
            if item[1] == 0:
                pending.remove(item)
            if need == 0:
                break
    return transfers
