__author__ = 'francois'

import unittest

import os
from PIL import Image
import DLC.graphics.image


class TestToString(unittest.TestCase):
    def test_simple_image(self):
        matrix = [[0, 1], [1, 1]]
        output = os.path.join(os.path.dirname(__file__), "../..", "resources/test.png")
        DLC.graphics.image.create_image_from_matrix(matrix).save(output)
        image = Image.open(output)
        self.assertEqual((2, 2), image.size)
        self.assertNotEqual(image.getpixel((0, 0)), image.getpixel((0, 1)))
        self.assertEqual(1, len({image.getpixel((0, 1)), image.getpixel((1, 0)), image.getpixel((1, 1))}))
        os.remove(output)