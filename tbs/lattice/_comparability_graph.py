from tbs.graph import topological_sort


def isa_lattice(comparability_graph):
    """Is the graph possible_lattice a lattice.

    Args:
        comparability_graph(DirectedGraph): a possible lattice comparability graph.

    Returns(bool):
        True if comparability_graph is a lattice order comprarability graph, False otherwise.
    """

    # topological_order = topological_sort(comparability_graph)
    #
    # if len(comparability_graph(topological_order[0], begin=False, end=True)) > 0:
    #     return False
    # if len(comparability_graph(topological_order[-1], begin=True, end=False)) > 0:
    #     return False
    # for x in topological_order[1:-1]:
    #     if not comparability_graph(x, begin=False, end=True) or not comparability_graph(x, begin=True, end=False):
    #         return False
    #
    #
    elements = list(comparability_graph)

    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            x = elements[i]
            y = elements[j]
            for graph in (comparability_graph, comparability_graph.dual_lattice):
                filter_x = graph.sup_filter(x)
                filter_y = graph.sup_filter(y)
                unique_generator = False
                intersection = filter_x.intersection(filter_y)
                for possible_generator in intersection:
                    if graph.sup_filter(possible_generator) == intersection:
                        unique_generator = True
                        break
                if not unique_generator:
                    return False
    return True

