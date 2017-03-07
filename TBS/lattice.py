# -*- coding: utf-8 -*-

"""Lattice manipulation.

.. currentmodule:: TBS.lattice

For TBS, lattice and lattice cover graph will be equivalent.

Glossary
--------

.. glossary:: 

    lattice
        Poset (E, <) such that for all x, y in E: x^y and xvy exist. 

    lattice cover graph
        :term:`directed graph` whose vertices are the elements E of a lattice and xy is an edge iff y covers x.


Module content
--------------

.. autosummary::
    :toctree:

    get_top
    get_bottom
    get_order
    comparability_function
    inf_irreducible
    sup_irreducible
    sup_irreducible_clusters
    inf_irreducible_clusters
    sup_filter
    dual_lattice
    delete_join_irreducible
    isa_lattice_cover_graph
    compute_height

"""

import collections
from TBS.graph import Graph

__all__ = ["get_top", "get_bottom",
           "get_order", "comparability_function",
           "sup_irreducible_clusters", "inf_irreducible_clusters", "inf_irreducible", "sup_irreducible",
           "sup_filter", "dual_lattice", "delete_join_irreducible", "isa_lattice",
           "compute_height"]


def get_top(lattice):
    """Return the largest element.

    :param lattice: a lattice
    :type lattice: :class:`TBS.graph.Graph`

    :rtype: a element of the lattice.
    """
    for x in lattice:
        if not lattice[x]:
            return x

    return None


def get_bottom(lattice):
    """Return the smallest element.

    :param lattice: a lattice
    :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

    :rtype: a element of the lattice.
    """

    return get_top(dual_lattice(lattice))


def get_order(lattice):
    """Return the order associated with the lattice.

    :param lattice: a lattice
    :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

    :rtype: TBS.graph.Graph :class:`TBS.graph.Graph`
    """

    bottom = get_bottom(lattice)

    dual_order = Graph([bottom], directed=True)
    dual = dual_lattice(lattice)
    for vertex in lattice.topological_sort(bottom):
        for cover in dual[vertex]:
            dual_order.update([(vertex, cover)])
            dual_order.update([(vertex, y) for y in dual_order[cover]], delete=False)
    return dual_order.dual()


def comparability_function(lattice):
    """Return a comparability function associated with the lattice.

    The return function takes two parameters and returns True if the first parameter is smaller than the second one
    for the given lattice.
    This function computes the lattice order (long). Should only be used for generic lattices where no other solution
    is avaliable.

    :param lattice: a lattice
    :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

    :rtype: function
    """
    lattice_order = get_order(lattice)

    def smaller_than(smaller, larger):
        """Comparability function.

        :param smaller: lattice element.
        :param larger: lattice element.

        :rtype: bool :class:`bool`
        """

        return larger in lattice_order[smaller]

    return smaller_than


def inf_irreducible(lattice):
    """ Inf-irreductibles elements of the cover graph.

    :param lattice: a cover graph (may or may not have a bottom).
    :type lattice: :class:`TBS.graph.Graph`

    :return: the inf-irreducibles elements of *cover_graph*
    :rtype: :class:`frozenset`.
    """
    irreducible = set()
    for vertex in lattice:
        if len(lattice[vertex]) == 1:
            irreducible.add(vertex)

    return frozenset(irreducible)


def sup_irreducible(cover_graph):
    """ Sup-irreductibles elements of the cover graph.

    :param cover_graph: a cover graph (may or may not have a top).
    :type cover_graph: :class:`TBS.graph.Graph`

    :return: the sup-irreducibles elements of *cover_graph*
    :rtype: :class:`frozenset`.
    """

    return inf_irreducible(dual_lattice(cover_graph))


def sup_irreducible_clusters(lattice):
    """ Sup-irrerducibles correspondance.

    :param lattice: a cover graph.
    :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

    :return: a dict associating each element to the sup-irreducible elements smaller than him.
    :rtype: :class:`dict`.
    """

    dual = dual_lattice(lattice)
    bottom = get_bottom(lattice)

    correspondance = {bottom: set()}

    for vertex in lattice.topological_sort(bottom):
        if vertex not in correspondance:
            correspondance[vertex] = set()
        if dual.isa_leaf(vertex):
            # sup_irreducible
            correspondance[vertex].add(vertex)
        for cover in dual[vertex]:
            correspondance[vertex].update(correspondance[cover])

    return {element: frozenset(sups) for element, sups in correspondance.items()}


def inf_irreducible_clusters(lattice):
    """ Inf-irrerducibles correspondance.

    :param lattice: a cover graph.
    :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

    :return: a dict associating each element to the inf-irreducible elements smaller than him.
    :rtype: :class:`dict`.
    """

    return sup_irreducible_clusters(dual_lattice(lattice))


def sup_filter(lattice, element):
    """Return {y | y >= element}

    :param lattice: a cover graph (may or may not have a top).
    :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`
    :param element: vertex of the lattice cover graph
    :type element: a vertex
    :rtype: :class:`frozenset`
    """

    element_filter = set()
    lattice.dfs(element, lambda vertex: element_filter.add(vertex))

    return frozenset(element_filter)


def dual_lattice(lattice):
    """Returns the dual lattice (x->y) do (y->x).

    :param lattice: lattice
    :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

    :rtype: TBS.graph.Graph :class:`TBS.graph.Graph`
    """

    return lattice.dual()


def delete_join_irreducible(lattice, join_irreducible):
    """Delete a join irreducible element from lattice.

    :param lattice: a crown free cover graph.
    :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`
    :param join_irreducible: a join irreducible element from the lattice.
    """
    v = lattice[join_irreducible][0]
    u = None
    for u in lattice:
        if join_irreducible in lattice[u]:
            break

    lattice.remove(join_irreducible)
    if not lattice.path(u, v):
        lattice.update([(u, v)])


def compute_height(lattice):
    """Index for vertices.

    if u covers v then index[u] < index[v]
    index[bottom] = 0 and for any u covering bottom index[u] = 1.

    :param lattice: possible lattice
    :type lattice: TBS.graph.Graph :class:`TBS.graph.Graph`

    :rtype: class:`dict`
    """

    bottom = get_bottom(lattice)

    number_remaining_predecessors = {}
    for u, v in lattice.edges():
        number_remaining_predecessors[v] = number_remaining_predecessors.get(v, 0) + 1

    height = {bottom: 0}

    fifo = collections.deque((bottom,))
    while fifo:
        vertex = fifo.pop()
        for neighbor in lattice[vertex]:
            number_remaining_predecessors[neighbor] -= 1
            if not number_remaining_predecessors[neighbor]:
                height[neighbor] = height[vertex] + 1
                fifo.appendleft(neighbor)

    return height


def isa_lattice(possible_lattice):
    """Is the graph possible_lattice a lattice.

    :param possible_lattice: possible lattice
    :type possible_lattice: :class:`TBS.graph.Graph`

    :rtype: class:`bool`
    """

    elements = list(possible_lattice)
    dual_graph = dual_lattice(possible_lattice)

    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            x = elements[i]
            y = elements[j]
            for graph in (possible_lattice, dual_graph):
                filter_x = sup_filter(graph, x)
                filter_y = sup_filter(graph, y)
                unique_generator = False
                intersection = filter_x.intersection(filter_y)
                for possible_generator in intersection:
                    if sup_filter(graph, possible_generator) == intersection:
                        unique_generator = True
                        break
                if not unique_generator:
                    return False
    return True
