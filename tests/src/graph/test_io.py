# -*- coding: utf-8 -*-

import unittest
import os
from TBS.graph import Graph
import TBS.graph.file_io


class TestIo(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), "../"))
        self.g = Graph(range(5)).update(((1, 2), (3, 4, 2), (0, 4, 3)))
        for x in list(self.g):
            self.g.rename(x, str(x))

    def test_load(self):
        """Load graphs."""

        f = open("../resources/graph_1.gr")
        g = TBS.graph.file_io.load(f)
        self.assertEqual(g, self.g)
        self.g.update([(str(3), str(4), str(2)), (str(0), str(4), str(3))])
        f.close()
        f = open("../resources/graph_1.gr")
        g = TBS.graph.file_io.load(f, number=False)
        self.assertEqual(g, self.g)
        f.close()

        f = open("../resources/graph_2.gr")
        g = TBS.graph.file_io.load(f, "edgesNb", number=False)
        self.g.add(str(5))
        self.assertEqual(g, self.g)

        self.g.remove(str(5))
        self.g.update([(str(3), str(4), None), (str(0), str(4), None)])
        f.close()
        f = open("../resources/graph_3.gr")
        g = TBS.graph.file_io.load(f, "dotBasic")
        self.assertEqual(g, self.g)

        self.g.directed = True
        self.g.add(str(5))
        self.g.update([(str(2), str(1)), (str(4), str(3)), (str(0), str(4))])
        f.close()
        f = open("../resources/graph_4.gr")
        g = TBS.graph.file_io.load(f, "dotBasic")
        self.assertEqual(g, self.g)

        f.close()
        f = open("../resources/graph_5.gr")
        self.assertRaises(ValueError, TBS.graph.file_io.load, f)
        f.close()
        f = open("../resources/graph_6.gr")
        self.assertRaises(ValueError, TBS.graph.file_io.load, f)
        f.close()

    def test_write(self):
        """Write graphs."""
        
        f = open("../resources/test_write.mat", "w")
        TBS.graph.file_io.save(self.g, f)
        f.close()
        f = open("../resources/test_write.mat")
        g = TBS.graph.file_io.load(f)
        f.close()
        self.assertEqual(g, self.g)
        os.remove("../resources/test_write.mat")