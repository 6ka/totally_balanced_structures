import unittest
from TBS.graph.mixed_graph import MixedGraph
from TBS.graph import Graph


class TestMixedGraph(unittest.TestCase):
    def test_len(self):
        mixed = MixedGraph()

        self.assertEquals(0, len(mixed))
        mixed.add_vertex(1)
        self.assertEquals(1, len(mixed))
        self.assertIn(1, mixed.vertices)
        self.assertIn(1, mixed.undirected)
        self.assertIn(1, mixed.directed)
        self.assertIn(1, mixed.directed_dual)

    def test_eq(self):
        self.assertEqual(MixedGraph(), MixedGraph())

    def test_eq_undirected_and_directed(self):
        mixed = MixedGraph()
        mixed.add_vertex(0)
        mixed.add_vertex(1)
        mixed.add_vertex(2)
        mixed.add_directed(1, 2)
        mixed.add_undirected(0, 2)

        mixed2 = MixedGraph()
        mixed2.add_vertex(0)
        mixed2.add_vertex(1)
        mixed2.add_vertex(2)
        mixed2.add_directed(1, 2)
        mixed2.add_undirected(0, 2)

        self.assertEqual(mixed, mixed2)

    def test_not_eq(self):
        mixed_graph = MixedGraph()
        mixed_graph.add_vertex(1)
        self.assertNotEqual(MixedGraph(),
                            mixed_graph)

    def test_add_undirected_edge(self):
        mixed = MixedGraph()
        mixed.add_vertex(0)
        mixed.add_vertex(1)
        mixed.add_vertex(2)
        mixed.add_undirected(1, 2)
        mixed.add_undirected(0, 2)

        self.assertEqual({0: {2},
                          1: {2},
                          2: {1, 0}
                          },
                         mixed.undirected)

    def test_remove_undirected_edge(self):
        mixed = MixedGraph()
        mixed.add_vertex(0)
        mixed.add_vertex(1)
        mixed.add_vertex(2)
        mixed.add_undirected(1, 2)
        mixed.add_undirected(0, 2)

        mixed.remove_undirected(0, 2)
        self.assertEqual({0: set(),
                          1: {2},
                          2: {1}
                          },
                         mixed.undirected)

    def test_add_directed_edge(self):
        mixed = MixedGraph()
        mixed.add_vertex(0)
        mixed.add_vertex(1)
        mixed.add_vertex(2)
        mixed.add_directed(1, 2)
        mixed.add_directed(2, 0)

        self.assertEqual({0: set(),
                          1: {2},
                          2: {0},
                          },
                         mixed.directed)

        self.assertEqual({0: {2},
                          1: set(),
                          2: {1}
                          },
                         mixed.directed_dual)

    def test_remove_directed_edge(self):
        mixed = MixedGraph()
        mixed.add_vertex(0)
        mixed.add_vertex(1)
        mixed.add_vertex(2)
        mixed.add_directed(1, 2)
        mixed.add_directed(2, 0)

        mixed.remove_directed(1, 2)

        self.assertEqual({0: set(),
                          1: set(),
                          2: {0},
                          },
                         mixed.directed)

        self.assertEqual({0: {2},
                          1: set(),
                          2: set()
                          },
                         mixed.directed_dual)

    def test_remove_begin_vertex_with_edges(self):
        mixed = MixedGraph()
        mixed.add_vertex(0)
        mixed.add_vertex(1)
        mixed.add_vertex(2)
        mixed.add_directed(1, 2)
        mixed.add_undirected(0, 2)

        mixed.remove_vertex(1)

        self.assertEqual(frozenset([0, 2]),
                         mixed.vertices)

        self.assertEqual({0: {2},
                          2: {0},
                          },
                         mixed.undirected)

        self.assertEqual({0: set(),
                          2: set(),
                          },
                         mixed.directed)
        self.assertEqual({0: set(),
                          2: set(),
                          },
                         mixed.directed_dual)

    def test_remove_end_vertex_with_edges(self):
        mixed = MixedGraph()
        mixed.add_vertex(0)
        mixed.add_vertex(1)
        mixed.add_vertex(2)
        mixed.add_directed(1, 2)
        mixed.add_undirected(0, 2)

        mixed.remove_vertex(2)

        self.assertEqual(frozenset([0, 1]),
                         mixed.vertices)

        self.assertEqual({0: set(),
                          1: set(),
                          },
                         mixed.undirected)

        self.assertEqual({0: set(),
                          1: set(),
                          },
                         mixed.directed)
        self.assertEqual({0: set(),
                          1: set(),
                          },
                         mixed.directed_dual)


class TestMixedGraphInit(unittest.TestCase):
    def setUp(self):
        self.mixed = MixedGraph()
        self.mixed.add_vertex(0)
        self.mixed.add_vertex(1)
        self.mixed.add_vertex(2)
        self.mixed.add_directed(1, 2)
        self.mixed.add_undirected(0, 2)

    def test_init_from_mixed_graph_copy_equal(self):
        mixed_copy = MixedGraph(self.mixed)
        self.assertEqual(self.mixed, mixed_copy)

    def test_init_from_mixed_graph_copy_remove_vertex(self):
        mixed_copy = MixedGraph(self.mixed)
        self.assertEqual(self.mixed, mixed_copy)

        mixed_copy2 = MixedGraph(mixed_copy)
        mixed_copy2.remove_vertex(0)

        self.assertNotEquals(mixed_copy, mixed_copy2)
        self.assertEqual(self.mixed, mixed_copy)

    def test_init_from_mixed_graph_copy_remove_undirect(self):
        mixed_copy = MixedGraph(self.mixed)
        self.assertEqual(self.mixed, mixed_copy)

        mixed_copy2 = MixedGraph(mixed_copy)
        mixed_copy2.remove_undirected(0, 2)

        self.assertNotEquals(mixed_copy, mixed_copy2)
        self.assertEqual(self.mixed, mixed_copy)

    def test_init_from_mixed_graph_copy_remove_direct(self):
        mixed_copy = MixedGraph(self.mixed)
        self.assertEqual(self.mixed, mixed_copy)

        mixed_copy2 = MixedGraph(mixed_copy)
        mixed_copy2.remove_directed(1, 2)

        self.assertNotEquals(mixed_copy, mixed_copy2)
        self.assertEqual(self.mixed, mixed_copy)

    def test_init_from_graph(self):
        graph = Graph()
        graph.update(((1, 2), (2, 3), (2, 4)))
        mixed_graph = MixedGraph.init_from_graph(graph)
        self.assertSetEqual(mixed_graph.undirected[1], {2})
        self.assertSetEqual(mixed_graph.undirected[2], {1, 3, 4})
        self.assertSetEqual(mixed_graph.undirected[3], {2})
        self.assertSetEqual(mixed_graph.undirected[4], {2})
        self.assertDictEqual(mixed_graph.directed, dict())
        self.assertSetEqual(mixed_graph.vertices, {1, 2, 3, 4})
