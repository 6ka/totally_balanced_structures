__author__ = 'fbrucker'

__all__ = ["hierarchical_height_from_lattice"]
import DLC.lattice


def unique_successor_decomposition(dismantable_lattice):
    cover_graph = dismantable_lattice.copy()
    dual_cover_graph = cover_graph.dual()

    maxima = [DLC.lattice.get_top(cover_graph)]
    current_height = 0
    height = {maxima[0]: current_height}

    while maxima:
        new_maxima = []
        for vertex in maxima:
            pile = [vertex]
            while pile:
                father = pile.pop()
                for current in dual_cover_graph[father]:
                    if cover_graph.degree(current) == 1:
                        height[current] = current_height
                        cover_graph.update([(current, father)])
                        dual_cover_graph.update([(father, current)])
                        pile.append(current)
                    elif cover_graph.degree(current) > 1:
                        new_maxima.append(father)

        current_height += 1
        maxima = new_maxima

    return height

def hierarchical_height_from_lattice(dismantable_lattice):

    vertex_height = dict()
    current_height = 0
    next_neighbor = dict()
    current_degree = {x: dismantable_lattice.degree(x) for x in dismantable_lattice}
    sup_irreducibles = set(DLC.lattice.sup_irreducible(dismantable_lattice))
    dual_lattice = dismantable_lattice.dual()
    while sup_irreducibles:
        current_chains = set()
        deleted_sup_irreducibles = set()
        for current_sup_irreducible in sup_irreducibles:
            possible_chain = set()
            vertex = current_sup_irreducible
            is_hierarchical = False
            while current_degree[vertex] <= 1:
                possible_chain.add(vertex)
                if current_degree[vertex] == 0 or vertex in current_chains:
                    is_hierarchical = True
                    break
                vertex = next_neighbor.get(vertex, dismantable_lattice[vertex][0])
            if is_hierarchical:
                deleted_sup_irreducibles.add(current_sup_irreducible)
                current_chains.update(possible_chain)

        for x in current_chains:
            vertex_height[x] = current_height
            for y in dual_lattice[x]:
                current_degree[y] -= 1
                if current_degree[y] == 1:
                    for z in dismantable_lattice[y]:
                        if z not in vertex_height:
                            next_neighbor[y] = z
                            break
        current_height += 1

        sup_irreducibles.difference_update(deleted_sup_irreducibles)
    return vertex_height