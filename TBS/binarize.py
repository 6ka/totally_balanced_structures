from TBS.lattice import get_bottom, comparability_function, dual_lattice
import random


def atoms(lattice):
    return set(lattice[get_bottom(lattice)])


def coatoms(lattice):
    dual = dual_lattice(lattice)
    return set(dual[get_bottom(dual)])


def smaller_atoms(lattice_atoms, element, smaller_than):
    return set(atom for atom in lattice_atoms if smaller_than(atom, element))


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
    for element in lattice:
        if len(lattice[element]) > 2 or len(dual[element]) > 2:
            return False
    return True


def element_is_binary(lattice, dual, element):
    return len(lattice[element]) <= 2 and len(dual[element]) <= 2


