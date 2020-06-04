"""Randomization.

.. currentmodule:: tbs.randomize


Module content
--------------

"""

import random

from . import gamma_free
from .contextmatrix import ContextMatrix
from .gamma_free import GammaFree


__author__ = 'fbrucker'

__all__ = ["randomize_edges",
           "random_01_matrix",
           "shuffle_line_and_column_from_context_matrix",
           "random_gamma_free_01_matrix"]


def randomize_edges(graph, probability_of_remaining_an_edge=0.5, probability_of_being_an_edge=0.5):
    """Random edge modification.

    Each pair (x, y) of vertices, has a probability of remaining or being an edge.

    Args:
        graph (Graph): original graph to be modified.
        probability_of_remaining_an_edge: probability for an existing edge to remain an edge in the new graph.
        probability_of_being_an_edge: probability for non existing edge to become an edge in the new graph.

    Returns:
        A new graph.
    """

    result = graph.copy()

    elems = list(graph)

    for i, x in enumerate(elems):
        if graph.directed:
            possibilities = elems
        else:
            possibilities = elems[i + 1:]

        for y in possibilities:
            if x is y:
                continue

            if graph.isa_edge(x, y):
                if random.random() > probability_of_remaining_an_edge:
                    result._update([(x, y)])
            else:
                if random.random() < probability_of_being_an_edge:
                    result._update([(x, y)])
    return result


def random_01_matrix(number_lines, number_column, probability_of_1=.5):
    return [[random.random() < probability_of_1 and 1 or 0 for j in range(number_column)] for i in range(number_lines)]


def random_gamma_free_01_matrix(number_lines, number_column, probability_of_1=.5):
    """
    return a 0/1-matrix admitting a gamma free order.

    :param number_lines:
    :param number_column:
    :param probability_of_1:
    :return:
    """
    matrix = [[random.random() < probability_of_1 and 1 or 0 for j in range(number_column)] for i in range(number_lines)]
    context_matrix = GammaFree.from_approximation(ContextMatrix(matrix))
    shuffle_line_and_column_from_context_matrix(context_matrix)

    return context_matrix.matrix


def shuffle_line_and_column_from_context_matrix(context_matrix):
    """
    line_order[i] = original line of index i
    column_order[j] = original column of index j
    :param context_matrix:
    :return: line_order, column_order
    """
    new_line_order = list(range(len(context_matrix.elements)))
    random.shuffle(new_line_order)
    new_column_order = list(range(len(context_matrix.attributes)))
    random.shuffle(new_column_order)
    context_matrix.reorder_lines(new_line_order)
    context_matrix.reorder_columns(new_column_order)
