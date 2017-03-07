# -*- coding: utf-8 -*-

"""Cover graph from doubly lexically ordered dismantable matrix

.. currentmodule:: TBS.clusters

Comes  from [BP_15_ICFCA]_


.. [BP_15_ICFCA] F. Brucker and P. Préa, Totally Balanced Formal Concepts, ICFA'15 proceedings, J. Baixeries, C. Sacarea, M Ojeda-Aciego eds, 169-182.



Module content
--------------

.. autosummary::
    :toctree:

    ClusterLineFromMatrix
    from_dlo_gamma_free_matrix
    to_string
    to_image
    concepts


"""

from .ClusterLineFromMatrix import ClusterLineFromMatrix
from . import from_dlo_gamma_free_matrix

__all__ = ["from_dlo_gamma_free_matrix",
           "ClusterLineFromMatrix", "to_string", "to_image", "concepts"]

