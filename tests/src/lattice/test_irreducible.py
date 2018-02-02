from tbs.lattice import Lattice, max_intersection
from tbs.graph import Graph
import unittest

class TestIrreducible(unittest.TestCase):
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

    def test_inf_irreducible(self):
        self.assertSetEqual(self.lattice.inf_irreducible(), frozenset({1, 3, 4, 5, 6, 7, 8, 9}))

    def test_sup_irreducible(self):
        self.assertSetEqual(self.lattice.sup_irreducible(), frozenset({1, 2, 3, 4, 9}))

    def test_sup_irreducible_clusters(self):
        clusters = self.lattice.sup_irreducible_clusters()
        self.assertSetEqual(clusters[5], frozenset({1, 2}))
        self.assertSetEqual(clusters[8], frozenset({1, 2, 3}))
        self.assertSetEqual(clusters["bottom"], frozenset())
        self.assertSetEqual(clusters["top"], frozenset({1, 2, 3, 4, 9}))

    def test_inf_irreducible_clusters(self):
        clusters = self.lattice.inf_irreducible_clusters()
        self.assertSetEqual(clusters["bottom"], frozenset({1, 3, 4, 5, 6, 7, 8, 9}))
        self.assertSetEqual(clusters[5], frozenset({5, 8}))
        self.assertSetEqual(clusters[8], frozenset({8}))
        self.assertSetEqual(clusters["top"], frozenset())

    def test_inf_irreducible_without_bottom(self):
        self.lattice.remove("bottom")
        self.assertEqual(frozenset([1, 3, 4, 5, 6, 7, 8, 9]), self.lattice.inf_irreducible())

    def test_sup_irreducible_without_top(self):
        self.lattice.remove("top")
        self.assertEqual(frozenset([1, 2, 3, 4, 9]), self.lattice.sup_irreducible())

    def test_delete_join_irreducible(self):
        self.lattice.delete_join_irreducible(4)
        self.assertEqual(frozenset({"bottom", "top", 1, 2, 3, 5, 6, 7, 8, 9}), set(self.lattice))
        self.assertEqual(frozenset({"bottom", "top", 1, 2, 3, 5, 6, 7, 8, 9}), set(self.lattice.dual_lattice))

    def test_dismantle(self):
        join_irreducible = self.lattice.inf_irreducible().intersection(self.lattice.sup_irreducible())
        while join_irreducible:
            for join in join_irreducible:
                self.lattice.delete_join_irreducible(join)
                self.assertTrue(self.lattice.is_a_lattice())
            join_irreducible = self.lattice.inf_irreducible().intersection(self.lattice.sup_irreducible())
        self.assertEqual(frozenset(["bottom", "top"]), set(self.lattice))
