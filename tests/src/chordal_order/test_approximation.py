import unittest

from DLC.chordal_order import chordal_diss_from_fixed_order
from DLC.diss import Diss


class TestApproximationFixedOrder(unittest.TestCase):
    def setUp(self):
        diss_matrix = [
            [0, 1, 1, 1, 2],
            [1, 0, 2, 2, 2],
            [1, 2, 0, 2, 1],
            [1, 2, 2, 0, 1],
            [2, 2, 1, 1, 0]]

        self.diss = Diss(range(5)).update(lambda x, y: diss_matrix[x][y])

    def test_no_changes(self):
        self.diss[2, 3] = 1
        diss_orig = self.diss.copy()
        chordal_diss_from_fixed_order(self.diss, [1, 0, 2, 3, 4])

        self.assertEqual(diss_orig, self.diss)

    def test_one_change(self):
        diss_solution = self.diss.copy()
        diss_solution[2, 3] = 1
        chordal_diss_from_fixed_order(self.diss, [1, 0, 2, 3, 4])

        self.assertEqual(diss_solution, self.diss)

