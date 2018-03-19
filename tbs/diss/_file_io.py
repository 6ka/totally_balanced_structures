# -*- coding: utf-8 -*-

"""Load and save :class:`tbs.diss.Diss`

.. currentmodule:: tbs.diss.file_io

Module content
--------------

"""

__author__ = 'fbrucker'

__all__ = ["load", "save"]

from ._diss import Diss
from ._to_string import to_string


def load(f, kind="guess", sep=None, number=True):
    """Load a dissimilarity from file *f*.

    Empty lines, lines containing only whitespaces and lines beginning with ``'#'``
    are discarded.

    :param f: file
    :type f: :class:`file`

    :param kind: if ``'guess'``, looks for the appropriate type.The other possible
                 choices are: ``'square'``, ``'squarel'``, ``'upper'``, ``'upperl'``,
                 ``'lower'``, ``'lowerl'``, ``'squarep'``, ``'upperp'`` or ``'lowerp'``.
    :param sep: delimiter string
    :type sep: :class:`str`

    :param number: if :const:`True` , values are converted into :class:`float`, :class:`str` otherwise.

    :rtype: :class:`diss.Diss`

    .. seealso:: :func:`diss.conversion.to_string`
    """

    if kind not in ("guess",
                    "square", "upper", "lower",
                    "squarel", "upperl", "lowerl",
                    "squarep", "upperp", "lowerp"):
        raise TypeError("invalid parameter kind")

    lines = []
    for line in f:
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line.split(sep))
    if len(lines) < 1:
        raise ValueError("file contains no useful lines or empty file")
    if kind == "guess":
        if len(lines) == 1:
            if len(lines[0]) == 1:
                kind = "square"
            elif len(lines[0]) == 2:
                kind = "squarel"
            else:
                raise ValueError(" is not a valid kind of file")
        else:
            if len(lines) > 1 and len(lines[0]) == 1 and int(lines[0][0]) == len(lines) - 1:
                if len(lines) == 2 and len(lines[1]) == 1:
                    kind = "upperp"
                elif len(lines) == 2 and len(lines[1]) == 2:
                    kind = "squarep"
                elif len(lines[1]) == int(lines[0][0]) + 1:
                    kind = "squarep"
                elif len(lines[1]) == int(lines[0][0]):
                    kind = "upperp"
                else:
                    kind = "lowerp"
            elif len(lines[0]) == len(lines[1]):
                kind = (len(lines) == len(lines[0])) and "square" or "squarel"
            elif len(lines[0]) < len(lines[1]):
                kind = (len(lines[0]) == 2) and "lowerl" or "lower"
            else:
                kind = (len(lines[-1]) == 2) and "upperl" or "upper"

    if kind == "squarep":
        lines.pop(0)
    elif kind == "upperp":
        lines.pop(0)
        for line in lines:
            line.insert(1, str(0))
    elif kind == "lowerp":
        lines.pop(0)
        for line in lines:
            line.append(str(0))
    if kind in ("upperl", "lowerl", "squarel",
                "squarep", "lowerp", "upperp"):
        kind = kind[:-1]
        labels = []
        for i, line in enumerate(lines):
            labels.append(line.pop(0).strip())
    else:
        labels = range(len(lines))

    count = 0

    for i, line in enumerate(lines):
        if kind == "square":
            if len(line) != len(lines):
                raise ValueError("line %i contains %i values (instead of %i for a %s matrix)" %
                                 (i + 1, len(line), len(lines), kind))
        elif kind == "upper":
            if len(line) != len(lines) - i:
                raise ValueError("line %i contains %i values (instead of %i for a %s matrix)" %
                                 (i + 1, len(line), len(lines) - i, kind))
        elif kind == "lower":
            if len(line) != i + 1:
                raise ValueError("line %i contains %i values (instead of %i for a %s matrix)" %
                                 (i + 1, len(line), i + 1, kind))

    d = Diss(labels)
    for i in range(len(d)):
        # noinspection PyArgumentList
        for j in range(i, len(d)):

            if kind == "square":
                value = lines[i][j]
                if lines[i][j] != lines[j][i]:
                    raise ValueError("not symmetrical matrix")
            elif kind == "upper":
                value = lines[i][j - i]
            else:
                #kind == lower
                value = lines[j][i]
            if number:
                value = float(value)

            d.set_by_pos(i, j, value)
    return d


def save(dissimilarity, f, kind="square", sep=" "):
    """Write the dissimilarity *d* in file f.

    :param dissimilarity: dissimilarity to save
    :type dissimilarity: :class:`tbs.diss.Diss`
    :param f: file
    :param kind: if ``'guess'``, looks for the appropriate type.The other possible
                 choices are: ``'square'``, ``'squarel'``, ``'upper'``, ``'upperl'``,
                 ``'lower'``, ``'lowerl'``, ``'squarep'``, ``'upperp'`` or ``'lowerp'``.
    :param sep: delimiter string
        :type sep: one caracter

    .. seealso:: :func:`tbs.conversion.to_string.from_diss`
    """

    f.write(to_string(dissimilarity, kind, sep))

    return f
