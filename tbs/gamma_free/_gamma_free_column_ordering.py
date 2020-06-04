from ..graph import DirectedGraph, topological_sort


def gamma_free_column_order(context_matrix):
    """ column Gamma free ordering

    The lines of the matrix should be strongly chordally ordered.

    :param context_matrix: ContextMatrix
    :return: new column ordering
    """

    column_index_order = topological_sort(_column_intersection_graphs(context_matrix.matrix),
                                          lambda key: key)

    return _order_refinement(context_matrix.matrix, column_index_order)


def _order_refinement(matrix, initial_column_order):
    matrix_number_1_under = matrix_count_number_1_under(matrix)

    def matrix_elem(line, column):
        return matrix[line][initial_column_order[column]]

    def matrix_count(line, column):
        return matrix_number_1_under[line][initial_column_order[column]]

    position = [-1] * len(initial_column_order)
    next_1 = [len(initial_column_order) - 1] * len(matrix)

    for l in range(len(next_1)):
        while next_1[l] >= 0 and (not matrix_elem(l, next_1[l]) or position[next_1[l]] >= 0):
            next_1[l] -= 1

    current_index = next_1[0]
    for l in range(len(next_1)):
        current_index = max(current_index, next_1[l])

    if current_index != -1:
        position[current_index] = len(position) - 1
    else:
        position[-1] = len(position) - 1

    while current_index >= 0:

        for l in range(len(next_1)):
            while next_1[l] >= 0 and (not matrix_elem(l, next_1[l]) or position[next_1[l]] >= 0):
                next_1[l] -= 1

        next_index = next_1[0]
        for l in range(len(next_1)):
            next_index = max(next_index, next_1[l])

            if matrix_elem(l, current_index) and matrix_count(l, next_1[l]) == matrix_count(l, current_index):
                next_index = next_1[l]
                break

        if next_index >= 0:
            position[next_index] = position[current_index] - 1

        current_index = next_index

    pos = min([x == -1 and (len(position) - 1) or x for x in position]) - 1
    for i in range(len(position) - 1, -1, -1):
        if position[i] == -1:
            position[i] = pos
            pos -= 1

    new_order = [-1] * len(position)
    for i in range(len(position)):
        new_order[position[i]] = initial_column_order[i]

    return new_order


def _column_intersection_graphs(matrix):
    """ directed acyclyc graph associated with the columns indices.



    :param matrix: the lines of the matrix should be strongly chordally ordered.
    :return: DirectedGraph
    """

    nb_lines = len(matrix)
    nb_columns = len((matrix[0]))

    edges_inclusion = []

    for c1 in range(nb_columns):
        for c2 in range(c1 + 1, nb_columns):
            first_line_both_true = 0
            for first_line_both_true in range(nb_lines):
                if matrix[first_line_both_true][c1] and matrix[first_line_both_true][c2]:
                    break

            if not matrix[first_line_both_true][c1] or not matrix[first_line_both_true][c2]:
                continue

            i_not_j = j_not_i = False

            for l in range(first_line_both_true, nb_lines):
                if matrix[l][c1] and not matrix[l][c2]:
                    i_not_j = True
                elif not matrix[l][c1] and matrix[l][c2]:
                    j_not_i = True

            if i_not_j and not j_not_i:
                edges_inclusion.append((c2, c1))

            elif j_not_i and not i_not_j:
                edges_inclusion.append((c1, c2))

    return DirectedGraph(range(nb_columns), edges_inclusion)


def matrix_count_number_1_under(matrix):
    reverse_matrix_count = [[element and 1 or 0 for element in matrix[-1]]]

    for l in range(len(matrix) - 2, -1, -1):
        line = []
        for c in range(len(matrix[l])):
            line.append(reverse_matrix_count[-1][c] + (matrix[l][c] and 1 or 0))
        reverse_matrix_count.append(line)

    reverse_matrix_count.reverse()
    return reverse_matrix_count
