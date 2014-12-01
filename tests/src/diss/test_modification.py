# -*- coding: utf-8 -*-

import unittest
from DLC.diss import Diss

class TestDissModification(unittest.TestCase):
    def test_update(self):
        """Update values."""
        
        d = Diss(range(3, 6))
        d.update(lambda x, y: 5)
        for x in d:
            for y in d:
                if x == y:
                    self.assertEqual(d(x,y), 0)
                else:
                    self.assertEqual(d(x,y), 5)
        d.update(lambda x,y: 3, True)
        for x in d:
            for y in d:
                self.assertEqual(d(x, y), 3)

    def test_rename(self):
        """Renaming elements."""
        
        d = Diss(range(5))
        d.update(lambda x, y: 5)
        self.d = d 
        
        self.d[2, 3] = 12
        self.d.rename(2, 9)
        self.assertFalse(2 in self.d)
        self.assertTrue(9 in self.d)
        self.assertEqual(self.d[9, 3], 12)
        self.assertEqual(self.d[9, 1], 5)
        self.assertEqual(self.d(9, 9), 0)
        
        self.assertRaises(ValueError, self.d.rename, 2, 9)
        self.assertRaises(ValueError, self.d.rename, 9, 1)
        
    def test_add_remove(self):
        """Adding or removing elements."""
        
        d = Diss(range(5))
        d.update(lambda x, y: 5)
        self.d = d 
        
        self.d.add(9)
        self.assertEqual(len(self.d), 6)
        self.assertEqual(self.d(9, 9), 0)
        self.assertEqual(self.d(9, 3), 0)
        self.d.remove(0)
        self.assertEqual(len(self.d), 5)
        
        self.assertRaises(ValueError, self.d.add, 9)
        self.assertRaises(ValueError, self.d.remove, "not in d")