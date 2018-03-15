import unittest
from tbs.graph import DirectedGraph, direct_acyclic_graph_to_direct_comparability_graph
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

    def test_from_lattice(self):
        hase_diagram = DirectedGraph("abcd", (("a", "b"),
                                              ("b", "c"),
                                              ("c", "d")))
        lattice_1 = Lattice(hase_diagram)

        lattice_2 = Lattice.from_lattice(Lattice(hase_diagram))
        self.assertEqual(lattice_1, lattice_2)

        lattice_2.add_join_irreducible("e", "a", "d")

        self.assertNotEqual(lattice_1, lattice_2)


class TestElements(unittest.TestCase):
    def setUp(self):
        self.lattice = Lattice(DirectedGraph.from_edges([("bottom", 1),
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

    def test_above(self):
        self.assertEqual({1, 2, 3, 4}, self.lattice.above(self.lattice.bottom))

    def test_under(self):
        self.assertEqual({5, 6}, self.lattice.under(8))

    def test_is_smaller_than_equality(self):
        self.assertFalse(self.lattice.is_smaller_than(5, 5))

    def test_is_larger_than_equality(self):
        self.assertFalse(self.lattice.is_larger_than(5, 5))

    def test_is_smaller_than_not_comparable(self):
        self.assertFalse(self.lattice.is_smaller_than(8, 9))

    def test_is_larger_than_not_comparable(self):
        self.assertFalse(self.lattice.is_larger_than(8, 9))

    def test_is_larger_than_ok(self):
        self.assertTrue(self.lattice.is_larger_than(8, 1))
        self.assertFalse(self.lattice.is_larger_than(1, 8))


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.lattice = Lattice(DirectedGraph.from_edges([("bottom", 1),
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
        self.assertEqual(frozenset(self.lattice), self.lattice.upper_filter(self.lattice.bottom))
        self.assertEqual(frozenset(["top"]), self.lattice.upper_filter(self.lattice.top))

    def test_inf(self):
        self.assertEqual(frozenset(self.lattice), self.lattice.lower_filter(self.lattice.top))
        self.assertEqual(frozenset(["bottom"]), self.lattice.lower_filter(self.lattice.bottom))


class TestIrreducible(unittest.TestCase):
    def setUp(self):
        self.lattice = Lattice(DirectedGraph.from_edges([("bottom", 1),
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

    def test_join(self):
        self.assertEqual({1, 3, 4, 9}, self.lattice.join_irreducible)

    def test_add_join_TypeError(self):
        self.assertRaises(TypeError,
                          self.lattice.add_join_irreducible, 2, 1, 5)
        self.assertRaises(TypeError,
                          self.lattice.add_join_irreducible, "new", 1, 1)
        self.assertRaises(TypeError,
                          self.lattice.add_join_irreducible, "new", "also new", 1)
        self.assertRaises(TypeError,
                          self.lattice.add_join_irreducible, "new", 1, "also new")
        self.assertRaises(TypeError,
                          self.lattice.add_join_irreducible, "new", 8, 9)

    def test_add_join_comparable_order(self):
        original_hase_diagram = self.lattice.hase_diagram

        self.assertEqual(Lattice(original_hase_diagram).add_join_irreducible("new", 1, 8),
                         Lattice(original_hase_diagram).add_join_irreducible("new", 8, 1))

    def test_add_join_comparable(self):
        new_hase = self.lattice.hase_diagram.difference([(1, 5)]).update([(1, "new"), ("new", 5)])

        self.lattice.add_join_irreducible("new", 1, 5)
        self.assertEqual(new_hase, self.lattice.hase_diagram)

        self.assertEqual(direct_acyclic_graph_to_direct_comparability_graph(new_hase),
                         self.lattice.directed_comparability)

    def test_add_join_from_empty_lattice(self):
        self.assertEqual(Lattice(DirectedGraph([0])), Lattice().add_join_irreducible(0, None, None))

    def test_add_join_from_one_element_lattice(self):
        self.assertEqual(Lattice(DirectedGraph([0, 1], ((0, 1),))),
                         Lattice(DirectedGraph([0])).add_join_irreducible(1, 0, None))
        self.assertEqual(Lattice(DirectedGraph([0, 1], ((1, 0),))),
                         Lattice(DirectedGraph([0])).add_join_irreducible(1, None, 0))


class TestAtoms(unittest.TestCase):
    def setUp(self):
        self.lattice = Lattice(DirectedGraph().update([(0, 1), (1, 2), (2, 3)]))

    def test_atoms(self):
        self.assertFalse(self.lattice.is_atomistic())
        self.assertEqual(Lattice(DirectedGraph().update([(0, 1), (1, 2),
                                                         (0, "2"), ("2", 2),
                                                         (0, "3"), ("3", 3), (2, 3)])),
                         self.lattice.make_atomistic(lambda lattice, x: str(x)))
        self.assertTrue(self.lattice.is_atomistic())

    def test_co_atoms(self):
        self.assertFalse(self.lattice.is_co_atomistic())
        self.assertEqual(Lattice(DirectedGraph().update([(0, 1), (0, "0"), ('0', 3),
                                                         (1, 2), (1, "1"), ("1", 3),
                                                         (2, 3)])),
                         self.lattice.make_co_atomistic(lambda lattice, x: str(x)))
        self.assertTrue(self.lattice.is_co_atomistic())

    def test_idempotence_atoms(self):
        lattice_orig = Lattice(DirectedGraph().update([(0, 1), (1, 2),
                                                       (0, "2"), ("2", 2),
                                                       (0, "3"), ("3", 3), (2, 3)]))
        lattice = Lattice(DirectedGraph().update([(0, 1), (1, 2),
                                                  (0, "2"), ("2", 2),
                                                  (0, "3"), ("3", 3), (2, 3)])).make_atomistic()

        self.assertEqual(lattice_orig, lattice)

    def test_idempotence_co_atoms(self):
        lattice_orig = Lattice(DirectedGraph().update([(0, 1), (0, "0"), ('0', 3),
                                                       (1, 2), (1, "1"), ("1", 3),
                                                       (2, 3)]))
        lattice = Lattice(DirectedGraph().update([(0, 1), (0, "0"), ('0', 3),
                                                  (1, 2), (1, "1"), ("1", 3),
                                                  (2, 3)])).make_co_atomistic()

        self.assertEqual(lattice_orig, lattice)

