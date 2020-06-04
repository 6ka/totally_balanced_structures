import unittest

import json
from tbs.graph import MixedGraph, DIRECTED_EDGE, UNDIRECTED_EDGE


class TestInit(unittest.TestCase):

    def test_no_vertices(self):
        """Initialisation and basic manipulations."""

        self.assertFalse(MixedGraph().vertices)

    def test_init_with_vertices(self):
        self.assertEqual({1, 3}, MixedGraph({1, 3}).vertices)

    def test_init_from_graph(self):
        self.assertEqual(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]),
                         MixedGraph.from_graph(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])))

        self.assertEqual(MixedGraph({1, 2}, [(1, 2)]),
                         MixedGraph.from_graph(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), {1, 2}))
        self.assertEqual(MixedGraph({2, 3}, [], [(2, 3)]),
                         MixedGraph.from_graph(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), {2, 3}))

        self.assertEqual(MixedGraph({1, 3}),
                         MixedGraph.from_graph(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), {1, 3}))

        self.assertEqual(MixedGraph(),
                         MixedGraph.from_graph(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), {}))

    def test_no_edges(self):
        self.assertEqual([frozenset(), frozenset()], MixedGraph().edges)

    def test_one_undirected_edge(self):
        self.assertEqual([frozenset([frozenset([1, 2])]), frozenset()], MixedGraph({1, 2},
                                                                                   undirected_edges=[(1, 2)]).edges)

    def test_one_directed_edge(self):
        self.assertEqual([frozenset(), frozenset([(1, 2)])], MixedGraph({1, 2}, directed_edges=[(1, 2)]).edges)

    def test_undirected_edge_not_in_vertices(self):
        self.assertEqual([frozenset([frozenset([1, 2])]), frozenset()], MixedGraph({1, 2},
                                                                                   undirected_edges=[(1, 2),
                                                                                                     (2, 3)]).edges)

    def test_directed_edge_not_in_vertices(self):
        self.assertEqual([frozenset(), frozenset([(1, 2)])], MixedGraph({1, 2}, directed_edges=[(1, 2),
                                                                                                (2, 3)]).edges)

    def test_directed_and_undirected_vertices(self):
        self.assertEqual([frozenset([frozenset([1, 2])]), frozenset([(2, 3)])],
                         MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]).edges)


class TestVerticesMixedGraph(unittest.TestCase):
    def test_add_vertices(self):
        g = MixedGraph()
        g.add(1)
        self.assertEqual({1}, g.vertices)

    def test_remove_vertices(self):
        g = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])
        g.remove(2)
        self.assertEqual({1, 3}, g.vertices)
        self.assertEqual([frozenset(), frozenset()], g.edges)


class TestUpdateRawMixedGraph(unittest.TestCase):
    def setUp(self):
        self.g = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])

    def test_update_raise_kind_error(self):
        self.assertRaises(ValueError, self.g.update, [(1, 1)], "UNKNOWN")

    def test_update_undirected_x_x_as_edge_not_vertices(self):
        self.g.update(UNDIRECTED_EDGE, [(4, 4)], node_creation=False)
        self.assertEqual([{frozenset([1, 2])}, {(2, 3)}], self.g.edges)

    def test_update_directed_x_x_as_edge_not_vertices(self):
        self.g.update(DIRECTED_EDGE, [(4, 4)], node_creation=False)
        self.assertEqual([{frozenset([1, 2])}, {(2, 3)}], self.g.edges)

    def test_add_undirected_edge_and_directed_edge_exist(self):
        self.g.update(UNDIRECTED_EDGE, [{3, 2}])
        self.assertEqual([{frozenset([1, 2]), frozenset((2, 3))}, frozenset()], self.g.edges)

    def test_add_directed_edge_and_directed_edge_exist(self):
        self.g.update(DIRECTED_EDGE, [(2, 1)])
        self.assertEqual([frozenset(), {(2, 1), (2, 3)}], self.g.edges)

    def test_not_remove(self):
        self.g.difference([(3, 2)])
        self.assertEqual([{frozenset((1, 2))}, {(2, 3)}], self.g.edges)

    def test_remove_undirected_edge(self):
        self.g.difference([(1, 2)])
        self.assertEqual([frozenset(), {(2, 3)}], self.g.edges)

    def test_remove_directed_edge(self):
        self.g.difference([(2, 3)])
        self.assertEqual([{frozenset((1, 2))}, set()], self.g.edges)


