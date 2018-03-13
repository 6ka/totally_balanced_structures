__author__ = "cchatel", "fbrucker"

from ..clusters import ClusterLineFromMatrix
from ..contextmatrix import ContextMatrix
from matplotlib import pyplot
import matplotlib
from ..clusters.to_string import BoxesToString


def draw(self):
    """Draws the lattice
    """
    formal_context_lattice = self.to_box_lattice()
    matrix = ContextMatrix.from_lattice(formal_context_lattice).matrix
    point_transformation = point_transformation_square(len(matrix))
    representant = {box: box[0] for box in formal_context_lattice if box not in ("BOTTOM", "TOP")}
    representant[self.get_bottom()] = (len(matrix), 0)
    representant[self.get_top()] = (0, len(matrix[0]))
    objects = formal_context_lattice.sup_irreducible()
    attributes = formal_context_lattice.inf_irreducible()
    hierarchy_association = formal_context_lattice.hierarchical_height()

    for elem in formal_context_lattice:
        x, y = point_transformation(*representant[elem])
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        pyplot.scatter(x, y, marker=type, zorder=1, color=formal_context_lattice.edge_color(elem, elem),
                       edgecolors='black')

        for neighbor in formal_context_lattice[elem]:
            x2, y2 = point_transformation(*representant[neighbor])
            color = formal_context_lattice.edge_color(elem, neighbor)
            if hierarchy_association[elem] != hierarchy_association[neighbor]:
                type = ":"
            else:
                type = "-"
            pyplot.plot([x, x2], [y, y2], color=color, zorder=0, linestyle=type)
    pyplot.show()

def edge_color(self, vertex1, vertex2=None):
    hierarchy_association = self.hierarchical_height()
    number_hierarchies = max(hierarchy_association.values()) + 1
    colors = matplotlib.cm.rainbow([0. + 1.0 * x / (number_hierarchies - 1) for x in range(number_hierarchies)])
    if vertex2 is None:
        vertex2 = vertex1

    return colors[max(hierarchy_association[vertex1], hierarchy_association[vertex2])]

def print_boxes(self):
    """Returns an object to print the lattice in the terminal.

    """
    context_matrix = ContextMatrix.from_lattice(self)
    context_matrix.reorder_doubly_lexical_order()
    lattice = self.to_box_lattice()
    boxes = self.boxes()

    return BoxesToString(boxes.values(),
                         context_matrix.elements, context_matrix.attributes,
                         {value: context_matrix.attributes[value[0][1]] for value in
                          boxes.values()},
                         lattice).run()

def boxes(self):
    """ Boxes and cluster number correspondence.

    A box is a couple ((l1, c1), (l2, c2)) where (l1, c1) is the top left corner (line, column) of the box and
    (l2, c2) the bottom right corner.

    :param matrix: doubly lexically ordered and Gamma free 0/1 matrix
    :return: :class:`dict` with key= class number and value= the associated box
    """
    context_matrix = ContextMatrix.from_lattice(self).reorder_doubly_lexical_order()
    matrix = context_matrix.matrix
    cluster_correspondence = dict()

    for i, line in enumerate(ClusterLineFromMatrix(matrix)):
        for j, elem in enumerate(line):
            if elem is None:
                continue
            if elem not in cluster_correspondence:
                cluster_correspondence[elem] = ((i, j), (i, j))
            else:
                begin, end = cluster_correspondence[elem]
                cluster_correspondence[elem] = (begin, (i, j))

    return cluster_correspondence


def to_box_lattice(self):
    context_matrix = ContextMatrix.from_lattice(self)
    context_matrix.reorder_doubly_lexical_order()
    box_lattice = Lattice()
    bottom = self.get_bottom()
    top = self.get_top()
    context_matrix = context_matrix.matrix
    cluster_correspondence = ClusterLineFromMatrix.boxes(context_matrix)

    last_line = last_line_not_0_for_matrix(context_matrix)
    last_clusters = [None] * len(context_matrix[0])
    line_iterator = ClusterLineFromMatrix(context_matrix)

    for i, current_line in enumerate(line_iterator):
        for j, elem in enumerate(current_line):
            if elem is None:
                continue

        j = len(current_line) - 1
        while j >= 0:
            if current_line[j] is None or current_line[j] in box_lattice:
                j -= 1
                continue

            current_cluster = current_line[j]
            # connect to bottom
            if i == last_line[j]:
                box_lattice.update([(bottom, cluster_correspondence[current_cluster])])

            # successor in line
            right_successor = True
            j_next = j + 1
            while j_next < len(current_line) and current_line[j_next] is None:
                j_next += 1

            if j_next == len(current_line):
                right_successor = False
            if i > 0 and line_iterator.previous_line[j] is not None:
                if j_next == len(current_line) or current_line[j_next] == line_iterator.previous_line[j_next]:
                    right_successor = False
            if right_successor:
                box_lattice.update([(cluster_correspondence[current_cluster],
                                     cluster_correspondence[current_line[j_next]])])

            # successor before line
            while j >= 0 and current_line[j] == current_cluster:
                if last_clusters[j] is not None and last_clusters[j] != current_cluster:
                    box_lattice.update([(cluster_correspondence[current_cluster],
                                         cluster_correspondence[last_clusters[j]])])
                    successor = last_clusters[j]
                    while j >= 0 and last_clusters[j] == successor:
                        j -= 1
                else:
                    break

            while j >= 0 and current_line[j] == current_cluster:
                j -= 1

        last_clusters = [new_cluster or old_cluster for new_cluster, old_cluster in
                         zip(current_line, last_clusters)]

    for vertex in set(x for x in box_lattice if box_lattice.degree(x) == 0):
        box_lattice.update([(vertex, top)])

    return box_lattice


def max_intersection(antichain):
    n_elements = len(antichain)
    indices_map = [i for i in range(n_elements)]
    random.shuffle(indices_map)
    i, j = 0, 1
    first_element, second_element = antichain[indices_map[i]], antichain[indices_map[j]]
    current_max = first_element.intersection(second_element)
    k = 2
    while k < n_elements:
        if current_max < first_element.intersection(antichain[indices_map[k]]):
            j = k
            second_element = antichain[indices_map[j]]
            current_max = first_element.intersection(second_element)
        elif current_max < second_element.intersection(antichain[indices_map[k]]):
            i = k
            first_element = antichain[indices_map[i]]
            current_max = first_element.intersection(second_element)
        k += 1
    return indices_map[i], indices_map[j]


def point_transformation_square(max_y):
    return lambda line, column: (column, max_y - line)


def last_line_not_0_for_matrix(matrix):
    last_line = [-1] * len(matrix[0])
    for j in range(len(matrix[0])):
        for i in range(len(matrix) - 1, -1, -1):
            if matrix[i][j] == 1:
                last_line[j] = i
                break
    return last_line
