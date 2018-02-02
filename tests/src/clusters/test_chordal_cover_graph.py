import unittest

from tbs.clusters.chordal_cover_graph import get_first_non_empty_lines, get_bounds, chordal_matrix_order, is_included, \
    chordal_matrix_cover_graph_from_chordal_matrix_order


class TestInclustionMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix = [[0, 0, 0, 0, 0, 1, 1, 1, 1],
                       [0, 0, 0, 0, 1, 0, 0, 1, 1],
                       [0, 0, 1, 1, 0, 0, 0, 0, 1],
                       [0, 1, 0, 1, 0, 0, 1, 1, 1],
                       [0, 0, 0, 0, 0, 0, 1, 1, 1]]

    def test_get_first_non_empty_lines(self):
        self.assertEqual([-1, 3, 2, 2, 1, 0, 0, 0, 0], get_first_non_empty_lines(self.matrix, empty=0))

    def test_get_bounds(self):
        line_bounds = get_bounds(self.matrix)
        self.assertEqual([[3, 1, 1], [2, 2, 3], [1, 4, 4], [0, 5, 8]], line_bounds)

    def test_get_bounds_different_empty(self):
        self.assertEqual(get_bounds(self.matrix), get_bounds(chordal_matrix_order(self.matrix), empty=None))

    def test_is_included(self):
        self.assertTrue(is_included(2, 3, 8, self.matrix))
        self.assertFalse(is_included(1, 4, 5, self.matrix))

    def test_chordal_matrix_order(self):
        self.assertEqual(chordal_matrix_order(self.matrix),
                         [[None, None, None, None, None, 0,    1,    2,    3],
                          [None, None, None, None, 0,    None, None, 0,    0],
                          [None, None, 0,    1,    None, None, None, None, 1],
                          [None, 0,    None, 0,    None, None, 0,    0,    0],
                          [None, None, None, None, None, None, -1,   -1,  -1]]
                         )

    def test_chordal_matrix_cover_graph_from_chordal_matrix_order(self):
        matrix_chordal = chordal_matrix_cover_graph_from_chordal_matrix_order(chordal_matrix_order(self.matrix))
        self.assertEqual(matrix_chordal,
                         [[None, None, None, None, None, 0,    1,    2,     3],
                          [None, None, None, None, 0,    None, None, 0,    -1],
                          [None, None, 0,    1,    None, None, None, None,  1],
                          [None, 0,    None, 0,    None, None, 0,    -1,   -1],
                          [None, None, None, None, None, None, -1,   -1,   -1]]
                         )