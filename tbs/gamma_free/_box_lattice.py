__author__ = 'fbrucker'

__all__ = ["box_lattice"]

from ..graph import DirectedGraph
from ..dismantlable import DismantlableLattice


def box_lattice(doubly_lexically_ordered_gamma_free):
    """Box lattice associated with a doubly lexically ordered gamma free context matrix

    The context matrix must be gamma free (otherwise `box_lattice(gamma_free.gamma_free.reorder_doubly_lexical())`). 
    No check are performed.

    Complexity is O(columns * lines)

    Args:
        doubly_lexically_ordered_gamma_free(GammaFree): doubly lexically ordered gama free context matrix.

    Returns(DismantlableLattice): lattice associated with the gamma free context matrix.
    """

    box_hase_diagram = DirectedGraph()

    box_matrix = ClusterLineFromMatrix.box_matrix(doubly_lexically_ordered_gamma_free.matrix)

    pile = [box_matrix[-1][0]]

    while pile:
        current = pile.pop()
        (line_begin, column_begin), (line_end, column_end) = current

        column = column_begin
        last_above = None

        while column <= column_end:
            line = line_begin - 1
            while line >= 0 and box_matrix[line][column] is None:
                line -= 1

            if line >= 0:
                above = box_matrix[line][column]
                box_hase_diagram.update([(current, above)])

                pile.append(above)
                last_above = above
                column = last_above[1][1] + 1
            else:
                column += 1

        column = column_end + 1

        while column < len(box_matrix[0]) and box_matrix[line_begin][column] is None:
            column += 1

        if column < len(box_matrix[0]):
            above = box_matrix[line_begin][column]
            if last_above is None or last_above[1][0] < above[0][0]:
                box_hase_diagram.update([(current, above)])

    return DismantlableLattice(box_hase_diagram)


class ClusterLineFromMatrix(object):

    @classmethod
    def box_matrix(cls, matrix):
        """ Cluster Matrix.

        Return a new matrix with the same dimensions. Each cell is equal to either None (if no box cluster) or a box
        representing the cluster. See [BP_15_ICFCA]_ for detailed explanations.

        A box is a couple ((l1, c1), (l2, c2)) where (l1, c1) is the top left corner (line, column) of the box and
        (l2, c2) the bottom right corner.

        :param matrix: doubly lexically ordered and Gamma free 0/1 matrix
        :return: a matrix with the same dimensions.
        """

        matrix = [current_line for current_line in cls(matrix)]

        cluster_correspondence = {None: None}

        for i, line in enumerate(matrix):
            for j, elem in enumerate(line):
                if elem is None:
                    continue
                if elem not in cluster_correspondence:
                    cluster_correspondence[elem] = ((i, j), (i, j))
                else:
                    begin, end = cluster_correspondence[elem]
                    cluster_correspondence[elem] = (begin, (i, j))

        return tuple(tuple(cluster_correspondence[x] for x in line) for line in matrix)

    def __init__(self, matrix):
        """

        :param matrix:   doubly lexically ordered and Gamma free 0/1 matrix.

        Add a last column full of 1 (top) and a last line full of 1 (bottom.
        """

        self.matrix = [list(line) + [1] for line in matrix]
        self.matrix.append([1] * (len(matrix[0]) + 1))

        self.current_line = None
        self.previous_line = None
        self.number_cluster = len(self.matrix)
        self.column_difference = self._compute_column_difference()

    def __iter__(self):
        for line in range(len(self.matrix)):
            self.current_line = [None] * len(self.matrix[line])
            cut = False
            for column in range(len(self.matrix[line]) - 1, -1, -1):
                if self.matrix[line][column] == 0:
                    continue

                if line and not cut and self.matrix[line - 1][column] == 1:
                    self.current_line[column] = self.previous_line[column]
                elif (line and self.matrix[line - 1][column] == 0) or cut or line == 0:
                    cut = True
                    self.current_line[column] = self.number_cluster
                    self.number_cluster += 1

            for column in range(len(self.matrix[0]) - 1):
                if self.matrix[line][column] == self.matrix[line][column + 1] == 1 \
                        and line > self.column_difference[column]:
                    self.current_line[column + 1] = self.current_line[column]

            yield self.current_line
            self.previous_line = self.current_line

    def _compute_column_difference(self):
        column_difference = [-1] * len(self.matrix[0])
        for j in range(len(self.matrix[0]) - 2, -1, -1):
            for i in range(len(self.matrix) - 1, -1, -1):
                if column_difference[j] == -1 and self.matrix[i][j] != self.matrix[i][j + 1]:
                    column_difference[j] = i
                    break
        return column_difference

