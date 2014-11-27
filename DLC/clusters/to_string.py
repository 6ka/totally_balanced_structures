__author__ = 'francois'

import math

from .clusters import boxes_clusters


def clusters_to_string(clusters, line_labels=None, column_labels=None):
    if line_labels is None:
        line_labels = list(range(len(clusters)))
    if column_labels is None:
        column_labels = list(range(len(clusters[0])))
    return DecompositionToString(clusters, False, line_labels, column_labels).run()


class DecompositionToString(object):
    def __init__(self, clusters, draw_edges, line_order, column_order):

        self.draw_edges = draw_edges

        self.box_y, self.box_x = boxes_clusters(clusters)
        self.clusters = self.box_x.keys()
        self.column_length = self.compute_length(line_order, column_order)
        self.ascii_matrix = AsciiMatrix(self.column_length, line_order, column_order)

    def draw_right_edge(self, max_x, min_y, max_y, neighbor_min_x):

        line_edge = (min_y + max_y) // 2
        if (max_y - min_y + 1) % 2 == 1:
            line = self.ascii_matrix.matrix[line_edge + 1]
            border = self.ascii_matrix.border_right[line_edge + 1]
        else:
            line = self.ascii_matrix.border_bottom[line_edge + 1]
            border = self.ascii_matrix.border_corner[line_edge + 1]

        # noinspection PyArgumentList
        for j in range(max_x + 1, neighbor_min_x - 1):
            line[j + 1] = AsciiCharacter.edge_right(line[j + 1])
            border[j + 1] = AsciiCharacter.edge_right(border[j + 1])
        line[neighbor_min_x - 1 + 1] = AsciiCharacter.edge_right(line[neighbor_min_x - 1 + 1])

    def draw_up_edge(self, min_y, neighbor_max_x, neighbor_max_y, neighbor_min_x):
        if (neighbor_max_x - neighbor_min_x + 1) % 2 == 1:
            line = self.ascii_matrix.matrix
            border = self.ascii_matrix.border_bottom
        else:
            line = self.ascii_matrix.border_right
            border = self.ascii_matrix.border_corner

        column_label = (neighbor_max_x + neighbor_min_x) // 2
        # noinspection PyArgumentList
        for i in range(neighbor_max_y + 1, min_y):
            line[i + 1][column_label + 1] = AsciiCharacter.edge_up(line[i + 1][column_label + 1])
        # noinspection PyArgumentList
        for i in range(neighbor_max_y + 1, min_y - 1):
            border[i + 1][column_label + 1] = AsciiCharacter.edge_up(border[i + 1][column_label + 1])

    def run(self):

        for vertex in self.clusters:

            min_x, max_x = self.box_x[vertex]
            min_y, max_y = self.box_y[vertex]

            self.draw_box(min_x, max_x, min_y, max_y, str(vertex))

            if self.draw_edges:
                for neighbor in self.clusters["lattice"][vertex]:
                    if neighbor == self.clusters["top"]:
                        continue

                    neighbor_min_x, neighbor_max_x = self.box_x[neighbor]
                    neighbor_min_y, neighbor_max_y = self.box_y[neighbor]

                    if neighbor_min_x > max_x + 1:
                        self.draw_right_edge(max_x, min_y, max_y, neighbor_min_x)
                    elif neighbor_max_y + 1 < min_y:
                        self.draw_up_edge(min_y, neighbor_max_x, neighbor_max_y, neighbor_min_x)

        return self.ascii_matrix.final_matrix()

    def compute_length(self, line_order, column_order):
        column_length = [len(str(x)) for x in column_order]

        for element in self.clusters:
            label_length = len(str(element))
            number_separation = self.box_x[element][1] - self.box_x[element][0]
            min_column_length = math.ceil(
                (label_length - number_separation) / (self.box_x[element][1] - self.box_x[element][0] + 1))

            # noinspection PyArgumentList
            for j in range(self.box_x[element][0], self.box_x[element][1] + 1):
                column_length[j] = max(column_length[j], min_column_length)

        column_length.insert(0, max([len(str(element)) for element in line_order]))

        return column_length

    def draw_box(self, min_x, max_x, min_y, max_y, label):
        self.inner_box(max_x, max_y, min_x, min_y)
        self.border_box(max_x, max_y, min_x, min_y)
        self.label_box(label, max_x, max_y, min_x, min_y)

    def inner_box(self, max_x, max_y, min_x, min_y):
        AsciiCharacter.fill_empty_cluster(self.ascii_matrix.border_corner, min_x, max_x - 1, min_y, max_y - 1)
        AsciiCharacter.fill_empty_cluster(self.ascii_matrix.border_bottom, min_x, max_x - 1, min_y, max_y - 1)
        AsciiCharacter.fill_empty_cluster(self.ascii_matrix.border_right, min_x, max_x - 1, min_y, max_y)
        AsciiCharacter.fill_empty_cluster(self.ascii_matrix.matrix, min_x, max_x, min_y, max_y)


    def border_box(self, max_x, max_y, min_x, min_y):
        # noinspection PyArgumentList
        for i in range(min_y, max_y + 1):
            self.ascii_matrix.border_right[i + 1][max_x + 1] = AsciiCharacter.BORDER
            self.ascii_matrix.border_right[i + 1][min_x + 1 - 1] = AsciiCharacter.BORDER

        for i in range(min_y, max_y):
            self.ascii_matrix.border_corner[i + 1][max_x + 1] = AsciiCharacter.BORDER
            self.ascii_matrix.border_corner[i + 1][min_x + 1 - 1] = AsciiCharacter.BORDER

        for j in range(min_x, max_x + 1):
            self.ascii_matrix.border_bottom[min_y - 1 + 1][j + 1] = AsciiCharacter.BOTTOM * len(self.ascii_matrix.border_bottom[min_y - 1 + 1][j + 1])
            self.ascii_matrix.border_bottom[max_y + 1][j + 1] = AsciiCharacter.BOTTOM * len(self.ascii_matrix.border_bottom[max_y + 1][j + 1])

        for j in range(min_x, max_x):
            self.ascii_matrix.border_corner[min_y - 1 + 1][j + 1] = AsciiCharacter.BOTTOM
            self.ascii_matrix.border_corner[max_y + 1][j + 1] = AsciiCharacter.BOTTOM

        self.ascii_matrix.border_corner[min_y - 1 + 1][min_x - 1 + 1] = AsciiCharacter.CORNER
        self.ascii_matrix.border_corner[max_y + 1][min_x - 1 + 1] = AsciiCharacter.CORNER
        self.ascii_matrix.border_corner[min_y - 1 + 1][max_x + 1] = AsciiCharacter.CORNER
        self.ascii_matrix.border_corner[max_y + 1][max_x + 1] = AsciiCharacter.CORNER


    def label_box(self, label, max_x, max_y, min_x, min_y):
        line_label = (min_y + max_y) // 2
        if (max_y - min_y + 1) % 2 == 1:
            line = self.ascii_matrix.matrix[line_label + 1]
            border = self.ascii_matrix.border_right[line_label + 1]
        else:
            line = self.ascii_matrix.border_bottom[line_label + 1]
            border = self.ascii_matrix.border_corner[line_label + 1]

        vertex_label = label.center(max_x - min_x + sum(self.column_length[min_x + 1:max_x + 2]), AsciiCharacter.EMPTY)
        offset = 0
        # noinspection PyArgumentList
        for j in range(min_x, max_x):
            line[j + 1] = vertex_label[offset:offset + self.column_length[j + 1]]
            offset += self.column_length[j + 1]
            border[j + 1] = vertex_label[offset]
            offset += 1
        line[max_x + 1] = vertex_label[offset:]


