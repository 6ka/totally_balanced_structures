__author__ = 'francois'

import sys
import os

sys.path.append(os.path.dirname('../'))
import io

from zipfile import ZipFile

import DLC
from DLC.progress_bar import ProgressBar
from movie_rating import download_file_if_not_present, get_info
from DLC.contextmatrix import ContextMatrix
import DLC.graphics
from DLC.diss import Diss, file_io

from DLC.subdominant import subdominant, subdominant_number_step


def create_dissimilarity_between_movies(zip_file, number_keep):
    base_directory = os.path.splitext(os.path.basename(zip_file))[0]
    number_users, number_movie, number_ratings = get_info(zip_file)
    movie_user = dict()
    DLC.progress_status.update_status("read data file")

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
            DLC.progress_status.add(1)
    DLC.progress_status.update_status("data read.")

    DLC.progress_status.update_status("select movies to keep")
    keep_movies = list(range(1, number_movie + 1))
    keep_movies.sort(key=lambda x: len(movie_user[x][0]))
    keep_movies.reverse()

    keep_movies = list(keep_movies[:number_keep])
    DLC.progress_status.add(number_keep * number_keep, "movies selected")

    DLC.progress_status.update_status("create dissimilarity")
    dissimilarity = Diss(keep_movies)
    for i in range(number_keep):
        for j in range(i + 1, number_keep):
            same_user = movie_user[keep_movies[i]][0] - movie_user[keep_movies[j]][0]
            both_liked = (movie_user[keep_movies[i]][1] - movie_user[keep_movies[j]][1]) - same_user
            if len(same_user) == 0:
                dissimilarity.set_by_pos(i, j, 1)
            else:
                dissimilarity.set_by_pos(i, j, 1 - len(both_liked) / len(same_user))
    DLC.progress_status.add(number_keep * number_keep, "dissimilarity created")
    return dissimilarity


def create_context_matrix_movie_movie(zip_file, number_keep):
    dissimilarity = create_dissimilarity_between_movies(zip_file, number_keep)
    DLC.progress_status.stop()
    DLC.progress_status = ProgressBar()
    DLC.progress_status.add_max(NUMBER_MOVIES_TO_KEEP * NUMBER_MOVIES_TO_KEEP * (NUMBER_MOVIES_TO_KEEP - 1) / 2)
    DLC.progress_status.add_max(subdominant_number_step(NUMBER_MOVIES_TO_KEEP))

    DLC.progress_status.update_status("approximate dissimilarity")
    approximation = subdominant(dissimilarity)
    DLC.progress_status.update_status("approximation done")

    DLC.progress_status.update_status("create clusters")
    matrix = [[] for i in range(number_keep)]
    known_two_balls = set()
    for i in range(len(approximation)):
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
            DLC.progress_status.add(number_keep * number_keep * (number_keep - 1) / 2)

    return ContextMatrix(matrix, elements=list(approximation), copy_matrix=False), dissimilarity, approximation


def compare(original_diss, approximated_diss):
    difference = approximated_diss - original_diss
    # print(difference)
    print(len(original_diss.values()), len(approximated_diss.values()))
    print("||approximated_diss - original_diss||_1")
    abs_difference = abs(difference)
    norm = sum(abs_difference.values())
    norm_normalized = 2.0 * norm / (len(difference) * (len(difference) - 1))
    print("raw       :", norm)
    print("normalized:", norm_normalized)
    print()


if __name__ == "__main__":
    DATA_FILE_NAME = "resources/ml-100k.zip"
    DATA_URL = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'

    NUMBER_MOVIES_TO_KEEP = 50
    OUTPUT_FILE_NAME = "movie_rating_dissimilarity.png"

    download_file_if_not_present(DATA_FILE_NAME, DATA_URL)
    number_users, number_movie, number_ratings = get_info(DATA_FILE_NAME)

    DLC.progress_status = ProgressBar()
    DLC.progress_status.add_max(number_ratings)
    DLC.progress_status.add_max(2 * NUMBER_MOVIES_TO_KEEP * NUMBER_MOVIES_TO_KEEP)
    context_matrix_original, original_dissimilarity, approximation = create_context_matrix_movie_movie(DATA_FILE_NAME,
                                                                                                       NUMBER_MOVIES_TO_KEEP)
    DLC.progress_status.update_status("context matrix created")
    DLC.progress_status.stop()
    compare(original_dissimilarity, approximation)
    DLC.progress_status = ProgressBar()
    matrix_size = len(context_matrix_original.elements) * len(context_matrix_original.attributes)
    DLC.progress_status.add_max(matrix_size)
    DLC.progress_status.update_status("reorder context matrix")
    context_matrix_original.reorder_doubly_lexical_order()
    DLC.progress_status.add(matrix_size, "matrix reordered.")
    DLC.progress_status.stop()
    compare(original_dissimilarity, approximation)
    DLC.progress_status = ProgressBar()

    DLC.progress_status.add_max(3 * matrix_size)
    DLC.progress_status.update_status("prune matrix")
    pruned_matrix = [[line[0]] for line in context_matrix_original.matrix]
    pruned_attributes = [context_matrix_original.attributes[0]]

    number = {pruned_attributes[-1]: 1}
    DLC.progress_status.add(matrix_size)
    deleted_columns = 0
    for column, element in zip(range(1, len(context_matrix_original.matrix[0])),
                               context_matrix_original.attributes[1:]):
        same = True
        for i in range(len(context_matrix_original.matrix)):
            if context_matrix_original.matrix[i][column] != pruned_matrix[i][-1]:
                same = False
                continue
        if same:
            number[pruned_attributes[-1]] += 1
            deleted_columns += 1
            continue

        for i in range(len(context_matrix_original.matrix)):
            pruned_matrix[i].append(context_matrix_original.matrix[i][column])
        pruned_attributes.append(element)
        number[element] = 1
        DLC.progress_status.add(len(context_matrix_original.elements))

    pruned_context_matrix = ContextMatrix(pruned_matrix, context_matrix_original.elements, pruned_attributes, False)

    DLC.progress_status.update_status("save image")
    image = DLC.graphics.create_image_from_matrix(pruned_context_matrix.matrix)
    image.save(OUTPUT_FILE_NAME)
    DLC.progress_status.add(matrix_size, "image saved")
    DLC.progress_status.stop()
    print("number of pruned columns:", deleted_columns,
          "{0: 3.0f}%".format(100 * deleted_columns / len(context_matrix_original.attributes)))
