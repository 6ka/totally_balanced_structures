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


def column_indices_from_chordally_compatible_diss(diss, context_matrix):
    """

    :param diss:
    :param context_matrix:

    :return:
    """

    index_order = [diss.vertex_index[x] for x in context_matrix.elements]
    columns_indices = [None] * len(context_matrix.attributes)
    for j in range(len(context_matrix.attributes)):
        center = None
        radius = None
        for i in range(len(context_matrix.elements)):
            if context_matrix.matrix[i][j]:
                if center is None:
                    center = i
                    radius = diss.get_by_pos(index_order[center], index_order[center])
                else:
                    radius = max(radius, diss.get_by_pos(index_order[center], index_order[i]))

        columns_indices[j] = radius

    return columns_indices

