__author__ = 'fbrucker'

import unittest

from DLC.clusters.clusters import cluster_matrix, column_difference_matrix, refine_same_clusters, \
    cluster_matrix_from_O1_matrix, boxes_clusters, atom_clusters_correspondence

from DLC.clusters.to_string import clusters_to_string
from DLC.contextmatrix import ContextMatrix


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


class TestMatrixClusterBoxes(unittest.TestCase):

    def setUp(self):
        self.matrix = [[1, 1, 0, 0],
                       [1, 1, 0, 1],
                       [0, 0, 1, 1]]

    def test_clusters(self):
        clusters = cluster_matrix(self.matrix)
        self.assertEqual([[9, 7, None, None], [8, 4, None, 3], [None, None, 6, 3]], clusters)

    def test_refine(self):
        clusters = cluster_matrix(self.matrix)
        refine_same_clusters(self.matrix, clusters)
        self.assertEqual([[9, 9, None, None], [8, 8, None, 3], [None, None, 6, 6]], clusters)

    def test_boxes(self):
        clusters = cluster_matrix_from_O1_matrix(self.matrix)
        boxes_i, boxes_j = boxes_clusters(clusters)
        self.assertEqual({8: (1, 1), 9: (0, 0), 3: (1, 1), 6: (2, 2)}, boxes_i)
        self.assertEqual({8: (0, 1), 9: (0, 1), 3: (3, 3), 6: (2, 3)}, boxes_j)


class TestAtomClusters(unittest.TestCase):
    def setUp(self):
        self.clusters = [[None, None, 3], [None, 4, 4], [5, 5, 5]]

    def test_atom_clusters(self):
        number_to_cluster, cluster_to_number = atom_clusters_correspondence(self.clusters)
        self.assertEqual({3: frozenset({0, 1, 2}), 4: frozenset({1, 2}), 5: frozenset({2})}, number_to_cluster)
        self.assertEqual({frozenset({1, 2}): 4, frozenset({0, 1, 2}): 3, frozenset({2}): 5}, cluster_to_number)

    def test_atom_clusters_with_rename(self):
        number_to_cluster, cluster_to_number = atom_clusters_correspondence(self.clusters, ["a", "b", "c"])
        self.assertEqual({3: frozenset({"a", "b", "c"}), 4: frozenset({"b", "c"}), 5: frozenset({"c"})}, number_to_cluster)
        self.assertEqual({frozenset({"b", "c"}): 4, frozenset({"a", "b", "c"}): 3, frozenset({"c"}): 5}, cluster_to_number)


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