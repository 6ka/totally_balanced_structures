import unittest

from tbs.dismantlable import DismantlableLattice
from tbs.graph import DirectedGraph

from tbs.gamma_free import GammaFree
from tbs.gamma_free._box_lattice import ClusterLineFromMatrix, box_lattice


class TestMatrixClusterBase(unittest.TestCase):
    def setUp(self):
        self.matrix = [[1, 0, 0],
                       [1, 0, 0],
                       [1, 1, 1]]

    def test_differences(self):
        cluster_line = ClusterLineFromMatrix(self.matrix)

        self.assertEqual([1, -1, 1, -1], cluster_line.column_difference)

    def test_whole_method(self):
        clusters = ClusterLineFromMatrix.box_matrix(self.matrix)
        c1 = clusters[0][0]
        self.assertEqual(((0, 0), (1, 0)), c1)
        c2 = clusters[-1][0]
        self.assertEqual(((2, 0), (3, 3)), c2)
        c3 = clusters[0][-1]
        self.assertEqual(((0, 3), (1, 3)), c3)

        self.assertEqual(((c1, None, None, c3), (c1, None, None, c3), (c2, c2, c2, c2), (c2, c2, c2, c2)), clusters)


class TestMatrixClusterAndBoxes(unittest.TestCase):

    def setUp(self):
        self.matrix = [[1, 1, 0, 0],
                       [1, 1, 0, 1],
                       [0, 0, 1, 1]]

    def test_clusters(self):
        clusters = ClusterLineFromMatrix.box_matrix(self.matrix)

        c1 = clusters[0][0]
        self.assertEqual(((0, 0), (0, 1)), c1)
        c2 = clusters[1][0]
        self.assertEqual(((1, 0), (1, 1)), c2)
        c3 = clusters[1][3]
        self.assertEqual(((1, 3), (1, 4)), c3)
        c4 = clusters[2][3]
        self.assertEqual(((2, 2), (2, 4)), c4)
        c5 = clusters[0][-1]
        self.assertEqual(((0, 4), (0, 4)), c5)
        c6 = clusters[-1][0]
        self.assertEqual(((3, 0), (3, 4)), c6)
        self.assertEqual(6, len({c1, c2, c3, c4, c5, c6}))

        self.assertEqual(((c1, c1, None, None, c5),
                          (c2, c2, None, c3, c3),
                          (None, None, c4, c4, c4),
                          (c6, c6, c6, c6, c6)), clusters)

    def test_lattice(self):
        c1 = ((0, 0), (0, 1))
        c2 = ((1, 0), (1, 1))
        c3 = ((1, 3), (1, 4))
        c4 = ((2, 2), (2, 4))
        t = ((0, 4), (0, 4))
        b = ((3, 0), (3, 4))

        lattice = box_lattice(GammaFree(self.matrix))
        self.assertEqual(frozenset([c1, c2, c3, c4, t, b]), frozenset(lattice))

        self.assertEqual(
            DismantlableLattice(DirectedGraph.from_edges([(b, c4), (b, c2),
                                                          (c4, c3), (c3, t),
                                                          (c2, c1), (c2, c3),
                                                          (c1, t)])),
            lattice)