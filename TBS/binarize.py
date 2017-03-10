from TBS.lattice import get_bottom, dual_lattice, inf_irreducible_clusters
import random


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
