import unittest

from DLC import graphics
from DLC.contextmatrix import ContextMatrix

__author__ = 'francois'


class TestToString(unittest.TestCase):
    def setUp(self):
        matrix = [[1, 0, 0, 0, 1],
                  [1, 1, 1, 1, 1],
                  [0, 1, 0, 0, 1],
                  [0, 0, 1, 1, 0],
                  [0, 0, 0, 1, 0]]
        self.context_matrix = ContextMatrix(matrix)
        self.context_matrix.reorder_doubly_lexical_order()

    def test_from_context_matrix(self):
        string_repr = graphics.from_context_matrix(self.context_matrix)
        # print(string_repr)

    def test_from_matrix(self):
        string_repr = graphics.raw_matrix(self.context_matrix.matrix)
        # print(string_repr)