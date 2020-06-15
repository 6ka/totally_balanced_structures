from ..graph import Graph, random_tree


def random_lehelian_hypergraph(vertices):

    hyperedges = set(frozenset((vertex,)) for vertex in vertices)

    current_tree = random_tree([frozenset((vertex,)) for vertex in vertices])

    while len(current_tree) > 1:

        new_tree = Graph()
        for x in current_tree:
            new_tree.update(random_tree([x | y for y in current_tree(x)]).edges)
        hyperedges.update(new_tree.vertices)

        current_tree = new_tree

    hyperedges.add(frozenset(vertices))

    return frozenset(hyperedges)
