from matplotlib import pyplot
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

from clusters.cover_graph import cover_graph_and_boxes_from_matrix
from diss import Diss
from lattice import sup_irreducible, sup_irreducible_clusters, inf_irreducible

import randomize
from subdominant import subdominant

__author__ = 'fbrucker'

import sys
import os

sys.path.append(os.path.dirname('../'))

from DLC.contextmatrix import ContextMatrix
import DLC.graphics.lattice_string
import DLC.diss.file_io


class Chain_robinson_matrix:
    UNMARKED = -1
    INITIAL_HEIGHT = 0
    EMPTY = None

    def __init__(self, matrix):
        self.number_lines = len(matrix)
        self.number_columns = len(matrix[0])
        self.current_height = self.INITIAL_HEIGHT
        self.height_matrix = self.init_height_matrix(matrix)

    def init_height_matrix(self, matrix):
        height_matrix = [[matrix[i][j] and self.UNMARKED or self.EMPTY for j in range(self.number_columns)]
                         for i in range(self.number_lines)]
        return height_matrix

    def run(self):

        path = [(self.number_lines - 1, self.number_columns - 1)]

        while path:

            current_end_path = path[-1]


            left = self.next_unmarked(current_end_path, (0, -1))
            if left:
                path.append(left)
                continue
            up = self.next_unmarked(current_end_path, (-1, 0))
            if up:
                path.append(up)
                continue

            current_line, current_column = current_end_path
            if self.height_matrix[current_line][current_column] == self.UNMARKED:
                self.propagate(current_end_path)
                self.current_height += 1

            path.pop()
        return self

    def next_unmarked(self, begin, increment):
        current_line, current_column = begin
        increment_line, increment_column = increment

        current_line += increment_line
        current_column += increment_column

        while 0 <= current_line < self.number_lines and 0 <= current_column < self.number_columns:

            if self.height_matrix[current_line][current_column] == self.UNMARKED:
                return current_line, current_column

            current_line += increment_line
            current_column += increment_column

        return tuple()

    def propagate(self, begin):
        current_line, current_column = begin
        self.height_matrix[current_line][current_column] = self.current_height
        elements_to_mark = [begin]
        while elements_to_mark:
            current = elements_to_mark.pop()
            self.mark(current)
            right = self.next_unmarked(current, (0, +1))
            if right:
                elements_to_mark.append(right)

            bottom = self.next_unmarked(current, (+1, 0))
            if bottom:
                elements_to_mark.append(bottom)

    def mark(self, element):
        current_line, current_column = element
        self.height_matrix[current_line][current_column] = self.current_height


def context_matrix_from_qu_arbo(original_dissimilarity):
    approximation = subdominant(original_dissimilarity)

    matrix = [[] for i in range(len(approximation))]
    known_two_balls = set()
    for i in range(len(approximation)):
        for j in range(i + 1, len(approximation)):

            two_ball = frozenset({z for z in range(len(approximation)) if
                                  approximation.get_by_pos(i, j) >= max(approximation.get_by_pos(i, z),
                                                                        approximation.get_by_pos(j, z))})
            if two_ball in known_two_balls:
                continue
            for line in matrix:
                line.append(0)
            for z in two_ball:
                matrix[z][-1] = 1

    context_matrix = ContextMatrix(matrix, elements=list(approximation), copy_matrix=False)
    context_matrix.reorder_doubly_lexical_order()
    return context_matrix


def dissimilarity_from_dismantlable_cover_graph(dismantable_lattice):
    clusters = sup_irreducible_clusters(dismantable_lattice)
    elements = list(sup_irreducible(dismantable_lattice))
    diss = Diss(elements)
    for x_pos in range(len(elements)):
        x = elements[x_pos]
        for y_pos in range(x_pos + 1, len(elements)):
            y = elements[y_pos]

            current_dissimilarity = None
            for cluster_name, cluster in clusters.items():
                if x in cluster and y in cluster:
                    if current_dissimilarity is None or len(cluster) < current_dissimilarity:
                        current_dissimilarity = len(cluster)
            diss[x, y] = current_dissimilarity
    return diss


def lattices_and_points(context_matrix):
    cover_graph, boxes_cluster_line, boxes_cluster_columns = cover_graph_and_boxes_from_matrix(context_matrix.matrix)
    representant = dict()
    for elem in boxes_cluster_line:
        representant[elem] = .5 * sum(boxes_cluster_line[elem]), .5 * sum(boxes_cluster_columns[elem])

    representant["BOTTOM"] = len(context_matrix.matrix), len(context_matrix.matrix[0])
    representant["TOP"] = 0, len(context_matrix.matrix[0])

    return representant, cover_graph


