from TBS.observer import Observable
from TBS.graph import Graph
from TBS.tree import radial_draw_tree
import collections
import random
from TBS.clusters import ClusterLineFromMatrix
from TBS.contextmatrix import ContextMatrix
from matplotlib import pyplot
import matplotlib
from TBS.clusters.to_string import BoxesToString

__author__ = "cchatel", "fbrucker"


class Lattice(Graph, Observable):
    """
    Lattice class seen as the oriented cover graph of the actual lattice
    """

    def __init__(self, vertices=tuple(), edges=tuple(), dual=None):
        """Creates a lattice object with vertices vertices and edges edges.

        :param vertices: a tuple of vertices to initialize the lattice
        :type vertices: iterable
        :param edges: a tuple of edges to initialize the lattice
        :type edges: iterable
        :param dual: used to maintain dual up to date, not to be used
        :type dual: :class:`TBS.lattice.Lattice`
        """
        Observable.__init__(self)
        Graph.__init__(self, directed=True)
        if dual is None:
            self.dual_lattice = Lattice(dual=self)
        else:
            self.dual_lattice = dual
        self.attach(self.dual_lattice)

        self._neighborhood = {}
        for x in vertices:
            self._neighborhood[x] = {}
        if edges:
            self.update(edges)

    @classmethod
    def random_dismantlable_lattice(cls, n_vertices):
        """Alternative constructor to create a random dismantlable lattice.

        :param n_vertices: the number of vertices (excluding bottom and top)
        :type n_vertices: int
        :return: a random dismantlable lattice with n_vertices vertices
        """
        crown_free = cls()
        bottom = "BOTTOM"
        top = "TOP"
        crown_free.update([(bottom, top)])

        all_elements = [bottom]
        for current_element in range(n_vertices):
            u = random.sample(all_elements, 1)[0]
            v = random.sample(crown_free.sup_filter(u) - {u}, 1)[0]
            crown_free.update([(u, current_element), (current_element, v)])
            all_elements.append(current_element)

        for u, v in crown_free.edges():
            crown_free.update([(u, v)])
            if not crown_free.path(u, v):
                crown_free.update([(u, v)])
        return crown_free

    @classmethod
    def from_dlo_matrix(cls, matrix, bottom="BOTTOM", top="TOP"):
        """ Lattice.

        Vertices are the boxes (see :func:`boxes`).

        :param matrix: doubly lexically ordered and Gamma free 0/1 matrix
        :param bottom: bottom element
        :param top: top element
        :return: :class:`Graph` associated lattice.
        """

        box_lattice = cls()

        cluster_correspondence = ClusterLineFromMatrix.boxes(matrix)

        last_line = last_line_not_0_for_matrix(matrix)
        last_clusters = [None] * len(matrix[0])
        line_iterator = ClusterLineFromMatrix(matrix)

        for i, current_line in enumerate(line_iterator):
            for j, elem in enumerate(current_line):
                if elem is None:
                    continue

            j = len(current_line) - 1
            while j >= 0:
                if current_line[j] is None or current_line[j] in box_lattice:
                    j -= 1
                    continue

                current_cluster = current_line[j]
                # connect to bottom
                if i == last_line[j]:
                    box_lattice.update([(bottom, cluster_correspondence[current_cluster])])

                # successor in line
                right_successor = True
                j_next = j + 1
                while j_next < len(current_line) and current_line[j_next] is None:
                    j_next += 1

                if j_next == len(current_line):
                    right_successor = False
                if i > 0 and line_iterator.previous_line[j] is not None:
                    if j_next == len(current_line) or current_line[j_next] == line_iterator.previous_line[j_next]:
                        right_successor = False
                if right_successor:
                    box_lattice.update([(cluster_correspondence[current_cluster],
                                         cluster_correspondence[current_line[j_next]])])

                # successor before line
                while j >= 0 and current_line[j] == current_cluster:
                    if last_clusters[j] is not None and last_clusters[j] != current_cluster:
                        box_lattice.update([(cluster_correspondence[current_cluster],
                                             cluster_correspondence[last_clusters[j]])])
                        successor = last_clusters[j]
                        while j >= 0 and last_clusters[j] == successor:
                            j -= 1
                    else:
                        break

                while j >= 0 and current_line[j] == current_cluster:
                    j -= 1

            last_clusters = [new_cluster or old_cluster for new_cluster, old_cluster in
                             zip(current_line, last_clusters)]

        for vertex in set(x for x in box_lattice if box_lattice.degree(x) == 0):
            box_lattice.update([(vertex, top)])

        return box_lattice

    def update(self, edges=tuple(), node_creation=True, delete=True):
        """Add/remove edges and keep dual object up to date.

        Each edge in *edges* is either added or removed depending if it
        already present or not.

        :param edges: Each edge is a pair `(x, y)`
        :type edges: iterable

        :param node_creation: If :const:`False`, edges connecting vertices
                             not in the graph are discarded.
                             If :const:`True`, missing vertices are added
                             before adding the edge.
        :type node_creation:  :class:`bool`

        :param delete: If :const:`False` edges already present are not
                       deleted from the graph.
        :type delete: :class:`bool`

        :raises: :exc:`ValueError` if the two vertices of an edge are equal.
        """
        Graph.update(self, edges, node_creation=True, delete=True)
        self.notify(edges)

    def dual_update(self, edges):
        """Add/remove edges in dual lattice.

        :param edges: Each edge is a pair `(x, y)`
        :type edges: iterable
        """
        Graph.update(self, ((y, x) for (x, y) in edges))

    def remove(self, x):
        """Remove vertex in lattice

        :param x: name of the vertex to remove
        """
        Graph.remove(self, x)
        Graph.remove(self.dual_lattice, x)

    def get_top(self):
        """Return the largest element.

        :rtype: an element of the lattice.
        """
        for x in self:
            if not self[x]:
                return x

        return None

    def get_bottom(self):
        """Return the smallest element.

        :rtype: an element of the lattice.
        """

        return self.dual_lattice.get_top()

    def get_order(self):
        """Return the order associated with the lattice.

        :rtype: TBS.graph.Graph :class:`TBS.graph.Graph`
        """

        bottom = self.get_bottom()

        dual_order = Graph([bottom], directed=True)
        for vertex in self.topological_sort(bottom):
            for cover in self.dual_lattice[vertex]:
                dual_order.update([(vertex, cover)])
                dual_order.update([(vertex, y) for y in dual_order[cover]], delete=False)
        return dual_order.dual()

    def comparability_function(self):
        """Return a comparability function associated with the lattice.

        The return function takes two parameters and returns True if the first parameter is smaller than the second one
        for the given lattice.
        This function computes the lattice order (long). Should only be used for generic lattices where no other solution
        is available.

        :rtype: function
        """
        lattice_order = self.get_order()

        def smaller_than(smaller, larger):
            """Comparability function.

            :param smaller: lattice element.
            :param larger: lattice element.

            :rtype: bool :class:`bool`
            """

            return larger in lattice_order[smaller]

        return smaller_than

    def inf_irreducible(self):
        """ Inf-irreductibles elements of the lattice.

        :return: the inf-irreducibles elements of the lattice
        :rtype: :class:`frozenset`.
        """
        irreducible = set()
        for vertex in self:
            if len(self[vertex]) == 1:
                irreducible.add(vertex)

        return frozenset(irreducible)

    def sup_irreducible(self):
        """ Sup-irreductibles elements of the lattice.

        :return: the sup-irreducibles elements of the lattice
        :rtype: :class:`frozenset`.
        """

        return self.dual_lattice.inf_irreducible()

    def sup_irreducible_clusters(self):
        """ Sup-irreducibles correspondance.

        :return: a dict associating each element to the sup-irreducible elements smaller than him.
        :rtype: :class:`dict`.
        """

        bottom = self.get_bottom()

        correspondance = {bottom: set()}

        for vertex in self.topological_sort(bottom):
            if vertex not in correspondance:
                correspondance[vertex] = set()
            if self.dual_lattice.isa_leaf(vertex):
                # sup_irreducible
                correspondance[vertex].add(vertex)
            for cover in self.dual_lattice[vertex]:
                correspondance[vertex].update(correspondance[cover])

        return {element: frozenset(sups) for element, sups in correspondance.items()}

    def inf_irreducible_clusters(self):
        """ Inf-irrerducibles correspondance.

        :return: a dict associating each element to the inf-irreducible elements smaller than him.
        :rtype: :class:`dict`.
        """

        return self.dual_lattice.sup_irreducible_clusters()

    def sup_filter(self, element):
        """Return {y | y >= element}

        :param element: vertex of the lattice
        :type element: a vertex
        :rtype: :class:`frozenset`
        """

        element_filter = set()
        self.dfs(element, lambda vertex: element_filter.add(vertex))

        return frozenset(element_filter)

    def is_a_lattice(self):
        """Is the graph possible_lattice a lattice.

        :rtype: :class:`bool`
        """

        elements = list(self)

        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                x = elements[i]
                y = elements[j]
                for graph in (self, self.dual_lattice):
                    filter_x = graph.sup_filter(x)
                    filter_y = graph.sup_filter(y)
                    unique_generator = False
                    intersection = filter_x.intersection(filter_y)
                    for possible_generator in intersection:
                        if graph.sup_filter(possible_generator) == intersection:
                            unique_generator = True
                            break
                    if not unique_generator:
                        return False
        return True

    def delete_join_irreducible(self, join_irreducible):
        """Delete a join irreducible element from lattice.

        :param join_irreducible: a join irreducible element from the lattice.
        """
        v = self[join_irreducible][0]
        u = None
        for u in self:
            if join_irreducible in self[u]:
                break

        self.remove(join_irreducible)
        if not self.path(u, v):
            self.update([(u, v)])

    def compute_height(self):
        """Index for vertices.

        if u covers v then index[u] < index[v]
        index[bottom] = 0 and for any u covering bottom index[u] = 1.

        :rtype: :class:`dict`
        """

        bottom = self.get_bottom()

        number_remaining_predecessors = {}
        for u, v in self.edges():
            number_remaining_predecessors[v] = number_remaining_predecessors.get(v, 0) + 1

        height = {bottom: 0}

        fifo = collections.deque((bottom,))
        while fifo:
            vertex = fifo.pop()
            for neighbor in self[vertex]:
                number_remaining_predecessors[neighbor] -= 1
                if not number_remaining_predecessors[neighbor]:
                    height[neighbor] = height[vertex] + 1
                    fifo.appendleft(neighbor)

        return height

    def sup(self, element, other_element):
        """Computes the sup of two elements

        :param element: a vertex of the lattice
        :param other_element: another vertex of the lattice
        :return: the element which is the sup of element and other_element
        """
        element_sup = self.sup_filter(element)
        other_element_sup = self.sup_filter(other_element)
        intersection_sup = element_sup.intersection(other_element_sup)
        for element in intersection_sup:
            if not frozenset(self.dual_lattice[element]).intersection(intersection_sup):
                return element

    def inf(self, element, other_element):
        """Computes the inf of two elements

        :param element: a vertex of the lattice
        :param other_element: another vertex of the lattice
        :return: the element which is the inf of element and other_element
        """
        return self.dual_lattice.sup(element, other_element)

    def atoms(self):
        """Returns atoms of the lattice

        :return: set of vertices
        """
        bottom = self.get_bottom()
        return set(self[bottom])

    def is_binary(self):
        """Checks whether the lattice is binary or not i.e if every vertex except the bottom covers maximum two elements
         and is covered by maximum two elements

        :return: True if the lattice is binary, False if not
        :rtype: :class:`bool`
        """
        bottom = self.get_bottom()
        for element in self:
            if element != bottom:
                if len(self[element]) > 2 or len(self.dual_lattice[element]) > 2:
                    return False
        return True

    def element_is_binary(self, element):
        return len(self[element]) <= 2 and len(self.dual_lattice[element]) <= 2

    def bottom_up_element_binarization(self, element):
        """Binarize an element covered by more than two elements

        :param element: a non binary vertex of the lattice
        """
        classes = self.inf_irreducible_clusters()
        while not len(self[element]) <= 2:
            antichain_indices = self[element]
            antichain = [classes[antichain_element] for antichain_element in antichain_indices]
            first_element_in_antichain, second_element_in_antichain = max_intersection(antichain)
            first_element, second_element = antichain_indices[first_element_in_antichain], antichain_indices[
                second_element_in_antichain]
            union_index = len(self) - 1
            classes[union_index] = classes[first_element].union(classes[second_element]).union({union_index})
            edges_to_add = ((union_index, first_element), (union_index, second_element), (element, union_index))
            edges_to_remove = ((element, first_element), (element, second_element))
            self.update(edges_to_add + edges_to_remove)

    def binarize_element(self, element):
        """Binarize an element in both direction

        :param element: an vertex of the lattice to binarize
        """
        self.bottom_up_element_binarization(element)
        self.dual_lattice.bottom_up_element_binarization(element)

    def binarize_bottom_up(self, ignored_elements={'BOTTOM'}):
        """Modifies the lattice such that no element is covered by more than two elements.

        :param ignored_elements: elements not to binarize
        :type ignored_elements: iterable
        """
        import collections

        bottom = self.get_bottom()

        fifo = collections.deque((bottom,))
        is_seen = {bottom}

        while fifo:
            vertex = fifo.pop()
            if len(self[vertex]) > 2 and vertex not in ignored_elements:
                self.binarize_element(vertex)
            visit_list = self[vertex]
            for neighbor in visit_list:
                if neighbor not in is_seen:
                    is_seen.add(neighbor)
                    fifo.appendleft(neighbor)

    def binarize_top_down(self, ignored_elements=set()):
        """Modifies the lattice such that no element covers more than two elements.

        :param ignored_elements: elements not to binarize
        :type ignored_elements: iterable
        """
        self.dual_lattice.binarize_bottom_up(ignored_elements=ignored_elements)

    def binarize(self, ignored_elements={'BOTTOM'}):
        """Modifies the lattice such that it is binary

        :param ignored_elements: elements not to binarize
        """
        self.binarize_bottom_up(ignored_elements=ignored_elements)
        self.binarize_top_down(ignored_elements=ignored_elements)

    def make_atomistic(self):
        """Makes the lattice atomistic i.e all objects are atoms.
        """
        sup_irr = self.sup_irreducible()
        bottom = self.get_bottom()
        atoms = self.atoms()
        current_element_index = len(self) - 1
        for sup in sup_irr:
            if sup not in atoms:
                self.update(((bottom, current_element_index), (current_element_index, sup)))
                current_element_index += 1

    def is_atomistic(self):
        """Check whether the lattice is atomistic or not

        :rtype: :class:`bool`
        """
        return self.atoms() == self.sup_irreducible()

    def other_successor(self, element, first_successor):
        successors = self[element]
        if len(successors) != 2:
            raise ValueError("element is not binary in lattice")
        elif successors[0] == first_successor:
            return successors[1]
        elif successors[1] == first_successor:
            return successors[0]
        else:
            raise ValueError("first_successor is not a successor of element in lattice")

    def contraction_order(self):
        """Computes a compatible contraction order.

        :return: ordered list of all the vertices
        :rtype: list
        """
        if not self.is_atomistic():
            self.make_atomistic()
        objects = self.atoms()
        predecessors_exist = set()
        take_after = set()
        arrow_head = set()
        arrows = {}
        order = []
        is_built = objects.copy()
        for element in objects:
            for successor in self[element]:
                if self.dual_lattice.other_successor(successor, element) in objects:
                    predecessors_exist.add(successor)
        while len(predecessors_exist) > 0:
            chosen_candidate = random.sample(predecessors_exist - take_after, 1)[0]
            predecessors_exist.remove(chosen_candidate)
            is_built.add(chosen_candidate)
            order.append(chosen_candidate)
            arrows[chosen_candidate] = []
            for predecessor in self.dual_lattice[chosen_candidate]:
                if len(self[predecessor]) == 2:
                    other_succ = self.other_successor(predecessor, chosen_candidate)
                    if other_succ not in is_built:
                        arrow_head.add(chosen_candidate)
                        arrows[chosen_candidate].append(predecessor)
                    else:
                        arrows[other_succ].remove(predecessor)
                        if len(arrows[other_succ]) == 0:
                            arrow_head.remove(other_succ)
                            for successor in self[other_succ]:
                                if self.dual_lattice.other_successor(successor, other_succ) not in arrow_head:
                                    take_after.discard(successor)
            for successor in self[chosen_candidate]:
                if self.dual_lattice.other_successor(successor, chosen_candidate) in is_built:
                    predecessors_exist.add(successor)
                    for other_succ_pred in self.dual_lattice[successor]:
                        if other_succ_pred in arrow_head:
                            take_after.add(successor)
        return order

    def support_tree(self):
        """Builds a support tree of an atomistic lattice.

        :return: a support tree
        :rtype: :class:`TBS.graph.Graph`
        """
        bottom = self.get_bottom()
        class_order = self.topological_sort(bottom)
        objects = self.atoms()
        representatives = {element: element for element in objects}
        classes = {element: {element} for element in objects}
        tree = Graph(vertices=tuple(frozenset({o}) for o in objects), directed=False)
        n_connected_parts = len(objects)
        colors = {object: i for i, object in enumerate(objects)}
        next(class_order)
        while n_connected_parts > 1:
            current_class_index = next(class_order)
            if current_class_index not in objects:
                predecessors = self.dual_lattice[current_class_index]
                first_class_representative = representatives[predecessors[0]]
                second_class_representative = representatives[predecessors[1]]
                representatives[current_class_index] = random.choice(
                    [first_class_representative, second_class_representative])
                if colors[first_class_representative] != colors[second_class_representative]:
                    tree.update(((frozenset({first_class_representative}), frozenset({second_class_representative})),))
                    color_to_change = colors[second_class_representative]
                    color_to_keep = colors[first_class_representative]
                    for element in colors:
                        if colors[element] == color_to_change:
                            colors[element] = color_to_keep
                    n_connected_parts -= 1
                classes[current_class_index] = classes[predecessors[0]].union(classes[predecessors[1]])
        return tree

    def contract_tree_edge(self, tree, class_to_create, already_created):
        dual = self.dual_lattice
        already_created.add(class_to_create)
        tree.update(((dual[class_to_create][0], dual[class_to_create][1]),))
        edges_to_update = tuple(())
        tree.add(class_to_create)
        for predecessor in dual[class_to_create]:
            if len(self[predecessor]) == 1:
                for neighbor in tree[predecessor]:
                    edges_to_update += ((neighbor, class_to_create),)
                tree.remove(predecessor)
            elif len(self[predecessor]) == 2:
                if self[predecessor][0] == class_to_create:
                    other_succ = self[predecessor][1]
                elif self[predecessor][1] == class_to_create:
                    other_succ = self[predecessor][0]
                else:
                    raise ValueError("Lattice is not binary")
                if other_succ not in already_created:
                    edges_to_update += ((predecessor, class_to_create),)
                    for neighbor in tree[predecessor]:
                        if self.sup_filter(neighbor).intersection(
                                self.sup_filter(predecessor)) <= self.sup_filter(class_to_create):
                            edges_to_update += ((neighbor, predecessor), (neighbor, class_to_create))
                else:
                    for neighbor in tree[predecessor]:
                        edges_to_update += ((neighbor, class_to_create),)
                    tree.remove(predecessor)
            else:
                raise ValueError("Lattice is not binary")
        tree.update(edges_to_update)
        return tree

    def contraction_trees(self, order=None):
        """Returns a family of trees creating all the vertices of the lattice.

        :param order: an order to create vertices
        :type order: iterable
        :return: a list of trees creating all vertices
        :rtype: list
        """
        tree = self.support_tree()
        if not order:
            order = iter(self.contraction_order())
        trees = [tree.copy()]
        already_created = set()
        for vertex in order:
            tree = self.contract_tree_edge(tree, vertex, already_created)
            trees.append(tree.copy())
        return trees

    def draw_binarisation_trees(self, order=None, show=True, save=None):
        if not order:
            order = self.contraction_order()
        trees = self.contraction_trees(order)
        directory = save
        if save:
            save = directory + "0"
        radial_draw_tree(trees[0], self, highlighted_edge={tuple(self.dual_lattice[order[0]])}, show=show, save=save)
        for i in range(1, len(trees) - 1):
            if save:
                save = directory + str(i)
            radial_draw_tree(trees[i], self, highlighted_edge={tuple(self.dual_lattice[order[i]])},
                             highlighted_node={order[i - 1]},
                             show=show, save=save)
        if save:
            save = directory + str(len(trees) - 1)
        radial_draw_tree(trees[-1], self, highlighted_node={order[-1]}, show=show, save=save)

    def hierarchical_height(self):
        """ Decompose the lattice into hierarchy.

        Every dismantable lattice can be decomposed into hierarchy.

        :return: A :class:`dict` whose key are the hierarchical level (0 is the first hierarchy) and value the
                 associated element of the lattice.


        """
        vertex_height = dict()
        current_height = 0
        next_neighbor = dict()
        current_degree = {x: self.degree(x) for x in self}
        sup_irreducibles = set(self.sup_irreducible())
        dual_lattice = self.dual()
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
                    vertex = next_neighbor.get(vertex, self[vertex][0])
                if is_hierarchical:
                    deleted_sup_irreducibles.add(current_sup_irreducible)
                    current_chains.update(possible_chain)

            for x in current_chains:
                vertex_height[x] = current_height
                for y in dual_lattice[x]:
                    current_degree[y] -= 1
                    if current_degree[y] == 1:
                        for z in self[y]:
                            if z not in vertex_height:
                                next_neighbor[y] = z
                                break
            current_height += 1

            sup_irreducibles.difference_update(deleted_sup_irreducibles)
            vertex_height[self.get_bottom()] = max(vertex_height.values()) + 1
        return vertex_height

    def draw(self):
        formal_context_lattice = self.to_box_lattice()
        matrix = ContextMatrix.from_lattice(formal_context_lattice).matrix
        point_transformation = point_transformation_square(len(matrix))
        representant = {box: box[0] for box in formal_context_lattice if box not in ("BOTTOM", "TOP")}
        representant[self.get_bottom()] = (len(matrix), 0)
        representant[self.get_top()] = (0, len(matrix))
        objects = formal_context_lattice.sup_irreducible()
        attributes = formal_context_lattice.inf_irreducible()
        hierarchy_association = formal_context_lattice.hierarchical_height()

        for elem in formal_context_lattice:
            x, y = point_transformation(*representant[elem])
            if elem in objects:
                type = "^"
            elif elem in attributes:
                type = "v"
            else:
                type = "o"
            if elem in objects and elem in attributes:
                type = "d"
            pyplot.scatter(x, y, marker=type, zorder=1, color=formal_context_lattice.edge_color(elem, elem),
                           edgecolors='black')

            for neighbor in formal_context_lattice[elem]:
                x2, y2 = point_transformation(*representant[neighbor])
                color = formal_context_lattice.edge_color(elem, neighbor)
                if hierarchy_association[elem] != hierarchy_association[neighbor]:
                    type = ":"
                else:
                    type = "-"
                pyplot.plot([x, x2], [y, y2], color=color, zorder=0, linestyle=type)
        pyplot.show()

    def edge_color(self, vertex1, vertex2=None):
        hierarchy_association = self.hierarchical_height()
        number_hierarchies = max(hierarchy_association.values()) + 1
        colors = matplotlib.cm.rainbow([0. + 1.0 * x / (number_hierarchies - 1) for x in range(number_hierarchies)])
        if vertex2 is None:
            vertex2 = vertex1

        return colors[max(hierarchy_association[vertex1], hierarchy_association[vertex2])]

    def print_boxes(self):
        context_matrix = ContextMatrix.from_lattice(self)
        context_matrix.reorder_doubly_lexical_order()
        lattice = self.to_box_lattice()
        boxes = self.boxes()

        return BoxesToString(boxes.values(),
                             context_matrix.elements, context_matrix.attributes,
                             {value: context_matrix.attributes[value[0][1]] for value in
                              boxes.values()},
                             lattice).run()

    def boxes(self):
        """ Boxes and cluster number correspondence.

        A box is a couple ((l1, c1), (l2, c2)) where (l1, c1) is the top left corner (line, column) of the box and
        (l2, c2) the bottom right corner.

        :param matrix: doubly lexically ordered and Gamma free 0/1 matrix
        :return: :class:`dict` with key= class number and value= the associated box
        """
        context_matrix = ContextMatrix.from_lattice(self).reorder_doubly_lexical_order()
        matrix = context_matrix.matrix
        cluster_correspondence = dict()

        for i, line in enumerate(ClusterLineFromMatrix(matrix)):
            for j, elem in enumerate(line):
                if elem is None:
                    continue
                if elem not in cluster_correspondence:
                    cluster_correspondence[elem] = ((i, j), (i, j))
                else:
                    begin, end = cluster_correspondence[elem]
                    cluster_correspondence[elem] = (begin, (i, j))

        return cluster_correspondence

    def to_box_lattice(self):
        context_matrix = ContextMatrix.from_lattice(self)
        context_matrix.reorder_doubly_lexical_order()
        box_lattice = Lattice()
        bottom = self.get_bottom()
        top = self.get_top()
        context_matrix = context_matrix.matrix
        cluster_correspondence = ClusterLineFromMatrix.boxes(context_matrix)

        last_line = last_line_not_0_for_matrix(context_matrix)
        last_clusters = [None] * len(context_matrix[0])
        line_iterator = ClusterLineFromMatrix(context_matrix)

        for i, current_line in enumerate(line_iterator):
            for j, elem in enumerate(current_line):
                if elem is None:
                    continue

            j = len(current_line) - 1
            while j >= 0:
                if current_line[j] is None or current_line[j] in box_lattice:
                    j -= 1
                    continue

                current_cluster = current_line[j]
                # connect to bottom
                if i == last_line[j]:
                    box_lattice.update([(bottom, cluster_correspondence[current_cluster])])

                # successor in line
                right_successor = True
                j_next = j + 1
                while j_next < len(current_line) and current_line[j_next] is None:
                    j_next += 1

                if j_next == len(current_line):
                    right_successor = False
                if i > 0 and line_iterator.previous_line[j] is not None:
                    if j_next == len(current_line) or current_line[j_next] == line_iterator.previous_line[j_next]:
                        right_successor = False
                if right_successor:
                    box_lattice.update([(cluster_correspondence[current_cluster],
                                         cluster_correspondence[current_line[j_next]])])

                # successor before line
                while j >= 0 and current_line[j] == current_cluster:
                    if last_clusters[j] is not None and last_clusters[j] != current_cluster:
                        box_lattice.update([(cluster_correspondence[current_cluster],
                                             cluster_correspondence[last_clusters[j]])])
                        successor = last_clusters[j]
                        while j >= 0 and last_clusters[j] == successor:
                            j -= 1
                    else:
                        break

                while j >= 0 and current_line[j] == current_cluster:
                    j -= 1

            last_clusters = [new_cluster or old_cluster for new_cluster, old_cluster in
                             zip(current_line, last_clusters)]

        for vertex in set(x for x in box_lattice if box_lattice.degree(x) == 0):
            box_lattice.update([(vertex, top)])

        return box_lattice


def max_intersection(antichain):
    n_elements = len(antichain)
    indices_map = [i for i in range(n_elements)]
    random.shuffle(indices_map)
    i, j = 0, 1
    first_element, second_element = antichain[indices_map[i]], antichain[indices_map[j]]
    current_max = first_element.intersection(second_element)
    k = 2
    while k < n_elements:
        if current_max < first_element.intersection(antichain[indices_map[k]]):
            j = k
            second_element = antichain[indices_map[j]]
            current_max = first_element.intersection(second_element)
        elif current_max < second_element.intersection(antichain[indices_map[k]]):
            i = k
            first_element = antichain[indices_map[i]]
            current_max = first_element.intersection(second_element)
        k += 1
    return indices_map[i], indices_map[j]


def point_transformation_square(max_y):
    return lambda line, column: (column, max_y - line)


def last_line_not_0_for_matrix(matrix):
    last_line = [-1] * len(matrix[0])
    for j in range(len(matrix[0])):
        for i in range(len(matrix) - 1, -1, -1):
            if matrix[i][j] == 1:
                last_line[j] = i
                break
    return last_line
