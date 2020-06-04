__author__ = "cchatel", "fbrucker"

from ._box_lattice import box_lattice


def draw_to_pyplot(doubly_lexically_ordered_gamma_free, pyplot, color_scheme):
    """Draws the box lattice topyplot.

    The context matrix must be gamma free (otherwise `box_lattice(gamma_free.gamma_free.reorder_doubly_lexical())`).
    No check are performed.

    Args:
        doubly_lexically_ordered_gamma_free(GammaFree): doubly lexically ordered gama free context matrix.
    """

    lattice = box_lattice(doubly_lexically_ordered_gamma_free)

    point = {box: box[0] for box in lattice}

    objects = lattice.sup_irreducible
    attributes = lattice.inf_irreducible

    hierarchy_association = lattice.hierarchical_decomposition()
    nb_colors = max(hierarchy_association.values()) + 1

    colors = color_scheme([0. + 1.0 * x / (nb_colors - 1) for x in range(nb_colors)])
    pyplot.axis('off')

    for y, elem in enumerate(doubly_lexically_ordered_gamma_free.elements):
        x = 0
        while not doubly_lexically_ordered_gamma_free.matrix[y][x]:
            x += 1
        pyplot.text(x, -y, str(elem), ha='right', va='top')

    for x, attr in enumerate(doubly_lexically_ordered_gamma_free.attributes):
        y = 0
        while not doubly_lexically_ordered_gamma_free.matrix[y][x]:
            y += 1
        pyplot.text(x, -y, str(attr), ha='left', va='bottom')

    for elem in lattice:

        x, y = point_transformation(*point[elem])
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        pyplot.scatter(x, y, marker=type, zorder=1, color=edge_color(colors, hierarchy_association, elem, elem),
                       edgecolors='black')

        for neighbor in lattice.above(elem):
            x2, y2 = point_transformation(*point[neighbor])
            color = edge_color(colors, hierarchy_association, elem, neighbor)
            if hierarchy_association[elem] != hierarchy_association[neighbor]:
                type = ":"
            else:
                type = "-"
            pyplot.plot([x, x2], [y, y2], color=color, zorder=0, linestyle=type)


def edge_color(colors, hierarchy_association, vertex1, vertex2):
    return colors[max(hierarchy_association[vertex1], hierarchy_association[vertex2])]


def point_transformation(line, column):
    return column, -line
