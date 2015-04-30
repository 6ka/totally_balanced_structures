from matplotlib import pyplot
import matplotlib
from matplotlib.patches import Rectangle

from clusters.cover_graph import cover_graph_and_boxes_from_matrix
from diss import Diss
from graph import Graph
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
        self.generators = []

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
                self.generators.append(current_end_path)
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

    def get_height(self, box):
        (min_line, max_line), (min_column, max_column) = box
        return self.height_matrix[max_line][max_column]

    def reorder_bottom_up(self):
        self.height_matrix = [[self.height_matrix[i][j] is not self.EMPTY and self.UNMARKED or self.EMPTY for j in
                               range(self.number_columns)]
                              for i in range(self.number_lines)]
        generators = list(self.generators)
        generators.sort()
        generators.reverse()
        self.current_height = self.INITIAL_HEIGHT
        for end_path in generators:
            self.propagate(end_path)
            self.current_height += 1

        return self


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
            known_two_balls.add(two_ball)

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
    cluster_matrix = [[None] * len(context_matrix.matrix[0]) for i in range(len(context_matrix.matrix))]
    representant = dict()
    for elem in boxes_cluster_line:
        representant[elem] = boxes_cluster_line[elem], boxes_cluster_columns[elem]
        for i in range(boxes_cluster_line[elem][0], boxes_cluster_line[elem][1] + 1):
            for j in range(boxes_cluster_columns[elem][0], boxes_cluster_columns[elem][1] + 1):
                cluster_matrix[i][j] = elem

    return representant, cover_graph, cluster_matrix


def draw_2D_lattice(plot2d, cover_graph, point_transformation):
    objects = sup_irreducible(cover_graph)
    attributes = inf_irreducible(cover_graph)

    for elem in cover_graph:
        coordinates = point_transformation(elem)
        if coordinates is None:
            continue
        x, y = coordinates
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        plot2d.scatter(x, y, marker=type, zorder=1, edgecolors='black')
        plot2d.annotate(str(elem), xy=(x, y), color="grey")


def draw_2D_boxes(plot2d, cover_graph, point_transformation, representant, colors):
    for elem in cover_graph:
        if elem not in representant:
            continue

        (min_line, max_line), (min_column, max_column) = representant[elem]
        x, y = point_transformation(max_line + 1, min_column)
        color = colors(elem)
        rectangle = Rectangle((x, y), max_column - min_column + 1, max_line - min_line + 1, facecolor=color,
                              edgecolor="black", alpha=.2)
        plot2d.add_patch(rectangle)
        x_text, y_text = point_transformation(min_line, min_column)
        plot2d.annotate(str(elem), xy=(x_text, y_text),
                        color="grey", horizontalalignment='left', verticalalignment='top')

def draw_2D_box_edges(plot2d, cover_graph, point_transformation, representant):
    for elem in cover_graph:
        if elem not in representant:
            continue

        (min_line, max_line), (min_column, max_column) = representant[elem]

        neighbors = [neighbor for neighbor in cover_graph[elem] if neighbor in representant]
        neighbors.sort(key=lambda vertex: -representant[vertex][0][0])

        color = "black"

        for neighbor in neighbors:
            if neighbor not in representant:
                continue

            (min_line_neighbor, max_line_neighbor), (min_column_neighbor, max_column_neighbor) = representant[neighbor]

            if min_line + 1 == max_line_neighbor:
                color = "red"
                continue
            if max_column + 1 == min_column_neighbor:
                color = "red"
                continue

            if min_line > max_line_neighbor:
                x, y = point_transformation(min_line, .5 * (min_column_neighbor + max_column_neighbor + 1))
                x2, y2 = point_transformation(max_line_neighbor + 1, .5 * (min_column_neighbor + max_column_neighbor + 1))
            else:
                x, y = point_transformation(.5 * (min_line + max_line + 1), max_column + 1)
                x2, y2 = point_transformation(.5 * (min_line + max_line + 1), min_column_neighbor)
            plot2d.plot([x, x2], [y, y2], color=color, zorder=0, linestyle="-")
            color = "red"


