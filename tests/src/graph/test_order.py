import unittest

from tbs.graph import MixedGraph, DIRECTED_EDGE, DirectedGraph, dfs, bfs, dfs_from_vertex, bfs_from_vertex,\
    topological_sort, direct_acyclic_graph_to_direct_comparability_graph, direct_comparability_graph_to_hase_diagram


class TestDag(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(DirectedGraph(), direct_acyclic_graph_to_direct_comparability_graph(DirectedGraph()))
        self.assertEqual(DirectedGraph(), direct_comparability_graph_to_hase_diagram(DirectedGraph()))

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

        self.assertEqual(hase_diagram, direct_comparability_graph_to_hase_diagram(comparability))

    def test_direct_acyclic_graph_to_hase_diagram(self):
        dag = DirectedGraph("abcd", (("a", "b"),
                                     ("b", "c"), ("b", "d"),
                                     ("c", "d")))
        hase_diagram = DirectedGraph("abcd", (("a", "b"),
                                              ("b", "c"),
                                              ("c", "d")))

        self.assertEqual(hase_diagram,
                         direct_comparability_graph_to_hase_diagram(direct_acyclic_graph_to_direct_comparability_graph(dag)))


class TestTopologicalSort(unittest.TestCase):
    def setUp(self):

        self.g = DirectedGraph(range(5), ((0, 1), (1, 2), (2, 4), (2, 3), (3, 4)))

    def test_topological_sort(self):
        self.assertEqual([0, 1, 2, 3, 4], topological_sort(self.g))

    def test_sort(self):
        self.g.difference(((1, 2), (2, 3)))
        self.g.update(((1, 3), ))
        self.assertEqual(2, topological_sort(self.g, key=lambda x: x == 2 and 1 or 2)[0])
        self.assertEqual([0, 2, 1, 3, 4], topological_sort(self.g, key=lambda x: (x == 0 and 1) or (x == 2) and 2 or 3))

    def test_cycle(self):
        self.g.update(((4, 0), ))
        self.assertRaises(TypeError, topological_sort, self.g)

    def test_not_connected(self):
        self.g.difference(((0, 1), ))
        self.assertEqual(set(range(5)), set(topological_sort(self.g)))


class TestDfs(unittest.TestCase):
    def setUp(self):
        self.g = MixedGraph(range(5), ({0, 1}, {2, 4}),  ((1, 2), (2, 3), (3, 4)))

    def test_all_elements(self):
        self.assertEqual(set(range(5)), set(dfs(self.g)))

    def test_not_connected(self):
        self.g.difference(((0, 1), ))
        self.assertEqual(set(range(5)), set(dfs(self.g)))

    def test_start_with_0(self):
        self.assertEqual(list(range(3)), dfs(self.g, key=lambda x: x == 0 and 1 or 2)[:3])

    def test_start_from_0(self):
        self.assertEqual(list(range(3)), dfs_from_vertex(self.g, 0)[:3])

    def test_start_from_2(self):
        self.assertEqual([2, 4], dfs_from_vertex(self.g, 2)[:2])

    def test_not_connected_directed(self):
        self.g.difference(((2, 3), ))
        self.g.update(DIRECTED_EDGE, ((3, 2), ))
        self.assertEqual([0, 1, 2, 4, 3], bfs(self.g, key=lambda x: x))


class TestBfs(unittest.TestCase):
    def setUp(self):
        self.g = MixedGraph(range(5), ({0, 1}, {2, 4}),  ((1, 2), (2, 3), (3, 4)))

    def test_all_elements(self):
        self.assertEqual(set(range(5)), set(bfs(self.g)))

    def test_not_connected(self):
        self.g.difference(((0, 1), ))
        self.assertEqual(set(range(5)), set(bfs(self.g)))

    def test_start_with_1(self):
        self.assertEqual([1, 0, 2, 3, 4], bfs(self.g, key=lambda x: x == 1 and -1 or x))

    def test_start_from_1(self):
        self.assertEqual([1, 0, 2, 3, 4], bfs_from_vertex(self.g, 1))

    def test_not_connected_directed(self):
        self.g.difference(((2, 3), ))
        self.g.update(DIRECTED_EDGE, ((3, 2), ))
        self.assertEqual([1, 0, 2, 4, 3], bfs(self.g, key=lambda x: x == 1 and -1 or x))
