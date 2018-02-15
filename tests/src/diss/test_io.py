import unittest
import os
from tbs.diss import Diss
import tbs.diss


class TestDissImpexport(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), "../"))
        self.d = Diss(range(3))
        self.dprim = Diss(("label1", "label2", "3"))
        self.d[0, 1] = self.dprim["label1", "label2"] = 1
        self.d[0, 2] = self.dprim["label1", "3"] = 2
        self.d[1, 2] = self.dprim["label2", "3"] = 3    

    def test_type(self):
        """Import type."""
        
        f = open("../resources/test_load_1.mat")
        d = tbs.diss.load(f)
        f.close()
        self.assertEqual(d, self.d)
        f = open("../resources/test_load_2.mat")
        d = tbs.diss.load(f)
        f.close()
        self.assertEqual(d, self.dprim)
        f = open("../resources/test_load_3.mat")
        d = tbs.diss.load(f)
        f.close()
        self.assertEqual(d, self.d)
        f = open("../resources/test_load_4.mat")
        self.assertRaises(ValueError, tbs.diss.load, f)
        f.close()
        f = open("../resources/test_load_5.mat")
        d = tbs.diss.load(f)
        f.close()
        self.assertEqual(d, self.d)
        f = open("../resources/test_load_6.mat")
        d = tbs.diss.load(f)
        f.close()
        self.assertEqual(d, self.dprim)
        f = open("../resources/test_load_7.mat")
        d = tbs.diss.load(f)
        f.close()
        self.assertEqual(d, self.d)
        f = open("../resources/test_load_8.mat")
        d = tbs.diss.load(f)
        self.assertEqual(d, self.dprim)

        self.assertRaises(TypeError, tbs.diss.load, f, "a crazy type")
        self.assertRaises(ValueError, tbs.diss.load, f)
        f.close()
        dprim = Diss([0])
        f = open("../resources/test_load_9.mat")
        d = tbs.diss.load(f)
        f.close()
        self.assertEqual(d, dprim)
        f = open("../resources/test_load_10.mat")
        d = tbs.diss.load(f)
        f.close()
        dprim.rename(0, "label")
        self.assertEqual(d, dprim)
        f = open("../resources/test_load_11.mat")
        self.assertRaises(ValueError, tbs.diss.load, f)
        f.close()
        f = open("../resources/test_load_12.mat")
        self.assertRaises(ValueError, tbs.diss.load, f)
        f.close()
        f = open("../resources/test_load_13.mat")
        self.assertRaises(ValueError, tbs.diss.load, f)
        f.close()
        f = open("../resources/test_load_14.mat")
        self.assertRaises(ValueError, tbs.diss.load, f)
        f.close()

        f = open("../resources/test_load_1.mat")
        d = tbs.diss.load(f, number=False)
        f.close()
        dprim = self.d.copy()
        for x in dprim:
            for y in dprim:
                dprim[x, y] = str(dprim(x, y))

        self.assertEqual(d, dprim)

        f = open("../resources/test_write.mat", "w")
        tbs.diss.save(d, f)
        f.close()
        f = open("../resources/test_write.mat")
        d = tbs.diss.load(f)
        f.close()
        os.remove("../resources/test_write.mat")
        self.assertEqual(d, self.d)

        d = Diss(["Alpha", "Beta", "Gamma", "Delta", "Epsilon"])
        d["Alpha", "Beta"] = 1.000
        d["Alpha", "Gamma"] = 2.000
        d["Alpha", "Delta"] = 3.000
        d["Alpha", "Epsilon"] = 3.000
        d["Beta", "Gamma"] = 2.000
        d["Beta", "Delta"] = 3.000
        d["Beta", "Epsilon"] = 3.000
        d["Gamma", "Delta"] = 3.000
        d["Gamma", "Epsilon"] = 3.000
        d["Delta", "Epsilon"] = 1.000

        f = open("../resources/test_load_15.mat")
        dprim = tbs.diss.load(f)
        f.close()
        self.assertEqual(dprim, d)
        f = open("../resources/test_load_16.mat")
        dprim = tbs.diss.load(f)
        f.close()
        self.assertEqual(dprim, d)
        f = open("../resources/test_load_17.mat")
        dprim = tbs.diss.load(f)
        f.close()
        self.assertEqual(dprim, d)

        f = open("../resources/test_load_18.mat")
        dprim = tbs.diss.load(f)
        f.close()
        self.assertEqual(dprim, d.restriction(["Alpha"]))
        f = open("../resources/test_load_19.mat")
        dprim = tbs.diss.load(f)
        f.close()
        self.assertEqual(dprim, d.restriction(["Alpha"]))
