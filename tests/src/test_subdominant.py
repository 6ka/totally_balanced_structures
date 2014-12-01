__author__ = 'fbrucker'

import unittest

from DLC.diss import Diss
from DLC.subdominant import subdominant


class TestSubdominant(unittest.TestCase):
    def setUp(self):
        diss_matrix = [
            # 0   1   2   3  4  5
            [ 0, 10, 12, 13, 4, 8],  # 0
            [10,  0, 14, 15, 1, 5],  # 1
            [12, 14,  0, 11, 2, 7],  # 2
            [13, 15, 11,  0, 3, 9],  # 3
            [ 4,  1,  2,  3, 0, 6],  # 4
            [ 8,  5,  7,  9, 6, 0]]  # 5
        self.qu_diss = Diss(range(6)).update(lambda x, y: diss_matrix[x][y])

    def test_no_changes(self):
        print(self.qu_diss)
        print("---")
        print(subdominant(self.qu_diss))
