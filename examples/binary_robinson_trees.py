from matplotlib import pyplot
import matplotlib.cm

from clusters.cover_graph import cover_graph_and_boxes_from_matrix
from diss import Diss
from graph import mst_from_set, Graph
from lattice import sup_irreducible, sup_irreducible_clusters, inf_irreducible

import randomize
from subdominant import subdominant

__author__ = 'fbrucker'

import sys
import os

sys.path.append(os.path.dirname('../'))

from DLC.contextmatrix import ContextMatrix
import DLC.graphics.lattice_string
import DLC.diss.file_io


def context_matrix_from_dissimilarity(original_dissimilarity):
    approximation = subdominant(original_dissimilarity)

    matrix = [[] for i in range(len(approximation))]
    known_two_balls = set()
    for i in range(len(approximation)):
        for j in range(i + 1, len(approximation)):

            two_ball = frozenset({z for z in range(len(approximation)) if
                                  approximation.get_by_pos(i, j) >= max(approximation.get_by_pos(i, z),
                                                                        approximation.get_by_pos(j, z))})
            if two_ball in known_two_balls:
                continue
            for line in matrix:
                line.append(0)
            for z in two_ball:
                matrix[z][-1] = 1

    context_matrix = ContextMatrix(matrix, elements=list(approximation), copy_matrix=False)
    context_matrix.reorder_doubly_lexical_order()
    return context_matrix


def context_matrix_from_sets(base_set, clusters):

    matrix = [[] for i in range(len(base_set))]
    line_corresp = {x: i for i, x in enumerate(base_set)}

    for cluster in clusters:
        for line in matrix:
            line.append(0)
        for x in cluster:
            matrix[line_corresp[x]][-1] = 1

    elements = [None] * len(base_set)
    for x, index in line_corresp.items():
        elements[index] = x

    context_matrix = ContextMatrix(matrix, elements=elements, copy_matrix=False)
    context_matrix.reorder_doubly_lexical_order()
    return context_matrix


def dissimilarity_from_cover_graph(dismantable_lattice):
    clusters = sup_irreducible_clusters(dismantable_lattice)
    elements = list(sup_irreducible(dismantable_lattice))
    diss = Diss(elements)
    for x_pos in range(len(elements)):
        x = elements[x_pos]
        for y_pos in range(x_pos + 1, len(elements)):
            y = elements[y_pos]

            current_dissimilarity = None
            for cluster_name, cluster in clusters.items():
                if x in cluster and y in cluster:
                    if current_dissimilarity is None or len(cluster) < current_dissimilarity:
                        current_dissimilarity = len(cluster)
            diss[x, y] = current_dissimilarity
    return diss


class Vertex:
    def __init__(self, x, y, father=None, mother=None):
        self.parents = [father, mother]
        self.generators = [x, y]
        if father and mother:
            self.set = father.set.union(mother.set)
        else:
            self.set = frozenset(self.generators)

    def __repr__(self):
        return str(self.set)

    def __str__(self):
        return repr(self)


def dissimilarity_between_vertices(dissimilarity):

    def diss(u, v):
        u_x, u_y = u.generators
        v_x, v_y = v.generators

        return dissimilarity.max([u_x, u_y, v_x, v_y])

    return diss


def clusters_from_context_matrix(context_matrix):
    cover_graph, boxes_cluster_line, boxes_cluster_columns = cover_graph_and_boxes_from_matrix(context_matrix.matrix)
    representant = dict()
    for elem in boxes_cluster_line:
        representant[elem] = boxes_cluster_line[elem][0], boxes_cluster_columns[elem][0]

    representant_cluster = dict()
    for key, value in representant.items():
        associated_cluster = frozenset(line for line in range(value[0], len(context_matrix.matrix)) if context_matrix.matrix[line][value[1]])
        representant_cluster[key] = associated_cluster
    return representant_cluster, representant, cover_graph


def point_transformation_square(max_y):
    return lambda line, column: (column, max_y - line)


