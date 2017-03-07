# -*- coding: utf-8 -*-

import unittest
from TBS.graph import Graph
from TBS.lattice import inf_irreducible, sup_irreducible, sup_irreducible_clusters, inf_irreducible_clusters, \
    isa_lattice, delete_join_irreducible
from TBS.randomize import random_dismantable_lattice


class TestIrreducible(unittest.TestCase):
    @staticmethod
    def new_lattice():
        lattice = Graph(directed=True)
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

    def test_inf_irreducible(self):
        self.assertEqual(frozenset([1, 3, 4, 5, 6, 7, 8, 9]), inf_irreducible(self.lattice))

    def test_sup_irreducible(self):
        self.assertEqual(frozenset([1, 2, 3, 4, 9]), sup_irreducible(self.lattice))

    def test_inf_irreducible_without_bottom(self):
        self.lattice.remove("bottom")
        self.assertEqual(frozenset([1, 3, 4, 5, 6, 7, 8, 9]), inf_irreducible(self.lattice))

    def test_sup_irreducible_without_top(self):
        self.lattice.remove("top")
        self.assertEqual(frozenset([1, 2, 3, 4, 9]), sup_irreducible(self.lattice))

    def test_sup_irreducible_clusters(self):
        corresp = sup_irreducible_clusters(self.lattice)
        self.assertEqual(frozenset([3, 2, 1]), corresp[8])
        self.assertEqual(frozenset([9, 4, 3, 2, 1]), corresp["top"])
        self.assertEqual(frozenset(), corresp["bottom"])

    def test_inf_irreducible_clusters(self):
        corresp = inf_irreducible_clusters(self.lattice)
        self.assertEqual(frozenset([8]), corresp[8])
        self.assertEqual(frozenset(), corresp["top"])
        self.assertEqual(frozenset([1, 3, 4, 5, 6, 7, 8, 9]), corresp["bottom"])

    def test_deletion(self):
        for i in range(2):
            lattice = random_dismantable_lattice(10)
            join_irreducible = inf_irreducible(lattice).intersection(sup_irreducible(lattice))
            while join_irreducible:
                for join in join_irreducible:
                    delete_join_irreducible(lattice, join)
                    self.assertTrue(isa_lattice(lattice))
                join_irreducible = inf_irreducible(lattice).intersection(sup_irreducible(lattice))
            self.assertEqual(frozenset(["BOTTOM", "TOP"]), set(lattice))
