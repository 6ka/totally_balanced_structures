__author__ = 'francois'

import sys
import os

sys.path.append(os.path.dirname('../'))
import io

import urllib.request
import shutil
from zipfile import ZipFile
import datetime

from DLC.doubly_lexical_order import gamma_free_matrix_top_down, gamma_free_matrix_bottom_up
from DLC.contextmatrix import ContextMatrix
from random_matrix_approximation import approximate, approximate_one_try, print_result_matrices
import DLC.graphics
from DLC.diss import Diss, file_io
from DLC.subdominant import subdominant


def download_file_if_not_present(file_name, url):
    if not os.path.isfile(file_name):
        print("download file from:", url, datetime.datetime.now(), file=sys.stderr)
        print("save it in:", file_name, file=sys.stderr)

        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("data saved.", file=sys.stderr)


def create_dissimilarity_between_movies(zip_file):
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
    keep_movies = list(keep_movies[:6])
    print("update dissimilarity values", datetime.datetime.now(), file=sys.stderr)
    dissimilarity = Diss(keep_movies)
    for i in range(len(keep_movies)):
        for j in range(i + 1, len(keep_movies)):
            same_user = movie_user[keep_movies[i]][0] - movie_user[keep_movies[j]][0]
            both_liked = (movie_user[keep_movies[i]][1] - movie_user[keep_movies[j]][1]) - same_user

            if len(same_user) == 0:
                dissimilarity.set_by_pos(i, j, 1)
            else:
                dissimilarity.set_by_pos(i, j, 1 - len(both_liked) / len(same_user))
    print("done", file=sys.stderr)
    return dissimilarity


def create_context_matrix_movie_movie(zip_file):
    print("create dissimilarity", datetime.datetime.now(), file=sys.stderr)
    dissimilarity = create_dissimilarity_between_movies(zip_file)
    print("done", file=sys.stderr)
    print("approximation", datetime.datetime.now(), file=sys.stderr)
    approximation = subdominant(dissimilarity)
    print(approximation)
    print("done", file=sys.stderr)

    print("save", datetime.datetime.now(), file=sys.stderr)
    file_io.save(approximation, open("approximation_dissimilarity.mat", "w"))
    print("done", file=sys.stderr)
    print("create clusters", datetime.datetime.now(), file=sys.stderr)
    f = open("dissimilarity_2_balls.csv", "w")
    for i in range(len(approximation)):
        print("   ", i, len(approximation), file=sys.stderr)
        for j in range(i + 1, len(approximation)):

            two_ball = frozenset({z for z in range(len(approximation)) if
                           approximation.get_by_pos(i, j) >= max(approximation.get_by_pos(i, z),
                                                                 approximation.get_by_pos(j, z))})
            f.write(",".join([str(x) for x in two_ball]))
            f.write("\n")
    f.close()
    print("done", file=sys.stderr)
    print("create context matrix", datetime.datetime.now(), file=sys.stderr)
    matrix = [[] for i in range(len(approximation))]
    f = open("dissimilarity_2_balls.csv")
    for two_ball_line in f:

        for line in matrix:
            line.append(0)
        two_ball = [int(x) for x in two_ball_line.split(",")]
        for z in two_ball:
            matrix[z][-1] = 1
    print("done", file=sys.stderr)
    print(matrix)
    return ContextMatrix(matrix, elements=list(approximation), copy_matrix=False)


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


if __name__ == "__main__":
    DATA_FILE_NAME = "resources/ml-100k.zip"
    DATA_URL = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'

    download_file_if_not_present(DATA_FILE_NAME, DATA_URL)
    # context_matrix_original = create_context_matrix_rating_vs_all_movies(DATA_FILE_NAME)
    # context_matrix_original = create_context_matrix_users_vs_all_movies(DATA_FILE_NAME)
    # context_matrix_original = create_context_matrix_users_vs_seen_movies(DATA_FILE_NAME)
    context_matrix_original = create_context_matrix_movie_movie(DATA_FILE_NAME)
    print("Approximation start", datetime.datetime.now(), file=sys.stderr)
    min_context_matrix, min_lines, min_columns, min_diff = approximate(context_matrix_original, number_try=4)
    print("done.", file=sys.stderr)
    print("reorder", datetime.datetime.now(), file=sys.stderr)
    context_matrix_original.reorder(min_lines, min_columns)
    print("done.", file=sys.stderr)
    # print_result_matrices(context_matrix_original, min_context_matrix)

    print("number of changes", min_diff, "percent",
          100 * min_diff / (len(context_matrix_original.elements) * len(context_matrix_original.attributes)), "%")
    image = DLC.graphics.create_image_from_matrix(min_context_matrix.matrix, context_matrix_original.matrix)
    image.save("movie_rating_diss.png")
