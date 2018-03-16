import unittest


from tbs.graph import cls, MixedGraph


class TestInit(unittest.TestCase):

    def test_init(self):
        self.assertEqual(cls({1, 2, 3}, [(1, 2), (2, 3)]), MixedGraph({1, 2, 3}, [(1, 2), (2, 3)], []))

    def test_repr(self):
        g = cls({1, 2, 3}, [(1, 2), (2, 3)])
        self.assertEqual(cls, eval(repr(g)).__class__)

        self.assertEqual(g, eval(repr(g)))

    def test_from_graph(self):
        self.assertEqual(cls, cls.from_graph(cls({1, 2, 3}, [(1, 2), (2, 3)])).__class__)
        self.assertEqual(cls({1, 2, 3}, [(1, 2), (2, 3)]),
                         cls.from_graph(cls({1, 2, 3}, [(1, 2), (2, 3)])))

    def test_from_mixed_graph(self):
        self.assertEqual(cls, cls.from_graph(MixedGraph({1, 2, 3}, [(1, 2), (2, 3)]), [(3, 1)]).__class__)
        self.assertEqual(cls({1, 2, 3}, [(1, 2), (2, 3)]),
                         MixedGraph({1, 2, 3}, [(1, 2), (2, 3)]), [(3, 1)])

    def test_from_neighborhoods(self):
        self.assertEqual(cls, cls.from_neighborhoods({1: (2,), 2: (3,)}).__class__)
        self.assertEqual(cls({1, 2, 3}, [(1, 2), (2, 3)]),
                         cls.from_neighborhoods({1: (2,), 2: (3,)}))

    def test_from_edges(self):
        self.assertEqual(cls, cls.from_edges([(1, 2), (2, 3)]).__class__)
        self.assertEqual(cls({1, 2, 3}, [(1, 2), (2, 3)]),
                         cls.from_edges([(1, 2), (2, 3)]))


class TestDifferencesWithMixedGraph(unittest.TestCase):
    def setUp(self):
        self.g = cls({1, 2, 3}, [(1, 2), (2, 3)])

    def test_edges(self):
        self.assertEqual({frozenset((1, 2)), frozenset((2, 3))}, self.g.edges)

    def test_call(self):
        self.assertEqual({1, 3}, self.g(2))

    def test_isa_edge(self):
        self.assertTrue(self.g.isa_edge(1, 2))
        self.assertTrue(self.g.isa_edge(2, 1))

    def test_update_difference(self):
        self.assertTrue(self.g.update([(1, 2)]).isa_edge(1, 2))
        self.assertFalse(self.g.difference([(1, 2)]).isa_edge(1, 2))
        self.assertTrue(self.g.update([(3, 1)]).isa_edge(1, 3))
