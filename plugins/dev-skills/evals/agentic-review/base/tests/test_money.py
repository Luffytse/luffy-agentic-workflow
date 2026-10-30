import unittest

from splitter.expenses import load_expenses, total_paid
from splitter.money import format_cents, parse_amount


class MoneyTest(unittest.TestCase):
    def test_parse_amount(self):
        self.assertEqual(parse_amount("12.30"), 1230)

    def test_format_cents(self):
        self.assertEqual(format_cents(1230), "12.30")
        self.assertEqual(format_cents(-5), "-0.05")

    def test_total_paid(self):
        expenses = load_expenses([("Ana", "10.00", "taxi"), ("Ana", "2.50", "water")])
        self.assertEqual(total_paid(expenses), {"Ana": 1250})


if __name__ == "__main__":
    unittest.main()
