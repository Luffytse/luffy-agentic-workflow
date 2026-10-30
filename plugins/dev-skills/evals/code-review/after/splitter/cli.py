import sys

from .money import format_cents, parse_amount
from .split import split_evenly


def main(argv):
    """splitter TOTAL NAME...: print each person's share of TOTAL."""
    total = parse_amount(argv[1])
    for person, share in split_evenly(total, argv[2:]).items():
        print(person, format_cents(share))


if __name__ == "__main__":
    main(sys.argv)
