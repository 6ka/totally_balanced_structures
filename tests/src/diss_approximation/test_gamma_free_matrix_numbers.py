import unittest

from contextmatrix import ContextMatrix
from DLC.diss_approximation.gamma_free_matrix_numbers import down_number_matrix, up_number_matrix, add_line_true_to_count


class TestUpAndDown(unittest.TestCase):
    def setUp(self):
        matrix = [
            # 0  1  2  3
            [0, 0, 1, 1, 0],  # 0
            [1, 0, 0, 1, 0],  # 1
            [1, 1, 1, 1, 0],  # 2
            [0, 1, 0, 1, 0]]  # 3
        self.context_matrix = ContextMatrix(matrix)

    def test_down_numbers(self):
        down_numbers = down_number_matrix(self.context_matrix.matrix)
        self.assertEqual([2, 2, 2, 4, 0], down_numbers[0])
        for line in range(4):
            self.assertEqual(4 - line, down_numbers[line][3])

    def test_up_numbers(self):
        up_numbers = up_number_matrix(self.context_matrix.matrix)
        self.assertEqual([0] * len(self.context_matrix.matrix[0]), up_numbers[0])

        for line in range(4):
            self.assertEqual(line, up_numbers[line][3])

    def test_add_line_to_count(self):
        line = [0, 1, 0]
        count = [1, 4, 6]
        add_line_true_to_count(line, count)
        self.assertEqual([0, 1, 0], line)
        self.assertEqual([1, 5, 6], count)