__author__ = 'francois'

import sys
import os

sys.path.append(os.path.dirname('../'))
import io

import urllib.request
import shutil
from zipfile import ZipFile
import datetime

from DLC.doubly_lexical_order import doubly_lexical_order, gamma_free_matrix_top_down, gamma_free_matrix_bottom_up
from DLC.contextmatrix import ContextMatrix
from random_matrix_approximation import approximate, differences, approximate_one_try, print_result_matrices
import DLC.graphics
from DLC.triangle import elimination_order_matrix
from DLC.diss import Diss
from DLC.subdominant import subdominant

def download_file_if_not_present(file_name, url):
    if not os.path.isfile(file_name):
        print("download file from:", url, datetime.datetime.now(), file=sys.stderr)
        print("save it in:", file_name, file=sys.stderr)

        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("data saved.", file=sys.stderr)


def create_context_matrix_between_most_seen_movies(zip_file, number_keep):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
    number_users, number_movie, number_ratings = get_info(zip_file, base_directory)
    movie_user = dict()
    print("read file u.data", datetime.datetime.now(), file=sys.stderr)
    with ZipFile(zip_file) as myzip:
        file = io.TextIOWrapper(myzip.open(os.path.join(base_directory, "u.data")))
        for line in file:
            line = line.strip().split()
            user = int(line[0])
            movie = int(line[1])
            rating = int(line[2])
            if movie not in movie_user:
                movie_user[movie] = (set(), set())
            movie_user[movie][0].add(user)
            if rating >= 3:
                movie_user[movie][1].add(user)
    print("done", file=sys.stderr)

    keep_movies = list(range(1, number_movie + 1))
    keep_movies.sort(key=lambda x: len(movie_user[x][0]))
    keep_movies.reverse()

    keep_movies = list(keep_movies[:number_keep])
    keep_movies_dict = {x: i for i, x in enumerate(keep_movies[:number_keep])}
    print("read file u.data", datetime.datetime.now(), file=sys.stderr)
    number_movie = len(keep_movies)
    number_one = 0
    matrix = [[0] * 2 * number_movie for i in range(number_users)]

    with ZipFile(zip_file) as myzip:
        file = io.TextIOWrapper(myzip.open(os.path.join(base_directory, "u.data")))
        for line in file:
            line = line.strip().split()
            user = int(line[0]) - 1
            movie = int(line[1])
            rating = int(line[2])

            if movie not in keep_movies_dict:
                continue
            else:
                movie = keep_movies_dict[movie]
            matrix[user][2 * movie] = 1
            number_one += 1
            matrix[user][2 * movie + 1] = rating >= 3 and 1 or 0
            if matrix[user][2 * movie + 1] == 1:
                number_one += 1

    percent = number_one / (number_ratings * 2 * number_movie)
    print("done.", "(number 1 =", str(number_one) + ",", "percent=", str(percent) + ")", file=sys.stderr)
    print("create context matrix", datetime.datetime.now(), file=sys.stderr)
    attributes = []
    for number in keep_movies:
        attributes.extend((number, str(number) + "_like"))

    context_matrix = ContextMatrix(matrix, attributes=attributes, copy_matrix=False)
    print("done.", file=sys.stderr)
    return context_matrix


def create_context_matrix_rating_vs_all_movies(zip_file):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
    number_users, number_movie, number_ratings = get_info(zip_file, base_directory)
    matrix = []
    print("read file u.data", datetime.datetime.now(), file=sys.stderr)
    number_one = 0
    with ZipFile(zip_file) as myzip:
        file = io.TextIOWrapper(myzip.open(os.path.join(base_directory, "u.data")))
        for line in file:
            matrix_line = [0] * number_movie * 2
            line = line.strip().split()
            movie = int(line[1]) - 1
            rating = int(line[2])
            matrix_line[2 * movie] = 1
            number_one += 1
            matrix_line[2 * movie + 1] = rating >= 3 and 1 or 0
            if matrix_line[2 * movie + 1] == 1:
                number_one += 1

            matrix.append(matrix_line)

    percent = number_one / (number_ratings * 2 * number_movie)
    print("done.", "(number 1 =", str(number_one) + ",", "percent=", str(percent) + ")", file=sys.stderr)
    print("create context matrix", datetime.datetime.now(), file=sys.stderr)
    attributes = []
    for number in range(1, number_movie + 1):
        attributes.extend((number, str(number) + "_like"))
    context_matrix = ContextMatrix(matrix, attributes=attributes, copy_matrix=False)
    print("done.", file=sys.stderr)
    return context_matrix


