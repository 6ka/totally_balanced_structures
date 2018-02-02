import unittest
from tbs.diss import Diss


class TestDissModification(unittest.TestCase):
    def test_update(self):
        """Update values."""
        
        d = Diss(range(3, 6))
        d.update(lambda x, y: 5)
        for x in d:
            for y in d:
                if x == y:
                    self.assertEqual(d(x, y), 0)
                else:
                    self.assertEqual(d(x, y), 5)
        d.update(lambda x, y: 3, True)
        for x in d:
            for y in d:
                self.assertEqual(d(x, y), 3)

    def test_update_by_pos(self):

        d = Diss(range(3, 6))
        d.update_by_pos(lambda x, y: x + y)
        for x in range(3):
            for y in range(3):
                if x == y:
                    self.assertEqual(d.get_by_pos(x, y), 0)
                else:
                    self.assertEqual(d.get_by_pos(x, y), x + y)

        d.update(lambda x, y: 3, True)
        for x in range(3):
            for y in range(3):
                self.assertEqual(d.get_by_pos(x, y), 3)

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