def draw(plot2d, cover_graph, representant, point_transformation, colors):
    objects = sup_irreducible(cover_graph)
    attributes = inf_irreducible(cover_graph)

    for elem in cover_graph:
        if elem not in representant:
            continue
        x, y, z = point_transformation(*representant[elem])
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        plot2d.scatter(x, y, marker=type, zorder=1, color=colors[z])
        # plot2d.annotate(str(elem), xy=(x, max_y - y), color="grey")

        for neighbor in cover_graph[elem]:
            if neighbor not in representant:
                continue
            x2, y2, z2 = point_transformation(*representant[neighbor])
            plot2d.plot([x, x2], [y, y2], zorder=0, color=colors[z])


def point_transformation_3d(max_y, clusters):
    return lambda line, column: (column, max_y - line, len(clusters[(line, column)]))


def point_transformation_3d_len(max_y, clusters):
    # return lambda line, column: (len(clusters[(line, column)]), max_y - line - ((max_y - 1)/ 2) * (len(clusters[(line, column)]) - 1) / (max_y - 1), len(clusters[(line, column)]))
    return lambda line, column: (len(clusters[(line, column)]), max_y - line - len(clusters[(line, column)]), len(clusters[(line, column)]))


def point_transformation_column_tree(max_y, max_z, column_abcisse):
    # return lambda line, column: (len(clusters[(line, column)]), max_y - line - ((max_y - 1)/ 2) * (len(clusters[(line, column)]) - 1) / (max_y - 1), len(clusters[(line, column)]))
    return lambda line, column: (column_abcisse[column], max_y - column, max_z - line)

def draw3d(plot3d, cover_graph, representant, point_transformation, colors):
    objects = sup_irreducible(cover_graph)
    attributes = inf_irreducible(cover_graph)

    for elem in cover_graph:
        if elem not in representant:
            continue
        x, y, z = point_transformation(*representant[elem])
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        plot3d.scatter(x, y, z, marker=type, zorder=1, color=colors[z])

        for neighbor in cover_graph[elem]:
            if neighbor not in representant:
                continue
            x2, y2, z2 = point_transformation(*representant[neighbor])
            plot3d.plot([x, x2], [y, y2], [z, z2], zorder=0, color=colors[z])


def column_tree(matrix):
    ordered_leaves = list()
    father = dict()
    last_line = dict()
    not_a_leaf = set()
    for column in range(len(matrix[0])):
        last_not_empty_line = len(matrix) - 1
        while last_not_empty_line >= 0 and not matrix[last_not_empty_line][column]:
            last_not_empty_line -= 1
        if column not in last_line:
            last_line[column] = last_not_empty_line
        if last_not_empty_line < 0:
            continue

        next_not_empty_column = column + 1
        while next_not_empty_column < len(matrix[0]) and not matrix[last_not_empty_line][next_not_empty_column]:
            next_not_empty_column += 1

        if next_not_empty_column >= len(matrix[0]):
            continue

        father[column] = next_not_empty_column
        not_a_leaf.add(next_not_empty_column)
        if column not in not_a_leaf:
            ordered_leaves.append(column)

    ordered_leaves.sort(key=lambda x: -last_line[x])
    return father, ordered_leaves


def column_position(tree, root, line_connection, matrix):
    position_matrix = [[None] * len(matrix[0]) for i in range(len(matrix))]
    next_vertex = [root]

    current_position = 0

    for i in range(len(matrix)):
        position_matrix[root][i] = current_position
    column_offset = {root: current_position}

    positions = dict()
    father = dict()
    while next_vertex:
        current_vertex = next_vertex.pop()
        current_position += column_offset[current_vertex]
        positions[current_vertex] = current_position
        neighborhood = [x for x in tree[current_vertex] if x not in positions]
        neighborhood.sort(key=lambda v: line_connection[v])
        print(current_vertex, neighborhood)
        next_vertex.extend(neighborhood)

        for neighbor in neighborhood[:-1]:
            column_offset[neighbor] = 1
        if neighborhood:
            column_offset[neighborhood[-1]] = 0

    return positions

