import random
from collections import deque

from TBS.contextmatrix import ContextMatrix
from TBS.graph import Graph
from TBS.lattice import get_bottom, dual_lattice, inf_irreducible_clusters, sup_irreducible, sup_filter, \
    sup_irreducible_clusters
from TBS.orders.doubly_lexical import doubly_lexical_order
from TBS.tree import radial_draw_tree


def atoms(lattice, bottom=None):
    if not bottom:
        bottom = get_bottom(lattice)
    return set(lattice[bottom])


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


def is_binary(lattice):
    dual = dual_lattice(lattice)
    bottom = get_bottom(lattice)
    for element in lattice:
        if element != bottom:
            if len(lattice[element]) > 2 or len(dual[element]) > 2:
                return False
    return True


def element_is_binary(lattice, element, dual=None):
    if not dual:
        dual = dual_lattice(lattice)
    return len(lattice[element]) <= 2 and len(dual[element]) <= 2


def bottom_up_element_binarization(lattice, element):
    """Binarize elements covered by more than two elements"""
    bottom_up_binarized_element_lattice = lattice.copy()
    classes = inf_irreducible_clusters(bottom_up_binarized_element_lattice)
    while not len(bottom_up_binarized_element_lattice[element]) <= 2:
        antichain_indices = bottom_up_binarized_element_lattice[element]
        antichain = [classes[antichain_element] for antichain_element in antichain_indices]
        first_element_in_antichain, second_element_in_antichain = max_intersection(antichain)
        first_element, second_element = antichain_indices[first_element_in_antichain], antichain_indices[
            second_element_in_antichain]
        union_index = len(bottom_up_binarized_element_lattice) - 1
        classes[union_index] = classes[first_element].union(classes[second_element]).union({union_index})
        edges_to_add = ((union_index, first_element), (union_index, second_element), (element, union_index))
        edges_to_remove = ((element, first_element), (element, second_element))
        bottom_up_binarized_element_lattice.update(edges_to_add + edges_to_remove)
    return bottom_up_binarized_element_lattice


def binarize_element(lattice, element):
    bottom_up_binarized_element_lattice = bottom_up_element_binarization(lattice, element)
    dual = dual_lattice(bottom_up_binarized_element_lattice)
    binarized_element_lattice = bottom_up_element_binarization(dual, element)
    return dual_lattice(binarized_element_lattice)


def bfs_binarization(lattice, binarization_condition, element_binarization, ignored_elements={'BOTTOM'}):
    import collections

    binarized_lattice = lattice.copy()
    dual_initial_lattice = dual_lattice(lattice)

    bottom = get_bottom(lattice)

    fifo = collections.deque((bottom,))
    is_seen = {bottom}

    while fifo:
        vertex = fifo.pop()
        if binarization_condition(lattice, vertex, dual_initial_lattice) and vertex not in ignored_elements:
            binarized_lattice = element_binarization(binarized_lattice, vertex)
        visit_list = lattice[vertex]
        for neighbor in visit_list:
            if neighbor not in is_seen:
                is_seen.add(neighbor)
                fifo.appendleft(neighbor)
    return binarized_lattice


def binarize_condition(lattice, vertex, dual_initial_lattice):
    return not element_is_binary(lattice, vertex, dual_initial_lattice)


def bottom_up_binarize_condition(lattice, vertex, *unused):
    return not len(lattice[vertex]) <= 2


def binarize(lattice, ignored_elements={'BOTTOM'}):
    return bfs_binarization(lattice, binarize_condition, binarize_element, ignored_elements)


def bottom_up_binarization(lattice, ignored_elements={'BOTTOM'}):
    return bfs_binarization(lattice, bottom_up_binarize_condition, bottom_up_element_binarization, ignored_elements)


def top_down_binarization(lattice):
    return dual_lattice(bottom_up_binarization(dual_lattice(lattice)))


def move_sup_irreducibles_to_atoms(lattice):
    flat_lattice = lattice.copy()
    sup_irr = sup_irreducible(flat_lattice)
    bottom = get_bottom(flat_lattice)
    atoms = flat_lattice[bottom]
    current_element_index = len(flat_lattice) - 1
    for sup in sup_irr:
        if sup not in atoms:
            flat_lattice.update(((bottom, current_element_index), (current_element_index, sup)))
            current_element_index += 1
    return flat_lattice


