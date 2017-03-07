import unittest

from TBS.graph import Graph
from TBS.hierarchical_decomposition import hierarchical_height_from_lattice


class TestHierarchicalFromLattice(unittest.TestCase):
    def setUp(self):
        self.lattice = Graph(directed=True).update([("bottom", 1),
                                                    ("bottom", 2),
                                                    ("bottom", 3),
                                                    ("bottom", 4),
                                                    (1, 5),
                                                    (2, 5),
                                                    (3, 6),
                                                    (4, 6),
                                                    (6, 7),
                                                    (5, "top"),
                                                    (7, "top")])

    def test_hierarchical_decomposition_from_hierarchy(self):
        vertex_height = hierarchical_height_from_lattice(self.lattice)
        self.assertEqual({1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 'top': 0}, vertex_height)

    def test_hierarchical_decomposition_from_non_atom_sup_irreducibe(self):
        self.lattice.update([(2, 6)])
        self.lattice.remove(3)
        self.lattice.remove(4)
        vertex_height = hierarchical_height_from_lattice(self.lattice)
        self.assertEqual({1: 0, 2: 1, 5: 0, 6: 0, 7: 0, 'top': 0}, vertex_height)