class TestCompare(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(MixedGraph(), MixedGraph())
        self.assertEqual(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]))

    def test_ne(self):
        self.assertNotEqual(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), MixedGraph({1, 2, 3, 4}, [(1, 2)], [(2, 3)]))
        self.assertNotEqual(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), MixedGraph({1, 2, 3}, [(2, 3)], [(1, 2)]))
        self.assertNotEqual(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), MixedGraph({1, 2, 3}, [(1, 2)]))
        self.assertNotEqual(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), MixedGraph({1, 2, 3}, [], [(1, 2)]))

    def test_len(self):
        self.assertEqual(0, len(MixedGraph()))
        self.assertEqual(3, len(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])))

    def test_nb_edges(self):
        self.assertEqual(0, MixedGraph().nb_edges)
        self.assertEqual(2, MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]).nb_edges)

    def test_degree(self):
        self.assertEqual(0, MixedGraph({1, 2, 3, 4}, [(1, 2)], [(2, 3)]).degree(4))
        self.assertEqual(1, MixedGraph({1, 2, 3, 4}, [(1, 2)], [(2, 3)]).degree(1))
        self.assertEqual(1, MixedGraph({1, 2, 3, 4}, [(1, 2)], [(2, 3)]).degree(3))
        self.assertEqual(2, MixedGraph({1, 2, 3, 4}, [(1, 2)], [(2, 3)]).degree(2))

    def test_repr(self):
        self.assertEqual(MixedGraph(), eval(repr(MixedGraph())))
        self.assertEqual(MixedGraph({1, 2, 3}, [(1, 2)]), eval(repr(MixedGraph({1, 2, 3}, [(1, 2)]))))

        self.assertEqual(MixedGraph({1, 2, 3}, directed_edges=[(2, 3)]),
                         eval(repr(MixedGraph({1, 2, 3}, [], [(2, 3)]))))

        self.assertEqual(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]),
                         eval(repr(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]))))

    def test_in(self):
        mixed_graph = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])
        self.assertTrue(1 in mixed_graph)
        self.assertFalse(4 in mixed_graph)


class TestGetSet(unittest.TestCase):
    def test_iter(self):
        self.assertEqual({1, 2, 3}, {x for x in MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])})

    def test_get_set_item(self):
        self.assertRaises(ValueError, MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]).__getitem__, (3, 2))

        g = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])
        self.assertIsNone(g[1, 2])
        g[1, 2] = "value"
        self.assertEqual("value", g[1, 2])


class TestCall(unittest.TestCase):
    def setUp(self):
        self.g = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])

    def test_call_raise_not_a_vertex(self):
        self.assertRaises(ValueError, self.g.__call__, 0)

    def test_call_nothing(self):
        self.assertEqual(frozenset(), self.g(2, undirected=False, begin=False, end=False, closed=False))

    def test_call_undirected(self):
        self.assertEqual({1}, self.g(2, undirected=True, begin=False, end=False, closed=False))

    def test_call_begin(self):
        self.assertEqual({3}, self.g(2, undirected=False, begin=True, end=False, closed=False))
        self.assertEqual(frozenset(), self.g(3, undirected=False, begin=True, end=False, closed=False))

    def test_call_end(self):
        self.assertEqual(frozenset(), self.g(2, undirected=False, begin=False, end=True, closed=False))
        self.assertEqual({2}, self.g(3, undirected=False, begin=False, end=True, closed=False))

    def test_call_closed(self):
        self.assertEqual({2}, self.g(2, undirected=False, begin=False, end=False, closed=True))


