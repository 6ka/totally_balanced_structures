__author__ = 'fbrucker'

__all__ = ["hierarchical_height_from_lattice"]
import DLC.lattice


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


def hierarchical_height_from_lattice_old(dismantable_lattice, bottom=None):
    #there is a bug....
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