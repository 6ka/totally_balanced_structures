import unittest

from tbs.graph import MixedGraph, DIRECTED_EDGE, UNDIRECTED_EDGE


class TestVerticesRawMixedGraph(unittest.TestCase):

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

    def test_add_vertices(self):
        g = MixedGraph()
        g.add(1)
        self.assertEqual({1}, g.vertices)

    def test_remove_vertices(self):
        g = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])
        g.remove(2)
        self.assertEqual({1, 3}, g.vertices)
        self.assertEqual([frozenset(), frozenset()], g.edges)


class TestInitRawMixedGraph(unittest.TestCase):
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


class TestUpdateRawMixedGraph(unittest.TestCase):
    def setUp(self):
        self.g = MixedGraph({1, 2, 3}, [(1, 2)], [(2, 3)])

    def test_update_raise_kind_error(self):
        self.assertRaises(ValueError, self.g.update, [(1, 1)], "UNKNOWN")

    def test_update_undirected_x_x_as_edge_not_vertices(self):
        self.g.update([(4, 4)], UNDIRECTED_EDGE, node_creation=False)
        self.assertEqual([{frozenset([1, 2])}, {(2, 3)}], self.g.edges)

    def test_update_directed_x_x_as_edge_not_vertices(self):
        self.g.update([(4, 4)], DIRECTED_EDGE, node_creation=False)
        self.assertEqual([{frozenset([1, 2])}, {(2, 3)}], self.g.edges)

    def test_add_undirected_edge_and_directed_edge_exist(self):
        self.g.update([{3, 2}], UNDIRECTED_EDGE)
        self.assertEqual([{frozenset([1, 2]), frozenset((2, 3))}, frozenset()], self.g.edges)

    def test_add_directed_edge_and_directed_edge_exist(self):
        self.g.update([(2, 1)], DIRECTED_EDGE)
        self.assertEqual([frozenset(), {(2, 1), (2, 3)}], self.g.edges)

    def test_remove_undirected_edge(self):
        self.g.update([(1, 2)], UNDIRECTED_EDGE, delete=True)
        self.assertEqual([frozenset(), {(2, 3)}], self.g.edges)


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

    def test_call_raise_not_a_veetex(self):
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
        self.g.update([(1, 1)], UNDIRECTED_EDGE)
        self.assertEqual({2, 1}, self.g(1, undirected=True, begin=False, end=False, closed=False))

    def test_xx_directed_edge(self):
        self.g.update([(1, 1)], DIRECTED_EDGE)
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
