import unittest
from tbs.graph import DirectedGraph
from tbs.lattice import Lattice


class TestInit(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(DirectedGraph(), Lattice().hase_diagram)

    def test_hase(self):
        dag = DirectedGraph("abcd", (("a", "b"),
                                     ("b", "c"), ("b", "d"),
                                     ("c", "d")))

        hase_diagram = DirectedGraph("abcd", (("a", "b"),
                                              ("b", "c"),
                                              ("c", "d")))

        self.assertEqual(hase_diagram, Lattice(dag).hase_diagram)

    def test_comparability(self):
        dag = DirectedGraph("abcd", (("a", "b"),
                                     ("b", "c"), ("b", "d"),
                                     ("c", "d")))

        comparability = DirectedGraph("abcd", (("a", "b"), ("a", "c"), ("a", "d"),
                                               ("b", "c"), ("b", "d"),
                                               ("c", "d")))

        self.assertEqual(comparability, Lattice(dag).directed_comparability)

    def test_eq(self):
        hase_diagram = DirectedGraph("abcd", (("a", "b"),
                                              ("b", "c"),
                                              ("c", "d")))
        comparability = DirectedGraph("abcd", (("a", "b"), ("a", "c"), ("a", "d"),
                                               ("b", "c"), ("b", "d"),
                                               ("c", "d")))

        self.assertEqual(Lattice(hase_diagram), Lattice(comparability))


class TestElements(unittest.TestCase):
    def setUp(self):
        self.lattice = Lattice(DirectedGraph().update([("bottom", 1),
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
                                                       (9, "top")]))

    def test_top_bottom_empty(self):
        self.assertEqual(None, Lattice().top)
        self.assertEqual(None, Lattice().top)

    def test_top_bottom(self):
        self.assertEqual("top", self.lattice.top)
        self.assertEqual("bottom", self.lattice.bottom)

    def test_sup(self):
        self.assertEqual(1, self.lattice.sup(1, 1))

        self.assertEqual(5, self.lattice.sup(1, 2))
        self.assertEqual("top", self.lattice.sup(1, 4))
        self.assertEqual(8, self.lattice.sup(1, 3))
        self.assertEqual(5, self.lattice.sup(1, 5))

    def test_inf(self):
        self.assertEqual(1, self.lattice.inf(1, 1))
        self.assertEqual(2, self.lattice.inf(5, 6))
        self.assertEqual(2, self.lattice.inf(5, 9))
        self.assertEqual(5, self.lattice.inf(5, 8))
        self.assertEqual("bottom", self.lattice.inf(5, 4))


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.lattice = Lattice(DirectedGraph().update([("bottom", 1),
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
                                                       (9, "top")]))

    def test_sup(self):
        self.assertEqual(frozenset(self.lattice), self.lattice.sup_filter(self.lattice.bottom))
        self.assertEqual(frozenset(["top"]), self.lattice.sup_filter(self.lattice.top))

    def test_inf(self):
        self.assertEqual(frozenset(self.lattice), self.lattice.inf_filter(self.lattice.top))
        self.assertEqual(frozenset(["bottom"]), self.lattice.inf_filter(self.lattice.bottom))


class TestIrreducible(unittest.TestCase):
    def setUp(self):
        self.lattice = Lattice(DirectedGraph().update([("bottom", 1),
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
                                                       (9, "top")]))

    def test_inf(self):
        self.assertEqual({1, 3, 4, 5, 6, 7, 8, 9}, self.lattice.inf_irreducible)

    def test_sup(self):
        self.assertEqual({1, 2, 3, 4, 9}, self.lattice.sup_irreducible)


if __name__ == "__main__":
    unittest.main()
