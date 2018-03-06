import unittest

from tbs.graph import DirectedGraph, direct_acyclic_graph_to_direct_comparability_graph
from tbs.lattice import isa_lattice_directed_comparability_graph


class TestIsaLattice(unittest.TestCase):
    def setUp(self):
        self.dag = direct_acyclic_graph_to_direct_comparability_graph(DirectedGraph().update([("bottom", 1),
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

    def test_empty(self):
        self.assertTrue(isa_lattice_directed_comparability_graph(DirectedGraph()))

    def test_bottom_top(self):
        self.assertTrue(isa_lattice_directed_comparability_graph(DirectedGraph().update([(0, 1)])))

    def test_lattice(self):
        self.assertTrue(isa_lattice_directed_comparability_graph(self.dag))

    def test_is_not_a_lattice(self):
        not_a_lattice = DirectedGraph()
        not_a_lattice.update([("bottom", 1),
                              ("bottom", 2),
                              (1, 3),
                              (2, 3),
                              (1, 4),
                              (2, 4),
                              (3, "top"),
                              (4, "top")])
        self.assertFalse(isa_lattice_directed_comparability_graph(not_a_lattice))
