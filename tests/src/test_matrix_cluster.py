__author__ = 'fbrucker'

import unittest

from DLC.clusters.clusters import cluster_matrix_from_O1_matrix, cluster_matrix_and_boxes_from_O1_matrix, \
    atom_clusters_correspondence, ClusterLineFromMatrix

from DLC.clusters.to_string import clusters_to_string
from DLC.contextmatrix import ContextMatrix


class TestMatrixClusterBase(unittest.TestCase):
    def setUp(self):
        self.matrix = [[1, 0, 0],
                       [1, 0, 0],
                       [1, 1, 1]]

    def test_differences(self):
        cluster_line = ClusterLineFromMatrix(self.matrix)
        self.assertEqual([1, -1, -1], cluster_line.column_difference)

    def test_whole_method(self):
        clusters = cluster_matrix_from_O1_matrix(self.matrix)
        c1 = clusters[0][0]
        self.assertIsNotNone(c1)
        c2 = clusters[2][0]
        self.assertIsNotNone(c2)
        self.assertNotEqual(c1, c2)

        self.assertEqual([[c1, None, None], [c1, None, None], [c2, c2, c2]], clusters)


class TestMatrixClusterAndBoxes(unittest.TestCase):

    def setUp(self):
        self.matrix = [[1, 1, 0, 0],
                       [1, 1, 0, 1],
                       [0, 0, 1, 1]]

    def test_clusters(self):
        clusters = cluster_matrix_from_O1_matrix(self.matrix)
        c1 = clusters[0][0]
        self.assertIsNotNone(c1)
        c2 = clusters[1][0]
        self.assertIsNotNone(c2)
        c3 = clusters[1][3]
        self.assertIsNotNone(c3)
        c4 = clusters[2][3]
        self.assertEqual(4, len({c1, c2, c3, c4}))
        self.assertEqual([[c1, c1, None, None], [c2, c2, None, c3], [None, None, c4, c4]], clusters)

    def test_boxes(self):
        clusters, boxes_i, boxes_j = cluster_matrix_and_boxes_from_O1_matrix(self.matrix)
        c1 = clusters[0][0]
        c2 = clusters[1][0]
        c3 = clusters[1][3]
        c4 = clusters[2][3]

        self.assertEqual({c1: (0, 0), c2: (1, 1), c3: (1, 1), c4: (2, 2)}, boxes_i)
        self.assertEqual({c1: (0, 1), c2: (0, 1), c3: (3, 3), c4: (2, 3)}, boxes_j)


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