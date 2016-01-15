from DLC import doubly_lexical_order
from DLC.chordal_order import chordal_diss_from_fixed_order
from DLC.chordal_order.clusters import context_matrix_from_order
from DLC.chordal_order.order import from_diss_approximate_order
from DLC.diss_approximation.diss_association import column_indices_from_chordally_compatible_diss, \
    cluster_matrix_from_column_indices, diss_from_cluster_matrix
from DLC.diss_approximation.gamma_free_matrix_numbers import columns_as_truncated_balls
from doubly_lexical_order import gamma_free_matrix_top_down

__author__ = 'fbrucker'
__all__ = ["totally_balanced_dissimilarity"]


def totally_balanced_dissimilarity_for_order(original_diss, order):
    temporary_diss = original_diss.copy()
    chordal_diss_from_fixed_order(temporary_diss, order)
    context_matrix = context_matrix_from_order(temporary_diss, order)

    new_line_order, new_column_order = doubly_lexical_order.doubly_lexical_order(context_matrix.matrix, order)

    column_permutation = [0] * len(new_column_order)
    for i, index in enumerate(new_column_order):
        column_permutation[index] = i

    context_matrix.reorder(column_permutation=column_permutation)
    gamma_free_matrix_top_down(context_matrix.matrix, transform_to_gamma_free=True)
    column_indices = gamma_free_context_matrix_and_column_indices(context_matrix, temporary_diss)
    approximated_diss = dissimlarity_from_indiced_context_matrix(context_matrix, column_indices)

    return approximated_diss


def totally_balanced_dissimilarity(original_diss):
    temporary_diss = original_diss.copy()

    context_matrix = chordal_diss_and_context_matrix(temporary_diss)
    context_matrix = doubly_lexical_order.context_matrix_approximation(context_matrix)

    column_indices = gamma_free_context_matrix_and_column_indices(context_matrix, temporary_diss)
    approximated_diss = dissimlarity_from_indiced_context_matrix(context_matrix, column_indices)

    return approximated_diss


def chordal_diss_and_context_matrix(diss):
    """
    diss is approximated

    :param diss:
    :return:
    """

    chordal_order = from_diss_approximate_order(diss)
    chordal_diss_from_fixed_order(diss, chordal_order)
    context_matrix = context_matrix_from_order(diss, chordal_order)
    return context_matrix


def gamma_free_context_matrix_and_column_indices(context_matrix, diss):
    """
    context_matrix and diss are approximated

    :param context_matrix:
    :param diss:
    :return:
    """


    chordal_diss_from_fixed_order(diss, context_matrix.elements)
    column_indices = column_indices_from_chordally_compatible_diss(diss, context_matrix)

    return column_indices


def dissimlarity_from_indiced_context_matrix(context_matrix, column_indices):
    truncated_balls = columns_as_truncated_balls(context_matrix.matrix)
    cluster_matrix = cluster_matrix_from_column_indices(truncated_balls, column_indices, context_matrix.matrix)
    diss = diss_from_cluster_matrix(cluster_matrix, names=context_matrix.elements)

    return diss
