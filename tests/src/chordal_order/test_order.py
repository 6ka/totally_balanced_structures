import unittest

from DLC.diss import Diss

import DLC.chordal_order
from DLC.chordal_order.order import ClusterOrder

__author__ = 'fbrucker'


class TestClusterOrder(unittest.TestCase):
    def setUp(self):
        diss_matrix = [
            # 0  1  2  3
            [0, 1, 1, 1],  # 0
            [1, 0, 1, 2],  # 1
            [1, 1, 0, 1],  # 2
            [1, 2, 1, 0]]  # 3
        self.diss = Diss(range(4)).update(lambda x, y: diss_matrix[x][y])

    def test_init(self):
        self.assertEqual({0: 2, 1: 0, 2: 2, 3: 0}, ClusterOrder(self.diss).delta)

    def test_update(self):
        triplets = ClusterOrder(self.diss)
        triplets._update_delta(1)
        self.assertEqual({0: 0, 2: 0, 3: 0}, triplets.delta)

    def test_order_as_list_of_sets(self):
        cluster_order = DLC.chordal_order.from_diss_as_list_of_sets(self.diss)
        self.assertEqual([{1, 3}, {0, 2}], cluster_order)

    def test_order(self):
        cluster_order = DLC.chordal_order.from_diss(self.diss)
        self.assertEqual(4, len(set(cluster_order)))
        self.assertEqual({1, 3}, {cluster_order[0], cluster_order[1]})
        self.assertEqual({0, 2}, {cluster_order[2], cluster_order[3]})

    def test_no_cluster_order(self):
        diss_matrix = [
            # 0  1  2  3
            [0, 1, 2, 1],  # 0
            [1, 0, 1, 2],  # 1
            [2, 1, 0, 1],  # 2
            [1, 2, 1, 0]]  # 3

        diss = Diss(range(4)).update(lambda x, y: diss_matrix[x][y])
        self.assertEqual({0: 2, 1: 2, 2: 2, 3: 2}, ClusterOrder(diss)._init_non_hierarchical_triplets())
        cluster_order = DLC.chordal_order.from_diss_as_list_of_sets(diss)
        self.assertEqual([], cluster_order)

    def test_isa_order(self):
        self.assertTrue(DLC.chordal_order.is_compatible_for_diss([1, 0, 2, 3], self.diss))
        self.assertFalse(DLC.chordal_order.is_compatible_for_diss([0, 1, 2, 3], self.diss))

    def test_3_value_dissimilarity(self):
        diss_matrix = [
            # 0  1  2  3
            [0, 1, 1, 2],  # 0
            [1, 0, 1, 3],  # 1
            [1, 1, 0, 2],  # 2
            [2, 3, 2, 0]]  # 3
        diss = Diss(range(4)).update(lambda x, y: diss_matrix[x][y])
        self.assertTrue(DLC.chordal_order.is_compatible_for_diss([1, 2, 0, 3], diss))


class TestApproximateChordalOrder(unittest.TestCase):
    def setUp(self):
        diss_matrix = [
            [0, 1, 1, 1, 2],
            [1, 0, 2, 2, 2],
            [1, 2, 0, 2, 1],
            [1, 2, 2, 0, 1],
            [2, 2, 1, 1, 0]]

        diss = Diss(range(5)).update(lambda x, y: diss_matrix[x][y])
        self.cluster_order = ClusterOrder(diss)

    def test_delta(self):
        self.assertEqual({0: 6, 1: 0, 2: 2, 3: 2, 4: 2}, self.cluster_order.delta)

    def test_min_decomposition(self):
        self.assertEqual({1}, self.cluster_order.next_min())
        self.cluster_order._update_delta(1)
        self.assertIn(self.cluster_order.next_min().pop(), {0, 2, 3, 4})
