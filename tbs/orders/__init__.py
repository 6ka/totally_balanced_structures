"""Orders.

.. currentmodule:: tbs.orders

Several orders useful for totally balanced structures.


Module content
--------------

"""

__all__ = ["is_doubly_lexical_ordered", "doubly_lexical_order",
           "chordal_order", "chordal_order_partition", "isa_chordal_order"]

from .doubly_lexical import is_doubly_lexical_ordered, doubly_lexical_order
from .chordal_order import chordal_order, chordal_order_partition, isa_chordal_order
