from PIL import Image
import colorsys

from ..dismantlable import DismantlableLattice

__all__ = ["create_image_from_dlo_gamma_free_matrix"]


def color_space_colors(number_colors):
    hsv_tuples = [(x * 1.0 / number_colors, 0.5, 0.5) for x in range(number_colors)]
    rgb_tuples = [tuple(int(255 * y) for y in colorsys.hsv_to_rgb(*x)) for x in hsv_tuples]

    return rgb_tuples


def color_space_grey(number_colors):

    rgb_tuples = [(int(x * 255 / number_colors), ) * 3 for x in range(number_colors)]

    return rgb_tuples


def create_image_from_dlo_gamma_free_matrix(matrix, color_space=color_space_colors, pixel_size=1):

    # height = hierarchical_height_from_lattice(from_dlo_gamma_free_matrix.lattice(matrix))
    height = DismantlableLattice.from_dlo_matrix(matrix).hierarchical_decomposition()
    height_colors = color_space(max(height.values()) + 1)

    image_matrix = Image.new("RGB", (len(matrix[0]) * pixel_size, len(matrix) * pixel_size), "white")
    for cluster in {key for key in height if key not in ("TOP", "BOTTOM")}:
        # for cluster in boxes_i:
        min_i, min_j = cluster[0]
        max_i, max_j = cluster[1]
        color = height_colors[height[cluster]]
        # color = (0, 0, 0)
        for i in range(min_i * pixel_size, (max_i + 1) * pixel_size):
            for j in range(min_j * pixel_size, (max_j + 1) * pixel_size):
                image_matrix.putpixel((j, i), color)

    return image_matrix

