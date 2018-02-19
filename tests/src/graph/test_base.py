# -*- coding: utf-8 -*-

import unittest

from tbs.graph import Graph


class TestGraphBase(unittest.TestCase):
    
    def test_inits(self):
        """Initialisation and basic manipulations."""
        
        self.assertFalse(Graph())
        g = Graph(range(1, 7))
        self.assertTrue(g)
        
        self.assertEqual(len(g), 6)
        self.assertEqual(len(g._neighborhood), 6)
        for x in g._neighborhood:
            self.assertEqual(len(g._neighborhood[x]), 0)
        
        self.assertRaises(ValueError, g.update, [(1, 1)])
        g.update([("toto", 1)], False)
        self.assertEqual(len(g), 6)
        g.update([(1, "toto")], False)
        self.assertEqual(len(g), 6)
        for x in g._neighborhood:
            self.assertEqual(len(g._neighborhood[x]), 0)
        
        g.update([("tutu", "toto")])
        g.update([(1, "toto")])
        
        self.assertEqual(len(g), 8)
        self.assertTrue(1 in g._neighborhood["toto"])
        self.assertTrue("toto" in g._neighborhood[1])
        self.assertEqual(len(g._neighborhood["toto"]), 2)
        self.assertEqual(len(g._neighborhood[1]), 1)
        self.assertEqual(g._neighborhood[1]["toto"], None)
        self.assertEqual(g._neighborhood["toto"][1], None)
        for x in g._neighborhood:
            if x in (1, "toto", "tutu"):
                continue
            self.assertEqual(len(g._neighborhood[x]), 0)
        
        g.update([(1, "toto", 42)])
        self.assertEqual(len(g), 8)
        self.assertTrue(1 in g._neighborhood["toto"])
        self.assertTrue("toto" in g._neighborhood[1])
        self.assertEqual(len(g._neighborhood["toto"]), 2)
        self.assertEqual(len(g._neighborhood[1]), 1)
        self.assertEqual(g._neighborhood[1]["toto"], 42)
        self.assertEqual(g._neighborhood["toto"][1], 42)
        for x in g._neighborhood:
            if x in (1, "toto", "tutu"):
                continue
            self.assertEqual(len(g._neighborhood[x]), 0)

        g.update([(1, "toto", 42)], delete=False)
        self.assertEqual(len(g), 8)
        self.assertTrue(1 in g._neighborhood["toto"])
        self.assertTrue("toto" in g._neighborhood[1])
        self.assertEqual(len(g._neighborhood["toto"]), 2)
        self.assertEqual(len(g._neighborhood[1]), 1)
        self.assertEqual(g._neighborhood[1]["toto"], 42)
        self.assertEqual(g._neighborhood["toto"][1], 42)
        for x in g._neighborhood:
            if x in (1, "toto", "tutu"):
                continue
            self.assertEqual(len(g._neighborhood[x]), 0)

        g.update([(1, "toto", 42)], delete=True)
        self.assertEqual(len(g), 8)
        for x in g._neighborhood:
            if x in ("toto", "tutu"):
                continue
            self.assertEqual(len(g._neighborhood[x]), 0)
        
        g.update([(1, "toto", None)])
        self.assertEqual(g._neighborhood[1]["toto"], None)
        g.update([(1, "toto", 42)])
        self.assertEqual(g._neighborhood[1]["toto"], 42)
        g.update([(1, "toto")], delete=True)
        self.assertEqual(len(g), 8)
        for x in g._neighborhood:
            if x in ("toto", "tutu"):
                continue            
            self.assertEqual(len(g._neighborhood[x]), 0)
        
        self.assertEqual(Graph(range(1, 7)), Graph(range(1, 7)))
        self.assertNotEqual(Graph(range(1, 7)), Graph(range(1, 7)).update([(1, 5)]))
        self.assertNotEqual(Graph(range(1, 7)), Graph(range(1, 7)).update([(1, 7)]))
        self.assertFalse(Graph(range(1, 7)) != Graph(range(1, 7)))
        elems = []
        for x in g:
            elems.append(x)
        self.assertEqual(set(elems), set(g._neighborhood))
        
        g = Graph(range(5))
        g.update(((1, 2), (3, 4), (0, 4)))
        self.assertEqual(len(g[4]), 2)
        self.assertEqual(set(g[4]), {0, 3})
        try:
            g["not there"]
        except ValueError:
            pass
        else:
            self.fail()
            
        self.assertEqual(g(1, 2), None)
        g.update([(1, 2, 34)])
        self.assertEqual(g(1, 2), 34)
        self.assertRaises(ValueError, g, 1, 4)
        self.assertRaises(ValueError, g, 9, 4)
                
    def test_directed(self):
        """Directed graphs."""
        
        g = Graph(range(5))
        g2 = Graph(range(5))
        g.update(((1, 2), (3, 4), (0, 4)))
        g2.update(((1, 2), (3, 4), (0, 4)))
        
        self.assertEqual(g.nb_edges(), 3)
        
        self.assertEqual(g.directed, False)

        g.directed = True
        self.assertEqual(g.nb_edges(), 6)
        
        g.update(((2,1),), delete=True)
        self.assertEqual(g.nb_edges(), 5)
        g.directed = False
        
        self.assertEqual(g, g2)

    def test_edge_vertices(self):
        """Vertex/edges manipulation."""
        
        g = Graph(range(5))
        g.update(((1, 2), (3, 4), (0, 4)))
        self.assertEqual(set(g), set(range(5)))
        self.assertEqual(set([frozenset([x, y]) for x, y in g.edges()]), 
                         set([frozenset([x, y]) for x, y in ((1, 2), (3, 4), (0, 4))]))
        self.assertEqual(g.nb_edges(), 3)
        g2 = g.copy()
        self.assertEqual(g2, g)
        g2.update([(1, 2)], delete=True)
        self.assertNotEqual(g2, g)
        g3 = g.restriction([2, 3, 4])
        self.assertEqual(len(g3), 3)
        self.assertEqual(g3.nb_edges(), 1)
        self.assertEqual(frozenset(g3.edges()[0]), frozenset([3, 4]))
        g3.directed = True
        g3.update([(3, 4)], delete=True)
        self.assertEqual(g3.edges(), [(4, 3)])
        
        g = Graph(range(5))
        g.update(((1, 2), (3, 4), (0, 4)))
        g.contraction(4, 3)
        self.assertEqual(len(g), 4)
        self.assertFalse(4 in g)
        self.assertTrue(g.isa_edge(3, 0))
        self.assertEqual(len(g[3]), 1)
        g = Graph(range(5))
        g.directed = True
        g.update(((1, 3), (2, 4), (4, 3), (4, 0)))
        g.contraction(4, 3)
        self.assertEqual(len(g[3]), 1)
        self.assertTrue(g.isa_edge(3, 0))
        self.assertTrue(g.isa_edge(1, 3))
        self.assertTrue(g.isa_edge(2, 3))

    def test_repr(self):
        g = Graph([0], directed=True)
        self.assertEqual("Graph(vertices=[0], edges=[], directed=True)", repr(g))

    def test_isa(self):
        """Isa_ methods."""
        
        g = Graph(range(5))
        g.update(((1, 2), (3, 4), (0, 4)))
        self.assertTrue(g.isa_vertex(0))
        self.assertFalse(g.isa_vertex(6))
        
        self.assertTrue(g.isa_leaf(1))
        self.assertFalse(g.isa_leaf(4))
        
        self.assertTrue(g.isa_edge(1, 2))
        self.assertFalse(g.isa_edge(1, 3))

    def test_dual(self):
        g = Graph(range(5))
        g.update(((1, 2), (3, 4, "one attribute"), (0, 4)))
        self.assertEqual(g, g.dual())

        g = Graph(range(5), directed=True)
        g.update(((1, 2), (3, 4, "one attribute"), (0, 4)))

        dual_g = Graph(range(5), directed=True)
        dual_g.update(((2, 1), (4, 3, "one attribute"), (4, 0)))

        self.assertEqual(dual_g, g.dual())


