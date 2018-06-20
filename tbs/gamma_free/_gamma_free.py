__author__ = 'fbrucker'


from ..contextmatrix import ContextMatrix
from ._gamma_free_column_ordering import gamma_free_column_order


class GammaFree(ContextMatrix):
    @classmethod
    def from_approximation(cls, context_matrix):
        """Gamma Free contextmatrix.

        Approximate *context_matrix*, in a Gamma-free matrix for the current order. Thus if the context_matrix is
        Gamma-free but for an another order, it will be modified. One can nevertheless do
        `GammaFree(context_matrix.reorder_doubly_lexical())` to first reorder the matrix into a Gamma free order
        whenever it is possible.

        Args:
            context_matrix(ContextMatrix): a possibly non Gamma-free context matrix.
        """

        gamma_free = cls.from_context_matrix(context_matrix)
        new_matrix = list(list(line) for line in gamma_free.matrix)
        approximate_gamma_free(new_matrix)
        gamma_free._matrix = tuple(tuple(line) for line in new_matrix)

        return gamma_free

    def is_gamma_free(self):
        """ Check whether the current order is Gamma free or not.
        """

        return is_gamma_free_matrix(self.matrix)

    def reorder_gamma_free_from_strongly_chordal_element_order(self):
        """ Gamma free column ordering.

            One assume that it is possible, thas is that the lines form a strongly chordal order.


        """

        column_order = gamma_free_column_order(self)
        self.reorder_columns(column_order)
        return self


def is_gamma_free_matrix(matrix):
    return gamma_free_matrix_top_down(matrix)


def approximate_gamma_free(matrix):
    """ Approximation into a Gamma-free matrix.

    Currently equivalent to :func:`approximate_gamma_free_top_down`

    :param matrix:
    """

    gamma_free_matrix_top_down(matrix, True)


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


