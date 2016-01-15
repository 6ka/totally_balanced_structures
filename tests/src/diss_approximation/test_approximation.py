import unittest
import random

from DLC.diss import Diss
from DLC.diss_approximation.approximation import totally_balanced_dissimilarity, \
    totally_balanced_dissimilarity_for_order


class TestApproximationNoApproximation(unittest.TestCase):
    def setUp(self):
        diss_matrix = [
            [0, 4, 1, 1, 2],  # 0
            [4, 0, 2, 1, 3],  # 1
            [1, 2, 0, 1, 2],  # 2
            [1, 1, 1, 0, 1],  # 3
            [2, 3, 2, 1, 0]]  # 4

        self.diss = Diss(range(5)).update(lambda x, y: diss_matrix[x][y])

    def test_approximation(self):
        approximated_diss = totally_balanced_dissimilarity(self.diss)
        self.assertEqual(self.diss, approximated_diss)

    def test_approximation_fixed_order_no_approximation(self):
        approximated_diss = totally_balanced_dissimilarity_for_order(self.diss, [0, 4, 2, 1, 3])

        self.assertEqual(self.diss, approximated_diss)


class TestApproximation(unittest.TestCase):
    def setUp(self):
        diss_matrix = [
            [0, 1, 1, 1, 1, 2],  # 0
            [1, 0, 1, 1, 2, 1],  # 1
            [1, 1, 0, 2, 1, 1],  # 2
            [1, 1, 2, 0, 2, 2],  # 3
            [1, 2, 1, 1, 0, 2],  # 4
            [2, 1, 1, 2, 2, 0]]  # 5

        self.diss = Diss(range(6)).update(lambda x, y: diss_matrix[x][y])

    def test_approximation(self):
        approximated_diss = totally_balanced_dissimilarity(self.diss)
        self.assertNotEqual(self.diss, approximated_diss)

    def test_approximation_fixed_order_no_approximation(self):
        approximated_diss = Diss(range(6)).update(
            totally_balanced_dissimilarity_for_order(self.diss, [3, 4, 5, 0, 1, 2]))
        self.assertNotEqual(self.diss, approximated_diss)


class TestApproximationRandom(unittest.TestCase):

    def test_random(self):
        for step in range(20):
            diss = Diss(range(20)).update(lambda x, y: random.randint(1, 20))
            approximate_diss = totally_balanced_dissimilarity(diss)
            self.assertEqual(approximate_diss, totally_balanced_dissimilarity(approximate_diss))


