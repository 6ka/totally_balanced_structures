import unittest
from tbs.diss import Diss

import tbs.conversion.diss


class TestDiss(unittest.TestCase):
    def test_to_graph(self):
        """Initialization, setting and getting attributes."""

        d = Diss(range(1, 6))
        d.update(lambda x, y: 5)
        d[1, 2] = 2
        g = tbs.conversion.diss.to_graph(d, 3)

        self.assertEqual(len(d), len(g))
        print(g.edges)
        self.assertEqual([{1, 2}], [set(x) for x in g.edges])

    def test_to_string(self):
        """String representation."""

        d = Diss(range(5))
        d.update(lambda x, y: x + y, True)
        square = "0 1 2 3 4\n1 2 3 4 5\n2 3 4 5 6\n3 4 5 6 7\n4 5 6 7 8"
        squarel = "0 0 1 2 3 4\n1 1 2 3 4 5\n2 2 3 4 5 6\n3 3 4 5 6 7\n4 4 5 6 7 8"
        upper = "0 1 2 3 4\n  2 3 4 5\n    4 5 6\n      6 7\n        8"
        upperl = "0 0 1 2 3 4\n1   2 3 4 5\n2     4 5 6\n3       6 7\n4         8"
        lower = "0\n1 2\n2 3 4\n3 4 5 6\n4 5 6 7 8"
        lowerl = "0,0\n1,1,2\n2,2,3,4\n3,3,4,5,6\n4,4,5,6,7,8"
        lowerp = "5\n0\n1,1\n2,2,3\n3,3,4,5\n4,4,5,6,7"
        squarep = "5\n0 0 1 2 3 4\n1 1 2 3 4 5\n2 2 3 4 5 6\n3 3 4 5 6 7\n4 4 5 6 7 8"
        upperp = "5\n0   1 2 3 4\n1     3 4 5\n2       5 6\n3         7\n4"
        self.assertEqual(str(d), square)
        self.assertEqual(tbs.conversion.diss.to_string(d, "squarel"), squarel)
        self.assertEqual(tbs.conversion.diss.to_string(d, "squarep"), squarep)
        self.assertEqual(tbs.conversion.diss.to_string(d, "upper"), upper)
        self.assertEqual(tbs.conversion.diss.to_string(d, "upperl"), upperl)
        self.assertEqual(tbs.conversion.diss.to_string(d, "upperp"), upperp)
        self.assertEqual(tbs.conversion.diss.to_string(d, "lower"), lower)
        self.assertEqual(tbs.conversion.diss.to_string(d, "lowerl", ','), lowerl)
        self.assertEqual(tbs.conversion.diss.to_string(d, "lowerp", ','), lowerp)
