__author__ = 'francois'

from PIL import Image
import colorsys

from DLC.clusters.cover_graph import cover_graph_and_boxes_from_matrix
from DLC.hierarchical_decomposition import hierarchical_height_from_lattice
import DLC.lattice


def create_image_from_matrix(matrix, orig_matrix=None):
    cover_graph, boxes_i, boxes_j = cover_graph_and_boxes_from_matrix(matrix)
    height = hierarchical_height_from_lattice(cover_graph)
    height_colors = color_space(max(height.values()) + 1)

    image_matrix = Image.new("RGB", (len(matrix[0]), len(matrix)), "white")
    bottom = DLC.lattice.get_bottom(cover_graph)
    top = DLC.lattice.get_top(cover_graph)
    for cluster in height:
    # for cluster in boxes_i:
        if cluster in (bottom, top):
            continue
        min_i, max_i = boxes_i[cluster]
        min_j, max_j = boxes_j[cluster]
        color = height_colors[height[cluster]]
        color = (0, 0, 0)
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):
                image_matrix.putpixel((j, i), color)

    if orig_matrix is not None:
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if orig_matrix[i][j] != matrix[i][j]:
                    image_matrix.putpixel((j, i), (255, 255, 255))
    return image_matrix


def color_space(number_colors):

    HSV_tuples = [(x * 1.0 / number_colors, 0.5, 0.5) for x in range(number_colors)]
    RGB_tuples = [tuple(int(255 * y) for y in colorsys.hsv_to_rgb(*x)) for x in HSV_tuples]
    RGB_tuples = [(int(x * 255 / number_colors), ) * 3  for x in range(number_colors)]
    return RGB_tuples