import unittest
from tbs.dismantlable import DismantlableLattice
from tbs.graph import DirectedGraph


class TestDismantlableLattice(unittest.TestCase):
    @staticmethod
    def new_lattice():
        lattice = DismantlableLattice(DirectedGraph.from_edges([("bottom", 1),
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
        return lattice

    def setUp(self):
        self.lattice = self.new_lattice()

    def test_from_lattice(self):
        self.assertEqual(DismantlableLattice, DismantlableLattice.from_lattice(self.lattice).__class__)

    def test_support_tree(self):
        self.lattice.make_atomistic(lambda lattice, x: str(x))
        tree = self.lattice.support_tree()

        self.assertEqual({1, 2, 3, 4, '9'}, tree.vertices)
        self.assertEqual(4, tree.nb_edges)
        self.assertTrue(tree.isa_edge(1, 2))
        self.assertTrue(tree.isa_edge(3, 2))
        self.assertTrue(tree.isa_edge(4, 2))
        self.assertTrue(tree.isa_edge('9', 2) or tree.isa_edge('9', 4))

    def test_hierarchical_decomposition(self):
        self.assertEqual({1: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 'top': 0, 'bottom': 2, 2: 1},
                         self.lattice.hierarchical_decomposition())

    def test_hierarchical_decomposition_not_bottom(self):
        lattice = DismantlableLattice(DirectedGraph.from_edges([("bottom", 1),
                                                                ("bottom", 2),
                                                                ("bottom", 3),
                                                                ("bottom", 4),
                                                                (1, 5),
                                                                (2, 5),
                                                                (2, 6),
                                                                (3, 7),
                                                                (3, 6),
                                                                (4, 7),
                                                                (5, 8),
                                                                (6, 8),
                                                                (7, 9),
                                                                (8, "top"),
                                                                (9, "top")]))

        self.assertEqual({1: 0, 3: 1, 4: 0, 5: 0, 6: 1, 7: 0, 8: 0, 9: 0, 'top': 0, 'bottom': 2, 2: 1},
                         lattice.hierarchical_decomposition())
