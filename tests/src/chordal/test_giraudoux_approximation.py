import unittest


from tbs.chordal import approximate_to_chordal_diss, isa_chordal_diss, isa_totally_balanced_diss, \
    approximation_to_totally_balanced_diss


class TestDissGiraudouxApproximation(unittest.TestCase):
    def setUp(self):

        import tbs.diss._file_io
        import os.path

        filename = os.path.join(os.path.dirname(__file__), "../../resources/giraudoux.mat")
        f = open(filename)
        self.diss = tbs.diss._file_io.load(f)
        f.close()

    def test_chordal_approximation(self):
        self.assertFalse(isa_chordal_diss(self.diss))
        diss_chordal = approximate_to_chordal_diss(self.diss)
        self.assertTrue(isa_chordal_diss(diss_chordal))

    def test_totally_balanced_approximation(self):

        self.assertFalse(isa_totally_balanced_diss(self.diss))
        diss_totally_balanced = approximation_to_totally_balanced_diss(self.diss)
        self.assertTrue(isa_totally_balanced_diss(diss_totally_balanced))