def create_context_matrix_users_vs_all_movies(zip_file):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
    number_users, number_movie, number_ratings = get_info(zip_file, base_directory)
    matrix = [[0] * 2 * number_movie for i in range(number_users)]
    print("read file u.data", datetime.datetime.now(), file=sys.stderr)
    number_one = 0

    with ZipFile(zip_file) as myzip:
        file = io.TextIOWrapper(myzip.open(os.path.join(base_directory, "u.data")))
        for line in file:
            line = line.strip().split()
            user = int(line[0]) - 1
            movie = int(line[1]) - 1
            rating = int(line[2])

            matrix[user][2 * movie] = 1
            number_one += 1
            matrix[user][2 * movie + 1] = rating >= 3 and 1 or 0
            if matrix[user][2 * movie + 1] == 1:
                number_one += 1

    percent = number_one / (len(matrix) * len(matrix[0]))
    print("done.", "(number 1 =", str(number_one) + ",", "percent=", str(percent) + ")", file=sys.stderr)
    print("create context matrix", datetime.datetime.now(), file=sys.stderr)
    attributes = []
    for number in range(1, number_movie + 1):
        attributes.extend((number, str(number) + "_like"))
    context_matrix = ContextMatrix(matrix, attributes=attributes, copy_matrix=False)
    print("done.", file=sys.stderr)
    return context_matrix


def create_context_matrix_users_vs_seen_movies(zip_file):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
    number_users, number_movie, number_ratings = get_info(zip_file, base_directory)
    matrix = [[0] * number_movie for i in range(number_users)]
    print("read file u.data", datetime.datetime.now(), file=sys.stderr)
    number_one = 0

    with ZipFile(zip_file) as myzip:
        file = io.TextIOWrapper(myzip.open(os.path.join(base_directory, "u.data")))
        for line in file:
            line = line.strip().split()
            user = int(line[0]) - 1
            movie = int(line[1]) - 1
            rating = int(line[2])

            matrix[user][movie] = 1
            number_one += 1

    percent = number_one / (len(matrix) * len(matrix[0]))
    print("done.", "(number 1 =", str(number_one) + ",", "percent=", str(percent) + ")", file=sys.stderr)
    print("create context matrix", datetime.datetime.now(), file=sys.stderr)
    context_matrix = ContextMatrix(matrix, copy_matrix=False)
    print("done.", file=sys.stderr)
    return context_matrix


def get_info(zip_file, base_directory):
    info = dict()
    with ZipFile(zip_file) as myzip:
        file = io.TextIOWrapper(myzip.open(os.path.join(base_directory, "u.info")))
        for line in file:
            line = line.strip().split()
            info[line[1]] = int(line[0])

    return info['users'], info['items'], info['ratings']


def approximate_from_triangle(context_matrix):
    order = elimination_order_matrix(context_matrix.matrix)
    lines, columns = doubly_lexical_order(context_matrix.matrix, order)
    min_diff = None
    min_context_matrix = None
    approximation = context_matrix.copy()
    line_permutation = [0] * len(approximation.matrix)
    for i, index in enumerate(lines):
        line_permutation[index] = i

    column_permutation = [0] * len(approximation.matrix[0])
    for i, index in enumerate(columns):
        column_permutation[index] = i

    approximation.reorder(line_permutation, column_permutation)

    for strategy in (gamma_free_matrix_bottom_up, gamma_free_matrix_top_down):
        test_context_matrix = approximation.copy()
        strategy(test_context_matrix.matrix, True)
        diff = differences(test_context_matrix, approximation)
        if min_diff is None or (min_diff > diff):
            min_diff = diff
            min_context_matrix = test_context_matrix
        print("        ", strategy.__name__, diff, file=sys.stderr)
        if min_diff == 0:
            break
    print("        ", "min:", min_diff, file=sys.stderr)

    return min_context_matrix, min_diff


def create_dissimilarity_between_movies(zip_file, number_keep):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
    number_users, number_movie, number_ratings = get_info(zip_file, base_directory)
    movie_user = dict()
    print("read file u.data", datetime.datetime.now(), file=sys.stderr)
    with ZipFile(zip_file) as myzip:
        file = io.TextIOWrapper(myzip.open(os.path.join(base_directory, "u.data")))
        for line in file:
            line = line.strip().split()
            user = int(line[0])
            movie = int(line[1])
            rating = int(line[2])
            if movie not in movie_user:
                movie_user[movie] = (set(), set())
            movie_user[movie][0].add(user)
            if rating >= 3:
                movie_user[movie][1].add(user)
    print("done", file=sys.stderr)
    keep_movies = list(range(1, number_movie + 1))
    keep_movies.sort(key=lambda x: len(movie_user[x][0]))
    keep_movies.reverse()

    keep_movies = list(keep_movies[:number_keep])
    keep_movies_dict = {x: i for i, x in enumerate(keep_movies[:number_keep])}

    print("update dissimilarity values", datetime.datetime.now(), file=sys.stderr)
    dissimilarity = Diss(keep_movies)
    for i in range(number_keep):
        for j in range(i + 1, number_keep):
            same_user = movie_user[keep_movies[i]][0] - movie_user[keep_movies[j]][0]
            both_liked = (movie_user[keep_movies[i]][1] - movie_user[keep_movies[j]][1]) - same_user
            if len(same_user) == 0:
                dissimilarity.set_by_pos(i, j, 1)
            else:
                dissimilarity.set_by_pos(i, j, 1 - len(both_liked) / len(same_user))
    print("done", file=sys.stderr)
    return dissimilarity