class AsciiCharacter:
    LABEL_BORDER_RIGHT = "|"
    LABEL_BORDER_BOTTOM = "-"
    BORDER = "|"
    CORNER = "+"
    BOTTOM = "-"
    EMPTY = " "
    EMPTY_CLUSTER = "."
    EDGE_UP = "|"
    EDGE_RIGHT = "-"
    EDGE_INTERSECTION = "*"

    @classmethod
    def edge_up(cls, str_to_replace):
        middle = len(str_to_replace) // 2
        return AsciiCharacter.replace(str_to_replace[middle], AsciiCharacter.EDGE_RIGHT, AsciiCharacter.EDGE_UP).join(
            [str_to_replace[:middle], str_to_replace[middle + 1:]])

    @classmethod
    def edge_right(cls, str_to_replace):
        edge = ""
        for char in str_to_replace:
            edge += AsciiCharacter.replace(char, AsciiCharacter.EDGE_UP, AsciiCharacter.EDGE_RIGHT)
        return edge

    @classmethod
    def replace(cls, char_to_replace, by_intersection, default_char):
        return char_to_replace == by_intersection and AsciiCharacter.EDGE_INTERSECTION or default_char


    @classmethod
    def init_matrix(cls, line_labels, column_labels, column_length):
        #noinspection PyUnusedLocal
        ascii_matrix = [[AsciiCharacter.EMPTY_CLUSTER.center(length, AsciiCharacter.EMPTY) for length in column_length]
                        for j in range(len(line_labels) + 1)]

        ascii_matrix[0][0] = AsciiCharacter.EMPTY * len(ascii_matrix[0][0])
        for i in range(len(line_labels)):
            ascii_matrix[i + 1][0] = str(line_labels[i]).ljust(column_length[0], AsciiCharacter.EMPTY)
        for i in range(len(column_labels)):
            ascii_matrix[0][i + 1] = str(column_labels[i]).center(column_length[i + 1], AsciiCharacter.EMPTY)

        return ascii_matrix

    @classmethod
    def fill_empty_cluster(cls, matrix, min_x, max_x, min_y, max_y):
        """ + 1 on line and column because inner matrix."""
        # noinspection PyArgumentList
        for j in range(min_x, max_x + 1):
            # noinspection PyArgumentList
            for i in range(min_y, max_y + 1):
                matrix[i + 1][j + 1] = AsciiCharacter.EMPTY * len(matrix[i + 1][j + 1])


