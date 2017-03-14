from TBS.lattice import get_bottom, dual_lattice, inf_irreducible_clusters, sup_irreducible
from TBS.graph import Graph
import random


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


def flat_contraction_order(flat_lattice):
    dual = dual_lattice(flat_lattice)
    bottom = get_bottom(flat_lattice)
    candidates = set(flat_lattice[bottom])
    contraction_order = []
    is_seen = set()
    while len(candidates) > 0:
        chosen_candidate = random.sample(candidates, 1)[0]
        candidates.remove(chosen_candidate)
        contraction_order.append(chosen_candidate)
        for successor in flat_lattice[chosen_candidate]:
            if successor not in is_seen:
                is_seen.add(chosen_candidate)
                predecessors = dual[successor]
                if len(predecessors) == 1:
                    candidates.add(successor)
                else:
                    if predecessors[0] == chosen_candidate and predecessors[1] in contraction_order \
                            or predecessors[1] == chosen_candidate and predecessors[0] in contraction_order:
                        candidates.add(successor)
    return contraction_order


def is_flat(lattice, bottom=None):
    objects = sup_irreducible(lattice)
    lattice_atoms = atoms(lattice, bottom)
    for object in objects:
        if object not in lattice_atoms:
            return False
    return True


def contraction_order(lattice):
    if not is_flat(lattice):
        lattice = move_sup_irreducibles_to_atoms(lattice)
    if not is_binary(lattice):
        lattice = binarize(lattice, ignored_elements={get_bottom(lattice)})
    return flat_contraction_order(lattice)


def support_tree(lattice, bottom=None):
    if not bottom:
        bottom = get_bottom(lattice)
    dual = dual_lattice(lattice)
    class_order = lattice.topological_sort(bottom)
    objects = atoms(lattice, bottom)
    classes = {object: {object} for object in objects}
    tree = Graph(vertices=tuple(objects), directed=False)
    n_connected_parts = len(objects)
    next(class_order)  # jumps bottom
    while n_connected_parts > 1:
        current_class_index = next(class_order)
        if current_class_index not in objects:
            predecessors = dual[current_class_index]
            if classes[predecessors[0]].intersection(classes[predecessors[1]]) == set():
                tree.update(tuple(
                    [(random.sample(classes[predecessors[0]], 1)[0], (random.sample(classes[predecessors[1]], 1)[0]))]))
                n_connected_parts -= 1
            classes[current_class_index] = classes[predecessors[0]].union(classes[predecessors[1]])
    return tree
