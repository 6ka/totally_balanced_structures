from DLC.diss import Diss


def cluster_matrix_from_column_indices(columns_as_truncated_balls, column_indices, binary_matrix):
    cluster_matrix = [[None] * len(binary_matrix) for i in range(len(binary_matrix))]

    for center, column in columns_as_truncated_balls:
        for line_index, line in enumerate(binary_matrix):
            if line[column] and \
                    (cluster_matrix[center][line_index] is None or cluster_matrix[center][line_index] > column_indices[
                        column]):
                cluster_matrix[center][line_index] = column_indices[column]

    return cluster_matrix


def diss_from_cluster_matrix(cluster_matrix, names=(), default_value=0):
    if not names:
        names = tuple(range(len(cluster_matrix)))
    diss = Diss(names, value=default_value)
    for i in range(len(cluster_matrix)):
        for j in range(i + 1, len(cluster_matrix)):
            diss_value = None
            for k in range(i + 1):
                if cluster_matrix[k][i] is not None and cluster_matrix[k][j] is not None:
                    value = max(cluster_matrix[k][i], cluster_matrix[k][j])

                    if diss_value is None or diss_value > value:
                        diss_value = value
            diss.set_by_pos(i, j, diss_value)
    return diss


def column_indices_from_chordaly_compatible_diss(diss, binary_matrix):
    """
    position for dissimilarity must coincide with the matrix lines

    :param binary_matrix:
    :param diss:
    :param columns_as_truncated_balls:

    :return:
    """

    columns_indices = [None] * len(binary_matrix[0])
    for j in range(len(binary_matrix[0])):
        center = None
        radius = None
        for i in range(len(binary_matrix)):
            if binary_matrix[i][j]:
                if center is None:
                    center = i
                    radius = diss.get_by_pos(center, center)
                else:
                    radius = max(radius, diss.get_by_pos(center, i))

        columns_indices[j] = radius

    return columns_indices

