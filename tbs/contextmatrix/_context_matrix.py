from ._order import doubly_lexical_order, is_doubly_lexically_ordered
from ._to_string import to_string


class ContextMatrix(object):
    """Context matrix."""

    def __init__(self, matrix, elements=tuple(), attributes=tuple()):
        """Context matrix

        Args:
            matrix(list of list): 2-dimensional 0/1-matrix whose lines are objects_name and columns attributes_name.
                Is a list of lines.

            elements(list of hashable): Objects name. Length must coincide with the *matrix* number of line. Line
                number by default.
            attributes(list of hashable): Attributes name. Length must coincide with the *matrix* number of columns.
                Column number by default.
            copy_matrix(bool): if False link the matrix, copy it otherwise.
        """

        self._matrix = tuple(tuple(line) for line in matrix)

        self._elements = elements and tuple(elements) or tuple(range(len(self._matrix)))
        self._attributes = attributes and tuple(attributes) or tuple(range(len(self._matrix[0])))

    @classmethod
    def from_context_matrix(cls, context_matrix):
        """copy of an existent context matrix."""

        return cls(context_matrix.matrix, context_matrix.elements, context_matrix.attributes)

    @classmethod
    def from_lattice(cls, lattice):
        """ Context matrix from Lattice

        the elements are the sup-irreducibles elements
        the attributes the inf-irreducibles elements

        Args:
            lattice(Lattice): cover graph of some lattice.
        """

        inf = list(lattice.inf_irreducible)
        inf_indices = {x: i for i, x in enumerate(inf)}

        sup = list(lattice.sup_irreducible)
        sup_indices = {x: i for i, x in enumerate(sup)}

        matrix = []
        for i in range(len(sup)):
            matrix.append([0] * len(inf))

        order = lattice.directed_comparability
        for vertex in sup:
            sup_index = sup_indices[vertex]
            for x in order(vertex, closed=True):
                if x in inf_indices:
                    matrix[sup_index][inf_indices[x]] = 1

        return cls(matrix, sup, inf)

    @classmethod
    def from_clusters(cls, clusters, elements=None):
        """

        Args:
            clusters(iterable): iterable of iterable from a base set. Forms the column order.
            elements(iterable): line order. If None, is union of all the clusters.
        """

        if elements is None:
            base_set = set()
            for cluster in clusters:
                base_set.update(cluster)

            elements = list(base_set)

        correspondance = {elem: index for index, elem in enumerate(elements)}

        matrix = []
        for i in range(len(elements)):
            matrix.append([0] * len(clusters))

        for j, cluster in enumerate(clusters):
            for elem in cluster:
                matrix[correspondance[elem]][j] = 1

        return cls(matrix, elements=elements)

    @classmethod
    def from_json(cls, json_matrix):
        """ContextMatrix from json format

        Args:
            json_matrix(dict): {"elements": [,], "attributes": [,], "matrix": [[]]}. "elements" and "attributes" are
                               optional.
        Returns(ContextMatrix): the context matrix associated with the json.
        """

        return cls(json_matrix["matrix"], json_matrix.get("elements", tuple()), json_matrix.get("attributes", tuple()))

    def json(self):
        """Json format.

        returns(dict): {"elements": [,], "attributes": [,], "matrix": [[]]}
        """

        return {"matrix": self.matrix, "elements": self.elements, "attributes": self.attributes}

    def transpose(self):
        """ Return the transpose.

        Returns(ContextMatrix): The transpose.
        """
        matrix = []
        for i in range(len(self._matrix[0])):
            matrix.append([0] * len(self._matrix))

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = self._matrix[j][i]

        return ContextMatrix(matrix, self.attributes, self.elements)

    def submatrix_elements(self, elements):
        """Submatrix with only selected elements

        :param elements:  iterable of elements
        :type elements: `iterable`

        :rtype: ContextMatrix :class:`tbs.contextmatrix.ContextMatrix`
        """

        return self.submatrix_elements_indices([self.elements.index(element) for element in elements])

    def submatrix_elements_indices(self, element_indices):
        """Submatrix with only selected element indices

        :param element_indices:  iterable of element indices
        :type element_indices: `iterable`

        :rtype: ContextMatrix :class:`tbs.contextmatrix.ContextMatrix`
        """

        submatrix = [self._matrix[i] for i in sorted(element_indices)]
        submatrix_elements = [self.elements[i] for i in sorted(element_indices)]
        return ContextMatrix(submatrix, submatrix_elements, self.attributes)

    def __str__(self):
        return to_string(self)

    def __repr__(self):

        return "".join(["ContextMatrix(",
                        repr(self.matrix),
                        ", ", "elements=", repr(self.elements),
                        ", ", "attributes=", repr(self.attributes),
                        ")"])

    @property
    def matrix(self):
        """binary matrix.

        Returns the matrix, not a copy of it. Should not be modified.

        Returns(list of list): 2-dimensional 0/1-matrix whose lines are objects_name and columns attributes_name.
        """

        return self._matrix

    @property
    def attributes(self):
        """attributes."""

        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """attributes.

        :param attributes: inf irreducible elements.
        """
        if len(attributes) != len(self._matrix[0]):
            raise ValueError("wrong size. Must be equal to the number of attributes")
        self._attributes = tuple(attributes)

    @property
    def elements(self):
        """elements."""
        return self._elements

    @elements.setter
    def elements(self, elements):
        """elements.

        :param elements: sup irreducible elements.

        """
        if len(elements) != len(self._matrix):
            raise ValueError("wrong size. Must be equal to the number of elements")
        self._elements = tuple(elements)

    def reorder_elements(self, permutation):
        """Line reordering.

        Args:
            permutation(list): list of elements consisting of the new order. Element at index i will be the ith line
            in the new context matrix.
        """

        index_correspondence = {element: i for i, element in enumerate(self.elements)}

        self.reorder_lines([index_correspondence[e] for e in permutation])

    def reorder_lines(self, permutation):
        """Line reordering.

        Args:
            permutation(list): permutation index list. current line number i will be line number permutation[i].
        """

        new_elements = [""] * len(self.elements)
        new_matrix = [[], ] * len(self.elements)
        for i in range(len(self.elements)):
            new_elements[i] = self.elements[permutation[i]]
            new_matrix[i] = self._matrix[permutation[i]]
        self.elements = tuple(new_elements)
        self._matrix = tuple(new_matrix)

    def reorder_attributes(self, permutation):
        """Column reordering.

        Args:
            permutation(list): list of attributes consisting of the new order. Attribute at index i will be the ith
            column in the new context matrix.
        """

        index_correspondence = {attribute: i for i, attribute in enumerate(self.attributes)}

        self.reorder_columns([index_correspondence[a] for a in permutation])

    def reorder_columns(self, permutation):
        """Column reordering.

        Args:
            permutation(list): permutation index list. current column number i will be column number permutation[i].
        """

        new_attributes = [""] * len(self.attributes)

        for i in range(len(self.attributes)):
            new_attributes[i] = self.attributes[permutation[i]]
        self.attributes = tuple(new_attributes)

        new_matrix = [[], ] * len(self.elements)
        for i in range(len(self._matrix)):
            new_line = [0] * len(self._matrix[i])
            for j in range(len(self._matrix[i])):
                new_line[j] = self._matrix[i][permutation[j]]
            new_matrix[i] = tuple(new_line)
        self._matrix = tuple(new_matrix)

    def is_doubly_lexically_ordered(self):
        """Test if the matrix is doubly lexically ordered."""

        return is_doubly_lexically_ordered(self.matrix)

    def reorder_doubly_lexical(self, order=None):
        lines, columns = doubly_lexical_order(self._matrix, order)

        self.reorder_lines(lines)
        self.reorder_columns(columns)

        return self
