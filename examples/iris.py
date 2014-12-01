__author__ = 'francois'

import sys
import os

sys.path.append(os.path.dirname('../'))

import csv

from DLC.contextmatrix import ContextMatrix
import DLC.graphics

from random_matrix_approximation import approximate, print_result_matrices


def compute_context_matrix():
    title = None
    matrix = []
    for line in csv.reader(open("resources/iris.csv")):
        if title is None:
            title = line
            continue
        matrix_line = [float(x) for x in line[:4]]
        if line[4].find("setosa") != -1:
            matrix_line.extend((1, 0, 0))
        elif line[4].find("versicolor") != -1:
            matrix_line.extend((0, 1, 0))
        elif line[4].find("virginica") != -1:
            matrix_line.extend((0, 0, 1))

        matrix.append(matrix_line)

    binarize_matrix(matrix)
    context_matrix = ContextMatrix(matrix)
    context_matrix.attributes = [x.strip() for x in title[:-1]] + ["setosa", "versicolor", "virginica"]
    return context_matrix


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

if __name__ == "__main__":
    context_matrix_original = compute_context_matrix()
    min_context_matrix, min_lines, min_columns, min_diff = approximate(context_matrix_original)
    context_matrix_original.reorder(min_lines, min_columns)
    # print_result_matrices(context_matrix_original, min_context_matrix)
    print(DLC.graphics.from_context_matrix(min_context_matrix))

    print("percentage of differences", min_diff,
          min_diff / (len(context_matrix_original.elements) * len(context_matrix_original.attributes)))


    pruned_matrix = [context_matrix_original.matrix[0]]
    pruned_elements = [context_matrix_original.elements[0]]
    number = {pruned_elements[-1]: 1}
    for line, element in zip(context_matrix_original.matrix[1:], context_matrix_original.elements[1:]):
        if line == pruned_matrix[-1]:
            number[pruned_elements[-1]] += 1
            continue
        pruned_matrix.append(line)
        pruned_elements.append(element)
        number[element] = 1

    pruned_context_matrix = ContextMatrix(pruned_matrix, pruned_elements, context_matrix_original.attributes)
    print(DLC.graphics.from_context_matrix(pruned_context_matrix))
    image = DLC.graphics.create_image_from_matrix(pruned_context_matrix.matrix)
    image.save("iris.png")

# for element in pruned_context_matrix.elements:
    #     print(element, number[element])
    #
    #
    # transpose = pruned_context_matrix.transpose()
    # transpose.reorder_doubly_lexical_order()
    # print(DLC.graphics.from_context_matrix(transpose))
