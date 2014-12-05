__author__ = 'francois'

import sys
import os

sys.path.append(os.path.dirname('../'))
sys.path.append(os.path.dirname('./'))

import io

import urllib.request
import shutil
from zipfile import ZipFile
import datetime

from DLC.doubly_lexical_order import gamma_free_matrix_top_down, gamma_free_matrix_bottom_up
from DLC.contextmatrix import ContextMatrix
from random_matrix_approximation import approximate, approximate_one_try, print_result_matrices

import DLC
from DLC.progress_bar import ProgressBar


def download_file_if_not_present(file_name, url):
    if not os.path.isfile(file_name):
        print("download file from:", url, datetime.datetime.now(), file=sys.stderr)
        print("save it in:", file_name, file=sys.stderr)

        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        print("data saved.", file=sys.stderr)


def create_context_matrix_users_vs_all_movies_and_ratings(zip_file, has_liked=3):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
    number_users, number_movie, number_ratings = get_info(zip_file)
    DLC.progress_status.add_max(2 * number_movie * number_users + number_ratings)

    DLC.progress_status.update_status("create empty matrix")
    matrix = [[0] * 2 * number_movie for i in range(number_users)]
    DLC.progress_status.add(2 * number_movie * number_users, "empty matrix created")

    DLC.progress_status.update_status("read data file")

    with ZipFile(zip_file) as myzip:
        file = io.TextIOWrapper(myzip.open(os.path.join(base_directory, "u.data")))
        for line in file:
            line = line.strip().split()
            user = int(line[0]) - 1
            movie = int(line[1]) - 1
            rating = int(line[2])

            matrix[user][2 * movie] = 1
            matrix[user][2 * movie + 1] = rating >= has_liked and 1 or 0
            DLC.progress_status.add(1)
    DLC.progress_status.update_status("data read.")

    attributes = []
    for number in range(1, number_movie + 1):
        attributes.extend((number, str(number) + "_like"))
    context_matrix = ContextMatrix(matrix, attributes=attributes, copy_matrix=False)
    return context_matrix


def create_context_matrix_users_vs_seen_movies(zip_file):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
    number_users, number_movie, number_ratings = get_info(zip_file)
    DLC.progress_status.add_max(number_movie * number_users + number_ratings)

    DLC.progress_status.update_status("create empty matrix")
    matrix = [[0] * number_movie for i in range(number_users)]
    DLC.progress_status.add(2 * number_movie * number_users, "empty matrix created")

    DLC.progress_status.update_status("read data file")

    with ZipFile(zip_file) as myzip:
        file = io.TextIOWrapper(myzip.open(os.path.join(base_directory, "u.data")))
        for line in file:
            line = line.strip().split()
            user = int(line[0]) - 1
            movie = int(line[1]) - 1

            matrix[user][movie] = 1
            DLC.progress_status.add(1)

    DLC.progress_status.update_status("data read.")

    context_matrix = ContextMatrix(matrix, copy_matrix=False)
    return context_matrix


def get_info(zip_file):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
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

    APPROXIMATION_NUMBER_TRY = 2
    APPROXIMATION_STRATEGIES = (gamma_free_matrix_bottom_up, gamma_free_matrix_top_down)

    OUTPUT_FILE_NAME = "movie_rating.png"

    number_users, number_movie, number_ratings = get_info(DATA_FILE_NAME)

    DLC.progress_status = ProgressBar()

    # context_matrix_original = create_context_matrix_users_vs_all_movies_and_ratings(DATA_FILE_NAME)
    context_matrix_original = create_context_matrix_users_vs_seen_movies(DATA_FILE_NAME)

    DLC.progress_status.update_status("context matrix created")
    DLC.progress_status.stop()
    DLC.progress_status = ProgressBar()
    matrix_size = len(context_matrix_original.elements) * len(context_matrix_original.attributes)
    DLC.progress_status.add_max(APPROXIMATION_NUMBER_TRY * len(APPROXIMATION_STRATEGIES) * matrix_size)
    DLC.progress_status.add_max(3 * matrix_size)

    min_context_matrix, min_lines, min_columns, min_diff = approximate(context_matrix_original,
                                                                       number_try=APPROXIMATION_NUMBER_TRY)
    DLC.progress_status.update_status("doubly lexically order the matrix")
    context_matrix_original.reorder(min_lines, min_columns)
    DLC.progress_status.add(matrix_size, "matrix reordered.")

    DLC.progress_status.update_status("save first image")
    image = DLC.graphics.create_image_from_matrix(min_context_matrix.matrix, context_matrix_original.matrix)
    image.save("compare_" + OUTPUT_FILE_NAME)
    DLC.progress_status.add(matrix_size, "image compare saved.")
    DLC.progress_status.update_status("save second image")
    image = DLC.graphics.create_image_from_matrix(min_context_matrix.matrix)
    image.save("approximation_" + OUTPUT_FILE_NAME)
    DLC.progress_status.add(matrix_size, "images saved.")
    DLC.progress_status.stop()
    DLC.reset_progress_status()

    print("number of changes", min_diff, "percent",
          100 * min_diff / (len(context_matrix_original.elements) * len(context_matrix_original.attributes)), "%")

