from TBS.randomize import random_dismantable_lattice
from TBS.binarize import binarize, move_sup_irreducibles_to_atoms, dlo_contraction_order, contraction_trees, \
    flat_contraction_order
from TBS.draw_lattice import point_coordinates
from TBS.tree import draw_3d_support_tree
from TBS.contextmatrix import ContextMatrix

NUMBER_ELEMENTS = 20
lattice = random_dismantable_lattice(NUMBER_ELEMENTS)
flat_binarized_lattice = move_sup_irreducibles_to_atoms(binarize(lattice))
context_matrix = ContextMatrix.from_lattice(flat_binarized_lattice)
context_matrix.reorder_doubly_lexical_order()
order = flat_contraction_order(flat_binarized_lattice, dual=None, bottom="BOTTOM", dlo=context_matrix.elements)
trees = contraction_trees(flat_binarized_lattice, order=order, bottom="BOTTOM", dlo=True)
coordinates = point_coordinates(flat_binarized_lattice)
for tree in trees:
    draw_3d_support_tree(tree, coordinates, flat_binarized_lattice)
