import random
from ._graph import Graph


def random_tree(vertices):
    """ Random tree.

    Args:
        vertices(list): list of vertices.

    Returns(Graph): A tree on the set of vertices.
    """

    if len(vertices) <= 2:
        return tree_from_prufer([], vertices)
    else:

        return tree_from_prufer([random.randint(0, len(vertices) - 1) for x in range(len(vertices) - 2)], vertices)


def tree_from_prufer(prufer_list, vertices):
    """Tree from Prüfer sequence.

    Return a Tree according to the prüfer sequences associated with the vertex list.
    Args:
        prufer_list(list): a len(vertices) - 2 length list of indices from 0 to len(vertices) - 1
        vertices(list): the vertices of the graph.

    Returns(Graph):a Tree.
    """

    tree = Graph(vertices)

    vertices_degree = [1] * len(vertices)
    for vertex_index in prufer_list:
        vertices_degree[vertex_index] += 1

    for prufer in prufer_list:
        leaf, degree = None, None
        for leaf, degree in enumerate(vertices_degree):
            if degree == 1:
                break
        tree.update([(vertices[prufer], vertices[leaf])])
        vertices_degree[prufer] -= 1
        vertices_degree[leaf] -= 1

    last_edge = [vertices[i] for i, degree in enumerate(vertices_degree) if degree == 1]
    if len(last_edge) == 2:
        tree.update([last_edge])

    return tree


def prufer_from_tree(tree, vertices_list):
    vertices_degree = [set(tree(x)) for x in vertices_list]

    number_edges_remaining = max(0, len(vertices_list) - 2)
    prufer = []

    while number_edges_remaining:
        leaf, neighbors = None, None
        for leaf, neighbors in enumerate(vertices_degree):
            if len(neighbors) == 1:
                break

        x = vertices_list[leaf]
        y = list(neighbors)[0]

        vertices_degree[leaf] = set()
        vertices_degree[vertices_list.index(y)].remove(x)

        prufer.append(vertices_list.index(y))
        number_edges_remaining -= 1

    return prufer
