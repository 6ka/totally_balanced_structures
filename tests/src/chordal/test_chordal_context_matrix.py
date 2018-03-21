import unittest

from tbs.chordal._chordal_context_matrix import chordal_clusters, chordal_context_matrix, sort_clusters_by_order
from tbs.diss import Diss


class TestChordalCLusters(unittest.TestCase):
    def setUp(self):
        self.diss = Diss(["x", "y", "z", "t", "u"]).update_by_pos(
            lambda i, j: [[0],
                          [3, 0],
                          [4, 4, 0],
                          [5, 2, 5, 0],
                          [3, 3, 4, 5, 0]][max(i, j)][min(i, j)])
        self.chordal_order = ["x", "z", "t", "y", "u"]

    def test_chordal_cluster(self):
        self.assertEqual({frozenset({'x'}), frozenset({'z'}), frozenset({'t'}), frozenset({'y'}), frozenset({'u'}),
                          frozenset({'x', 'z', 'y', 'u'}),
                          frozenset({'x', 'z', 't', 'y', 'u'}),
                          frozenset({'x', 'y', 'u'}),
                          frozenset({'t', 'y'})},
                         chordal_clusters(self.diss, self.chordal_order)
                         )


class TestChordalContextMatrix(unittest.TestCase):
    def setUp(self):
        self.diss = Diss(["x", "y", "z", "t", "u"]).update_by_pos(
            lambda i, j: [[0],
                          [3, 0],
                          [4, 4, 0],
                          [5, 2, 5, 0],
                          [3, 3, 4, 5, 0]][max(i, j)][min(i, j)])
        self.chordal_order = ("x", "z", "t", "y", "u")

    def test_sort_clusters_by_order(self):
        context_matrix = chordal_context_matrix(self.diss, self.chordal_order)

        self.assertEqual(
            ((0, 0, 0, 0, 0, 1, 1, 1, 1),
             (0, 0, 0, 0, 1, 0, 0, 1, 1),
             (0, 0, 1, 1, 0, 0, 0, 0, 1),
             (0, 1, 0, 1, 0, 0, 1, 1, 1),
             (1, 0, 0, 0, 0, 0, 1, 1, 1)), context_matrix.matrix)
        self.assertEqual(self.chordal_order, context_matrix.elements)


class TestSortClustersWithChordalOrder(unittest.TestCase):
    def setUp(self):
        self.diss = Diss(["x", "y", "z", "t", "u"]).update_by_pos(
            lambda i, j: [[0],
                          [3, 0],
                          [4, 4, 0],
                          [5, 2, 5, 0],
                          [3, 3, 4, 5, 0]][max(i, j)][min(i, j)])
        self.clusters = chordal_clusters(self.diss)

    def test_orders(self):
        sorted_clusters = sort_clusters_by_order(self.clusters, ["x", "z", "t", "y", "u"])
        self.assertEqual(len(self.clusters), sum(len(x) for x in sorted_clusters))
        self.assertEqual(
            [[frozenset({'x'}), frozenset({'y', 'x', 'u'}), frozenset({'y', 'z', 'x', 'u'}),
              frozenset({'y', 'z', 'x', 'u', 't'})],
             [frozenset({'z'})],
             [frozenset({'t'}), frozenset({'y', 't'})],
             [frozenset({'y'})],
             [frozenset({'u'})]],
            sorted_clusters)
