__author__ = 'fbrucker'

__all__ = ["hierarchical_height_from_lattice"]
import DLC.lattice
from DLC.clusters import ClusterLineFromMatrix


def hierarchical_height_from_lattice(dismantable_lattice, bottom=None):
    if bottom is None:
        bottom = DLC.lattice.get_bottom(dismantable_lattice)
    atoms = set(DLC.lattice.sup_irreducible(dismantable_lattice))
    current_graph = dismantable_lattice.copy()
    current_graph.remove(bottom)
    vertex_height = dict()
    current_height = 0
    while atoms:
        current_chains = set()
        current_atoms = set(atoms)
        while current_atoms:
            vertex = current_atoms.pop()
            possible_chain = set()
            current = vertex
            if vertex in current_chains:
                atoms.remove(vertex)
                continue
            while current_graph.degree(current) <= 1:
                possible_chain.add(current)
                if current_graph.degree(current) == 0 or current in current_chains:
                    current_chains.update(possible_chain)
                    if vertex in atoms:
                        atoms.remove(vertex)
                    break
                else:
                    current = current_graph[current][0]
        for x in current_chains:
            vertex_height[x] = current_height
            current_graph.remove(x)
        current_height += 1

    return vertex_height


# def hierarchical_height_from_DLO_matrix(matrix):
#     last_clusters = [None] * len(matrix[0])
#     line_iterator = ClusterLineFromMatrix(matrix)
#     last_height = [0] * len(matrix[0])
#     vertex_height = dict()
#     for i, current_line in enumerate(line_iterator):
#         j = len(current_line) - 1
#         while j >= 0:
#             if current_line[j] is None or (i > 0 and current_line[j] == line_iterator.previous_line[j]):
#                 j -= 1
#                 continue
#
#             current_cluster = current_line[j]
#
#             # successor in line
#             if i > 0
#             right_successor = True
#             j_next = j + 1
#             while j_next < len(current_line) and current_line[j_next] is None:
#                 j_next += 1
#
#             if j_next == len(current_line):
#                 right_successor = False
#             if i > 0 and line_iterator.previous_line[j] is not None:
#                 if j_next == len(current_line) or current_line[j_next] == line_iterator.previous_line[j_next]:
#                     right_successor = False
#             if right_successor:
#                 cover_graph.update([(current_cluster, current_line[j_next])])
#
#             # successor before line
#             while j >= 0 and current_line[j] == current_cluster:
#                 if last_clusters[j] is not None:
#                     cover_graph.update([(current_cluster, last_clusters[j])])
#                     successor = last_clusters[j]
#                     while j >= 0 and last_clusters[j] == successor:
#                         j -= 1
#                 else:
#                     break
#
#             while j >= 0 and current_line[j] == current_cluster:
#                 j -= 1
#
#         last_clusters = [new_cluster or old_cluster for new_cluster, old_cluster in zip(current_line, last_clusters)]
#     return vertex_height