def point_transformation_square(max_y):
    return lambda line, column: (column, max_y - line)


def draw(plot2d, cover_graph, point_transformation, representant, colors):
    objects = sup_irreducible(cover_graph)
    attributes = inf_irreducible(cover_graph)

    for elem in cover_graph:
        x, y = point_transformation(*representant[elem])
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        plot2d.scatter(x, y, marker=type, zorder=1, color=colors(*representant[elem]), edgecolors='black')
        # plot2d.annotate(str(elem), xy=(x, max_y - y), color="grey")

        for neighbor in cover_graph[elem]:

            x2, y2 = point_transformation(*representant[neighbor])
            plot2d.plot([x, x2], [y, y2], color="black", zorder=0, linestyle="-")


def draw_boxes(plot2d, matrix, point_transformation, colors):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] is None:
                continue
            x, y = point_transformation(i, j)

            plot2d.scatter(x, y, color=colors(i, j))

def draw_2d_vertices(plot, rectangles):
    from matplotlib.patches import Rectangle

    for rectangle in rectangles.values():
        plot.add_patch(rectangle)


def rect_matrices(boxes):

    from matplotlib.patches import Rectangle
    associaded_rect = {}
    for elem in boxes:
        (min_x, min_y), (max_x, max_y) = boxes[elem]
        rect = Rectangle((min_x, min_y), max_x - min_x + 1, max_y - min_y + 1, picker=1)
        associaded_rect[elem] = rect

    return associaded_rect


def draw3d(plot2d, cover_graph, point_transformation, representant, height, colors):
    objects = sup_irreducible(cover_graph)
    attributes = inf_irreducible(cover_graph)

    for elem in cover_graph:
        x, y = point_transformation(*representant[elem])
        z = height(*representant[elem])
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"

        x, y, z = z, -x, y
        plot2d.scatter(x, y, z, marker=type, zorder=1, color=colors(*representant[elem]), edgecolors='black')
        # plot2d.annotate(str(elem), xy=(x, max_y - y), color="grey")

        for neighbor in cover_graph[elem]:

            x2, y2 = point_transformation(*representant[neighbor])
            z2 = height(*representant[neighbor])
            if z2 > z:
                color = colors(*representant[neighbor])
            else:
                color = colors(*representant[elem])
            x2, y2, z2 = z2, -x2, y2
            plot2d.plot([x, x2], [y, y2], [z, z2], color=color, zorder=0, linestyle="-")

if __name__ == "__main__":
    LATTICE_NUMBER_VERTICES = 13
    DISSIMILARITY_FILENAME = "resources/giraudoux.mat"
    if DISSIMILARITY_FILENAME:
        dissimilarity = subdominant(DLC.diss.file_io.load(open(DISSIMILARITY_FILENAME)))
    else:
        dissimilarity = dissimilarity_from_dismantlable_cover_graph(randomize.random_dismantable_lattice(LATTICE_NUMBER_VERTICES))

    context_matrix = context_matrix_from_qu_arbo(dissimilarity)

    print(DLC.graphics.from_context_matrix(context_matrix))
    chain_robinson = Chain_robinson_matrix(context_matrix.matrix).run()
    height_matrix = chain_robinson.height_matrix
    number_color = chain_robinson.current_height
    print(number_color)
    # for line in height_matrix:
    #     print(line)


    plot2d = pyplot.subplot2grid((2, 1), (0, 0))
    point_transformation = point_transformation_square(len(context_matrix.matrix))
    representant, cover_graph = lattices_and_points(context_matrix)
    colors = matplotlib.cm.rainbow([0. + 1.0 * x / (number_color - 1) for x in range(number_color)])

    def get_color(x, y):
        x, y = int(x), int(y)
        if x >= len(height_matrix) or y >= len(height_matrix[0]):
            return colors[0]
        else:
            if height_matrix[x][y] == 0:
                return "black"
            return colors[height_matrix[x][y]]

    # draw(plot2d, cover_graph, point_transformation, representant, get_color)
    draw_boxes(plot2d, height_matrix, point_transformation, get_color)

    def get_z(x, y):
        if x >= len(height_matrix) or y >= len(height_matrix[0]):
            return 0
        return 10 * height_matrix[int(x)][int(y)]

    plot3d = pyplot.subplot2grid((2, 1), (1, 0), projection='3d')
    draw3d(plot3d, cover_graph, point_transformation, representant, get_z, get_color)

    pyplot.show()