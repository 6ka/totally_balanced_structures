import unittest

from TBS.clusters.to_image import create_image_from_dlo_gamma_free_matrix


class TestToString(unittest.TestCase):
    def test_simple_image(self):
        matrix = [[0, 1], [1, 1]]
        image = create_image_from_dlo_gamma_free_matrix(matrix)
        self.assertEqual((2, 2), image.size)
        self.assertNotEqual(image.getpixel((0, 0)), image.getpixel((0, 1)))
        self.assertEqual(1, len({image.getpixel((0, 1)), image.getpixel((1, 0)), image.getpixel((1, 1))}))
