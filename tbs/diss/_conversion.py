from ._diss import Diss


def from_context_matrix(context_matrix, indexed_function, default_value=0):
    """
    if for some i, j there is no columns with both i and j the dissimilarity value is default_value.
    :param context_matrix:
    :param indexed_function: f(attribute_name) = number
    :return:
    """

    diss = Diss(context_matrix.elements, value=default_value)

    for i in range(len(context_matrix.elements)):
        for j in range(i + 1, len(context_matrix.elements)):
            diss_value = None
            has_value = False
            for k in range(len(context_matrix.attributes)):
                if context_matrix.matrix[i][k] and context_matrix.matrix[j][k]:
                    if diss_value is None or diss_value > indexed_function(context_matrix.attributes[k]):
                        diss_value = indexed_function(context_matrix.attributes[k])
                        has_value = True

            if has_value:
                diss.set_by_pos(i, j, diss_value)

    return diss