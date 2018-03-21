import unittest

from tbs.diss import Diss
from tbs.chordal._order_finder import all_min_map_count, order_by_map_partition
from tbs.chordal._order_finder import has_order_by_map
from tbs.chordal._order_finder import init_map_count, min_map_count, update_map_count, order_by_map


class TestOrderByMap(unittest.TestCase):
    def setUp(self):
        self.diss = Diss(["x", "y", "z"]).update_by_pos(
            lambda i, j: [[0],
                          [2, 0],
                          [3, 1, 0]][max(i, j)][min(i, j)])
        self.map_balls = lambda x, y, z: self.diss(y, z) > max(self.diss(x, y), self.diss(x, z)) and 1 or 0

    def test_init_map_count(self):
        self.assertEqual(init_map_count(self.diss, self.map_balls), {"x": 0, "z": 0, "y": 2})

    def test_min_map_count(self):
        self.assertEqual(min_map_count({"x": 0, "y": 1, "z": 2}), "x")

    def test_update_map_count(self):
        map_count = {"x": 0, "z": 0, "y": 2}
        update_map_count("z", map_count, self.map_balls)
        self.assertEqual(map_count, {"x": 0, "y": 0})

    def test_order_by_map(self):
        order = order_by_map(self.diss, self.map_balls)

        self.assertEqual({"x", "y", "z"}, set(order))
        self.assertNotEqual("y", order[0])


class TestOrderByMapPartition(unittest.TestCase):
    def setUp(self):
        self.diss = Diss(["x", "y", "z"]).update_by_pos(
            lambda i, j: [[0],
                          [2, 0],
                          [1, 1, 0]][max(i, j)][min(i, j)])
        self.map_balls = lambda x, y, z: self.diss(y, z) > max(self.diss(x, y), self.diss(x, z)) and 1 or 0

    def test_all_min_map_count(self):
        map_count = init_map_count(self.diss, self.map_balls)
        self.assertEqual(set(all_min_map_count(map_count)), {'x', 'y'})

    def test_order_by_map_partition(self):

        self.assertEqual(order_by_map_partition(self.diss, self.map_balls), [{'x', 'y'}, {'z'}])


class TestHasOrderByMap(unittest.TestCase):
    def test_has_order(self):
        diss = Diss(["x", "y", "z"]).update_by_pos(
            lambda i, j: [[0],
                          [2, 0],
                          [3, 1, 0]][max(i, j)][min(i, j)])
        map_balls = lambda x, y, z: diss(y, z) > max(diss(x, y), diss(x, z)) and 1 or 0

        self.assertTrue(has_order_by_map(diss, map_balls))

    def test_has_not_order(self):
        diss = Diss(["x", "y", "z", "t"]).update_by_pos(
            lambda i, j: [[0],
                          [1, 0],
                          [1, 2, 0],
                          [2, 1, 1, 0]][max(i, j)][min(i, j)])
        map_balls = lambda x, y, z: diss(y, z) > max(diss(x, y), diss(x, z)) and 1 or 0

        self.assertFalse(has_order_by_map(diss, map_balls))
