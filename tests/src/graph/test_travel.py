# -*- coding: utf-8 -*-

import unittest

from tbs.graph import Graph, dfs, bfs, topological_sort


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.g_undirected = Graph(range(5))
        self.g_undirected.update(((1, 2), (3, 4), (0, 4)))

        self.g_directed = Graph(range(5), directed=True)
        self.g_directed.update(((0, 1), (1, 2), (2, 4), (1, 3), (3, 4)))

    def test_dfs_undirected(self):
        g = self.g_undirected

        seen = list()
        def action(vertex):
            seen.append(vertex)

        dfs(g, 0, action)

        self.assertEqual(3, len(seen))
        self.assertEqual({0, 3, 4}, set(seen))

    def test_dfs_directed(self):
        g = self.g_directed

        seen = list()
        def action(vertex):
            seen.append(vertex)

        dfs(g, 1, action)

        self.assertEqual(4, len(seen))
        self.assertEqual({1, 2, 3, 4}, set(seen))

    def test_bfs_undirected(self):
        g = self.g_undirected

        seen = list()
        def action(vertex):
            seen.append(vertex)

        bfs(g, 0, action)

        self.assertEqual(3, len(seen))
        self.assertEqual([0, 4, 3], seen)

    def test_bfs_directed(self):
        g = self.g_directed

        seen = list()

        def action(vertex):
            seen.append(vertex)

        bfs(g, 1, action, order_key=lambda x: -x)

        self.assertEqual(4, len(seen))
        self.assertEqual([1, 3, 2, 4], seen)

    def test_topological_sort_undirected(self):
        g = self.g_undirected
        order_iterator = topological_sort(g, 0)
        self.assertEqual([0, 4, 3], list(order_iterator))

    def test_topological_sort_directed(self):
        g = self.g_directed
        order_iterator = topological_sort(g, 0, order_key=lambda x: -x)
        self.assertEqual([0, 1, 2, 3, 4], list(order_iterator))
