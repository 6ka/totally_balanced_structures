__author__ = 'fbrucker'

import unittest

from DLC.diss import Diss
from DLC.subdominant import subdominant


class TestSubdominant(unittest.TestCase):
    def setUp(self):
        diss_matrix = [
            # 0  1  2  3
            [0, 1, 2, 1],  # 0
            [1, 0, 1, 2],  # 1
            [2, 1, 0, 1],  # 2
            [1, 2, 1, 0]]  # 3
        self.qu_diss = Diss(range(4)).update(lambda x, y: diss_matrix[x][y])

    def test_approximation(self):
        solution_matrix = [
            # 0  1  2  3
            [0, 1, 1, 1],  # 0
            [1, 0, 1, 1],  # 1
            [1, 1, 0, 1],  # 2
            [1, 2, 1, 0]]  # 3

        self.assertEqual(Diss(range(4)).update(lambda x, y: solution_matrix[x][y]), subdominant(self.qu_diss))
        self.assertEqual(subdominant(self.qu_diss), subdominant(subdominant(self.qu_diss)))

    def test_no_changes(self):
        self.qu_diss[0, 1] = 2
        self.assertEqual(self.qu_diss, subdominant(self.qu_diss))
