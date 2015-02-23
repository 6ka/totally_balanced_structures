import math

from matplotlib import pyplot
import matplotlib
import matplotlib.cm
from mpl_toolkits.mplot3d import Axes3D

from clusters.cover_graph import cover_graph_and_boxes_from_matrix
from concepts import concepts_from_matrix
from hierarchical_decomposition import hierarchical_height_from_lattice
from lattice import inf_irreducible, sup_irreducible, sup_irreducible_clusters

import randomize
from subdominant import subdominant

__author__ = 'fbrucker'

import sys
import os

sys.path.append(os.path.dirname('../'))

from DLC.contextmatrix import ContextMatrix
import DLC.graphics.lattice_string
import DLC.diss.file_io


def lattices_and_points(context_matrix):
    context_matrix.reorder_doubly_lexical_order()
    print(DLC.graphics.lattice_string.from_context_matrix(context_matrix))
    concept_representant = concepts_from_matrix(context_matrix.matrix)
    cover_graph, boxes_cluster_line, boxes_cluster_columns = cover_graph_and_boxes_from_matrix(context_matrix.matrix)
    representant = dict()
    for elem in boxes_cluster_line:
        representant[elem] = boxes_cluster_line[elem][0], boxes_cluster_columns[elem][0]

    representant["BOTTOM"] = len(context_matrix.matrix), 0
    representant["TOP"] = 0, len(context_matrix.matrix[0])

    return representant, cover_graph


def point_transformation_square(max_y):
    return lambda line, column: (column, max_y - line)


def point_transformation_radial(max_line, max_column):
    def transformation_point(line, column):
        r = max_column - column
        theta = math.pi * line / max_line
        return r * math.cos(theta), r * math.sin(theta)

    return transformation_point


def draw(plot2d, cover_graph, point_transformation, representant):
    objects = sup_irreducible(cover_graph)
    attributes = inf_irreducible(cover_graph)

    for elem in cover_graph:
        x, y = point_transformation(*representant[elem])
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        plot2d.scatter(x, y, marker=type, zorder=1, color=colors[hierarchical_edges[elem]], edgecolors='black')
        # plot2d.annotate(str(elem), xy=(x, max_y - y), color="grey")

        for neighbor in cover_graph[elem]:
            x2, y2 = point_transformation(*representant[neighbor])
            color = colors[max(hierarchical_edges[elem], hierarchical_edges[neighbor])]
            if hierarchical_edges[elem] != hierarchical_edges[neighbor]:
                type = ":"
            else:
                type = "-"
            plot2d.plot([x, x2], [y, y2], color=color, zorder=0, linestyle=type)


def context_matrix_from_dissimilarity(filename):
    original_dissimilarity = DLC.diss.file_io.load(open(filename))

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

    return ContextMatrix(matrix, elements=list(approximation), copy_matrix=False)


