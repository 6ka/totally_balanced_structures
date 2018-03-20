import unittest

from tbs.gamma_free._gamma_free import GammaFree, gamma_free_matrix_top_down, gamma_free_matrix_bottom_up
from tbs.contextmatrix import ContextMatrix


class TestIsGammaFree(unittest.TestCase):
    def setUp(self):
        self.matrix = [[0, 1, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1]]

    def test_isa_false(self):
        self.assertFalse(gamma_free_matrix_top_down(self.matrix))
        self.assertFalse(gamma_free_matrix_bottom_up(self.matrix))

    def test_isa_true(self):
        self.matrix[1][2] = 1
        self.assertTrue(gamma_free_matrix_top_down(self.matrix))
        self.assertTrue(gamma_free_matrix_bottom_up(self.matrix))

    def test_transform(self):
        gamma_free_matrix_top_down(self.matrix, True)
        self.assertTrue(gamma_free_matrix_top_down(self.matrix))
        self.assertEqual([[0, 1, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]], self.matrix)

    def test_transform_bottom_up_delete_right(self):
        gamma_free_matrix_bottom_up(self.matrix, True)
        self.assertTrue(gamma_free_matrix_bottom_up(self.matrix))
        self.assertEqual([[0, 1, 0, 0], [0, 1, 0, 1], [0, 0, 1, 1]], self.matrix)


class TestLimitCaseBottomUp(unittest.TestCase):
    def test_0_and_propagate(self):
        matrix = [[1, 1, 0, 1, 0],
                  [1, 0, 1, 0, 1],
                  [0, 0, 0, 1, 1]]
        self.assertFalse(gamma_free_matrix_bottom_up(matrix))
        gamma_free_matrix_bottom_up(matrix, True)
        self.assertTrue(gamma_free_matrix_bottom_up(matrix))


class TestContextMatrixApproximation(unittest.TestCase):
    def setUp(self):
        self.context_matrix = ContextMatrix([[1, 1, 0], [1, 0, 1], [0, 1, 1]])

    def test_context_matrix_approximation(self):
        context_matrix = GammaFree.from_approximation(self.context_matrix)
        self.assertTrue(context_matrix.is_gamma_free())
        self.assertEqual(1, context_matrix.matrix[1][1])
