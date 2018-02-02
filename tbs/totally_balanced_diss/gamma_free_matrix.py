from ..diss import Diss

__all__ = ["diss_from_valued_gamma_free_matrix"]


def diss_from_valued_gamma_free_matrix(gamma_free_matrix, valuation):
    """Dissimilarity associated with a gama free valued 0/1- matrix.

    Args:
        gamma_free_matrix (list): A gamma free binary matrix. Last column must be full of 1.
        valuation (list): a real valuation

    Returns:

    """

    n = len(gamma_free_matrix)
    m = len(gamma_free_matrix[0])
    number = [0] * m
    d = Diss(range(n))
    for i in range(n - 1, -1, -1):
        for j in range(m):
            number[j] += gamma_free_matrix[i][j]
        columns = [m - 1]
        c = m - 1
        for j in range(m - 1, -1, -1):
            if gamma_free_matrix[i][j] and valuation[j] < valuation[c]:
                if number[c] > number[j]:
                    columns.append(j)
                else:
                    columns[-1] = j
                c = j
        for j in range(i + 1, n):
            d.set_by_pos(i, j, min(valuation[k] for k in columns if gamma_free_matrix[j][k]))

    return d