if __name__ == "__main__":
    LATTICE_NUMBER_VERTICES = 12
    DISSIMILARITY_FILENAME = "" #"resources/giraudoux.mat"
    if DISSIMILARITY_FILENAME:
        dissimilarity = subdominant(DLC.diss.file_io.load(open(DISSIMILARITY_FILENAME)))
    else:
        dissimilarity = dissimilarity_from_cover_graph(randomize.random_dismantable_lattice(LATTICE_NUMBER_VERTICES))

    print(DLC.graphics.from_context_matrix(context_matrix_from_dissimilarity(dissimilarity)))
    print(DLC.diss.conversion.to_string(dissimilarity))
    diss_vertices_tree = dissimilarity_between_vertices(dissimilarity)
    trees = [mst_from_set([Vertex(u, u) for u in dissimilarity], diss_vertices_tree)]

    clusters = set([x.set for x in trees[-1]])
    for step in range(1, len(dissimilarity)):
        vertices = []
        sub_trees_vertices = dict()
        for u, v in trees[-1].edges():
            subset_diameter = []
            subset_diameter.extend(u.generators)
            subset_diameter.extend(v.generators)
            new_indices = dissimilarity.max(subset_diameter, True)
            vertex_from_edge = Vertex(new_indices['x'], new_indices['y'], u, v)
            clusters.add(vertex_from_edge.set)
            vertices.append(vertex_from_edge)
            for vertex in (u, v):
                if vertex not in sub_trees_vertices:
                    sub_trees_vertices[vertex] = []
                sub_trees_vertices[vertex].append(vertex_from_edge)


        tree = Graph(vertices)
        for sub_tree in sub_trees_vertices.values():
            mst_sub_tree = mst_from_set(sub_tree, diss_vertices_tree)
            tree.update(mst_sub_tree.edges(), delete=False)
        trees.append(tree)

    for tree in trees:
        print(tree)
        print("---")

    context_matrix = context_matrix_from_sets(set(dissimilarity), clusters)
    print(DLC.graphics.from_context_matrix(context_matrix))
    column_mst_father, ordered_leaves = column_tree(context_matrix.matrix)
    print(column_mst_father, ordered_leaves)
    # positions_mst = column_position(column_mst, len(context_matrix.matrix[0]) - 1, line_connection, context_matrix.matrix)
    # print(positions_mst)
    # representant_cluster, representant, cover_graph = clusters_from_context_matrix(context_matrix)
    # n = len(context_matrix.matrix)
    # print(n)
    # colors = matplotlib.cm.rainbow([0. + 1.0 * x / (n) for x in range(n + 1)])
    # plot2d = pyplot.subplot2grid((2, 1), (0, 0))
    # point_transformation3d = point_transformation_3d(len(context_matrix.matrix), {value: representant_cluster[key] for key, value in representant.items()})
    # point_transformation = point_transformation_square(len(context_matrix.matrix))
    # draw(plot2d, cover_graph, representant, point_transformation3d, colors)
    #
    #
    # plot2d2 = pyplot.subplot2grid((2, 1), (1, 0))
    # # point_transformation3d2 = point_transformation_3d_len(len(context_matrix.matrix), {value: representant_cluster[key] for key, value in representant.items()})
    #
    # point_transformation = point_transformation_column_tree(len(context_matrix.matrix[0]) - 1,
    #                                                         len(context_matrix.matrix) - 1,
    #                                                         positions_mst)
    # # draw(plot2d2, cover_graph, representant, point_transformation, colors)
    #
    #
    # from mpl_toolkits.mplot3d import Axes3D
    # plot3d = pyplot.subplot2grid((2, 1), (1, 0), projection='3d')
    # draw3d(plot3d, cover_graph, representant, point_transformation, colors)
    #
    # pyplot.show()