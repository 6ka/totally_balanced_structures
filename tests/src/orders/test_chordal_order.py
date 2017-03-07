import unittest

from TBS.diss import Diss
from TBS.orders.chordal_order import isa_chordal_order


class TestIsaChordalOrder(unittest.TestCase):
    def setUp(self):
        self.diss = Diss(["x", "y", "z", "t", "u"]).update_by_pos(
            lambda i, j: [[0],
                          [3, 0],
                          [4, 4, 0],
                          [5, 2, 5, 0],
                          [3, 3, 4, 5, 0]][max(i, j)][min(i, j)])
        self.chordal_order = ["x", "z", "t", "y", "u"]

    def test_isa_chordal_order(self):
        self.assertTrue(isa_chordal_order(self.chordal_order, self.diss))

    def test_is_not_a_chordal_order_subset(self):
        self.assertFalse(isa_chordal_order(["x", "z"], self.diss))

    def test_is_not_a_chordal_order(self):
        self.assertFalse(isa_chordal_order(["y", "z", "t", "x", "u"], self.diss))


