import unittest
from tbs.dismantlable import DismantlableLattice, random_dismantlable_lattice
from tbs.lattice import isa_lattice_directed_comparability_graph
from tbs.graph import DirectedGraph


class TestDismantlableLattice(unittest.TestCase):
    def test_random_tb_init(self):
        random_lattice = random_dismantlable_lattice(n_vertices=10)
        self.assertTrue(isa_lattice_directed_comparability_graph(random_lattice.hase_diagram))
        self.assertEqual({"BOTTOM", "TOP", 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, set(random_lattice))

    def test_from_context_matrix(self):
        matrix = [[1, 1, 0, 0],
                  [1, 1, 0, 1],
                  [0, 0, 1, 1]]

        c1 = ((0, 0), (0, 1))
        c2 = ((1, 0), (1, 1))
        c3 = ((1, 3), (1, 3))
        c4 = ((2, 2), (2, 3))

        cover_graph = DirectedGraph.from_edges([(c1, "TOP"),
                                                (c3, "TOP"),
                                                (c2, c1),
                                                (c2, c3),
                                                (c4, c3),
                                                ("BOTTOM", c2),
                                                ("BOTTOM", c4)])

        self.assertEqual(cover_graph, DismantlableLattice.from_dlo_matrix(matrix))
