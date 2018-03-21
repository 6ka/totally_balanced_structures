NOT_AN_ELEMENT = None
NOT_INCLUDED = -1


def chordal_matrix_cover_graph_from_chordal_matrix_order(chordal_matrix_order):
    chordal_matrix_cover_graph = [[x for x in line] for line in chordal_matrix_order]
    bounds = get_bounds(chordal_matrix_order, empty=NOT_AN_ELEMENT)
    column_min_tab = [-1] * len(chordal_matrix_order)
    line_min_tab = [-1] * len(chordal_matrix_order[0])

    for line, column_min, column_max in bounds:
        column_min_tab[line] = column_min
        for c in range(column_min, column_max + 1):
            line_min_tab[c] = line

        for l in range(line, len(chordal_matrix_cover_graph)):
            for c in range(column_min, column_max + 1):
                if chordal_matrix_order[l][c] in (NOT_AN_ELEMENT, NOT_INCLUDED):
                    continue
                elif c > column_min and chordal_matrix_order[l][c - 1] == chordal_matrix_order[l][c]:
                    chordal_matrix_cover_graph[l][c] = NOT_INCLUDED
                else:
                    for l_before in range(line_min_tab[c] + 1, l):
                        if chordal_matrix_order[l_before][c] not in (NOT_AN_ELEMENT, NOT_INCLUDED):
                            pred_column = chordal_matrix_order[l_before][c] + column_min_tab[l_before]
                            if chordal_matrix_order[l][pred_column] not in (NOT_AN_ELEMENT, NOT_INCLUDED) and \
                                            chordal_matrix_order[l][pred_column] >= chordal_matrix_order[l][c]:
                                chordal_matrix_cover_graph[l][c] = NOT_INCLUDED

    return chordal_matrix_cover_graph


def chordal_matrix_order(chordal_matrix):
    order_matrix = [[x and NOT_INCLUDED or NOT_AN_ELEMENT for x in line] for line in chordal_matrix]

    bounds = get_bounds(chordal_matrix)

    for i in range(len(bounds)):
        line, column_min, column_max = bounds[i]
        for column in range(column_min, column_max + 1):
            order_matrix[line][column] = column - column_min

        for j in range(i + 1, len(bounds)):
            line_inclusion, column_min_inclusion, column_max_inclusion = bounds[j]

            column = column_min
            column_inclusion = column_min_inclusion

            while column <= column_max and column_inclusion <= column_max_inclusion:
                if is_included(line, column, column_inclusion, chordal_matrix):
                    order_matrix[line][column_inclusion] = column - column_min
                    column += 1
                else:
                    column_inclusion += 1

            for column in range(column_min_inclusion + 1, column_max_inclusion + 1):
                if order_matrix[line][column] == NOT_INCLUDED:
                    order_matrix[line][column] = order_matrix[line][column - 1]

    return order_matrix


def is_included(line, column_1, column_2, matrix):
    for l in range(line, len(matrix)):
        if matrix[l][column_1] and not matrix[l][column_2]:
            return False
    return True


def get_bounds(chordal_matrix, empty=0):
    """

    Args:
        chordal_matrix: chordally orderd matrix

    Returns:

    """
    bounds = []
    for column, line in enumerate(get_first_non_empty_lines(chordal_matrix, empty)):
        if line == -1:
            continue
        if not bounds or bounds[-1][0] != line:
            bounds.append([line, column, column])
        else:
            bounds[-1][-1] = column

    return bounds


def get_first_non_empty_lines(matrix, empty):
    first_non_empty_line = []
    for column in range(len(matrix[0])):
        not_empty_line = -1
        for line in range(len(matrix)):
            if matrix[line][column] != empty:
                not_empty_line = line
                break
        first_non_empty_line.append(not_empty_line)
    return first_non_empty_line