def line_scale(cover_graph, hierarchical_edges, representant):
    representant = dict(representant)
    for vertex in cover_graph:
        for neighbor in cover_graph[vertex]:
            if hierarchical_edges[vertex] == hierarchical_edges[neighbor] and \
                            representant[vertex][1] == representant[neighbor][1]:
                offest_position = representant[vertex][1]
                for offset_vertex in cover_graph:
                    if representant[offset_vertex][1] >= offest_position and representant[offset_vertex][0] < \
                            representant[vertex][0]:
                        representant[offset_vertex] = representant[offset_vertex][0], representant[offset_vertex][1] + 1

    columns = list(x[1] for x in representant.values())
    columns.sort()
    for x in representant:
        representant[x] = representant[x][0], columns.index(representant[x][1])
    representant_scaled = dict()
    sorted_vertices = list(cover_graph)
    sorted_vertices.sort(key=lambda x: hierarchical_edges[x] * len(cover_graph) - representant[x][1])
    for vertex in sorted_vertices:
        if hierarchical_edges[vertex] == 0:
            representant_scaled[vertex] = representant[vertex]
            continue
        same_height = None
        move = False
        for neighbor in cover_graph[vertex]:
            if hierarchical_edges[vertex] == hierarchical_edges[neighbor]:
                same_height = neighbor
            elif hierarchical_edges[vertex] > hierarchical_edges[neighbor]:
                move = True

        if move:
            mean_lines_columns = []
            for neighbor in cover_graph[vertex]:
                if hierarchical_edges[vertex] > hierarchical_edges[neighbor]:
                    if same_height is None or representant[same_height][0] > representant[neighbor][0]:
                        mean_lines_columns.append(representant_scaled[neighbor])

            if not mean_lines_columns:
                if same_height:
                    representant_scaled[vertex] = representant_scaled[same_height][0], representant[vertex][1]
                else:
                    representant_scaled[vertex] = representant[vertex]
            else:
                # representant_scaled[vertex] = sum(list(x[0] for x in mean_lines_columns)) / len(mean_lines_columns), representant[vertex][1]
                representant_scaled[vertex] = sum(list(x[0] for x in mean_lines_columns)) / len(
                    mean_lines_columns), sum(list(x[1] for x in mean_lines_columns)) / len(mean_lines_columns)

        else:
            if same_height:
                representant_scaled[vertex] = representant_scaled[same_height][0], representant[vertex][1]
            else:
                representant_scaled[vertex] = representant[vertex]
    return representant_scaled


def dissimilarity_from_lattice(dismantable_lattice):
    clusters = sup_irreducible_clusters(dismantable_lattice)
    elements = sup_irreducible(dismantable_lattice)

    for key, value in clusters.items():
        print(key, value)


if __name__ == "__main__":
    LATTICE_NUMBER_VERTICES = 50
    context_matrix = ContextMatrix.from_cover_graph(randomize.random_dismantable_lattice(LATTICE_NUMBER_VERTICES))
    # context_matrix = context_matrix_from_dissimilarity("resources/giraudoux.mat")

    representant, cover_graph, = lattices_and_points(context_matrix)
    dissimilarity_from_lattice(cover_graph)
    hierarchical_edges = hierarchical_height_from_lattice(cover_graph)
    print(hierarchical_edges)
    hierarchical_edges["BOTTOM"] = max(hierarchical_edges.values()) + 1
    hierarchical_edges["TOP"] = 0
    number_hierarchies = max(hierarchical_edges.values()) + 1
    colors = matplotlib.cm.rainbow([0. + 1.0 * x / (number_hierarchies - 1) for x in range(number_hierarchies)])

    plot2d = pyplot.subplot2grid((2, 1), (0, 0))
    point_transformation = point_transformation_square(len(context_matrix.matrix))
    draw(plot2d, cover_graph, point_transformation, representant)

    # plot2d = pyplot.subplot2grid((2, 1), (1, 0))
    # point_transformation = point_transformation_radial(len(context_matrix.matrix), len(context_matrix.matrix[0]))
    # draw(plot2d, cover_graph, point_transformation)


    plot3d = plot3d = pyplot.subplot2grid((2, 1), (1, 0), projection='3d')

    objects = sup_irreducible(cover_graph)
    attributes = inf_irreducible(cover_graph)
    representant_scaled = line_scale(cover_graph, hierarchical_edges, representant)
    # representant_scaled = representant
    for elem in cover_graph:
        x, y = representant_scaled[elem]
        z = -hierarchical_edges[elem] * len(context_matrix.matrix[0]) / number_hierarchies
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        plot3d.scatter(x, y, z, marker=type, zorder=1, color=colors[hierarchical_edges[elem]], edgecolors='black')

        for neighbor in cover_graph[elem]:
            x2, y2 = representant_scaled[neighbor]
            z2 = -hierarchical_edges[neighbor] * len(context_matrix.matrix[0]) / number_hierarchies

            color = colors[min(hierarchical_edges[elem], hierarchical_edges[neighbor])]
            if hierarchical_edges[elem] != hierarchical_edges[neighbor]:
                type = ":"
            else:
                type = "-"

            plot3d.plot([x, x2], [y, y2], [z, z2], color=color, zorder=0, linestyle=type)

    pyplot.show()