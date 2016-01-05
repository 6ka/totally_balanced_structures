import unittest

from DLC.diss import Diss

import DLC.cluster_order
from DLC.cluster_order import ClusterOrder

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
        cluster_order = DLC.cluster_order.from_diss_as_list_of_sets(self.diss)
        self.assertEqual([{1, 3}, {0, 2}], cluster_order)

    def test_order(self):
        cluster_order = DLC.cluster_order.from_diss(self.diss)
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
        cluster_order = DLC.cluster_order.from_diss_as_list_of_sets(diss)
        self.assertEqual([], cluster_order)

