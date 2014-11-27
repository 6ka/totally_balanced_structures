__author__ = 'fbrucker'

from DLC.graph import Graph
from .clusters import boxes_clusters, atom_clusters_correspondence
from DLC.lattice import sup_irreducible_clusters


def cover_graph_from_clusters(clusters, bottom="BOTTOM", top="TOP"):
    cover_graph = Graph(directed=True)
    for atom in matrix_atoms(clusters):
        cover_graph.update([(bottom, atom)])

    boxes_i, boxes_j = boxes_clusters(clusters)
    if not boxes_i:
        cover_graph.update([(bottom, top)])
        return cover_graph

    for vertex in boxes_i:
        min_i, max_i = boxes_i[vertex]
        min_j, max_j = boxes_j[vertex]

        first_neighbor_up = pred_cluster_line(min_i, max_j, clusters)
        neighbor_right = next_cluster_column(min_i, max_j, clusters)

        if neighbor_right is not None:
            neighbor_up_min_i, neighbor_up_max_i = boxes_i.get(first_neighbor_up, (-1, -1))
            neighbor_right_min_i, neighbor_right_max_i = boxes_i[neighbor_right]
            if first_neighbor_up is None or neighbor_up_max_i < neighbor_right_min_i:
                cover_graph.update([(vertex, neighbor_right)])

        j = max_j
        neighbor_up = first_neighbor_up
        while neighbor_up is not None and j >= min_j:
            cover_graph.update([(vertex, neighbor_up)])
            j, drop = boxes_j.get(neighbor_up, (-1, -1))
            j -= 1
            neighbor_up = pred_cluster_line(min_i, j, clusters)

    before_top = set(x for x in cover_graph if cover_graph.degree(x) == 0)
    for vertex in before_top:
        cover_graph.update([(vertex, top)])

    return cover_graph


def next_cluster_column(i, j, clusters):
    for next_j in range(j + 1, len(clusters[i])):
        if clusters[i][next_j] is not None:
            return clusters[i][next_j]
    return None


def pred_cluster_line(i, j, clusters):
    for next_i in range(i - 1, -1, -1):
        if clusters[next_i][j] is not None:
            return clusters[next_i][j]
    return None


def matrix_atoms(clusters):
    last_clusters = set()
    for j in range(len(clusters[0])):
        for i in range(len(clusters) - 1, -1, -1):
            if clusters[i][j] is not None:
                last_clusters.add(clusters[i][j])
                break
    return last_clusters


def cluster_cover_graph_correspondence(clusters, cover_graph, line_atom_correspondence):

    number_to_cluster, cluster_to_number = atom_clusters_correspondence(clusters, line_atom_correspondence)
    number_to_cluster_lattice = sup_irreducible_clusters(cover_graph)
    cluster_to_number_lattice = {cluster: number for number, cluster in number_to_cluster_lattice.items()}
    clusters_lattice = []
    for i in range(len(clusters)):
        clusters_lattice.append(list(clusters[i]))
        for j in range(len(clusters[i])):
            if clusters[i][j] is not None:
                clusters_lattice[i][j] = cluster_to_number_lattice[number_to_cluster[clusters[i][j]]]
    return clusters_lattice