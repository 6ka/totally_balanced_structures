# -*- coding: utf-8 -*-

import unittest
from DLC.diss import Diss
import DLC.diss.conversion.to_string


class TestDissUtils(unittest.TestCase):
    def test_min_max(self):
        """Minimum and maximum of subsets."""
        
        d = Diss(range(5))
        d.update(lambda x, y: 5)
        self.d = d 
        
        self.d[0, 0] = 50
        self.d[3, 4] = 25
        self.d[1, 2] = 1
        
        the_min = self.d.min([0])
        self.assertEqual(the_min, 50)
        
        the_min = self.d.min(indices=True)
        self.assertEqual({the_min['x'], the_min['y']}, {1, 2})
        the_min = self.d.min(indices=True, index=True)
        self.assertEqual({the_min['x'], the_min['y']}, {1, 2})
        self.assertEqual(the_min['min'], 1)
        self.assertEqual(self.d.min(), 1)
        the_min = self.d.min(indices=True, xx=True)
        self.assertEqual(the_min['x'], the_min['y'])
        self.assertEqual(the_min['min'], 0)
        the_min = self.d.min(element_subset=[2, 3, 0, 1, 4], indices=True)
        self.assertEqual({the_min['x'], the_min['y']}, {1, 2})
        self.assertEqual(the_min['min'], 1)
        the_min = self.d.min(element_subset=[2, 4, 0], indices=True)
        self.assertTrue(the_min['x'] != the_min['y'])
        self.assertEqual(the_min['min'], 5)
        
        the_max = self.d.max([0])
        self.assertEqual(the_max, 50)
        
        the_max = self.d.max(indices=True)
        self.assertEqual({the_max['x'], the_max['y']}, {3, 4})
        self.assertEqual(the_max['max'], 25)
        self.assertEqual(self.d.max(), 25)
        the_max = self.d.max(indices=True, xx=True)
        self.assertEqual(the_max['x'], the_max['y'])
        the_max = self.d.max(indices=True, xx=True, index=True)
        self.assertEqual(the_max['x'], 0)
        self.assertEqual(the_max['y'], 0)
        self.assertEqual(the_max['x'], 0)
        self.assertEqual(the_max['max'], 50)
        the_max = self.d.max(element_subset=[2, 4, 0, 1, 3], indices=True)
        self.assertEqual({the_max['x'], the_max['y']}, {3, 4})
        self.assertEqual(the_max['max'], 25)
        the_max = self.d.max(element_subset=[2, 4, 0], indices=True)
        self.assertTrue(the_max['x'] != the_max['y'])
        self.assertEqual(the_max['max'], 5)
        
    def test_rank(self):
        """Ranks."""
        
        d = Diss(range(5))
        d.update(lambda  x, y: y + x)
        r = d.rank()
        for x in range(5):
            order = [i for i in range(5) if i != x]
            order.insert(0, x)
            for i, y in enumerate(order):
                self.assertEqual(r[x][y], i)
                
        elems = [0, 1, 4]
        r2 = d.rank(elems)
        for x in elems:
            order = [i for i in elems if i != x]
            order.insert(0, x)
            for i, y in enumerate(order):
                self.assertEqual(r2[x][y], i)
        
        d.update(lambda  x, y: 1)
        r = d.rank()        
        for x in range(5):
            for y in range(5):
                if x == y:
                    self.assertEqual(r[x][y], 0)
                else:
                    self.assertEqual(r[x][y], 1)

    def test_string(self):
        """String representation."""
        
        d = Diss(range(5))
        d.update(lambda  x, y: x + y, True)
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
        self.assertEqual(DLC.diss.conversion.to_string(d, "squarel"), squarel)
        self.assertEqual(DLC.diss.conversion.to_string(d, "squarep"), squarep)
        self.assertEqual(DLC.diss.conversion.to_string(d, "upper"), upper)
        self.assertEqual(DLC.diss.conversion.to_string(d, "upperl"), upperl)
        self.assertEqual(DLC.diss.conversion.to_string(d, "upperp"), upperp)
        self.assertEqual(DLC.diss.conversion.to_string(d, "lower"), lower)
        self.assertEqual(DLC.diss.conversion.to_string(d, "lowerl",','), lowerl)
        self.assertEqual(DLC.diss.conversion.to_string(d, "lowerp",','), lowerp)