import unittest

from TBS.contextmatrix import ContextMatrix
from TBS.clusters import to_string

__author__ = 'francois'


class TestToString(unittest.TestCase):
    def setUp(self):
        matrix = [[1, 0, 0, 0, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [0, 1, 0, 0, 1, 1],
                  [0, 0, 1, 1, 0, 1],
                  [0, 0, 0, 1, 0, 1]]
        self.context_matrix = ContextMatrix(matrix)
        self.context_matrix.reorder([3, 4, 2, 1, 0], [3, 2, 0, 1, 4, 5])

    def test_from_context_matrix(self):
        string_repr = to_string.from_dlo_gamma_free_context_matrix(self.context_matrix)

        result = " |2 3 1 0 4 5 " + "\n" + \
                 "-+-+-+-+-+-+-+" + "\n" + \
                 "4|.|3|-----| |" + "\n" + \
                 " +---+     |5|" + "\n" + \
                 "3| 2 |. . .| |" + "\n" + \
                 " +---+-+ +---+" + "\n" + \
                 "2|.|.|1|-| 4 |" + "\n" + \
                 " + | +-+-----+" + "\n" + \
                 "0|.|. ||  0  |" + "\n" + \
                 " +-----------+" + "\n" + \
                 "1|     2     |" + "\n" + \
                 " +-----------+"

        self.assertEqual(string_repr, result)

# def test_from_matrix(self):
#     string_repr = to_string.raw_matrix(self.context_matrix.matrix)
#     # print(string_repr)
