"""Gamma freecontext matrix.


.. [BP_15_ICFCA] F. Brucker and P. Préa, Totally Balanced Formal Concepts, ICFA'15 proceedings, J. Baixeries, C. Sacarea, M Ojeda-Aciego eds, 169-182.


"""

__all__ = ["GammaFree", "is_gamma_free_matrix",
           "box_lattice",
           "to_string",
           "draw_to_pyplot"]

from ._gamma_free import GammaFree, is_gamma_free_matrix
from ._box_lattice import box_lattice
from ._to_string import to_string
from ._draw_pyplot import draw_to_pyplot
