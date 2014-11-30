__author__ = 'francois'


def raw_matrix(matrix, digit=lambda x: x == 1 and "X" or "."):
    return "\n".join(["".join([digit(elem) for elem in line]) for line in matrix])


def raw_matrix_indices(matrix, digit=lambda i, j, matrix: matrix[i][j] == 1 and "X" or "."):
    return "\n".join(["".join([digit(i, j, matrix) for j in range(len(matrix[0]))]) for i in range(len(matrix))])


def compare_raw_matrices(matrix_original, matrix_solution, digit=lambda x, y: x == 1 and "X" or "."):
    lines = []
    for line_original, line_solution in zip(matrix_original, matrix_solution):
        lines.append(" ".join(["".join([digit(line_original[i], line_solution[i]) for i in range(len(line_original))]),
                               "".join([digit(line_solution[i], line_original[i]) for i in range(len(line_solution))])]))

    return "\n".join(line for line in lines)
