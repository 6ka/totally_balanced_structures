__author__ = "cchatel", "fbrucker"


from matplotlib import pyplot
import matplotlib


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
