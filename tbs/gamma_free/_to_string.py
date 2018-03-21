import math

from ._box_lattice import box_lattice


def to_string(doubly_lexically_ordered_gamma_free):
    """string representation with a doubly lexically ordered gamma free context matrix

    The context matrix must be gamma free (otherwise `box_lattice(gamma_free.gamma_free.reorder_doubly_lexical())`).
    No check are performed.

    Args:
        doubly_lexically_ordered_gamma_free(GammaFree): doubly lexically ordered gama free context matrix.

    Returns(str): lattice matrixical representation
    """

    lattice = box_lattice(doubly_lexically_ordered_gamma_free)
    boxes = list(lattice)

    attributes_labels = [str(x) for x in doubly_lexically_ordered_gamma_free.attributes] + ["⊤"]
    elements_labels = [str(x) for x in doubly_lexically_ordered_gamma_free.elements] + ["⊥"]

    box_label = {value: attributes_labels[value[0][1]] for value in boxes}
    box_label[lattice.bottom] = elements_labels[-1]
    box_label[lattice.top] = attributes_labels[-1]

    return BoxesToString(boxes,
                         elements_labels, attributes_labels,
                         box_label,
                         lattice).run()


class BoxesToString(object):
    def __init__(self, boxes, line_labels, column_labels, boxes_labels, lattice=None):

        self.lattice = lattice

        self.boxes = boxes
        self.line_labels = line_labels  # [label_line_0, ..., label_line_n-1]
        self.column_labels = column_labels  # [column_line_0, ..., column_line_n-1]
        self.boxes_labels = boxes_labels  # {box: box_label, ...}

        self.column_length = self.compute_length()

        self.ascii_matrix = AsciiMatrix(self.column_length, self.line_labels, self.column_labels)

    def draw_right_edge(self, max_x, min_y, max_y, neighbor_min_x):

        line_edge = (min_y + max_y) // 2
        if (max_y - min_y + 1) % 2 == 1:
            line = self.ascii_matrix.matrix[line_edge + 1]
            border = self.ascii_matrix.border_right[line_edge + 1]
        else:
            line = self.ascii_matrix.border_bottom[line_edge + 1]
            border = self.ascii_matrix.border_corner[line_edge + 1]

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
        for i in range(neighbor_max_y + 1, min_y):
            line[i + 1][column_label + 1] = AsciiCharacter.edge_up(line[i + 1][column_label + 1])
        for i in range(neighbor_max_y + 1, min_y - 1):
            border[i + 1][column_label + 1] = AsciiCharacter.edge_up(border[i + 1][column_label + 1])

    def run(self):
        for box in self.boxes:

            min_y, min_x = box[0]
            max_y, max_x = box[1]

            self.draw_box(min_x, max_x, min_y, max_y, str(self.boxes_labels[box]))

            if self.lattice:
                for neighbor in self.lattice.above(box):
                    if neighbor not in self.boxes:
                        continue

                    neighbor_min_y, neighbor_min_x = neighbor[0]
                    neighbor_max_y, neighbor_max_x = neighbor[1]

                    if neighbor_min_x > max_x + 1:
                        self.draw_right_edge(max_x, min_y, max_y, neighbor_min_x)
                    elif neighbor_max_y + 1 < min_y:
                        self.draw_up_edge(min_y, neighbor_max_x, neighbor_max_y, neighbor_min_x)

        return self.ascii_matrix.final_matrix()

    def compute_length(self):
        column_length = [len(str(x)) for x in self.column_labels]

        for box, box_label in self.boxes_labels.items():
            label_length = len(str(box_label))
            number_separation = box[1][1] - box[0][1]

            min_column_length = math.ceil(
                (label_length - number_separation) / (number_separation + 1))

            for j in range(box[0][1], box[1][1] + 1):
                column_length[j] = max(column_length[j], min_column_length)

        column_length.insert(0, max([len(str(element)) for element in self.line_labels]))

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
            self.ascii_matrix.border_bottom[min_y - 1 + 1][j + 1] = \
                AsciiCharacter.BOTTOM * len(self.ascii_matrix.border_bottom[min_y - 1 + 1][j + 1])
            self.ascii_matrix.border_bottom[max_y + 1][j + 1] = \
                AsciiCharacter.BOTTOM * len(self.ascii_matrix.border_bottom[max_y + 1][j + 1])

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
        ascii_matrix = []
        for j in range(len(line_labels) + 1):
            ascii_matrix.append(
                [AsciiCharacter.EMPTY_CLUSTER.center(length, AsciiCharacter.EMPTY) for length in column_length])

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
        border_right = []
        for i in range(len(self.matrix)):
            border_right.append([AsciiCharacter.EMPTY] * len(self.matrix[0]))

        for line in border_right:
            line[0] = AsciiCharacter.LABEL_BORDER_RIGHT

        return border_right

    def init_matrix_bottom(self):
        border_bottom = []
        for j in range(len(self.matrix)):
            border_bottom.append([AsciiCharacter.EMPTY * length for length in self.column_length])

        for j in range(len(border_bottom[0])):
            border_bottom[0][j] = AsciiCharacter.LABEL_BORDER_BOTTOM * self.column_length[j]

        return border_bottom

    def init_matrix_corner(self):
        matrix_corner = []
        for i in range(len(self.matrix)):
            matrix_corner.append([AsciiCharacter.EMPTY] * len(self.matrix[0]))
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
        return "\n".join(["".join(line) for line in final_matrix])
