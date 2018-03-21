__author__ = "cchatel", "fbrucker"


def draw_to_pyplot(box_lattice, pyplot, color_scheme):
    """Draws the box lattice topyplot.
    """

    point = {box: box[0] for box in box_lattice}

    objects = box_lattice.sup_irreducible
    attributes = box_lattice.inf_irreducible

    hierarchy_association = box_lattice.hierarchical_height()

    for elem in box_lattice:
        x, y = point_transformation(*point[elem])
        if elem in objects:
            type = "^"
        elif elem in attributes:
            type = "v"
        else:
            type = "o"
        if elem in objects and elem in attributes:
            type = "d"
        pyplot.scatter(x, y, marker=type, zorder=1, color=edge_color(color_scheme, hierarchy_association, elem, elem),
                       edgecolors='black')

        for neighbor in box_lattice.above(elem):
            x2, y2 = point_transformation(*point[neighbor])
            color = edge_color(color_scheme, hierarchy_association, elem, neighbor)
            if hierarchy_association[elem] != hierarchy_association[neighbor]:
                type = ":"
            else:
                type = "-"
            pyplot.plot([x, x2], [y, y2], color=color, zorder=0, linestyle=type)
    pyplot.show()


def edge_color(colors, hierarchy_association, vertex1, vertex2):
    return colors[max(hierarchy_association[vertex1], hierarchy_association[vertex2])]


def point_transformation(line, column):
    return column, -line
