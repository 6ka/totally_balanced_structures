from ._chordal_order import chordal_order

from ._chordal_diss import approximate_to_chordal_diss, isa_chordal_diss
from ._chordal_context_matrix import chordal_context_matrix

from ..diss import Diss
from ..gamma_free import GammaFree, is_gamma_free_matrix


__all__ = ["isa_strongly_chordal_graph", "isa_totally_balanced_diss", "approximation_to_totally_balanced_diss"]


def isa_strongly_chordal_graph(graph):
    return isa_totally_balanced_diss(Diss(graph).update(lambda x, y: graph.isa_edge(x, y) and 1 or 2))


def isa_totally_balanced_diss(diss):
    return isa_chordal_diss(diss) and is_gamma_free_matrix(chordal_context_matrix(diss).reorder_doubly_lexical().matrix)


def approximation_to_totally_balanced_diss(diss_orig, order=None):
    diss = Diss(diss_orig).update(diss_orig)
    if order is None:
        order = chordal_order(diss)
    approximate_to_chordal_diss(diss, order)
    context_matrix = chordal_context_matrix(diss)

    context_matrix.reorder_elements(order)

    valuations = dict()
    for attribute, j in enumerate(context_matrix.attributes):
        for i in range(len(context_matrix.elements)):
            if context_matrix.matrix[i][j]:
                break
        valuations[attribute] = max(diss(context_matrix.elements[i], context_matrix.elements[u])
                                    for u in range(i, len(context_matrix.elements))
                                    if context_matrix.matrix[u][j])


    #shuffle
    import random
    columns = list(context_matrix.attributes)
    elements = list(context_matrix.elements)
    random.shuffle(columns)
    random.shuffle(elements)
    context_matrix.reorder_columns(columns)
    context_matrix.reorder_elements(elements)


    context_matrix.reorder_doubly_lexical()  # compatible order are not necessarily strongly compatible.
    gamma_free = GammaFree.from_approximation(context_matrix)

    return Diss(gamma_free.elements).update_by_pos(
        diss_from_valued_gamma_free_matrix(gamma_free.matrix, [valuations[x] for x in context_matrix.attributes]))


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

