import unittest

from TBS.totally_balanced_diss.chordal_diss import approximate_chordal_diss, isa_chordal_diss
from TBS.diss import Diss
from TBS.contextmatrix import ContextMatrix


class TestIsaChordalDiss(unittest.TestCase):
    def test_isa_chordal_diss(self):
        diss = Diss(["x", "y", "z", "t", "u"]).update_by_pos(
            lambda i, j: [[0],
                          [3, 0],
                          [4, 4, 0],
                          [5, 2, 5, 0],
                          [3, 3, 4, 5, 0]][max(i, j)][min(i, j)])

        self.assertTrue(isa_chordal_diss(diss))

    def test_is_not_a_chordal_diss(self):
        diss = Diss(["x", "y", "z", "t"]).update_by_pos(
            lambda i, j: [[0],
                          [1, 0],
                          [1, 2, 0],
                          [2, 1, 1, 0]][max(i, j)][min(i, j)])
        self.assertFalse(isa_chordal_diss(diss))


class TestChordalApproximation(unittest.TestCase):
    def test_chordal_diss(self):
        diss = Diss(["x", "y", "z", "t"]).update_by_pos(
            lambda i, j: [[0],
                          [1, 0],
                          [1, 2, 0],
                          [2, 1, 1, 0]][max(i, j)][min(i, j)])

        self.assertEqual(approximate_chordal_diss(diss, ["x", "y", "z", "t"]),
                         Diss(["x", "y", "z", "t"]).update_by_pos(
                             lambda i, j: [[0],
                                           [1, 0],
                                           [1, 1, 0],
                                           [2, 1, 1, 0]][max(i, j)][min(i, j)]))
