"""

.. autoclass:: tbs.diss.Diss
    :special-members:
    :members:
    :exclude-members: __init__

.. automethod:: __init__

"""


__author__ = 'fbrucker'

__all__ = ["Diss"]

from ._to_string import to_string


class Diss(object):
    """Generic Dissimilarity class.
    """

    def __init__(self, elements=tuple(), value=0):
        """A dissimilarity d on *elements*.

        Create a constant *value* dissimilarity.

        Args:
            elements (iterable): list of pairwise different elements. The ordering is important when accessing the
                elements by position instead of value.
            value: initial value.

        Returns:
            A constant *value* dissimilarity for the *elements*
        """

        if not elements:
            elements = []

        self._vertex = []
        self.vertex_index = dict()
        for index, element in enumerate(elements):
            self._vertex.append(element)
            self.vertex_index[element] = index

        n = len(self._vertex)
        # list [[d(0,0)..d(n,n)],[d(1,1)..d(n,n)],...,[d(n,n)]]
        if n:
            self._d = [[value] * (n - i) for i in range(n)]
        else:
            self._d = []

    @classmethod
    def from_json(cls, json_diss):
        """Diss from json format

        Args:
            json_diss(dict): {"elements": [,],  "matrix": [[]]}. "elements" is optional, and matrix can be either
                             lower-triangular, upper-triangular, or square.

        Returns(Diss): the context matrix associated with the json.
        """
        if len(json_diss["matrix"][0]) == 1:
            kind = "lower"
            elements = list(range(len(json_diss["matrix"][-1])))
        elif len(json_diss["matrix"][-1]) == 1:
            kind = "upper"
            elements = list(range(len(json_diss["matrix"][0])))
        else:
            kind = "square"
            elements = list(range(len(json_diss["matrix"][0])))

        diss = Diss(json_diss.get("elements", elements))

        for i, line in enumerate(json_diss["matrix"]):
            for j, value in enumerate(line):
                if kind == "upper":
                    j += i
                diss.set_by_pos(i, j, value)

        return diss

    def json(self):
        """Json format.

        The matrix is lower-triangular.

        returns(dict): {"elements": [,], "matrix": [[]]}
        """

        return {"elements": self._vertex, "matrix": [[self.get_by_pos(i, j) for j in range(i + 1)]
                                                     for i in range(len(self))]}

    def __str__(self):
        """Square matrix representation."""

        return to_string(self)

    def __len__(self):
        """Number of elements in the base set."""

        return len(self._vertex)

    def __iter__(self):
        """Iteration upon the base set."""

        for x in self._vertex:
            yield x

    def __getitem__(self, pair):
        """Dissimilarity value.

        Args:
            pair (couple): couple of elements.

        Returns:
            the value of the couple of elements.
        """

        x, y = pair
        return self(x, y)

    def __setitem__(self, pair, value):
        """Dissimilarity value.

        Args:
            pair: couple of elements.
            value: dissimilarity new value.
        """

        x, y = pair
        idx1, idx2 = self.vertex_index[x], self.vertex_index[y]
        self.set_by_pos(idx1, idx2, value)
        return value

    def __call__(self, x, y):
        """Dissimilarity between elements x and y."""

        idx1, idx2 = self.vertex_index[x], self.vertex_index[y]
        if idx1 > idx2:
            idx1, idx2 = idx2, idx1

        return self._d[idx1][idx2 - idx1]

    def set_by_pos(self, index_1, index_2, value):
        """Dissimilarity value.

        :param index_1: index of the first element
        :type index_1: :class:`int`
        :param index_2: index of the second element
        :type index_2: :class:`int`

        :param value: dissimilarity new value.
        """
        if index_1 > index_2:
            index_1, index_2 = index_2, index_1
        self._d[index_1][index_2 - index_1] = value

    def get_by_pos(self, index_1, index_2):
        """Dissimilarity value.

        :param index_1: index of the first element
        :type index_1: :class:`int`
        :param index_2: index of the second element
        :type index_2: :class:`int`

        """
        if index_1 > index_2:
            index_1, index_2 = index_2, index_1
        return self._d[index_1][index_2 - index_1]

    def label_by_pos(self, i):
        return self._vertex[i]

    def values(self, xx=False):
        """All dissimilarity values.

        :param xx: if :const:`True` , the values of *self* (x, x) are also added.
        :type xx: :class:`bool`
        """

        vals = set()
        elems = list(self)
        for i, x in enumerate(elems):
            for y in elems[i:]:
                if x != y or xx:
                    vals.add(self(x, y))
        return frozenset(vals)

    def update(self, d, xx=False):
        """Update the value of the dissimilarity according to *d*.

        :param d: defined for the elements of *self*.
        :type d: function(x, y)

        :param xx: if :const:`True` , the values of *self* (x, x) are also updated.
        :type xx: :class:`bool`

        :returns: self[x, y] = d(x, y)
        """

        elems = list(self)
        for x in range(len(elems)):
            # noinspection PyArgumentList
            for y in range(x, len(elems)):
                if x != y or xx:
                    self[elems[x], elems[y]] = d(elems[x], elems[y])
        return self

    def update_by_pos(self, index_correspondence, xx=False):
        """Update the value of the dissimilarity according to *index_correspondence*.

        :param index_correspondence: defined for the indices of d (from 0 to len(d)-1).
        :type index_correspondence: function(x, y)

        :param xx: if :const:`True` , the values of *self* (x, x) are also updated.
        :type xx: :class:`bool`

        :returns: self[x, y] = d(x, y)
        """

        for x in range(len(self)):
            for y in range(x, len(self)):
                if x != y or xx:
                    self.set_by_pos(x, y, index_correspondence(x, y))
        return self

    def restriction(self, element_subset):
        """Restriction to *Y*.

        :param element_subset: subset of self's base set. If ``None``, Y is considered to be the base set.
        :type element_subset: iterable

        :rtype: :class:`Diss`
        """

        return self.__class__(element_subset).update(self, True)

    def copy(self):
        return self.__class__(self._vertex).update(self, True)

    def rename(self, x, new_x):
        """Rename element *x* to *new_x*.

        :param x: element of *self*.
        :param new_x: the replacing element.

        :raises: :exc:`ValueError` if either *x* is not an element or
                 *new_x* is already one.
        """

        if (x not in self) or (new_x in self):
            raise ValueError("Element already present or removing a non-element.")
        self._vertex[self.vertex_index[x]] = new_x
        self.vertex_index[new_x] = self.vertex_index[x]
        del self.vertex_index[x]
        return new_x

    def add(self, x, zero=0):
        """Add *x* to the base set.

        :param x: element not in *self*.
        :param zero: *self* (x, y) = zero for any y in the base set.

        :raises: :exc:`ValueError` if *x* is already an element.
        """

        if x in self.vertex_index:
            raise ValueError("Element already present.")

        self._vertex.append(x)
        self.vertex_index[x] = len(self._vertex) - 1
        self._d.append([])
        for y in range(len(self)):
            self._d[y].append(zero)

        return x

    def remove(self, x):
        if x not in self:
            raise ValueError("Element not present.")

        pos = self.vertex_index[x]
        for y in range(pos):
            del self._d[y][pos - y]
        del self._d[pos]

        self._vertex.remove(x)
        self.vertex_index = {x: i for i, x in enumerate(self._vertex)}
        return x

    def __nonzero__(self):
        """False if no elements."""

        if self._vertex:
            return True
        return False

    # rich comparison
    def _base_set_equality(self, other):
        if len(self._vertex) != len(list(other)):
            return False
        for x in self:
            if x not in other:
                return False

        return True

    def __lt__(self, d):
        """Pairwise order. Must have the same base set."""

        if not self._base_set_equality(d):
            return False

        strict = False
        for x in self:
            for y in d:
                if self(x, y) > d(x, y):
                    return False
                if self(x, y) < d(x, y):
                    strict = True
        return strict

    def __le__(self, d):
        """Pairwise order. Must have the same base set."""

        if not self._base_set_equality(d):
            return False

        for x in self:
            for y in d:
                if self(x, y) > d(x, y):
                    return False
        return True

    def __eq__(self, d):
        """Same base set and the same values."""

        if not self._base_set_equality(d):
            return False

        # values
        for x in self:
            for y in d:
                if self(x, y) != d(x, y):
                    return False

        return True

    def __ne__(self, d):
        """not ==."""

        return not self == d

    def __gt__(self, d):
        """Pairwise order. Must have the same base set."""

        if not self._base_set_equality(d):
            return False

        # values
        strict = False
        for x in self:
            for y in d:
                if self(x, y) < d(x, y):
                    return False
                if self(x, y) > d(x, y):
                    strict = True

        return strict

    def __ge__(self, d):
        """Pairwise order. Must have the same base set."""

        if not self._base_set_equality(d):
            return False

        # values
        for x in self:
            for y in d:
                if self(x, y) < d(x, y):
                    return False
        return True

    def __add__(self, other_dissimilarity):
        """result(x, y) = self(x, y) + other_dissimilarity(x, y).

        :param other_dissimilarity: its elements must contains those of *self*.
        :type other_dissimilarity: :class:`tbs.diss.Diss`

        :returns: the pointwise sum.
        :rtype: :class:`tbs.diss.Diss`
        """

        elems = list(self)
        result = self.__class__(elems)

        for i, x in enumerate(elems):
            for y in elems[i:]:
                result[x, y] = self(x, y) + other_dissimilarity(x, y)
        return result

    def __sub__(self, d):
        """result(x, y) = self(x, y) - d(x, y).

        :param d: its elements must contains those of *self*.
        :type d: :class:`Diss`

        :returns: the pointwise differences.
        :rtype: :class:`Diss`
        """

        elems = list(self)
        result = self.__class__(elems)

        for i, x in enumerate(elems):
            for y in elems[i:]:
                result[x, y] = self(x, y) - d(x, y)
        return result

    def __mul__(self, d):
        """result(x, y) = self(x, y) * d(x, y).

        :param d: its elements must contains those of *self*.
        :type d: :class:`Diss`

        :returns: the pointwise multiplication.
        :rtype: :class:`Diss`
        """

        elems = list(self)
        result = self.__class__(elems)

        for i, x in enumerate(elems):
            for y in elems[i:]:
                result[x, y] = self(x, y) * d(x, y)
        return result

    def __truediv__(self, d):
        """result(x, y) = self(x, y) / d(x, y) for x != y.

        :param d: must have non zero values.
        :type d: :class:`tbs.diss.Diss`

        :returns: the pointwise / for pairs of different elements.
        :rtype: :class:`tbs.diss.Diss`

        .. warning:: values of result(x, x) are equal to *self*\ (x, x).
        """

        elems = list(self)
        result = self.__class__(elems)

        for i, x in enumerate(elems):
            for y in elems[i:]:
                if x == y:
                    result[x, y] = self(x, y)
                else:
                    result[x, y] = self(x, y) / d(x, y)
        return result

    # += -= *= and /=
    def __iadd__(self, value):
        """self(x, y) = self(x, y) + value for x != y.

        .. warning:: values of *self* (x, x) are unchanged.
        """

        elems = list(self)

        for i, x in enumerate(elems):
            for y in elems[i + 1:]:
                self[x, y] = self(x, y) + value

        return self

    def __isub__(self, value):
        """self(x, y) = self(x, y) - value for x != y.

        .. warning:: values of *self* (x, x) are unchanged.
        """

        elems = list(self)

        for i, x in enumerate(elems):
            for y in elems[i + 1:]:
                self[x, y] = self(x, y) - value

        return self

    def __imul__(self, value):
        """self(x, y) = self(x, y) * value for x != y.

        .. warning:: values of *self* (x, x) are unchanged.
        """

        elems = list(self)

        for i, x in enumerate(elems):
            for y in elems[i + 1:]:
                self[x, y] = self(x, y) * value

        return self

    def __itruediv__(self, value):
        """self(x, y) = self(x, y) / value for x != y.

        .. warning:: values of *self* (x, x) are unchanged.
        """

        elems = list(self)

        for i, x in enumerate(elems):
            for y in elems[i + 1:]:
                self[x, y] = self(x, y) / value

        return self

    # +d -d abs(d)
    def __pos__(self):
        """result(x, y) = +self(x, y)."""

        result = self.copy()
        elems = list(self)

        for i, x in enumerate(elems):
            for y in elems[i:]:
                result[x, y] = +self(x, y)
        return result

    def __neg__(self):
        """result(x, y) = -self(x, y)."""

        result = self.copy()
        elems = list(self)

        for i, x in enumerate(elems):
            for y in elems[i:]:
                result[x, y] = -self(x, y)
        return result

    def __abs__(self):
        """result(x, y) = :meth:`abs`\ (*self* (x, y))."""

        result = self.copy()
        elems = list(self)

        for i, x in enumerate(elems):
            for y in elems[i:]:
                result[x, y] = abs(self(x, y))
        return result
