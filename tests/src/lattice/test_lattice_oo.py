from TBS.lattice_oo import Lattice
import unittest


class TestCoverGraph(unittest.TestCase):
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

    def test_init(self):
        self.assertSetEqual(frozenset(self.lattice.edges()), {("bottom", 1),
                                                    ("bottom", 2), ("bottom", 3), ("bottom", 4), (1, 5), (2, 5), (2, 6),
                                                    (2, 7), (3, 6), (4, 7), (5, 8), (6, 8), (7, 9), (8, "top"),
                                                    (9, "top")})
        self.assertSetEqual(frozenset(self.lattice.dual_lattice.edges()), {(1, "bottom"),
                                                                           (2, "bottom"), (3, "bottom"), (4, "bottom"), (5, 1), (5, 2), (6, 2),
                                                                           (7, 2), (6, 3), (7, 4), (8, 5), (8, 6), (9, 7), ("top", 8),
                                                                           ("top", 9)})

    def test_update(self):
        self.lattice.update((("bottom", 10), (10, 9)))
        self.assertIn((10, 9), self.lattice.edges())
        self.assertIn((9, 10), self.lattice.dual_lattice.edges())
        self.assertIn(("bottom", 10), self.lattice.edges())
        self.assertIn((10, "bottom"), self.lattice.dual_lattice.edges())

    def test_get_top(self):
        self.assertEqual(self.lattice.get_top(), "top")

    def test_get_bottom(self):
        self.assertEqual(self.lattice.get_bottom(), "bottom")

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
