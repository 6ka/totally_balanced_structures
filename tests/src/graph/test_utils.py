# -*- coding: utf-8 -*-

import unittest
from DLC.graph import Graph, CircuitError


class TestUtils(unittest.TestCase):
    
    def test_stuff(self):
        """Degree and vertex manipulation."""
        
        g = Graph(range(5))
        g.update(((1, 2), (3, 4), (0, 4)))
        self.assertEqual(g.degree(1), 1)
        self.assertEqual(g.degree(4), 2)
        self.assertEqual(g.degree(2), 1)
        g.directed = True
        g.update([(2, 1), (4, 0)])
        self.assertEqual(g.degree(1), 1)
        self.assertEqual(g.degree(1, False), 0)
        self.assertEqual(g.degree(4), 1)
        self.assertEqual(g.degree(4, False), 2)

        g = Graph(range(5))
        g.update(((1, 2), (3, 4), (0, 4)))        
        g.add("a vertex")
        self.assertRaises(ValueError, g.add, "a vertex")
        self.assertEqual(len(g), 6)
        self.assertEqual(g.degree("a vertex"), 0)
        g.remove("a vertex")
        g.remove(4)
        self.assertRaises(ValueError, g.remove, 4)        
        self.assertEqual(len(g), 4)
        self.assertEqual(g.degree(2), 1)
        g.clear()
        self.assertEqual(g.nb_edges(), 0)
        self.assertEqual(len(g), 4)
        g.update([(1, 2)])
        g.rename(1, "vertex")
        self.assertEqual(g.degree("vertex"), 1)
        self.assertRaises(ValueError, g.rename, 1, "vertex")

        g = Graph(range(5))
        g.update(((1, 2), (3, 4), (0, 4)))        
        cps = g.connected_parts()
        self.assertEqual(cps, frozenset([frozenset([1, 2]),
                                         frozenset([3, 4, 0])]))
        cps = g.connected_parts([2, 3, 0])
        self.assertEqual(cps, frozenset([frozenset([2]),
                                         frozenset([3]),
                                         frozenset([0])]))

    def test_paths(self):
        """Path finding methods."""
        
        g = Graph(range(5))
        g.update(((1, 2), (3, 4), (0, 4)))
        
        self.assertRaises(ValueError, g.path, 1, 6)
        self.assertEqual(g.path(1, 1), [1])
        self.assertEqual(g.path(3, 0), [3, 4, 0])
        self.assertEqual(g.path(1, 3), [])
        
        g.update([(1, 2, 1), (2, 0, 10), (0, 4, 3), (4, 3, 4), (3, 0, -8)])
        self.assertRaises(CircuitError, g.paths_from, 1, lambda x:x)