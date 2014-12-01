# -*- coding: utf-8 -*-

import sys


def number_of_non_pointed_ultrametric_triangle(matrix):
    """Number of non-ultrametric triangle for delta_diss elements.

    :param delta_diss: delta dissimilarity
    :type delta_diss: :class:`CTK.diss.Diss`

    Return a dict where keys are delta_diss elements and value the number of
    non ultrametric triangle for this element.

    :rtype: :class:`dict`
    """
    number = dict([(x, 0) for x in range(len(matrix))])
    base_set = list(range(len(matrix)))
    number_of_elements = len(base_set)

    for x_index in range(number_of_elements):
        print(x_index, number_of_elements)
        x = x_index
        # noinspection PyArgumentList
        for y_index in range(x_index + 1, number_of_elements):
            y = base_set[y_index]
            # noinspection PyArgumentList
            for z_index in range(y_index + 1, number_of_elements):
                z = base_set[z_index]
                update_number_of_non_pointed_ultrametric_triangle_for_triplet(x, y, z, number, matrix)

    return number


def update_number_of_non_pointed_ultrametric_triangle_for_triplet(x, y, z, number, matrix):
    """
    :param x: element of delta_diss
    :param y: element of delta_diss
    :param z: element of delta_diss

    :param number: actual number of non-ultrametric triangles.
    :type number: :class:`dict`

    :param delta_diss: delta dissimilarity
    :type delta_diss: :class:`CTK.diss.Diss`
    """
    if is_non_pointed_ultrametric_triangle(x, y, z, matrix):
        number[x] += 1
    if is_non_pointed_ultrametric_triangle(y, x, z, matrix):
        number[y] += 1
    if is_non_pointed_ultrametric_triangle(z, x, y, matrix):
        number[z] += 1


def is_non_pointed_ultrametric_triangle(x, y_1, y_2, matrix):
    """delta_diss(x, y_1) and delta_diss(x, y_2) properly intersect on x.

    :param x: element of delta_diss
    :param y_1: element of delta_diss
    :param y_2: element of delta_diss

    :param delta_diss: delta dissimilarity
    :type delta_diss: :class:`CTK.diss.Diss`

    :rtype: :class:`bool`
    """
    x_y1_without_y2 = False
    x_y2_without_y1 = False
    for j in range(len(matrix[x])):
        if matrix[x][j] == 1 and matrix[y_1][j] == 1 and matrix[y_2][j] == 0:
            x_y1_without_y2 = True
        if matrix[x][j] == 1 and matrix[y_2][j] == 1 and matrix[y_1][j] == 0:
            x_y2_without_y1 = True
        if x_y1_without_y2 == x_y2_without_y1 == True:
            return True

    return False


def update_number_of_non_pointed_ultrametric_triangle(delta, x, matrix, current_set):
    """Update number of non ultrametric triangle when x is no more in X.

    :param delta: actual number of non-ultrametric triangles.
    :type delta: :class:`dict`

    :param x: removed element.
    :param delta_diss: delta dissimilarity
    :type delta_diss: :class:`CTK.diss.Diss`

    :param current_set: base set. x must not be in X.
    :type current_set: iterable.
    """
    current_list = list(current_set)

    for yl in range(len(current_list)):
        y = current_list[yl]
        # noinspection PyArgumentList
        for zl in range(yl + 1, len(current_list)):
            z = current_list[zl]
            if is_non_pointed_ultrametric_triangle(y, x, z, matrix):
                delta[y] -= 1
            if is_non_pointed_ultrametric_triangle(z, x, y, matrix):
                delta[z] -= 1


def elimination_order_matrix(matrix, last_elem=None):
    """Elimination order delta dissimilarity.

    If *delta_diss* is a parsimonious delta dissimilarity, returns a leaf order. If not,
    returns a possible choice for leaf elimination.

    :param last_elem: any element can be the last. If None, one is arbitrarily chosen.

    :param delta_diss: delta dissimilarity.
    :type delta_diss: :class:`CTK.diss.Diss`

    :rtype: :class:`list`
    """

    remaining_elements = set(range(len(matrix)))
    remaining_elements_for_update = set(range(len(matrix)))
    l = len(remaining_elements)

    count = 0
    max_count = (l - 1) * l * l + l * (l - 1) * (l - 2) / 6

    number = number_of_non_pointed_ultrametric_triangle(matrix)

    if last_elem is not None:
        remaining_elements.remove(last_elem)

    order = []

    while remaining_elements:

        new_element = min([x for x in remaining_elements], key=lambda u: number[u])

        order.append(new_element)
        remaining_elements.remove(new_element)
        remaining_elements_for_update.remove(new_element)

        update_number_of_non_pointed_ultrametric_triangle(number, new_element, matrix, remaining_elements_for_update)

        count += l * l
        print(count/max_count, file=sys.stderr)

    if last_elem is not None:
        order.append(last_elem)

    return order