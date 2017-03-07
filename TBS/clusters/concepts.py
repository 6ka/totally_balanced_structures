def concepts_from_dlo_gamma_free_matrix(matrix):
    return line_concept_from_dlo_gamma_free_matrix(matrix).intersection(column_concept_from_dlo_gamma_free_matrix(matrix))


def line_concept_from_dlo_gamma_free_matrix(matrix):
    line_concepts = set()
    for i in range(len(matrix)):
        new_if_true = False
        for j in range(len(matrix[i]) - 1, -1, -1):
            if matrix[i][j]:
                if i == 0 or not matrix[i - 1][j]:
                    new_if_true = True

                if new_if_true:
                    line_concepts.add((i, j))

    return line_concepts


def column_concept_from_dlo_gamma_free_matrix(matrix):
    column_concepts = set()
    for j in range(len(matrix[0])):
        new_if_true = False
        for i in range(len(matrix) - 1, -1, -1):
            if matrix[i][j]:
                if j == 0 or not matrix[i][j - 1]:
                    new_if_true = True

                if new_if_true:
                    column_concepts.add((i, j))

    return column_concepts