def lower_class_in_dlo_matrix(classes, order):
    current_candidate = None
    for candidate in classes:
        if current_candidate is None:
            current_candidate = candidate
        current_min = min(classes[current_candidate], key=lambda x: order.index(x))
        candidate_min = min(classes[candidate], key=lambda x: order.index(x))
        if order.index(candidate_min) > order.index(current_min):
            current_candidate = candidate
    return current_candidate


def flat_contraction_order(flat_lattice, dual=None, bottom=None, dlo=None):
    if not dual:
        dual = dual_lattice(flat_lattice)
    if not bottom:
        bottom = get_bottom(flat_lattice)
    objects = atoms(flat_lattice, bottom)
    classes = sup_irreducible_clusters(flat_lattice)
    predecessors_exist = set()
    take_after = set()
    arrow_head = set()
    arrows = {}
    order = []
    is_built = objects.copy()
    for element in objects:
        for successor in flat_lattice[element]:
            if other_successor(dual, successor, element) in objects:
                predecessors_exist.add(successor)
    while len(predecessors_exist) > 0:
        if dlo:
            chosen_candidate = lower_class_in_dlo_matrix(
                {element: classes[element] for element in predecessors_exist - take_after}, dlo)
        else:
            chosen_candidate = random.sample(predecessors_exist - take_after, 1)[0]
        predecessors_exist.remove(chosen_candidate)
        is_built.add(chosen_candidate)
        order.append(chosen_candidate)
        arrows[chosen_candidate] = []
        for predecessor in dual[chosen_candidate]:
            if len(flat_lattice[predecessor]) == 2:
                other_succ = other_successor(flat_lattice, predecessor, chosen_candidate)
                if other_succ not in is_built:
                    arrow_head.add(chosen_candidate)
                    arrows[chosen_candidate].append(predecessor)
                else:
                    arrows[other_succ].remove(predecessor)
                    if len(arrows[other_succ]) == 0:
                        arrow_head.remove(other_succ)
                        for successor in flat_lattice[other_succ]:
                            if other_successor(dual, successor, other_succ) not in arrow_head:
                                take_after.discard(successor)
        for successor in flat_lattice[chosen_candidate]:
            if other_successor(dual, successor, chosen_candidate) in is_built:
                predecessors_exist.add(successor)
                for other_succ_pred in dual[successor]:
                    if other_succ_pred in arrow_head:
                        take_after.add(successor)
    return order


def other_successor(lattice, element, first_successor):
    successors = lattice[element]
    if len(successors) != 2:
        raise ValueError("element is not binary in lattice")
    elif successors[0] == first_successor:
        return successors[1]
    elif successors[1] == first_successor:
        return successors[0]
    else:
        raise ValueError("first_successor is not a successor of element in lattice")


def is_flat(lattice, bottom=None):
    objects = sup_irreducible(lattice)
    lattice_atoms = atoms(lattice, bottom)
    return objects == lattice_atoms


def contraction_order(lattice):
    if not is_binary(lattice):
        lattice = binarize(lattice, ignored_elements={get_bottom(lattice)})
    if not is_flat(lattice):
        lattice = move_sup_irreducibles_to_atoms(lattice)
    return flat_contraction_order(lattice)


def support_tree(lattice, bottom=None, dual=None):
    if not bottom:
        bottom = get_bottom(lattice)
    if not dual:
        dual = dual_lattice(lattice)
    class_order = lattice.topological_sort(bottom)
    objects = atoms(lattice, bottom)
    representatives = {object: object for object in objects}
    classes = {object: {object} for object in objects}
    tree = Graph(vertices=tuple(objects), directed=False)
    n_connected_parts = len(objects)
    colors = {object: i for i, object in enumerate(objects)}
    next(class_order)
    while n_connected_parts > 1:
        current_class_index = next(class_order)
        if current_class_index not in objects:
            predecessors = dual[current_class_index]
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


