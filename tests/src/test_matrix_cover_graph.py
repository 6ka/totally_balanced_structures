__author__ = 'fbrucker'

import unittest

from DLC.clusters.cover_graph import cover_graph_from_matrix, cover_graph_and_boxes_from_matrix
from DLC.clusters import cluster_matrix_from_O1_matrix
from DLC.graph import Graph


class TestProgressMethods(unittest.TestCase):
    def setUp(self):
        self.clusters = [[None,    1,    2, None, None],
                         [   3,    3,    2, None, None],
                         [None, None, None,    4, None],
                         [None, None,    5,    5, None],
                         [   6,    6, None, None,    7],
                         [None, None,    8,    8,    8]]


class TestCoverGraphFromClusters(unittest.TestCase):
    def setUp(self):
        self.matrix = [[0, 1, 1, 0, 0],
                       [1, 1, 1, 0, 0],
                       [0, 0, 0, 1, 0],
                       [0, 0, 1, 1, 0],
                       [1, 1, 0, 0, 1],
                       [0, 0, 1, 1, 1]]

        self.clusters = cluster_matrix_from_O1_matrix(self.matrix)

    def test_clusters(self):
        c1 = self.clusters[0][1]
        c2 = self.clusters[0][2]
        c3 = self.clusters[1][0]
        c4 = self.clusters[2][3]
        c5 = self.clusters[3][3]
        c6 = self.clusters[4][0]
        c7 = self.clusters[4][4]
        c8 = self.clusters[5][2]

        real_clusters = [[None,   c1,   c2, None, None],
                         [c3,     c3,   c2, None, None],
                         [None, None, None,   c4, None],
                         [None, None,   c5,   c5, None],
                         [c6,     c6, None, None,   c7],
                         [None, None,   c8,   c8,   c8]]

        self.assertEqual(real_clusters, self.clusters)

    def test_cover_graph_and_boxes_from_matrix(self):
        c1 = self.clusters[0][1]
        c2 = self.clusters[0][2]
        c3 = self.clusters[1][0]
        c4 = self.clusters[2][3]
        c5 = self.clusters[3][3]
        c6 = self.clusters[4][0]
        c7 = self.clusters[4][4]
        c8 = self.clusters[5][2]
        cover_graph, boxes_i, boxes_j = cover_graph_and_boxes_from_matrix(self.matrix)
        self.assertEqual(
            {c1: (0, 0), c2: (0, 1), c3: (1, 1), c4: (2, 2), c5: (3, 3), c6: (4, 4), c7: (4, 4), c8: (5, 5)},
            boxes_i)
        self.assertEqual(
            {c1: (1, 1), c2: (2, 2), c3: (0, 1), c4: (3, 3), c5: (2, 3), c6: (0, 1), c7: (4, 4), c8: (2, 4)},
            boxes_j)

    def test_cover_graph_from_matrix(self):
        c1 = self.clusters[0][1]
        c2 = self.clusters[0][2]
        c3 = self.clusters[1][0]
        c4 = self.clusters[2][3]
        c5 = self.clusters[3][3]
        c6 = self.clusters[4][0]
        c7 = self.clusters[4][4]
        c8 = self.clusters[5][2]

        cover_graph = Graph(directed=True).update([(c1, c2),
                                                   (c2, "TOP"),
                                                   (c3, c1),
                                                   (c4, "TOP"),
                                                   (c5, c2),
                                                   (c5, c4),
                                                   (c6, c3),
                                                   (c6, c7),
                                                   (c7, "TOP"),
                                                   (c8, c5),
                                                   (c8, c7),
                                                   ("BOTTOM", c8),
                                                   ("BOTTOM", c6)])
        self.assertEqual(cover_graph, cover_graph_from_matrix(self.matrix))