from TBS.randomize import random_dismantable_lattice
from TBS.binarize import binarize, move_sup_irreducibles_to_atoms, dlo_contraction_order, contraction_trees, \
    flat_contraction_order
from draw_lattice import draw_binarisation_trees_dlo_3d
from TBS.draw_lattice import point_coordinates
from TBS.tree import draw_3d_support_tree
from TBS.contextmatrix import ContextMatrix
from TBS.clusters.to_string import from_dlo_gamma_free_context_matrix

NUMBER_ELEMENTS = 20
lattice = random_dismantable_lattice(NUMBER_ELEMENTS)
flat_binarized_lattice = move_sup_irreducibles_to_atoms(binarize(lattice))
context_matrix = ContextMatrix.from_lattice(flat_binarized_lattice)
context_matrix.reorder_doubly_lexical_order()
print(from_dlo_gamma_free_context_matrix(context_matrix))
order = flat_contraction_order(flat_binarized_lattice, dual=None, bottom="BOTTOM", dlo=context_matrix.elements)
trees = contraction_trees(flat_binarized_lattice, order=order, bottom="BOTTOM", dlo=True)
coordinates = point_coordinates(flat_binarized_lattice)
draw_binarisation_trees_dlo_3d(flat_binarized_lattice, bottom="BOTTOM")
