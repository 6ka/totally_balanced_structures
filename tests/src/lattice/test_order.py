# -*- coding: utf-8 -*-

import unittest
import TBS.graph
import TBS.lattice


class TestOrder(unittest.TestCase):

    @staticmethod
    def generic_lattice():
        lattice = TBS.graph.Graph(directed=True)
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

    def test_get_order(self):
        dual_lattice_order = TBS.lattice.get_order(self.generic_lattice()).dual()
        self.assertEqual({"bottom", 1, 2, 3, 4, 5, 6, 7, 8, 9}, set(dual_lattice_order["top"]))
        self.assertEqual({"bottom", 2, 4}, set(dual_lattice_order[7]))

    def test_comparability_function(self):
        smaller_than = TBS.lattice.comparability_function(self.generic_lattice())
        self.assertTrue(smaller_than("bottom", "top"))
        self.assertTrue(smaller_than(1, 5))
        self.assertFalse(smaller_than(5, 1))
        self.assertFalse(smaller_than(7, 8))
