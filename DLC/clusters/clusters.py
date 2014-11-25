__author__ = 'fbrucker'


def cluster_matrix_from_O1_matrix(matrix):
    """

    :param matrix: 0/1 matrix
    :return: matrix with cluster names
    """

    clusters = cluster_matrix(matrix)
    rafine_same_clusters(matrix, clusters)

    return clusters


def boxes_clusters(clusters):
    boxes_cluster_line = dict()
    boxes_cluster_columns = dict()
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            if clusters[i][j] is None:
                continue
            elem = clusters[i][j]
            min_actu_line, max_actu_line = boxes_cluster_line.get(elem, (i, i))
            min_actu_column, max_actu_column = boxes_cluster_columns.get(elem, (j, j))
            boxes_cluster_line[elem] = (min(i, min_actu_line), max(i, max_actu_line))
            boxes_cluster_columns[elem] = (min(j, min_actu_column), max(j, max_actu_column))

    return boxes_cluster_line, boxes_cluster_columns


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
                clusters[line][column] = current_cluster
                if possible_new:
                    possible_new = False
                    number_cluster += 1
                    if line > 0:
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


def rafine_same_clusters(matrix, clusters):
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
