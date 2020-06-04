import random
import collections

from ..lattice import Lattice

from tbs.graph import Graph, topological_sort

__author__ = "cchatel", "fbrucker"


class DismantlableLattice(Lattice):
    """
    Dismantlable Lattice
    """

    def support_tree(self):
        """Builds a support tree of an atomistic lattice.

        :return: a support tree
        :rtype: :class:`tbs.graph.Graph`
        """
        if not self.is_atomistic():
            raise ValueError("lattice is not atomistic")

        class_order = topological_sort(self._hase_diagram)
        objects = self.above(self.bottom)
        representatives = {element: element for element in objects}
        classes = {element: {element} for element in objects}
        tree = Graph(objects)
        n_connected_parts = len(objects)
        colors = {obj: i for i, obj in enumerate(objects)}

        class_order_position = 1
        while n_connected_parts > 1:
            class_order_position += 1
            current_class_index = class_order[class_order_position]
            if current_class_index not in objects:
                predecessors = list(self.under(current_class_index))
                first_class_representative = representatives[predecessors[0]]
                second_class_representative = representatives[predecessors[1]]
                representatives[current_class_index] = random.choice(
                    [first_class_representative, second_class_representative])
                if colors[first_class_representative] != colors[second_class_representative]:
                    tree.update(((first_class_representative, second_class_representative),))
                    color_to_change = colors[second_class_representative]
                    color_to_keep = colors[first_class_representative]
                    for element in colors:
                        if colors[element] == color_to_change:
                            colors[element] = color_to_keep
                    n_connected_parts -= 1
                classes[current_class_index] = classes[predecessors[0]].union(classes[predecessors[1]])
        return tree

    def hierarchical_decomposition(self):
        """ Decompose the lattice into hierarchies.

        Every dismantlable lattice can be decomposed into hierarchy.

        Returns(dict):
            A :class:`dict` whose keys are are the the associated element of the lattice and their associated values
            the hierarchical level (0 is the first hierarchy).
        """

        vertex_height = dict()
        current_height = 0
        next_neighbor = dict()
        current_degree = {x: len(self._hase_diagram(x)) for x in self}
        sup_irreducibles = set(self.sup_irreducible)

        while sup_irreducibles:
            current_chains = set()
            deleted_sup_irreducibles = set()
            for current_sup_irreducible in sup_irreducibles:
                possible_chain = set()
                vertex = current_sup_irreducible
                is_hierarchical = False
                while current_degree[vertex] <= 1:
                    possible_chain.add(vertex)
                    if current_degree[vertex] == 0 or vertex in current_chains:
                        is_hierarchical = True
                        break
                    vertex = next_neighbor.get(vertex, list(self.above(vertex))[0])
                if is_hierarchical:
                    deleted_sup_irreducibles.add(current_sup_irreducible)
                    current_chains.update(possible_chain)

            for x in current_chains:
                vertex_height[x] = current_height
                for y in self.under(x):
                    current_degree[y] -= 1
                    if current_degree[y] == 1:
                        for z in self.above(y):
                            if z not in vertex_height:
                                next_neighbor[y] = z
                                break
            current_height += 1

            sup_irreducibles.difference_update(deleted_sup_irreducibles)
            vertex_height[self.bottom] = max(vertex_height.values()) + 1
        return vertex_height

    def is_binary(self):
        """Checks whether the lattice is binary or not i.e if every vertex except the bottom covers maximum two elements
         and is covered by maximum two elements

        :return: True if the lattice is binary, False if not
        :rtype: :class:`bool`
        """

        for element in self:
            if element != self.bottom and not self.isa_binary_element(element):
                return False
        return True

    def isa_binary_element(self, element):
        """Checks whether a given element is binary or not i.e if it covers maximum two elements
         and is covered by maximum two elements

        :return: True if the lattice is binary, False if not
        :rtype: :class:`bool`
        """

        return len(self.above(element)) <= 2 and len(self.under(element)) <= 2

    def binarization_element_above(self, element, new_object=lambda lattice, x, y: len(lattice)):
        """Binarize an element covered by more than two elements

        Args:
            element: a non binary vertex of the lattice
            new_object(lattice, x, y -> new): return the new element in lattice sup of x and y.
        """

        while len(self.above(element)) > 2:
            successors = list(self.above(element))
            x = successors[0]
            y = successors[1]
            size = len(self.above_filter(self.sup(x, y)))

            for i in range(len(successors)):
                first = successors[i]
                for j in range(i + 1, len(successors)):
                    second = successors[j]
                    if len(self.above_filter(self.sup(first, second))) > size:
                        x = first
                        y = second
                        size = len(self.above_filter(self.sup(first, second)))
            new = new_object(self, x, y)

            self._hase_diagram.add(new)
            self._hase_diagram.difference([(element, x), (element, y)])
            self._hase_diagram.update([(new, x), (new, y), (element, new)])

            self._order.add(new)
            self._order.update([(new, x), (new, y), (element, new)])
            self._order.update((z, new) for z in self._order(element, begin=False, end=True))
            self._order.update((new, z) for z in self._order(x))
            self._order.update((new, z) for z in self._order(y))

        return self

    def binarization_element_under(self, element, new_attribute=lambda lattice, x, y: frozenset((x, y))):
        """Binarize an element above more than two elements

        Args:
            element: a non binary vertex of the lattice.
            new_attribute(lattice, x, y -> new): return the new element in lattice sup of x and y.
        """
        while len(self.under(element)) > 2:
            predecessors = list(self.under(element))
            x = predecessors[0]
            y = predecessors[1]
            size = len(self.under_filter(self.inf(x, y)))

            for i in range(len(predecessors)):
                first = predecessors[i]
                for j in range(i + 1, len(predecessors)):
                    second = predecessors[j]
                    if len(self.under_filter(self.inf(first, second))) > size:
                        x = first
                        y = second
                        size = len(self.under_filter(self.inf(first, second)))
            new = new_attribute(self, x, y)

            self._hase_diagram.add(new)
            self._hase_diagram.difference([(x, element), (y, element)])
            self._hase_diagram.update([(x, new), (y, new), (new, element)])

            self._order.add(new)
            self._order.update([(x, new), (y, new), (new, element)])
            self._order.update((new, z) for z in self._order(element))
            self._order.update((z, new) for z in self._order(x, begin=False, end=True))
            self._order.update((z, new) for z in self._order(y, begin=False, end=True))

        return self

    def binarize_element(self, element,
                         new_object=lambda lattice, x, y: len(lattice),
                         new_attribute=lambda lattice, x, y: frozenset((x, y))):
        """Binarize an element in both direction

        Args:
            element: a non binary vertex of the lattice.
            new_object(lattice, x, y -> new): return the new element in lattice sup of x and y.
            new_attribute(lattice, x, y -> new): return the new element in lattice sup of x and y.
        """

        self.binarization_element_above(element, new_object)
        self.binarization_element_under(element, new_attribute)

        return self

    def binarize_bottom_up(self, ignored_elements=('BOTTOM',), new_object=lambda lattice, x, y: len(lattice)):
        """Modifies the lattice such that no element is covered by more than two elements.

        Args:
            ignored_elements(iterable): elements not to binarize
            new_object(lattice, x, y -> new): return the new object in lattice sup of x and y.
        """
        fifo = collections.deque((self.bottom,))
        is_seen = {self.bottom}

        while fifo:
            vertex = fifo.pop()
            if len(self.above(vertex)) > 2 and vertex not in ignored_elements:
                self.binarization_element_above(vertex, new_object)
            visit_list = self.above(vertex)
            for neighbor in visit_list:
                if neighbor not in is_seen:
                    is_seen.add(neighbor)
                    fifo.appendleft(neighbor)

        return self

    def binarize_top_down(self, ignored_elements=frozenset()):
        """Modifies the lattice such that no element covers more than two elements.

        :param ignored_elements: elements not to binarize
        :type ignored_elements: iterable
        """

        fifo = collections.deque((self.top,))
        is_seen = {self.top}

        while fifo:
            # print("\n", fifo)
            vertex = fifo.pop()
            # print("element ", vertex)
            if len(self.under(vertex)) > 2 and vertex not in ignored_elements:
                self.binarization_element_under(vertex)
            visit_list = self.under(vertex)
            for neighbor in visit_list:
                if neighbor not in is_seen:
                    is_seen.add(neighbor)
                    fifo.appendleft(neighbor)

        return self

    def binarize(self, ignored_elements=('BOTTOM',)):
        """Modifies the lattice such that it is binary

        :param ignored_elements: elements not to binarize
        """
        self.binarize_bottom_up(ignored_elements=ignored_elements)
        self.binarize_top_down(ignored_elements=ignored_elements)

        return self

    def other_above(self, element, first_successor):
        """Returns the successor of element different from first_successor in a binary lattice

        :param element: vertex
        :type first_successor: vertex

        :return: the other successor of element
        """
        successors = list(self.above(element))
        if len(successors) != 2:
            raise ValueError("element is not binary in lattice")
        elif successors[0] == first_successor:
            return successors[1]
        elif successors[1] == first_successor:
            return successors[0]
        else:
            raise ValueError("first_successor is not a successor of element in lattice")

    def other_under(self, element, first_predecessor):
        """Returns the predecessor of element different from first_predecessor in a binary lattice

        :param element: vertex
        :type first_predecessor: vertex

        :return: the other predecessor of element
        """
        predecessors = list(self.under(element))
        if len(predecessors) != 2:
            raise ValueError("element is not binary in lattice")
        elif predecessors[0] == first_predecessor:
            return predecessors[1]
        elif predecessors[1] == first_predecessor:
            return predecessors[0]
        else:
            raise ValueError("first_successor is not a successor of element in lattice")

    def decomposition_order(self):
        """Computes a compatible contraction order.

        :return: ordered list of all the vertices
        :rtype: list
        """
        if not self.is_atomistic():
            self.make_atomistic()
        objects = set(self.above(self.bottom))
        predecessors_exist = set()
        take_after = set()
        arrow_head = set()
        arrows = {}
        order = []
        is_built = objects.copy()
        for element in objects:
            for successor in self.above(element):
                if self.other_under(successor, element) in objects:
                    predecessors_exist.add(successor)
        while len(predecessors_exist) > 0:
            chosen_candidate = random.sample(predecessors_exist - take_after, 1)[0]
            predecessors_exist.remove(chosen_candidate)
            is_built.add(chosen_candidate)
            order.append(chosen_candidate)
            arrows[chosen_candidate] = []
            for predecessor in self.under(chosen_candidate):
                if len(self.above(predecessor)) == 2:
                    other_succ = self.other_above(predecessor, chosen_candidate)
                    if other_succ not in is_built:
                        arrow_head.add(chosen_candidate)
                        arrows[chosen_candidate].append(predecessor)
                    else:
                        arrows[other_succ].remove(predecessor)
                        if len(arrows[other_succ]) == 0:
                            arrow_head.remove(other_succ)
                            for successor in self.above(other_succ):
                                if self.other_under(successor, other_succ) not in arrow_head:
                                    take_after.discard(successor)
            for successor in self.above(chosen_candidate):
                if self.other_under(successor, chosen_candidate) in is_built:
                    predecessors_exist.add(successor)
                    for other_succ_pred in self.under(successor):
                        if other_succ_pred in arrow_head:
                            take_after.add(successor)
        return order