def draw_2D_box_edges_full(plot2d, cover_graph, point_transformation, representant):
    for elem in cover_graph:
        if elem not in representant:
            continue

        (min_line, max_line), (min_column, max_column) = representant[elem]

        neighbors = [neighbor for neighbor in cover_graph[elem] if neighbor in representant]
        neighbors.sort(key=lambda vertex: -representant[vertex][0][0])

        color = "black"

        center_line = .5 * (min_line + max_line + 1)
        center_column = .5 * (min_column + max_column + 1)
        begin_x, begin_y = point_transformation(center_line, center_column)
        for neighbor in neighbors:
            if neighbor not in representant:
                continue

            (min_line_neighbor, max_line_neighbor), (min_column_neighbor, max_column_neighbor) = representant[neighbor]
            center_neighbor_line = .5 * (min_line_neighbor + max_line_neighbor + 1)
            center_neighbor_column = .5 * (min_column_neighbor + max_column_neighbor + 1)
            end_x, end_y = point_transformation(center_neighbor_line, center_neighbor_column)

            if min_line > max_line_neighbor:
                border_line = min_line
                border_column = center_neighbor_column
                border_line_neighbor = max_line_neighbor + 1
                border_column_neighbor = center_neighbor_column
            else:
                border_line = center_line
                border_column = max_column + 1
                border_line_neighbor = center_line
                border_column_neighbor = min_column_neighbor


            x1, y1 = point_transformation(border_line, border_column)
            x2, y2 = point_transformation(border_line_neighbor, border_column_neighbor)

            plot2d.plot([begin_x, x1, x2, end_x],
                        [begin_y, y1, y2, end_y], color=color, zorder=0, linestyle="-")
            color = "red"


def point_transformation_square(max_y):
    from math import pi, cos, sin
    def transformation(line, column):
        x, y = column, max_y - line
        return x, y
        # y *= 7
        # angle = pi / 4
        # x2 = cos(angle) * x - sin(angle) * y
        # y2 = sin(angle) * x + cos(angle) * y
        # return x2, y2
    return transformation


def point_transformation_middle(representant_box, point_transformation):
    def point_coordinates(elem):
        if elem not in representant:
            return None
        (min_line, max_line), (min_column, max_column) = representant_box[elem]
        center_line = .5 * (min_line + max_line + 1)
        center_column = .5 * (min_column + max_column + 1)
        x, y = point_transformation(center_line, center_column)

        return x, y

    return point_coordinates


if __name__ == "__main__":
    LATTICE_NUMBER_VERTICES = 13
    DISSIMILARITY_FILENAME = "resources/giraudoux.mat"
    if DISSIMILARITY_FILENAME:
        dissimilarity = subdominant(DLC.diss.file_io.load(open(DISSIMILARITY_FILENAME)))
    else:
        dissimilarity = dissimilarity_from_dismantlable_cover_graph(
            randomize.random_dismantable_lattice(LATTICE_NUMBER_VERTICES))

    context_matrix = context_matrix_from_qu_arbo(dissimilarity)
    representant, cover_graph, cluster_matrix = lattices_and_points(context_matrix)

    print(DLC.graphics.from_context_matrix(context_matrix))
    chain_robinson = Chain_robinson_matrix(context_matrix.matrix).run()
    chain_robinson.reorder_bottom_up()
    height_matrix = chain_robinson.height_matrix
    number_color = chain_robinson.current_height
    print("number of different robinsons:", number_color)

    point_transformation = point_transformation_square(len(context_matrix.matrix))
    colors = matplotlib.cm.rainbow([0. + 1.0 * x / (number_color - 1) for x in range(number_color)])
    color_from_representant = lambda elem: colors[chain_robinson.get_height(representant[elem])]

    plot2d = pyplot.subplot2grid((1, 1), (0, 0))
    plot2d.set_xlim([0, len(context_matrix.matrix[0])])
    plot2d.set_ylim([0, len(context_matrix.matrix)])

    BOXES = 0
    DRAW = BOXES_WITH_EDGES = 1
    LATTICE = 2


    if DRAW is BOXES:
        draw_2D_boxes(plot2d, cover_graph, point_transformation, representant,
                      color_from_representant)
    elif DRAW is BOXES_WITH_EDGES:
        draw_2D_boxes(plot2d, cover_graph, point_transformation, representant,
                      color_from_representant)
        draw_2D_box_edges(plot2d, cover_graph, point_transformation, representant)
    elif DRAW is LATTICE:
        draw_2D_lattice(plot2d, cover_graph, point_transformation_middle(representant, point_transformation))
        draw_2D_box_edges_full(plot2d, cover_graph, point_transformation, representant)


    pyplot.show()