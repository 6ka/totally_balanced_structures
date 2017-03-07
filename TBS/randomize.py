"""Randomization.

.. currentmodule:: TBS.randomize


Module content
--------------

.. autosummary::
    :toctree:

    randomize_edges
    random_dismantable_lattice
    random_01_matrix
    shuffle_line_and_column_from_context_matrix
    random_gamma_free_01_matrix


"""

import random

from . import gamma_free
from .contextmatrix import ContextMatrix
from .graph import Graph
from .lattice import sup_filter


__author__ = 'fbrucker'

__all__ = ["randomize_edges",
           "random_dismantable_lattice",
           "random_01_matrix",
           "shuffle_line_and_column_from_context_matrix",
           "random_gamma_free_01_matrix"]


def randomize_edges(graph, probability_of_remaining_an_edge=0.5, probability_of_being_an_edge=0.5):
    """Random edge modification.

    :param graph: original graph.
    :type graph: TBS.graph.Graph :class:`TBS.graph.Graph`

    For each pair (x, y) of vertices, has a probability of remaining or being an edge.

    :param probability_of_remaining_an_edge: for an existing edge
    :type probability_of_remaining_an_edge: 0 <= :class:`float` <= 1
    :param probability_of_being_an_edge: not an edge
    :type probability_of_being_an_edge: 0 <= :class:`float` <= 1

    :rtype: :class:`TBS.graph.Graph`
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


def random_dismantable_lattice(number_of_elements, bottom="BOTTOM", top="TOP"):
    """Random dismantable lattice.

    :param number_of_elements: final number of elements
    :type number_of_elements: class:`int`
    """
    crown_free = Graph(directed=True)
    crown_free.update([(bottom, top)])

    all_elements = [bottom]
    for current_element in range(number_of_elements):
        u = random.sample(all_elements, 1)[0]
        v = random.sample(sup_filter(crown_free, u) - {u}, 1)[0]
        crown_free.update([(u, current_element), (current_element, v)])
        all_elements.append(current_element)

    for u, v in crown_free.edges():
        crown_free.update([(u, v)])
        if not crown_free.path(u, v):
            crown_free.update([(u, v)])
    return crown_free


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
    context_matrix = ContextMatrix(matrix, copy_matrix=False)
    gamma_free.context_matrix_approximation(context_matrix, in_place=True)
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
    context_matrix.reorder(new_line_order, new_column_order)
    line_order = [0] * len(new_line_order)
    for i, x in enumerate(new_line_order):
        line_order[x] = i

    column_order = [0] * len(new_column_order)
    for j, x in enumerate(new_column_order):
        column_order[x] = j

    return line_order, column_order
