__author__ = 'fbrucker'

__all__ = ["hierarchical_height_from_lattice"]
import DLC.lattice


def hierarchical_height_from_lattice(dismantable_lattice, bottom=None):
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