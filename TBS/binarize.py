import random
from TBS.graph import Graph
from TBS.lattice import get_bottom, dual_lattice, inf_irreducible_clusters, sup_irreducible, sup_filter
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


def flat_contraction_order(flat_lattice, dual=None, bottom=None):
    if not dual:
        dual = dual_lattice(flat_lattice)
    if not bottom:
        bottom = get_bottom(flat_lattice)
    objects = atoms(flat_lattice, bottom)
    predecessors_exist = set()
    order = []
    is_built = objects.copy()
    for element in objects:
        for successor in flat_lattice[element]:
            if other_successor(dual, successor, element) in objects:
                predecessors_exist.add(successor)
    while len(predecessors_exist) > 0:
        chosen_candidate = random.sample(predecessors_exist, 1)[0]
        predecessors_exist.remove(chosen_candidate)
        order.append(chosen_candidate)
        is_built.add(chosen_candidate)
        for successor in flat_lattice[chosen_candidate]:
            if successor not in is_built:
                predecessors = dual[successor]
                if len(predecessors) == 1:
                    predecessors_exist.add(successor)
                else:
                    other_predecessor = other_successor(dual, successor, chosen_candidate)
                    if other_predecessor in is_built or other_predecessor in objects:
                        predecessors_exist.add(successor)

    order = [vertex for vertex in order if vertex not in objects]
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
                other_successor = lattice[predecessor][1]
            elif lattice[predecessor][1] == class_to_create:
                other_successor = lattice[predecessor][0]
            else:
                raise ValueError("Lattice is not binary")
            if other_successor not in already_created:
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


def contraction_trees(lattice, order=None, bottom=None):
    if not bottom:
        bottom = get_bottom(lattice)
    if not order:
        order = iter(contraction_order(lattice))
    dual = dual_lattice(lattice)
    tree = support_tree(lattice, bottom)
    trees = [tree.copy()]
    already_created = set()
    for vertex in order:
        tree = contract_edge(tree, vertex, lattice, dual, already_created)
        trees.append(tree.copy())
    return trees


def draw_binarisation_trees(lattice, bottom=None, order=None, show=True, save=None):
    if not bottom:
        bottom = get_bottom(lattice)
    if not order:
        order = contraction_order(lattice)
    dual = dual_lattice(lattice)
    trees = contraction_trees(lattice, order=order, bottom=bottom)
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
