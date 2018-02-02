import unittest
from tbs.diss import Diss


class TestDissComparison(unittest.TestCase):
    def test_comparisons(self):
        """Comparisons."""
        
        d = Diss()
        self.assertFalse(d)
        d.add("an element")
        self.assertTrue(d)
        d.remove("an element")
        self.assertFalse(d)
        
        d = Diss(range(5))
        d.update(lambda x, y: x + y)
        dprim = Diss(range(5))
        dprim.update(lambda x, y: x + y)
        self.assertTrue(d == dprim)
        dprim.add("an element")
        self.assertFalse(d == dprim)
        self.assertFalse(d >= dprim)
        self.assertFalse(d <= dprim)
        self.assertFalse(d < dprim)
        self.assertFalse(d > dprim)
        self.assertTrue(d != dprim)
        dprim.remove("an element")
        dprim.rename(0, 9)
        self.assertFalse(d == dprim)
        self.assertFalse(d >= dprim)
        self.assertFalse(d <= dprim)
        self.assertFalse(d < dprim)
        self.assertFalse(d > dprim)
        dprim.rename(9, 0)
        self.assertTrue(d == dprim)
        self.assertTrue(d <= dprim)
        self.assertTrue(d >= dprim)
        self.assertFalse(d < dprim)
        self.assertFalse(d > dprim)
        d[1, 2] += 1
        self.assertTrue(d >= dprim)
        self.assertFalse(dprim >= d)
        self.assertTrue(d != dprim)
        self.assertTrue(dprim <= d)
        self.assertFalse(d <= dprim)
        self.assertTrue(d > dprim)
        self.assertFalse(dprim > d)
        self.assertTrue(dprim < d)
        self.assertFalse(d < dprim)
        self.assertFalse(d == dprim)