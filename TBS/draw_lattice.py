from matplotlib import pyplot

from TBS.contextmatrix import ContextMatrix
from TBS.hierarchical_decomposition import hierarchical_height_from_lattice
from TBS import clusters
from TBS.lattice import sup_irreducible, inf_irreducible, sup_irreducible_clusters
from TBS.clusters import from_dlo_gamma_free_matrix
from mpl_toolkits.mplot3d import Axes3D


# draw helper methods


def point_transformation_square(max_y):
    return lambda line, column: (column, max_y - line)


def z_point_position(element, dual, points_positions):# to compute height according to predecessors height : max + 1
    pred1, pred2 = dual[element][0], dual[element][1]
    points_positions[element] = max(points_positions[pred1], points_positions[pred2]) + 2
    return points_positions


def edge_color(vertex1, colors, hierarchy_association, vertex2=None):
    if vertex2 is None:
        vertex2 = vertex1

    return colors[max(hierarchy_association[vertex1], hierarchy_association[vertex2])]


def draw(lattice, colors):
    context_matrix = ContextMatrix.from_lattice(lattice)
    context_matrix.reorder_doubly_lexical_order()
    formal_context_lattice = clusters.from_dlo_gamma_free_matrix.lattice(context_matrix.matrix)
    objects = sup_irreducible(formal_context_lattice)
    attributes = inf_irreducible(formal_context_lattice)
    coordinates = boxes_coordinates(lattice)
    for elem in formal_context_lattice:
        x, y, z = coordinates[elem]
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        pyplot.scatter(x, y, marker=type, color=colors[z], edgecolors='black')

        for neighbor in formal_context_lattice[elem]:
            x2, y2, z2 = coordinates[neighbor]
            if z2 != z:
                type = ":"
            else:
                type = "-"
            pyplot.plot([x, x2], [y, y2], color=colors[max(z, z2)], zorder=0, linestyle=type)


def draw_3d(lattice, colors):
    context_matrix = ContextMatrix.from_lattice(lattice)
    context_matrix.reorder_doubly_lexical_order()
    formal_context_lattice = clusters.from_dlo_gamma_free_matrix.lattice(context_matrix.matrix)
    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    objects = sup_irreducible(formal_context_lattice)
    attributes = inf_irreducible(formal_context_lattice)
    coordinates = boxes_coordinates(lattice)
    for elem in formal_context_lattice:
        x, y, z = coordinates[elem]
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        ax.scatter(xs=x, ys=y, zs=z, marker=type, color=colors[z], edgecolors='black')

        for neighbor in formal_context_lattice[elem]:
            x2, y2, z2 = coordinates[neighbor]
            if z2 != z:
                type = ":"
            else:
                type = "-"
            ax.plot([x, x2], [y, y2], [z, z2], color=colors[max(z, z2)], zorder=0, linestyle=type)


def boxes_coordinates(lattice):
    context_matrix = ContextMatrix.from_lattice(lattice)
    context_matrix.reorder_doubly_lexical_order()
    formal_context_lattice = clusters.from_dlo_gamma_free_matrix.lattice(context_matrix.matrix)
    point_tranformation = point_transformation_square(len(context_matrix.matrix))
    hierarchy_association = hierarchical_height_from_lattice(formal_context_lattice)
    hierarchy_association["BOTTOM"] = max(hierarchy_association.values()) + 1
    hierarchy_association["TOP"] = 0
    points_positions = hierarchy_association.copy()
    points_positions['BOTTOM'] = 0
    points = {box: box[0] for box in formal_context_lattice if box not in ("BOTTOM", "TOP")}
    points["BOTTOM"] = (len(context_matrix.matrix), 0)
    points["TOP"] = (0, len(context_matrix.matrix[0]))
    coordinates = dict()
    for elem in formal_context_lattice:
        x, y = point_tranformation(*points[elem])
        z = points_positions[elem]
        coordinates[elem] = (x, y, z)
    return coordinates


def point_coordinates(lattice):
    coord = boxes_coordinates(lattice)
    context_matrix = ContextMatrix.from_lattice(lattice)
    context_matrix.reorder_doubly_lexical_order()
    boxes = from_dlo_gamma_free_matrix.boxes(context_matrix.matrix)
    classes = sup_irreducible_clusters(lattice)
    classes_label = {classes[element]: element for element in classes}
    boxes_to_element = {box: class_associated_to_box(context_matrix, box, classes_label) for box in boxes.values()}
    boxes_to_element['BOTTOM'] = 'BOTTOM'
    boxes_to_element['TOP'] = 'TOP'
    coordinates = {boxes_to_element[element]: coord[element] for element in coord}
    return coordinates


def class_associated_to_box(context_matrix, box, classes_label):
    box_column_index = box[0][1]
    box_row_index = box[0][0]
    column_from_box = [context_matrix.matrix[i][box_column_index] for i in
                       range(box_row_index, len(context_matrix.matrix))]
    box_class = frozenset(
        [context_matrix.elements[i + box_row_index] for i in range(len(column_from_box)) if column_from_box[i] == 1])
    return classes_label[box_class]
