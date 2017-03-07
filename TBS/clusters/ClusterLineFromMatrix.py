__author__ = 'fbrucker'

__all__ = ["ClusterLineFromMatrix"]


class ClusterLineFromMatrix(object):

    def __init__(self, matrix):
        """

        :param matrix:   doubly lexically ordered and Gamma free 0/1 matrix
        """

        self.matrix = matrix
        self.current_line = None
        self.previous_line = None
        self.number_cluster = len(matrix)
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

    @staticmethod
    def cluster_matrix(matrix):
        """ Cluster Matrix.

        Return a new matrix with the same dimensions. Each cell is equal to either None (if no box cluster) or
        and integer (label of the cluster).

        Each integer forms a box representing the cluster. See [BP_15_ICFCA]_ for detailed explanations.

        :param matrix: doubly lexically ordered and Gamma free 0/1 matrix
        :return: a matrix with the same dimensions.
        """

        return [current_line for current_line in ClusterLineFromMatrix(matrix)]

    @staticmethod
    def boxes(matrix):
        """ Boxes and cluster number correspondence.

        A box is a couple ((l1, c1), (l2, c2)) where (l1, c1) is the top left corner (line, column) of the box and
        (l2, c2) the bottom right corner.

        :param matrix: Result from :meth:`ClusterLineFromMatrix.cluster_matrix`
        :return: :class:`dict` with key= class number and value= the associated box
        """

        cluster_correspondence = dict()

        for i, line in enumerate(ClusterLineFromMatrix(matrix)):
            for j, elem in enumerate(line):
                if elem is None:
                    continue
                if elem not in cluster_correspondence:
                    cluster_correspondence[elem] = ((i, j), (i, j))
                else:
                    begin, end = cluster_correspondence[elem]
                    cluster_correspondence[elem] = (begin, (i, j))

        return cluster_correspondence
