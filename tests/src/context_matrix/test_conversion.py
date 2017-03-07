
import unittest

from TBS.contextmatrix import ContextMatrix
from TBS.contextmatrix import conversion
from TBS.diss import Diss


class TestDissConversion(unittest.TestCase):
    def setUp(self):
        matrix = [[1, 1, 1],
                  [1, 0, 1],
                  [0, 1, 0]]
        self.context_matrix = ContextMatrix(matrix, elements=("a", "b", "c"), copy_matrix=False)

    def test_to_diss(self):

        diss = conversion.to_diss(self.context_matrix, lambda x: x + 1)
        diss_matrix = [[0, 1, 2],
                       [1, 0, 0],
                       [2, 0, 0]]
        self.assertEqual(diss, Diss(("a", "b", "c")).update_by_pos(lambda x, y: diss_matrix[x][y]))

