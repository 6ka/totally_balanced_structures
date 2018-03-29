__author__ = "cchatel", "fbrucker"

from matplotlib import collections
import math
from ..graph import bfs_from_vertex
from ..gamma_free import GammaFree


def draw_binary_mixed_tree_to_pyplot(binary_mixed_tree, pyplot, highlighted_edge=set(), highlighted_node=set()):
    fig, ax = pyplot.subplots()
    root = binary_mixed_tree.find_root_as_undirected()
    coordinates = get_radial_tree_coordinates(binary_mixed_tree, root)
    lines = []
    red_lines = []
    green_lines = []
    for vertex in binary_mixed_tree.vertices:
        for neighbour in binary_mixed_tree(vertex, undirected=True, begin=False, end=False):
            if (vertex, neighbour) not in highlighted_edge and (neighbour, vertex) not in highlighted_edge:
                lines.append([tuple(coordinates[vertex]), tuple(coordinates[neighbour])])
            else:
                green_lines.append([tuple(coordinates[vertex]), tuple(coordinates[neighbour])])
        for neighbour in binary_mixed_tree(vertex, undirected=False, begin=True, end=False):
            red_lines.append((coordinates[vertex], coordinates[neighbour]))
    line_collection = collections.LineCollection(lines)
    red_line_collection = collections.LineCollection(red_lines, colors="red")
    green_line_collection = collections.LineCollection(green_lines, colors="#42c432")
    ax.add_collection(line_collection)
    ax.add_collection(red_line_collection)
    ax.add_collection(green_line_collection)
    pyplot.scatter([coordinates[vertex][0] for vertex in coordinates if vertex not in highlighted_node],
                   [coordinates[vertex][1] for vertex in coordinates if vertex not in highlighted_node])
    pyplot.scatter([coordinates[vertex][0] for vertex in highlighted_node],
                   [coordinates[vertex][1] for vertex in highlighted_node], c='#42c432')
    for i, vertex in enumerate(coordinates):
        pyplot.annotate(vertex, (coordinates[vertex][0], coordinates[vertex][1]))


def draw_dismantlable_lattice_to_pyplot(dismantlable_lattice, pyplot, color_scheme):
    from tbs.gamma_free._draw_pyplot import draw_to_pyplot
    context_matrix = GammaFree.from_lattice(dismantlable_lattice)
    context_matrix.reorder_doubly_lexical()
    draw_to_pyplot(context_matrix, pyplot, color_scheme)


def draw_tree_decomposition_to_pyplot(tree_decomposition, tree_index, pyplot):
    """Draw all trees contained in history of the tree decomposition
    """
    n_steps = len(tree_decomposition.history)
    tree = tree_decomposition.history[tree_index]
    highlighted_edge = set()
    highlighted_node = set()
    if tree_index != 0:
        highlighted_node = [tree_decomposition.order[tree_index - 1][0].union(tree_decomposition.order[tree_index - 1][1])]
    if tree_index != n_steps - 1:
        highlighted_edge = [tree_decomposition.order[tree_index]]
    draw_binary_mixed_tree_to_pyplot(tree, pyplot, highlighted_edge=highlighted_edge, highlighted_node=highlighted_node)


def get_radial_tree_coordinates(binary_mixed_tree, root=None, order=None):
    tree = binary_mixed_tree.to_graph()
    if len(tree) == 1:
        return {list(tree)[0]: [0, 0]}
    if not root:
        root = binary_mixed_tree.find_root_as_undirected()
    if not order:
        order = list(bfs_from_vertex(tree, root))
    angles = {}
    leaves = [vertex for vertex in order if len(tree(vertex)) == 1 and vertex != root]
    for index, leaf in enumerate(leaves):
        angles[leaf] = 2 * math.pi * index / len(leaves)
    for vertex in reversed(order):
        if vertex not in angles:
            neighbors_angles = [angles[neighbor] for neighbor in tree(vertex) if neighbor in angles]
            angles[vertex] = sum(neighbors_angles) / len(neighbors_angles)
    coordinates = {order[0]: [0, 0]}
    for vertex in order[1:]:
        i = 0
        possible_predecessors = list(tree(vertex))
        predecessor = possible_predecessors[i]
        while predecessor not in coordinates:
            predecessor = possible_predecessors[i + 1]
            i += 1
        coordinates[vertex] = [coordinates[predecessor][0] + math.cos(angles[vertex]),
                               coordinates[predecessor][1] + math.sin(angles[vertex])]
    return coordinates