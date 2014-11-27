__author__ = 'fbrucker'

__all__ = ["cluster_matrix_from_O1_matrix", "boxes_clusters", "atom_clusters"]


def cluster_matrix_from_O1_matrix(matrix):
    """

    :param matrix: 0/1 matrix
    :return: matrix with cluster names
    """

    clusters = cluster_matrix(matrix)
    refine_same_clusters(matrix, clusters)

    return clusters


def cluster_matrix(matrix):

    clusters = [[None] * len(matrix[0]) for i in range(len(matrix))]
    number_cluster = len(matrix)
    for column in range(len(matrix[0]) - 1, -1, -1):
        possible_new = True
        current_cluster = number_cluster
        for line in range(len(matrix)):
            if matrix[line][column] == 1:
                if clusters[line][column] is not None:
                    current_cluster = clusters[line][column]
                    possible_new = True
                else:
                    clusters[line][column] = current_cluster
                    number_cluster += 1
                if possible_new:
                    possible_new = False

                    for previous in range(column - 1, -1, -1):
                        if matrix[line][previous] == 1:
                            if matrix[line - 1][previous] == 1:
                                clusters[line][previous] = number_cluster
                                number_cluster += 1
                            break

            if matrix[line][column] == 0:
                possible_new = True
                current_cluster = number_cluster

    return clusters


def refine_same_clusters(matrix, clusters):
    columns_difference = column_difference_matrix(matrix)
    for j in range(len(matrix[0]) - 1):
        for i in range(len(matrix)):
            if matrix[i][j] == matrix[i][j + 1] == 1 and i > columns_difference[j]:
                clusters[i][j + 1] = clusters[i][j]


def column_difference_matrix(matrix):
    column_difference = [-1] * len(matrix[0])
    for i in range(len(matrix) - 1, -1, -1):
        for j in range(len(matrix[0]) - 2, -1, -1):
            if column_difference[j] == -1 and matrix[i][j] != matrix[i][j + 1]:
                column_difference[j] = i

    return column_difference


def boxes_clusters(clusters):
    boxes_cluster_line = dict()
    boxes_cluster_columns = dict()
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            if clusters[i][j] is None:
                continue
            elem = clusters[i][j]
            min_current_line, max_current_line = boxes_cluster_line.get(elem, (i, i))
            min_current_column, max_current_column = boxes_cluster_columns.get(elem, (j, j))
            boxes_cluster_line[elem] = (min(i, min_current_line), max(i, max_current_line))
            boxes_cluster_columns[elem] = (min(j, min_current_column), max(j, max_current_column))

    return boxes_cluster_line, boxes_cluster_columns


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