class AsciiMatrix(object):
    def __init__(self, column_length, line_order, column_order):
        self.column_length = column_length
        self.matrix = AsciiCharacter.init_matrix(line_order, column_order, column_length)
        self.border_right = self.init_right()
        self.border_bottom = self.init_matrix_bottom()
        self.border_corner = self.init_matrix_corner()


    def init_right(self):
        #noinspection PyUnusedLocal
        border_right = [[AsciiCharacter.EMPTY] * len(self.matrix[0]) for i in range(len(self.matrix))]

        for line in border_right:
            line[0] = AsciiCharacter.LABEL_BORDER_RIGHT

        return border_right

    def init_matrix_bottom(self):
        # noinspection PyUnusedLocal
        border_bottom = [[AsciiCharacter.EMPTY * length for length in self.column_length] for j in
                         range(len(self.matrix))]

        for j in range(len(border_bottom[0])):
            border_bottom[0][j] = AsciiCharacter.LABEL_BORDER_BOTTOM * self.column_length[j]

        return border_bottom

    def init_matrix_corner(self):
        # noinspection PyUnusedLocal
        matrix_corner =  [[AsciiCharacter.EMPTY] * len(self.matrix[0]) for i in range(len(self.matrix))]
        matrix_corner[0] = [AsciiCharacter.CORNER] * len(self.matrix[0])
        for line in matrix_corner:
            line[0] = AsciiCharacter.CORNER
        return matrix_corner

    def final_matrix(self):
        final_matrix = []
        for i in range(len(self.matrix)):
            line = []
            for j in range(len(self.matrix[i])):
                line.append(self.matrix[i][j])
                line.append(self.border_right[i][j])
            final_matrix.append(line)
            line = []
            for j in range(len(self.matrix[i])):
                line.append(self.border_bottom[i][j])
                line.append(self.border_corner[i][j])
            final_matrix.append(line)
        return "".join(["".join(line + ["\n"]) for line in final_matrix])