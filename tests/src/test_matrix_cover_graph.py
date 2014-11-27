__author__ = 'fbrucker'

import unittest

from DLC.clusters.cover_graph import pred_cluster_line, next_cluster_column, matrix_atoms, cover_graph_from_clusters
from DLC.graph import Graph


class TestProgressMethods(unittest.TestCase):
    def setUp(self):
        self.clusters = [[None,    1,    2, None, None],
                         [   3,    3,    2, None, None],
                         [None, None, None,    4, None],
                         [None, None,    5,    5, None],
                         [   6,    6, None, None,    7],
                         [None, None,    8,    8,    8]
                         ]

    def test_next_cluster_column(self):
        self.assertEqual(7, next_cluster_column(4, 1, self.clusters))
        self.assertIsNone(next_cluster_column(0, 2, self.clusters))

    def test_pred_cluster_line(self):
        self.assertEqual(3, pred_cluster_line(4, 1, self.clusters))
        self.assertIsNone(pred_cluster_line(1, 0, self.clusters))

    def test_pred_cluster_line_border(self):
        self.assertIsNone(pred_cluster_line(1, -1, self.clusters))

    def test_matrix_atoms(self):
        self.assertEqual({8, 6}, matrix_atoms(self.clusters))


class TestCoverGraphFromClusters(unittest.TestCase):
    def setUp(self):
        self.clusters = [[None,    1,    2, None, None],
                         [   3,    3,    2, None, None],
                         [None, None, None,    4, None],
                         [None, None,    5,    5, None],
                         [   6,    6, None, None,    7],
                         [None, None,    8,    8,    8]]

    def test_cover_graph_from_clusters(self):
        cover_graph = Graph(directed=True).update([(1, 2),
                                                   (2, "TOP"),
                                                   (3, 1),
                                                   (4, "TOP"),
                                                   (5, 2),
                                                   (5, 4),
                                                   (6, 3),
                                                   (6, 7),
                                                   (7, "TOP"),
                                                   (8, 5),
                                                   (8, 7),
                                                   ("BOTTOM", 8),
                                                   ("BOTTOM", 6)])

        self.assertEqual(cover_graph, cover_graph_from_clusters(self.clusters))