from autocorrector import lev_distance
import unittest


class TestLevenshtein(unittest.TestCase):
    def test_same(self):
        self.assertEqual(lev_distance("writting", "writing"), 1)
        self.assertEqual(lev_distance("", ""), 0)

    def test_single_edit(self):
        self.assertEqual(lev_distance("kite", "site"), 1)
        self.assertEqual(lev_distance("cat", "cart"), 1)
        self.assertEqual(lev_distance("dg", "dog"), 1)
        self.assertEqual(lev_distance("writting", "writing"), 1)
        self.assertEqual(lev_distance("house", "mouse"), 1)

    def test_multiple_edits(self):
        self.assertEqual(lev_distance("algorithm", "logarithm"), 3)
        self.assertEqual(lev_distance("hello", "olleh"), 4)
        self.assertEqual(lev_distance("apple", "alppe"), 2)
        self.assertEqual(lev_distance("car", "crazy"), 3)
        self.assertEqual(lev_distance("kitten", "sitting"), 3)
        self.assertEqual(lev_distance("kangaroo", "parrot"), 5)
        self.assertEqual(lev_distance("banana", "bnnaaa"), 2)
        self.assertEqual(lev_distance("computer", "compooter"), 2)

    def test_empty_string(self):
        self.assertEqual(lev_distance("", "apple"), 5)
        self.assertEqual(lev_distance("apple", ""), 5)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)



