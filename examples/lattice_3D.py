from TBS.randomize import random_dismantable_lattice
from TBS.binarize import binarize, move_sup_irreducibles_to_atoms
from TBS.contextmatrix import ContextMatrix
from TBS.clusters import to_string
from TBS.hierarchical_decomposition import hierarchical_height_from_lattice
from TBS import clusters
from TBS.draw_lattice import draw, draw_3d
from matplotlib import pyplot
import matplotlib

NUMBER_OF_ELEMENTS = 12
lattice = random_dismantable_lattice(NUMBER_OF_ELEMENTS)

binarized_lattice = binarize(lattice)
flat_binarized_lattice = move_sup_irreducibles_to_atoms(binarized_lattice)

context_matrix = ContextMatrix.from_lattice(flat_binarized_lattice)
context_matrix.reorder_doubly_lexical_order()

box_matrix = to_string.from_dlo_gamma_free_context_matrix(context_matrix)
print("Box matrix\n", box_matrix)
formal_context_lattice = clusters.from_dlo_gamma_free_matrix.lattice(context_matrix.matrix)
hierarchy_association = hierarchical_height_from_lattice(formal_context_lattice)

hierarchy_association["BOTTOM"] = max(hierarchy_association.values()) + 1
hierarchy_association["TOP"] = 0

number_hierarchies = max(hierarchy_association.values()) + 1

points = {box: box[0] for box in formal_context_lattice if box not in ("BOTTOM", "TOP")}
points["BOTTOM"] = (len(context_matrix.matrix), 0)
points["TOP"] = (0, len(context_matrix.matrix[0]))
colors = matplotlib.cm.rainbow([0. + 1.0 * x / (number_hierarchies - 1) for x in range(number_hierarchies)])
draw(formal_context_lattice, colors)

pyplot.show()
draw_3d(flat_binarized_lattice, colors, hierarchy_association)

pyplot.show()

draw_3d(flat_binarized_lattice, colors, hierarchy_association, z_position="cross")

pyplot.show()
