# -*- coding: utf-8 -*-

import unittest
import DLC.graph
import DLC.lattice


class TestCoverGraph(unittest.TestCase):

    def new_lattice(self):
        lattice = DLC.graph.Graph(directed=True)
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
        filter = DLC.lattice.sup_filter(self.lattice, "bottom")
        self.assertEqual(frozenset(self.lattice), filter)
        filter = DLC.lattice.sup_filter(self.lattice, "top")
        self.assertEqual(frozenset(["top"]), filter)

    def test_isa_lattice(self):
        self.assertTrue(DLC.lattice.isa_lattice_cover_graph(self.lattice))
        not_a_lattice = DLC.graph.Graph(directed=True).update([("bottom", 1),
                                                               ("bottom", 2),
                                                               (1, 3),
                                                               (2, 3),
                                                               (1, 4),
                                                               (2, 4),
                                                               (3, "top"),
                                                               (4, "top")])
        self.assertFalse(DLC.lattice.isa_lattice_cover_graph(not_a_lattice))

    def test_top_bottom(self):
        self.assertEqual("top", DLC.lattice.get_top(self.lattice))
        self.assertEqual("bottom", DLC.lattice.get_bottom(self.lattice))

    def test_height(self):
        DLC.lattice.delete_join_irreducible(self.lattice, 9)
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
        self.assertEqual(expected, DLC.lattice.compute_height(self.lattice))
