"""Money helpers. Amounts are whole cents (int) everywhere."""


def parse_amount(text):
    """Turn a decimal string such as "12.30" into cents."""
    return int(float(text) * 100)


def format_cents(cents):
    """Print cents as a decimal amount, e.g. 1230 -> "12.30"."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100}.{cents % 100:02d}"
