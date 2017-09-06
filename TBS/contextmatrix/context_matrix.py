from TBS import orders


class ContextMatrix(object):
    """Context matrix."""

    def __init__(self, matrix, elements=tuple(), attributes=tuple(), copy_matrix=True):
        """Context matrix

        :param matrix: 2-dimensional 0/1-matrix whose lines are objects_name and columns attributes_name.
        :type matrix: :class:`list` of :class:`list`.

        :param elements: Objects name. Must coincide with the *matrix* number of line. Line number by default
        :type elements: :class:`list` of :class:`str`.

        :param attributes: Attributes name. Must coincide with the *matrix* number of columns. Column number by default
        :type attributes: :class:`list` of :class:`str`.
        :param copy_matrix: if False link the matrix, copy it otherwise
        :type copy_matrix: :class:`bool`
        """

        if copy_matrix:
            self.matrix = matrix
        else:
            self._matrix = matrix
        self._elements = elements and tuple(elements) or tuple(range(len(self._matrix)))
        self._attributes = attributes and tuple(attributes) or tuple(range(len(self._matrix[0])))

    @staticmethod
    def from_lattice(lattice, inf=None, sup=None):
        """ Context matrix from lattice cover graph.

        the elements are the sup-irreducibles elements
        the attributes the inf-irreducibles elements

        :param lattice: cover graph of some lattice.
        :type lattice: directed :class:`CTK.graph.Graph`

        :param inf: inf-irreducible order
        :type inf: tuple

        :param sup: sup-irreducible order
        :type sup: tuple

        """
        if inf is None:
            inf = list(lattice.inf_irreducible())
        else:
            inf = list(inf)
        inf_indices = {x: i for i, x in enumerate(inf)}
        if sup is None:
            sup = list(lattice.sup_irreducible())
        else:
            sup = list(sup)
        sup_indices = {x: i for i, x in enumerate(sup)}

        matrix = []
        for i in range(len(sup)):
            matrix.append([0] * len(inf))

        def get_attribute_action_for_sup(sup_irreducible_element):
            """
            :param sup_irreducible_element: lattice element.
            :return: :func:
            """
            sup_index = sup_indices[sup_irreducible_element]

            def action(lattice_element):
                """
                :param lattice_element: lattice element
                """
                if lattice_element in inf_indices:
                    matrix[sup_index][inf_indices[lattice_element]] = 1

            return action

        for vertex in sup:
            lattice.dfs(vertex, get_attribute_action_for_sup(vertex))

        return ContextMatrix(matrix, sup, inf)

    @staticmethod
    def from_clusters(clusters, elements=None):
        """

        Args (iterable):
            clusters: iterable of iterable from a base set. Forms the column order.
            elements: line order. If None, is union of all the clusters.

        Returns: `ContextMatrix`

        """

        base_set = set()
        for cluster in clusters:
            base_set.update(cluster)

        if elements is None:
            elements = list(base_set)

        correspondance = {elem: index for index, elem in enumerate(elements)}

        matrix = []
        for i in range(len(elements)):
            matrix.append([0] * len(clusters))

        for j, cluster in enumerate(clusters):
            for elem in cluster:

                matrix[correspondance[elem]][j] = 1

        return ContextMatrix(matrix, elements=elements)

    def __str__(self):
        from .conversion.to_string import to_string

        return to_string(self)

    def copy(self):
        """Deep copy."""

        return ContextMatrix(self._matrix, self.elements, self.attributes)

    @property
    def matrix(self):
        """binary matrix."""

        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        """binary matrix.

        :param matrix: is copied to become the new binary matrix.
        """
        self._matrix = [list(line) for line in matrix]

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

    def reorder(self, line_permutation=None, column_permutation=None):
        """Line and column reordering.

        :param line_permutation: permutation index list. current line number i will be line number line_permutation[i].
                                 if `None` no line permutation.
        :type line_permutation: `iterable`of :class:`int`

        :param column_permutation: permutation index list. current column number j will be line number
                                   column_permutation[j].
                                   if `None` no column permutation.
        :type column_permutation: `iterable`of :class:`int`
        """

        if line_permutation:
            new_elements = [""] * len(self.elements)
            new_matrix = [[]] * len(self.elements)
            for i in range(len(self.elements)):
                new_elements[line_permutation[i]] = self.elements[i]
                new_matrix[line_permutation[i]] = self._matrix[i]
            self.elements = new_elements
            self._matrix = new_matrix

        if column_permutation:
            new_attributes = [""] * len(self.attributes)
            for i in range(len(self.attributes)):
                new_attributes[column_permutation[i]] = self.attributes[i]
            self.attributes = new_attributes
            for i in range(len(self._matrix)):
                new_line = [0] * len(self._matrix[i])
                for j in range(len(self._matrix[i])):
                    new_line[column_permutation[j]] = self._matrix[i][j]
                self._matrix[i] = new_line

    def transpose(self):
        """ Return the transpose.

         :rtype: :class:`TBS.contextmatrix.ContextMatrix`
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

        :rtype: ContextMatrix :class:`TBS.contextmatrix.ContextMatrix`
        """

        return self.submatrix_elements_indices([self.elements.index(element) for element in elements])

    def submatrix_elements_indices(self, element_indices):
        """Submatrix with only selected element indices

        :param element_indices:  iterable of element indices
        :type element_indices: `iterable`

        :rtype: ContextMatrix :class:`TBS.contextmatrix.ContextMatrix`
        """

        submatrix = [self._matrix[i] for i in sorted(element_indices)]
        submatrix_elements = [self.elements[i] for i in sorted(element_indices)]
        return ContextMatrix(submatrix, submatrix_elements, self.attributes)

    def reorder_doubly_lexical_order(self):
        lines, columns = orders.doubly_lexical_order(self._matrix)

        line_permutation = [0] * len(self._matrix)
        for i, index in enumerate(lines):
            line_permutation[index] = i

        column_permutation = [0] * len(self._matrix[0])
        for i, index in enumerate(columns):
            column_permutation[index] = i

        self.reorder(line_permutation, column_permutation)
        return self
