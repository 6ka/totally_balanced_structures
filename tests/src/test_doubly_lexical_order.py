__author__ = 'fbrucker'

import unittest
from doubly_lexical_order import Node, ColumnBlock, RowBlock, row_ordering_from_last_row_block, \
    column_ordering_from_last_column_block, doubly_lexical_order, is_doubly_lexical_ordered, gamma_free_matrix

class TestNode(unittest.TestCase):
    def test_add_node_pred(self):
        node = Node()
        node_left = Node()
        node.add_pred(node_left)
        self.assertEqual(node_left.next, node)
        self.assertEqual(node.pred, node_left)
        self.assertIsNone(node.next)
        self.assertIsNone(node_left.pred)

    def test_add_node_pred_not_None(self):
        node = Node()
        node_left = Node()
        node.add_pred(node_left)

        node_insert = Node()
        node.add_pred(node_insert)
        self.assertEqual(node_left.next, node_insert)
        self.assertEqual(node_insert.pred, node_left)

    def test_add_node_next(self):
        node = Node()
        node_right = Node()
        node.add_next(node_right)
        self.assertEqual(node_right.pred, node)
        self.assertEqual(node.next, node_right)
        self.assertIsNone(node.pred)
        self.assertIsNone(node_right.next)

    def test_add_node_next_not_None(self):
        node = Node()
        node_next = Node()
        node.add_next(node_next)

        node_insert = Node()
        node.add_next(node_insert)
        self.assertEqual(node_next.pred, node_insert)
        self.assertEqual(node_insert.next, node_next)


class TestColumnBlock(unittest.TestCase):
    def setUp(self):
        self.column_block = ColumnBlock(list(range(4)))
        self.column_block.rows.add(3)

    def test_split_intersection(self):
        split = self.column_block.split({1, 2})
        self.assertNotEqual(self.column_block, split)
        self.assertEqual(self.column_block.pred, split)
        self.assertEqual({1, 2}, self.column_block.columns)
        self.assertEqual({0, 3}, split.columns)
        self.assertEqual(set(), split.rows)
        self.assertEqual({3}, self.column_block.rows)

    def test_split_empty_intersection_all_elements(self):
        split = self.column_block.split({0, 1, 2, 3})
        self.assertEqual(self.column_block, split)
        self.assertEqual({0, 1, 2, 3}, self.column_block.columns)
        self.assertEqual({3}, self.column_block.rows)

    def test_split_empty_intersection_none_elements(self):
        split = self.column_block.split(set())
        self.assertEqual(self.column_block, split)
        self.assertEqual({0, 1, 2, 3}, self.column_block.columns)
        self.assertEqual({3}, self.column_block.rows)


class TestFinalPartition(unittest.TestCase):
    def test_final_rows(self):
        last_row_block = RowBlock([4])
        current = last_row_block
        for i in range(3, -1, -1):
            current.add_pred(RowBlock([i]))
            current = current.pred
        self.assertEqual(list(range(5)), row_ordering_from_last_row_block(last_row_block))


    def test_final_columns(self):
        last_column_block = ColumnBlock([4])
        current = last_column_block
        for i in range(3, -1, -1):
            current.add_pred(ColumnBlock([i]))
            current = current.pred
        self.assertEqual(list(range(5)), column_ordering_from_last_column_block(last_column_block))


class TestDoublyLinkedOrdering(unittest.TestCase):
    def setUp(self):
        self.matrix = [[1, 1, 1, 1, 1],
                       [1, 0, 1, 1, 0],
                       [0, 1, 1, 0, 0],
                       [1, 1, 1, 0, 0],
                       [0, 1, 0, 1, 1],
                       [1, 0, 0, 1, 0]]

    def test_run(self):
        line_ordering, column_ordering = doubly_lexical_order(self.matrix)
        # for i in range(len(self.matrix)):
        #     for j in range(len(self.matrix[i])):
        #         print(self.matrix[i][j], end=" ")
        #     print()
        # print(line_ordering, column_ordering)

        reordered_matrix = [[self.matrix[line_ordering[i]][column_ordering[j]] for j in range(len(self.matrix[i]))] for i in range(len(self.matrix))]
        # for i in range(len(reordered_matrix)):
        #     for j in range(len(reordered_matrix[i])):
        #         print(reordered_matrix[i][j], end=" ")
        #     print()

        self.assertEqual(True, is_doubly_lexical_ordered(reordered_matrix))

    def test_run_no_gamma(self):
        matrix = [[1, 1, 1], [1, 0, 1], [0, 0, 1]]
        line_ordering, column_ordering = doubly_lexical_order(matrix)
        self.assertEqual([2, 1, 0], line_ordering)
        self.assertEqual([1, 0, 2], column_ordering)


class TestIsaDoublyLexicallyOrdered(unittest.TestCase):
    def test_is_not(self):
        matrix = [[1, 0], [0, 1]]
        self.assertEqual(True, is_doubly_lexical_ordered(matrix))

    def test_isa(self):
        matrix = [[0, 1], [1, 0]]
        self.assertEqual(False, is_doubly_lexical_ordered(matrix))

class TestIsGammaFree(unittest.TestCase):
    def setUp(self):
        self.matrix = [[1, 1], [1, 0]]

    def test_isa(self):
        self.assertFalse(gamma_free_matrix(self.matrix))

    def test_transform(self):
        gamma_free_matrix(self.matrix, True)
        self.assertTrue(gamma_free_matrix(self.matrix))
        self.assertEqual([[1, 1], [1, 1]], self.matrix)
