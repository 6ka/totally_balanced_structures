import unittest

from tbs.diss import Diss
from tbs.totally_balanced_diss.gamma_free_matrix import diss_from_valued_gamma_free_matrix
from tbs.totally_balanced_diss.totally_balanced_diss import isa_totally_balanced_diss


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

        matrix = [[0, 1, 0,   1],
                  [1, 1, 1,   1],
                  [0, 0, 1,   1],
                  [1, 1, 1,   1],
                  [1, 1, 1,   1]]

        diss = Diss(list(range(len(matrix)))).update_by_pos(diss_from_valued_gamma_free_matrix(matrix, valuations))
        self.assertTrue(isa_totally_balanced_diss(diss))
        self.assertEqual(diss(3, 4), 1)