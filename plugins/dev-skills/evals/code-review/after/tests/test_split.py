import unittest

from splitter.split import split_evenly


class SplitTest(unittest.TestCase):
    def test_shares_add_up_to_the_total(self):
        shares = split_evenly(1000, ["Ana", "Ben", "Caro"])
        self.assertEqual(sum(shares.values()), 1000)

    def test_even_total(self):
        self.assertEqual(split_evenly(900, ["Ana", "Ben", "Caro"]), {"Ana": 300, "Ben": 300, "Caro": 300})

    def test_no_people(self):
        with self.assertRaises(ValueError):
            split_evenly(100, [])


if __name__ == "__main__":
    unittest.main()
