__author__ = 'fbrucker'

__all__ = ["is_gamma_free", "approximate_gamma_free",
           "approximate_gamma_free_top_down", "approximate_gamma_free_bottom_up",
           "context_matrix_approximation"]


def is_gamma_free(matrix):
    """ Check whether the matrix is gamma free or not.

    :param matrix:
    :return: :class:`bool`
    """

    return gamma_free_matrix_top_down(matrix)


def approximate_gamma_free(matrix):
    """ Approximation into a Gamma-free matrix.

    Currently equivalent to :func:`approximate_gamma_free_top_down`

    :param matrix:
    """

    gamma_free_matrix_top_down(matrix, True)


def approximate_gamma_free_top_down(matrix):
    """ Approximation into a Gamma-free matrix.

    Top-down scheme. Adds 1 in order to transform the current matrix onto a gamma-free one.

    :param matrix:
    """

    gamma_free_matrix_top_down(matrix, True)


def approximate_gamma_free_bottom_up(matrix):
    """ Approximation into a Gamma-free matrix.

    Bottom-up scheme. Adds 0 in order to transform the current matrix onto a gamma-free one.

    :param matrix:
    """

    gamma_free_matrix_bottom_up(matrix, True)


def context_matrix_approximation(context_matrix, approximation_method=approximate_gamma_free_top_down, in_place=False):
    """ Gamma free approximation.


    return a Doubly lexically ordered and gamma free context matrix.

    new_context_matrix[i][j] == context_matrix[line_order[i]][column_order[j]]

    :param context_matrix:
    :param approximation_method: :func:`approximate_gamma_free_top_down` or :func:`approximate_gamma_free_bottom_up`
    :param in_place: if True, modify the context matrix. If False, returns a new one.
    :type in_place: :class:`bool`

    :return: :class:`ContextMatrix
    """

    if in_place:
        approximation = context_matrix
    else:
        approximation = context_matrix.copy()

    approximation.reorder_doubly_lexical_order()


    approximation_method(approximation.matrix, True)


    approximation.reorder_doubly_lexical_order()

    return approximation


def gamma_free_matrix_top_down(matrix, transform_to_gamma_free=False):
    """ adds 1

    :param matrix:
    :param transform_to_gamma_free:
    :return:
    """
    was_gamma_free = True
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                i_next = i + 1
                while i_next < len(matrix) and matrix[i_next][j] == 0:
                    i_next += 1

                if i_next == len(matrix):
                    continue
                j_next = j + 1
                while j_next < len(matrix[i]) and matrix[i][j_next] == 0:
                    j_next += 1
                if j_next == len(matrix[i]):
                    continue

                if matrix[i_next][j_next] == 0:
                    was_gamma_free = False
                    if transform_to_gamma_free:
                        matrix[i_next][j_next] = 1
                    else:
                        return was_gamma_free

    return was_gamma_free


def gamma_free_matrix_bottom_up(matrix, transform_to_gamma_free=False):
    """ adds 0

    :param matrix:
    :param transform_to_gamma_free:
    :return:
    """
    was_gamma_free = True
    for i in range(len(matrix) - 1, -1, -1):
        j = 0
        while j < len(matrix[i]):
            if matrix[i][j] == 0:
                j += 1
                continue

            i_next = i + 1
            while i_next < len(matrix) and matrix[i_next][j] == 0:
                i_next += 1

            if i_next == len(matrix):
                j += 1
                continue

            j_next = j + 1
            while j_next < len(matrix[i]):
                while j_next < len(matrix[i]) and matrix[i][j_next] == 0:
                    j_next += 1

                if j_next == len(matrix[i]):
                    j_next = j + 1
                    break

                if matrix[i_next][j_next] == 0:
                    was_gamma_free = False
                    if transform_to_gamma_free:
                        matrix[i][j_next] = 0
                    else:
                        return was_gamma_free
                else:
                    break

            j = j_next
    return was_gamma_free


