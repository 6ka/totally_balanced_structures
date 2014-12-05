__author__ = 'francois'

import sys
import os

sys.path.append(os.path.dirname('../'))

import csv

from DLC.contextmatrix import ContextMatrix
import DLC.graphics

from random_matrix_approximation import approximate, print_result_matrices
from movie_rating import download_file_if_not_present


def compute_context_matrix(file_name):
    title = None
    matrix = []
    for line in csv.reader(open(file_name)):
        if title is None:
            title = line
            continue
        matrix_line = [float(x) for x in line[1:]]
        matrix_line_no_class = [float(x) for x in line[1:]]
        if int(line[0]) == 0:  # Setosa
            matrix_line.extend((1, 0, 0))
        elif int(line[0]) == 1:  # Virginica
            matrix_line.extend((0, 1, 0))
        elif int(line[0]) == 2:  # Versicolor
            matrix_line.extend((0, 0, 1))

        matrix.append(matrix_line)

    binarize_matrix(matrix)
    matrix_no_class = [list(line[3:]) for line in matrix]
    context_matrix = ContextMatrix(matrix, attributes=[x.strip() for x in title[:-1]] + ["Setosa", "Virginica", "Versicolor"], copy_matrix=False)
    context_matrix_no_class = ContextMatrix(matrix_no_class, attributes=[x.strip() for x in title[:-1]], copy_matrix=False)
    return context_matrix, context_matrix_no_class


def binarize_matrix(matrix):
    mean = [0, 0, 0, 0]
    for line in matrix:
        mean = [mean[i] + line[i] for i in range(4)]

    mean = [x / len(matrix) for x in mean]
    for line in matrix:
        for i in range(4):
            if line[i] <= mean[i]:
                line[i] = 0
            else:
                line[i] = 1


def prune_context_matrix(context_matrix):
    pruned_matrix = [context_matrix.matrix[0]]
    pruned_elements = [context_matrix.elements[0]]
    number = {pruned_elements[-1]: {context_matrix.elements[0]}}
    for line, element in zip(context_matrix.matrix[1:], context_matrix.elements[1:]):
        if line == pruned_matrix[-1]:
            number[pruned_elements[-1]].add(element)
            continue
        pruned_matrix.append(line)
        pruned_elements.append(element)
        number[element] = {element}

    return ContextMatrix(pruned_matrix, pruned_elements, context_matrix.attributes, False), number


if __name__ == "__main__":
    DATA_FILE_NAME = "resources/fisher.csv"
    DATA_URL = 'http://www.math.uah.edu/stat/data/Fisher.csv'

    download_file_if_not_present(DATA_FILE_NAME, DATA_URL)

    APPROXIMATION_NUMBER_TRY = 2

    OUTPUT_FILE_NAME = "iris.png"

    context_matrix_original, context_matrix_without_class = compute_context_matrix(DATA_FILE_NAME)

    min_context_matrix, min_lines, min_columns, min_diff = approximate(context_matrix_original)
    print("number of changes", min_diff, "percent",
          100 * min_diff / (len(context_matrix_original.elements) * len(context_matrix_original.attributes)), "%")

    context_matrix_original.reorder(min_lines, min_columns)
    different_lines = []
    original_lines = []
    elements = []
    for i, (line_approximation, line_original) in enumerate(zip(min_context_matrix.matrix, context_matrix_original.matrix)):
        if line_approximation != line_original:
            different_lines.append(line_approximation)
            original_lines.append(line_original)
            elements.append(context_matrix_original.elements[i])

    print("elements which differ:", elements)
    print("attributes:", context_matrix_original.attributes)
    print_result_matrices(different_lines, original_lines)

    pruned_context_matrix, number = prune_context_matrix(min_context_matrix)
    print("Number of line pruned:", len(min_context_matrix.elements) - len(pruned_context_matrix.elements))
    print(DLC.graphics.from_context_matrix(pruned_context_matrix))


    min_context_matrix, min_lines, min_columns, min_diff = approximate(context_matrix_without_class)
    print("number of changes", min_diff, "percent",
          100 * min_diff / (len(context_matrix_original.elements) * len(context_matrix_original.attributes)), "%")

    pruned_context_matrix, number = prune_context_matrix(min_context_matrix)
    print("Number of line pruned:", len(min_context_matrix.elements) - len(pruned_context_matrix.elements))
    print(DLC.graphics.from_context_matrix(pruned_context_matrix))


    setosa_index = context_matrix_original.attributes.index("Setosa")
    virginica_index = context_matrix_original.attributes.index("Virginica")
    versicolor_index = context_matrix_original.attributes.index("Versicolor")
    for i in pruned_context_matrix.elements:
        lines = number[i]
        setosa = {x for x in lines if
                  context_matrix_original.matrix[context_matrix_original.elements.index(x)][setosa_index] == 1}
        virginica = {x for x in lines if
                     context_matrix_original.matrix[context_matrix_original.elements.index(x)][virginica_index] == 1}
        versicolor = {x for x in lines if
                      context_matrix_original.matrix[context_matrix_original.elements.index(x)][versicolor_index] == 1}
        print("line", i, "number Setosa:", len(setosa), "number virginica:", len(virginica), "number versicolor",
              len(versicolor))
