__author__ = 'fbrucker'

__all__ = ["cluster_matrix_from_O1_matrix", "cluster_matrix_and_boxes_from_O1_matrix", "atom_matrix_clusters",
           "ClusterLineFromMatrix"]


def cluster_matrix_from_O1_matrix(matrix):
    return [current_line for current_line in ClusterLineFromMatrix(matrix)]


def cluster_matrix_and_boxes_from_O1_matrix(matrix):
    clusters = []
    boxes_cluster_line = dict()
    boxes_cluster_columns = dict()
    for i, current_line in enumerate(ClusterLineFromMatrix(matrix)):
        clusters.append(current_line)
        for j, elem in enumerate(current_line):
            if elem is None:
                continue
            min_current_line, max_current_line = boxes_cluster_line.get(elem, (i, i))
            min_current_column, max_current_column = boxes_cluster_columns.get(elem, (j, j))
            boxes_cluster_line[elem] = (min(i, min_current_line), max(i, max_current_line))
            boxes_cluster_columns[elem] = (min(j, min_current_column), max(j, max_current_column))

    return clusters, boxes_cluster_line, boxes_cluster_columns


class ClusterLineFromMatrix(object):
    def __init__(self, matrix):
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


def atom_clusters_correspondence(clusters, atom_line_correspondence=None):
    if atom_line_correspondence is None:
        atom_line_correspondence = list(range(len(clusters)))

    number_to_cluster = dict()
    cluster_to_number = dict()
    for j in range(len(clusters[0])):
        cluster_in_progress = set()
        for i in range(len(clusters)):
            current = clusters[i][j]
            if current is not None:
                if current not in number_to_cluster:
                    cluster_in_progress.add(current)
                    number_to_cluster[current] = set()
                for number in cluster_in_progress:
                    number_to_cluster[number].add(atom_line_correspondence[i])
        for cluster in cluster_in_progress:
            number_to_cluster[cluster] = frozenset(number_to_cluster[cluster])
            cluster_to_number[number_to_cluster[cluster]] = cluster
    return number_to_cluster, cluster_to_number
