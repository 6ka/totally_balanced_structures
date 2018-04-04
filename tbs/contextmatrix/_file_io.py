"""Load and save :class:`context_matrix.ContextMatrix`

.. currentmodule:: tbs.contextmatrix.file_io

Module content
--------------

.. autosummary::
    :toctree:

"""

__author__ = 'fbrucker'

__all__ = ["load", "save"]

from ._to_string import to_string
from ._context_matrix import ContextMatrix


def load(f, has_elements_label=True, has_attributes_label=True, has_attribute=lambda x: x == "1", sep=","):
    """Load a dissimilarity from file *f*.

    Empty lines, lines containing only whitespaces and lines beginig with ``'#'``
    are discarded.

    :param f: file
    :type f: :class:`file`

    :param has_elements_label: if first column is elements labels
    :type has_elements_label: :class:`bool`

    :param has_attributes_label: if first line is attributes names
    :type has_attributes_label: :class:`bool`

    :param has_attribute: True if element is present, Falseotherwise
    :type has_attribute: function(str) -> bool

    :param sep: delimiter string
    :type sep: :class:`str`. String split method arameter. If None, the string.split method is used with no parameter.

    :rtype: :class:`tbs.lattice.ContextMatrix`

    """

    attributes_labels = []
    elem_labels = []
    table = []

    my_split = lambda string: sep is None and string.split() or string.split(sep)

    if has_attributes_label:
        attributes_labels = my_split(f.readline().strip())

    l = f.readline()

    while l:
        elems = my_split(l)
        if has_elements_label:
            elem_labels.append(elems[0])
            del elems[0]

        table.append([has_attribute(x.strip()) and 1 or 0 for x in elems])

        l = f.readline()

    return ContextMatrix(table, elem_labels, attributes_labels)


def save(context_matrix, f, has_attribute="1", has_not_attribute="0", has_elements_label=True,
         has_attributes_label=True, sep=" "):
    """Write the contextmatrix in file f

    :param context_matrix: context matrix to save
    :type context_matrix: :class:`tbs.lattice.ContextMatrix`

    :param f: file opened forw writing

    :param has_attribute: string printed when element has attribute
    :type has_attribute: :class:`str`

    :param has_not_attribute: string printed when element has attribute
    :type has_not_attribute: :class:`str`

    :param has_elements_label: if first column is elements labels
    :type has_elements_label: :class:`bool`

    :param has_attributes_label: if first line is attributes names
    :type has_attributes_label: :class:`bool`

    :param sep: delimiter string
    :type sep: one character

    """

    f.write(to_string(context_matrix, has_attribute, has_not_attribute, has_elements_label,
                      has_attributes_label, sep))

    return f
