# -*- coding: utf-8 -*-

import unittest
import TBS.graph
import TBS.lattice


class TestCoverGraph(unittest.TestCase):

    @staticmethod
    def new_lattice():
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

    def setUp(self):
        self.lattice = self.new_lattice()

    def test_filter(self):
        sup_filter = TBS.lattice.sup_filter(self.lattice, "bottom")
        self.assertEqual(frozenset(self.lattice), sup_filter)
        sup_filter = TBS.lattice.sup_filter(self.lattice, "top")
        self.assertEqual(frozenset(["top"]), sup_filter)

    def test_isa_lattice(self):
        self.assertTrue(TBS.lattice.isa_lattice(self.lattice))

    def test_is_not_a_lattice(self):
        not_a_lattice = TBS.graph.Graph(directed=True).update([("bottom", 1),
                                                               ("bottom", 2),
                                                               (1, 3),
                                                               (2, 3),
                                                               (1, 4),
                                                               (2, 4),
                                                               (3, "top"),
                                                               (4, "top")])
        self.assertFalse(TBS.lattice.isa_lattice(not_a_lattice))

    def test_top_bottom(self):
        self.assertEqual("top", TBS.lattice.get_top(self.lattice))
        self.assertEqual("bottom", TBS.lattice.get_bottom(self.lattice))

    def test_height(self):
        TBS.lattice.delete_join_irreducible(self.lattice, 9)
        expected = {"bottom": 0,
                    1: 1,
                    2: 1,
                    3: 1,
                    4: 1,
                    5: 2,
                    6: 2,
                    7: 2,
                    8: 3,
                    "top": 4}
        self.assertEqual(expected, TBS.lattice.compute_height(self.lattice))
