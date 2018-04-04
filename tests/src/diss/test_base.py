# -*- coding: utf-8 -*-

import random
import unittest
from tbs.diss import Diss
import tbs.diss


class TestDissBase(unittest.TestCase):
    def test_init(self):
        """Initialization, setting and getting attributes."""

        d = Diss(range(1, 6))
        d.update(lambda x, y: 5)
        self.d = d
        self.assertEqual(len(self.d._vertex), 5)
        self.assertEqual(len(self.d.vertex_index), 5)

        for i, x in enumerate(self.d):
            self.assertEqual(x, self.d._vertex[i])
            self.assertEqual(i, self.d.vertex_index[x])
        self.assertEqual(len(self.d), 5)
        self.assertEqual(len(self.d._d), 5)

        for i, x in enumerate(self.d._d):
            self.assertEqual(len(x), 5 - i)
        for x in self.d:
            for y in self.d:
                if x == y:
                    self.assertEqual(self.d(x, y), 0)
                else:
                    self.assertEqual(self.d(x, y), 5)
        self.d._d[1][1] = 2
        self.assertEqual(self.d(2, 3), 2)
        self.d[2, 3] = 6
        self.assertEqual(self.d._d[1][1], 6)
        self.d[3, 2] = 19
        self.assertEqual(self.d(2, 3), 19)
        self.d._d[4][0] = 12
        self.assertEqual(self.d(5, 5), 12)

        d = Diss(reversed(range(5)), value=None)

        for x in d:
            for y in d:
                self.assertEqual(d(x, y), None)

        d = Diss(range(5))
        d.update(lambda x, y: random.randint(1, 5))

        self.assertEqual(d._vertex, list(d))
        val = set()
        valsd = d.values()
        for x in d:
            for y in d:
                if x != y:
                    self.assertTrue(d(x, y) in valsd)
                    val.add(d(x, y))
                else:
                    self.assertFalse(d(x, y) in valsd)

        self.assertEqual(val, valsd)
        valsdzero = d.values(True)
        self.assertEqual(len(valsd) + 1, len(valsdzero))
        self.assertTrue(0 in valsdzero)
        self.assertFalse(0 in valsd)

    def test_copy(self):
        """Copy and restriction"""

        d = Diss(range(6))
        d.update(lambda x, y: 5, True)

        dprim = d.copy()
        self.assertEqual(set(dprim), set(d))
        self.assertEqual(dprim.values(True), dprim.values(True))
        dprim.remove(0)
        self.assertNotEqual(set(dprim), set(d))
        self.assertEqual(len(dprim) + 1, len(d))
        dprim = d.copy()
        for x in d:
            for y in d:
                self.assertEqual(d(x, y), dprim(x, y))

        dprim = d.restriction([1, 3, 5])
        self.assertEqual(set(dprim), {1, 3, 5})
        for x in dprim:
            for y in dprim:
                self.assertEqual(d(x, y), dprim(x, y))

    def test_combine(self):
        """Combining dissimilarities."""

        d = Diss(range(5))
        d.update(lambda x, y: x + y, True)
        dprim = Diss(range(7))
        dprim.update(lambda x, y: x + y)

        d2 = d + dprim
        for x in d:
            for y in d:
                self.assertEqual(d2(x, y), d(x, y) + dprim(x, y))

        d2 = d - dprim
        for x in d:
            for y in d:
                self.assertEqual(d2(x, y), d(x, y) - dprim(x, y))

        d2 = d * dprim
        for x in d:
            for y in d:
                self.assertEqual(d2(x, y), d(x, y) * dprim(x, y))

        d2 = d / dprim
        for x in d:
            for y in d:
                if x == y:
                    self.assertEqual(d2(x, y), d(x, y))
                else:
                    self.assertEqual(d2(x, y), d(x, y) / dprim(x, y))
        d2 = d.copy()
        d2 += 1
        for x in d:
            for y in d:
                if x == y:
                    self.assertEqual(d2(x, y), d(x, y))
                else:
                    self.assertEqual(d2(x, y), d(x, y) + 1)

        d2 = d.copy()
        d2 -= 1
        for x in d:
            for y in d:
                if x == y:
                    self.assertEqual(d2(x, y), d(x, y))
                else:
                    self.assertEqual(d2(x, y), d(x, y) - 1)

        d2 = d.copy()
        d2 *= 4
        for x in d:
            for y in d:
                if x == y:
                    self.assertEqual(d2(x, y), d(x, y))
                else:
                    self.assertEqual(d2(x, y), 4 * d(x, y))
        d2 = d.copy()
        d2 /= 1.3
        for x in d:
            for y in d:
                if x == y:
                    self.assertEqual(d2(x, y), d(x, y))
                else:
                    self.assertEqual(d2(x, y), d(x, y) / 1.3)

        d2 = -d
        for x in d:
            for y in d:
                self.assertEqual(d2(x, y), -d(x, y))

        d2 = +d
        for x in d:
            for y in d:
                self.assertEqual(d2(x, y), d(x, y))

        d2 = abs(-d)
        assert callable(d2)
        for x in d:
            for y in d:
                self.assertEqual(d2(x, y), abs(-d(x, y)))


class testStringAndJson(unittest.TestCase):
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
        self.assertEqual(tbs.diss.to_string(d, "squarel"), squarel)
        self.assertEqual(tbs.diss.to_string(d, "squarep"), squarep)
        self.assertEqual(tbs.diss.to_string(d, "upper"), upper)
        self.assertEqual(tbs.diss.to_string(d, "upperl"), upperl)
        self.assertEqual(tbs.diss.to_string(d, "upperp"), upperp)
        self.assertEqual(tbs.diss.to_string(d, "lower"), lower)
        self.assertEqual(tbs.diss.to_string(d, "lowerl", ','), lowerl)
        self.assertEqual(tbs.diss.to_string(d, "lowerp", ','), lowerp)

    def test_json(self):
        d = Diss(range(5, 10)).update(lambda x, y: x + y, True)
        self.assertEqual({'elements': [5, 6, 7, 8, 9],
                          'matrix': [[10],
                                     [11, 12],
                                     [12, 13, 14],
                                     [13, 14, 15, 16],
                                     [14, 15, 16, 17, 18]]},
                         d.json())
        self.assertEqual(d, Diss.from_json(d.json()))

        self.assertEqual(Diss(range(5)).update(lambda x, y: 10 + x + y, True),
                         Diss.from_json({'matrix': [[10, 11, 12, 13, 14],
                                                    [11, 12, 13, 14, 15],
                                                    [12, 13, 14, 15, 16],
                                                    [13, 14, 15, 16, 17],
                                                    [14, 15, 16, 17, 18]
                                                    ]}))

        self.assertEqual(Diss(range(5)).update(lambda x, y: 10 + x + y, True),
                         Diss.from_json({'matrix': [[10, 11, 12, 13, 14],
                                                        [12, 13, 14, 15],
                                                            [14, 15, 16],
                                                                [16, 17],
                                                                    [18]
                                                    ]}))
