import unittest
from tbs.lattice import Lattice, isa_lattice


class TestLattice(unittest.TestCase):
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
                                                              ("bottom", 2), ("bottom", 3), ("bottom", 4), (1, 5),
                                                              (2, 5), (2, 6),
                                                              (2, 7), (3, 6), (4, 7), (5, 8), (6, 8), (7, 9),
                                                              (8, "top"),
                                                              (9, "top")})
        self.assertSetEqual(frozenset(self.lattice.dual_lattice.edges()), {(1, "bottom"),
                                                                           (2, "bottom"), (3, "bottom"), (4, "bottom"),
                                                                           (5, 1), (5, 2), (6, 2),
                                                                           (7, 2), (6, 3), (7, 4), (8, 5), (8, 6),
                                                                           (9, 7), ("top", 8),
                                                                           ("top", 9)})

    def test_update(self):
        self.lattice.update((("bottom", 10), (10, 9)))
        self.assertIn((10, 9), self.lattice.edges())
        self.assertIn((9, 10), self.lattice.dual_lattice.edges())
        self.assertIn(("bottom", 10), self.lattice.edges())
        self.assertIn((10, "bottom"), self.lattice.dual_lattice.edges())


    def test_remove(self):
        self.lattice.remove(4)
        self.assertSetEqual(frozenset({"bottom", "top", 1, 2, 3, 5, 6, 7, 8, 9}), frozenset(self.lattice))
        self.assertSetEqual(frozenset({"bottom", "top", 1, 2, 3, 5, 6, 7, 8, 9}), frozenset(self.lattice.dual_lattice))

    def test_get_top(self):
        self.assertEqual(self.lattice.get_top(), "top")

    def test_get_bottom(self):
        self.assertEqual(self.lattice.get_bottom(), "bottom")

    def test_filter(self):
        sup_filter = self.lattice.sup_filter("bottom")
        self.assertEqual(frozenset(self.lattice), sup_filter)
        sup_filter = self.lattice.sup_filter("top")
        self.assertEqual(frozenset(["top"]), sup_filter)

    def test_isa_lattice(self):
        self.assertTrue(isa_lattice(self.lattice))

    def test_is_not_a_lattice(self):
        not_a_lattice = Lattice()
        not_a_lattice.update([("bottom", 1),
                              ("bottom", 2),
                              (1, 3),
                              (2, 3),
                              (1, 4),
                              (2, 4),
                              (3, "top"),
                              (4, "top")])
        self.assertFalse(isa_lattice(not_a_lattice))

    def test_compute_height(self):
        self.assertEqual(4, self.lattice.compute_height()["top"])
        self.assertEqual(0, self.lattice.compute_height()["bottom"])
        self.assertEqual(1, self.lattice.compute_height()[4])
        self.assertEqual(3, self.lattice.compute_height()[8])

    def test_sup(self):
        self.assertEqual(self.lattice.sup(1, 2), 5)
        self.assertEqual(self.lattice.sup(1, 4), "top")
        self.assertEqual(self.lattice.sup(1, 3), 8)
        self.assertEqual(self.lattice.sup(1, 5), 5)

    def test_inf(self):
        self.assertEqual(self.lattice.inf(5, 6), 2)
        self.assertEqual(self.lattice.inf(5, 9), 2)
        self.assertEqual(self.lattice.inf(5, 8), 5)
        self.assertEqual(self.lattice.inf(5, 4), "bottom")

    def test_atoms(self):
        self.assertSetEqual(self.lattice.atoms(), {1, 2, 3, 4})
        self.assertSetEqual(self.lattice.atoms(), {1, 2, 3, 4})

    def test_make_atomistic(self):
        self.lattice.make_atomistic()
        self.assertSetEqual(self.lattice.atoms(), {1, 2, 3, 4, 10})
        self.assertListEqual(self.lattice[10], [9])

    def test_is_atomistic(self):
        self.assertFalse(self.lattice.is_atomistic())
        self.lattice.update((('bottom', 10), (10, 9)))
        self.assertTrue(self.lattice.is_atomistic())


if __name__ == "__main__":
    unittest.main()
