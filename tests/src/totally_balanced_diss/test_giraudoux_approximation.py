import unittest


from tbs.totally_balanced_diss.chordal_diss import approximate_chordal_diss, isa_chordal_diss
from tbs.totally_balanced_diss.totally_balanced_diss import isa_totally_balanced_diss, \
    approximation_totally_balanced_diss


class TestDissGiraudouxApproximation(unittest.TestCase):
    def setUp(self):

        import tbs.diss.file_io
        import os.path

        filename = os.path.join(os.path.dirname(__file__), "../../resources/giraudoux.mat")
        f = open(filename)
        self.diss = tbs.diss.file_io.load(f)
        f.close()

    def test_chordal_approximation(self):
        self.assertFalse(isa_chordal_diss(self.diss))
        diss_chordal = approximate_chordal_diss(self.diss)
        self.assertTrue(isa_chordal_diss(diss_chordal))

    def test_totally_balanced_approximation(self):

        self.assertFalse(isa_totally_balanced_diss(self.diss))
        diss_totally_balanced = approximation_totally_balanced_diss(self.diss)
        self.assertTrue(isa_totally_balanced_diss(diss_totally_balanced))
