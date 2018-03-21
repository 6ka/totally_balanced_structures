import unittest

from tbs.diss import Diss
from tbs.graph import Graph
from tbs.chordal._totally_balanced_diss import isa_chordal_diss, isa_totally_balanced_diss, \
    approximation_to_totally_balanced_diss, isa_strongly_chordal_graph, diss_from_valued_gamma_free_matrix


class TestIsaStronglyChordalGraph(unittest.TestCase):
    def test_isa_strongly_chordal_graph(self):
        g = Graph.from_edges(((1, 2), (2, 3)))
        self.assertTrue(isa_strongly_chordal_graph(g))

        g = Graph.from_edges(((1, 4), (1, 5),
                              (2, 5), (2, 6),
                              (3, 4), (3, 6),
                              (4, 5), (5, 6), (6, 4)))
        self.assertFalse(isa_strongly_chordal_graph(g))


class TestIsaTotallyBalancedDiss(unittest.TestCase):
    def test_is_totally_balanced_cycle(self):
        diss = Diss(["x", "y", "z", "t"]).update_by_pos(
            lambda i, j: [[0],
                          [1, 0],
                          [1, 2, 0],
                          [2, 1, 1, 0]][max(i, j)][min(i, j)])
        self.assertFalse(isa_totally_balanced_diss(diss))

    def test_not_totally_balanced_but_chordal(self):
        diss = Diss(["x", "y", "z", "t"]).update_by_pos(
            lambda i, j: [[0],
                          [2, 0],
                          [2, 2, 0],
                          [3, 1, 1, 0]][max(i, j)][min(i, j)])
        self.assertTrue(isa_chordal_diss(diss))
        self.assertFalse(isa_totally_balanced_diss(diss))


class TestApproximateTotallyBalanced(unittest.TestCase):
    def test_no_modification(self):
        diss = Diss(["x", "y", "z", "t", "u"]).update_by_pos(
            lambda i, j: [[0],
                          [3, 0],
                          [4, 4, 0],
                          [5, 2, 5, 0],
                          [3, 3, 4, 5, 0]][max(i, j)][min(i, j)])
        self.assertTrue(isa_totally_balanced_diss(diss))
        self.assertEqual(diss, approximation_to_totally_balanced_diss(diss))

    def test_compatible_order_not_strongly_compatible(self):
        diss = Diss(["x", "y", "z", "t", "u"]).update_by_pos(
            lambda i, j: [[0],
                          [3, 0],
                          [4, 4, 0],
                          [5, 2, 5, 0],
                          [3, 3, 4, 5, 0]][max(i, j)][min(i, j)])

        self.assertEqual(diss, approximation_to_totally_balanced_diss(diss, ['u', 'z', 'x', 'y', 't']))

    def test_modif(self):
        diss = Diss(["x", "y", "z", "t"]).update_by_pos(
            lambda i, j: [[0],
                          [2, 0],
                          [2, 2, 0],
                          [3, 1, 1, 0]][max(i, j)][min(i, j)])

        diss_approximate = approximation_to_totally_balanced_diss(diss)
        self.assertNotEqual(diss, diss_approximate)
        self.assertFalse(isa_totally_balanced_diss(diss))
        self.assertTrue(isa_totally_balanced_diss(diss_approximate))


class TestDissFromGammaFreeMatrix(unittest.TestCase):
    def test_diss_from_valued_gamma_free_matrix(self):
        matrix = [[1, 0, 0, 1],
                  [0, 0, 1, 1],
                  [0, 1, 1, 1],
                  [0, 1, 1, 1],
                  [1, 1, 1, 1]]
        valuation = [2, 3, 4, 5]

        self.assertEqual(
            Diss(["x", "y", "z", "t", "u"]).update_by_pos(
                lambda i, j: [[0],
                              [3, 0],
                              [4, 4, 0],
                              [5, 2, 5, 0],
                              [3, 3, 4, 5, 0]][max(i, j)][min(i, j)]),
            Diss(["t", "z", "x", "u", "y"]).update_by_pos(diss_from_valued_gamma_free_matrix(matrix, valuation)))

    def test_columns_update(self):
        valuations = [3, 1, 2, 4]

        matrix = [[0, 1, 0, 1],
                  [1, 1, 1, 1],
                  [0, 0, 1, 1],
                  [1, 1, 1, 1],
                  [1, 1, 1, 1]]

        diss = Diss(list(range(len(matrix)))).update_by_pos(diss_from_valued_gamma_free_matrix(matrix, valuations))
        self.assertTrue(isa_totally_balanced_diss(diss))
        self.assertEqual(diss(3, 4), 1)
