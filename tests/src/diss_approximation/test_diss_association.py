import unittest

from DLC.diss_approximation.diss_association import cluster_matrix_from_column_indices, diss_from_cluster_matrix, \
    column_indices_from_chordally_compatible_diss
from DLC.diss import Diss
from contextmatrix import ContextMatrix


class TestIndexedColumns(unittest.TestCase):
    def setUp(self):
        self.matrix = [
            [0, 0, 1, 1, 0, 0],  # 0
            [1, 0, 0, 1, 0, 1],  # 1
            [1, 1, 1, 1, 0, 1],  # 2
            [0, 1, 0, 1, 0, 0]]  # 3

        self.balls = [(0, 2), (0, 3), (1, 0), (2, 1)]
        self.column_indices = [1, 2, 3, 4, 5, 6]

    def test_columns_as_truncated_balls(self):
        cluster_matrix = cluster_matrix_from_column_indices(self.balls, self.column_indices, self.matrix)
        self.assertEqual([[3, 4, 3, 4],
                          [None, 1, 1, None],
                          [None, None, 2, 2],
                          [None, None, None, None]], cluster_matrix)

    def test_diss_from_cluster_matrix(self):
        cluster_matrix = cluster_matrix_from_column_indices(self.balls, self.column_indices, self.matrix)
        diss_matrix = [[0, 4, 3, 4], [4, 0, 1, 4], [3, 1, 0, 2], [4, 4, 2, 0]]
        self.assertEqual(Diss(range(4)).update(lambda x, y: diss_matrix[x][y]),
                         diss_from_cluster_matrix(cluster_matrix))

    def test_column_indices_from_chordaly_compatible_diss(self):
        diss_matrix = [[0, 1, 3, 2],  # 2
                       [1, 0, 4, 4],  # 1
                       [3, 4, 0, 4],  # 0
                       [2, 4, 4, 0]]  # 3
        diss = Diss(range(4)).update(lambda x, y: diss_matrix[x][y])
        matrix = [
            [0, 0, 1, 1, 0, 0, 1],  # 0
            [1, 0, 0, 1, 0, 1, 0],  # 1
            [1, 1, 1, 1, 0, 1, 0],  # 2
            [0, 1, 0, 1, 0, 0, 0]]  # 3

        column_indices = column_indices_from_chordally_compatible_diss(diss, ContextMatrix(matrix,
                                                                                           elements=(2, 1, 0, 3),
                                                                                           copy_matrix=False))
        self.assertEqual([1, 2, 3, 4, None, 1, 0], column_indices)