class TestIsa(unittest.TestCase):
    def setUp(self):
        self.g = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])

    def test_isa_vertex(self):
        self.assertFalse(self.g.isa_vertex(0))
        self.assertTrue(self.g.isa_vertex(1))

    def test_isa_undirected_edge(self):
        self.assertFalse(self.g.isa_edge(2, 3, UNDIRECTED_EDGE))
        self.assertTrue(self.g.isa_edge(2, 1, UNDIRECTED_EDGE))

    def test_isa_directed_edge(self):
        self.assertFalse(self.g.isa_edge(3, 2, DIRECTED_EDGE))
        self.assertFalse(self.g.isa_edge(1, 2, DIRECTED_EDGE))
        self.assertTrue(self.g.isa_edge(2, 3, DIRECTED_EDGE))

    def test_isa_edge(self):
        self.assertTrue(self.g.isa_edge(2, 1))
        self.assertTrue(self.g.isa_edge(2, 3))
        self.assertFalse(self.g.isa_edge(3, 2))
        self.assertFalse(self.g.isa_edge(3, 1))


class TestLoop(unittest.TestCase):

    def setUp(self):
        self.g = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])

    def test_xx_undirected_edge(self):
        self.g.update(UNDIRECTED_EDGE, [(1, 1)])
        self.assertEqual({2, 1}, self.g(1, undirected=True, begin=False, end=False, closed=False))

    def test_xx_directed_edge(self):
        self.g.update(DIRECTED_EDGE, [(1, 1)])
        self.assertEqual({1}, self.g(1, undirected=False, begin=True, end=False, closed=False))
        self.assertEqual({1}, self.g(1, undirected=False, begin=False, end=True, closed=False))


class TestContraction(unittest.TestCase):
    def setUp(self):
        self.g = MixedGraph({1, 2, 3, 4}, [(1, 2), (1, 4), (4, 3)], [(2, 3)])

    def test_contraction_x(self):
        self.g.contraction(1, 2, 1)
        self.assertEqual(MixedGraph({1, 3, 4}, [(1, 4), (4, 3)], [(1, 3)]), self.g)

    def test_contraction_new_vertex(self):
        self.g.contraction(1, 2, 5)
        self.assertEqual(MixedGraph({5, 3, 4}, [(5, 4), (4, 3)], [(5, 3)]), self.g)


class TestPath(unittest.TestCase):
    def setUp(self):
        self.g = MixedGraph({1, 2, 3, 4, 5, 6}, [(1, 2), (2, 3), (5, 6)], [(3, 4), (4, 5)])

    def test_undirected_path(self):
        self.assertEqual([1, 2, 3], self.g.path(1, 3))

    def test_directed_path(self):
        self.assertEqual([3, 4, 5], self.g.path(3, 5))

    def test_mixed_path(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], self.g.path(1, 6))

    def test_no_path(self):
        self.assertEqual([], self.g.path(6, 1))

    def test_no_crcuit_error(self):
        self.g.update(DIRECTED_EDGE, [(5, 3)])
        self.assertEqual([1, 2, 3, 4, 5, 6], self.g.path(1, 6))

    def test_circuit_error(self):
        self.g.update(DIRECTED_EDGE, [(5, 3)])
        with self.assertRaises(Exception):
            self.g.path(1, 6, lambda u, v: (u != 5 and v != 3) and 1 or -5)


class TestJson(unittest.TestCase):
    def test_undirected(self):
        g = MixedGraph({1, 2}, [(1, 2)])
        g_son = g.json()

        self.assertEqual(2, len(g_son["graph"]["nodes"]))
        self.assertEqual(1, len(g_son["graph"]["edges"]))
        self.assertFalse(g_son["graph"]["edges"][0]["directed"])

    def test_directed(self):
        g = MixedGraph({1, 2}, [], [(1, 2)])
        g_son = g.json()

        self.assertEqual(2, len(g_son["graph"]["nodes"]))
        self.assertEqual(1, len(g_son["graph"]["edges"]))
        self.assertTrue(g_son["graph"]["edges"][0]["directed"])

    def test_both(self):
        g = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])

        g_son = g.json()

        self.assertEqual(3, len(g_son["graph"]["nodes"]))
        self.assertEqual(2, len(g_son["graph"]["edges"]))
        self.assertFalse(g_son["graph"]["edges"][1]["directed"])
        self.assertTrue(g_son["graph"]["edges"][0]["directed"])

    def test_load(self):
        g_son = {"graph": {
            "nodes": [{"id": "1"}, {"id": "2"}, {"id": "3"}],
            "edges": [{"source": "2", "target": "3", "directed": True},
                      {"source": "1", "target": "2", "directed": False}]
        }
        }

        self.assertEqual(MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)]), MixedGraph.from_json(g_son))