def dlo_support_tree(lattice):
    matrix = ContextMatrix.from_lattice(lattice)
    row_order = doubly_lexical_order(matrix.matrix)[0]
    row_order = [matrix.elements[row_order[i]] for i in range(len(row_order))]
    tree = Graph()
    classes = sup_irreducible_clusters(lattice)
    for element in row_order[:-1]:
        neighbour = dlo_support_tree_neighbour(lattice, row_order, element, classes)
        tree.update(((element, neighbour),))
    return tree


def dlo_support_tree_neighbour(lattice, row_order, element, classes):
    found = False
    current_element = element
    current_class = element
    inferiors = {row_order[i] for i in range(row_order.index(current_element) + 1)}
    while not found:
        successor_right = successor_to_the_right_in_context_matrix(lattice, current_class, classes, row_order)
        if successor_right != -1:
            neighbour = min(classes[successor_right] - inferiors, key=lambda x: row_order.index(x))
            found = True
        else:
            current_class, current_element = just_on_top_element(lattice, current_class, current_element, row_order, classes)
    return neighbour


def dlo_contraction_order(lattice):  # returns the order from left to right and bottom to top of dlo context matrix
    matrix = ContextMatrix.from_lattice(lattice)
    row_order = doubly_lexical_order(matrix.matrix)[0]
    row_order = [matrix.elements[row_order[i]] for i in range(len(row_order))]
    classes = sup_irreducible_clusters(lattice)
    order = []
    for element in reversed(row_order[:-1]):
        right_successor = successor_to_the_right_in_context_matrix(lattice, element, classes, row_order)
        while right_successor != -1:
            order.append(right_successor)
            element = right_successor
            right_successor = successor_to_the_right_in_context_matrix(lattice, element, classes, row_order)
    return order


def successor_to_the_right_in_context_matrix(lattice, current_class, classes, row_order):
    if len(lattice[current_class]) == 0:
        return -1
    if len(lattice[current_class]) == 1:
        successor = lattice[current_class][0]
        if min(classes[successor], key=lambda x: row_order.index(x)) == min(classes[current_class],
                                                                            key=lambda x: row_order.index(x)):
            return successor
        else:
            return -1
    elif len(lattice[current_class]) == 2:
        first_successor = lattice[current_class][0]
        second_successor = lattice[current_class][1]
        if min(classes[first_successor], key=lambda x: row_order.index(x)) == min(classes[current_class],
                                                                                  key=lambda x: row_order.index(x)):
            # first successor is to the right
            return first_successor
        elif min(classes[second_successor], key=lambda x: row_order.index(x)) == min(classes[current_class],
                                                                                     key=lambda x: row_order.index(x)):
            # second successor is to the right
            return second_successor
        else:  # both successors are on top
            return -1


def just_on_top_element(lattice, current_class, current_element, row_order, classes):  # when no element to the right
    if len(lattice[current_class]) == 1:
        successor = lattice[current_class][0]
        return successor, min(classes[successor], key=lambda x: row_order.index(x))
    elif len(lattice[current_class]) == 2:
        first_successor = lattice[current_class][0]
        second_successor = lattice[current_class][1]
        previous_element = row_order[row_order.index(current_element) - 1]
        if previous_element in classes[first_successor]:
            just_on_top_element = min(classes[first_successor], key=lambda x: row_order.index(x))
        else:
            just_on_top_element = min(classes[second_successor], key=lambda x: row_order.index(x))
        if just_on_top_element in classes[first_successor]:
            current_class = first_successor
        else:
            current_class = second_successor
        current_element = just_on_top_element
        return current_class, current_element


def on_top_successors(lattice, current_class, classes, row_order):
    on_top_succ = []
    if len(lattice[current_class]) > 0:
        successors = lattice[current_class]
        class_min = min(classes[current_class], key= lambda x: row_order.index(x))
        for successor in successors:
            successor_min = min(classes[successor], key=lambda x: row_order.index(x))
            if row_order.index(successor_min )< row_order.index(class_min):
                on_top_succ.append(successor)
    return on_top_succ


