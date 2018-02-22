def isa_lattice(comparability_graph):
    """Is the graph possible_lattice a lattice.

    :rtype: :class:`bool`
    """

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
