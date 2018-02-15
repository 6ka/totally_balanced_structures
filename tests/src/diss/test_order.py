import unittest
from tbs.diss import Diss
from tbs import diss


class TestOrder(unittest.TestCase):
    def test_min_max(self):
        """Minimum and maximum of subsets."""
        
        d = Diss(range(5))
        d.update(lambda x, y: 5)

        d[0, 0] = 50
        d[3, 4] = 25
        d[1, 2] = 1
        
        the_min = diss.min(d, [0])
        self.assertEqual(the_min, 50)
        
        the_min = diss.min(d, indices=True)
        self.assertEqual({1, 2}, {the_min['x'], the_min['y']})

        the_min = diss.min(d, indices=True, index=True)
        self.assertEqual({1, 2}, {the_min['x'], the_min['y']})

        self.assertEqual(1, the_min['min'])
        self.assertEqual(diss.min(d,), 1)
        the_min = diss.min(d, indices=True, xx=True)
        self.assertEqual(the_min['x'], the_min['y'])
        self.assertEqual(the_min['min'], 0)
        the_min = diss.min(d, element_subset=[2, 3, 0, 1, 4], indices=True)
        self.assertEqual({the_min['x'], the_min['y']}, {1, 2})
        self.assertEqual(the_min['min'], 1)
        the_min = diss.min(d, element_subset=[2, 4, 0], indices=True)
        self.assertTrue(the_min['x'] != the_min['y'])
        self.assertEqual(the_min['min'], 5)
        
        the_max = diss.max(d, [0])
        self.assertEqual(50, the_max)
        
        the_max = diss.max(d, indices=True)
        self.assertEqual({3, 4}, {the_max['x'], the_max['y']})
        self.assertEqual(the_max['max'], 25)
        self.assertEqual(diss.max(d, ), 25)
        the_max = diss.max(d, indices=True, xx=True)
        self.assertEqual(the_max['x'], the_max['y'])
        the_max = diss.max(d, indices=True, xx=True, index=True)
        self.assertEqual(the_max['x'], 0)
        self.assertEqual(the_max['y'], 0)
        self.assertEqual(the_max['x'], 0)
        self.assertEqual(the_max['max'], 50)
        the_max = diss.max(d, element_subset=[2, 4, 0, 1, 3], indices=True)
        self.assertEqual({the_max['x'], the_max['y']}, {3, 4})
        self.assertEqual(the_max['max'], 25)
        the_max = diss.max(d, element_subset=[2, 4, 0], indices=True)
        self.assertTrue(the_max['x'] != the_max['y'])
        self.assertEqual(the_max['max'], 5)
        
    def test_rank(self):
        """Ranks."""
        
        d = Diss(range(5))
        d.update(lambda x, y: y + x)
        r = diss.rank(d)
        for x in range(5):
            order = [i for i in range(5) if i != x]
            order.insert(0, x)
            for i, y in enumerate(order):
                self.assertEqual(r[x][y], i)
                
        elems = [0, 1, 4]
        r2 = diss.rank(d, elems)
        for x in elems:
            order = [i for i in elems if i != x]
            order.insert(0, x)
            for i, y in enumerate(order):
                self.assertEqual(r2[x][y], i)
        
        d.update(lambda x, y: 1)
        r = diss.rank(d)
        for x in range(5):
            for y in range(5):
                if x == y:
                    self.assertEqual(r[x][y], 0)
                else:
                    self.assertEqual(r[x][y], 1)
