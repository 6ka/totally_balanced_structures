import unittest
from TBS.lattice import Lattice


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

    def test_random_tb_init(self):
        random_lattice = Lattice.random_dismantlable_lattice(n_vertices=10)
        self.assertTrue(random_lattice.is_a_lattice())
        self.assertEqual(len(random_lattice), 12)

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
        self.assertTrue(self.lattice.is_a_lattice())

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
        self.assertFalse(not_a_lattice.is_a_lattice())

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

    def test_support_tree(self):
        self.lattice.make_atomistic()
        tree = self.lattice.support_tree()
        self.assertTrue(tree.isa_edge(frozenset({1}), frozenset({2})))
        self.assertTrue(tree.isa_edge(frozenset({3}), frozenset({2})))
        self.assertTrue(tree.isa_edge(frozenset({4}), frozenset({2})))
        self.assertTrue(
            tree.isa_edge(frozenset({10}), frozenset({2})) or tree.isa_edge(frozenset({10}), frozenset({4})))
        self.assertFalse(tree.isa_edge(frozenset({1}), frozenset({3})))
        self.assertFalse(tree.isa_edge(frozenset({1}), frozenset({4})))
        self.assertFalse(tree.isa_edge(frozenset({3}), frozenset({4})))
        self.assertFalse(tree.isa_edge(frozenset({10}), frozenset({1})))
        self.assertFalse(tree.isa_edge(frozenset({10}), frozenset({3})))
        self.assertFalse(
            tree.isa_edge(frozenset({10}), frozenset({2})) and tree.isa_edge(frozenset({10}), frozenset({4})))

    def test_from_context_matrix(self):
        matrix = [[1, 1, 0, 0],
                  [1, 1, 0, 1],
                  [0, 0, 1, 1]]

        c1 = ((0, 0), (0, 1))
        c2 = ((1, 0), (1, 1))
        c3 = ((1, 3), (1, 3))
        c4 = ((2, 2), (2, 3))

        cover_graph = Lattice()
        cover_graph.update([(c1, "TOP"),
                            (c3, "TOP"),
                            (c2, c1),
                            (c2, c3),
                            (c4, c3),
                            ("BOTTOM", c2),
                            ("BOTTOM", c4)])

        self.assertEqual(cover_graph, Lattice.from_dlo_matrix(matrix))

    def test_print_boxes(self):
        string_repr = self.lattice.print_boxes()

        result = " |4 3 7 9 6 1 5 8 " + "\n" + \
                 "-+-+-+-+-+-+-+-+-+" + "\n" + \
                 "9|. . .|9|. . . . " + "\n" + \
                 " +-+ +---+        " + "\n" + \
                 "4|4|-| 7 |. . . . " + "\n" + \
                 " +-+-+---+-+   +-+" + "\n" + \
                 "3|.|3|-*-|6|---|8|" + "\n" + \
                 " + +-+-----+ +---+" + "\n" + \
                 "2|. .|  7  |-| 5 |" + "\n" + \
                 " +   +-----+-----+" + "\n" + \
                 "1|. . . . .|  1  |" + "\n" + \
                 " +         +-----+"

        self.assertEqual(string_repr, result)


if __name__ == "__main__":
    unittest.main()
