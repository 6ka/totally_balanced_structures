__author__ = 'francois'

import sys
import os

sys.path.append(os.path.dirname('../'))

import DLC
from DLC.progress_bar import ProgressBar

import DLC.graphics
import DLC.randomize
import DLC.doubly_lexical_order
from DLC.doubly_lexical_order import gamma_free_matrix_bottom_up, gamma_free_matrix_top_down
from DLC.contextmatrix import ContextMatrix

import colorama


def differences_position(original_matrix, approximated_matrix):
    string_repr = ""
    for i in range(len(original_matrix)):
        for j in range(len(original_matrix[i])):
            if original_matrix[i][j] == approximated_matrix[i][j] == 0:
                string_repr = "".join([string_repr, "."])
            elif original_matrix[i][j] == approximated_matrix[i][j] == 1:
                string_repr = "".join([string_repr, "X"])
            elif approximated_matrix[i][j] == 0 and original_matrix[i][j] != approximated_matrix[i][j]:
                string_repr = "".join([string_repr, ","])
            else:
                string_repr = "".join([string_repr, "*"])
        string_repr = "".join([string_repr, "\n"])

    return string_repr


def approximate(context_matrix_original, number_try=20,
                strategies=(gamma_free_matrix_bottom_up, gamma_free_matrix_top_down)):
    DLC.progress_status.update_status("approximation process begin")
    original_element_index = {x: i for i, x in enumerate(context_matrix_original.elements)}
    original_attributes_index = {x: i for i, x in enumerate(context_matrix_original.attributes)}
    min_diff = min_context_matrix = None
    for current_try in range(number_try):
        DLC.progress_status.update_status(" ".join(
            ("try", str(current_try + 1), "/", str(number_try), min_diff and "current min: " + str(min_diff) or "")))
        context_matrix, diff = approximate_one_try(context_matrix_original, strategies)

        if min_diff is None or (min_diff > diff):
            min_diff = diff
            min_context_matrix = context_matrix
            if min_diff == 0:
                break

        if current_try < number_try - 1:
            context_matrix_original = context_matrix_original.copy()
            DLC.randomize.shuffle_line_and_column_from_context_matrix(context_matrix_original)

    line_order = [0] * len(context_matrix_original.elements)
    for i, x in enumerate(min_context_matrix.elements):
        line_order[original_element_index[x]] = i

    column_order = [0] * len(context_matrix_original.attributes)
    for i, x in enumerate(min_context_matrix.attributes):
        column_order[original_attributes_index[x]] = i

    return min_context_matrix, line_order, column_order, min_diff


def approximate_one_try(context_matrix_original, strategies=(gamma_free_matrix_bottom_up, gamma_free_matrix_top_down)):
    min_diff = None
    min_context_matrix = None
    status = DLC.progress_status.status
    matrix_size = len(context_matrix_original.elements) * len(context_matrix_original.attributes)
    number_approximation = 0
    for strategy in strategies:
        DLC.progress_status.update_status(" ".join((status, "stategy:", strategy.__name__)))
        context_matrix = DLC.doubly_lexical_order.context_matrix_approximation(context_matrix_original, strategy)
        diff = differences(context_matrix_original, context_matrix)
        if min_diff is None or (min_diff > diff):
            min_diff = diff
            min_context_matrix = context_matrix
        DLC.progress_status.add(matrix_size, " ".join(("diff:", str(diff), "minimal:", str(min_diff))))
        number_approximation += 1
        if min_diff == 0:
            if number_approximation < len(strategies):
                DLC.progress_status.add(matrix_size * (len(strategies) - number_approximation),
                                        " ".join(("diff:", str(min_diff))))
            break

    return min_context_matrix, min_diff


def differences(original, approximated):
    original_element_index = {x: i for i, x in enumerate(original.elements)}
    original_attributes_index = {x: i for i, x in enumerate(original.attributes)}

    number = 0
    for i, x in enumerate(approximated.elements):
        for j, y in enumerate(approximated.attributes):
            if approximated.matrix[i][j] != original.matrix[original_element_index[x]][original_attributes_index[y]]:
                number += 1

    return number


def change_color(x, y):
    if x != y:
        digit = colorama.Fore.RED
    else:
        digit = colorama.Fore.WHITE
    if x == 0:
        digit += "."
    else:
        digit += "X"

    return digit


def diff_digit(compare_matrix):
    def change_color(i, j, matrix):
        if compare_matrix[i][j] != matrix[i][j]:
            digit = colorama.Fore.RED
        else:
            digit = colorama.Fore.WHITE
        if matrix[i][j] == 0:
            digit += "."
        else:
            digit += "X"

        return digit

    return change_color


def print_result_matrices(original, approximation):
    colorama.init()
    print(DLC.graphics.raw_matrix_indices(approximation.matrix, diff_digit(original.matrix)))
    print(colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL)


if __name__ == "__main__":
    CONTEXT_MATRIX_NUMBER_LINES = 60
    CONTEXT_MATRIX_NUMBER_COLUMNS = 150
    CONTEXT_MATRIX_PROBABILITY_OF_ONE = .1
    APPROXIMATION_NUMBER_TRY = 20
    APPROXIMATION_STRATEGIES = (gamma_free_matrix_bottom_up, gamma_free_matrix_top_down)

    matrix_size = CONTEXT_MATRIX_NUMBER_LINES * CONTEXT_MATRIX_NUMBER_COLUMNS
    DLC.progress_status = ProgressBar()
    DLC.progress_status.add_max(matrix_size)
    DLC.progress_status.add_max(APPROXIMATION_NUMBER_TRY * len(APPROXIMATION_STRATEGIES) * matrix_size)
    DLC.progress_status.add_max(matrix_size)

    DLC.progress_status.update_status("create random matrix")
    context_matrix_orig = ContextMatrix(
        DLC.randomize.random_01_matrix(CONTEXT_MATRIX_NUMBER_LINES, CONTEXT_MATRIX_NUMBER_COLUMNS,
                                       CONTEXT_MATRIX_PROBABILITY_OF_ONE))
    DLC.progress_status.add(matrix_size, "context matrix created")
    min_context_matrix, min_lines, min_columns, min_diff = approximate(context_matrix_orig)
    DLC.progress_status.update_status("doubly lexically order the matrix")
    context_matrix_orig.reorder(min_lines, min_columns)
    DLC.progress_status.add(matrix_size, "matrix reordered.")
    DLC.progress_status.stop()
    DLC.reset_progress_status()
    print_result_matrices(context_matrix_orig, min_context_matrix)
    print("number of changes", min_diff, "percent",
          100 * min_diff / (len(context_matrix_orig.elements) * len(context_matrix_orig.attributes)))