def left_predecessor(dual, current_class, classes, row_order):  # parent class on the left of current_class in matrix
    if len(classes[current_class]) != 1:
        first_parent = dual[current_class][0]
        second_parent = dual[current_class][1]
        min_class_element = min(classes[current_class], key=lambda x: row_order.index(x))
        if min_class_element in classes[first_parent]:
            return first_parent
        elif min_class_element in classes[second_parent]:
            return second_parent
        else:
            raise ValueError("current_class has no left parent")
    else:
        raise ValueError("current_class is an element so it has no parent")


def on_the_top_and_left(lattice, current_class, classes, row_order):
    top_left_elements = set()
    class_queue = deque()
    class_queue.append(current_class)
    dual = dual_lattice(lattice)
    while class_queue:
        current_class = class_queue.pop()
        if len(classes[current_class]) > 1:
            left_pred = left_predecessor(dual, current_class, classes, row_order)
            top_left_elements.add(left_pred)
            class_queue.append(left_pred)
        top_succ = on_top_successors(lattice, current_class, classes, row_order)
        for succ in top_succ:
            top_left_elements.add(succ)
            class_queue.append(succ)
    return top_left_elements


def contract_edge(tree, class_to_create, lattice, dual, already_created):
    already_created.add(class_to_create)
    tree.update(((dual[class_to_create][0], dual[class_to_create][1]),))
    edges_to_update = tuple(())
    tree.add(class_to_create)
    for predecessor in dual[class_to_create]:
        if len(lattice[predecessor]) == 1:
            for neighbor in tree[predecessor]:
                edges_to_update += ((neighbor, class_to_create),)
            tree.remove(predecessor)
        elif len(lattice[predecessor]) == 2:
            if lattice[predecessor][0] == class_to_create:
                other_succ = lattice[predecessor][1]
            elif lattice[predecessor][1] == class_to_create:
                other_succ = lattice[predecessor][0]
            else:
                raise ValueError("Lattice is not binary")
            if other_succ not in already_created:
                edges_to_update += ((predecessor, class_to_create),)
                for neighbor in tree[predecessor]:
                    if sup_filter(lattice, neighbor).intersection(sup_filter(lattice, predecessor)) <= sup_filter(
                            lattice, class_to_create):
                        edges_to_update += ((neighbor, predecessor), (neighbor, class_to_create))
            else:
                for neighbor in tree[predecessor]:
                    edges_to_update += ((neighbor, class_to_create),)
                tree.remove(predecessor)
        else:
            raise ValueError("Lattice is not binary")
    tree.update(edges_to_update)
    return tree


def contraction_trees(lattice, order=None, bottom=None, dlo=False):
    if not bottom:
        bottom = get_bottom(lattice)
    if dlo:
        tree = dlo_support_tree(lattice)
        if not order:
            order = iter(dlo_contraction_order(lattice))
    else:
        tree = support_tree(lattice, bottom)
        if not order:
            order = iter(contraction_order(lattice))
    dual = dual_lattice(lattice)
    trees = [tree.copy()]
    already_created = set()
    for vertex in order:
        tree = contract_edge(tree, vertex, lattice, dual, already_created)
        trees.append(tree.copy())
    return trees


def draw_binarisation_trees(lattice, bottom=None, order=None, dlo=False, show=True, save=None):
    if not bottom:
        bottom = get_bottom(lattice)
    if not order:
        order = contraction_order(lattice)
    dual = dual_lattice(lattice)
    trees = contraction_trees(lattice, order=order, bottom=bottom, dlo=dlo)
    directory = save
    if save:
        save = directory + "0"
    radial_draw_tree(trees[0], lattice, highlighted_edge={tuple(dual[order[0]])}, show=show, save=save)
    for i in range(1, len(trees) - 1):
        if save:
            save = directory + str(i)
        radial_draw_tree(trees[i], lattice, highlighted_edge={tuple(dual[order[i]])}, highlighted_node={order[i - 1]},
                         show=show, save=save)
    if save:
        save = directory + str(len(trees) - 1)
    radial_draw_tree(trees[-1], lattice, highlighted_node={order[-1]}, show=show, save=save)


