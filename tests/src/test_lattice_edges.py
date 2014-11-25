__author__ = 'fbrucker'

import unittest

from clusters.clusters import cluster_matrix, column_difference_matrix, rafine_same_clusters, \
    cluster_matrix_from_O1_matrix, boxes_clusters
from clusters.to_string import clusters_to_string
from contextmatrix import ContextMatrix

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


class TestMatrixCluster(unittest.TestCase):
    def setUp(self):
        self.matrix = [[1, 0, 0],
                       [1, 0, 0],
                       [1, 1, 1]]

    def test_differences(self):
        column_difference = column_difference_matrix(self.matrix)
        self.assertEqual([1, -1, -1], column_difference)

    def test_whole_method(self):
        clusters = cluster_matrix_from_O1_matrix(self.matrix)
        self.assertEqual([[6, None, None], [6, None, None], [5, 5, 5]], clusters)


class TestMaxtrixClusterBoxes(unittest.TestCase):
    def setUp(self):
        self.matrix = [[0, 0, 1],
                       [0, 1, 1],
                       [1, 1, 1]]

    def test_rafine_clusters_propagate(self):
        clusters = cluster_matrix(self.matrix)
        rafine_same_clusters(self.matrix, clusters)
        self.assertEqual([[None, None, 3], [None, 4, 4], [5, 5, 5]], clusters)

    def test_boxes(self):
        clusters = cluster_matrix_from_O1_matrix(self.matrix)
        boxes_i, boxes_j = boxes_clusters(clusters)
        self.assertEqual({3: (0, 0), 4: (1, 1), 5: (2, 2)}, boxes_i)
        self.assertEqual({3: (2, 2), 4: (1, 2), 5: (0, 2)}, boxes_j)


class TestToString(unittest.TestCase):
    def setUp(self):
        matrix = [[1, 0, 0, 0, 1],
                  [1, 1, 1, 1, 1],
                  [0, 1, 0, 0, 1],
                  [0, 0, 1, 1, 0],
                  [0, 0, 0, 1, 0]]
        self.context_matrix = ContextMatrix(matrix)
        self.context_matrix.reorder_doubly_lexical_order()

    # def test_to_string(self):
    #
    #     clusters = cluster_matrix_from_O1_matrix(self.context_matrix.matrix)
    #     print(clusters_to_string(clusters, self.context_matrix.elements, self.context_matrix.attributes))
