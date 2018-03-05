# -*- coding: utf-8 -*-

import unittest

from tbs.graph import Graph, DirectedGraph, dfs, bfs,\
    topological_sort, direct_acyclic_graph_to_direct_comparability_graph, direct_acyclic_graph_to_hase_diagram


class TestDag(unittest.TestCase):
    def test_direct_acyclic_graph_to_direct_comparability_graph(self):
        dag = DirectedGraph("abcd", (("a", "b"),
                                     ("b", "c"), ("b", "d"),
                                     ("c", "d")))
        comparability = DirectedGraph("abcd", (("a", "b"), ("a", "c"), ("a", "d"),
                                               ("b", "c"), ("b", "d"),
                                               ("c", "d")))

        self.assertEqual(comparability, direct_acyclic_graph_to_direct_comparability_graph(dag))

    def test_comparability_to_hase_diagram(self):
        comparability = DirectedGraph("abcd", (("a", "b"), ("a", "c"), ("a", "d"),
                                               ("b", "c"), ("b", "d"),
                                               ("c", "d")))
        hase_diagram = DirectedGraph("abcd", (("a", "b"),
                                              ("b", "c"),
                                              ("c", "d")))

        self.assertEqual(hase_diagram, direct_acyclic_graph_to_hase_diagram(comparability))

    def test_direct_acyclic_graph_to_hase_diagram(self):
        dag = DirectedGraph("abcd", (("a", "b"),
                                     ("b", "c"), ("b", "d"),
                                     ("c", "d")))
        hase_diagram = DirectedGraph("abcd", (("a", "b"),
                                              ("b", "c"),
                                              ("c", "d")))

        self.assertEqual(hase_diagram, direct_acyclic_graph_to_hase_diagram(dag))


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.g_undirected = Graph(range(5))
        self.g_undirected.update(((1, 2), (3, 4), (0, 4)))

        self.g_directed = DirectedGraph(range(5))
        self.g_directed.update(((0, 1), (1, 2), (2, 4), (1, 3), (3, 4)))

    def test_dfs_undirected(self):
        g = self.g_undirected

        seen = list()
        def action(vertex):
            seen.append(vertex)

        dfs(g, 0, action)

        self.assertEqual(3, len(seen))
        self.assertEqual({0, 3, 4}, set(seen))

    # def test_dfs_directed(self):
    #     g = self.g_directed
    #
    #     seen = list()
    #     def action(vertex):
    #         seen.append(vertex)
    #
    #     dfs(g, 1, action)
    #
    #     self.assertEqual(4, len(seen))
    #     self.assertEqual({1, 2, 3, 4}, set(seen))

    def test_bfs_undirected(self):
        g = self.g_undirected

        seen = list()
        def action(vertex):
            seen.append(vertex)

        bfs(g, 0, action)

        self.assertEqual(3, len(seen))
        self.assertEqual([0, 4, 3], seen)

    # def test_bfs_directed(self):
    #     g = self.g_directed
    #
    #     seen = list()
    #
    #     def action(vertex):
    #         seen.append(vertex)
    #
    #     bfs(g, 1, action, order_key=lambda x: -x)
    #
    #     self.assertEqual(4, len(seen))
    #     self.assertEqual([1, 3, 2, 4], seen)

    # def test_topological_sort_undirected(self):
    #     g = self.g_undirected
    #     order_iterator = topological_sort(g, 0)
    #     self.assertEqual([0, 4, 3], list(order_iterator))

    # def test_topological_sort_directed(self):
    #     g = self.g_directed
    #     order_iterator = topological_sort(g, order_key=lambda x: -x)
    #     self.assertEqual([0, 1, 2, 3, 4], list(order_iterator))
