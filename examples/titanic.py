__author__ = 'francois'

import sys
import os

sys.path.append(os.path.dirname('../'))

import csv
import urllib.request
import shutil

from DLC.contextmatrix import ContextMatrix

from random_matrix_approximation import approximate, print_result_matrices


def csv_file():
    TITANIC_FILE = "resources/titanic.csv"
    TITANIC_URL = 'http://vincentarelbundock.github.io/Rdatasets/csv/datasets/Titanic.csv'

    if not os.path.isfile(TITANIC_FILE):
        with urllib.request.urlopen(TITANIC_URL) as response, open(TITANIC_FILE, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    file = open(TITANIC_FILE)
    return csv.reader(open(TITANIC_FILE))


def compute_context_matrix():
    title = None
    matrix = []
    for line in csv_file():
        if title is None:
            title = line
            continue

        matrix_line = []
        if line[1] == "1st":
            matrix_line.extend((1, 0, 0, 0))
        elif line[1] == "2nd":
            matrix_line.extend((0, 1, 0, 0))
        elif line[1] == "3rd":
            matrix_line.extend((0, 0, 1, 0))
        elif line[1] == "Crew":
            matrix_line.extend((0, 0, 0, 1))

        if line[2] == "Male":
            matrix_line.append(1)
        else:
            matrix_line.append(0)
        if line[3] == "Child":
            matrix_line.append(0)
        else:
            matrix_line.append(1)

        if line[4] == "No":
            matrix_line.append(0)
        else:
            matrix_line.append(1)

        for i in range(int(line[5])):
            matrix.append(matrix_line)

    context_matrix = ContextMatrix(matrix)
    context_matrix.attributes = ("1st", "2nd", "3rd", "crew", "sex", "age", "survived")
    return context_matrix


if __name__ == "__main__":
    context_matrix_original = compute_context_matrix()

    min_context_matrix, min_lines, min_columns, min_diff = approximate(context_matrix_original)
    context_matrix_original.reorder(min_lines, min_columns)
    print_result_matrices(context_matrix_original, min_context_matrix)
    print("percentage of differences", min_diff,
          min_diff / (len(context_matrix_original.elements) * len(context_matrix_original.attributes)))
