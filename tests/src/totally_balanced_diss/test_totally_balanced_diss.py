import unittest

from tbs.diss import Diss
from tbs.graph import cls
from tbs.totally_balanced_diss.chordal_diss import isa_chordal_diss
from tbs.totally_balanced_diss.totally_balanced_diss import isa_totally_balanced_diss, \
    approximation_totally_balanced_diss, isa_strongly_chordal_graph


class TestIsaStronglyChordalGraph(unittest.TestCase):
    def test_isa_strongly_chordal_graph(self):
        g = cls(edges=((1, 2), (2, 3)))
        self.assertTrue(isa_strongly_chordal_graph(g))

        g = cls(edges=((1, 4), (1, 5),
                       (2, 5), (2, 6),
                       (3, 4), (3, 6),
                       (4, 5), (5, 6), (6, 4)))
        self.assertFalse(isa_strongly_chordal_graph(g))


class TestIsaTotallyBalancedDiss(unittest.TestCase):
    def test_is_totally_balanced_cycle(self):
        diss = Diss(["x", "y", "z", "t"]).update_by_pos(
            lambda i, j: [[0],
                          [1, 0],
                          [1, 2, 0],
                          [2, 1, 1, 0]][max(i, j)][min(i, j)])
        self.assertFalse(isa_totally_balanced_diss(diss))

    def test_not_totally_balanced_but_chordal(self):
        diss = Diss(["x", "y", "z", "t"]).update_by_pos(
            lambda i, j: [[0],
                          [2, 0],
                          [2, 2, 0],
                          [3, 1, 1, 0]][max(i, j)][min(i, j)])
        self.assertTrue(isa_chordal_diss(diss))
        self.assertFalse(isa_totally_balanced_diss(diss))


class TestApproximateTotallyBalanced(unittest.TestCase):
    def test_no_modification(self):
        diss = Diss(["x", "y", "z", "t", "u"]).update_by_pos(
            lambda i, j: [[0],
                          [3, 0],
                          [4, 4, 0],
                          [5, 2, 5, 0],
                          [3, 3, 4, 5, 0]][max(i, j)][min(i, j)])
        self.assertTrue(isa_totally_balanced_diss(diss))
        self.assertEqual(diss, approximation_totally_balanced_diss(diss))

    def test_compatible_order_not_strongly_compatible(self):
        diss = Diss(["x", "y", "z", "t", "u"]).update_by_pos(
            lambda i, j: [[0],
                          [3, 0],
                          [4, 4, 0],
                          [5, 2, 5, 0],
                          [3, 3, 4, 5, 0]][max(i, j)][min(i, j)])

        self.assertEqual(diss, approximation_totally_balanced_diss(diss, ['u', 'z', 'x', 'y', 't']))

    def test_modif(self):
        diss = Diss(["x", "y", "z", "t"]).update_by_pos(
            lambda i, j: [[0],
                          [2, 0],
                          [2, 2, 0],
                          [3, 1, 1, 0]][max(i, j)][min(i, j)])

        diss_approximate = approximation_totally_balanced_diss(diss)
        self.assertNotEqual(diss, diss_approximate)
        self.assertFalse(isa_totally_balanced_diss(diss))
        self.assertTrue(isa_totally_balanced_diss(diss_approximate))
