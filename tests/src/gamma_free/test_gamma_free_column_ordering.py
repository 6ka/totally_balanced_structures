import unittest

from tbs.graph import DirectedGraph
from tbs.gamma_free._gamma_free import GammaFree
from tbs.gamma_free._gamma_free_column_ordering import _column_intersection_graphs, _matrix_count, _order_refinement


class TestStronglyChordalToGammaFree(unittest.TestCase):
    def test_graph_intersection_no_edges(self):
        context_matrix = GammaFree([[1, 1, 0], [1, 0, 0], [0, 1, 1]])
        self.assertEqual(DirectedGraph((0, 1, 2)),
                         _column_intersection_graphs(context_matrix.matrix))

    def test_graph_intersection_2_edges(self):
        context_matrix = GammaFree([[1, 1, 0], [1, 0, 1], [0, 0, 1]])

        self.assertEqual(DirectedGraph((0, 1, 2), ((1, 0), (0, 2))),
                         _column_intersection_graphs(context_matrix.matrix))

    def test_matrix_count(self):
        context_matrix = GammaFree([[1, 1, 0], [1, 0, 1], [0, 0, 1]])
        self.assertEqual([[2, 1, 2], [1, 0, 2], [0, 0, 1]], _matrix_count(context_matrix.matrix))

    def test_order_refinement_no_initial_ordering(self):
        context_matrix = GammaFree([[0, 1, 0, 0, 1, 0],
                                    [0, 0, 0, 1, 0, 0],
                                    [0, 1, 0, 1, 1, 0]])
        self.assertEqual([0, 2, 5, 3, 1, 4], _order_refinement(context_matrix.matrix, [0, 1, 2, 3, 4, 5]))

    def test_order_refinement_initial_ordering(self):
        context_matrix = GammaFree([[0, 0, 0, 1, 1, 0],
                                    [0, 0, 0, 0, 0, 1],
                                    [0, 0, 0, 1, 1, 1]])
        self.assertEqual([0, 1, 2, 5, 3, 4], _order_refinement(context_matrix.matrix, [0, 3, 1, 5, 4, 2]))

    def test_context_matrix(self):
        context_matrix = GammaFree([[0, 1, 0, 0, 1, 0],
                                    [0, 0, 0, 1, 0, 0],
                                    [0, 1, 0, 1, 1, 0]])
        context_matrix.reorder_gamma_free_from_strongly_chordal_element_order()
        self.assertEqual((0, 1, 2), context_matrix.elements)
        self.assertEqual(((0, 0, 0, 0, 1, 1),
                          (0, 0, 0, 1, 0, 0),
                          (0, 0, 0, 1, 1, 1)), context_matrix.matrix)
