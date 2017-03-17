import math
import random
import matplotlib.collections
from matplotlib import pyplot


def find_root(tree):
    pruned_tree = tree.copy()
    while len(pruned_tree) > 2:
        leaves = [vertex for vertex in pruned_tree if pruned_tree.isa_leaf(vertex)]
        for leaf in leaves:
            pruned_tree.remove(leaf)
    possible_roots = [root for root in pruned_tree]  # 1 or 2 possibilities
    return random.choice(possible_roots)


def radial_draw_tree(tree, root=None, order=None):
    fig, ax = pyplot.subplots()
    if not root:
        root = find_root(tree)
    if not order:
        order = list(tree.topological_sort(root))
    angles = {}
    leaves = [vertex for vertex in order if tree.isa_leaf(vertex)]
    for index, leaf in enumerate(leaves):
        angles[leaf] = 2 * math.pi * index / len(leaves)
    for vertex in reversed(order):
        if vertex not in angles:
            neighbors_angles = [angles[neighbor] for neighbor in tree[vertex] if neighbor in angles]
            angles[vertex] = sum(neighbors_angles) / len(neighbors_angles)
    coordinates = {order[0]: [0, 0]}
    lines = []
    for vertex in order[1:]:
        i = 0
        predecessor = tree[vertex][i]
        while predecessor not in coordinates:
            predecessor = tree[vertex][i + 1]
            i += 1
        coordinates[vertex] = [coordinates[predecessor][0] + math.cos(angles[vertex]),
                               coordinates[predecessor][1] + math.sin(angles[vertex])]
        lines.append([tuple(coordinates[predecessor]), tuple(coordinates[vertex])])
    line_collection = matplotlib.collections.LineCollection(lines)
    ax.add_collection(line_collection)
    pyplot.scatter([coordinates[vertex][0] for vertex in coordinates],
                   [coordinates[vertex][1] for vertex in coordinates])
    for i, vertex in enumerate(coordinates):
        pyplot.annotate(vertex, (coordinates[vertex][0], coordinates[vertex][1]))
    pyplot.show()