def create_context_matrix_movie_movie(zip_file, number_keep):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
    number_users, number_movie, number_ratings = get_info(zip_file, base_directory)

    print("create dissimilarity", datetime.datetime.now(), file=sys.stderr)
    dissimilarity = create_dissimilarity_between_movies(zip_file, number_keep)
    print("done", file=sys.stderr)
    print("approximation", datetime.datetime.now(), file=sys.stderr)
    approximation = subdominant(dissimilarity)
    compare(dissimilarity, approximation)
    print("done", file=sys.stderr)
    # print("save", datetime.datetime.now(), file=sys.stderr)
    # file_io.save(approximation, open("approximation_dissimilarity.mat", "w"))
    # print("done", file=sys.stderr)
    two_balls = set()
    print("create clusters", datetime.datetime.now(), file=sys.stderr)
    matrix = [[] for i in range(number_keep)]
    known_two_balls = set()
    for i in range(len(approximation)):
        print("   ", i, len(approximation), file=sys.stderr)
        for j in range(i + 1, len(approximation)):

            two_ball = frozenset({z for z in range(len(approximation)) if
                                  approximation.get_by_pos(i, j) >= max(approximation.get_by_pos(i, z),
                                                                        approximation.get_by_pos(j, z))})
            if two_ball in known_two_balls:
                continue
            for line in matrix:
                line.append(0)
            for z in two_ball:
                matrix[z][-1] = 1

    print("done", file=sys.stderr)
    return ContextMatrix(matrix, elements=list(approximation), copy_matrix=False)


def compare(original_diss, approximated_diss):
    difference = approximated_diss - original_diss
    # print(difference)
    print(len(original_diss.values()), len(approximated_diss.values()))
    print("||approximated_diss - original_diss||_1")
    abs_difference = abs(difference)
    norm = sum(abs_difference .values())
    norm_normalized = 2.0 * norm / (len(difference) * (len(difference) - 1))
    print("raw       :", norm)
    print("normalized:", norm_normalized)
    print()

if __name__ == "__main__":
    DATA_FILE_NAME = "resources/ml-100k.zip"
    DATA_URL = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'

    download_file_if_not_present(DATA_FILE_NAME, DATA_URL)
    # context_matrix_original = create_context_matrix_rating_vs_all_movies(DATA_FILE_NAME)
    # context_matrix_original = create_context_matrix_users_vs_all_movies(DATA_FILE_NAME)
    # context_matrix_original = create_context_matrix_between_most_seen_movies(DATA_FILE_NAME, 100).transpose()
    # print(len(context_matrix_original.elements), len(context_matrix_original.attributes))
    # order_context_matrix, order_diff = approximate_from_triangle(context_matrix_original)
    # context_matrix_original = create_context_matrix_users_vs_seen_movies(DATA_FILE_NAME)
    context_matrix_original = create_context_matrix_movie_movie(DATA_FILE_NAME, 200)
    # print(context_matrix_original)
    print("Approximation start", datetime.datetime.now(), file=sys.stderr)
    min_context_matrix, min_lines, min_columns, min_diff = approximate(context_matrix_original, number_try=4)
    print("done.", file=sys.stderr)
    print("reorder", datetime.datetime.now(), file=sys.stderr)
    context_matrix_original.reorder(min_lines, min_columns)
    print("done.", file=sys.stderr)
    # print_result_matrices(context_matrix_original, min_context_matrix)

    print("number of changes", min_diff, "percent",
          100 * min_diff / (len(context_matrix_original.elements) * len(context_matrix_original.attributes)), "%")

    pruned_matrix = [[line[0]] for line in context_matrix_original.matrix]
    pruned_attributes = [context_matrix_original.attributes[0]]
    number = {pruned_attributes[-1]: 1}
    for column, element in zip(range(1, len(context_matrix_original.matrix[0])), context_matrix_original.attributes[1:]):
        same = True
        for i in range(len(context_matrix_original.matrix)):
            if context_matrix_original.matrix[i][column] != pruned_matrix[i][-1]:
                same = False
                continue
        if same:
            number[pruned_attributes[-1]] += 1
            continue

        for i in range(len(context_matrix_original.matrix)):
            pruned_matrix[i].append(context_matrix_original.matrix[i][column])
        pruned_attributes.append(element)
        number[element] = 1

    print(number)
    pruned_context_matrix = ContextMatrix(pruned_matrix, context_matrix_original.elements, pruned_attributes)

    # image = DLC.graphics.create_image_from_matrix(min_context_matrix.matrix, context_matrix_original.matrix)
    image = DLC.graphics.create_image_from_matrix(pruned_context_matrix.matrix)
    image.save("movie_rating_diss.png")
