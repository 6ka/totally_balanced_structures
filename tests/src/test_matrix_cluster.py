__author__ = 'fbrucker'


import unittest

from clusters import cluster_matrix


class TestMatrixCluster(unittest.TestCase):
    def test_only_column(self):
        matrix = [[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]]
        clusters = cluster_matrix(matrix)
        self.assertEqual([[5, None, None], [None, 4, None], [None, None, 3]], clusters)

    def test_several_for_one_column(self):
        matrix = [[1, 0],
                  [0, 1],
                  [1, 0]]
        clusters = cluster_matrix(matrix)
        self.assertEqual([[4, None], [None, 3], [5, None]], clusters)

    def test_intersection(self):
        matrix = [[1, 0, 0],
                  [1, 1, 0],
                  [1, 1, 1]]
        clusters = cluster_matrix(matrix)
        self.assertEqual([[7, None, None], [6, 5, None], [6, 4, 3]], clusters)
