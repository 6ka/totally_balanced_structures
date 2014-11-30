__author__ = 'fbrucker'

from DLC.graph import Graph
from .clusters import ClusterLineFromMatrix


def cover_graph_and_boxes_from_matrix(matrix, bottom="BOTTOM", top="TOP"):
    cover_graph = Graph(directed=True)
    boxes_cluster_line = dict()
    boxes_cluster_columns = dict()

    last_line = last_line_not_0_for_matrix(matrix)
    last_clusters = [None] * len(matrix[0])
    line_iterator = ClusterLineFromMatrix(matrix)
    for i, current_line in enumerate(line_iterator):
        for j, elem in enumerate(current_line):
            if elem is None:
                continue
            min_current_line, max_current_line = boxes_cluster_line.get(elem, (i, i))
            min_current_column, max_current_column = boxes_cluster_columns.get(elem, (j, j))
            boxes_cluster_line[elem] = (min(i, min_current_line), max(i, max_current_line))
            boxes_cluster_columns[elem] = (min(j, min_current_column), max(j, max_current_column))

        j = len(current_line) - 1
        while j >= 0:
            if current_line[j] is None or current_line[j] in cover_graph:
                j -= 1
                continue

            current_cluster = current_line[j]
            # connect to bottom
            if i == last_line[j]:
                cover_graph.update([(bottom, current_cluster)])

            # successor in line
            right_successor = True
            j_next = j + 1
            while j_next < len(current_line) and current_line[j_next] is None:
                j_next += 1

            if j_next == len(current_line):
                right_successor = False
            if i > 0 and line_iterator.previous_line[j] is not None:
                if j_next == len(current_line) or current_line[j_next] == line_iterator.previous_line[j_next]:
                    right_successor = False
            if right_successor:
                cover_graph.update([(current_cluster, current_line[j_next])])

            # successor before line
            while j >= 0 and current_line[j] == current_cluster:
                if last_clusters[j] is not None and last_clusters[j] != current_cluster:
                    cover_graph.update([(current_cluster, last_clusters[j])])
                    successor = last_clusters[j]
                    while j >= 0 and last_clusters[j] == successor:
                        j -= 1
                else:
                    break

            while j >= 0 and current_line[j] == current_cluster:
                j -= 1

        last_clusters = [new_cluster or old_cluster for new_cluster, old_cluster in zip(current_line, last_clusters)]

    for vertex in set(x for x in cover_graph if cover_graph.degree(x) == 0):
        cover_graph.update([(vertex, top)])

    return cover_graph, boxes_cluster_line, boxes_cluster_columns


def cover_graph_from_matrix(matrix, bottom="BOTTOM", top="TOP"):
    return cover_graph_and_boxes_from_matrix(matrix, bottom, top)[0]


def last_line_not_0_for_matrix(matrix):
    last_line = [-1] * len(matrix[0])
    for j in range(len(matrix[0])):
        for i in range(len(matrix) - 1, -1, -1):
            if matrix[i][j] == 1:
                last_line[j] = i
                break
    return last_line