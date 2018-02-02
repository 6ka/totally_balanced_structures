# -*- coding: utf-8 -*-

import random
import unittest
from tbs.diss import Diss


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
        d.update(lambda  x, y: x + y, True)
        dprim = Diss(range(7))
        dprim.update(lambda  x, y: x + y)
        
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
                    self.assertEqual(d2(x, y), 4*d(x, y))
        d2 = d.copy()
        d2 /= 1.3
        for x in d:
            for y in d:
                if x == y:
                    self.assertEqual(d2(x, y), d(x, y))
                else:
                    self.assertEqual(d2(x, y), d(x, y)/1.3)
        
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