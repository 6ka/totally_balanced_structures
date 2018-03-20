from ..clusters.from_chordal import chordal_clusters
from ..orders.chordal_order import chordal_order
from .chordal_diss import approximate_chordal_diss, isa_chordal_diss
from .gamma_free_matrix import diss_from_valued_gamma_free_matrix
from ..contextmatrix import ContextMatrix
from ..diss import Diss
from ..gamma_free import GammaFree, is_gamma_free_matrix


def isa_strongly_chordal_graph(graph):
    return isa_totally_balanced_diss(Diss(graph).update(lambda x, y: graph.isa_edge(x, y) and 1 or 2))


def isa_totally_balanced_diss(diss):
    if not isa_chordal_diss(diss):
        return False

    context_matrix = ContextMatrix.from_clusters(chordal_clusters(diss, chordal_order(diss))) \
        .reorder_doubly_lexical()

    return is_gamma_free_matrix(context_matrix.matrix)


def approximation_totally_balanced_diss(diss_orig, order=None):
    diss = Diss(diss_orig).update(diss_orig)
    if order is None:
        order = chordal_order(diss)
    approximate_chordal_diss(diss, order)
    context_matrix = ContextMatrix.from_clusters(chordal_clusters(diss))
    corresp = {value: index for index, value in enumerate(order)}
    context_matrix.reorder_lines([corresp[x] for x in context_matrix.elements])

    valuations = dict()
    for attribute, j in enumerate(context_matrix.attributes):
        for i in range(len(context_matrix.elements)):
            if context_matrix.matrix[i][j]:
                break
        valuations[attribute] = max(diss(context_matrix.elements[i], context_matrix.elements[u])
                                    for u in range(i, len(context_matrix.elements))
                                    if context_matrix.matrix[u][j])

    context_matrix.reorder_doubly_lexical()  # compatible order are not necessarily strongly compatible.
    gamma_free = GammaFree.from_approximation(context_matrix)

    return Diss(gamma_free.elements).update_by_pos(
        diss_from_valued_gamma_free_matrix(gamma_free.matrix, [valuations[x] for x in context_matrix.attributes]))
