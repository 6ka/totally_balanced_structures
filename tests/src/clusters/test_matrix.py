import unittest

from TBS.graph import Graph

from TBS.clusters.ClusterLineFromMatrix import ClusterLineFromMatrix
from TBS.clusters import from_dlo_gamma_free_matrix


class TestMatrixClusterBase(unittest.TestCase):
    def setUp(self):
        self.matrix = [[1, 0, 0],
                       [1, 0, 0],
                       [1, 1, 1]]

    def test_differences(self):
        cluster_line = ClusterLineFromMatrix(self.matrix)
        self.assertEqual([1, -1, -1], cluster_line.column_difference)

    def test_whole_method(self):
        clusters = from_dlo_gamma_free_matrix.cluster_matrix(self.matrix)
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
        clusters = from_dlo_gamma_free_matrix.cluster_matrix(self.matrix)
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
        clusters = from_dlo_gamma_free_matrix.cluster_matrix(self.matrix)
        boxes = from_dlo_gamma_free_matrix.boxes(self.matrix)

        c1 = clusters[0][0]
        c2 = clusters[1][0]
        c3 = clusters[1][3]
        c4 = clusters[2][3]

        self.assertEqual({c1: ((0, 0), (0, 1)),
                          c2: ((1, 0), (1, 1)),
                          c3: ((1, 3), (1, 3)),
                          c4: ((2, 2), (2, 3))},
                         boxes)

    def test_lattice(self):
        c1 = ((0, 0), (0, 1))
        c2 = ((1, 0), (1, 1))
        c3 = ((1, 3), (1, 3))
        c4 = ((2, 2), (2, 3))

        cover_graph = Graph(directed=True).update([(c1, "TOP"),
                                                   (c3, "TOP"),
                                                   (c2, c1),
                                                   (c2, c3),
                                                   (c4, c3),
                                                   ("BOTTOM", c2),
                                                   ("BOTTOM", c4)])

        self.assertEqual(cover_graph, from_dlo_gamma_free_matrix.lattice(self.matrix))