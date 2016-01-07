import unittest

from DLC.diss import Diss

from DLC.chordal_order.clusters import Balls, clusters_from_order

__author__ = 'fbrucker'


class TestBalls(unittest.TestCase):
    def setUp(self):
        diss_matrix = [
            # 0  1  2  3
            [0, 1, 1, 1],  # 0
            [1, 0, 1, 2],  # 1
            [1, 1, 0, 1],  # 2
            [1, 2, 1, 0]]  # 3
        self.diss = Diss(range(4)).update(lambda x, y: diss_matrix[x][y])

    def test_singleton(self):
        self.assertEqual({0}, Balls(self.diss)(0, 0))

    def test_whole_set(self):
        self.assertEqual(set(range(4)), Balls(self.diss)(0, 42))

    def test_a_ball(self):
        self.assertEqual(set(range(3)), Balls(self.diss)(1, 1.5))

    def test_base_set(self):
        self.assertEqual(set(range(3)), Balls(self.diss)(0, 42, [0, 1, 2]))


class TestClusters(unittest.TestCase):
    def setUp(self):
        diss_matrix = [
            # 0  1  2  3
            [0, 1, 1, 2],  # 0
            [1, 0, 1, 3],  # 1
            [1, 1, 0, 2],  # 2
            [2, 3, 2, 0]]  # 3
        self.diss = Diss(range(4)).update(lambda x, y: diss_matrix[x][y])
        self.chordal_order = [1, 2, 0, 3]

    def test_clusters(self):
        clusters = clusters_from_order(self.diss, self.chordal_order)
        self.assertEqual({frozenset({0, 2, 3}), frozenset({3}), frozenset({0}), frozenset({0, 1, 2, 3}),
                          frozenset({1}), frozenset({0, 1, 2}), frozenset({2})}, clusters)
