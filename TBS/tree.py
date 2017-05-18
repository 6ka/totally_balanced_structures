import math
import random
import matplotlib.collections
from matplotlib import pyplot
from TBS.lattice import sup


def find_root(tree):
    pruned_tree = tree.copy()
    while len(pruned_tree) > 2:
        leaves = [vertex for vertex in pruned_tree if pruned_tree.isa_leaf(vertex)]
        for leaf in leaves:
            pruned_tree.remove(leaf)
    possible_roots = [root for root in pruned_tree]  # 1 or 2 possibilities
    return random.choice(possible_roots)


def get_radial_tree_coordinates(tree, root=None, order=None):
    if len(tree) == 1:
        return {list(tree)[0]: [0, 0]}
    if not root:
        root = find_root(tree)
    if not order:
        order = list(tree.topological_sort(root))
    angles = {}
    leaves = [vertex for vertex in order if tree.isa_leaf(vertex) and vertex != root]
    for index, leaf in enumerate(leaves):
        angles[leaf] = 2 * math.pi * index / len(leaves)
    for vertex in reversed(order):
        if vertex not in angles:
            neighbors_angles = [angles[neighbor] for neighbor in tree[vertex] if neighbor in angles]
            angles[vertex] = sum(neighbors_angles) / len(neighbors_angles)
    coordinates = {order[0]: [0, 0]}
    for vertex in order[1:]:
        i = 0
        predecessor = tree[vertex][i]
        while predecessor not in coordinates:
            predecessor = tree[vertex][i + 1]
            i += 1
        coordinates[vertex] = [coordinates[predecessor][0] + math.cos(angles[vertex]),
                               coordinates[predecessor][1] + math.sin(angles[vertex])]
    return coordinates


def radial_draw_tree(tree, lattice, root=None, order=None, highlighted_edge=set(), highlighted_node=set(), save=None,
                     show=True):
    fig, ax = pyplot.subplots()
    coordinates = get_radial_tree_coordinates(tree, root, order)
    lines = []
    red_lines = []
    green_lines = []
    for vertex in tree:
        for neighbour in tree[vertex]:
            edge_sup = sup(lattice, vertex, neighbour)
            if edge_sup == vertex or edge_sup == neighbour:
                red_lines.append((coordinates[vertex], coordinates[neighbour]))
            else:
                if (vertex, neighbour) not in highlighted_edge and (neighbour, vertex) not in highlighted_edge:
                    lines.append([tuple(coordinates[vertex]), tuple(coordinates[neighbour])])
                else:
                    green_lines.append([tuple(coordinates[vertex]), tuple(coordinates[neighbour])])
            edge_middle = [(coordinates[vertex][i] + coordinates[neighbour][i]) / 2 for i in
                           range(len(coordinates[vertex]))]
            pyplot.annotate(edge_sup, edge_middle, color='#0d749e')
    line_collection = matplotlib.collections.LineCollection(lines)
    red_line_collection = matplotlib.collections.LineCollection(red_lines, colors="red")
    green_line_collection = matplotlib.collections.LineCollection(green_lines, colors="#42c432")
    ax.add_collection(line_collection)
    ax.add_collection(red_line_collection)
    ax.add_collection(green_line_collection)
    pyplot.scatter([coordinates[vertex][0] for vertex in coordinates if vertex not in highlighted_node],
                   [coordinates[vertex][1] for vertex in coordinates if vertex not in highlighted_node])
    pyplot.scatter([coordinates[vertex][0] for vertex in highlighted_node],
                   [coordinates[vertex][1] for vertex in highlighted_node], c='#42c432')
    for i, vertex in enumerate(coordinates):
        pyplot.annotate(vertex, (coordinates[vertex][0], coordinates[vertex][1]))
    if save:
        pyplot.savefig(save)
    if show:
        pyplot.show()
    pyplot.close()


def draw_3d_support_tree(tree, coordinates, lattice):
    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    number_hierarchies = max([coordinates[elem][2] + 2 for elem in coordinates])
    colors = matplotlib.cm.rainbow([0. + 1.0 * x / (number_hierarchies - 1) for x in range(number_hierarchies)])
    for node in tree:
        x, y, z = coordinates[node]
        ax.scatter(xs=x, ys=y, zs=z, color=colors[z])
    for edge in tree.edges():
        if coordinates[edge[0]][1] > coordinates[edge[1]][1]:
            max_y = edge[0]
            min_y = edge[1]
        else:
            max_y = edge[1]
            min_y = edge[0]
        x1, y1, z1 = coordinates[max_y]
        x2, y2, z2 = coordinates[min_y]
        # x_int, y_int, z_int = coordinates[sup(lattice, min_y, max_y)]
        x_int, y_int, z_int = (x2, y1, z1)
        ax.plot([x1, x_int], [y1, y_int], [z1, z_int], color=colors[z1])
        ax.plot([x_int, x2], [y_int, y2], [z_int, z2], color=colors[min(z1, z2)])
    pyplot.show()
    pyplot.close()
