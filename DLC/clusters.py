__author__ = 'fbrucker'


def cluster_matrix(matrix):
    """

    :param matrix: 0/1 matrix
    :return: matrix with cluster names
    """

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