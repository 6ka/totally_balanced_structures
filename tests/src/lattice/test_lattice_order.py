from TBS.lattice import Lattice, max_intersection
from TBS.graph import Graph
import unittest


class TestLatticeOrder(unittest.TestCase):
    @staticmethod
    def new_lattice():
        lattice = Lattice()
        lattice.update([("bottom", 1),
                        ("bottom", 2),
                        ("bottom", 3),
                        ("bottom", 4),
                        (1, 5),
                        (2, 5),
                        (2, 6),
                        (2, 7),
                        (3, 6),
                        (4, 7),
                        (5, 8),
                        (6, 8),
                        (7, 9),
                        (8, "top"),
                        (9, "top")])
        return lattice

    def setUp(self):
        self.lattice = self.new_lattice()

    def test_get_order(self):
        order = self.lattice.get_order()
        self.assertEqual({"top", 1, 2, 3, 4, 5, 6, 7, 8, 9}, frozenset(order["bottom"]))
        self.assertEqual({9, "top"}, set(order[7]))

    def test_comparability_function(self):
        smaller_than = self.lattice.comparability_function()
        self.assertTrue(smaller_than("bottom", "top"))
        self.assertTrue(smaller_than(1, 5))
        self.assertFalse(smaller_than(5, 1))
        self.assertFalse(smaller_than(7, 8))
